from fastapi import APIRouter

from app.api.endpoints import frameworks, categories, controls

api_router = APIRouter()

api_router.include_router(
    frameworks.router, prefix="/frameworks", tags=["frameworks"]
)
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)
api_router.include_router(
    controls.router, prefix="/controls", tags=["controls"]
)
