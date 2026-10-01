from uncloak.blocklist import is_blocked
from uncloak.models import Capture


def filter_captures(captures: list[Capture]) -> list[Capture]:
    filtered = []

    BAD_TYPES = {"image", "font", "stylesheet", "media", "websocket", "script"}

    for c in captures:
        if c.status < 200 or c.status >= 300:
            continue

        if c.resource_type in BAD_TYPES:
            continue

        if is_blocked(c.url):
            continue

        content_type = c.response_headers.get("content-type", "").lower()
        if "application/json" not in content_type and "text/json" not in content_type:
            continue

        filtered.append(c)

    return filtered
