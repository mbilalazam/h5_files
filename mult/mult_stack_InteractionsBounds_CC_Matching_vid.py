"""
Date: September 06, 2023
Author: Muhammad Bilal Azam
Structure of this code is as follows:
1. Loop over traj_id from Stack
2. Set part_status to 1 from Stack
3. Set isCC to TRUE from interactions.
4. Apply bounds for FV from interactions.
5. It checks for matching vertex_id from stack and interactions datasets. That is, it first filters the vertex_id values from the interactions dataset where isCC is true. Then, it uses these vertex_id values to filter the data in the stack dataset.
6. Collect vertex_id from Stack
7. Make an array of part_pdg corresponding to vertex_id from Stack
8. Count the elements in part_pdg array and plot histogram of the multiplicity
"""

