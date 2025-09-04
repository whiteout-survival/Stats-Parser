from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from bonus_overview import parse_bonus_overview
from battle_report import (
    parse_battle_report,
)
from schemas.inputs import (
    ReadStatsFromReportRequest,
    ReadStatsFromBonusOverviewRequest,
)
from schemas.outputs import (
    Stats,
    BonusOverviewOutput,
    BattleReportOutput,
    BattleOutcome,
)
from schemas.errors import ErrorResponse, ErrorDetail
from error_messages import missing_page_message_from_value_error

app = FastAPI(title="Report Reader API", version="1.0")

allowed_origins = ["https://stats-parser.neptunedevs.com", "http://stats-parser.neptunedevs.com", "https://sim.tundra.land", "sim.tundra.land", "localhost:8000"]
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Common error responses to attach to routes
COMMON_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        ErrorDetail(loc=list(err.get("loc", [])), msg=err.get("msg"), type=err.get("type"))
        for err in exc.errors()
    ]
    payload = ErrorResponse(code="validation_error", detail="Validation failed", errors=details)
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail_str = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    code = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        422: "validation_error",
        429: "rate_limited",
        500: "internal_server_error",
    }.get(exc.status_code, "error")
    payload = ErrorResponse(code=code, detail=detail_str)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Convert domain ValueErrors into 400 responses with friendly messages."""
    friendly = missing_page_message_from_value_error(exc)
    payload = ErrorResponse(code="bad_request", detail=friendly or str(exc))
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    payload = ErrorResponse(code="internal_server_error", detail="An unexpected error occurred")
    return JSONResponse(status_code=500, content=payload.model_dump())

 

@app.post(
    "/api/v1/read_bonus_overview",
    response_model=BonusOverviewOutput,
    responses=COMMON_ERROR_RESPONSES,
)
def read_bonus_overview(request: ReadStatsFromBonusOverviewRequest) -> BonusOverviewOutput:
    images_b64 = [img.image_data for img in request.images]
    stats = parse_bonus_overview(images_b64, request.ocr_engine)
    return BonusOverviewOutput.from_stats_dict(stats)

@app.post(
    "/api/v1/read_battle_report",
    response_model=BattleReportOutput,
    responses=COMMON_ERROR_RESPONSES,
)
def read_battle_report(request: ReadStatsFromReportRequest) -> BattleReportOutput:
    images_b64 = [img.image_data for img in request.images]
    stats, outcome = parse_battle_report(
        images_b64=images_b64,
        ocr_engine=request.ocr_engine,
        stats_only=request.stats_only,
    )
    return BattleReportOutput(
        left_stats=Stats.from_dict(stats["left"]),
        right_stats=Stats.from_dict(stats["right"]),
        troops_outcome=BattleOutcome.from_dict(outcome) if outcome is not None else None,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8001,
    )
