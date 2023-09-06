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
7. Select events for which parent_id not equal to 0 and -1.
8. Collect vertex_id from Stack
9. Make an array of part_pdg corresponding to vertex_id from Stack
10. Count the elements in part_pdg array and plot histogram of the multiplicity
"""
