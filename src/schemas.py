from pydantic import BaseModel, Field
from typing import List, Dict


class ImageData(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")


class ReadStatsRequest(BaseModel):
    images: List[ImageData] = Field(..., description="List of base64 encoded images")
    ocr_engine: str = Field(default="rapidocr", description="OCR engine to use ('easyocr' or 'rapidocr')")
    stats_only: bool = Field(default = True, description="Whether to only look for stats and not the full OCR output")


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

class TroopOutcome(BaseModel):
    initial_troops: int = Field(..., description="Initial number of troops")
    losses: int = Field(..., description="Number of troops lost")
    injured: int = Field(..., description="Number of injured troops")
    lightly_injured: int = Field(..., description="Number of lightly injured troops")
    survivors: int = Field(..., description="Number of surviving troops")
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "TroopOutcome":
        return cls(
            initial_troops=data["initial_troops"],
            losses=data["losses"],
            injured=data["injured"],
            lightly_injured=data["lightly_injured"],
            survivors=data["survivors"]
        )
    
class BattleOutcome(BaseModel):
    left: TroopOutcome = Field(..., description="Left side troop outcome")
    right: TroopOutcome = Field(..., description="Right side troop outcome")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, int]]) -> "BattleOutcome":
        return cls(
            left=TroopOutcome.from_dict(data["left"]),
            right=TroopOutcome.from_dict(data["right"])
        )

class BonusOverviewOutput(BaseModel):
    stats: Stats = Field(..., description="Stats by troop type")
    
    @classmethod
    def from_stats_dict(cls, stats: Dict[str, List[float]]) -> "BonusOverviewOutput":
        return cls(
            stats=Stats.from_dict(stats)
        )


class BattleReportOutput(BaseModel):
    troops_outcome: BattleOutcome | None = Field(..., description="Troop outcomes for both sides")
    left_stats: Stats = Field(..., description="Left side stats by troop type")
    right_stats: Stats = Field(..., description="Right side stats by troop type")
