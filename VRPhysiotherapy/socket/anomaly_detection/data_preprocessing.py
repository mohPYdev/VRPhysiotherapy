# data_preprocessing.py

import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import ast


class MyDataset(Dataset):
    def __init__(self, folder_path, window_size):
        self.folder_path = folder_path
        self.window_size = window_size
        self.data, self.indices = self.load_csv_files()
        self.num_rows, self.num_features = self.data.shape

    def convert_string_to_list(self, string):
        return ast.literal_eval(string)

    def load_csv_files(self):
        files = sorted([f for f in os.listdir(self.folder_path) if f.endswith('.csv')])
        all_data, indices = [], []
        current_index = 0

        for filename in files:
            df = pd.read_csv(os.path.join(self.folder_path, filename))
            preprocessed_rows = []
            for _, row in df.iterrows():
                all_features = []
                for item in row:
                    if isinstance(item, str):
                        try:
                            item = self.convert_string_to_list(item)
                        except (ValueError, SyntaxError):
                            continue
                    all_features.extend(item if isinstance(item, list) else [item])
                preprocessed_rows.append(all_features)

            preprocessed_df = pd.DataFrame(preprocessed_rows)
            all_data.append(preprocessed_df)
            current_index += len(preprocessed_df)
            indices.append(current_index)

        concatenated_data = pd.concat(all_data, ignore_index=True)
        return concatenated_data, indices

    def __getitem__(self, global_index):
        file_index = next((i for i, idx in enumerate(self.indices) if idx > global_index), -1)

        if file_index == -1:
            return None  # Global index out of the range of provided indices

        if file_index > 0:
            local_index = global_index - self.indices[file_index - 1]
        else:
            local_index = global_index

        if local_index + self.window_size > (self.indices[file_index] - self.indices[file_index - 1] if file_index > 0 else self.indices[file_index]):
            return None  # This window would span across different files or out of current file's range

        window = self.data.iloc[global_index:global_index + self.window_size].values

        if np.isnan(window).any():
            return None  # Skip windows containing NaN values

        return torch.from_numpy(window)

    def __len__(self):
        # Count only valid windows across all files by considering file boundaries
        valid_ranges = sum(max(0, (idx - self.indices[i - 1] if i > 0 else idx) - self.window_size + 1) for i, idx in enumerate(self.indices))
        return valid_ranges

def custom_collate_fn(batch):
    batch = [item for item in batch if item is not None]
    if len(batch) == 0:
        return None  # Return None to indicate an empty batch
    return torch.utils.data.dataloader.default_collate(batch)

def create_dataloader(dataset, batch_size, shuffle, num_workers):
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, collate_fn=custom_collate_fn, num_workers=num_workers)