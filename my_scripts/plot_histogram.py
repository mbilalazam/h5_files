""" 
This script is to read some data from an h5 file and then plot a histogram using that data.
Author: Muhammad Bilal Azam
"""

import h5py
import matplotlib.pyplot as plt

def plot_energy_histogram_from_h5(filename, dataset_name, bins=50):
    with h5py.File(filename, 'r') as f:
        # Extract the energy component of part_4mom
        energy = f[dataset_name]['part_4mom'][:, 0]  # Assuming energy is the first component
        
        # Plot the histogram
        plt.hist(energy, bins=bins)
        plt.xlabel('Energy')
        plt.ylabel('Frequency')
        plt.title('Histogram of Energy from part_4mom')
        plt.show()

if __name__ == "__main__":
    filename = "MicroRun3.1_1E18_FHC.flow.00000.FLOW.h5"
    dataset_path = "/mc_truth/stack/data"
    plot_energy_histogram_from_h5(filename, dataset_path)
