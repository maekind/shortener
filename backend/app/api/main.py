from fastapi import APIRouter

from app.api.routes import shorten, utils

api_router = APIRouter()
api_router.include_router(shorten.router, tags=["shorten"])
api_router.include_router(utils.router, tags=["utils"])
