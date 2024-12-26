from fastapi import FastAPI, Depends, Request
import os
from fastapi.responses import RedirectResponse

from app.users.router import router as router_users
from app.users.router import get_router as router_users_for_get
from app.films.router import router as router_films
from app.genres.router import router as router_genres
from app.filmgenres.router import router as router_filmgenres
from app.directors.router import router as router_directors
from app.filmdirectors.router import router as router_filmdirectors
from app.actors.router import router as router_actors
from app.filmactors.router import router as router_filmactors
from app.filmgrades.router import router as router_filmgrades
from app.favoritefilms.router import router as router_favoritefilms
from app.exceptions import TokenExpiredException, TokenNotFoundException

from elasticsearch import Elasticsearch
from app.config import settings



# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'students.json')

app = FastAPI()

es = Elasticsearch(settings.ES_HOST)


@app.get("/")
def home_page():
    return {"message": "Привет, БД!"}


app.include_router(router_users)
app.include_router(router_users_for_get)
app.include_router(router_films)
app.include_router(router_genres)
app.include_router(router_filmgenres)
app.include_router(router_filmdirectors)
app.include_router(router_directors)
app.include_router(router_filmactors)
app.include_router(router_actors)
app.include_router(router_filmgrades)
app.include_router(router_favoritefilms)


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
    # Перенаправляем пользователя на страницу /auth
    return RedirectResponse(url="/auth")

@app.exception_handler(TokenNotFoundException)
async def token_not_found_exception_handler(request: Request, exc: TokenNotFoundException):
    # Перенаправляем пользователя на страницу /auth
    return RedirectResponse(url="/auth")
