import hashlib, json, uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.task import Task, Approval, AuditEvent
from app.schemas.tasks import TaskCreate, ApprovalCreate, ApprovalDecision
from app.services.registry import load_registry
from app.services.workflow import marketing_graph
from app.services.audit import record_audit
from app.core.security import Principal, current_principal, require_org_role
router = APIRouter()
WRITER = {"organization_owner", "marketing_manager"}
APPROVER = {"organization_owner", "approver"}
def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
@router.get("/health")
async def health():
    return {"status":"ok","service":"ai-marketing-department"}
@router.get("/agents")
async def agents(_: Principal = Depends(current_principal)):
    return load_registry()
@router.post("/tasks", status_code=201)
async def create_task(body: TaskCreate, principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    require_org_role(body.organization_id, WRITER, principal)
    row = Task(id=str(uuid.uuid4()), organization_id=body.organization_id, brand_id=body.brand_id,
               title=body.title, objective=body.objective, requested_by=principal.subject)
    db.add(row); await db.flush()
    await record_audit(db, actor=principal.subject, organization_id=row.organization_id, event_type="task.created", resource_type="task", resource_id=row.id)
    plan = await marketing_graph.ainvoke({"task":{"objective":row.objective,"title":row.title}})
    row.status = plan.get("status","planned"); row.result = plan.get("plan")
    await db.commit(); await db.refresh(row)
    return serialize_task(row)
@router.get("/tasks")
async def list_tasks(organization_id: str, brand_id: str | None = None, principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    require_org_role(organization_id, {"organization_owner","marketing_manager","approver","analyst"}, principal)
    q = select(Task).where(Task.organization_id == organization_id)
    if brand_id: q = q.where(Task.brand_id == brand_id)
    rows = (await db.execute(q.order_by(Task.created_at.desc()))).scalars().all()
    return [serialize_task(x) for x in rows]
@router.post("/tasks/{task_id}/approvals", status_code=201)
async def create_approval(task_id: str, body: ApprovalCreate, principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    task = await db.get(Task, task_id)
    if not task: raise HTTPException(404,"Task not found")
    require_org_role(task.organization_id, WRITER, principal)
    now = datetime.now(timezone.utc)
    row = Approval(id=str(uuid.uuid4()), task_id=task_id, organization_id=task.organization_id, action_type=body.action_type,
        payload=body.payload, payload_hash=canonical_hash(body.payload), payload_version=1, requested_by=principal.subject,
        expires_at=now + timedelta(minutes=body.expires_in_minutes))
    db.add(row)
    await record_audit(db, actor=principal.subject, organization_id=task.organization_id, event_type="approval.requested", resource_type="approval", resource_id=row.id, metadata={"action_type":row.action_type,"payload_hash":row.payload_hash})
    await db.commit(); await db.refresh(row)
    return serialize_approval(row)
@router.get("/approvals")
async def list_approvals(organization_id: str, status: str = "pending", principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    require_org_role(organization_id, {"organization_owner","marketing_manager","approver"}, principal)
    rows = (await db.execute(select(Approval).where(Approval.organization_id==organization_id, Approval.status==status).order_by(Approval.created_at.desc()))).scalars().all()
    return [serialize_approval(x) for x in rows]
@router.post("/approvals/{approval_id}/decision")
async def decide_approval(approval_id: str, body: ApprovalDecision, principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    row = await db.get(Approval, approval_id)
    if not row: raise HTTPException(404,"Approval not found")
    require_org_role(row.organization_id, APPROVER, principal)
    if row.status != "pending": raise HTTPException(409,"Approval is already decided")
    if row.expires_at and row.expires_at <= datetime.now(timezone.utc): raise HTTPException(409,"Approval has expired")
    if canonical_hash(row.payload) != row.payload_hash: raise HTTPException(409,"Approval payload changed; request a new approval")
    row.status=body.decision; row.decided_by=principal.subject; row.decision_note=body.note; row.decided_at=datetime.now(timezone.utc)
    await record_audit(db, actor=principal.subject, organization_id=row.organization_id, event_type="approval.decided", resource_type="approval", resource_id=row.id, metadata={"decision":body.decision,"payload_hash":row.payload_hash})
    await db.commit(); await db.refresh(row)
    return serialize_approval(row)
@router.get("/audit")
async def list_audit(organization_id: str, principal: Principal = Depends(current_principal), db: AsyncSession = Depends(get_db)):
    require_org_role(organization_id, {"organization_owner","platform_admin"}, principal)
    rows=(await db.execute(select(AuditEvent).where(AuditEvent.organization_id==organization_id).order_by(AuditEvent.created_at.desc()).limit(500))).scalars().all()
    return [{"id":x.id,"actor":x.actor,"event_type":x.event_type,"resource_type":x.resource_type,"resource_id":x.resource_id,"outcome":x.outcome,"metadata":x.metadata_json,"created_at":x.created_at} for x in rows]
def serialize_task(x):
    return {"id":x.id,"organization_id":x.organization_id,"brand_id":x.brand_id,"title":x.title,"objective":x.objective,"status":x.status,"assigned_agents":x.assigned_agents,"result":x.result,"created_at":x.created_at}
def serialize_approval(x):
    return {"id":x.id,"task_id":x.task_id,"organization_id":x.organization_id,"action_type":x.action_type,"payload":x.payload,"payload_hash":x.payload_hash,"payload_version":x.payload_version,"status":x.status,"requested_by":x.requested_by,"decided_by":x.decided_by,"decision_note":x.decision_note,"created_at":x.created_at,"decided_at":x.decided_at,"expires_at":x.expires_at}
