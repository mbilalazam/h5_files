""" 
This script is to inspect and print out the names and datatypes of datasets contained within a specified HDF5 file.
Author: Muhammad Bilal Azam
"""

import h5py

def inspect_dataset(dataset):
    """Print dataset name and datatype."""
    print(f"Dataset: {dataset.name}")
    print(f"    Datatype: {dataset.dtype}")

def inspect_h5_file(filename):
    with h5py.File(filename, 'r') as f:
        def explore(name, obj):
            if isinstance(obj, h5py.Dataset):
                inspect_dataset(obj)

        f.visititems(explore)

if __name__ == "__main__":
    filename = "MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5"
    inspect_h5_file(filename)


