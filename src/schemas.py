from pydantic import BaseModel, Field
from typing import List, Dict


class ImageData(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")


class ReadStatsRequest(BaseModel):
    images: List[ImageData] = Field(..., description="List of base64 encoded images")
    ocr_engine: str = Field(default="rapidocr", description="OCR engine to use ('easyocr' or 'rapidocr')")


class Stats(BaseModel):
    infantry: List[float] = Field(..., description="Infantry stats [attack, defense, lethality, health]")
    lancer: List[float] = Field(..., description="Lancer stats [attack, defense, lethality, health]")
    marksman: List[float] = Field(..., description="Marksman stats [attack, defense, lethality, health]")
    
    @classmethod
    def from_dict(cls, data: Dict[str, List[float]]) -> "Stats":
        return cls(
            infantry=[data["infantry"][0], data["infantry"][1], data["infantry"][2], data["infantry"][3]],
            lancer=[data["lancer"][0], data["lancer"][1], data["lancer"][2], data["lancer"][3]],
            marksman=[data["marksman"][0], data["marksman"][1], data["marksman"][2], data["marksman"][3]]
        )


class BonusOverviewOutput(BaseModel):
    stats: Stats = Field(..., description="Stats by troop type")
    
    @classmethod
    def from_stats_dict(cls, stats: Dict[str, List[float]]) -> "BonusOverviewOutput":
        return cls(
            stats=Stats.from_dict(stats)
        )


class BattleReportOutput(BaseModel):
    left_stats: Stats = Field(..., description="Left side stats by troop type")
    right_stats: Stats = Field(..., description="Right side stats by troop type")
