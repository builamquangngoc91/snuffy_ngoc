import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class FeatureDataset(Dataset):
    def __init__(self, feature_file, transform=None):
        self.feature_file = feature_file
        self.transform = transform
        with h5py.File(feature_file, 'r') as f:
            self.features = f['features'][:]  

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        x = self.features[index]
        x = torch.tensor(x, dtype=torch.float)
        if self.transform is not None:
            x = self.transform(x)
        return [x, x], 0