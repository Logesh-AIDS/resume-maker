import uuid

from sqlalchemy import Date, ForeignKey, Integer, SmallInteger, String, Text, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.base import TimestampMixin, new_uuid


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    full_name: Mapped[str | None] = mapped_column(String(200))
    professional_title: Mapped[str | None] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(320))
    phone: Mapped[str | None] = mapped_column(String(50))
    location: Mapped[str | None] = mapped_column(String(200))
    portfolio_url: Mapped[str | None] = mapped_column(Text)
    linkedin_url: Mapped[str | None] = mapped_column(Text)
    github_url: Mapped[str | None] = mapped_column(Text)
    other_links: Mapped[list[dict]] = mapped_column(JSONB, default=list, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    completion_pct: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")  # type: ignore[name-defined]  # noqa: F821
    education: Mapped[list["Education"]] = relationship(
        "Education", back_populates="profile", cascade="all, delete-orphan",
        order_by="Education.display_order"
    )
    experiences: Mapped[list["Experience"]] = relationship(
        "Experience", back_populates="profile", cascade="all, delete-orphan",
        order_by="Experience.display_order"
    )
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="profile", cascade="all, delete-orphan",
        order_by="Project.display_order"
    )
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", back_populates="profile", cascade="all, delete-orphan"
    )
    achievements: Mapped[list["Achievement"]] = relationship(
        "Achievement", back_populates="profile", cascade="all, delete-orphan"
    )


class Education(Base, TimestampMixin):
    __tablename__ = "education"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    institution: Mapped[str] = mapped_column(String(300), nullable=False)
    degree: Mapped[str | None] = mapped_column(String(200))
    field: Mapped[str | None] = mapped_column(String(200))
    start_date: Mapped[str | None] = mapped_column(String(20))   # stored as "YYYY-MM" for flexibility
    end_date: Mapped[str | None] = mapped_column(String(20))
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    gpa: Mapped[str | None] = mapped_column(String(20))
    coursework: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    display_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="education")


class Experience(Base, TimestampMixin):
    __tablename__ = "experiences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company: Mapped[str] = mapped_column(String(300), nullable=False)
    position: Mapped[str] = mapped_column(String(300), nullable=False)
    location: Mapped[str | None] = mapped_column(String(200))
    start_date: Mapped[str | None] = mapped_column(String(20))
    end_date: Mapped[str | None] = mapped_column(String(20))
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    responsibilities: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    achievements: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    technologies: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    display_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="experiences")


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    technologies: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    responsibilities: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    achievements: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    github_url: Mapped[str | None] = mapped_column(Text)
    demo_url: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="projects")


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    proficiency_level: Mapped[str | None] = mapped_column(String(50))

    profile: Mapped["Profile"] = relationship("Profile", back_populates="skills")


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(400), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    date: Mapped[str | None] = mapped_column(String(20))
    url: Mapped[str | None] = mapped_column(Text)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="achievements")
