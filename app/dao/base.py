from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from app.database import async_session_maker

class BaseDAO:
    model = None
    table_name = None  # Имя таблицы, связанной с моделью

    @classmethod
    async def find_all(cls, **filter_by):
        filters = {key: value for key, value in filter_by.items()}
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters])
        query = text(f"SELECT * FROM {cls.table_name} " + (f"WHERE {where_clause}" if where_clause else ""))

        async with async_session_maker() as session:
            result = await session.execute(query, filters)
            return result.fetchall()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        query = text(f"SELECT * FROM {cls.table_name} WHERE id = :id")
        params = {"id": data_id}
        async with async_session_maker() as session:
            result = await session.execute(query, params)
            return result.fetchone()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        filters = {key: value for key, value in filter_by.items()}
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters])
        query = text(f"SELECT * FROM {cls.table_name} " + (f"WHERE {where_clause}" if where_clause else ""))

        async with async_session_maker() as session:
            result = await session.execute(query, filters)
            return result.fetchone()

    @classmethod
    async def add(cls, **values):
        columns = ", ".join(values.keys())
        placeholders = ", ".join([f":{key}" for key in values.keys()])
        query = text(f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})")
        print(query)
        print(values)
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(query, values)
                    await session.commit()
                    return result.rowcount
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    @classmethod
    async def update(cls, filter_by, **values):
        print(cls)
        set_clause = ", ".join([f"{key} = :set_{key}" for key in values.keys()])
        where_clause = " AND ".join([f"{key} = :filter_{key}" for key in filter_by.keys()])
        query = text(f"UPDATE {cls.table_name} SET {set_clause} WHERE {where_clause}")

        params = {f"set_{key}": value for key, value in values.items()}
        params.update({f"filter_{key}": value for key, value in filter_by.items()})

        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(query, params)
                    await session.commit()
                    return result.rowcount
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        filters = {key: value for key, value in filter_by.items()}
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters])
        query = text(f"DELETE FROM {cls.table_name} " + (f"WHERE {where_clause}" if where_clause else ""))

        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(query, filters)
                    await session.commit()
                    return result.rowcount
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
