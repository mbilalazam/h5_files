"""
Date: September 07, 2023
Author: Muhammad Bilal Azam
Conditions of the code:
1. Loop over each file in the `filenames` list.
2. Within each file, loop over `traj_id` from the Stack dataset.
3. Set `part_status` to 1 and filter data where `parent_id` from the Trajectories dataset is -1.
4. For each unique `vertex_id` in the filtered data, extract corresponding `part_pdg` values from the Stack dataset.
5. Count the number of `part_pdg` values for each `vertex_id`.
6. Plot a histogram of the multiplicity using the counts of `part_pdg` values.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW"
filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW.h5" for i in range(1024)]

pdg_counts = []

for idx, file in enumerate(filenames):
    print(f"File {idx + 1}/{len(filenames)}: {file.split('/')[-1]}")
    
    with h5py.File(file, 'r') as f:
        stack_data = f['/mc_truth/stack/data']
        trajectories_data = f['/mc_truth/trajectories/data']
        
        traj_ids_stack = stack_data['traj_id'][:]
        part_statuses = stack_data['part_status'][:]
        vertex_ids = stack_data['vertex_id'][:]
        part_pdgs = stack_data['part_pdg'][:]
        
        traj_ids_trajectories = trajectories_data['traj_id'][:]
        parent_ids_trajectories = trajectories_data['parent_id'][:]
        
        # Filter based on part_status and parent_id from trajectories
        valid_traj_ids = traj_ids_trajectories[parent_ids_trajectories == -1]
        mask = (part_statuses == 1) & np.isin(traj_ids_stack, valid_traj_ids)
        filtered_traj_ids = traj_ids_stack[mask]
        filtered_vertex_ids = vertex_ids[mask]
        filtered_part_pdgs = part_pdgs[mask]
        
        # Group by vertex_id and append all part_pdg values
        for unique_vertex_id in np.unique(filtered_vertex_ids):
            vertex_mask = filtered_vertex_ids == unique_vertex_id
            pdg_array = filtered_part_pdgs[vertex_mask]
            count = len(pdg_array)
            pdg_counts.append(count)
            
            # Print the first traj_id for the given vertex_id
            traj_id_for_vertex = filtered_traj_ids[vertex_mask][0]
            parent_id_for_traj = parent_ids_trajectories[np.where(traj_ids_trajectories == traj_id_for_vertex)[0][0]]
            #print(f"traj_id = {traj_id_for_vertex}; part_status = 1; vertex_id = {unique_vertex_id}; part_pdg = {list(pdg_array)}; count = {count}; parent_id = {parent_id_for_traj}")

# Plot histogram
entries = len(pdg_counts)
mean = np.mean(pdg_counts)
std_dev = np.std(pdg_counts)
label_text = f"Entries: {entries}\nMean: {mean:.2f}\nStd Dev: {std_dev:.2f}"

plt.hist(pdg_counts, bins=range(1, 21), label=label_text)
plt.xlabel('Multiplicity')
plt.ylabel('Number of Events')
plt.title('Multiplicity Distribution (MiniRun4_RHC)')
plt.xticks(range(1, 21))  # Ensures that every integer between 1 and 21 inclusive is shown
plt.xlim(1, 21)  # Set x-axis limits from 1 to 21
plt.legend(loc='upper right')  # Add statbox to the histogram
plt.savefig("mult_ParentID_noBounds.png")
plt.show()
