# anomaly_detection.py

import pandas as pd
import torch
import threading
from scipy.signal import savgol_filter
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import numpy as np


use_gpu = False
device  = torch.device("cuda:0" if use_gpu and torch.cuda.is_available() else "cpu")


def elbo_loss(recon_x, x, mu, logvar, kld_weight=1):
    reconstruction_function = nn.MSELoss(reduction='sum')
    recons_loss = torch.mean(reconstruction_function(recon_x, x))
    kld_loss = torch.mean(-0.5 * torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1), dim=0)
    loss = recons_loss + kld_weight * kld_loss
    return loss, recons_loss.detach(), -kld_loss.detach()


def get_encodings_with_loss(dataset, vae_model, batch_size):
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    encodings = []
    losses = []
    lock = threading.Lock()

    with torch.no_grad():
        for batch in dataloader:
            if batch is not None:
                batch = batch.to(device).float()
                x_recon, z_mean, z_log_var = vae_model(batch)
                encodings.extend(z_mean.tolist())
                loss, recons_loss, kld_loss = elbo_loss(x_recon, batch, z_mean, z_log_var)
                with lock:
                    losses.append({'batch': len(losses), 'ELBO_loss': loss.item(),
                                   'reconstruction_loss': recons_loss.item(),
                                   'KLD_loss': kld_loss.item()})

    loss_df = pd.DataFrame(losses)
    return encodings, loss_df

def create_encodings_dataframe(encodings, num_features):
    columns = [f"feature_{i}" for i in range(num_features)]
    df_encodings = pd.DataFrame(encodings, columns=columns)
    return df_encodings

class LSTMTrainingDataset(Dataset):
    def __init__(self, data, seq_length):
        self.data = data
        self.seq_length = seq_length
        self.num_rows = len(data)

    def __getitem__(self, index):
        end_index = index + self.seq_length

        if end_index >= self.num_rows:
            raise IndexError("Invalid index. End of sequence exceeds DataFrame size.")

        sequence = self.data.iloc[index:end_index].values
        target = self.data.iloc[end_index].values

        if np.isnan(sequence).any() or np.isnan(target).any():
            raise ValueError(f"Skipping sequence starting at index {index} due to NaN values.")

        input_seq = torch.from_numpy(sequence).float()
        target = torch.from_numpy(target).float()

        return input_seq, target

    def __len__(self):
        return self.num_rows - self.seq_length

def get_lstm_loss(dataset, lstm_model, batch_size):
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    criterion  = nn.MSELoss()

    losses = []
    lock = threading.Lock()

    with torch.no_grad():
        for input_seq, target in dataloader:
            outputs = lstm_model(input_seq)
            loss = criterion(outputs, target)
            with lock:
                losses.append({'batch': len(losses), 'LSTM_loss': loss.item()})

    loss_df = pd.DataFrame(losses)
    return loss_df

def detect_outliers(data, window_length=51, polyorder=3, threshold=1.5):
    mu_values = [0.25, 0.5, 0.75]
    smoothed_trend = {}
    outliers = {}

    for mu in mu_values:
        combined_loss = mu * data['ELBO_loss'] + (1 - mu) * data['LSTM_loss']
        smoothed = savgol_filter(combined_loss, window_length, polyorder)
        smoothed_trend[mu] = smoothed
        std_dev = np.std(combined_loss - smoothed)
        outliers[mu] = np.abs(combined_loss - smoothed) > threshold * std_dev

    return {
        'smoothed_trend': smoothed_trend,
        'outliers': outliers
    }

def identify_anomalous_batches(data, outliers):
    anomalous_batches = {}

    for mu, mask in outliers.items():
        anomalous_batches[mu] = data.loc[mask, 'batch'].tolist()

    return anomalous_batches