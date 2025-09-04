"""
Schemas package exposing input, output, and error models.

This module splits the previous monolithic `schemas.py` into
`inputs.py`, `outputs.py`, and `errors.py` for clarity.
"""

# Optional re-exports for convenience
from .inputs import (
    ImageData,
    ReadStatsRequest,
    ReadStatsFromReportRequest,
    ReadStatsFromBonusOverviewRequest,
)

from .outputs import (
    Stats,
    TroopOutcome,
    BattleOutcome,
    BonusOverviewOutput,
    BattleReportOutput,
)

from .errors import (
    ErrorResponse,
)

__all__ = [
    # inputs
    "ImageData",
    "ReadStatsRequest",
    "ReadStatsFromReportRequest",
    "ReadStatsFromBonusOverviewRequest",
    # outputs
    "Stats",
    "TroopOutcome",
    "BattleOutcome",
    "BonusOverviewOutput",
    "BattleReportOutput",
    # errors
    "ErrorResponse",
]

