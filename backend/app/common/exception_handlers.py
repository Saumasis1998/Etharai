import logging
import traceback

from fastapi import Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings

logger = logging.getLogger("hrms_app.exceptions")


async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    logger.warning("HTTP error: %s %s", exc.status_code, exc.detail)
    payload = {"error": True, "message": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=payload)


async def generic_exception_handler(request: Request, exc: Exception):
    # Log full traceback
    tb = traceback.format_exc()
    logger.error("Unhandled exception: %s", tb)

    payload = {"error": True, "message": "Internal server error"}
    if settings.debug:
        payload["detail"] = str(exc)
        payload["traceback"] = tb

    return JSONResponse(status_code=500, content=payload)
