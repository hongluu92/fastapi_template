from fastapi import APIRouter

from .endpoint.users.user_api import router as user_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(user_router, prefix="/users", tags=["users"])


