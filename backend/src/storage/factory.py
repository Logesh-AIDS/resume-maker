"""
Storage provider factory — returns the configured provider.
"""
from functools import lru_cache

from src.core.config import get_settings
from src.core.exceptions import AppError
from src.storage.base import StorageProvider


@lru_cache(maxsize=1)
def get_storage_provider() -> StorageProvider:
    settings = get_settings()

    if settings.storage_provider == "local":
        from src.storage.local import LocalStorageProvider
        return LocalStorageProvider()

    if settings.storage_provider == "s3":
        # S3 provider is a post-MVP addition
        raise AppError("S3 storage provider is not yet implemented. Use STORAGE_PROVIDER=local.")

    raise AppError(f"Unknown storage provider: '{settings.storage_provider}'.")
