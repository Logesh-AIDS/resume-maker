"""
Global exception handlers.
Every unhandled exception is caught here, logged, and returned as a consistent JSON error.
Sensitive information (stack traces, internal details) is never exposed to clients in production.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from src.core.config import get_settings
from src.core.exceptions import AppError
from src.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


def _error_response(status_code: int, detail: str | list) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": detail})


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        """Handle all known application errors with their mapped HTTP status codes."""
        logger.warning(
            "app_error",
            error_type=type(exc).__name__,
            message=exc.message,
            status_code=exc.status_code,
        )
        return _error_response(exc.status_code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic request body validation errors — return field-level detail."""
        errors = [
            {
                "field": ".".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        logger.info("request_validation_error", errors=errors)
        return _error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, errors)

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
        return _error_response(
            status.HTTP_404_NOT_FOUND,
            f"The requested resource '{request.url.path}' was not found.",
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all for unexpected errors — logs full detail, returns generic message."""
        logger.exception(
            "unhandled_error",
            error_type=type(exc).__name__,
            error=str(exc),
            path=request.url.path,
        )
        # Never leak internal error details to clients in production
        detail = str(exc) if settings.is_development else "An internal server error occurred."
        return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
