"""
Application-level exception hierarchy.
All domain errors inherit from AppError so the global handler can catch them uniformly.
"""
from http import HTTPStatus


class AppError(Exception):
    """Base class for all application errors."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    default_message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    default_message = "Resource not found."


class ConflictError(AppError):
    status_code = HTTPStatus.CONFLICT
    default_message = "Resource already exists."


class UnauthorizedError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    default_message = "Authentication required."


class ForbiddenError(AppError):
    status_code = HTTPStatus.FORBIDDEN
    default_message = "You do not have permission to access this resource."


class ValidationError(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    default_message = "Validation failed."


class FileUploadError(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    default_message = "File upload failed."


class DocumentParseError(AppError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    default_message = "Could not parse the uploaded document."


class AIServiceError(AppError):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE
    default_message = "AI service temporarily unavailable."


class RenderingError(AppError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    default_message = "Resume rendering failed."
