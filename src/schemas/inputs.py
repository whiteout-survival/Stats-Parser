from typing import List
from pydantic import BaseModel, Field


class ImageData(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")


class ReadStatsRequest(BaseModel):
    images: List[ImageData] = Field(..., description="List of base64 encoded images")
    ocr_engine: str = Field(default="rapidocr", description="OCR engine to use (easyocr has been deprecated)")


class ReadStatsFromReportRequest(ReadStatsRequest):
    stats_only: bool = Field(default=True, description="Whether to only look for stats and not the full output")


class ReadStatsFromBonusOverviewRequest(ReadStatsRequest):
    pass

