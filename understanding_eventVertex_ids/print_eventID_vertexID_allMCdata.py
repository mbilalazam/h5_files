"""
Extracts and matches "event_id" and "vertex_id" from various datasets within an HDF5 file.
Generates a CSV and XLSX report detailing the counts of each matched pair for the categories:
interactions, stack, segments, and trajectories.
Author: Muhammad Bilal Azam
"""

import h5py
import csv
import pandas as pd

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

    for i, (eid, vid) in enumerate(zip(eventIDs_interactions, vertexIDs_interactions)):
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
    with open('eventID_vertexID_allMCdata.csv', 'w', newline='') as csvfile:
        fieldnames = ["Entry", "Pair (event_id, vertex_id)", "interactions", "stack", "segments", "trajectories"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    # Writing to XLSX
    df = pd.DataFrame(csv_data)
    df.to_excel("eventID_vertexID_allMCdata.xlsx", index=False)

total_pairs = len(csv_data)
total_interactions = sum(entry["interactions"] for entry in csv_data)
total_stack = sum(entry["stack"] for entry in csv_data)
total_segments = sum(entry["segments"] for entry in csv_data)
total_trajectories = sum(entry["trajectories"] for entry in csv_data)

print(f"Total number of entries for 'Pair (event_id, vertex_id)': {total_pairs}")
print(f"Sum of 'interactions': {total_interactions}")
print(f"Sum of 'stack': {total_stack}")
print(f"Sum of 'segments': {total_segments}")
print(f"Sum of 'trajectories': {total_trajectories}")

print("Summary saved to eventID_vertexID_allMCdata.csv and eventID_vertexID_allMCdata.xlsx")
