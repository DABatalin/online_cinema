from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_uniq, int_pk

from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


created_at = Annotated[datetime, mapped_column(server_default=func.now())]

class UserLog(Base):
    
    log_id: Mapped[int_pk]
    user_id: Mapped[int]
    login_date: Mapped[created_at]
    operation_status: Mapped[str]
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.log_id})"