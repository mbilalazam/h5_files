"""
The given script is used to merge the contents of /interactions and /stack into a new dataset /one and creates a new .h5 file (from .FLOW.h5 to .FLOW_MERGED.h5).
Author: Muhammad Bilal Azam
"""

import h5py
import numpy as np

# Open the input file
with h5py.File("MiniRun4_1E19_RHC.flow.00000.FLOW.h5", "r") as infile:
    
    # Extract the datasets
    interactions_data = infile["/mc_truth/interactions/data"][:]
    stack_data = infile["/mc_truth/stack/data"][:]

# Define new field names for interactions dataset
interactions_dtype = [
    ("event_id_interactions", "uint32"),
    ("vertex_id_interactions", "uint64"),
    ("vertex_interactions", "<f8", (4,)),
    ("target_interactions", "uint32"),
    ("reaction_interactions", "int32"),
    ("isCC_interactions", "bool"),
    ("isQES_interactions", "bool"),
    ("isMEC_interactions", "bool"),
    ("isRES_interactions", "bool"),
    ("isDIS_interactions", "bool"),
    ("isCOH_interactions", "bool"),
    ("Enu_interactions", "float32"),
    ("nu_4mom_interactions", "<f4", (4,)),
    ("nu_pdg_interactions", "int32"),
    ("Elep_interactions", "float32"),
    ("lep_mom_interactions", "float32"),
    ("lep_ang_interactions", "float32"),
    ("lep_pdg_interactions", "int32"),
    ("q0_interactions", "float32"),
    ("q3_interactions", "float32"),
    ("Q2_interactions", "float32"),
    ("x_interactions", "float32"),
    ("y_interactions", "float32")
]

# Define new field names for stack dataset
stack_dtype = [
    ("event_id_stack", "uint32"),
    ("vertex_id_stack", "uint64"),
    ("traj_id_stack", "int32"),
    ("part_4mom_stack", "<f4", (4,)),
    ("part_pdg_stack", "int32"),
    ("part_status_stack", "int32")
]

# Determine the merged dataset's length
merged_length = max(len(interactions_data), len(stack_data))

# Create a merged structured array with given dtypes and length
merged_data = np.zeros(merged_length, dtype=interactions_dtype + stack_dtype)

# Populate the merged_data array with interactions and stack data
for name, new_name in zip(interactions_data.dtype.names, [field[0] for field in interactions_dtype]):
    merged_data[new_name][:len(interactions_data)] = interactions_data[name]

for name, new_name in zip(stack_data.dtype.names, [field[0] for field in stack_dtype]):
    merged_data[new_name][:len(stack_data)] = stack_data[name]

# Create the new .h5 file with merged dataset
with h5py.File("MiniRun4_1E19_RHC.flow.00000.FLOW_MERGED.h5", "w") as outfile:
    dset = outfile.create_dataset("/mc_truth/one", data=merged_data)

print("Merging completed!")
