import uuid

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.base import TimestampMixin, new_uuid


class Template(Base, TimestampMixin):
    __tablename__ = "templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_format: Mapped[str] = mapped_column(String(10), nullable=False)     # "docx" | "pdf"
    original_file_path: Mapped[str] = mapped_column(Text, nullable=False)
    schema: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)  # TemplateSchema
    reconstruction_confidence: Mapped[float] = mapped_column(Numeric(4, 2), default=0.0)
    parse_warnings: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="templates")  # type: ignore[name-defined]  # noqa: F821
    resume_sessions: Mapped[list["ResumeSession"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ResumeSession", back_populates="template"
    )

    def __repr__(self) -> str:
        return f"<Template id={self.id} name={self.name} format={self.source_format}>"
