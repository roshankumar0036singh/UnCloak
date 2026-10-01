from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Capture(BaseModel):
    id: str
    method: str
    url: str
    status: int
    request_headers: dict[str, str]
    response_headers: dict[str, str]
    response_body: str
    resource_type: str


class ScoreBreakdown(BaseModel):
    is_json: float = 0.0
    has_data_array: float = 0.0
    values_in_page_text: float = 0.0
    response_size: float = 0.0
    url_path_hints: float = 0.0
    pagination_repeat: float = 0.0
    is_analytics: float = 0.0
    is_tiny_or_config: float = 0.0
    is_related_reco: float = 0.0
    total: float = 0.0


class Candidate(BaseModel):
    score: float
    breakdown: ScoreBreakdown
    captures: list[Capture]


class ParamSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    in_: Literal["query", "header", "path", "cookie"] = Field(alias="in")
    type: str = "string"
    required: bool = False
    classification: Literal[
        "constant", "filter", "pagination", "auth", "volatile", "unknown"
    ] = "unknown"
    default_value: str | None = None


class Endpoint(BaseModel):
    host: str
    method: str
    path_template: str
    params: list[ParamSpec]
    reliable: bool = True


class FieldStats(BaseModel):
    types: list[str]
    required: bool
    null_rate: float


class PaginationSpec(BaseModel):
    type: Literal["page", "offset", "cursor"]
    param: str


class Tolerances(BaseModel):
    null_rate_increase_threshold: float = 0.1
    allow_optional_field_removal: bool = True


class Contract(BaseModel):
    version: int = 1
    uncloak_version: str
    generated_at: str
    endpoint: Endpoint
    response_schema: dict[str, Any]
    fields: dict[str, FieldStats]
    array_path: str | None
    min_items: int = 0
    pagination: PaginationSpec | None = None
    tolerances: Tolerances = Field(default_factory=Tolerances)


class Finding(BaseModel):
    code: str
    severity: Literal["breaking", "error", "warning", "info"]
    message: str
