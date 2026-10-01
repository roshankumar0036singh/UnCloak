import pytest
from uncloak.models import Contract, Tolerances
from uncloak.exceptions import ContractError

def test_contract_version_validation():
    base_data = {
        "uncloak_version": "0.1.0",
        "generated_at": "now",
        "endpoint": {
            "host": "api.com", "method": "GET", "path_template": "/", "params": []
        },
        "response_schema": {},
        "fields": {},
        "array_path": None
    }
    
    with pytest.raises(ContractError, match="upgrade"):
        Contract(version=99, **base_data)
        
    c = Contract(version=1, **base_data)
    
    assert c.tolerances is not None
    assert c.tolerances.null_rate_increase == 0.15
    assert c.tolerances.min_items_ratio == 0.5
    assert c.tolerances.fail_on == "breaking"

@pytest.fixture
def base_contract():
    return Contract(
        uncloak_version="0.1.0",
        generated_at="now",
        endpoint={
            "host": "api.com", "method": "GET", "path_template": "/", "params": []
        },
        response_schema={"type": "object"},
        fields={
            "data.items[].id": {"types": ["number"], "required": True, "null_rate": 0.0},
            "data.items[].desc": {"types": ["string"], "required": False, "null_rate": 0.0}
        },
        array_path="data.items",
        min_items=10
    )

def test_diff_endpoint_gone(base_contract):
    from uncloak.check.diff import compare
    findings = compare(base_contract, 404, None)
    assert len(findings) == 1
    assert findings[0].code == "ENDPOINT_GONE"
    assert findings[0].severity == "breaking"

def test_diff_auth_required(base_contract):
    from uncloak.check.diff import compare
    findings = compare(base_contract, 401, None)
    assert len(findings) == 1
    assert findings[0].code == "AUTH_REQUIRED"
    assert findings[0].severity == "error"

def test_diff_not_json(base_contract):
    from uncloak.check.diff import compare
    findings = compare(base_contract, 200, None)
    assert len(findings) == 1
    assert findings[0].code == "NOT_JSON"
    assert findings[0].severity == "breaking"

def test_diff_array_path_missing(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"other": []}}
    findings = compare(base_contract, 200, res)
    assert any(f.code == "ARRAY_PATH_MISSING" for f in findings)
    
def test_diff_min_items_violated(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"items": [{"id": 1}, {"id": 2}]}}  # length 2, expected min 10 * 0.5 = 5
    findings = compare(base_contract, 200, res)
    assert any(f.code == "MIN_ITEMS_VIOLATED" for f in findings)

def test_diff_field_removed_required(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"items": [{"desc": "foo"}] * 10}}
    findings = compare(base_contract, 200, res)
    req = [f for f in findings if f.code == "FIELD_REMOVED" and f.severity == "breaking"]
    assert len(req) == 1
    assert req[0].path == "data.items[].id"

def test_diff_field_removed_optional(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"items": [{"id": 1}] * 10}}
    findings = compare(base_contract, 200, res)
    opt = [f for f in findings if f.code == "FIELD_REMOVED" and f.severity == "warning"]
    assert len(opt) == 1
    assert opt[0].path == "data.items[].desc"

def test_diff_type_changed(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"items": [{"id": "not_a_number", "desc": "foo"}] * 10}}
    findings = compare(base_contract, 200, res)
    assert any(f.code == "TYPE_CHANGED" and f.path == "data.items[].id" for f in findings)

def test_diff_field_added(base_contract):
    from uncloak.check.diff import compare
    res = {"data": {"items": [{"id": 1, "desc": "foo", "new_field": True}] * 10}}
    findings = compare(base_contract, 200, res)
    added = [f for f in findings if f.code == "FIELD_ADDED"]
    assert len(added) == 1
    assert added[0].severity == "info"

def test_diff_null_rate_up(base_contract):
    from uncloak.check.diff import compare
    # out of 10 items, 5 are null (50% null rate). Original is 0.0, tolerance is +0.15 (so 15% allowed). 50% is too much.
    res = {"data": {"items": [{"id": (1 if i < 5 else None), "desc": "foo"} for i in range(10)]}}
    findings = compare(base_contract, 200, res)
    null_up = [f for f in findings if f.code == "NULL_RATE_UP"]
    assert len(null_up) == 1
    assert null_up[0].severity == "warning"
