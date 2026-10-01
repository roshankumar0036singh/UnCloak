import os

from jinja2 import Environment, FileSystemLoader

from uncloak.models import Contract


def _json_type_to_python(schema_type: str) -> str:
    mapping = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "list",
        "object": "dict",
    }
    return mapping.get(schema_type, "Any")


def emit_client(contract: Contract, client_name: str = "ApiClient") -> str:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("client.py.jinja")

    properties = {}
    schema = contract.response_schema
    if schema.get("type") == "object":
        for k, v in schema.get("properties", {}).items():
            if isinstance(v, dict):
                properties[k] = {
                    "type_str": _json_type_to_python(v.get("type", "string"))
                }
            else:
                properties[k] = {"type_str": "Any"}

    path_params = [p for p in contract.endpoint.params if p.in_ == "path"]

    return template.render(
        contract=contract,
        client_name=client_name,
        properties=properties,
        path_params=path_params,
    )
