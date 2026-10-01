"""
User data access — all DB queries for users live here.
No business logic; no HTTP concerns.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.profile import Profile


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        result = await self._db.execute(
            select(User.id).where(User.email == email.lower())
        )
        return result.scalar_one_or_none() is not None

    async def create(self, email: str, hashed_password: str) -> User:
        user = User(email=email.lower(), hashed_password=hashed_password)
        self._db.add(user)
        await self._db.flush()  # get ID without committing
        # Auto-create empty profile
        profile = Profile(user_id=user.id, other_links=[], completion_pct=0)
        self._db.add(profile)
        await self._db.flush()
        return user

    async def update_password(self, user: User, hashed_password: str) -> User:
        user.hashed_password = hashed_password
        await self._db.flush()
        return user

    async def deactivate(self, user: User) -> User:
        user.is_active = False
        await self._db.flush()
        return user
