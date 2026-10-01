"""
File validation and path utilities for uploads.
"""
import mimetypes
import uuid
from pathlib import PurePosixPath

from src.core.config import get_settings
from src.core.exceptions import FileUploadError
from src.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Magic bytes for supported file types
_MAGIC_BYTES: dict[str, bytes] = {
    ".pdf":  b"%PDF",
    ".docx": b"PK\x03\x04",  # ZIP-based (OOXML)
}


def validate_upload(filename: str, data: bytes) -> str:
    """
    Validate file extension, size, and magic bytes.
    Returns the validated extension.
    Raises FileUploadError on any violation.
    """
    if not filename:
        raise FileUploadError("Filename is required.")

    suffix = PurePosixPath(filename).suffix.lower()

    if suffix not in settings.allowed_upload_extensions:
        allowed = ", ".join(settings.allowed_upload_extensions)
        raise FileUploadError(
            f"File type '{suffix}' is not supported. Allowed types: {allowed}."
        )

    if len(data) > settings.max_upload_size_bytes:
        mb = settings.max_upload_size_bytes // (1024 * 1024)
        raise FileUploadError(f"File exceeds the maximum allowed size of {mb} MB.")

    if len(data) == 0:
        raise FileUploadError("Uploaded file is empty.")

    # Validate magic bytes — never trust the extension alone
    expected_magic = _MAGIC_BYTES.get(suffix)
    if expected_magic and not data.startswith(expected_magic):
        raise FileUploadError(
            f"File content does not match the expected format for '{suffix}'. "
            "Ensure you are uploading a real PDF or DOCX file."
        )

    return suffix


def build_upload_path(user_id: str, category: str, filename: str) -> str:
    """
    Build a deterministic, collision-resistant storage path.
    Format: uploads/{category}/{user_id}/{uuid}{suffix}
    """
    suffix = PurePosixPath(filename).suffix.lower()
    unique_name = f"{uuid.uuid4()}{suffix}"
    return f"uploads/{category}/{user_id}/{unique_name}"


def content_type_for(suffix: str) -> str:
    mime, _ = mimetypes.guess_type(f"file{suffix}")
    return mime or "application/octet-stream"
