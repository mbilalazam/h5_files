"""
Date: September 07, 2023
Author: Muhammad Bilal Azam
Description: This script processes particle interaction data to generate a histogram of multiplicity based on specific conditions and interaction modes.

Conditions of the code:
1. Loop over each file in the `filenames` list.
2. Define spatial bounds for `xyz_start` values from the Trajectories dataset.
3. Within each file, loop over `traj_id` from the Stack dataset.
4. Apply the spatial bounds on `xyz_start` values and filter data where `parent_id` from the Trajectories dataset is -1.
5. Set `part_status` to 1 and filter data based on the valid `traj_ids` within the spatial bounds.
6. For each unique `vertex_id` in the filtered data, extract corresponding `part_pdg` values from the Stack dataset.
7. Count the number of `part_pdg` values for each `vertex_id`.
8. Only select events where `isCC` is `True` and `target` is 18 (liquid argon).
9. Filter events based on specific interaction modes: QES, RES, DIS, COH, and MEC.
10. Plot a stacked histogram of the multiplicity using the counts of `part_pdg` values for each interaction mode.
"""


import h5py
import numpy as np
import matplotlib.pyplot as plt

base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW"
filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW.h5" for i in range(1024)]

# Define bounds
Xnegbound, Xposbound = -67, +67
Ynegbound, Yposbound = -328, -201
Znegbound, Zposbound = +1233, +1367

interaction_types = ['isQES', 'isRES', 'isDIS', 'isCOH', 'isMEC']
colors = {'isQES': 'black', 'isMEC': 'magenta', 'isRES': 'red', 'isDIS': 'blue', 'isCOH': 'green'}
pdg_counts_modes = {mode: [] for mode in interaction_types}

for idx, file in enumerate(filenames):
    print(f"File {idx + 1}/{len(filenames)}: {file.split('/')[-1]}")
    
    with h5py.File(file, 'r') as f:
        stack_data = f['/mc_truth/stack/data']
        trajectories_data = f['/mc_truth/trajectories/data']
        interactions_data = f['/mc_truth/interactions/data']

        # Extract vertex_id, interaction modes, isCC values, and target values from the interactions dataset
        interactions_vertex_ids = interactions_data['vertex_id'][:]
        isCC_values = interactions_data['isCC'][:]
        target_values = interactions_data['target'][:]
        interaction_modes = {mode: interactions_data[mode][:] for mode in interaction_types}
        
        # Create dictionaries mapping vertex_id to its isCC value, target value, and interaction modes
        vertex_id_to_isCC = dict(zip(interactions_vertex_ids, isCC_values))
        vertex_id_to_target = dict(zip(interactions_vertex_ids, target_values))
        vertex_id_to_modes = {mode: dict(zip(interactions_vertex_ids, interaction_modes[mode])) for mode in interaction_types}
        
        traj_ids_stack = stack_data['traj_id'][:]
        part_statuses = stack_data['part_status'][:]
        vertex_ids = stack_data['vertex_id'][:]
        part_pdgs = stack_data['part_pdg'][:]
        
        traj_ids_trajectories = trajectories_data['traj_id'][:]
        parent_ids_trajectories = trajectories_data['parent_id'][:]
        xyz_starts = trajectories_data['xyz_start'][:]
        
        # Apply bounds on xyz_start
        bounds_mask = (xyz_starts[:, 0] >= Xnegbound) & (xyz_starts[:, 0] <= Xposbound) & \
                      (xyz_starts[:, 1] >= Ynegbound) & (xyz_starts[:, 1] <= Yposbound) & \
                      (xyz_starts[:, 2] >= Znegbound) & (xyz_starts[:, 2] <= Zposbound)
        
        valid_traj_ids = traj_ids_trajectories[(parent_ids_trajectories == -1) & bounds_mask]
        
        # Filter based on part_status and valid traj_ids
        mask = (part_statuses == 1) & np.isin(traj_ids_stack, valid_traj_ids)
        filtered_traj_ids = traj_ids_stack[mask]
        filtered_vertex_ids = vertex_ids[mask]
        filtered_part_pdgs = part_pdgs[mask]
        
        # Group by vertex_id and append all part_pdg values
        for unique_vertex_id in np.unique(filtered_vertex_ids):
            # Extract the isCC value, target value, and interaction modes for the current vertex_id from the dictionaries
            isCC_for_vertex = vertex_id_to_isCC.get(unique_vertex_id, False)  # Default to False if vertex_id not found
            target_for_vertex = vertex_id_to_target.get(unique_vertex_id, 0)  # Default to 0 if vertex_id not found
            modes_for_vertex = {mode: vertex_id_to_modes[mode].get(unique_vertex_id, False) for mode in interaction_types}
            
            # Only process vertices where isCC is True and target is 18
            if isCC_for_vertex and target_for_vertex == 18:
                vertex_mask = filtered_vertex_ids == unique_vertex_id
                pdg_array = filtered_part_pdgs[vertex_mask]
                count = len(pdg_array)
                
                # Append to the respective interaction mode's list if the mode is True for the vertex
                for mode in interaction_types:
                    if modes_for_vertex[mode]:
                        pdg_counts_modes[mode].append(count)
                
                # Print the traj_id, part_pdg values, count, parent_id, isCC value, target value, and interaction modes for the given vertex_id
                traj_id_for_vertex = filtered_traj_ids[vertex_mask][0]
                parent_id_for_traj = parent_ids_trajectories[np.where(traj_ids_trajectories == traj_id_for_vertex)[0][0]]
                #print(f"traj_id = {traj_id_for_vertex}; part_status = 1; vertex_id = {unique_vertex_id}; part_pdg = {list(pdg_array)}; count = {count}; parent_id = {parent_id_for_traj}; isCC = {isCC_for_vertex}; target = {target_for_vertex}; modes = {[mode[2:] for mode in interaction_types if modes_for_vertex[mode]]}")

# Plot stacked histogram
bins = range(1, 21)
total_counts = sum([len(pdg_counts_modes[mode]) for mode in interaction_types])
plt.hist([pdg_counts_modes[mode] for mode in interaction_types], bins=bins, stacked=True, color=[colors[mode] for mode in interaction_types], edgecolor='black', label=[f"{mode[2:]} ({len(pdg_counts_modes[mode])}, {len(pdg_counts_modes[mode])/total_counts*100:.2f}%)" for mode in interaction_types])
plt.xlabel('CC Multiplicity')
plt.ylabel('Number of Events')
plt.title('Multiplicity Distribution (MiniRun4_RHC) by Interaction Modes')
plt.xticks(bins)  # Ensures that every integer between 1 and 21 inclusive is shown
plt.xlim(1, 21)  # Set x-axis limits from 1 to 21
plt.legend(loc='upper right')  # Add legend to the histogram
plt.savefig("mult_parentID_Bounds_CC_tgt18_mode.png")
plt.show()
