from fastapi import APIRouter

from crud import user as crud_user

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"ping": "pong"}

@router.get("/user/{email}")
async def get_user(email: str):
    _ = crud_user.get_by_email(email)
    return {"email": email}