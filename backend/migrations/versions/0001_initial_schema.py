"""Create Exam AI relational schema."""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("stored_path", sa.Text(), nullable=False),
        sa.Column("document_type", sa.String(20), nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("total_pages", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("extracted_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "chapters",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("chapter_number", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "questions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id", ondelete="SET NULL")),
        sa.Column("chapter_id", sa.String(36), sa.ForeignKey("chapters.id", ondelete="SET NULL")),
        sa.Column("topic", sa.String(255)),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text()),
        sa.Column("source_type", sa.String(20), nullable=False),
        sa.Column("difficulty", sa.String(20), nullable=False),
        sa.Column("correct_option", sa.String(1), nullable=False),
        sa.Column("options_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "attempts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("exam_id", sa.String(36), nullable=False),
        sa.Column("question_id", sa.String(36), sa.ForeignKey("questions.id"), nullable=False),
        sa.Column("selected_option", sa.String(1)),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("response_time_seconds", sa.Float(), nullable=False, server_default="0"),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("attempts")
    op.drop_table("questions")
    op.drop_table("chapters")
    op.drop_table("documents")
