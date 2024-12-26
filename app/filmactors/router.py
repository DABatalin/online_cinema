from fastapi import APIRouter, Depends, HTTPException, status

from app.filmactors.dao import FilmActorDAO
from app.filmactors.rb import RBFilmActor
from app.filmactors.schemas import SFilmActor, SFilmActorAdd


router = APIRouter(prefix='/filmactors', tags=['Работа с связью актеров и фильмом'])


@router.get("/", summary="Получить все связи")
async def get_all_film_actors(request_body: RBFilmActor = Depends()) -> list[SFilmActor]:
    return await FilmActorDAO.find_all(**request_body.to_dict())


@router.get("/{film_id}/{actor_id}", summary="Получить связь фильма и актера")
async def get_film_and_actor(request_body: RBFilmActor = Depends()) -> SFilmActor:
    response = await FilmActorDAO.find_one_or_none_by_two_ids(request_body.film_id, request_body.actor_id)
    if response: 
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого сочетания фильм - актер id не существует!')


@router.post("/add/")
async def add_film_actor(film_actor: SFilmActorAdd) -> dict:
    check = await FilmActorDAO.add(**film_actor.dict())
    if check:
        return {"message": "Связь актера с фильмом успешно добавлена!", "film_actor": film_actor}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{actor_id}")
async def dell_film_actor_by_id(film_id: int, actor_id: int) -> dict:
    check = await FilmActorDAO.delete(film_id = film_id, actor_id = actor_id)
    if check:
        return {"message": f"Связь фильма {film_id} c актером {actor_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении связи!"}
    

@router.put("/update/")
async def update_film(
    filmActor: SFilmActor
) -> dict:
    try:
        film_id = filmActor.dict().pop('id1')
        actor_id = filmActor.dict().pop('id2')
        check = await FilmActorDAO.update(filter_by={'film_id': film_id, 'actor_id': actor_id}, **filmActor.dict())
        if check:
            return {"message": f"Связь ID {filmActor.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
