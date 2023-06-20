from fastapi import APIRouter

from app.api.v1.endpoints import monitor

api_router = APIRouter()
api_router.include_router(monitor.router, prefix="/monitor", tags=["monitor"])
