from uncloak.redact import redact_capture
from uncloak.models import Capture

def test_redact_sensitive_headers():
    capture = Capture(
        id="1", method="GET", url="https://api.com", status=200,
        request_headers={"authorization": "Bearer secret", "x-api-key": "123", "accept": "application/json"},
        response_headers={"set-cookie": "session=abc", "content-type": "application/json"},
        response_body="{}", resource_type="fetch"
    )
    
    redacted = redact_capture(capture)
    assert redacted.request_headers["authorization"] == "[REDACTED]"
    assert redacted.request_headers["x-api-key"] == "[REDACTED]"
    assert redacted.request_headers["accept"] == "application/json"
    
    assert redacted.response_headers["set-cookie"] == "[REDACTED]"
    assert redacted.response_headers["content-type"] == "application/json"
