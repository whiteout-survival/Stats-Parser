

KEYS = ["Troops Attack", "Troops Defense","Troops Lethality", "Troops Health",
    "Infantry Attack", "Infantry Defense", "Infantry Lethality", "Infantry Health",
    "Lancer Attack", "Lancer Defense", "Lancer Lethality", "Lancer Health",
    "Marksman Attack", "Marksman Defense", "Marksman Lethality", "Marksman Health"
]

def merge_stats(stats: list[dict[str, list[float]]]) -> dict[str, list[float]]:
    """
    Merges two stats dictionaries by taking max values for each stat.
    
    Args:
        stats1 (dict[str, list[float]]): First stats dictionary.
        stats2 (dict[str, list[float]]): Second stats dictionary.
        
    Returns:
        dict[str, list[float]]: Merged stats dictionary.
    """
    merged_stats = {}
    for troop_type in stats[0].keys():
        merged_stats[troop_type] = [max(*values) for values in zip(*[stat[troop_type] for stat in stats])]
    
    merged_stats["infantry"][0] = merged_stats["infantry"][0] + merged_stats["troops"][0]
    merged_stats["infantry"][1] = merged_stats["infantry"][1] + merged_stats["troops"][1]
    merged_stats["infantry"][2] = merged_stats["infantry"][2] + merged_stats["troops"][2]
    merged_stats["infantry"][3] = merged_stats["infantry"][3] + merged_stats["troops"][3]
    merged_stats["lancers"][0] = merged_stats["lancers"][0] + merged_stats["troops"][0]
    merged_stats["lancers"][1] = merged_stats["lancers"][1] + merged_stats["troops"][1]
    merged_stats["lancers"][2] = merged_stats["lancers"][2] + merged_stats["troops"][2]
    merged_stats["lancers"][3] = merged_stats["lancers"][3] + merged_stats["troops"][3]
    merged_stats["marksmen"][0] = merged_stats["marksmen"][0] + merged_stats["troops"][0]
    merged_stats["marksmen"][1] = merged_stats["marksmen"][1] + merged_stats["troops"][1]
    merged_stats["marksmen"][2] = merged_stats["marksmen"][2] + merged_stats["troops"][2]
    merged_stats["marksmen"][3] = merged_stats["marksmen"][3] + merged_stats["troops"][3]
    del merged_stats["troops"]  # Remove the 'troops' key as it's now merged into others
    for troop_type in merged_stats.keys():
        merged_stats[troop_type] = [round(stat, 2) for stat in merged_stats[troop_type]]
    return merged_stats

def convert_to_stats(raw_ocr_output: list[str]) -> dict[str, list[float]]:
    """
    Converts raw OCR output into a structured stats dictionary.
    
    Args:
        raw_ocr_output (list[str]): List of strings from OCR output.
        
    Returns:
        dict[str, list[float]]: Dictionary with structured stats.
    """
    merged_results = handle_split_boxes(raw_ocr_output)
    extracted = extract_stats(merged_results, KEYS)
    for key, value in extracted.items():
        # print(f"Extracted {key}: {value}")
        if isinstance(value, str) and value.replace("%", "", 1).replace('.', '', 1).isdigit():
            extracted[key] = float(value.replace("%", "", 1))
        elif isinstance(value, str):
            extracted[key] = 0.0  # Default to 0.0 if the value is not a number

    return format_stats(extracted)


def format_stats(kv_dict: dict) -> dict[str, list[float]]:
    stats: dict[str, list[float]] = {
        "troops": [0.0, 0.0, 0.0, 0.0],
        "infantry": [0.0, 0.0, 0.0, 0.0],
        "lancers": [0.0, 0.0, 0.0, 0.0],
        "marksmen": [0.0, 0.0, 0.0, 0.0]
    }
    stats["troops"][0] = kv_dict["Troops Attack"]
    stats["troops"][1] = kv_dict["Troops Defense"]
    stats["troops"][2] = kv_dict["Troops Lethality"]
    stats["troops"][3] = kv_dict["Troops Health"]
    # Add infantry, lancers, and marksmen stats
    stats["infantry"][0] = kv_dict["Infantry Attack"]
    stats["infantry"][1] = kv_dict["Infantry Defense"]
    stats["infantry"][2] = kv_dict["Infantry Lethality"]
    stats["infantry"][3] = kv_dict["Infantry Health"]
    stats["lancers"][0] = kv_dict["Lancer Attack"]
    stats["lancers"][1] = kv_dict["Lancer Defense"]
    stats["lancers"][2] = kv_dict["Lancer Lethality"]
    stats["lancers"][3] = kv_dict["Lancer Health"]
    stats["marksmen"][0] = kv_dict["Marksman Attack"]
    stats["marksmen"][1] = kv_dict["Marksman Defense"]
    stats["marksmen"][2] = kv_dict["Marksman Lethality"]
    stats["marksmen"][3] = kv_dict["Marksman Health"]
    return stats

def extract_stats(results, keys):
    """
    Given OCR results and a list of keys, match each key to its value by finding the closest y-axis value.
    Returns a dictionary of key-value pairs.
    """
    # Prepare a list of (avg_y, text, bbox) for all results
    ocr_entries = []
    for bbox, text, prob in results:
        y_coords = [pt[1] for pt in bbox]
        avg_y = sum(y_coords) / len(y_coords)
        ocr_entries.append({'avg_y': avg_y, 'text': text, 'bbox': bbox})

    kv_dict = {}
    for key in keys:
        # Find the OCR entry that matches the key (case-insensitive)
        key_entry = next((entry for entry in ocr_entries if entry['text'].strip().lower() == key.strip().lower()), None)
        if key_entry is None:
            kv_dict[key] = 0.0  # Key not found in OCR results
            continue  # Key not found in OCR results

        key_y = key_entry['avg_y']
        # Find the closest entry (excluding the key itself) by y-axis
        value_entry = min(
            (entry for entry in ocr_entries if entry['text'] != key_entry['text']),
            key=lambda entry: abs(entry['avg_y'] - key_y),
            default=None
        )
        if value_entry:
            kv_dict[key] = value_entry['text']

    return kv_dict

