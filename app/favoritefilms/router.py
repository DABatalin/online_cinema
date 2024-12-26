from fastapi import APIRouter, Depends, HTTPException, status

from app.favoritefilms.dao import FavoriteFilmDAO
from app.favoritefilms.rb import RBFavoriteFilm
from app.favoritefilms.schemas import SFavoriteFilm, SFavoriteFilmAdd


router = APIRouter(prefix='/favoritefilms', tags=['Работа с любимыми фильмами'])


@router.get("/", summary="Получить все связи")
async def get_all_film_users(request_body: RBFavoriteFilm = Depends()) -> list[SFavoriteFilm]:
    return await FavoriteFilmDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}/{user_id}", summary="Получить связь фильма и режиссера")
async def get_film_and_user(request_body: RBFavoriteFilm = Depends()) -> SFavoriteFilm:
    response = await FavoriteFilmDAO.find_one_or_none_by_two_ids(request_body.film_id, request_body.user_id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сочетания фильм - пользователь id не существует!')


@router.post("/add/")
async def add_film_user(film_user: SFavoriteFilmAdd) -> dict:
    check = await FavoriteFilmDAO.add(**film_user.dict())
    if check:
        return {"message": "Любимый фильм успешно добавлен!", "film_user": film_user}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{user_id}")
async def dell_film_user_by_id(film_id: int, user_id: int) -> dict:
    check = await FavoriteFilmDAO.delete(film_id = film_id, user_id = user_id)
    if check:
        return {"message": f"Связь фильма {film_id} c пользователем {user_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении связи!"}
    

@router.put("/update/")
async def update_film(
    filmDirector: SFavoriteFilm
) -> dict:
    try:
        film_id = filmDirector.dict().pop('film_id')
        user_id = filmDirector.dict().pop('user_id')
        check = await FavoriteFilmDAO.update(filter_by={'film_id': film_id, 'user_id': user_id}, **filmDirector.dict())
        if check:
            return {"message": f"Связь ID {filmDirector.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
