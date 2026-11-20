"""Protect audit event rows from UPDATE and DELETE."""
from alembic import op

revision = "0002_audit_append_only"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION prevent_audit_event_mutation()
    RETURNS trigger AS $$
    BEGIN
      RAISE EXCEPTION 'audit_events is append-only';
    END;
    $$ LANGUAGE plpgsql;
    """)
    op.execute("""
    CREATE TRIGGER audit_events_no_mutation
    BEFORE UPDATE OR DELETE ON audit_events
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_event_mutation();
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS audit_events_no_mutation ON audit_events")
    op.execute("DROP FUNCTION IF EXISTS prevent_audit_event_mutation()")
