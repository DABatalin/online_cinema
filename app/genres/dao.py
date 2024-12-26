from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.genres.models import Genre

from app.database import async_session_maker
from sqlalchemy import update, delete, event


class GenreDAO(BaseDAO):
    model = Genre
    table_name = "genres"

    # @classmethod
    # async def find_full_data(cls, genre_id: int):
    #     async with async_session_maker() as session:

    #         query = select(cls.model).filter_by(id=genre_id)
    #         result = await session.execute(query)
    #         genre_info = result.scalar_one_or_none()


    #         if not genre_info:
    #             return None

    #         genre_data = genre_info.to_dict()
    #         return genre_data
        

    # @classmethod
    # async def add_genre(cls, **genre_data: dict):
    #     async with async_session_maker() as session:
    #         async with session.begin():
    #             new_genre = Genre(**genre_data)
    #             session.add(new_genre)
    #             await session.flush()
    #             new_genre_id = new_genre.id
    #             await session.commit()
    #             return new_genre_id
            
            
    # @classmethod
    # async def delete_genre_by_id(cls, genre_id: int):
    #     async with async_session_maker() as session:
    #         async with session.begin():
    #             query = select(cls.model).filter_by(id=genre_id)
    #             result = await session.execute(query)
    #             genre_to_delete = result.scalar_one_or_none()

    #             if not genre_to_delete:
    #                 return None

    #             await session.execute(
    #                 delete(cls.model).filter_by(id=genre_id)
    #             )

    #             await session.commit()
    #             return genre_id