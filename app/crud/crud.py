import datetime

from sqlalchemy.orm import Session
from typing import List, Union

import app.core.security
from app.models.models import User, Game
from app.schemas import schemas
from app.core import security


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Union[User, None]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Union[User, None]:
    user = db.query(User).filter(User.has_email == True, User.email == email).first()
    return user


def get_users(db: Session, offset: int = 0, limit: int = 0) -> Union[List[User], None]:
    if limit == 0:
        return db.query(User).offset(offset).limit(limit).all()
    return db.query(User).offset(offset).all()


def create_user(db: Session, user: schemas.UserCreate) -> User:
    hashed_pw = security.get_password_hash(user.plain_password)
    creation_time = datetime.datetime.now()
    has_email = True if user.email else False
    db_user = User(
        username=user.username,
        email=user.email,
        date_joined=creation_time,
        hashed_password=hashed_pw,
        has_email=has_email,
        admin=user.admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> User:
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete


def update_user(db: Session, user_id: int, new_user_data: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.username = new_user_data.username
    if new_user_data.email:
        db_user = new_user_data.email
        db_user.has_email = True

    if new_user_data.plain_password:
        hashed_pass = app.core.security.get_password_hash(new_user_data.plain_password)
        db_user.password = hashed_pass
    db.commit()
    return db_user


def update_password(db: Session, old_plain_password, plain_password: str, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id)
    if app.core.security.check_password(old_plain_password, user.hashed_password):
        hashed_pass = app.core.security.get_password_hash(plain_password)
        user.hashed_password = hashed_pass
        return True
    return False


# Games
def get_games_of_user(db: Session, user_id: int) -> List[Game]:
    return db.query(Game).filter(Game.user_id == user_id).all()


def get_all_games(db: Session) -> List[Game]:
    return db.query(Game).all()


def create_game(db: Session, game: schemas.Game) -> Game:
    played_at = datetime.datetime.now()

    db_game = Game(
        hits=game.hits,
        misses=game.misses,
        ending=game.ending,
        played_at=played_at,
        round_length=game.round_length,
        user_id=schemas.Game.user_id,
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game
