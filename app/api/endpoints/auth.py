from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import crud_user
from app.core.dependancies import get_db, get_current_user
from app.core.auth import authenticate, create_access_token
from app.schemas import schemas
from app.models.models import User

router = APIRouter()


@router.post("/register", status_code=201, response_model=schemas.User)
def register_user(
        db: Session = Depends(get_db),
        *,
        user_in: schemas.UserCreate,
        response: Response
) -> schemas.User:
    user = crud_user.get_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username taken.")

    user = crud_user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email taken.")
    user = crud_user.create(db=db, obj_in=user_in)
    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=user.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return user


@router.post("/register_guest", status_code=201, response_model=schemas.User)
def register_guest(response: Response, db: Session = Depends(get_db)) -> schemas.User:
    guest_schema = schemas.GuestCreate()
    guest = crud_user.create_guests(db=db, obj_in=guest_schema)
    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=guest.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return guest


@router.post("/login", response_model=schemas.User)
def login_user(
        response: Response,
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.User:
    # Set JWT for a user with data from OAuth2 request form body
    user = authenticate(username=form_data.username, plain_password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=user.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return user


@router.post("/login_guest", response_model=schemas.User)
def login_guest(db: Session = Depends(get_db), *, username: str, response: Response) -> schemas.User:
    guest = crud_user.get_by_username(db=db, username=username)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest account not found")
    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=guest.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return guest


@router.post("/logout", status_code=200, response_model=schemas.User)
def logout(response: Response, current_user: User = Depends(get_current_user)):
    user = current_user
    response.delete_cookie(key="access_token")
    return user


@router.put("/update", status_code=200, response_model=schemas.User)
def update_user(user_in: schemas.UserUpdate,
                response: Response,
                current_user: User = Depends(get_current_user),
                db: User = Depends(get_db)):
    if user_in.username != current_user.username:
        user = crud_user.get_by_username(db=db, username=user_in.username)
        if user:
            raise HTTPException(status_code=400, detail="Username taken.")
    if user_in.email != current_user.email:
        user = crud_user.get_by_email(db=db, email=user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Email taken.")

    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=user_in.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return crud_user.update(db=db, db_obj=current_user, obj_in=user_in)


@router.put("/claim_guest_account", status_code=200, response_model=schemas.User)
def claim_guest_account(
        response: Response,
        user_in: schemas.UserCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> schemas.User:
    if not current_user.is_guest:
        raise HTTPException(status_code=400, detail="User not a guest.")

    user = crud_user.get_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username taken.")

    user = crud_user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email taken.")

    user = crud_user.update(db=db, obj_in=user_in, db_obj=current_user)
    response.set_cookie(key="access_token",
                        value=f"Bearer {create_access_token(sub=user.username)}",
                        httponly=True,
                        expires=settings.COOKIE_EXPIRATION)
    return user


@router.delete("/delete", status_code=200, response_model=schemas.User)
def delete_account(
        response: Response,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> schemas.User:
    response.delete_cookie(key="access_token")
    return crud_user.remove(db=db, id=current_user.id)
