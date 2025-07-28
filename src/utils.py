

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
