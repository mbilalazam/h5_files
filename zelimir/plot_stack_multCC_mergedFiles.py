"""
The given script is used to plot CC Multiplicity from FLOW_MERGED files. 
Author: Muhammad Bilal Azam
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import os

base_path = "/dune/app/users/mazam/working_area/dunendlar_multiplicity/bilal_work/inProgress/MiniRun4_RHC/combined"
filenames = [f"{base_path}/MiniRun4_1E19_RHC.flow.{i:05}.FLOW_MERGED.h5" for i in range(10)]  # 100 files

def get_pdg_codes_for_status1(filename):
    event_data = {}

    with h5py.File(filename, 'r') as f:
        # Get the datasets
        event_ids = f['/mc_truth/one']['vertex_id_stack'][:]
        pdg_codes = f['/mc_truth/one']['part_pdg_stack'][:]
        statuses = f['/mc_truth/one']['part_status_stack'][:]
        
        # Extract isCC values
        isCC_values = f['/mc_truth/one']['isCC_interactions'][:]

        for event_id, pdg, status, isCC in zip(event_ids, pdg_codes, statuses, isCC_values):
            if status == 1 and isCC:
                if event_id in event_data:
                    event_data[event_id]['pdgs'].append(pdg)
                else:
                    event_data[event_id] = {'pdgs': [pdg], 'status': status}
    return event_data

# Collect the counts of PDG codes for each event
pdg_counts = []

for idx, filename in enumerate(filenames, 1):
    print(f"File {idx}/{len(filenames)}: {os.path.basename(filename)}")
    event_data = get_pdg_codes_for_status1(filename)
    for event_id, data in event_data.items():
        pdg_counts.append(len(data['pdgs']))

# Plot histogram
entries = len(pdg_counts)
mean = np.mean(pdg_counts)
std_dev = np.std(pdg_counts)
label_text = f"Entries: {entries}\nMean: {mean:.2f}\nStd Dev: {std_dev:.2f}"

plt.hist(pdg_counts, bins=range(1, 30), label=label_text)
plt.xlabel('Multiplicity')
plt.ylabel('Number of Events')
plt.title('Multiplicity Distribution')
plt.xticks(range(1, 30))
plt.xlim(1, 30)
plt.legend(loc='upper right')
plt.show()
