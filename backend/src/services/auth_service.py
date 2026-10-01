"""
Authentication business logic.
Depends on UserRepository; does NOT import FastAPI or HTTP concerns.
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictError, UnauthorizedError
from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    needs_rehash,
    verify_password,
)
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.auth import AuthResponse, UserOut


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = UserRepository(db)
        self._db = db

    async def signup(self, email: str, password: str) -> AuthResponse:
        if await self._repo.email_exists(email):
            raise ConflictError("An account with this email already exists.")

        hashed = hash_password(password)
        user = await self._repo.create(email=email, hashed_password=hashed)

        return self._build_auth_response(user)

    async def login(self, email: str, password: str) -> AuthResponse:
        user = await self._repo.get_by_email(email)

        # Constant-time failure path — always call verify even if user not found
        # to prevent timing-based email enumeration
        dummy_hash = "$argon2id$v=19$m=65536,t=2,p=2$placeholder"
        stored_hash = user.hashed_password if user else dummy_hash

        if not verify_password(password, stored_hash) or not user:
            raise UnauthorizedError("Invalid email or password.")

        if not user.is_active:
            raise UnauthorizedError("This account has been deactivated.")

        # Opportunistic rehash if parameters changed
        if needs_rehash(user.hashed_password):
            await self._repo.update_password(user, hash_password(password))

        return self._build_auth_response(user)

    async def refresh(self, refresh_token: str) -> tuple[str, UserOut]:
        """Validate refresh token and issue new access token."""
        from jose import JWTError

        try:
            payload = decode_token(refresh_token, expected_type="refresh")
        except JWTError as exc:
            raise UnauthorizedError("Invalid or expired refresh token.") from exc

        user_id = uuid.UUID(payload["sub"])
        user = await self._repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive.")

        new_access = create_access_token(str(user.id))
        return new_access, UserOut.model_validate(user)

    async def get_current_user(self, access_token: str) -> User:
        from jose import JWTError

        try:
            payload = decode_token(access_token, expected_type="access")
        except JWTError as exc:
            raise UnauthorizedError("Invalid or expired access token.") from exc

        user_id = uuid.UUID(payload["sub"])
        user = await self._repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive.")

        return user

    # ── Private ───────────────────────────────────────────────────────────

    def _build_auth_response(self, user: User) -> AuthResponse:
        access_token = create_access_token(str(user.id))
        return AuthResponse(
            user=UserOut.model_validate(user),
            access_token=access_token,
        )
