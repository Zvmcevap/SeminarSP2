from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from jose import jwt

from app.models.models import User
from app.core.config import settings
from app.core.security import check_password
from app.crud.crud_user import crud_user

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]


def authenticate(*, username: str, plain_password: str, db: Session) -> Optional[User]:
    user = crud_user.get_by_username(db=db, username=username)
    if not user:
        return None
    if not check_password(plain_password=plain_password, hashed_password=user.hashed_password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )


def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str
) -> str:
    payload = {}
    expire = datetime.now() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.now()
    payload["sub"] = sub
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
