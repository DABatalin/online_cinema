from fastapi import APIRouter, Depends, HTTPException, status

from app.comments.dao import CommentDAO
from app.comments.rb import RBComment
from app.comments.schemas import SComment, SCommentAdd


router = APIRouter(prefix='/comments', tags=['Работа с комментариями'])


@router.get("/", summary="Получить все комментарии")
async def get_all_film_comments(request_body: RBComment = Depends()) -> list[SComment]:
    return await CommentDAO.find_all()


@router.get("/{comment_id}", summary="Получить один комментарий по айди")
async def get_actor(request_body: RBComment = Depends()) -> SComment:
    response = await CommentDAO.find_one_or_none_by_id(request_body.id)
    if response: 
        return response 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Комментария с таким айди не существует!')


@router.post("/add/")
async def add_film_comment(film_comment: SCommentAdd) -> dict:
    check = await CommentDAO.add(**film_comment.model_dump())
    if check:
        return {"message": "Комментарий успешно добавлен!", "film_comment": film_comment}
    else:
        return {"message": "Ошибка при добавлении связи!"}
    

@router.delete("/del/{film_id}/{user_id}")
async def del_film_comment_by_id(film_id: int, user_id: int) -> dict:
    check = await CommentDAO.delete(film_id = film_id, user_id = user_id)
    if check:
        return {"message": f"Комментарий удален!"}
    else:
        return {"message": "Ошибка при удалении комментария!"}
    

@router.put("/update/")
async def update_film(
    comment: SComment
) -> dict:
    try:
        id = comment.model_dump().pop('id')
        check = await CommentDAO.update(filter_by={'id': id}, **comment.model_dump())
        if check:
            return {"message": f"Коментарий ID {comment.id} успешно обновлен!"}
        else:
            return {"message": "Ошибка обновления связи."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
