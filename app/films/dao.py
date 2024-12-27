from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.films.models import Film
from app.films.schemas import SFilm

from app.database import async_session_maker
from sqlalchemy import update, delete, event
from typing import List



class FilmDAO(BaseDAO):
    model = Film
    table_name = "films"

    @classmethod
    async def find_by_ids(cls, movie_ids: List[int]) -> List[SFilm]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id.in_(movie_ids))
            result = await session.execute(query)
            return result.scalars().all()
        
        