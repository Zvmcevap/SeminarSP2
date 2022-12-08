from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from sqladmin import Admin, ModelView

from app.api.api import api_router
from app.database.session import engine
from app.models.models import User, Game
from app.core.dependancies import admin_authenticator

app = FastAPI(title="Wack-a-Krt")
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
admin = Admin(app=app, engine=engine, authentication_backend=admin_authenticator)


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.has_email,
        User.date_joined,
        User.is_guest,
        User.is_superuser,
        User.games
    ]


class GameAdmin(ModelView, model=Game):
    column_list = [
        Game.id,
        Game.user,
        Game.played_at,
        Game.round_length,
        Game.hits,
        Game.misses,
        Game.ending
    ]


admin.add_view(UserAdmin)
admin.add_view(GameAdmin)


@app.get("/")
def root():
    return FileResponse("app/static/index.html")


@app.get("/test")
def test():
    return "test"


app.include_router(api_router)
