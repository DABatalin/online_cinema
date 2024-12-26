from fastapi import APIRouter, Depends, HTTPException, status

from app.actors.dao import ActorDAO
from app.actors.rb import RBActor
from app.actors.schemas import SActor, SActorAdd


router = APIRouter(prefix='/actors', tags=['Работа с актерами'])


@router.get("/", summary="Получить всех актеров")
async def get_all_actors(request_body: RBActor = Depends()) -> list[SActor]:
    return await ActorDAO.find_all(**request_body.to_dict())


@router.get("/{actor_id}", summary="Получить одного актера по айди")
async def get_actor(request_body: RBActor = Depends()) -> SActor:
    response = await ActorDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Актера с таким id не существует!')


@router.post("/add/")
async def add_actor(actor: SActorAdd) -> dict:
    check = await ActorDAO.add(**actormodel_dump())
    if check:
        return {"message": "Актер успешно добавлен!", "actor": actor}
    else:
        return {"message": "Ошибка при добавлении актера!"}
    

@router.delete("/del/{actor_id}")
async def dell_actor_by_id(actor_id: int) -> dict:
    check = await ActorDAO.delete(id=actor_id)
    if check:
        return {"message": f"Актер с ID {actor_id} удален!"}
    else:
        return {"message": "Ошибка при удалении актера!"}
    
    
@router.put("/update/")
async def update_actor(
    actor: SActor
) -> dict:
    try:
        id = actormodel_dump().pop('id')
        check = await ActorDAO.update(filter_by={'id': id}, **actormodel_dump())
        if check:
            return {"message": f"Актер с ID {actor.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления актера или актер не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
