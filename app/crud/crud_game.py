import datetime
from typing import List

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.models import Game, User
from app.schemas.schemas import GameCreate, GameUpdate


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    def get_my_games(self, db: Session, user: User) -> List[Game]:
        return db.query(Game).filter(Game.user == user).all()

    def create(self, db: Session, *, obj_in: GameCreate) -> Game:
        db_obj = Game(**obj_in.dict())
        db_obj.played_at = datetime.datetime.now()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_game = CRUDGame(Game)
