"""Initial task, approval and append-only audit schema."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("organization_id", sa.String(100), nullable=False, index=True),
        sa.Column("brand_id", sa.String(100), nullable=False, index=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("status", sa.String(40), nullable=False, server_default="queued", index=True),
        sa.Column("requested_by", sa.String(200), nullable=False),
        sa.Column("assigned_agents", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("approvals",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id"), nullable=False, index=True),
        sa.Column("organization_id", sa.String(100), nullable=False, index=True),
        sa.Column("action_type", sa.String(100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("payload_hash", sa.String(64), nullable=False),
        sa.Column("payload_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending", index=True),
        sa.Column("requested_by", sa.String(200), nullable=False),
        sa.Column("decided_by", sa.String(200), nullable=True),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_table("audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor", sa.String(200), nullable=False),
        sa.Column("organization_id", sa.String(100), nullable=False, index=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(100), nullable=False),
        sa.Column("outcome", sa.String(40), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))

def downgrade():
    op.drop_table("audit_events")
    op.drop_table("approvals")
    op.drop_table("tasks")
