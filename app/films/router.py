from fastapi import APIRouter, Depends, HTTPException, status

from app.films.dao import FilmDAO
from app.films.rb import RBFilm
from app.films.schemas import SFilm, SFilmAdd
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User

router = APIRouter(prefix='/films', tags=['Работа с фильмами'])


@router.get("/", summary="Получить все фильмы")
async def get_all_students(request_body: RBFilm = Depends()) -> list[SFilm]:
    return await FilmDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}", summary="Получить один фильм по айди")
async def get_film(request_body: RBFilm = Depends()) -> SFilm:
    response = await FilmDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Фильма с таким id не существует!')


@router.post("/add/")
async def add_film(film: SFilmAdd) -> dict:
    check = await FilmDAO.add(**film.dict())
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
        id = film.dict().pop('id')
        check = await FilmDAO.update(filter_by={'id': id}, **film.dict())
        if check:
            return {"message": f"Фильм с ID {film.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления фильма или фильм не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
