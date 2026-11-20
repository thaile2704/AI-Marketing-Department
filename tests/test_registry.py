import json
from pathlib import Path
def test_registry_has_expected_logical_roles():
    p=Path(__file__).parents[1]/"departments"/"agent_registry.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    assert data["count"] == 56
    assert len(data["agents"]) == 56
    assert len(data["departments"]) == 10
    assert sum(len(x["specialists"]) for x in data["departments"].values()) == 45
