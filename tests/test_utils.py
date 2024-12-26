import pytest
from app.users.auth import get_password_hash, verify_password

@pytest.mark.asyncio
async def test_password_hashing():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False