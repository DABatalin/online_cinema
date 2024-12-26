from fastapi import APIRouter, Depends, HTTPException, status

from app.filmdirectors.dao import FilmDirectorDAO
from app.filmdirectors.rb import RBFilmDirector
from app.filmdirectors.schemas import SFilmDirector, SFilmDirectorAdd


router = APIRouter(prefix='/filmdirectors', tags=['Работа с связью режиссеров и фильмом'])


@router.get("/", summary="Получить все связи")
async def get_all_film_directors(request_body: RBFilmDirector = Depends()) -> list[SFilmDirector]:
    return await FilmDirectorDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}/{director_id}", summary="Получить связь фильма и режиссера")
async def get_film_and_director(request_body: RBFilmDirector = Depends()) -> SFilmDirector:
    response = await FilmDirectorDAO.find_one_or_none_by_two_ids(request_body.film_id, request_body.director_id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Не существует такого сочетания фильм - режиссер id не существует!')


@router.post("/add/")
async def add_film_director(film_director: SFilmDirectorAdd) -> dict:
    check = await FilmDirectorDAO.add(**film_director.dict())
    if check:
        return {"message": "Связь режиссера с фильмом успешно добавлена!", "film_director": film_director}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{director_id}")
async def dell_film_director_by_id(film_id: int, director_id: int) -> dict:
    check = await FilmDirectorDAO.delete(film_id = film_id, director_id = director_id)
    if check:
        return {"message": f"Связь фильма {film_id} c режиссером {director_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении связи!"}
    

@router.put("/update/")
async def update_film(
    filmDirector: SFilmDirector
) -> dict:
    try:
        film_id = filmDirector.dict().pop('id1')
        director_id = filmDirector.dict().pop('id2')
        check = await FilmDirectorDAO.update(filter_by={'film_id': film_id, 'director_id': director_id}, **filmDirector.dict())
        if check:
            return {"message": f"Связь ID {filmDirector.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
