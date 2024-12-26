import pytest
from fastapi import status
from app.films.schemas import SFilmAdd
from app.genres.schemas import SGenreAdd
from app.actors.schemas import SActorAdd

@pytest.mark.asyncio
async def test_create_film(client):
    film_data = {
        "title": "Test Film",
        "film_link": "http://example.com",
        "description": "Test Description",
        "vote_count": 10,
        "average_rating": 5.0
    }
    response = client.post("/films/add/", json=film_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Фильм успешно добавлен!"

@pytest.mark.asyncio
async def test_create_genre(client):
    genre_data = {"name": "Test Genre"}
    response = client.post("/genres/add/", json=genre_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Жанр успешно добавлена!"

@pytest.mark.asyncio
async def test_create_actor(client):
    actor_data = {"name": "Test Actor", "surname": "Test Surname"}
    response = client.post("/actors/add/", json=actor_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Актер успешно добавлен!"