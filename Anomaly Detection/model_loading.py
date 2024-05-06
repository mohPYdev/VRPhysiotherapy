# model_loading.py

import torch
import torch.nn as nn
import torch.nn.functional as F

use_gpu = False
device  = torch.device("cuda:0" if use_gpu and torch.cuda.is_available() else "cpu")

class Encoder(nn.Module):
    def __init__(self, window_length, num_features, embedding_size):
        super(Encoder, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, (3, 3), padding=1)
        self.conv2 = nn.Conv2d(16, 32, (3, 3), padding=1)
        self.pool = nn.MaxPool2d((2, 2))
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(192, 256)
        self.fc_mean = nn.Linear(256, embedding_size)
        self.fc_log_var = nn.Linear(256, embedding_size)

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        z_mean = self.fc_mean(x)
        z_log_var = self.fc_log_var(x)
        sample = self.reparameterize(z_mean, z_log_var)
        return sample, z_mean, z_log_var

    def reparameterize(self, z_mean, z_log_var):
        std = torch.exp(0.5 * z_log_var)
        eps = torch.randn_like(std)
        return eps * std + z_mean

class Trim(nn.Module):
    def __init__(self, *args):
        super().__init__()

    def forward(self, x):
        return x[:, :, :5, :24]

class Decoder(nn.Module):
    def __init__(self, window_length, num_features, embedding_size):
        super(Decoder, self).__init__()
        self.fc = nn.Linear(embedding_size, 192)
        self.unflatten = nn.Unflatten(1, (32, 1, 6))
        self.conv_trans0 = nn.ConvTranspose2d(32, 32, (3, 3), stride=2, padding=1, output_padding=1)
        self.conv_trans1 = nn.ConvTranspose2d(32, 16, (3, 3), stride=2, padding=1, output_padding=1)
        self.conv_trans2 = nn.ConvTranspose2d(16, 1, kernel_size=2, stride=1, padding=0)
        self.trim = Trim()

    def forward(self, z):
        x = F.relu(self.fc(z))
        x = self.unflatten(x)
        x = F.relu(self.conv_trans0(x))
        x = F.relu(self.conv_trans1(x))
        x = self.conv_trans2(x)
        x = self.trim(x)
        return x

class VAE(nn.Module):
    def __init__(self, window_length, num_features, embedding_size):
        super(VAE, self).__init__()
        self.encoder = Encoder(window_length, num_features, embedding_size)
        self.decoder = Decoder(window_length, num_features, embedding_size)

    def forward(self, x):
        sample, z_mean, z_log_var = self.encoder(x)
        x_recon = self.decoder(sample)
        return x_recon, z_mean, z_log_var

def load_vae_model(vae_weights_path, window_length, num_features, embedding_size):
    state_dict = torch.load(vae_weights_path)
    vae_model = VAE(window_length, num_features, embedding_size)
    vae_model.load_state_dict(state_dict)
    return vae_model

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

def load_lstm_model(lstm_weights_path, input_size, hidden_size, num_layers, output_size, device):
    state_dict = torch.load(lstm_weights_path)
    lstm_model = LSTMModel(input_size, hidden_size, num_layers, output_size).to(device)
    lstm_model.load_state_dict(state_dict)
    return lstm_model