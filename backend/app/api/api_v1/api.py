from fastapi import APIRouter

from app.api.api_v1.endpoint import hwmock


api_router = APIRouter()
api_router.include_router(hwmock.router, tags=['hw'], prefix='')