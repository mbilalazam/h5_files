"""
This code is to print the datasets and data types in tabulated form. It caters to datasets with both compound and simple datatypes within the HDF5 file.
Author: Muhammad Bilal Azam
"""
import h5py

def print_dtype_in_tabulated_form(dtype):
    """Print the dtype in a tabulated form."""
    # Check if the dtype is compound (structured)
    if dtype.names:
        names = dtype.names
        formats = [dtype.fields[name][0] for name in names]
        offsets = [dtype.fields[name][1] for name in names]

        # Print table header for compound dtypes
        print("\nNames           Formats    Offsets")
        print("-----------------------------------")
        
        # Print each row for compound dtypes
        for name, fmt, offset in zip(names, formats, offsets):
            print(f"{name:<15} {fmt!s:<10} {offset}")
    else:
        # Handle non-compound dtypes
        print(f"\nDatatype: {dtype}")

def inspect_dataset(dataset):
    """Print dataset name and datatype in tabulated form."""
    print(f"\nDataset: {dataset.name}")
    print_dtype_in_tabulated_form(dataset.dtype)

def inspect_h5_file(filename):
    with h5py.File(filename, 'r') as f:
        def explore(name, obj):
            if isinstance(obj, h5py.Dataset):
                inspect_dataset(obj)
                
        f.visititems(explore)

if __name__ == "__main__":
    filename = "MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5"
    inspect_h5_file(filename)
