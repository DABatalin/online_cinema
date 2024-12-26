from fastapi import APIRouter, Depends, HTTPException, status

from app.filmgrades.dao import FilmGradeDAO
from app.filmgrades.rb import RBFilmGrade
from app.filmgrades.schemas import SFilmGrade, SFilmGradeAdd


router = APIRouter(prefix='/filmgrades', tags=['Работа с оценками фильмов'])


@router.get("/", summary="Получить все оценки")
async def get_all_film_grades(request_body: RBFilmGrade = Depends()) -> list[SFilmGrade]:
    return await FilmGradeDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}/{user_id}", summary="Получить связь фильма и user'а")
async def get_film_and_grade(request_body: RBFilmGrade = Depends()) -> SFilmGrade:
    response = await FilmGradeDAO.find_one_or_none_by_two_ids(request_body.film_id, request_body.user_id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сочетания фильм - пользователь id не существует!')


@router.post("/add/")
async def add_film_grade(film_grade: SFilmGradeAdd) -> dict:
    check = await FilmGradeDAO.add(**film_grade.dict())
    if check:
        return {"message": "Связь режиссера с фильмом успешно добавлена!", "film_grade": film_grade}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{user_id}")
async def dell_film_grade_by_id(film_id: int, user_id: int) -> dict:
    check = await FilmGradeDAO.delete(film_id = film_id, user_id = user_id)
    if check:
        return {"message": f"Связь фильма {film_id} c режиссером {user_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении связи!"}
    

@router.put("/update/")
async def update_film(
    filmGrade: SFilmGrade
) -> dict:
    try:
        print(filmGrade.dict())
        film_id = filmGrade.dict().pop('film_id')
        user_id = filmGrade.dict().pop('user_id')
        print(filmGrade.dict())
        check = await FilmGradeDAO.update(filter_by={'film_id': film_id, 'user_id': user_id}, **filmGrade.dict())
        if check:
            return {"message": f"Связь ID {filmGrade.film_id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
