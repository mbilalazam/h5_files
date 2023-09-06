"""
Date: September 06, 2023
Author: Muhammad Bilal Azam
Structure of this code is as follows:
1. Loop over traj_id from Stack
2. Set part_status to 1 from Stack
3. Set isCC to TRUE from interactions (it checks for matching vertex_id from stack and interactions datasets)
That is, it first filters the vertex_id values from the interactions dataset where isCC is true. Then, it uses these vertex_id values to filter the data in the stack dataset.
3. Collect vertex_id from Stack
4. Make an array of part_pdg corresponding to vertex_id from Stack
5. Count the elements in part_pdg array and plot histogram of the multiplicity
"""

