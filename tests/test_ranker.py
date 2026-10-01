from uncloak.models import Capture, Candidate
from uncloak.ranker import group_by_endpoint, rank_candidates
from uncloak.scoring import score_candidate

def test_group_by_endpoint():
    captures = [
        Capture(id="1", method="GET", url="https://api.com/v1/users?page=1", status=200, request_headers={}, response_headers={}, response_body="", resource_type="fetch"),
        Capture(id="2", method="GET", url="https://api.com/v1/users?page=2", status=200, request_headers={}, response_headers={}, response_body="", resource_type="fetch"),
        Capture(id="3", method="POST", url="https://api.com/v1/users", status=200, request_headers={}, response_headers={}, response_body="", resource_type="fetch"),
    ]
    
    candidates = group_by_endpoint(captures)
    assert len(candidates) == 2
    
    get_cand = next(c for c in candidates if c.captures[0].method == "GET")
    assert len(get_cand.captures) == 2

def test_score_candidate():
    cap = Capture(
        id="1", method="GET", url="https://api.com/v1/items", status=200,
        request_headers={}, response_headers={"content-type": "application/json"},
        response_body='{"data": [{"id": 1}, {"id": 2}]}', resource_type="fetch"
    )
    cand = Candidate(score=0.0, breakdown={}, captures=[cap])
    
    scored = score_candidate(cand)
    assert scored.score > 0
    assert scored.breakdown.has_data_array > 0
    assert scored.breakdown.is_json > 0

def test_rank_candidates():
    # High score
    c1 = Capture(id="1", method="GET", url="https://api.com/v1/items", status=200, request_headers={}, response_headers={"content-type": "application/json"}, response_body='[{"a":1}]', resource_type="fetch")
    # Low score
    c2 = Capture(id="2", method="GET", url="https://api.com/v1/config", status=200, request_headers={}, response_headers={"content-type": "application/json"}, response_body='{"version": "1.0"}', resource_type="fetch")
    
    candidates = group_by_endpoint([c1, c2])
    ranked = rank_candidates(candidates)
    
    assert len(ranked) == 2
    assert ranked[0].captures[0].url.endswith("/items")
