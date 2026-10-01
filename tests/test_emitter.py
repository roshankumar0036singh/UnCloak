from uncloak.emitter import emit_client
from uncloak.models import Contract, Endpoint, ParamSpec

def test_emit_client():
    contract = Contract(
        version=1, 
        uncloak_version="0.1.0", 
        generated_at="now",
        endpoint=Endpoint(
            host="api.com", method="GET", path_template="/users/{id}",
            params=[ParamSpec(**{"name": "id", "in": "path", "type": "string", "required": True})]  # type: ignore[call-arg]
        ),
        response_schema={"type": "object", "properties": {"name": {"type": "string"}}},
        fields={}, 
        array_path=None
    )
    
    code = emit_client(contract, "MyClient")
    assert "class MyClient:" in code
    assert "def request(" in code
    assert "name: str" in code
