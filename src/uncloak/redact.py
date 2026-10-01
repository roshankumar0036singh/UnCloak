from uncloak.models import Capture

SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
}


def redact_capture(capture: Capture) -> Capture:
    redacted = capture.model_copy(deep=True)

    for headers in (redacted.request_headers, redacted.response_headers):
        for k in headers.keys():
            k_lower = k.lower()
            if k_lower in SENSITIVE_HEADERS or k_lower.startswith("x-csrf"):
                headers[k] = "[REDACTED]"

    return redacted
