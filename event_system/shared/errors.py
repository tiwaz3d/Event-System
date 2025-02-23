from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse


class EventSystemException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
        message: str = "Validation error",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


async def event_exception_handler(request: Request, exc: EventSystemException):
    return JSONResponse(
        status_code=exc.status_code, content={"status": "error", "message": exc.message, "details": exc.details}
    )
