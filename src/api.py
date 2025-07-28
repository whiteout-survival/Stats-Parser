from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

import easyocr
import cv2
import numpy as np
import base64
from fastapi.responses import JSONResponse

from bonus_overview import get_bonus_overview_stats
from battle_report import get_battle_report_stats

app = FastAPI(title="Report Reader API", version="1.0")
reader = easyocr.Reader(['en'])  # 'en' for English

class ImageData(BaseModel):
    image_data: str  # Base64 encoded image data

class ReadStatsRequest(BaseModel):
    images: List[ImageData]

def preprocess_images(rawrequestdata: ReadStatsRequest) -> list[Any]:
    """Takes raw b64encoded images, processes them, and performs OCR on them

    Args:
        rawrequestdata (ReadStatsRequest): The raw request data 

    Returns:
        list[list[Any]]: List of all files, each of which are a list of each detection
    """
    imgdata = [base64.b64decode(image.image_data) for image in rawrequestdata.images]
    images = [cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) for data in imgdata]
    images_text = [reader.readtext(img) for img in images]
    return images_text

@app.post("/api/v1/read_bonus_overview")
def read_bonus_overview(request: ReadStatsRequest) -> Dict[str, Any]:
    
    print("Received request with images:", len(request.images))
    parsed_images = preprocess_images(request)

    stats = get_bonus_overview_stats(parsed_images)
    return JSONResponse(
        {
            "stats": stats
        }, 
        status_code=200
    )

@app.post("/api/v1/read_battle_report")
def read_battle_report(request: ReadStatsRequest) -> Dict[str, Any]:
    parsed_images = preprocess_images(request)
    stats = get_battle_report_stats(parsed_images)
    return JSONResponse(
        {
            "stats": stats
        }, 
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000)