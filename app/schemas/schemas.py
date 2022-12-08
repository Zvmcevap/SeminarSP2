from typing import List, Union, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Base model shared by all Game Schemas (User will be the same way)
class GameBase(BaseModel):
    hits: int
    misses: int
    ending: str
    round_length: int
    user_id: int
    played_at: datetime = datetime.now()


# attributes exclusively needed for creating the schema
class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


# attributes added when returning the schema
class Game(GameBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr]


class UserCreate(UserBase):
    plain_password: str

    class Config:
        orm_mode = True


class UserSuperCreate(UserCreate):
    is_superuser: bool

    class Config:
        orm_mode = True


class UserUpdatePassword(UserBase):
    plain_password: str
    new_password: str


class User(UserBase):
    id: int
    date_joined: datetime
    has_email: bool
    is_superuser: bool
    is_guest: bool

    games: List[Game] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


# Guest account
class GuestBase(UserBase):
    username: Optional[str]
    has_email = False
    is_guest = True


class GuestCreate(GuestBase):
    date_joined: datetime = datetime.now()


class Guest(User):
    pass
