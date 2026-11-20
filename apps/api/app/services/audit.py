import json
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import AuditEvent

async def record_audit(db: AsyncSession, *, actor: str, organization_id: str, event_type: str,
                       resource_type: str, resource_id: str, outcome: str = "success",
                       metadata: dict | None = None) -> None:
    db.add(AuditEvent(actor=actor, organization_id=organization_id, event_type=event_type,
                      resource_type=resource_type, resource_id=resource_id, outcome=outcome,
                      metadata_json=metadata or {}, created_at=datetime.now(timezone.utc)))
