import h5py
import os
import argparse

def read_h5_files(folder_path):
    """
    Read all H5 files from the specified folder
    
    Args:
        folder_path (str): Path to folder containing H5 files
        
    Returns:
        list: List of loaded H5 file objects
    """
    h5_files = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder {folder_path} does not exist")
    
    data_dict = {}
    # Get all .h5 files in folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.h5'):
            file_path = os.path.join(folder_path, filename)

            
            with h5py.File(file_path, "r") as f:
                basename = filename.split('.')[0]
                # Initialize an entry for basename if it doesn't exist
                data_dict[basename] = f['features'][:].shape[0]

                
    return data_dict


def write_to_csv(data_dict):
    with open('f5_features.csv', 'w') as f:
        for key, value in data_dict.items():
            f.write(f"{key},{value}\n")

def __main__():
    parser = argparse.ArgumentParser(description='Process H5 files from a folder')
    parser.add_argument('--folder_path', type=str, help='Path to folder containing H5 files')
    args = parser.parse_args()
    folder_path = args.folder_path

    data_dict = read_h5_files(folder_path)
    write_to_csv(data_dict)


if __name__ == "__main__":
    __main__()