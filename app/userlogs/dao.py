from app.dao.base import BaseDAO
from app.userlogs.models import UserLog
from sqlalchemy.sql import text
from app.database import async_session_maker

class UserLogDAO(BaseDAO):
    model = UserLog
    table_name = "userlogs"