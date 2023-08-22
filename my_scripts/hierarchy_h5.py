"""
The given script is used to display the structure of an HDF5 (Hierarchical Data Format version 5) file. The hierarchical nature of HDF5 files means they can contain datasets and groups, and these groups can further contain datasets or sub-groups, and so on. This script will print this hierarchy.
Author: Muhammad Bilal Azam
"""

import h5py

def print_h5_item_structure(g, offset='    '):
    """Prints the input file/group/dataset (g) name and begin iterations on its content"""
    if isinstance(g, h5py.File):
        print(g.file, '(File)', g.name)
    elif isinstance(g, h5py.Dataset):
        print('(Dataset)', g.name, '    len =', g.shape) # shape gives dimensions
    elif isinstance(g, h5py.Group):
        print('(Group)', g.name)

    if 'keys' in dir(g):
        for key in g.keys():
            subg = g[key]
            print(offset, key, ":", end=' ')
            print_h5_item_structure(subg, offset + '    ')

filename = 'MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5' # The name of your h5 file
with h5py.File(filename, 'r') as f:
    print_h5_item_structure(f)
