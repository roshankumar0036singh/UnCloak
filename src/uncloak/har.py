import base64
import json
import uuid

from uncloak.models import Capture


def load_har(file_path: str) -> list[Capture]:
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("log", {}).get("entries", [])
    captures = []

    for entry in entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})

        req_headers = {h["name"].lower(): h["value"] for h in req.get("headers", [])}
        resp_headers = {h["name"].lower(): h["value"] for h in resp.get("headers", [])}

        content = resp.get("content", {})
        text = content.get("text", "")
        encoding = content.get("encoding", "")

        if encoding == "base64" and text:
            try:
                decoded = base64.b64decode(text)
                text = decoded.decode("utf-8", errors="replace")
            except Exception:
                text = ""

        captures.append(
            Capture(
                id=str(uuid.uuid4()),
                method=req.get("method", ""),
                url=req.get("url", ""),
                status=resp.get("status", 0),
                request_headers=req_headers,
                response_headers=resp_headers,
                response_body=text,
                resource_type=entry.get("_resourceType", "unknown"),
            )
        )

    return captures
