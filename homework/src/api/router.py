from fastapi import APIRouter

from .conferences.router import router as _api_conferences_router

router = APIRouter()

router.include_router(_api_conferences_router, prefix='', tags=["applications"])
