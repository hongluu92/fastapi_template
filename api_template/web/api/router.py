from fastapi.routing import APIRouter

from api_template.web.api import docs, monitoring
from api_template.web.api.api_v1 import api

api_router = APIRouter()
api_router.include_router(api.api_router)
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
