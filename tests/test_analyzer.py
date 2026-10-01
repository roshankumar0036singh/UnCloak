from uncloak.analyzer import extract_params, detect_path_template
from uncloak.models import Capture, Candidate

def test_detect_path_template():
    # Should abstract numeric IDs
    assert detect_path_template("/api/users/123/posts") == "/api/users/{id}/posts"
    # Should abstract UUIDs
    assert detect_path_template("/api/users/123e4567-e89b-12d3-a456-426614174000/posts") == "/api/users/{id}/posts"
    # Unchanged
    assert detect_path_template("/api/users/profile") == "/api/users/profile"

def test_extract_params():
    cap = Capture(
        id="1", method="GET",
        url="https://api.com/users/123?page=2&limit=10&_t=1234567890&q=test",
        status=200, request_headers={"authorization": "Bearer token", "x-custom": "value"},
        response_headers={}, response_body="", resource_type="fetch"
    )
    cand = Candidate(score=0.0, breakdown={}, captures=[cap])
    
    endpoint = extract_params(cand)
    
    # Path template
    assert endpoint.path_template == "/users/{id}"
    
    # Path param
    path_param = next(p for p in endpoint.params if p.in_ == "path")
    assert path_param.name == "id"
    
    # Query params
    query_params = {p.name: p for p in endpoint.params if p.in_ == "query"}
    assert "page" in query_params
    assert query_params["page"].classification == "pagination"
    assert query_params["limit"].classification == "pagination"
    assert "_t" in query_params
    assert query_params["_t"].classification == "volatile"
    assert query_params["q"].classification == "filter"
    
    # Header params
    header_params = {p.name: p for p in endpoint.params if p.in_ == "header"}
    assert "authorization" in header_params
    assert header_params["authorization"].classification == "auth"
    assert header_params["x-custom"].classification == "unknown"
