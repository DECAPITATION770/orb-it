from fastapi import APIRouter

from crud import user as crud_user
from core.db import get_db
router = APIRouter()

@router.get("/ping")
async def ping():
    return {"ping": "pong"}

@router.get("/user/{email}")
async def get_user(email: str):
    _ = crud_user.get_by_email(get_db(), email)
    return {"data": email}

@router.get("/users/")
async def get_users(skip: int, limit: int):
    _ = crud_user.list_users(get_db(), skip=skip, limit=limit)
    return {"data": _}