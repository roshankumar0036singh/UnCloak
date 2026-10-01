from uncloak.models import Capture
from uncloak.schema import infer_schema, infer_array_path

def test_infer_schema_basic():
    c1 = Capture(
        id="1", method="GET", url="https://api.com", status=200, 
        request_headers={}, response_headers={}, 
        response_body='{"name": "Alice"}', resource_type="fetch"
    )
    c2 = Capture(
        id="2", method="GET", url="https://api.com", status=200, 
        request_headers={}, response_headers={}, 
        response_body='{"name": "Bob", "age": 30}', resource_type="fetch"
    )
    
    schema = infer_schema([c1, c2])
    assert schema["type"] == "object"
    assert "name" in schema["properties"]
    assert "age" in schema["properties"]
    # Check that it doesn't include the $schema draft URI by default, or we can just ignore it

def test_infer_array_path():
    schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": {"type": "object"}
            },
            "meta": {"type": "object"}
        }
    }
    assert infer_array_path(schema) == "data"
    
    schema_direct = {"type": "array", "items": {"type": "object"}}
    assert infer_array_path(schema_direct) is None
