"""
Extracts and matches "event_id" and "vertex_id" from various datasets within an HDF5 file within FV.
Generates a text report detailing the counts of each matched pair for the categories:
interactions, stack, segments, and trajectories.
Author: Muhammad Bilal Azam
"""

import h5py
import csv
import pandas as pd  # For writing to .xlsx

Xnegbound = -60
Xposbound = 60
Ynegbound = -328
Yposbound = 208
Znegbound = 1240
Zposbound = 1360

def get_matching_counts(target_event_ids, target_vertex_ids, source_event_ids, source_vertex_ids):
    """
    Generate a list of counts for each pair in target dataset that matches with source dataset.
    """
    counts = []
    for eid, vid in zip(target_event_ids, target_vertex_ids):
        count = sum(1 for seid, svid in zip(source_event_ids, source_vertex_ids) if seid == eid and svid == vid)
        counts.append(count)
    return counts

with h5py.File("MiniRun4_1E19_RHC.flow.00000.FLOW.h5", "r") as file:
    # Access the datasets for interactions, stack, segments, and trajectories
    interactions_dataset = file["/mc_truth/interactions/data"]
    vertex_data = interactions_dataset["vertex"][:]
    
    eventIDs_interactions = interactions_dataset["event_id"][:]
    vertexIDs_interactions = interactions_dataset["vertex_id"][:]

    stack_dataset = file["/mc_truth/stack/data"]
    eventIDs_stack = stack_dataset["event_id"][:]
    vertexIDs_stack = stack_dataset["vertex_id"][:]

    segments_dataset = file["/mc_truth/segments/data"]
    eventIDs_segments = segments_dataset["event_id"][:]
    vertexIDs_segments = segments_dataset["vertex_id"][:]

    trajectories_dataset = file["/mc_truth/trajectories/data"]
    eventIDs_trajectories = trajectories_dataset["event_id"][:]
    vertexIDs_trajectories = trajectories_dataset["vertex_id"][:]
    
    interactions_counts = get_matching_counts(eventIDs_interactions, vertexIDs_interactions, eventIDs_interactions, vertexIDs_interactions)
    stack_counts = get_matching_counts(eventIDs_interactions, vertexIDs_interactions, eventIDs_stack, vertexIDs_stack)
    segments_counts = get_matching_counts(eventIDs_interactions, vertexIDs_interactions, eventIDs_segments, vertexIDs_segments)
    trajectories_counts = get_matching_counts(eventIDs_interactions, vertexIDs_interactions, eventIDs_trajectories, vertexIDs_trajectories)

    csv_data = []

    filtered_indices = [
        i for i, vertex in enumerate(vertex_data)
        if Xnegbound <= vertex[0] <= Xposbound and 
           Ynegbound <= vertex[1] <= Yposbound and 
           Znegbound <= vertex[2] <= Zposbound
    ]

    for i in filtered_indices:
        eid = eventIDs_interactions[i]
        vid = vertexIDs_interactions[i]
        # Preparing data for CSV
        csv_data.append({
            "Entry": i+1,
            "Pair (event_id, vertex_id)": f"({eid}, {vid})",
            "interactions": interactions_counts[i],
            "stack": stack_counts[i],
            "segments": segments_counts[i],
            "trajectories": trajectories_counts[i]
        })

    # Writing to CSV
    with open('eventID_vertexID_allMCdata_withBounds.csv', 'w', newline='') as csvfile:
        fieldnames = ["Entry", "Pair (event_id, vertex_id)", "interactions", "stack", "segments", "trajectories"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    # Writing to .xlsx
    df = pd.DataFrame(csv_data)
    df.to_excel('eventID_vertexID_allMCdata_withBounds.xlsx', index=False)

    # Writing to TXT
    with open('eventID_vertexID_allMCdata_withBounds.txt', 'w') as txtfile:
        summary_statements = []

        for i, (eid, vid) in enumerate(zip(eventIDs_interactions, vertexIDs_interactions)):
            # Construct the base string
            base_str = f"interactions -> Entry {i+1}: ({eid}, {vid}),"
            txtfile.write(base_str)

            # Create lists of formatted strings for each of the other counts
            stacks = [f"stack -> Entry {j+1}: ({eid}, {vid})" for j in range(stack_counts[i])]
            segments = [f"segments -> Entry {j+1}: ({eid}, {vid})" for j in range(segments_counts[i])]
            trajectories = [f"trajectories -> Entry {j+1}: ({eid}, {vid})" for j in range(trajectories_counts[i])]

            # Using zip_longest to write multiple lines that are aligned
            from itertools import zip_longest
            for s, seg, t in zip_longest(stacks, segments, trajectories, fillvalue=''):
                txtfile.write(f"\n{' ' * len(base_str)} {s}, {seg}, {t}")

            txtfile.write("\n\n")
            
            # Constructing the summary statements
            summary = f"Entry {i+1}: For ({eid}, {vid}) in interactions,"
            if stack_counts[i]:
                summary += f" there are {stack_counts[i]} entries in stack,"
            if segments_counts[i]:
                summary += f" {segments_counts[i]} in segments,"
            if trajectories_counts[i]:
                summary += f" {trajectories_counts[i]} in trajectories."
            summary_statements.append(summary.strip(","))

        for s in summary_statements:
            txtfile.write(f"{s}\n")

print("Summary saved to eventID_vertexID_allMCdata_withBounds.csv, .xlsx, and .txt")
