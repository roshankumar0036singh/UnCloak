import pytest
from pathlib import Path
from uncloak.har import load_har

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_load_har_basic():
    har_path = FIXTURES_DIR / "ecommerce_basic" / "capture.har"
    captures = load_har(str(har_path))
    
    assert len(captures) > 0
    assert len(captures) == 2
    
    c = captures[0]
    assert c.method == "GET"
    assert c.url == "https://api.shop.local/v1/products?page=1"
    assert c.status == 200
    assert c.resource_type == "fetch"
    assert c.response_body.startswith('{"data":')

def test_load_har_assigns_ids():
    har_path = FIXTURES_DIR / "ecommerce_basic" / "capture.har"
    captures = load_har(str(har_path))
    assert captures[0].id != captures[1].id
    assert captures[0].id is not None
