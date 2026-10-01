"""
Profile API routes.
All routes require authentication. Ownership is enforced in the service layer.
Routes are intentionally thin — they validate input, call the service, return output.
"""
import uuid

from fastapi import APIRouter, Depends, status

from src.api.deps import CurrentUser, DbSession
from src.core.exceptions import NotFoundError, ForbiddenError
from src.schemas.profile import (
    AchievementIn, AchievementOut,
    CompletionOut,
    EducationIn, EducationOut,
    ExperienceIn, ExperienceOut,
    PersonalInfoIn, ProfileOut,
    ProjectIn, ProjectOut,
    SkillBulkIn, SkillIn, SkillOut,
)
from src.schemas.auth import MessageResponse
from src.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])


def _svc(db: DbSession) -> ProfileService:
    return ProfileService(db)


# ── Profile ───────────────────────────────────────────────────────────────────

@router.get("", response_model=ProfileOut, summary="Get my full profile")
async def get_profile(
    current_user: CurrentUser,
    db: DbSession,
) -> ProfileOut:
    svc = _svc(db)
    profile = await svc.get_profile(current_user.id)
    return ProfileOut.model_validate(profile)


@router.put("", response_model=ProfileOut, summary="Update personal info")
async def update_personal_info(
    body: PersonalInfoIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ProfileOut:
    svc = _svc(db)
    profile = await svc.update_personal_info(current_user.id, body)
    return ProfileOut.model_validate(profile)


@router.get(
    "/completion",
    response_model=CompletionOut,
    summary="Get profile completion breakdown",
)
async def get_completion(
    current_user: CurrentUser,
    db: DbSession,
) -> CompletionOut:
    svc = _svc(db)
    return await svc.get_completion(current_user.id)


# ── Education ─────────────────────────────────────────────────────────────────

@router.post(
    "/education",
    response_model=EducationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add education entry",
)
async def add_education(
    body: EducationIn,
    current_user: CurrentUser,
    db: DbSession,
) -> EducationOut:
    svc = _svc(db)
    edu = await svc.add_education(current_user.id, body)
    return EducationOut.model_validate(edu)


@router.put(
    "/education/{education_id}",
    response_model=EducationOut,
    summary="Update education entry",
)
async def update_education(
    education_id: uuid.UUID,
    body: EducationIn,
    current_user: CurrentUser,
    db: DbSession,
) -> EducationOut:
    svc = _svc(db)
    edu = await svc.update_education(current_user.id, education_id, body)
    return EducationOut.model_validate(edu)


@router.delete(
    "/education/{education_id}",
    response_model=MessageResponse,
    summary="Delete education entry",
)
async def delete_education(
    education_id: uuid.UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> MessageResponse:
    svc = _svc(db)
    await svc.delete_education(current_user.id, education_id)
    return MessageResponse(message="Education entry deleted.")


# ── Experience ────────────────────────────────────────────────────────────────

@router.post(
    "/experiences",
    response_model=ExperienceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add experience entry",
)
async def add_experience(
    body: ExperienceIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ExperienceOut:
    svc = _svc(db)
    exp = await svc.add_experience(current_user.id, body)
    return ExperienceOut.model_validate(exp)


@router.put(
    "/experiences/{experience_id}",
    response_model=ExperienceOut,
    summary="Update experience entry",
)
async def update_experience(
    experience_id: uuid.UUID,
    body: ExperienceIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ExperienceOut:
    svc = _svc(db)
    exp = await svc.update_experience(current_user.id, experience_id, body)
    return ExperienceOut.model_validate(exp)


@router.delete(
    "/experiences/{experience_id}",
    response_model=MessageResponse,
    summary="Delete experience entry",
)
async def delete_experience(
    experience_id: uuid.UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> MessageResponse:
    svc = _svc(db)
    await svc.delete_experience(current_user.id, experience_id)
    return MessageResponse(message="Experience entry deleted.")


# ── Projects ──────────────────────────────────────────────────────────────────

@router.post(
    "/projects",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add project",
)
async def add_project(
    body: ProjectIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ProjectOut:
    svc = _svc(db)
    proj = await svc.add_project(current_user.id, body)
    return ProjectOut.model_validate(proj)


@router.put(
    "/projects/{project_id}",
    response_model=ProjectOut,
    summary="Update project",
)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ProjectOut:
    svc = _svc(db)
    proj = await svc.update_project(current_user.id, project_id, body)
    return ProjectOut.model_validate(proj)


@router.delete(
    "/projects/{project_id}",
    response_model=MessageResponse,
    summary="Delete project",
)
async def delete_project(
    project_id: uuid.UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> MessageResponse:
    svc = _svc(db)
    await svc.delete_project(current_user.id, project_id)
    return MessageResponse(message="Project deleted.")


# ── Skills ────────────────────────────────────────────────────────────────────

@router.post(
    "/skills",
    response_model=SkillOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add a single skill",
)
async def add_skill(
    body: SkillIn,
    current_user: CurrentUser,
    db: DbSession,
) -> SkillOut:
    svc = _svc(db)
    skill = await svc.add_skill(current_user.id, body)
    return SkillOut.model_validate(skill)


@router.post(
    "/skills/bulk",
    response_model=list[SkillOut],
    status_code=status.HTTP_201_CREATED,
    summary="Add multiple skills at once",
)
async def add_skills_bulk(
    body: SkillBulkIn,
    current_user: CurrentUser,
    db: DbSession,
) -> list[SkillOut]:
    svc = _svc(db)
    skills = await svc.add_skills_bulk(current_user.id, body)
    return [SkillOut.model_validate(s) for s in skills]


@router.put(
    "/skills/{skill_id}",
    response_model=SkillOut,
    summary="Update a skill",
)
async def update_skill(
    skill_id: uuid.UUID,
    body: SkillIn,
    current_user: CurrentUser,
    db: DbSession,
) -> SkillOut:
    svc = _svc(db)
    skill = await svc.update_skill(current_user.id, skill_id, body)
    return SkillOut.model_validate(skill)


@router.delete(
    "/skills/{skill_id}",
    response_model=MessageResponse,
    summary="Delete a skill",
)
async def delete_skill(
    skill_id: uuid.UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> MessageResponse:
    svc = _svc(db)
    await svc.delete_skill(current_user.id, skill_id)
    return MessageResponse(message="Skill deleted.")


# ── Achievements ──────────────────────────────────────────────────────────────

@router.post(
    "/achievements",
    response_model=AchievementOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add achievement",
)
async def add_achievement(
    body: AchievementIn,
    current_user: CurrentUser,
    db: DbSession,
) -> AchievementOut:
    svc = _svc(db)
    ach = await svc.add_achievement(current_user.id, body)
    return AchievementOut.model_validate(ach)


@router.put(
    "/achievements/{achievement_id}",
    response_model=AchievementOut,
    summary="Update achievement",
)
async def update_achievement(
    achievement_id: uuid.UUID,
    body: AchievementIn,
    current_user: CurrentUser,
    db: DbSession,
) -> AchievementOut:
    svc = _svc(db)
    ach = await svc.update_achievement(current_user.id, achievement_id, body)
    return AchievementOut.model_validate(ach)


@router.delete(
    "/achievements/{achievement_id}",
    response_model=MessageResponse,
    summary="Delete achievement",
)
async def delete_achievement(
    achievement_id: uuid.UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> MessageResponse:
    svc = _svc(db)
    await svc.delete_achievement(current_user.id, achievement_id)
    return MessageResponse(message="Achievement deleted.")
