from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import uuid
import hashlib

import jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _make_jti() -> str:
    return uuid.uuid4().hex


def create_access_token(subject: str, *, additional_claims: dict | None = None) -> str:
    exp = _now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(subject),
        "exp": int(exp.timestamp()),
        "type": "access",
        "jti": _make_jti(),
        "iss": getattr(settings, "JWT_ISSUER", None),
    }
    if additional_claims:
        payload.update(additional_claims)
    payload = {k: v for k, v in payload.items() if v is not None}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def create_refresh_token(subject: str) -> Tuple[str, datetime, str]:
    exp = _now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = _make_jti()
    payload = {
        "sub": str(subject),
        "exp": int(exp.timestamp()),
        "type": "refresh",
        "jti": jti,
        "iss": getattr(settings, "JWT_ISSUER", None),
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, exp, jti


def decode_token(token: str, *, verify_exp: bool = True) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": verify_exp},
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
