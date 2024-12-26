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