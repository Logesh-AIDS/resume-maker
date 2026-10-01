"""
Pydantic schemas for the Master Career Profile.
Separate In/Out models to control what fields are user-settable vs read-only.
"""
import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


# ── Shared helpers ────────────────────────────────────────────────────────────

OptStr = str | None
OptInt = int | None

SKILL_CATEGORIES = {
    "programming_languages",
    "frameworks",
    "databases",
    "cloud",
    "devops",
    "ai_ml",
    "tools",
    "other",
}

ACHIEVEMENT_CATEGORIES = {
    "competitive",
    "award",
    "hackathon",
    "certification",
    "publication",
    "leadership",
    "other",
}


def _clean_url(v: OptStr) -> OptStr:
    """Strip whitespace, return None for empty strings."""
    if v is None:
        return None
    v = v.strip()
    return v if v else None


# ── External Links ────────────────────────────────────────────────────────────

class ExternalLinkIn(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=500)


class ExternalLinkOut(ExternalLinkIn):
    pass


# ── Personal Info ─────────────────────────────────────────────────────────────

class PersonalInfoIn(BaseModel):
    full_name: OptStr = Field(None, max_length=200)
    professional_title: OptStr = Field(None, max_length=200)
    email: OptStr = Field(None, max_length=320)
    phone: OptStr = Field(None, max_length=50)
    location: OptStr = Field(None, max_length=200)
    portfolio_url: OptStr = Field(None, max_length=500)
    linkedin_url: OptStr = Field(None, max_length=500)
    github_url: OptStr = Field(None, max_length=500)
    other_links: list[ExternalLinkIn] = Field(default_factory=list, max_length=10)
    summary: OptStr = Field(None, max_length=2000)

    @field_validator("portfolio_url", "linkedin_url", "github_url", mode="before")
    @classmethod
    def clean_url(cls, v: OptStr) -> OptStr:
        return _clean_url(v)


class ProfileOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: OptStr
    professional_title: OptStr
    email: OptStr
    phone: OptStr
    location: OptStr
    portfolio_url: OptStr
    linkedin_url: OptStr
    github_url: OptStr
    other_links: list[ExternalLinkOut]
    summary: OptStr
    completion_pct: int
    education: list["EducationOut"] = []
    experiences: list["ExperienceOut"] = []
    projects: list["ProjectOut"] = []
    skills: list["SkillOut"] = []
    achievements: list["AchievementOut"] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Education ─────────────────────────────────────────────────────────────────

class EducationIn(BaseModel):
    institution: str = Field(min_length=1, max_length=300)
    degree: OptStr = Field(None, max_length=200)
    field: OptStr = Field(None, max_length=200)
    start_date: OptStr = Field(None, max_length=20,
                               description="Format: YYYY-MM or YYYY")
    end_date: OptStr = Field(None, max_length=20)
    is_current: bool = False
    gpa: OptStr = Field(None, max_length=20)
    coursework: list[str] = Field(default_factory=list, max_length=20)
    display_order: int = Field(0, ge=0)

    @model_validator(mode="after")
    def end_date_required_if_not_current(self) -> "EducationIn":
        if not self.is_current and not self.end_date and self.start_date:
            pass  # end_date optional — user may be filling incrementally
        return self


class EducationOut(EducationIn):
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Experience ────────────────────────────────────────────────────────────────

class ExperienceIn(BaseModel):
    company: str = Field(min_length=1, max_length=300)
    position: str = Field(min_length=1, max_length=300)
    location: OptStr = Field(None, max_length=200)
    start_date: OptStr = Field(None, max_length=20)
    end_date: OptStr = Field(None, max_length=20)
    is_current: bool = False
    responsibilities: list[str] = Field(default_factory=list, max_length=20)
    achievements: list[str] = Field(default_factory=list, max_length=20)
    technologies: list[str] = Field(default_factory=list, max_length=50)
    metrics: dict[str, str] = Field(default_factory=dict)
    display_order: int = Field(0, ge=0)


class ExperienceOut(ExperienceIn):
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Project ───────────────────────────────────────────────────────────────────

class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=300)
    description: OptStr = Field(None, max_length=2000)
    technologies: list[str] = Field(default_factory=list, max_length=50)
    responsibilities: list[str] = Field(default_factory=list, max_length=20)
    achievements: list[str] = Field(default_factory=list, max_length=20)
    github_url: OptStr = Field(None, max_length=500)
    demo_url: OptStr = Field(None, max_length=500)
    display_order: int = Field(0, ge=0)

    @field_validator("github_url", "demo_url", mode="before")
    @classmethod
    def clean_url(cls, v: OptStr) -> OptStr:
        return _clean_url(v)


class ProjectOut(ProjectIn):
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Skill ─────────────────────────────────────────────────────────────────────

class SkillIn(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    proficiency_level: OptStr = Field(None, max_length=50)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in SKILL_CATEGORIES:
            raise ValueError(
                f"Invalid skill category '{v}'. "
                f"Must be one of: {', '.join(sorted(SKILL_CATEGORIES))}"
            )
        return v


class SkillOut(SkillIn):
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class SkillBulkIn(BaseModel):
    """Create multiple skills at once (used for import / tag input)."""
    skills: list[SkillIn] = Field(min_length=1, max_length=100)


# ── Achievement ───────────────────────────────────────────────────────────────

class AchievementIn(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    title: str = Field(min_length=1, max_length=400)
    description: OptStr = Field(None, max_length=2000)
    date: OptStr = Field(None, max_length=20)
    url: OptStr = Field(None, max_length=500)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in ACHIEVEMENT_CATEGORIES:
            raise ValueError(
                f"Invalid achievement category '{v}'. "
                f"Must be one of: {', '.join(sorted(ACHIEVEMENT_CATEGORIES))}"
            )
        return v

    @field_validator("url", mode="before")
    @classmethod
    def clean_url(cls, v: OptStr) -> OptStr:
        return _clean_url(v)


class AchievementOut(AchievementIn):
    id: uuid.UUID
    profile_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Completion ────────────────────────────────────────────────────────────────

class CompletionOut(BaseModel):
    overall: int  # 0–100
    sections: dict[str, int]  # section_name → 0 or 100
    missing: list[str]        # sections with no data
