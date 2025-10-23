from fastapi import APIRouter, Depends
from starlette.requests import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user as crud_user
from schemas import user as user_schema
from core.db import get_db
router = APIRouter()

# @router.post("/create_user")
# @router.post("/verify_code")


@router.get("/user/{email}", response_model=user_schema.UserEmailRead)
async def get_user(email: str, db: AsyncSession = Depends(get_db)):
    _ = await crud_user.get_by_email(db, email)
    return {"data": _}

@router.patch("/user/{id}", response_model=user_schema.UserEmailRead)
async def update_user(user_id: int, updates: user_schema.UpdateUser, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _ = await crud_user.update_user(db, user, updates.model_dump())
    return {"data": _}


@router.get("/users/")
async def get_users(skip: int, limit: int):
    _ = crud_user.list_users(get_db(), skip=skip, limit=limit)
    return {"data": _}