import re
import urllib.parse
from typing import Literal

from uncloak.models import Candidate, Endpoint, ParamSpec

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)
NUM_RE = re.compile(r"^\d+$")


def detect_path_template(path: str) -> str:
    parts = path.split("/")
    new_parts = []
    for part in parts:
        if UUID_RE.match(part) or NUM_RE.match(part):
            new_parts.append("{id}")
        else:
            new_parts.append(part)
    return "/".join(new_parts)


def extract_params(candidate: Candidate) -> Endpoint:
    if not candidate.captures:
        return Endpoint(host="", method="", path_template="", params=[])

    cap = candidate.captures[0]
    parsed = urllib.parse.urlparse(cap.url)

    path_template = detect_path_template(parsed.path)

    params = []

    if "{id}" in path_template:
        params.append(
            ParamSpec(name="id", in_="path", type="string", required=True)  # type: ignore[call-arg]
        )

    query = urllib.parse.parse_qs(parsed.query)
    for k, _ in query.items():
        k_lower = k.lower()
        classification: Literal[
            "constant", "filter", "pagination", "auth", "volatile", "unknown"
        ] = "unknown"
        if k_lower in ("page", "limit", "offset", "cursor", "size"):
            classification = "pagination"
        elif k_lower in ("_", "t", "timestamp", "nonce", "_t"):
            classification = "volatile"
        elif k_lower in ("q", "query", "search", "filter", "sort", "order"):
            classification = "filter"

        params.append(
            ParamSpec(name=k, in_="query", classification=classification)  # type: ignore[call-arg]
        )

    ignore_headers = {
        "host",
        "connection",
        "accept",
        "user-agent",
        "referer",
        "accept-encoding",
        "accept-language",
        "origin",
        "sec-fetch-dest",
        "sec-fetch-mode",
        "sec-fetch-site",
        "sec-ch-ua",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "content-length",
        "content-type",
    }

    for k in cap.request_headers:
        k_lower = k.lower()
        if k_lower in ignore_headers:
            continue

        classification2: Literal[
            "constant", "filter", "pagination", "auth", "volatile", "unknown"
        ] = "unknown"
        if "auth" in k_lower or "token" in k_lower:
            classification2 = "auth"

        params.append(
            ParamSpec(name=k, in_="header", classification=classification2)  # type: ignore[call-arg]
        )

    return Endpoint(
        host=parsed.netloc,
        method=cap.method,
        path_template=path_template,
        params=params,
        reliable=True,
    )
