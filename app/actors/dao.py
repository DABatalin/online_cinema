from sqlalchemy import insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.actors.models import Actor

from app.database import async_session_maker
from sqlalchemy import update, delete, event


class ActorDAO(BaseDAO):
    model = Actor
    table_name = "actors"
