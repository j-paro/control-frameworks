from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.responses import CategoryResponse
from app.schemas.mem_data import Category
from app.lifespan import data


router = APIRouter()


@router.get("/by_framework/{framework_id}", response_model=list[CategoryResponse])
async def get_categories_by_framework(framework_id: UUID):
    """
    Get all categories for a framework
    """
    framework = data.frameworks.get(framework_id)
    if framework is None:
        raise HTTPException(status_code=404, detail="Framework not found")

    return framework.categories


@router.get("/id/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID):
    """
    Get a category
    """
    category = data.category_index.get(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/search", response_model=list[CategoryResponse])
async def search_categories(search_string: str):
    """
    Search for categories; the "name", "cat_string_id", "description", and
    "type" fields are searched.
    """
    categories = [
        category
        for category in data.category_index.values()
        if search_string.lower()
        in (
            category.name
            + category.cat_string_id
            + (category.description or "")
            + category.type
        ).lower()
    ]
    return categories
