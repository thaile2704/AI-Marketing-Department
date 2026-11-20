from pydantic import BaseModel, Field
class TaskCreate(BaseModel):
    organization_id: str = Field(min_length=1, max_length=100)
    brand_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=3, max_length=300)
    objective: str = Field(min_length=5)
class ApprovalCreate(BaseModel):
    action_type: str = Field(min_length=2, max_length=100)
    payload: dict
    expires_in_minutes: int = Field(default=1440, ge=1, le=10080)
class ApprovalDecision(BaseModel):
    decision: str = Field(pattern="^(approved|rejected|revision_requested)$")
    note: str | None = Field(default=None, max_length=2000)
