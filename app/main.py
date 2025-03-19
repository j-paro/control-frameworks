"""Main FastAPI app instance declaration."""

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.api import api_router
from app.core import config
from app.lifespan import lifespan


app = FastAPI(
    title="Control Frameworks API",
    version="1.0.0",
    description="An API for cybersecurity control frameworks",
    openapi_url="/openapi.json",
    docs_url="/",
    lifespan=lifespan,
)
app.include_router(api_router)

# Guards against HTTP Host Header attacks
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=config.settings.ALLOWED_HOSTS
)
