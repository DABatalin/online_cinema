from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text

from app.dao.base import BaseDAO
from app.favoritefilms.models import FavoriteFilm
from app.database import async_session_maker
from sqlalchemy import update, delete, event


class FavoriteFilmDAO(BaseDAO):
    model = FavoriteFilm
    table_name = "favoritefilms"

    @classmethod
    async def find_one_or_none_by_two_ids(cls, film_id: int, user_id: int):
        query = text(f"SELECT * FROM {cls.table_name} WHERE film_id = :film_id AND user_id = :user_id")
        params = {"film_id": film_id, "user_id": user_id}
        async with async_session_maker() as session:
            result = await session.execute(query, params)
            return result.fetchone()