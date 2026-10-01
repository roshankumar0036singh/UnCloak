import json
from typing import Any

from genson import SchemaBuilder  # type: ignore[import-untyped]

from uncloak.models import Capture


def infer_schema(captures: list[Capture]) -> dict[str, Any]:
    builder = SchemaBuilder(schema_uri=None)
    for cap in captures:
        try:
            data = json.loads(cap.response_body)
            builder.add_object(data)
        except Exception:
            pass

    return builder.to_schema()  # type: ignore[no-any-return]


def infer_array_path(schema: dict[str, Any]) -> str | None:
    if schema.get("type") == "array":
        return None

    if schema.get("type") == "object":
        properties = schema.get("properties", {})
        for k, v in properties.items():
            if isinstance(v, dict) and v.get("type") == "array":
                return str(k)

    return None
