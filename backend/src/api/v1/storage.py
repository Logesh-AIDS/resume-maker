"""
Storage download endpoint.
Serves locally stored files via signed time-limited URLs.
"""
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response

from src.core.config import get_settings
from src.core.logging import get_logger
from src.storage.factory import get_storage_provider

router = APIRouter(prefix="/storage", tags=["storage"])
logger = get_logger(__name__)
settings = get_settings()


@router.get("/download", summary="Download a file via signed URL")
async def download_file(
    path: str = Query(..., description="Relative storage path"),
    expires: int = Query(..., description="Unix timestamp expiry"),
    sig: str = Query(..., description="HMAC signature"),
) -> Response:
    """
    Validate the signed URL and stream the file bytes.
    Only works with LocalStorageProvider — S3 uses direct pre-signed URLs.
    """
    if settings.storage_provider != "local":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Direct download only supported for local storage.",
        )

    from src.storage.local import LocalStorageProvider

    provider = get_storage_provider()
    if not isinstance(provider, LocalStorageProvider):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Storage misconfiguration.")

    if not provider.verify_url(path, expires, sig):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired download link.",
        )

    try:
        data = await provider.read(path)
    except FileNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found.")

    # Determine content-type from extension
    from src.storage.utils import content_type_for
    from pathlib import PurePosixPath

    suffix = PurePosixPath(path).suffix.lower()
    content_type = content_type_for(suffix)

    filename = PurePosixPath(path).name
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
