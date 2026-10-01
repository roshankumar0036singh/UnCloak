import pytest
from pydantic import ValidationError
from uncloak.models import (
    Capture,
    ScoreBreakdown,
    Candidate,
    ParamSpec,
    Endpoint,
    FieldStats,
    PaginationSpec,
    Tolerances,
    Contract,
    Finding,
)

def test_capture_model():
    capture = Capture(
        id="req_1",
        method="GET",
        url="https://api.example.com/data",
        status=200,
        request_headers={"Authorization": "Bearer token"},
        response_headers={"Content-Type": "application/json"},
        response_body='{"ok": true}',
        resource_type="xhr",
    )
    assert capture.method == "GET"
    # Round-trip test
    dumped = capture.model_dump_json()
    loaded = Capture.model_validate_json(dumped)
    assert loaded.id == capture.id

def test_tolerances_defaults():
    t = Tolerances()
    assert t.null_rate_increase == 0.15
    assert t.min_items_ratio == 0.5
    assert t.fail_on == "breaking"

def test_contract_roundtrip():
    contract = Contract(
        version=1,
        uncloak_version="0.1.0",
        generated_at="2026-10-01T12:00:00Z",
        endpoint=Endpoint(
            host="api.example.com",
            method="GET",
            path_template="/v1/items",
            params=[]
        ),
        response_schema={"type": "object"},
        fields={},
        array_path="data",
        min_items=5,
        pagination=PaginationSpec(type="page", param="p"),
        tolerances=Tolerances()
    )
    
    dumped = contract.model_dump_json()
    loaded = Contract.model_validate_json(dumped)
    assert loaded.version == 1
    assert loaded.endpoint.host == "api.example.com"

def test_invalid_data_rejected():
    with pytest.raises(ValidationError):
        Capture(id="123")  # missing required fields
