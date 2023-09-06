"""
Date: September 06, 2023
Author: Muhammad Bilal Azam
Structure of this code is as follows:
1. Loop over traj_id from Stack
2. Set part_status to 1 from Stack
3. Set isCC to TRUE from interactions (it does not check for matching vertex_id from stack and interactions datasets)
That is, it determines the minimum length between traj_id and isCC_mask and then loop only up to that length.
3. Collect vertex_id from Stack
4. Make an array of part_pdg corresponding to vertex_id from Stack
5. Count the elements in part_pdg array and plot histogram of the multiplicity
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW"
filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW.h5" for i in range(1024)]

pdg_counts = []

for idx, filename in enumerate(filenames):
    with h5py.File(filename, 'r') as f:
        print(f"File {idx+1}/{len(filenames)}: {filename.split('/')[-1]}")
        
        traj_id = f['/mc_truth/stack/data']['traj_id'][:]
        part_status = f['/mc_truth/stack/data']['part_status'][:]
        vertex_id = f['/mc_truth/stack/data']['vertex_id'][:]
        part_pdg = f['/mc_truth/stack/data']['part_pdg'][:]
        
        # Extract the isCC data
        isCC_mask = f['/mc_truth/interactions/data']['isCC'][:]
        
        # Check if the lengths are different
        min_length = min(len(traj_id), len(isCC_mask))
        
        for i in range(min_length):
            if part_status[i] == 1 and isCC_mask[i]:
                current_vertex_id = vertex_id[i]
                current_pdgs = part_pdg[vertex_id == current_vertex_id]
                pdg_counts.append(len(current_pdgs))
                
                #if i < 20:
                    #print(f"i: {i+1}; traj_id: {traj_id[i]}; part_status: {part_status[i]}; vertex_id: {vertex_id[i]}; part_pdg: {list(current_pdgs)}; count: {len(current_pdgs)}")

# Plotting histogram
entries = len(pdg_counts)
mean = np.mean(pdg_counts)
std_dev = np.std(pdg_counts)
label_text = f"Entries: {entries}\nMean: {mean:.2f}\nStd Dev: {std_dev:.2f}"

# Set bin edges explicitly for integer alignment
bins = [i-0.5 for i in range(1, 22)]

plt.hist(pdg_counts, bins=bins, label=label_text, align='left')
plt.xlabel('CC Multiplicity (no matching verte_id)')
plt.ylabel('Number of Events')
plt.title('Multiplicity Distribution (Minirun4_RHC)')
plt.xticks(range(1, 21))
plt.xlim(0.5, 20.5)
plt.legend(loc='upper right')
plt.savefig("mult_stack_noBounds_CC_noMatching_vid.png", dpi=300)
plt.show()
