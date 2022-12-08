from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.crud.crud_user import crud_user
from app.models.models import User
from app.schemas import schemas
from app.core.dependancies import get_db, get_current_user, get_superuser

router = APIRouter()


@router.get("/users", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)) -> List[schemas.User]:
    return crud_user.get_multi(db=db)


@router.get("/me", status_code=200, response_model=schemas.User)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

