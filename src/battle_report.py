from typing import Any

from utils import handle_split_boxes

KEYS = [    
    "Infantry Attack", "Infantry Defense", "Infantry Lethality", "Infantry Health",
    "Lancer Attack", "Lancer Defense", "Lancer Lethality", "Lancer Health",
    "Marksman Attack", "Marksman Defense", "Marksman Lethality", "Marksman Health"
]

def parse_battle_report(images_text: list[list[Any]], stats_only: bool) -> tuple[dict[str, dict[str, list[float]]], dict[str, dict[str, int]] | None]:
    stats = get_battle_report_stats(images_text)
    if not stats_only:
        outcome = get_battle_report_troops_outcome(images_text)
        return stats, outcome
    return stats, None

def get_battle_report_stats(images_text: list[list[Any]]) -> dict[str, dict[str, list[float]]]:
    img_idx, stats_image_text = str_in_image_from_images_list(images_text, "stat")
    stats_image_text = handle_split_boxes(stats_image_text)
    stats = read_stats(stats_image_text)
    return stats
def get_battle_report_troops_outcome(images_text: list[list[Any]]) -> dict[str, dict[str, list[float]]]:
    img_idx, troops_outcome_text = str_in_image_from_images_list(images_text, "Battle Overview")
    troops_outcome_text = handle_split_boxes(troops_outcome_text)
    outcome = read_outcome(troops_outcome_text)
    return outcome

def str_in_image_from_images_list(text_in_images: list[list[str]], text_to_find: str) -> tuple[int, list]:
    """
    Processes a list of images to find the one containing the "Stat" text.
    Returns the first image that contains the text "Stat".
    """
    text_to_find = text_to_find.lower()
    for i, image_text in enumerate(text_in_images):
        for found_string in image_text:
            if isinstance(found_string, tuple):
                found_string = found_string[1]
            found_string = str(found_string).lower()
            if found_string.__contains__(text_to_find):
                print(f"Found '{text_to_find}' in image # {i}")
                return i, image_text
    raise ValueError(f"{text_to_find} page not found.")


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


def read_outcome(text_in_image: list[str]) -> dict:
    """
    Reads the battle outcome values from the text in the image and returns a dictionary with the troop counts.
    """
    troops_count_dict = {
        "left": {
            "initial_troops": 0,
            "losses": 0,
            "injured": 0,
            "lightly_injured": 0,
            "survivors": 0
        },
        "right": {
            "initial_troops": 0,
            "losses": 0,
            "injured": 0,
            "lightly_injured": 0,
            "survivors": 0
        }
    }
    format_map = str.maketrans(
        {
            "%": "",
            "+": "",
            ",": "",
            "o": "0",
            "O": "0",
        }
    )
    for i, text in enumerate(text_in_image):
        if isinstance(text, tuple):
            text = text[1]
        text = str(text).strip().lower()
        print(text)
        if text.__contains__("troops"):
            troops_count_dict["left"]["initial_troops"] = int(str(text_in_image[i-1][1]).strip().translate(format_map))
            troops_count_dict["right"]["initial_troops"] = int(str(text_in_image[i+1][1]).strip().translate(format_map))
        elif text.__contains__("losses"):
            troops_count_dict["left"]["losses"] = int(str(text_in_image[i-1][1]).strip().translate(format_map))
            troops_count_dict["right"]["losses"] = int(str(text_in_image[i+1][1]).strip().translate(format_map))
        elif text.__contains__("injured") and not text.__contains__("lightly"):
            troops_count_dict["left"]["injured"] = int(str(text_in_image[i-1][1]).strip().translate(format_map))
            troops_count_dict["right"]["injured"] = int(str(text_in_image[i+1][1]).strip().translate(format_map))
        elif text.__contains__("lightly injured"):
            troops_count_dict["left"]["lightly_injured"] = int(str(text_in_image[i-1][1]).strip().translate(format_map))
            troops_count_dict["right"]["lightly_injured"] = int(str(text_in_image[i+1][1]).strip().translate(format_map))
        elif text.__contains__("survivors"):
            troops_count_dict["left"]["survivors"] = int(str(text_in_image[i-1][1]).strip().translate(format_map))
            troops_count_dict["right"]["survivors"] = int(str(text_in_image[i+1][1]).strip().translate(format_map))

    return troops_count_dict
