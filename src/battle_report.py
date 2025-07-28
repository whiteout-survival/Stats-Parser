from typing import Any

from utils import handle_split_boxes

KEYS = [    
    "Infantry Attack", "Infantry Defense", "Infantry Lethality", "Infantry Health",
    "Lancer Attack", "Lancer Defense", "Lancer Lethality", "Lancer Health",
    "Marksman Attack", "Marksman Defense", "Marksman Lethality", "Marksman Health"
]

def get_battle_report_stats(images_text: list[list[Any]]) -> dict[str, dict[str, list[float]]]:
    img_idx, stats_image_text = stats_image_from_images_list(images_text)
    stats_image_text = handle_split_boxes(stats_image_text)
    stats = read_stats(stats_image_text)
    return stats

def stats_image_from_images_list(text_in_images: list[list[str]]) -> tuple[int, list]:
    """
    Processes a list of images to find the one containing the "Stat" text.
    Returns the first image that contains the text "Stat".
    """
    for i, image_text in enumerate(text_in_images):
        is_special_bonuses_page = False
        is_stats_page = False
        for found_string in image_text:
            if isinstance(found_string, tuple):
                found_string = found_string[1]
            found_string = str(found_string).lower()
            if found_string.__contains__("stat"):
                print(f"Found 'stat' in image{i}: {found_string}")
                is_stats_page = True
            if found_string.__contains__("special") or \
                found_string.__contains__("enemy"):
                is_special_bonuses_page = True
                print(f"Special bonus page({i}): {found_string}")
                break
        if is_stats_page:
            if not is_special_bonuses_page:
                return i, image_text
    raise ValueError("Stat page not found.")

def read_stats(text_in_image: list[str]) -> dict:
    """
    Reads the stats from the text in the image and returns a dictionary with the stats.
    """
    stats_dict = {
        "left": {
            "infantry": [0.0, 0.0, 0.0, 0.0],
            "lancer": [0.0, 0.0, 0.0, 0.0],
            "marksman": [0.0, 0.0, 0.0, 0.0]
        },
        "right": {
            "infantry": [0.0, 0.0, 0.0, 0.0],
            "lancer": [0.0, 0.0, 0.0, 0.0],
            "marksman": [0.0, 0.0, 0.0, 0.0]
        }
    }
    
    for i, text in enumerate(text_in_image):
        if isinstance(text, tuple):
            text = text[1]
        text = str(text).strip().lower()
        if text.__contains__("infantry attack"):
            stats_dict["left"]["infantry"][0] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["infantry"][0] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("infantry defense"):
            stats_dict["left"]["infantry"][1] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["infantry"][1] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("infantry lethality"):
            stats_dict["left"]["infantry"][2] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["infantry"][2] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("infantry health"):
            stats_dict["left"]["infantry"][3] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["infantry"][3] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("lancer attack"):
            stats_dict["left"]["lancer"][0] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["lancer"][0] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("lancer defense"):
            stats_dict["left"]["lancer"][1] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["lancer"][1] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("lancer lethality"):
            stats_dict["left"]["lancer"][2] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["lancer"][2] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("lancer health"):
            stats_dict["left"]["lancer"][3] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["lancer"][3] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("marksman attack"):
            stats_dict["left"]["marksman"][0] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["marksman"][0] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("marksman defense"):
            stats_dict["left"]["marksman"][1] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["marksman"][1] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("marksman lethality"):
            stats_dict["left"]["marksman"][2] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["marksman"][2] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))
        elif text.__contains__("marksman health"):
            stats_dict["left"]["marksman"][3] = float(str(text_in_image[i-1][1]).strip().replace("%", "").replace("+", ""))
            stats_dict["right"]["marksman"][3] = float(str(text_in_image[i+1][1]).strip().replace("%", "").replace("+", ""))

    return stats_dict