from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.analytics_api import router as analytics_router
from app.api import router
from app.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", description="Explainable RAG-based financial research assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
