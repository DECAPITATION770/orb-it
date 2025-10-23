from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone


from models.user import User, RoleEnum

async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    _ = select(User).where(User.email == email)
    res = await db.execute(_)
    return res.scalar()

async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    q = select(User).where(User.id == user_id)
    res = await db.execute(q)
    return res.scalars().first()

async def list_users(db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
    _ = select(User).offset(skip).limit(limit)
    res = await db.execute(_)
    return res.scalars().all()

async def create_user(
        db: AsyncSession,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        role: RoleEnum = RoleEnum.user,
        is_verified: bool = False,
        verification_code: Optional[str] = None,
        verification_expires_at: Optional[datetime] = None
) -> User:
    user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_verified=is_verified,
        verification_code=verification_code,
        verification_expires_at=verification_expires_at
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(
        db: AsyncSession,
        user: User,
        updates: Optional[dict]
) -> User:
    if not updates:
        return 0

    pw = updates.pop('password', None)
    if pw is not None:
        ...

    _ = (
        update(user)
        .values(**updates)
        .execution_options(synchronize_session="fetch")
    )

    res = await db.execute(_)
    await db.commit()
    return res.rowcount or 0

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()


async def delete_unverified_older_than(db: AsyncSession, *, days: int = 2) -> int:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
    q = delete(User).where(User.is_verified == False, User.created_at < cutoff)
    res = await db.execute(q)
    await db.commit()
    try:
        return res.rowcount or 0
    except Exception:
        return 0