from fastapi import APIRouter

from server.api.endpoints import health, sources, verify

api_router = APIRouter()

api_router.include_router(verify.router, tags=["verification"])
api_router.include_router(sources.router, tags=["sources"])
api_router.include_router(health.router, tags=["health"])
