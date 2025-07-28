import os
import base64
import requests
from typing import Literal

REPORT_TYPES = Literal['battle_report', "battle", "bonus", "bonus_overview", "overview"]

BASE_URL = "http://cd2db4qq-8000.use.devtunnels.ms/" # Replace with your actual base URL

def get_stats(img_paths: list[str], report_type: REPORT_TYPES) -> dict:

    images_data = [open(filepath, "rb").read() for filepath in img_paths]
    data_b64enc = [base64.b64encode(data).decode("utf-8") for data in images_data]
    if report_type.__contains__("battle"):
        endpoint = "api/v1/read_battle_report"
    elif report_type.__contains__("bonus") or report_type.__contains__("overview"):
        endpoint = "api/v1/read_bonus_overview"
    else: 
        raise ValueError(f"Unrecognized report type: {report_type}")
    url = f"{BASE_URL}{endpoint}"

    response = requests.post(url, json = {"images": [{"image_data": img_data} for img_data in data_b64enc]})
    if response.status_code == 200:
        print("Stats:")
        print(response.json().get("stats"))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
def imgs_in_dir(directory: str, accepted_formats: tuple[str] = ("png", "jpg")) -> list[str]:
    return [
        os.path.join(directory, filename) 
            for filename in os.listdir(directory) 
                if filename.endswith(accepted_formats)
    ]
    
def main():
    # Bonus Overview Demo
    bonus_overview_stats_dir = "../images/minnie"
    bonus_overview_stats_files = imgs_in_dir(bonus_overview_stats_dir)
    get_stats(bonus_overview_stats_files, report_type="bonus_overview")
    
    # Battle Report Demo
    report_dir = "../images/test_battle_report"
    report_files = sorted(imgs_in_dir(report_dir))
    print(f"Loading {len(report_files)} files from folder {report_dir.split('/')[-1]}")
    print("Fetching stats...")
    import time
    start = time.time()
    get_stats(report_files, report_type="battle_report")
    print(f"Time taken: {time.time() - start:.2f}s")
if __name__ == "__main__":
    main()
    