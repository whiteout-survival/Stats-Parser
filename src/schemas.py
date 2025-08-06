from pydantic import BaseModel, Field
from typing import List, Dict


class ImageData(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")


class ReadStatsRequest(BaseModel):
    images: List[ImageData] = Field(..., description="List of base64 encoded images")
    ocr_engine: str = Field(default="easyocr", description="OCR engine to use ('easyocr' or 'rapidocr')")


class TroopStats(BaseModel):
    attack: float = Field(..., description="Attack bonus percentage")
    defense: float = Field(..., description="Defense bonus percentage")
    lethality: float = Field(..., description="Lethality bonus percentage")
    health: float = Field(..., description="Health bonus percentage")


class Stats(BaseModel):
    infantry: TroopStats
    lancer: TroopStats
    marksmen: TroopStats
    
    @classmethod
    def from_dict(cls, data: Dict[str, List[float]]) -> "Stats":
        return cls(
            infantry=TroopStats(
                attack=data["infantry"][0],
                defense=data["infantry"][1],
                lethality=data["infantry"][2],
                health=data["infantry"][3]
            ),
            lancer=TroopStats(
                attack=data["lancer"][0],
                defense=data["lancer"][1],
                lethality=data["lancer"][2],
                health=data["lancer"][3]
            ),
            marksmen=TroopStats(
                attack=data["marksman"][0],
                defense=data["marksman"][1],
                lethality=data["marksman"][2],
                health=data["marksman"][3]
            )
        )


class BonusOverviewOutput(BaseModel):
    infantry: TroopStats = Field(..., description="Infantry stats [attack, defense, lethality, health]")
    lancers: TroopStats = Field(..., description="Lancer stats [attack, defense, lethality, health]")
    marksmen: TroopStats = Field(..., description="Marksman stats [attack, defense, lethality, health]")
    
    @classmethod
    def from_stats_dict(cls, stats: Dict[str, List[float]]) -> "BonusOverviewOutput":
        return cls(
            infantry=TroopStats(
                attack=stats["infantry"][0],
                defense=stats["infantry"][1],
                lethality=stats["infantry"][2],
                health=stats["infantry"][3]
            ),
            lancers=TroopStats(
                attack=stats["lancers"][0],
                defense=stats["lancers"][1],
                lethality=stats["lancers"][2],
                health=stats["lancers"][3]
            ),
            marksmen=TroopStats(
                attack=stats["marksmen"][0],
                defense=stats["marksmen"][1],
                lethality=stats["marksmen"][2],
                health=stats["marksmen"][3]
            )
        )


class BattleReportOutput(BaseModel):
    left_stats: Stats = Field(..., description="Left side stats by troop type")
    right_stats: Stats = Field(..., description="Right side stats by troop type")
