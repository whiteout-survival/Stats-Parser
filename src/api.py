from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

import easyocr
import cv2
import numpy as np
import base64
from fastapi.responses import JSONResponse

from utils import convert_to_stats, merge_stats

reader = easyocr.Reader(['en'])  # 'en' for English

class ImageData(BaseModel):
    image_data: str  # Base64 encoded image data

class ReadStatsRequest(BaseModel):
    images: List[ImageData]

class ErrorResponse(BaseModel):
    error: str
    response_code: int = 400

app = FastAPI(title="Report Reader API", version="1.0")
@app.post("/api/v1/read_stats")
def read_stats(request: ReadStatsRequest) -> Dict[str, Any]:
    response = None
    
    print("Received request with images:", len(request.images))
    imgdata = [base64.b64decode(image.image_data) for image in request.images]

    images = [cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) for data in imgdata]
    if any([img is None for img in images]):
        raise ValueError("Failed to decode an image.")

    results = [reader.readtext(img) for img in images]

    stats = [convert_to_stats(result) for result in results]
    merged_stats = merge_stats(stats)
    if response:
        return response
    
    return JSONResponse(
        {
            "merged_stats": merged_stats
        }, 
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000)