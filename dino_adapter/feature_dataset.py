import os
import torch
from torch.utils.data import Dataset
import h5py
import numpy as np

class FeatureDataset(Dataset):
    def __init__(self, feature_dir, transform=None):
        self.transform = transform
        self.feature_files = []
        self.labels = []
        
        # Recursively find all .h5 files in subdirectories
        for root, _, files in os.walk(feature_dir):
            for f in files:
                if f.endswith('.h5'):
                    self.feature_files.append(os.path.join(root, f))
                    # Get label from parent directory name (0_normal -> 0, 1_tumor -> 1)
                    parent_dir = os.path.basename(root)
                    label = int(parent_dir.split('_')[0])
                    self.labels.append(label)

        print(f'feature_dir: {feature_dir}')
        print(f'Found {len(self.feature_files)} feature files')
        print(f'Labels distribution: {np.bincount(self.labels)}')
        
        if not self.feature_files:
            raise ValueError("No .h5 files found in the provided directory or its subdirectories")

        # Load all features into memory
        self.features = []
        for h5_file in self.feature_files:
            with h5py.File(h5_file, 'r') as f:
                self.features.append(f['features'][:])
        self.features = np.concatenate(self.features, axis=0)
        self.labels = np.repeat(self.labels, [len(f) for f in self.features])

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        x = self.features[index]
        label = self.labels[index]
        x = torch.tensor(x, dtype=torch.float)
        if self.transform is not None:
            x = self.transform(x)
        return [x, x], label