from typing import Generator, Optional

from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqladmin.authentication import AuthenticationBackend

from app.core.config import settings
from app.database.session import SessionLocal
from app.models.models import User
from app.crud.crud_user import crud_user
from app.core.security import OAuth2PasswordBearerWithCookie


# Database dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User dependency
class TokenData(BaseModel):
    username: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/me")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate your credentials!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(username=user_id)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_superuser(current_user: User = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You're no superuser!",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not current_user.is_superuser:
        raise credentials_exception

    return current_user


class AdminAuthenticator(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        return False

    async def logout(self, request: Request) -> bool:
        return True

    async def authenticate(self, request: Request) -> bool:
        db = next(get_db())
        token = await oauth2_scheme.__call__(request=request)
        user = await get_current_user(db=db, token=token)
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="You might be a user, but you are no *super*!")
        return user.is_superuser


admin_authenticator = AdminAuthenticator(secret_key=settings.SECRET_KEY)
