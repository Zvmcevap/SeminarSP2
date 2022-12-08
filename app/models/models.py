from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, default=f"Guest#{id}")
    email = Column(String, unique=True, index=True, nullable=True)
    has_email = Column(Boolean, nullable=False, default=True)
    hashed_password = Column(String, nullable=True)
    date_joined = Column(DateTime, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_guest = Column(Boolean, nullable=False, default=False)

    games = relationship("Game", back_populates="user", uselist=True)

    def __str__(self):
        return f"user_id: {self.id} username: {self.username}"


class Game(Base):
    id = Column(Integer, primary_key=True, index=True)
    played_at = Column(DateTime, index=True, nullable=False, default=datetime.now())
    round_length = Column(Integer, nullable=False)
    hits = Column(Integer, nullable=False)
    misses = Column(Integer, nullable=False)
    ending = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="games")
