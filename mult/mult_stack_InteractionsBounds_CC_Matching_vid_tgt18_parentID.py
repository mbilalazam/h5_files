"""
Date: September 06, 2023
Author: Muhammad Bilal Azam
Structure of this code is as follows:
1. Loop over traj_id from Stack
2. Set part_status to 1 from Stack
3. Set isCC to TRUE from interactions.
4. Apply bounds for FV from interactions.
5. This script first extracts the vertex data from the interactions dataset and applies the given bounds to filter the vertex_id values. It then matches these vertex_id values with the stack dataset
6. Set target to 18 (argon).
7. Select events for which parent_id is equal to -1.
8. Collect vertex_id from Stack
9. Make an array of part_pdg corresponding to vertex_id from Stack
10. Count the elements in part_pdg array and plot histogram of the multiplicity
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

# Define bounds
Xnegbound, Xposbound = -67, +67
Ynegbound, Yposbound = -328, -201
Znegbound, Zposbound = +1233, +1367

base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW"
filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW.h5" for i in range(1024)]

pdg_counts = []

for idx, filename in enumerate(filenames):
    with h5py.File(filename, 'r') as f:
        print(f"File {idx+1}/{len(filenames)}: {filename.split('/')[-1]}")
        
        # Extract the isCC data, vertex data, target, and corresponding vertex_id from interactions dataset
        isCC_mask = f['/mc_truth/interactions/data']['isCC'][:]
        vertex_data = f['/mc_truth/interactions/data']['vertex'][:]
        target_data = f['/mc_truth/interactions/data']['target'][:]
        vertex_id_interactions = f['/mc_truth/interactions/data']['vertex_id'][:]
        
        # Apply bounds on vertex data
        bounds_mask = (vertex_data[:, 0] >= Xnegbound) & (vertex_data[:, 0] <= Xposbound) & \
                      (vertex_data[:, 1] >= Ynegbound) & (vertex_data[:, 1] <= Yposbound) & \
                      (vertex_data[:, 2] >= Znegbound) & (vertex_data[:, 2] <= Zposbound)
        
        # Filter vertex_id values where isCC is true, within bounds, and target is 18
        valid_mask = isCC_mask & bounds_mask & (target_data == 18)
        cc_vertex_ids = vertex_id_interactions[valid_mask]
        
        # Extract traj_id and parent_id from trajectories dataset
        traj_id_trajectories = f['/mc_truth/trajectories/data']['traj_id'][:]
        parent_id_trajectories = f['/mc_truth/trajectories/data']['parent_id'][:]
        
        # Filter traj_id where parent_id is -1
        valid_traj_ids = traj_id_trajectories[parent_id_trajectories == -1]
        
        # Extract data from stack dataset
        traj_id_stack = f['/mc_truth/stack/data']['traj_id'][:]
        part_status = f['/mc_truth/stack/data']['part_status'][:]
        vertex_id_stack = f['/mc_truth/stack/data']['vertex_id'][:]
        part_pdg = f['/mc_truth/stack/data']['part_pdg'][:]
        
        # Create a mask for traj_id values in the stack dataset that match valid traj_ids from trajectories
        traj_id_mask = np.isin(traj_id_stack, valid_traj_ids)
        
        for vid in cc_vertex_ids:
            mask = (vertex_id_stack == vid) & (part_status == 1) & traj_id_mask
            current_pdgs = part_pdg[mask]
            pdg_counts.append(len(current_pdgs))
            
            #if vid in cc_vertex_ids[:20]:
                #print(f"vertex_id: {vid}; part_pdg: {list(current_pdgs)}; count: {len(current_pdgs)}")

# Plotting histogram
entries = len(pdg_counts)
mean = np.mean(pdg_counts)
std_dev = np.std(pdg_counts)
label_text = f"Entries: {entries}\nMean: {mean:.2f}\nStd Dev: {std_dev:.2f}"

# Set bin edges explicitly for integer alignment
bins = [i-0.5 for i in range(1, 22)]

plt.hist(pdg_counts, bins=bins, label=label_text, align='left')
plt.xlabel('CC Multiplicity (Matching vertex_id within FV; Z = 18 and parentID = -1)')
plt.ylabel('Number of Events')
plt.title('Multiplicity Distribution (Minirun4_RHC)')
plt.xticks(range(1, 21))
plt.xlim(0.5, 20.5)
plt.legend(loc='upper right')
plt.savefig("mult_stack_InteractionsBounds_CC_Matching_vid_tgt18_parentID.png", dpi=300)
plt.show()
