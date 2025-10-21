from fastapi import APIRouter
router = APIRouter(prefix="/v1")

from . auth import router as auth_router
from . users import router as users_router

router.include_router(auth_router)
router.include_router(users_router)