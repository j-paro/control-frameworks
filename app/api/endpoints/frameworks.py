from fastapi import APIRouter, HTTPException

from app.schemas.responses import FrameworkResponse
from app.lifespan import data


router = APIRouter()


@router.get("", response_model=list[FrameworkResponse])
async def get_frameworks():
    """
    Get all frameworks
    """
    return [framework for framework in data.frameworks.values()]


@router.get("/id/{framework_id}", response_model=FrameworkResponse)
async def get_framework_by_id(framework_id: str):
    """
    Get a framework by id
    """
    framework = data.frameworks.get(framework_id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return framework


@router.get("/search", response_model=list[FrameworkResponse])
async def search_frameworks(search_string: str):
    """
    Search for frameworks; the "name", "description", and "owner" fields are
    searched.
    """

    results = [
        framework
        for framework in data.frameworks.values()
        if search_string.lower()
        in (framework.name + framework.description + framework.owner).lower()
    ]

    return results
