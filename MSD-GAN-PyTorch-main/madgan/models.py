from pathlib import Path
from typing import Optional, Protocol, Union
from madgan.wavenet import WaveNet
import torch
import torch.nn as nn


class SerializableModule(Protocol):

    def save(self, fpath: Union[str, Path]) -> None:
        ...

    @classmethod
    def from_pretrained(
            cls, fpath: Union[str, Path],
            map_location: Optional[torch.device]) -> "SerializableModule":
        ...


class Generator(nn.Module):

    def __init__(self,
                 latent_space_dim: int,
                 hidden_units: int,
                 output_dim: int,
                 n_lstm_layers: int = 2) -> None:
        super().__init__()
        self.latent_space_dim = latent_space_dim
        self.hidden_units = hidden_units
        self.n_lstm_layers = n_lstm_layers
        self.output_dim = output_dim

        self.lstm = nn.LSTM(input_size=self.latent_space_dim,
                            hidden_size=self.hidden_units,
                            num_layers=self.n_lstm_layers,
                            batch_first=True,
                            dropout=.1)

        self.linear = nn.Linear(in_features=self.hidden_units,
                                out_features=self.output_dim)
        
        # Initialize weights with Xavier Uniform initialization
        self.init_weights()

    def init_weights(self):
        # Initialize LSTM weights
        for name, param in self.lstm.named_parameters():
            if 'weight_ih' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'weight_hh' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'bias' in name:
                param.data.fill_(0)

        # Initialize linear layer weights
        nn.init.xavier_uniform_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rnn_output, _ = self.lstm(x)
        return self.linear(rnn_output)

    def save(self, fpath: Union[Path, str]) -> None:
        chkp = {
            "config": {
                "latent_space_dim": self.latent_space_dim,
                "hidden_units": self.hidden_units,
                "n_lstm_layers": self.n_lstm_layers,
                "output_dim": self.output_dim
            },
            "weights": self.state_dict(),
        }
        torch.save(chkp, fpath)

    @classmethod
    def from_pretrained(
            cls,
            fpath: Union[Path, str],
            map_location: Optional[torch.device] = None) -> "Generator":
        chkp = torch.load(fpath, map_location=map_location)
        model = cls(**chkp.pop("config"))
        model.load_state_dict(chkp.pop("weights"))
        model.eval()
        return model


class GeneratorWithWaveNet(nn.Module):
    def __init__(self, latent_space_dim: int, output_dim: int, kernel_size: int, stack_size: int, layer_size: int) -> None:
        super().__init__()
        self.latent_space_dim = latent_space_dim
        self.output_dim = output_dim
        self.kernel_size = kernel_size
        self.stack_size = stack_size
        self.layer_size = layer_size

        # Configuring WaveNet with the given parameters
        self.wavenet = WaveNet(in_channels=latent_space_dim,
                               out_channels=output_dim,
                               kernel_size=kernel_size,
                               stack_size=stack_size,
                               layer_size=layer_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Assuming x has dimensions [batch, channels, sequence length]
        # WaveNet expects a 3D Tensor (batch_size, num_channels, length_of_sequence)
        return self.wavenet(x)
    
    
    def save(self, fpath: Union[Path, str]) -> None:
        """Saves the model's configuration and weights to the specified path."""
        chkp = {
            "config": {
                "latent_space_dim": self.latent_space_dim,
                "output_dim": self.output_dim,
                "kernel_size": self.kernel_size,
                "stack_size": self.stack_size,
                "layer_size": self.layer_size
            },
            "weights": self.state_dict(),
        }
        torch.save(chkp, fpath)

    @classmethod
    def from_pretrained(
            cls,
            fpath: Union[Path, str],
            map_location: Optional[torch.device] = None) -> "GeneratorWithWaveNet":
        """Loads a pretrained model from the specified path."""
        chkp = torch.load(fpath, map_location=map_location)
        model = cls(**chkp.pop("config"))
        model.load_state_dict(chkp.pop("weights"))
        model.eval()  # Set the model to evaluation mode
        return model


class Discriminator(nn.Module):

    def __init__(self,
                 input_dim: int,
                 hidden_units: int,
                 n_lstm_layers: int = 2,
                 add_batch_mean: bool = False) -> None:
        super().__init__()
        self.add_batch_mean = add_batch_mean
        self.hidden_units = hidden_units
        
        self.input_dim = 2 * input_dim if self.add_batch_mean else input_dim

        self.n_lstm_layers = n_lstm_layers

        extra_features = self.hidden_units if self.add_batch_mean else 0
        self.lstm = nn.LSTM(input_size=self.input_dim,
                            hidden_size=self.hidden_units + extra_features,
                            num_layers=self.n_lstm_layers,
                            batch_first=True,
                            dropout=.1)

        self.linear = nn.Linear(in_features=self.hidden_units + extra_features,
                                out_features=1)
        
        self.init_weights()

        self.activation = nn.Sigmoid()

    def init_weights(self):
        # Initialize LSTM weights
        for name, param in self.lstm.named_parameters():
            if 'weight_ih' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'weight_hh' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'bias' in name:
                param.data.fill_(0)

        # Initialize linear layer weights
        nn.init.xavier_uniform_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.add_batch_mean:
            bs = x.size(0)
            batch_mean = x.mean(0, keepdim=True).repeat(bs, 1, 1)
            x = torch.cat([x, batch_mean], dim=-1)

        rnn_output, _ = self.lstm(x)
        last_output = rnn_output[:, -1, :]
        return self.activation(self.linear(last_output))

    def save(self, fpath: Union[Path, str]) -> None:
        chkp = {
            "config": {
                "add_batch_mean": self.add_batch_mean,
                "hidden_units": self.hidden_units,
                "input_dim": self.input_dim,
                "n_lstm_layers": self.n_lstm_layers
            },
            "weights": self.state_dict(),
        }
        torch.save(chkp, fpath)

    @classmethod
    def from_pretrained(
            cls,
            fpath: Union[Path, str],
            map_location: Optional[torch.device] = None) -> "Discriminator":
        chkp = torch.load(fpath, map_location=map_location)
        model = cls(**chkp.pop("config"))
        model.load_state_dict(chkp.pop("weights"))
        model.eval()
        return model
