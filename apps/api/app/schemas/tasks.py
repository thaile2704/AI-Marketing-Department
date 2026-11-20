from pydantic import BaseModel, Field
class TaskCreate(BaseModel):
    organization_id: str = Field(min_length=1, max_length=100)
    brand_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=3, max_length=300)
    objective: str = Field(min_length=5)
    requested_by: str = "ceo"
class ApprovalCreate(BaseModel):
    action_type: str
    payload: dict
    requested_by: str = "marketing_director"
class ApprovalDecision(BaseModel):
    decision: str = Field(pattern="^(approved|rejected|revision_requested)$")
    decided_by: str
    note: str | None = None
