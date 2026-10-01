"""
Profile data access layer.
All DB queries for profiles and sub-sections live here.
Ownership is enforced at this layer — never rely solely on route-level checks.
"""
import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.profile import (
    Profile, Education, Experience, Project, Skill, Achievement
)


class ProfileRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    # ── Profile ───────────────────────────────────────────────────────────────

    async def get_by_user_id(self, user_id: uuid.UUID) -> Profile | None:
        """Fetch full profile with all relations eager-loaded."""
        result = await self._db.execute(
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(
                selectinload(Profile.education),
                selectinload(Profile.experiences),
                selectinload(Profile.projects),
                selectinload(Profile.skills),
                selectinload(Profile.achievements),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, profile_id: uuid.UUID) -> Profile | None:
        result = await self._db.execute(
            select(Profile).where(Profile.id == profile_id)
        )
        return result.scalar_one_or_none()

    async def update_personal_info(
        self, profile: Profile, data: dict
    ) -> Profile:
        for key, value in data.items():
            setattr(profile, key, value)
        await self._db.flush()
        return profile

    async def update_completion(
        self, profile: Profile, pct: int
    ) -> Profile:
        profile.completion_pct = pct
        await self._db.flush()
        return profile

    # ── Education ─────────────────────────────────────────────────────────────

    async def get_education(
        self, education_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Education | None:
        result = await self._db.execute(
            select(Education).where(
                Education.id == education_id,
                Education.profile_id == profile_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_education(
        self, profile_id: uuid.UUID, data: dict
    ) -> Education:
        edu = Education(profile_id=profile_id, **data)
        self._db.add(edu)
        await self._db.flush()
        return edu

    async def update_education(
        self, edu: Education, data: dict
    ) -> Education:
        for key, value in data.items():
            setattr(edu, key, value)
        await self._db.flush()
        return edu

    async def delete_education(self, edu: Education) -> None:
        await self._db.delete(edu)
        await self._db.flush()

    # ── Experience ────────────────────────────────────────────────────────────

    async def get_experience(
        self, exp_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Experience | None:
        result = await self._db.execute(
            select(Experience).where(
                Experience.id == exp_id,
                Experience.profile_id == profile_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_experience(
        self, profile_id: uuid.UUID, data: dict
    ) -> Experience:
        exp = Experience(profile_id=profile_id, **data)
        self._db.add(exp)
        await self._db.flush()
        return exp

    async def update_experience(
        self, exp: Experience, data: dict
    ) -> Experience:
        for key, value in data.items():
            setattr(exp, key, value)
        await self._db.flush()
        return exp

    async def delete_experience(self, exp: Experience) -> None:
        await self._db.delete(exp)
        await self._db.flush()

    # ── Project ───────────────────────────────────────────────────────────────

    async def get_project(
        self, project_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Project | None:
        result = await self._db.execute(
            select(Project).where(
                Project.id == project_id,
                Project.profile_id == profile_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_project(
        self, profile_id: uuid.UUID, data: dict
    ) -> Project:
        proj = Project(profile_id=profile_id, **data)
        self._db.add(proj)
        await self._db.flush()
        return proj

    async def update_project(
        self, proj: Project, data: dict
    ) -> Project:
        for key, value in data.items():
            setattr(proj, key, value)
        await self._db.flush()
        return proj

    async def delete_project(self, proj: Project) -> None:
        await self._db.delete(proj)
        await self._db.flush()

    # ── Skill ─────────────────────────────────────────────────────────────────

    async def get_skill(
        self, skill_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Skill | None:
        result = await self._db.execute(
            select(Skill).where(
                Skill.id == skill_id,
                Skill.profile_id == profile_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_skill(
        self, profile_id: uuid.UUID, data: dict
    ) -> Skill:
        skill = Skill(profile_id=profile_id, **data)
        self._db.add(skill)
        await self._db.flush()
        return skill

    async def create_skills_bulk(
        self, profile_id: uuid.UUID, items: list[dict]
    ) -> list[Skill]:
        skills = [Skill(profile_id=profile_id, **d) for d in items]
        self._db.add_all(skills)
        await self._db.flush()
        return skills

    async def update_skill(self, skill: Skill, data: dict) -> Skill:
        for key, value in data.items():
            setattr(skill, key, value)
        await self._db.flush()
        return skill

    async def delete_skill(self, skill: Skill) -> None:
        await self._db.delete(skill)
        await self._db.flush()

    async def delete_all_skills(self, profile_id: uuid.UUID) -> None:
        await self._db.execute(
            delete(Skill).where(Skill.profile_id == profile_id)
        )
        await self._db.flush()

    # ── Achievement ───────────────────────────────────────────────────────────

    async def get_achievement(
        self, ach_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Achievement | None:
        result = await self._db.execute(
            select(Achievement).where(
                Achievement.id == ach_id,
                Achievement.profile_id == profile_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_achievement(
        self, profile_id: uuid.UUID, data: dict
    ) -> Achievement:
        ach = Achievement(profile_id=profile_id, **data)
        self._db.add(ach)
        await self._db.flush()
        return ach

    async def update_achievement(
        self, ach: Achievement, data: dict
    ) -> Achievement:
        for key, value in data.items():
            setattr(ach, key, value)
        await self._db.flush()
        return ach

    async def delete_achievement(self, ach: Achievement) -> None:
        await self._db.delete(ach)
        await self._db.flush()
