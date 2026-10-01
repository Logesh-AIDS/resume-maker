"""
Local filesystem storage provider.
Used in development. Files are stored under LOCAL_STORAGE_PATH (default: ./uploads).

Security notes:
  - Paths are sanitised to prevent directory traversal.
  - Files are stored outside the web root (not publicly served directly).
  - Download access is via signed application URLs with expiry.
"""
import hashlib
import hmac
import time
from pathlib import Path

import aiofiles
import aiofiles.os

from src.core.config import get_settings
from src.core.exceptions import FileUploadError
from src.core.logging import get_logger
from src.storage.base import StoredFile, StorageProvider

logger = get_logger(__name__)
settings = get_settings()


class LocalStorageProvider(StorageProvider):
    """Async local filesystem storage."""

    def __init__(self) -> None:
        self._root = Path(settings.local_storage_path).resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        logger.info("local_storage_initialized", root=str(self._root))

    def _safe_path(self, relative: str) -> Path:
        """
        Resolve relative path under storage root.
        Raises FileUploadError on directory traversal attempts.
        """
        resolved = (self._root / relative).resolve()
        if not str(resolved).startswith(str(self._root)):
            raise FileUploadError("Invalid storage path — directory traversal detected.")
        return resolved

    async def save(
        self,
        data: bytes,
        path: str,
        content_type: str = "application/octet-stream",
    ) -> StoredFile:
        dest = self._safe_path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(dest, "wb") as f:
            await f.write(data)

        size = dest.stat().st_size
        logger.debug("storage_file_saved", path=path, size_bytes=size)
        return StoredFile(path=path, size_bytes=size, content_type=content_type)

    async def read(self, path: str) -> bytes:
        src = self._safe_path(path)
        if not src.exists():
            raise FileNotFoundError(f"Storage file not found: {path}")
        async with aiofiles.open(src, "rb") as f:
            return await f.read()

    async def delete(self, path: str) -> None:
        target = self._safe_path(path)
        if target.exists():
            target.unlink()
            logger.debug("storage_file_deleted", path=path)

    async def exists(self, path: str) -> bool:
        return self._safe_path(path).exists()

    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        """
        Generate a time-limited HMAC-signed URL for the file.
        The signature is validated by the /storage/download endpoint.
        """
        expires_at = int(time.time()) + expires_in
        signature = self._sign(path, expires_at)
        return (
            f"/api/v1/storage/download"
            f"?path={path}&expires={expires_at}&sig={signature}"
        )

    def verify_url(self, path: str, expires: int, sig: str) -> bool:
        """Validate a signed download URL."""
        if time.time() > expires:
            return False
        expected = self._sign(path, expires)
        return hmac.compare_digest(expected, sig)

    def _sign(self, path: str, expires: int) -> str:
        key = settings.secret_key.encode()
        message = f"{path}:{expires}".encode()
        return hmac.new(key, message, hashlib.sha256).hexdigest()
