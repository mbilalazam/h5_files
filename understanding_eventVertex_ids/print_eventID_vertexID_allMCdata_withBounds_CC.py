# Header
"""
Script to extract and save details for interactions, stack, segments, and trajectories datasets.
Additionally, it only selects events for which the isCC boolean variable is true.
The script outputs results to TXT, CSV, and XLSX files.
Author: Muhammad Bilal Azam
Date: 2023-08-31
"""

import h5py
import csv
import xlsxwriter

# Define bounds
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
    isCC_data = interactions_dataset["isCC"][:]

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

    # Data for CSV and XLSX
    csv_data = []
    filtered_indices = [
        i for i, vertex in enumerate(vertex_data)
        if Xnegbound <= vertex[0] <= Xposbound and 
           Ynegbound <= vertex[1] <= Yposbound and 
           Znegbound <= vertex[2] <= Zposbound and
           isCC_data[i] == True
    ]

    for i in filtered_indices:
        eid = eventIDs_interactions[i]
        vid = vertexIDs_interactions[i]
        csv_data.append({
            "Entry": i+1,
            "Pair (event_id, vertex_id)": f"({eid}, {vid})",
            "interactions": interactions_counts[i],
            "stack": stack_counts[i],
            "segments": segments_counts[i],
            "trajectories": trajectories_counts[i]
        })

    # Writing to CSV
    with open('eventID_vertexID_allMCdata_withBounds_CC.csv', 'w', newline='') as csvfile:
        fieldnames = ["Entry", "Pair (event_id, vertex_id)", "interactions", "stack", "segments", "trajectories"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    # Data for TXT
    txt_data = []

    for idx, i in enumerate(filtered_indices, start=1):
        eid = eventIDs_interactions[i]
        vid = vertexIDs_interactions[i]
        
        # Interactions line
        line = f"interactions -> Entry {idx}: ({eid}, {vid}),\n"
        
        # For Stack
        for s_idx in range(stack_counts[i]):
            line += f"{' ' * 33}stack -> Entry {s_idx + 1}: ({eid}, {vid}), "
            
            # For Segments
            if s_idx < segments_counts[i]:
                line += f"segments -> Entry {s_idx + 1}: ({eid}, {vid}), "
            else:
                line += ", "
            
            # For Trajectories
            if s_idx < trajectories_counts[i]:
                line += f"trajectories -> Entry {s_idx + 1}: ({eid}, {vid})"
            else:
                line += ","
            
            line += "\n"
        
        # If there are more trajectories than stacks or segments
        for t_idx in range(max(stack_counts[i], segments_counts[i]), trajectories_counts[i]):
            line += f"{' ' * 33}, , trajectories -> Entry {t_idx + 1}: ({eid}, {vid})\n"
        
        txt_data.append(line)

    # Write the formatted data to .txt file
    with open('eventID_vertexID_allMCdata_withBounds_CC.txt', 'w') as txtfile:
        for line in txt_data:
            txtfile.write(line + '\n')

    # Writing to XLSX
    workbook = xlsxwriter.Workbook('eventID_vertexID_allMCdata_withBounds_CC.xlsx')
    worksheet = workbook.add_worksheet()
    col = 0
    for header in fieldnames:
        worksheet.write(0, col, header)
        col += 1
    row = 1
    for data_row in csv_data:
        col = 0
        for header in fieldnames:
            worksheet.write(row, col, data_row[header])
            col += 1
        row += 1
    workbook.close()

print("Summary saved to eventID_vertexID_allMCdata_withBounds_CC.csv, eventID_vertexID_allMCdata_withBounds_CC.xlsx, and eventID_vertexID_allMCdata_withBounds_CC.txt.")
