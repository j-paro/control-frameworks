from __future__ import annotations

from pydantic import BaseModel, computed_field


class CustomField(BaseModel):
    name: str
    value: str | bool | None = None


class Framework(BaseModel):
    string_id: str
    name: str
    description: str
    owner: str
    categories: list[Category] = []
    controls: list[Control] = []
    custom_fields: list[CustomField] | None = []

    def __repr__(self):
        return f"Framework(id={self.id}, name={self.name})"


class Category(BaseModel):
    cat_string_id: str
    name: str
    type: str
    description: str | None = None
    framework: Framework
    categories: list[Category] | None = []
    controls: list[Control] = []
    custom_fields: list[CustomField] | None = []

    @computed_field
    @property
    def framework_id(self) -> str:
        return self.framework.string_id

    def __repr__(self):
        return f"Category(id={self.cat_string_id}, name={self.name})"


class Control(BaseModel):
    control_string_id: str
    title: str | None = None
    text: str
    framework: Framework
    category: Category
    custom_fields: list[CustomField] | None = []

    @computed_field
    @property
    def framework_id(self) -> str:
        return self.framework.string_id

    @computed_field
    @property
    def category_id(self) -> str:
        return self.category.cat_string_id

    def __repr__(self):
        return f"Control(id={self.control_string_id}, text={self.text})"
