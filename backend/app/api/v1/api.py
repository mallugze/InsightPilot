from fastapi import APIRouter
from app.api.v1.endpoints import workspaces, upload, analysis, ai

api_router = APIRouter()
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(upload.router, prefix="", tags=["datasets"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
