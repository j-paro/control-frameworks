from __future__ import annotations
from uuid import uuid4, UUID

from pydantic import BaseModel, computed_field, Field


class CustomField(BaseModel):
    name: str
    value: str | bool | None = None


class Framework(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    owner: str
    categories: list[Category] = []
    controls: list[Control] = []
    custom_fields: list[CustomField] | None = []

    def __repr__(self):
        return f"Framework(id={self.id}, name={self.name})"

    def get_category_id_list(self) -> list[UUID]:
        def get_category_ids(category: Category):
            category_ids = [category.id]
            for child in category.categories:
                category_ids.extend(get_category_ids(child))
            return category_ids

        category_ids = []
        for category in self.categories:
            category_ids.extend(get_category_ids(category))

        return category_ids

    def get_control_id_list(self) -> list[UUID]:
        control_ids = []
        for category in self.categories:
            control_ids.extend(category.get_control_id_list())

        return control_ids


class Category(BaseModel):
    id: UUID = Field(default_factory=uuid4)
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
    def framework_id(self) -> UUID:
        return self.framework.id

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"

    def get_control_id_list(self) -> list[UUID]:
        control_ids = []
        for control in self.controls:
            control_ids.append(control.id)

        for category in self.categories:
            control_ids.extend(category.get_control_id_list)

        return control_ids


class Control(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    control_string_id: str
    title: str | None = None
    text: str
    framework: Framework
    category: Category
    custom_fields: list[CustomField] | None = []

    @computed_field
    @property
    def framework_id(self) -> UUID:
        return self.framework.id

    @computed_field
    @property
    def category_id(self) -> UUID:
        return self.category.id

    def __repr__(self):
        return f"Control(id={self.id}, text={self.text})"
