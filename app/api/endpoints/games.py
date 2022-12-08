from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.models.models import Game, User
from app.crud.crud_game import crud_game
from app.core.dependancies import get_db, get_current_user

router = APIRouter()


@router.get("/all_games", response_model=List[schemas.Game])
def get_all_games(db: Session = Depends(get_db)) -> List[schemas.Game]:
    return crud_game.get_multi(db=db)


@router.get("/my_games", response_model=List[schemas.Game])
def get_my_games(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> List[schemas.Game]:
    return crud_game.get_my_games(db=db, user=current_user)


@router.post("/save_game", response_model=schemas.Game)
def save_game(
        game_in: schemas.GameCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> schemas.Game:
    game_in.user_id = current_user.id
    return crud_game.create(db=db, obj_in=game_in)

