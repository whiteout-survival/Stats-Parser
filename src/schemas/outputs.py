from typing import Dict, List
from pydantic import BaseModel, Field


class Stats(BaseModel):
    infantry: List[float] = Field(default=[0.0, 0.0, 0.0, 0.0], description="Infantry stats [attack, defense, lethality, health]")
    lancer: List[float] = Field(default=[0.0, 0.0, 0.0, 0.0], description="Lancer stats [attack, defense, lethality, health]")
    marksman: List[float] = Field(default=[0.0, 0.0, 0.0, 0.0], description="Marksman stats [attack, defense, lethality, health]")

    @classmethod
    def from_dict(cls, data: Dict[str, List[float]]) -> "Stats":
        return cls(
            infantry=[data["infantry"][0], data["infantry"][1], data["infantry"][2], data["infantry"][3]],
            lancer=[data["lancer"][0], data["lancer"][1], data["lancer"][2], data["lancer"][3]],
            marksman=[data["marksman"][0], data["marksman"][1], data["marksman"][2], data["marksman"][3]],
        )


class TroopOutcome(BaseModel):
    initial_troops: int = Field(default=0, description="Initial number of troops")
    losses: int = Field(default=0, description="Number of troops lost")
    injured: int = Field(default=0, description="Number of injured troops")
    lightly_injured: int = Field(default=0, description="Number of lightly injured troops")
    survivors: int = Field(default=0, description="Number of surviving troops")

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "TroopOutcome":
        return cls(
            initial_troops=data["initial_troops"],
            losses=data["losses"],
            injured=data["injured"],
            lightly_injured=data["lightly_injured"],
            survivors=data["survivors"],
        )


class BattleOutcome(BaseModel):
    left: TroopOutcome = Field(..., description="Left side troop outcome")
    right: TroopOutcome = Field(..., description="Right side troop outcome")

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, int]] | None) -> "BattleOutcome | None":
        if data:
            return cls(
                left=TroopOutcome.from_dict(data["left"]),
                right=TroopOutcome.from_dict(data["right"]),
            )
        else:
            return None


class BonusOverviewOutput(BaseModel):
    stats: Stats = Field(..., description="Stats by troop type")

    @classmethod
    def from_stats_dict(cls, stats: Dict[str, List[float]]) -> "BonusOverviewOutput":
        return cls(stats=Stats.from_dict(stats))


class BattleReportOutput(BaseModel):
    troops_outcome: BattleOutcome | None = Field(..., description="Troop outcomes for both sides")
    left_stats: Stats = Field(..., description="Left side stats by troop type")
    right_stats: Stats = Field(..., description="Right side stats by troop type")

