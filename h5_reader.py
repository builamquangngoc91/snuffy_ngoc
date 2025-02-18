#!/usr/bin/env python3
import h5py
import argparse
import numpy as np

def read_h5_file(file_path):
    with h5py.File(file_path, 'r') as hf:
        data_dict = {}
        
        data_dict['coordinates'] = hf['coordinates'][:]
        data_dict['features'] = hf['features'][:]
        data_dict['label'] = hf['label'][:]
        data_dict['patch_indices'] = hf['patch_indices'][:]
        data_dict['spixel_idx'] = hf['spixel_idx'][:]

        print(data_dict['features'][0])
        print(data_dict['patch_indices'])
        coordinates = data_dict['coordinates'][:]


        return data_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read an H5 file and display a preview of its datasets.")
    parser.add_argument('file_path', type=str, help="Path to the H5 file")
    args = parser.parse_args()

    read_h5_file(args.file_path)