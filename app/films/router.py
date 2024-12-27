from fastapi import APIRouter, Depends, HTTPException, status

from app.films.dao import FilmDAO
from app.films.rb import RBFilm
from app.films.schemas import SFilm, SFilmAdd
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User
from elasticsearch import Elasticsearch

import httpx
from typing import List
from pydantic import BaseModel

es = Elasticsearch("http://localhost:9200")

router = APIRouter(prefix='/films', tags=['Работа с фильмами'])

# URL вашего Docker-контейнера с FastAPI
RECOMMENDATION_API_URL = "http://localhost:80/recommend/"

class MovieList(BaseModel):
    movie_ids: List[int]

@router.get("/", summary="Получить все фильмы")
async def get_all_students(request_body: RBFilm = Depends()) -> list[SFilm]:
    return await FilmDAO.find_all(**request_body.to_dict())


@router.get("/search/")
async def search_films(query: str):
    # Поиск по названию и описанию
    result = es.search(index="movies", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description"]
            }
        }
    })
    return result["hits"]["hits"]


@router.get("/{film_id}", summary="Получить один фильм по айди")
async def get_film(request_body: RBFilm = Depends()) -> SFilm:
    response = await FilmDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Фильма с таким id не существует!')


@router.post("/add/")
async def add_film(film: SFilmAdd) -> dict:
    check = await FilmDAO.add(**film.model_dump())
    if check:
        return {"message": "Фильм успешно добавлен!", "film": film}
    else:
        return {"message": "Ошибка при добавлении фильма!"}
    

@router.delete("/del/{film_id}")
async def dell_film_by_id(film_id: int) -> dict:
    check = await FilmDAO.delete(id=film_id)
    if check:
        return {"message": f"Фильм с ID {film_id} удален!"}
    else:
        return {"message": "Ошибка при удалении фильма!"}
    

@router.put("/update/")
async def update_film(
    film: SFilm
) -> dict:
    try:
        id = film.model_dump().pop('id')
        check = await FilmDAO.update(filter_by={'id': id}, **film.model_dump())
        if check:
            return {"message": f"Фильм с ID {film.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления фильма или фильм не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}


@router.post("/recommend/", summary="Получить рекомендации по фильмам")
async def get_recommendations(movies: MovieList):
    try:
        # Отправляем POST-запрос к Docker-контейнеру
        async with httpx.AsyncClient() as client:
            response = await client.post(RECOMMENDATION_API_URL, json={"movie_ids": movies.movie_ids})
            response.raise_for_status()  # Проверяем на ошибки
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    

@router.post("/batch/", summary="Получить информацию о нескольких фильмах по их ID")
async def get_films_by_ids(movie_ids: List[int]) -> List[SFilm]:
    # Получаем все фильмы по переданным ID
    films = await FilmDAO.find_by_ids(movie_ids)
    
    if not films:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фильмы с такими ID не найдены!")
    
    return films