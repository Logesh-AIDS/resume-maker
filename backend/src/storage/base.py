"""
Storage provider abstraction.

Keeps all file I/O behind a clean interface so local ↔ S3 swap
requires only an env var change, no code changes in services.

Paths are always relative, forward-slash strings (e.g. "uploads/user-id/file.pdf").
The provider resolves them to the actual location.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class StoredFile:
    """Result returned after a successful store operation."""
    path: str           # relative storage path (used as the DB reference)
    size_bytes: int
    content_type: str


class StorageProvider(ABC):

    @abstractmethod
    async def save(
        self,
        data: bytes,
        path: str,
        content_type: str = "application/octet-stream",
    ) -> StoredFile:
        """
        Persist bytes at the given relative path.
        Creates intermediate directories if needed.
        Overwrites if path already exists.
        """
        ...

    @abstractmethod
    async def read(self, path: str) -> bytes:
        """Read a file by its relative storage path. Raises FileNotFoundError if missing."""
        ...

    @abstractmethod
    async def delete(self, path: str) -> None:
        """Delete a file. Silently ignores missing files."""
        ...

    @abstractmethod
    async def exists(self, path: str) -> bool:
        """Return True if the path exists in storage."""
        ...

    @abstractmethod
    async def get_url(self, path: str, expires_in: int = 3600) -> str:
        """
        Return a URL to access the file.
        - Local: a signed application URL (served by FastAPI).
        - S3: a pre-signed S3 URL.
        """
        ...
