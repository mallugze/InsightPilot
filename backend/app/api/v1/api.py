from fastapi import APIRouter
from app.api.v1.endpoints import workspaces, upload, analysis

api_router = APIRouter()
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(upload.router, prefix="", tags=["datasets"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["analysis"])
