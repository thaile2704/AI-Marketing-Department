from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
class MarketingTaskState(TypedDict, total=False):
    task: dict
    plan: dict
    status: str
    error: str
async def classify_task(state: MarketingTaskState):
    task = state["task"]
    # Safe first milestone: create a deterministic plan; model-backed planning is a later backlog item.
    return {"plan": {"objective": task["objective"], "phases": ["research", "strategy", "department_execution", "quality_review", "human_approval"], "requires_human_approval": True}, "status": "planned"}
def build_graph():
    graph = StateGraph(MarketingTaskState)
    graph.add_node("classify_and_plan", classify_task)
    graph.set_entry_point("classify_and_plan")
    graph.add_edge("classify_and_plan", END)
    return graph.compile()
marketing_graph = build_graph()