def are_in_same_row(bbox1, bbox2, y_tolerance_factor=0.1):
    # Get the average y-coordinate for each bbox
    y1_center = (bbox1[0][1] + bbox1[2][1]) / 2
    y2_center = (bbox2[0][1] + bbox2[2][1]) / 2

    # Get the height of the bounding boxes
    h1 = abs(bbox1[2][1] - bbox1[0][1])
    h2 = abs(bbox2[2][1] - bbox2[0][1])

    # A tolerance based on the average height of the boxes
    tolerance = max(h1, h2) * y_tolerance_factor

    return abs(y1_center - y2_center) < tolerance

def are_horizontally_close_and_touching(bbox1, bbox2, x_overlap_tolerance=5):
    # Get x-coordinates of the left and right edges
    x1_left = min(p[0] for p in bbox1)
    x1_right = max(p[0] for p in bbox1)
    x2_left = min(p[0] for p in bbox2)
    x2_right = max(p[0] for p in bbox2)

    # Check for horizontal overlap
    overlap = max(0, min(x1_right, x2_right) - max(x1_left, x2_left))

    # Calculate horizontal gap (positive if separated, negative if overlapping)
    gap = 0
    if x1_right < x2_left: # bbox1 is to the left of bbox2
        gap = x2_left - x1_right
    elif x2_right < x1_left: # bbox2 is to the left of bbox1
        gap = x1_left - x2_right
    # If they already overlap significantly, 'gap' calculation might be tricky without
    # careful handling of order. The primary goal is 'touching or very close'.

    # Let's redefine "touching" as a small gap or slight overlap.
    # If they are very close (e.g., gap less than x_overlap_tolerance) or overlap slightly
    return (gap >= 0 and gap < x_overlap_tolerance) or \
           (overlap > 0 and overlap < x_overlap_tolerance) # small overlap counts as touching/close

def merge_bboxes(data1, data2):
    bbox1, text1, prob1 = data1
    bbox2, text2, prob2 = data2

    # Calculate new bounding box (min x, min y, max x, max y)
    all_x = [p[0] for p in bbox1] + [p[0] for p in bbox2]
    all_y = [p[1] for p in bbox1] + [p[1] for p in bbox2]

    min_x, min_y = min(all_x), min(all_y)
    max_x, max_y = max(all_x), max(all_y)

    # EasyOCR's bbox is usually 4 points, ordered top-left, top-right, bottom-right, bottom-left
    # We'll return a similar format for consistency, even if it's axis-aligned.
    merged_bbox = [
        [min_x, min_y],
        [max_x, min_y],
        [max_x, max_y],
        [min_x, max_y]
    ]

    # Decide order for text concatenation. Assume left-to-right reading.
    # Compare average x-coordinates or the min x of top-left points.
    if min(p[0] for p in bbox1) < min(p[0] for p in bbox2):
        merged_text = f"{text1} {text2}"
    else:
        merged_text = f"{text2} {text1}"

    merged_prob = min(prob1, prob2)

    return (merged_bbox, merged_text, merged_prob)

def handle_split_boxes(results):
    """Merges horizontally close bounding boxes that are in the same row.

    Args:
        results (list): List of OCR results, each in the format (bbox, text, confidence).
    """
    current_results = [(i, r[0], r[1], r[2]) for i, r in enumerate(results)]

    # Iterate until no more merges can be made
    has_merged_in_pass = True
    while has_merged_in_pass:
        has_merged_in_pass = False
        new_results_for_pass = []
        merged_this_pass = set()

        for i, (idx1, bbox1, text1, prob1) in enumerate(current_results):
            if idx1 in merged_this_pass:
                continue

            found_merge = False
            for j, (idx2, bbox2, text2, prob2) in enumerate(current_results):
                if i == j or idx2 in merged_this_pass:
                    continue

                # Check if they can be merged
                if are_in_same_row(bbox1, bbox2, y_tolerance_factor=0.2) and \
                are_horizontally_close_and_touching(bbox1, bbox2, x_overlap_tolerance=20): # Increased tolerance
                    # Merge them
                    merged_data = merge_bboxes((bbox1, text1, prob1), (bbox2, text2, prob2))
                    new_results_for_pass.append((-1, merged_data[0], merged_data[1], merged_data[2]))
                    merged_this_pass.add(idx1)
                    merged_this_pass.add(idx2)
                    has_merged_in_pass = True
                    found_merge = True
                    break # Move to the next item in current_results for bbox1

            if not found_merge and idx1 not in merged_this_pass:
                new_results_for_pass.append((idx1, bbox1, text1, prob1))

        temp_current_results = []
        for item in new_results_for_pass:
            # If it's a newly merged item, give it a new temporary unique ID for further merging attempts
            if item[0] == -1:
                temp_current_results.append((len(results) + len(temp_current_results), item[1], item[2], item[3]))
            else:
                temp_current_results.append(item)
        current_results = temp_current_results
    # The final merged results are now in current_results (minus the index at the start)
    return [(r[1], r[2], r[3]) for r in current_results]
