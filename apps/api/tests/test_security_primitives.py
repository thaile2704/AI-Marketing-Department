import hashlib
import json
import pytest
from app.api.routes import canonical_hash
from app.core.security import Principal, require_org_role

def test_canonical_hash_is_key_order_independent():
    assert canonical_hash({"a": 1, "b": 2}) == canonical_hash({"b": 2, "a": 1})

def test_canonical_hash_changes_when_payload_changes():
    assert canonical_hash({"budget": 100}) != canonical_hash({"budget": 101})

def test_org_role_is_scoped_to_requested_organization():
    principal = Principal("user-1", {"org-a": ["approver"]})
    require_org_role("org-a", {"approver"}, principal)
    with pytest.raises(Exception):
        require_org_role("org-b", {"approver"}, principal)
