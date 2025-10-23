from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.user import RoleEnum

class UserEmailRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: str
    first_name: str
    last_name: str
    role: RoleEnum
    is_verified: bool
    verification_expires_at: Optional[datetime]


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    role: RoleEnum
    is_verified: bool
