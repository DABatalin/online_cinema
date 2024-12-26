from fastapi import APIRouter, Depends, HTTPException, status

from app.directors.dao import DirectorDAO
from app.directors.rb import RBDirector
from app.directors.schemas import SDirector, SDirectorAdd


router = APIRouter(prefix='/directors', tags=['Работа с режиссерами'])


@router.get("/", summary="Получить всех режиссеров")
async def get_all_directors(request_body: RBDirector = Depends()) -> list[SDirector]:
    return await DirectorDAO.find_all(**request_body.to_dict())


@router.get("/{director_id}", summary="Получить одного режиссера по айди")
async def get_director(request_body: RBDirector = Depends()) -> SDirector:
    response = await DirectorDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Режиссера с таким id не существует!')


@router.post("/add/")
async def add_director(director: SDirectorAdd) -> dict:
    check = await DirectorDAO.add(**director.dict())
    if check:
        return {"message": "Режиссер успешно добавлен!", "director": director}
    else:
        return {"message": "Ошибка при добавлении режиссера!"}
    

@router.delete("/del/{director_id}")
async def dell_director_by_id(director_id: int) -> dict:
    check = await DirectorDAO.delete(id=director_id)
    if check:
        return {"message": f"Режиссер с ID {director_id} удалена!"}
    else:
        return {"message": "Ошибка при удалении режиссера!"}
    
    
@router.put("/update/")
async def update_director(
    director: SDirector
) -> dict:
    try:
        print(director.dict())
        id = director.dict().pop('id')
        check = await DirectorDAO.update(filter_by={'id': id}, **director.dict())
        if check:
            return {"message": f"Режиссер с ID {director.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления режиссера или режиссер не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
