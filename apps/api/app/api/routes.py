from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.task import Task, Approval
from app.schemas.tasks import TaskCreate, ApprovalCreate, ApprovalDecision
from app.services.registry import load_registry
from app.services.workflow import marketing_graph
router = APIRouter()
@router.get("/health")
async def health(): return {"status":"ok","service":"ai-marketing-department"}
@router.get("/agents")
async def agents(): return load_registry()
@router.post("/tasks", status_code=201)
async def create_task(body: TaskCreate, db: AsyncSession = Depends(get_db)):
    row=Task(**body.model_dump())
    db.add(row); await db.commit(); await db.refresh(row)
    plan=await marketing_graph.ainvoke({"task":{"objective":row.objective,"title":row.title}})
    row.status=plan.get("status","planned"); row.result=plan.get("plan")
    await db.commit(); await db.refresh(row)
    return serialize_task(row)
@router.get("/tasks")
async def list_tasks(organization_id: str, brand_id: str | None = None, db: AsyncSession = Depends(get_db)):
    q=select(Task).where(Task.organization_id==organization_id)
    if brand_id: q=q.where(Task.brand_id==brand_id)
    rows=(await db.execute(q.order_by(Task.created_at.desc()))).scalars().all()
    return [serialize_task(x) for x in rows]
@router.post("/tasks/{task_id}/approvals", status_code=201)
async def create_approval(task_id: str, body: ApprovalCreate, db: AsyncSession=Depends(get_db)):
    task=await db.get(Task,task_id)
    if not task: raise HTTPException(404,"Task not found")
    row=Approval(task_id=task_id,**body.model_dump()); db.add(row); await db.commit(); await db.refresh(row)
    return serialize_approval(row)
@router.get("/approvals")
async def list_approvals(status: str="pending", db: AsyncSession=Depends(get_db)):
    rows=(await db.execute(select(Approval).where(Approval.status==status).order_by(Approval.created_at.desc()))).scalars().all()
    return [serialize_approval(x) for x in rows]
@router.post("/approvals/{approval_id}/decision")
async def decide_approval(approval_id: str, body: ApprovalDecision, db: AsyncSession=Depends(get_db)):
    row=await db.get(Approval,approval_id)
    if not row: raise HTTPException(404,"Approval not found")
    if row.status!="pending": raise HTTPException(409,"Approval is already decided")
    row.status=body.decision; row.decided_by=body.decided_by; row.decision_note=body.note; row.decided_at=datetime.now(timezone.utc)
    await db.commit(); await db.refresh(row)
    # Decision is recorded only. No external action is executed by this scaffold.
    return serialize_approval(row)
def serialize_task(x):
    return {"id":x.id,"organization_id":x.organization_id,"brand_id":x.brand_id,"title":x.title,"objective":x.objective,"status":x.status,"assigned_agents":x.assigned_agents,"result":x.result,"created_at":x.created_at}
def serialize_approval(x):
    return {"id":x.id,"task_id":x.task_id,"action_type":x.action_type,"payload":x.payload,"status":x.status,"requested_by":x.requested_by,"decided_by":x.decided_by,"decision_note":x.decision_note,"created_at":x.created_at,"decided_at":x.decided_at}
