"""
Profile business logic.
Owns completion calculation, section CRUD coordination, and profile enrichment.
No HTTP/FastAPI imports here — pure domain logic.
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ForbiddenError, NotFoundError
from src.core.logging import get_logger
from src.models.profile import (
    Achievement, Education, Experience, Profile, Project, Skill
)
from src.repositories.profile_repository import ProfileRepository
from src.schemas.profile import (
    AchievementIn, CompletionOut, EducationIn, ExperienceIn,
    PersonalInfoIn, ProjectIn, SkillBulkIn, SkillIn
)

logger = get_logger(__name__)


class ProfileService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = ProfileRepository(db)

    # ── Profile ───────────────────────────────────────────────────────────────

    async def get_profile(self, user_id: uuid.UUID) -> Profile:
        """Return the user's profile (with all sub-sections loaded)."""
        profile = await self._repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found. Please contact support.")
        return profile

    async def update_personal_info(
        self, user_id: uuid.UUID, data: PersonalInfoIn
    ) -> Profile:
        profile = await self._get_owned_profile(user_id)

        update_dict = data.model_dump(exclude_unset=False)
        # Convert ExternalLinkIn objects to plain dicts for JSONB storage
        if "other_links" in update_dict:
            update_dict["other_links"] = [
                lnk.model_dump() if hasattr(lnk, "model_dump") else lnk
                for lnk in update_dict["other_links"]
            ]

        await self._repo.update_personal_info(profile, update_dict)
        await self._refresh_completion(profile)
        logger.info("profile_personal_info_updated", user_id=str(user_id))
        return await self._repo.get_by_user_id(user_id)  # type: ignore[return-value]

    async def get_completion(self, user_id: uuid.UUID) -> CompletionOut:
        profile = await self.get_profile(user_id)
        return _calculate_completion(profile)

    # ── Education ─────────────────────────────────────────────────────────────

    async def add_education(
        self, user_id: uuid.UUID, data: EducationIn
    ) -> Education:
        profile = await self._get_owned_profile(user_id)
        edu = await self._repo.create_education(
            profile.id, data.model_dump()
        )
        await self._refresh_completion(profile)
        return edu

    async def update_education(
        self, user_id: uuid.UUID, edu_id: uuid.UUID, data: EducationIn
    ) -> Education:
        profile = await self._get_owned_profile(user_id)
        edu = await self._get_education(edu_id, profile.id)
        updated = await self._repo.update_education(edu, data.model_dump())
        await self._refresh_completion(profile)
        return updated

    async def delete_education(
        self, user_id: uuid.UUID, edu_id: uuid.UUID
    ) -> None:
        profile = await self._get_owned_profile(user_id)
        edu = await self._get_education(edu_id, profile.id)
        await self._repo.delete_education(edu)
        await self._refresh_completion(profile)

    # ── Experience ────────────────────────────────────────────────────────────

    async def add_experience(
        self, user_id: uuid.UUID, data: ExperienceIn
    ) -> Experience:
        profile = await self._get_owned_profile(user_id)
        exp = await self._repo.create_experience(
            profile.id, data.model_dump()
        )
        await self._refresh_completion(profile)
        return exp

    async def update_experience(
        self, user_id: uuid.UUID, exp_id: uuid.UUID, data: ExperienceIn
    ) -> Experience:
        profile = await self._get_owned_profile(user_id)
        exp = await self._get_experience(exp_id, profile.id)
        updated = await self._repo.update_experience(exp, data.model_dump())
        await self._refresh_completion(profile)
        return updated

    async def delete_experience(
        self, user_id: uuid.UUID, exp_id: uuid.UUID
    ) -> None:
        profile = await self._get_owned_profile(user_id)
        exp = await self._get_experience(exp_id, profile.id)
        await self._repo.delete_experience(exp)
        await self._refresh_completion(profile)

    # ── Projects ──────────────────────────────────────────────────────────────

    async def add_project(
        self, user_id: uuid.UUID, data: ProjectIn
    ) -> Project:
        profile = await self._get_owned_profile(user_id)
        proj = await self._repo.create_project(
            profile.id, data.model_dump()
        )
        await self._refresh_completion(profile)
        return proj

    async def update_project(
        self, user_id: uuid.UUID, proj_id: uuid.UUID, data: ProjectIn
    ) -> Project:
        profile = await self._get_owned_profile(user_id)
        proj = await self._get_project(proj_id, profile.id)
        updated = await self._repo.update_project(proj, data.model_dump())
        await self._refresh_completion(profile)
        return updated

    async def delete_project(
        self, user_id: uuid.UUID, proj_id: uuid.UUID
    ) -> None:
        profile = await self._get_owned_profile(user_id)
        proj = await self._get_project(proj_id, profile.id)
        await self._repo.delete_project(proj)
        await self._refresh_completion(profile)

    # ── Skills ────────────────────────────────────────────────────────────────

    async def add_skill(
        self, user_id: uuid.UUID, data: SkillIn
    ) -> Skill:
        profile = await self._get_owned_profile(user_id)
        skill = await self._repo.create_skill(profile.id, data.model_dump())
        await self._refresh_completion(profile)
        return skill

    async def add_skills_bulk(
        self, user_id: uuid.UUID, data: SkillBulkIn
    ) -> list[Skill]:
        profile = await self._get_owned_profile(user_id)
        skills = await self._repo.create_skills_bulk(
            profile.id, [s.model_dump() for s in data.skills]
        )
        await self._refresh_completion(profile)
        return skills

    async def update_skill(
        self, user_id: uuid.UUID, skill_id: uuid.UUID, data: SkillIn
    ) -> Skill:
        profile = await self._get_owned_profile(user_id)
        skill = await self._get_skill(skill_id, profile.id)
        updated = await self._repo.update_skill(skill, data.model_dump())
        await self._refresh_completion(profile)
        return updated

    async def delete_skill(
        self, user_id: uuid.UUID, skill_id: uuid.UUID
    ) -> None:
        profile = await self._get_owned_profile(user_id)
        skill = await self._get_skill(skill_id, profile.id)
        await self._repo.delete_skill(skill)
        await self._refresh_completion(profile)

    # ── Achievements ──────────────────────────────────────────────────────────

    async def add_achievement(
        self, user_id: uuid.UUID, data: AchievementIn
    ) -> Achievement:
        profile = await self._get_owned_profile(user_id)
        ach = await self._repo.create_achievement(
            profile.id, data.model_dump()
        )
        await self._refresh_completion(profile)
        return ach

    async def update_achievement(
        self, user_id: uuid.UUID, ach_id: uuid.UUID, data: AchievementIn
    ) -> Achievement:
        profile = await self._get_owned_profile(user_id)
        ach = await self._get_achievement(ach_id, profile.id)
        updated = await self._repo.update_achievement(ach, data.model_dump())
        await self._refresh_completion(profile)
        return updated

    async def delete_achievement(
        self, user_id: uuid.UUID, ach_id: uuid.UUID
    ) -> None:
        profile = await self._get_owned_profile(user_id)
        ach = await self._get_achievement(ach_id, profile.id)
        await self._repo.delete_achievement(ach)
        await self._refresh_completion(profile)

    # ── Private helpers ───────────────────────────────────────────────────────

    async def _get_owned_profile(self, user_id: uuid.UUID) -> Profile:
        """Fetch lightweight profile (no sub-sections) for mutation operations."""
        profile = await self._repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundError("Profile not found.")
        return profile

    async def _get_education(
        self, edu_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Education:
        edu = await self._repo.get_education(edu_id, profile_id)
        if not edu:
            raise NotFoundError("Education entry not found.")
        return edu

    async def _get_experience(
        self, exp_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Experience:
        exp = await self._repo.get_experience(exp_id, profile_id)
        if not exp:
            raise NotFoundError("Experience entry not found.")
        return exp

    async def _get_project(
        self, proj_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Project:
        proj = await self._repo.get_project(proj_id, profile_id)
        if not proj:
            raise NotFoundError("Project not found.")
        return proj

    async def _get_skill(
        self, skill_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Skill:
        skill = await self._repo.get_skill(skill_id, profile_id)
        if not skill:
            raise NotFoundError("Skill not found.")
        return skill

    async def _get_achievement(
        self, ach_id: uuid.UUID, profile_id: uuid.UUID
    ) -> Achievement:
        ach = await self._repo.get_achievement(ach_id, profile_id)
        if not ach:
            raise NotFoundError("Achievement not found.")
        return ach

    async def _refresh_completion(self, profile: Profile) -> None:
        """Reload profile with sub-sections then persist new completion %."""
        fresh = await self._repo.get_by_user_id(profile.user_id)
        if fresh:
            result = _calculate_completion(fresh)
            await self._repo.update_completion(fresh, result.overall)


# ── Completion calculator (pure function — deterministic, no AI) ──────────────

def _calculate_completion(profile: Profile) -> CompletionOut:
    """
    Calculate profile completion percentage.
    Each section is either complete (100) or incomplete (0).
    Overall = average across all sections.
    """
    sections: dict[str, int] = {}

    # Personal info — requires at minimum name + email + title
    personal_fields = [
        profile.full_name,
        profile.email,
        profile.professional_title,
    ]
    sections["personal_info"] = 100 if all(personal_fields) else 0

    # Summary
    sections["summary"] = 100 if profile.summary and len(profile.summary) > 20 else 0

    # Education — at least one entry
    sections["education"] = 100 if profile.education else 0

    # Experience — at least one entry with responsibilities
    has_exp = any(
        bool(e.responsibilities) for e in profile.experiences
    )
    sections["experience"] = 100 if has_exp else 0

    # Projects — at least one entry with description
    has_proj = any(
        bool(p.description) for p in profile.projects
    )
    sections["projects"] = 100 if has_proj else 0

    # Skills — at least 3 skills
    sections["skills"] = 100 if len(profile.skills) >= 3 else 0

    # Achievements — optional but tracked
    sections["achievements"] = 100 if profile.achievements else 0

    # Contact info — phone or portfolio
    sections["contact"] = 100 if (profile.phone or profile.portfolio_url or
                                   profile.linkedin_url or profile.github_url) else 0

    completed = sum(1 for v in sections.values() if v == 100)
    overall = round((completed / len(sections)) * 100)

    missing = [k for k, v in sections.items() if v == 0]

    return CompletionOut(
        overall=overall,
        sections=sections,
        missing=missing,
    )
