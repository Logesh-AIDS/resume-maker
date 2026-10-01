import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.base import TimestampMixin, new_uuid


class JobDescription(Base, TimestampMixin):
    __tablename__ = "job_descriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str | None] = mapped_column(String(300))
    role_title: Mapped[str | None] = mapped_column(String(300))
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="job_descriptions")  # type: ignore[name-defined]  # noqa: F821
    requirements: Mapped[list["JDRequirement"]] = relationship(
        "JDRequirement", back_populates="job_description", cascade="all, delete-orphan"
    )
    resume_sessions: Mapped[list["ResumeSession"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ResumeSession", back_populates="job_description"
    )

    def __repr__(self) -> str:
        return f"<JobDescription id={self.id} role={self.role_title}>"


class JDRequirement(Base, TimestampMixin):
    __tablename__ = "jd_requirements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    jd_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    # categories: required_skill, preferred_skill, language, framework, database,
    #             cloud, devops, ai_ml, responsibility, qualification, education,
    #             domain, terminology, action_verb
    value: Mapped[str] = mapped_column(Text, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    context: Mapped[str | None] = mapped_column(Text)  # surrounding sentence from JD

    job_description: Mapped["JobDescription"] = relationship("JobDescription", back_populates="requirements")
