"""
Import all models here so Alembic autogenerate can discover them.
"""
from src.models.user import User
from src.models.profile import Profile, Education, Experience, Project, Skill, Achievement
from src.models.template import Template
from src.models.job_description import JobDescription, JDRequirement
from src.models.resume import (
    ResumeSession,
    Question,
    Answer,
    ResumeVersion,
    ResumeSectionContent,
    GeneratedDocument,
    ATSAnalysis,
)

__all__ = [
    "User",
    "Profile",
    "Education",
    "Experience",
    "Project",
    "Skill",
    "Achievement",
    "Template",
    "JobDescription",
    "JDRequirement",
    "ResumeSession",
    "Question",
    "Answer",
    "ResumeVersion",
    "ResumeSectionContent",
    "GeneratedDocument",
    "ATSAnalysis",
]
