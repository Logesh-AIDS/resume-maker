import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.base import TimestampMixin, new_uuid


class ResumeSession(Base, TimestampMixin):
    """
    A single job application context.
    Ties together: profile + JD + template + all generated versions.
    """
    __tablename__ = "resume_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    jd_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("templates.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(400), nullable=False)
    # status: draft | questioning | optimizing | ready | exported
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resume_sessions")  # type: ignore[name-defined]  # noqa: F821
    job_description: Mapped["JobDescription"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "JobDescription", back_populates="resume_sessions"
    )
    template: Mapped["Template"] = relationship("Template", back_populates="resume_sessions")  # type: ignore[name-defined]  # noqa: F821
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="session", cascade="all, delete-orphan",
        order_by="Question.display_order"
    )
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="session", cascade="all, delete-orphan"
    )
    versions: Mapped[list["ResumeVersion"]] = relationship(
        "ResumeVersion", back_populates="session", cascade="all, delete-orphan",
        order_by="ResumeVersion.version_number"
    )

    def __repr__(self) -> str:
        return f"<ResumeSession id={self.id} name={self.name} status={self.status}>"


class Question(Base, TimestampMixin):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    # question_type: yes_no | mcq | short_answer | detailed | numeric | tech_confirm | depth
    question_type: Mapped[str] = mapped_column(String(30), nullable=False)
    options: Mapped[list[str] | None] = mapped_column(JSONB)  # for MCQ
    context: Mapped[str] = mapped_column(Text, nullable=False, default="")
    jd_requirement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jd_requirements.id", ondelete="SET NULL"), nullable=True
    )
    display_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    session: Mapped["ResumeSession"] = relationship("ResumeSession", back_populates="questions")
    answer: Mapped["Answer | None"] = relationship(
        "Answer", back_populates="question", uselist=False
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_answer: Mapped[str] = mapped_column(Text, nullable=False)
    interpreted_value: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    confirmed_facts: Mapped[list[dict]] = mapped_column(JSONB, default=list, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    question: Mapped["Question"] = relationship("Question", back_populates="answer")
    session: Mapped["ResumeSession"] = relationship("ResumeSession", back_populates="answers")


class ResumeVersion(Base, TimestampMixin):
    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    profile_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    jd_snapshot: Mapped[str] = mapped_column(Text, nullable=False, default="")
    answers_snapshot: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    generated_content: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    provenance_map: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    ats_score: Mapped[dict | None] = mapped_column(JSONB)
    # status: generating | ready | failed
    status: Mapped[str] = mapped_column(String(20), default="generating", nullable=False)

    session: Mapped["ResumeSession"] = relationship("ResumeSession", back_populates="versions")
    section_contents: Mapped[list["ResumeSectionContent"]] = relationship(
        "ResumeSectionContent", back_populates="version", cascade="all, delete-orphan",
        order_by="ResumeSectionContent.display_order"
    )
    generated_documents: Mapped[list["GeneratedDocument"]] = relationship(
        "GeneratedDocument", back_populates="version", cascade="all, delete-orphan"
    )
    ats_analyses: Mapped[list["ATSAnalysis"]] = relationship(
        "ATSAnalysis", back_populates="version", cascade="all, delete-orphan"
    )


class ResumeSectionContent(Base):
    __tablename__ = "resume_section_contents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    section_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    display_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_edited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="section_contents")


class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    format: Mapped[str] = mapped_column(String(10), nullable=False)  # "pdf" | "docx"
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column()
    is_valid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validation_report: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="generated_documents")


class ATSAnalysis(Base):
    __tablename__ = "ats_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scores: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    overall_score: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    issues: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="ats_analyses")
