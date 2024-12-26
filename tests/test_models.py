import pytest
from app.films.models import Film
from app.genres.models import Genre
from app.actors.models import Actor

@pytest.mark.asyncio
async def test_film_model():
    film = Film(title="Test Film", description="Test Description", vote_count=10, average_rating=5.0)
    assert film.title == "Test Film"
    assert film.description == "Test Description"
    assert film.vote_count == 10
    assert film.average_rating == 5.0

@pytest.mark.asyncio
async def test_genre_model():
    genre = Genre(name="Test Genre")
    assert genre.name == "Test Genre"

@pytest.mark.asyncio
async def test_actor_model():
    actor = Actor(name="Test Actor", surname="Test Surname")
    assert actor.name == "Test Actor"
    assert actor.surname == "Test Surname"