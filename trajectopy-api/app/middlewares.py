import logging

from app.exceptions import (ResultNotFoundException,
                            SessionAlreadyExistsException,
                            SessionNotFoundException,
                            TrajectoryNotFoundException)
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("root")

EXCEPTION_MAPPING = {
    TrajectoryNotFoundException: 404,
    SessionNotFoundException: 404,
    SessionAlreadyExistsException: 409,
    ResultNotFoundException: 404,
    ValueError: 400,
}


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        logger.info(f"Request: {request.method} {request.url}")
        return await call_next(request)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(
            status_code=EXCEPTION_MAPPING.get(type(e), 500),
            content={"message": str(e)},
            headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        )
