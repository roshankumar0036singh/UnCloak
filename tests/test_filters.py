from pathlib import Path
from uncloak.filters import filter_captures
from uncloak.models import Capture
from uncloak.har import load_har

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_filter_drops_noise():
    har_path = FIXTURES_DIR / "ecommerce_basic" / "capture.har"
    captures = load_har(str(har_path))
    
    assert len(captures) == 2
    
    filtered = filter_captures(captures)
    assert len(filtered) == 1
    assert filtered[0].url == "https://api.shop.local/v1/products?page=1"

def test_filter_criteria():
    captures = [
        # Good JSON endpoint
        Capture(id="1", method="GET", url="https://api.com/data", status=200, request_headers={}, response_headers={"content-type": "application/json"}, response_body="{}", resource_type="fetch"),
        # Bad status
        Capture(id="2", method="GET", url="https://api.com/err", status=500, request_headers={}, response_headers={"content-type": "application/json"}, response_body="{}", resource_type="fetch"),
        # Bad resource type
        Capture(id="3", method="GET", url="https://api.com/img.png", status=200, request_headers={}, response_headers={"content-type": "image/png"}, response_body="", resource_type="image"),
        # Blocked domain
        Capture(id="4", method="GET", url="https://analytics.google.com/test", status=200, request_headers={}, response_headers={"content-type": "application/json"}, response_body="{}", resource_type="fetch"),
        # Non-JSON content type
        Capture(id="5", method="GET", url="https://api.com/text", status=200, request_headers={}, response_headers={"content-type": "text/html"}, response_body="<html></html>", resource_type="document"),
    ]
    
    filtered = filter_captures(captures)
    assert len(filtered) == 1
    assert filtered[0].id == "1"
