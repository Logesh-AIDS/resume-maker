"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-09-16
"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── users ─────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("hashed_password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── profiles ──────────────────────────────────────────────────────────
    op.create_table(
        "profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("full_name", sa.String(200)),
        sa.Column("professional_title", sa.String(200)),
        sa.Column("email", sa.String(320)),
        sa.Column("phone", sa.String(50)),
        sa.Column("location", sa.String(200)),
        sa.Column("portfolio_url", sa.Text),
        sa.Column("linkedin_url", sa.Text),
        sa.Column("github_url", sa.Text),
        sa.Column("other_links", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("summary", sa.Text),
        sa.Column("completion_pct", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_profiles_user_id", "profiles", ["user_id"], unique=True)

    # ── education ─────────────────────────────────────────────────────────
    op.create_table(
        "education",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("institution", sa.String(300), nullable=False),
        sa.Column("degree", sa.String(200)),
        sa.Column("field", sa.String(200)),
        sa.Column("start_date", sa.String(20)),
        sa.Column("end_date", sa.String(20)),
        sa.Column("is_current", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("gpa", sa.String(20)),
        sa.Column("coursework", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("display_order", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_education_profile_id", "education", ["profile_id"])

    # ── experiences ───────────────────────────────────────────────────────
    op.create_table(
        "experiences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company", sa.String(300), nullable=False),
        sa.Column("position", sa.String(300), nullable=False),
        sa.Column("location", sa.String(200)),
        sa.Column("start_date", sa.String(20)),
        sa.Column("end_date", sa.String(20)),
        sa.Column("is_current", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("responsibilities", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("achievements", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("technologies", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("metrics", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("display_order", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_experiences_profile_id", "experiences", ["profile_id"])

    # ── projects ──────────────────────────────────────────────────────────
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("technologies", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("responsibilities", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("achievements", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("github_url", sa.Text),
        sa.Column("demo_url", sa.Text),
        sa.Column("display_order", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_projects_profile_id", "projects", ["profile_id"])

    # ── skills ────────────────────────────────────────────────────────────
    op.create_table(
        "skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("proficiency_level", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_skills_profile_id", "skills", ["profile_id"])

    # ── achievements ──────────────────────────────────────────────────────
    op.create_table(
        "achievements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("title", sa.String(400), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("date", sa.String(20)),
        sa.Column("url", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_achievements_profile_id", "achievements", ["profile_id"])

    # ── templates ─────────────────────────────────────────────────────────
    op.create_table(
        "templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("source_format", sa.String(10), nullable=False),
        sa.Column("original_file_path", sa.Text, nullable=False),
        sa.Column("schema", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("reconstruction_confidence", sa.Numeric(4, 2), server_default="0.0"),
        sa.Column("parse_warnings", postgresql.ARRAY(sa.Text), nullable=False, server_default="{}"),
        sa.Column("is_default", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_templates_user_id", "templates", ["user_id"])

    # ── job_descriptions ──────────────────────────────────────────────────
    op.create_table(
        "job_descriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_text", sa.Text, nullable=False),
        sa.Column("company", sa.String(300)),
        sa.Column("role_title", sa.String(300)),
        sa.Column("analyzed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_jd_user_id", "job_descriptions", ["user_id"])

    # ── jd_requirements ───────────────────────────────────────────────────
    op.create_table(
        "jd_requirements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("jd_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("value", sa.Text, nullable=False),
        sa.Column("is_required", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("context", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_jd_requirements_jd_id", "jd_requirements", ["jd_id"])

    # ── resume_sessions ───────────────────────────────────────────────────
    op.create_table(
        "resume_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("jd_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("templates.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(400), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_resume_sessions_user_id", "resume_sessions", ["user_id"])

    # ── questions ─────────────────────────────────────────────────────────
    op.create_table(
        "questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_text", sa.Text, nullable=False),
        sa.Column("question_type", sa.String(30), nullable=False),
        sa.Column("options", postgresql.JSONB),
        sa.Column("context", sa.Text, nullable=False, server_default=""),
        sa.Column("jd_requirement_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("jd_requirements.id", ondelete="SET NULL"), nullable=True),
        sa.Column("display_order", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_questions_session_id", "questions", ["session_id"])

    # ── answers ───────────────────────────────────────────────────────────
    op.create_table(
        "answers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("question_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_answer", sa.Text, nullable=False),
        sa.Column("interpreted_value", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("confirmed_facts", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_answers_session_id", "answers", ["session_id"])
    op.create_unique_constraint("uq_answers_question_id", "answers", ["question_id"])

    # ── resume_versions ───────────────────────────────────────────────────
    op.create_table(
        "resume_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version_number", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("profile_snapshot", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("jd_snapshot", sa.Text, nullable=False, server_default=""),
        sa.Column("answers_snapshot", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("generated_content", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("provenance_map", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("ats_score", postgresql.JSONB),
        sa.Column("status", sa.String(20), nullable=False, server_default="generating"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_resume_versions_session_id", "resume_versions", ["session_id"])

    # ── resume_section_contents ───────────────────────────────────────────
    op.create_table(
        "resume_section_contents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_type", sa.String(50), nullable=False),
        sa.Column("content", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("display_order", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("is_visible", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("last_edited_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_section_contents_version_id", "resume_section_contents", ["version_id"])

    # ── generated_documents ───────────────────────────────────────────────
    op.create_table(
        "generated_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("format", sa.String(10), nullable=False),
        sa.Column("file_path", sa.Text, nullable=False),
        sa.Column("file_size_bytes", sa.Integer),
        sa.Column("is_valid", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("validation_report", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_generated_documents_version_id", "generated_documents", ["version_id"])

    # ── ats_analyses ──────────────────────────────────────────────────────
    op.create_table(
        "ats_analyses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("resume_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scores", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("overall_score", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("issues", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ats_analyses_version_id", "ats_analyses", ["version_id"])


def downgrade() -> None:
    op.drop_table("ats_analyses")
    op.drop_table("generated_documents")
    op.drop_table("resume_section_contents")
    op.drop_table("resume_versions")
    op.drop_table("answers")
    op.drop_table("questions")
    op.drop_table("resume_sessions")
    op.drop_table("jd_requirements")
    op.drop_table("job_descriptions")
    op.drop_table("templates")
    op.drop_table("achievements")
    op.drop_table("skills")
    op.drop_table("projects")
    op.drop_table("experiences")
    op.drop_table("education")
    op.drop_table("profiles")
    op.drop_table("users")
