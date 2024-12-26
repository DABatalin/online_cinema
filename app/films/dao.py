from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.films.models import Film

from app.database import async_session_maker
from sqlalchemy import update, delete, event


class FilmDAO(BaseDAO):
    model = Film
    table_name = "films"

    # @classmethod
    # async def find_full_data(cls, film_id: int):
    #     async with async_session_maker() as session:
    #         # Запрос для получения информации о студенте вместе с информацией о факультете
    #         query = select(cls.model).filter_by(id=film_id)
    #         result = await session.execute(query)
    #         film_info = result.scalar_one_or_none()

    #         # Если студент не найден, возвращаем None
    #         if not film_info:
    #             return None

    #         film_data = film_info.to_dict()
    #         return film_data
        

    # @classmethod
    # async def add_film(cls, **film_data: dict):
    #     async with async_session_maker() as session:
    #         async with session.begin():
    #             new_film = Film(**film_data)
    #             session.add(new_film)
    #             await session.flush()
    #             new_film_id = new_film.id
    #             await session.commit()
    #             return new_film_id
            
            
    # @classmethod
    # async def delete_film_by_id(cls, film_id: int):
    #     async with async_session_maker() as session:
    #         async with session.begin():
    #             query = select(cls.model).filter_by(id=film_id)
    #             result = await session.execute(query)
    #             film_to_delete = result.scalar_one_or_none()

    #             if not film_to_delete:
    #                 return None

    #             # Удаляем фильм
    #             await session.execute(
    #                 delete(cls.model).filter_by(id=film_id)
    #             )

    #             await session.commit()
    #             return film_id