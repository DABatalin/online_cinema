from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text

from app.dao.base import BaseDAO
from app.filmactors.models import FilmActor
from app.database import async_session_maker
from sqlalchemy import update, delete, event


class FilmActorDAO(BaseDAO):
    model = FilmActor
    table_name = "filmactors"

    @classmethod
    async def find_one_or_none_by_two_ids(cls, film_id: int, actor_id: int):
        query = text(f"SELECT * FROM {cls.table_name} WHERE film_id = :film_id AND actor_id = :actor_id")
        params = {"film_id": film_id, "actor_id": actor_id}
        async with async_session_maker() as session:
            result = await session.execute(query, params)
            return result.fetchone()