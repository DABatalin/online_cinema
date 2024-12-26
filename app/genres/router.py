from fastapi import APIRouter, Depends, HTTPException, status

from app.genres.dao import GenreDAO
from app.genres.rb import RBGenre
from app.genres.schemas import SGenre, SGenreAdd


router = APIRouter(prefix='/genres', tags=['Работа с жанрми'])


@router.get("/", summary="Получить все жанра")
async def get_all_genres(request_body: RBGenre = Depends()) -> list[SGenre]:
    return await GenreDAO.find_all(**request_body.to_dict())


@router.get("/{genre_id}", summary="Получить одну жанр по айди")
async def get_genre(request_body: RBGenre = Depends()) -> SGenre:
    response = await GenreDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Жанра с таким id не существует!')


@router.post("/add/")
async def add_genre(genre: SGenreAdd) -> dict:
    check = await GenreDAO.add(**genre.model_dump())
    if check:
        return {"message": "Жанр успешно добавлена!", "genre": genre}
    else:
        return {"message": "Ошибка при добавлении жанра!"}
    

@router.delete("/del/{genre_id}")
async def dell_genre_by_id(genre_id: int) -> dict:
    check = await GenreDAO.delete(id=genre_id)
    if check:
        return {"message": f"Жанр с ID {genre_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении жанра!"}
    
    
@router.put("/update/")
async def update_genre(
    genre: SGenre
) -> dict:
    try:
        print(genre.model_dump())
        id = genre.model_dump().pop('id')
        check = await GenreDAO.update(filter_by={'id': id}, **genre.model_dump())
        if check:
            return {"message": f"Жанр с ID {genre.id} успешно обновлена!"}
        else:
            return {"message": "Ошибка обновления катгории или жанр не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
