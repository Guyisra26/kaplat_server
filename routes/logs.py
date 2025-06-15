from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from init_services import request_logger, stack_logger, independent_logger
import logging

router = APIRouter()

logger_map = {
    "request-logger": request_logger,
    "stack-logger": stack_logger,
    "independent-logger": independent_logger,
}

@router.get("/logs/level", response_model=None)
def get_log_level(logger_name: str = Query(..., alias="logger-name")) -> PlainTextResponse:
    logger = logger_map.get(logger_name)
    if logger is None:
        return PlainTextResponse(f"Logger '{logger_name}' not found", status_code=404)

    level = logging.getLevelName(logger.level)
    return PlainTextResponse(level.upper())

@router.put("/logs/level", response_model=None)
def set_log_level(
    logger_name: str = Query(..., alias="logger-name"),
    logger_level: str = Query(..., alias="logger-level")) -> PlainTextResponse:
    logger = logger_map.get(logger_name)
    if logger is None:
        return PlainTextResponse(f"Logger '{logger_name}' not found", status_code=404)

    try:
        level = logger_level.upper()
        logger.setLevel(getattr(logging, level))
        return PlainTextResponse(level)
    except AttributeError:
        return PlainTextResponse(f"Invalid log level '{logger_level}'", status_code=400)
