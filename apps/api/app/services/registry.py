import json
from pathlib import Path

HERE = Path(__file__).resolve()
CANDIDATES = [HERE.parents[2] / "departments" / "agent_registry.json", HERE.parents[4] / "departments" / "agent_registry.json"]
REGISTRY_PATH = next((p for p in CANDIDATES if p.exists()), CANDIDATES[0])

def load_registry():
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return json.load(f)
