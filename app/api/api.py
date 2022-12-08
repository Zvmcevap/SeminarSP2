from fastapi import APIRouter, Depends

from app.api.endpoints import auth, users, games
from app.core.dependancies import get_current_user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])
api_router.include_router(games.router, prefix="/games", tags=["games"], dependencies=[Depends(get_current_user)])
