"""
Incident Neutrino Beam Energy Analysis (MiniRun4_RHC)
Author: Muhammad Bilal Azam
This script visualizes the energy distribution of neutrino events across different interaction types using a stacked histogram and within FV. 
Data is sourced from a series of HDF5 files, and the final output is saved as "enu_withBounds.png".
"""

import h5py
import matplotlib.pyplot as plt

def create_stacked_histogram(filenames, dataset_name):
    interaction_types = ['isQES', 'isRES', 'isDIS', 'isCOH', 'isMEC']
    colors = {'isQES': 'black', 'isMEC': 'magenta', 'isRES': 'red', 'isDIS': 'blue', 'isCOH': 'green'}
    
    enu_values_by_type = {itype: [] for itype in interaction_types}
    counts = {itype: 0 for itype in interaction_types}

    # Define bounds
    Xnegbound, Xposbound = -67, +67
    Ynegbound, Yposbound = -328, -201
    Znegbound, Zposbound = +1233, +1367

    for idx, filename in enumerate(filenames, 1):
        print(f"File {idx}/{len(filenames)}: {filename.split('/')[-1]}")
        with h5py.File(filename, 'r') as f:
            data = f[dataset_name]
            
            x, y, z, _ = data['vertex'][()].T
            bounds_mask = (x >= Xnegbound) & (x <= Xposbound) & \
                          (y >= Ynegbound) & (y <= Yposbound) & \
                          (z >= Znegbound) & (z <= Zposbound)
            
            for interaction_type in interaction_types:
                mask = data[interaction_type][()] & bounds_mask
                enu_values_by_type[interaction_type].extend(data['Enu'][mask] / 1000)  # Convert MeV to GeV
                counts[interaction_type] += mask.sum()

    total_events = sum(counts.values())
    percentages = {itype: (counts[itype] / total_events) * 100 for itype in interaction_types}

    enu_values_for_hist = [enu_values_by_type[itype] for itype in interaction_types]

    labels = [f"{interaction_type[2:]} ({counts[interaction_type]}, {percentages[interaction_type]:.2f}%)" for interaction_type in interaction_types]
    color_values = [colors[itype] for itype in interaction_types]
    
    plt.hist(enu_values_for_hist, bins=50, range=(1, 11), stacked=True, label=labels, color=color_values, edgecolor='black')
    
    plt.xlabel('Neutrino Energy (GeV)')
    plt.ylabel('Number of Events')
    plt.title('Incident Neutrino Beam Energy (MiniRun4_RHC)')
    
    # Set the range for the x-axis
    plt.xlim(1, 11)
    
    plt.legend()
    plt.tight_layout()
    plt.savefig("enu_withBounds.png")
    plt.show()

if __name__ == "__main__":
    base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW"
    filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW.h5" for i in range(1024)]
    dataset_name = "/mc_truth/interactions/data"
    create_stacked_histogram(filenames, dataset_name)

