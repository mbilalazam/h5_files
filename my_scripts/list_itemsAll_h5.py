""" 
The script is designed to list the names of all items (groups and datasets) contained within a specific h5 file.
Author: Muhammad Bilal Azam
"""

import h5py

def list_names(name, obj):
    """Callback function for h5py's visititems method."""
    print(name)

def print_all_names_in_h5_file(filename):
    with h5py.File(filename, 'r') as f:
        f.visititems(list_names)

if __name__ == "__main__":
    filename = "MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5"
    print_all_names_in_h5_file(filename)


