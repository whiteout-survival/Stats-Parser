from typing import Any

from utils import handle_split_boxes
from ocr import ocr_images_b64

KEYS = ["Troops Attack", "Troops Defense","Troops Lethality", "Troops Health",
    "Infantry Attack", "Infantry Defense", "Infantry Lethality", "Infantry Health",
    "Lancer Attack", "Lancer Defense", "Lancer Lethality", "Lancer Health",
    "Marksman Attack", "Marksman Defense", "Marksman Lethality", "Marksman Health"
]    

def get_bonus_overview_stats(images_text: list[list[Any]]) -> dict[str, dict[str, list[float]]]:
    stats = [convert_to_stats(result) for result in images_text]
    merged_stats = merge_stats(stats)
    return merged_stats


def parse_bonus_overview(images_b64: list[str], ocr_engine: str = "rapidocr") -> dict[str, dict[str, list[float]]]:
    """Decode, OCR, and parse bonus overview images from base64 payloads."""
    images_text = ocr_images_b64(images_b64, ocr_engine)
    return get_bonus_overview_stats(images_text)

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
        "lancer": [0.0, 0.0, 0.0, 0.0],
        "marksman": [0.0, 0.0, 0.0, 0.0]
    }
    stats["troops"][0] = kv_dict["Troops Attack"]
    stats["troops"][1] = kv_dict["Troops Defense"]
    stats["troops"][2] = kv_dict["Troops Lethality"]
    stats["troops"][3] = kv_dict["Troops Health"]
    # Add infantry, lancer, and marksman stats
    stats["infantry"][0] = kv_dict["Infantry Attack"]
    stats["infantry"][1] = kv_dict["Infantry Defense"]
    stats["infantry"][2] = kv_dict["Infantry Lethality"]
    stats["infantry"][3] = kv_dict["Infantry Health"]
    stats["lancer"][0] = kv_dict["Lancer Attack"]
    stats["lancer"][1] = kv_dict["Lancer Defense"]
    stats["lancer"][2] = kv_dict["Lancer Lethality"]
    stats["lancer"][3] = kv_dict["Lancer Health"]
    stats["marksman"][0] = kv_dict["Marksman Attack"]
    stats["marksman"][1] = kv_dict["Marksman Defense"]
    stats["marksman"][2] = kv_dict["Marksman Lethality"]
    stats["marksman"][3] = kv_dict["Marksman Health"]
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
    if len(stats) > 1:
        for troop_type in stats[0].keys():
            merged_stats[troop_type] = [max(*values) for values in zip(*[stat[troop_type] for stat in stats])]
    else:
        merged_stats = stats[0]

    merged_stats["infantry"][0] = merged_stats["infantry"][0] + merged_stats["troops"][0]
    merged_stats["infantry"][1] = merged_stats["infantry"][1] + merged_stats["troops"][1]
    merged_stats["infantry"][2] = merged_stats["infantry"][2] + merged_stats["troops"][2]
    merged_stats["infantry"][3] = merged_stats["infantry"][3] + merged_stats["troops"][3]
    merged_stats["lancer"][0] = merged_stats["lancer"][0] + merged_stats["troops"][0]
    merged_stats["lancer"][1] = merged_stats["lancer"][1] + merged_stats["troops"][1]
    merged_stats["lancer"][2] = merged_stats["lancer"][2] + merged_stats["troops"][2]
    merged_stats["lancer"][3] = merged_stats["lancer"][3] + merged_stats["troops"][3]
    merged_stats["marksman"][0] = merged_stats["marksman"][0] + merged_stats["troops"][0]
    merged_stats["marksman"][1] = merged_stats["marksman"][1] + merged_stats["troops"][1]
    merged_stats["marksman"][2] = merged_stats["marksman"][2] + merged_stats["troops"][2]
    merged_stats["marksman"][3] = merged_stats["marksman"][3] + merged_stats["troops"][3]
    del merged_stats["troops"]  # Remove the 'troops' key as it's now merged into others
    for troop_type in merged_stats.keys():
        merged_stats[troop_type] = [round(stat, 2) for stat in merged_stats[troop_type]]
    return merged_stats
