from typing import Any
from uncloak.models import Contract, Finding

def _resolve_array(data: Any, array_path: str | None) -> list[Any] | None:
    if not array_path:
        return data if isinstance(data, list) else None
    parts = array_path.split(".")
    curr = data
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return None
    return curr if isinstance(curr, list) else None

def _get_type_name(val: Any) -> str:
    if val is None: return "null"
    if isinstance(val, bool): return "boolean"
    if isinstance(val, int): return "number"
    if isinstance(val, float): return "number"
    if isinstance(val, str): return "string"
    if isinstance(val, list): return "array"
    if isinstance(val, dict): return "object"
    return "unknown"

def compare(contract: Contract, status_code: int, response_json: Any | None = None) -> list[Finding]:
    findings = []
    
    if status_code in (404, 410):
        findings.append(Finding(code="ENDPOINT_GONE", severity="breaking", message=f"Endpoint returned {status_code}"))
        return findings
        
    if status_code in (401, 403):
        findings.append(Finding(code="AUTH_REQUIRED", severity="error", message=f"Endpoint returned {status_code}"))
        return findings
        
    if response_json is None:
        findings.append(Finding(code="NOT_JSON", severity="breaking", message="Response is not JSON"))
        return findings

    arr = _resolve_array(response_json, contract.array_path)
    if arr is None:
        findings.append(Finding(code="ARRAY_PATH_MISSING", severity="breaking", message=f"Array path {contract.array_path} missing"))
        return findings

    min_items_expected = contract.min_items * contract.tolerances.min_items_ratio
    if len(arr) < min_items_expected:
        findings.append(Finding(code="MIN_ITEMS_VIOLATED", severity="breaking", message=f"Expected min items {min_items_expected}, got {len(arr)}"))
        
    base_prefix = contract.array_path + "[]." if contract.array_path else "[]."
    
    observed_fields = {}
    for item in arr:
        if isinstance(item, dict):
            for k, v in item.items():
                path = base_prefix + k
                if path not in observed_fields:
                    observed_fields[path] = {"count": 0, "nulls": 0, "types": set()}
                observed_fields[path]["count"] += 1
                t = _get_type_name(v)
                observed_fields[path]["types"].add(t)
                if v is None:
                    observed_fields[path]["nulls"] += 1

    arr_len = len(arr) if len(arr) > 0 else 1
    
    for path, expected_stats in contract.fields.items():
        if path not in observed_fields:
            if expected_stats.required:
                findings.append(Finding(code="FIELD_REMOVED", severity="breaking", path=path, message="Required field removed"))
            else:
                findings.append(Finding(code="FIELD_REMOVED", severity="warning", path=path, message="Optional field removed"))
            continue
            
        obs = observed_fields[path]
        expected_types = set(expected_stats.types)
        obs_non_null = obs["types"] - {"null"}
        exp_non_null = expected_types - {"null"}
        
        if obs_non_null and not obs_non_null.issubset(exp_non_null):
            findings.append(Finding(code="TYPE_CHANGED", severity="breaking", path=path, message=f"Type changed from {exp_non_null} to {obs_non_null}"))
            
        null_rate = obs["nulls"] / arr_len
        expected_null_rate = expected_stats.null_rate
        if null_rate > expected_null_rate + contract.tolerances.null_rate_increase:
            findings.append(Finding(code="NULL_RATE_UP", severity="warning", path=path, message=f"Null rate {null_rate} exceeded tolerance"))
            
    for path in observed_fields:
        if path not in contract.fields:
            findings.append(Finding(code="FIELD_ADDED", severity="info", path=path, message="New field added"))

    return findings
