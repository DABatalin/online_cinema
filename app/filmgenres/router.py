from fastapi import APIRouter, Depends, HTTPException, status

from app.filmgenres.dao import FilmGenreDAO
from app.filmgenres.rb import RBFilmGenre
from app.filmgenres.schemas import SFilmGenre, SFilmGenreAdd


router = APIRouter(prefix='/filmgenres', tags=['Работа с связью жанров и фильмом'])


@router.get("/", summary="Получить все связи")
async def get_all_film_genres(request_body: RBFilmGenre = Depends()) -> list[SFilmGenre]:
    return await FilmGenreDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}/{genre_id}", summary="Получить связь фильма и жанра")
async def get_film_and_genre(request_body: RBFilmGenre = Depends()) -> SFilmGenre:
    response = await FilmGenreDAO.find_one_or_none_by_two_ids(request_body.film_id, request_body.genre_id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Фильма с таким id не существует!')


@router.post("/add/")
async def add_film_genre(film_genre: SFilmGenreAdd) -> dict:
    check = await FilmGenreDAO.add(**film_genre.dict())
    if check:
        return {"message": "Связь жанра с фильмом успешно добавлена!", "film_genre": film_genre}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{genre_id}")
async def dell_film_genre_by_id(film_id: int, genre_id: int) -> dict:
    check = await FilmGenreDAO.delete(film_id = film_id, genre_id = genre_id)
    if check:
        return {"message": f"Связь фильма {film_id} c категорией {genre_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении связи!"}
    

@router.put("/update/")
async def update_film(
    filmGenre: SFilmGenre
) -> dict:
    try:
        film_id = filmGenre.dict().pop('id1')
        genre_id = filmGenre.dict().pop('id2')
        check = await FilmGenreDAO.update(filter_by={'film_id': film_id, 'genre_id': genre_id}, **filmGenre.dict())
        if check:
            return {"message": f"Связь ID {filmGenre.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
