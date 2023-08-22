"""
This script is to display the hierarchical structure of an HDF5 file. HDF5 files can contain both datasets (essentially data arrays) and groups (which can be seen as directories or folders containing datasets or other sub-groups). The script provides a visual representation of the file's contents, indicating groups and datasets in an indented manner to represent the hierarchy.
Author: Muhammad Bilal Azam
"""

import h5py

def print_h5_structure(h5_object, level=0):
    """Recursively print the structure of the h5 object."""
    for key in h5_object.keys():
        print("  " * level + f"Group Name: {key}")

        if isinstance(h5_object[key], h5py.Group):
            print_h5_structure(h5_object[key], level + 1)

        elif isinstance(h5_object[key], h5py.Dataset):
            print("  " * (level + 1) + f"Dataset Name: {key}")

with h5py.File("MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5", "r") as h5_file:
    print("=== HDF5 Structure ===")
    print_h5_structure(h5_file)
