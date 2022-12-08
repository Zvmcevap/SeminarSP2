import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate, GuestCreate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if user:
            if user.email:
                return user
        return None

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        db_obj.has_email = True
        db_obj.is_guest = False
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # Remove plain text password
        create_data = obj_in.dict()
        create_data.pop("plain_password")
        create_data["date_joined"] = datetime.datetime.now()
        db_obj = User(**create_data)
        # Add the hashy password
        db_obj.hashed_password = get_password_hash(obj_in.plain_password)
        db_obj.has_email = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def create_guests(self, db: Session, *, obj_in: GuestCreate) -> User:
        guest = User(**obj_in.dict())
        guest.username = "Guest"
        db.add(guest)
        db.commit()
        db.refresh(guest)
        guest.username = guest.username + f"#{guest.id}"
        guest.date_joined = datetime.datetime.now()
        db.commit()
        db.refresh(guest)
        return guest


crud_user = CRUDUser(User)
