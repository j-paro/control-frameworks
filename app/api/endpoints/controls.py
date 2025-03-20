from uuid import UUID

from fastapi import APIRouter, HTTPException
from app.schemas.mem_data import Control
from app.schemas.responses import (
    ControlResponse,
    ControlMappingsResponse,
    CategoryWithControlsResponse,
)
from app.lifespan import data


router = APIRouter()


@router.get(
    "/id/{control_id}",
    response_model=ControlResponse,
)
async def get_control_by_id(control_id: UUID):
    """
    Get a control by its ID
    """
    control = data.control_index.get(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control


@router.get(
    "/by_control_string_id/{control_string_id}",
    response_model=list[ControlResponse],
)
async def get_control_by_string_id(control_string_id: str):
    """
    Get a control by its string ID -- this can be a partial string ID
    """
    controls = [
        control
        for control in data.control_index.values()
        if control_string_id.lower() in control.control_string_id.lower()
    ]
    return controls


@router.get(
    "/by_category/{category_id}",
    response_model=CategoryWithControlsResponse,
)
async def get_controls_by_category(category_id: UUID):
    """
    Get all controls for a category
    """
    category = data.category_index.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/by_framework/{framework_id}", response_model=list[ControlResponse])
async def get_controls_by_framework(framework_id: UUID):
    """
    Get all controls for a framework
    """
    framework = data.frameworks.get(framework_id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return framework.controls


# @router.get("/mappings", response_model=ControlMappingsResponse)
# async def get_control_mappings(
#     control_id: int,
#     framework_id: int | None = None,
#     session: AsyncSession = Depends(deps.get_session),
# ):
#     """
#     Get all mappings for a control
#     """
#     result = await session.execute(
#         select(Control)
#         .where(Control.id == control_id)
#         .options(selectinload(Control.control_mappings))
#     )
#     control = result.scalar_one_or_none()
#     if not control:
#         raise HTTPException(status_code=404, detail="Control not found")

#     if framework_id:
#         control.control_mappings = [
#             mapping
#             for mapping in control.control_mappings
#             if mapping.framework_id == framework_id
#         ]
#     return control


@router.get("/search", response_model=list[ControlResponse])
async def search_controls(search_string: str):
    """
    Search for controls; the "control_string_id", "title", and "text" fields
    are searched
    """
    controls = [
        control
        for control in data.control_index.values()
        if search_string.lower()
        in (control.control_string_id + (control.title or "") + control.text).lower()
    ]
    return controls
