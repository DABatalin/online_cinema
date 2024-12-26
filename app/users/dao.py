from app.dao.base import BaseDAO
from app.users.models import User
from sqlalchemy.sql import text
from app.database import async_session_maker

class UserDAO(BaseDAO):
    model = User
    table_name = "users"