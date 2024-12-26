import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import async_session_maker, engine, Base

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session

@pytest.fixture
def client():
    return TestClient(app)