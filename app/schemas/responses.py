from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    # may define additional fields or config shared across responses
    model_config = ConfigDict(
        from_attributes=True,
    )


class CustomFieldResponse(BaseModel):
    name: str
    value: str | bool | None


class FrameworkResponse(BaseResponse):
    id: UUID
    name: str
    description: str | None
    owner: str


class CategoryResponse(BaseResponse):
    id: UUID
    cat_string_id: str
    name: str
    type: str
    description: str | None
    framework_id: UUID | None
    categories: list["CategoryResponse"] | None
    custom_fields: list[CustomFieldResponse] | None


class ControlResponse(BaseResponse):
    id: UUID
    control_string_id: str
    title: str | None
    text: str
    category_id: UUID
    framework_id: UUID
    custom_fields: list[CustomFieldResponse] | None


class CategoryWithControlsResponse(CategoryResponse):
    controls: list[ControlResponse] | None


class ControlMappingsResponse(ControlResponse):
    control_mappings: list[ControlResponse] | None
