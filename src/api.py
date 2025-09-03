from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, List, Tuple, Union

from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
import base64

from bonus_overview import get_bonus_overview_stats
from battle_report import parse_battle_report
from schemas import (
    ReadStatsRequest,
    ReadStatsFromReportRequest,
    ReadStatsFromBonusOverviewRequest,
    Stats,
    BonusOverviewOutput,
    BattleReportOutput,
    BattleOutcome
)

app = FastAPI(title="Report Reader API", version="1.0")

allowed_origins = ["https://stats-parser.neptunedevs.com", "http://stats-parser.neptunedevs.com", "https://sim.tundra.land", "sim.tundra.land", "localhost:8000"]
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
rapidocr_reader = RapidOCR()

def normalize_rapidocr_result(result: Tuple[List[List[Union[List[List[float]], str, float]]], Any]) -> List[Tuple[List[List[float]], str, float]]:
    """Normalize RapidOCR result to match EasyOCR format."""
    if result[0] is None:
        return []
    # Extract the first element which contains the detections
    detections = result[0]
    # Convert each detection to match EasyOCR format
    normalized = []
    for detection in detections:
        # detection is [bbox, text, confidence]
        bbox = detection[0]  # Already in the correct format
        text = detection[1]  # String
        confidence = detection[2]  # Float
        normalized.append((bbox, text, confidence))
    return normalized

def preprocess_images(rawrequestdata: ReadStatsRequest) -> list[Any]:
    """Takes raw b64encoded images, processes them, and performs OCR on them

    Args:
        rawrequestdata (ReadStatsRequest): The raw request data 

    Returns:
        list[list[Any]]: list of all files, each of which are a list of each detection
    """
    imgdata = [base64.b64decode(image.image_data) for image in rawrequestdata.images]
    images = [cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) for data in imgdata]
    
    if rawrequestdata.ocr_engine == "rapidocr":
        images_text = []
        for img in images:
            result = rapidocr_reader(img)
            normalized_result = normalize_rapidocr_result(result)
            images_text.append(normalized_result)
    else:  # default to rapidocr (in case another engine is added later)
        images_text = []
        for img in images:
            result = rapidocr_reader(img)
            normalized_result = normalize_rapidocr_result(result)
            images_text.append(normalized_result)
    return images_text

@app.post("/api/v1/read_bonus_overview", response_model=BonusOverviewOutput)
def read_bonus_overview(request: ReadStatsFromBonusOverviewRequest) -> BonusOverviewOutput:
    
    print("Received request with images:", len(request.images))
    parsed_images = preprocess_images(request)

    stats = get_bonus_overview_stats(parsed_images)
    return BonusOverviewOutput.from_stats_dict(stats)

@app.post("/api/v1/read_battle_report", response_model=BattleReportOutput)
def read_battle_report(request: ReadStatsFromReportRequest) -> BattleReportOutput:
    
    parsed_images = preprocess_images(request)
    stats, outcome = parse_battle_report(parsed_images, stats_only=request.stats_only)
    print(stats, outcome)
    return BattleReportOutput(
        left_stats=Stats.from_dict(stats["left"]),
        right_stats=Stats.from_dict(stats["right"]),
        troops_outcome = BattleOutcome.from_dict(outcome)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8001)
