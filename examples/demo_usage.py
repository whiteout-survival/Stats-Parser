import os
import base64
import requests
from typing import Literal
import json
import time

REPORT_TYPES = Literal['battle_report', "battle", "bonus", "bonus_overview", "overview"]

# BASE_URL = "https://stats-parser.neptunedevs.com/" # Replace with your actual base URL
BASE_URL = "http://localhost:8001/" # Replace with your actual base URL

def get_stats(img_paths: list[str], report_type: REPORT_TYPES, ocr_engine: str = "rapidocr") -> dict:

    images_data = [open(filepath, "rb").read() for filepath in img_paths]
    data_b64enc = [base64.b64encode(data).decode("utf-8") for data in images_data]
    if report_type.__contains__("battle"):
        endpoint = "api/v1/read_battle_report"
    elif report_type.__contains__("bonus") or report_type.__contains__("overview"):
        endpoint = "api/v1/read_bonus_overview"
    else: 
        raise ValueError(f"Unrecognized report type: {report_type}")
    url = f"{BASE_URL}{endpoint}"
    print(f"Sending request to {url} with {len(data_b64enc)} images using {ocr_engine} OCR engine...")
    response = requests.post(url, json = {
        "images": [{"image_data": img_data} for img_data in data_b64enc],
        "ocr_engine": ocr_engine,
        "stats_only": False
    })
    if response.status_code == 200:
        print("Stats:")
        print(json.loads(response.text))
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
    # Bonus Overview Demo with EasyOCR
    # print("=== Bonus Overview Demo with EasyOCR ===")
    # bonus_overview_stats_dir = "../images/minime"
    # bonus_overview_stats_files = imgs_in_dir(bonus_overview_stats_dir)
    # print("Fetching stats...")
    # start = time.time()
    # get_stats(bonus_overview_stats_files, report_type="bonus_overview", ocr_engine="easyocr")
    # print(f"Time taken: {time.time() - start:.2f}s")
    
    # Bonus Overview Demo with RapidOCR
    
    # print("\n=== Bonus Overview Demo with RapidOCR ===")
    # print("Fetching stats...")
    # start = time.time()
    # get_stats(bonus_overview_stats_files, report_type="bonus_overview", ocr_engine="rapidocr")
    # print(f"Time taken: {time.time() - start:.2f}s")
    
    report_dir = "../images/test_battle_report"
    report_files = sorted(imgs_in_dir(report_dir))

    # Battle Report Demo with RapidOCR
    print("\n=== Battle Report Demo with RapidOCR ===")
    print(f"Loading {len(report_files)} files from folder {report_dir.split('/')[-1]}")
    print("Fetching stats...")
    start = time.time()
    get_stats(report_files, report_type="battle_report", ocr_engine="rapidocr")
    print(f"Time taken: {time.time() - start:.2f}s")
if __name__ == "__main__":
    main()
