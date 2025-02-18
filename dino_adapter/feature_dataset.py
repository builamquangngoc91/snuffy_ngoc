import os
import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class FeatureDataset(Dataset):
    def __init__(self, feature_dir, transform=None):
        self.transform = transform
        # List all .h5 files in the provided directory
        self.feature_files = [
            os.path.join(feature_dir, f) for f in os.listdir(feature_dir) if f.endswith('.h5')
        ]
        print(f'feature_dir: {feature_dir}')
        print(f'feature_files: {self.feature_files}')
        if not self.feature_files:
            raise ValueError("No .h5 files found in the provided directory")
        # For simplicity, let's load features from the first file
        with h5py.File(self.feature_files[0], 'r') as f:
            self.features = f['features'][:]

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        x = self.features[index]
        x = torch.tensor(x, dtype=torch.float)
        if self.transform is not None:
            x = self.transform(x)
        return [x, x], 0