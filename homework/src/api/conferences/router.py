from fastapi import APIRouter

from .applications import router as _user_router

VERSION = 'conferences'

router = APIRouter()

router.include_router(_user_router, prefix=f'/{VERSION}', tags=["applications"])
