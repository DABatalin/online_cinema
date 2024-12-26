import pytest
from app.films.dao import FilmDAO
from app.genres.dao import GenreDAO
from app.actors.dao import ActorDAO

@pytest.mark.asyncio
async def test_film_dao(session):
    film_data = {"title": "Test Film", "description": "Test Description", "vote_count": 10, "average_rating": 5.0}
    film_id = await FilmDAO.add(**film_data)
    film = await FilmDAO.find_one_or_none_by_id(film_id)
    assert film.title == "Test Film"
    assert film.description == "Test Description"

@pytest.mark.asyncio
async def test_genre_dao(session):
    genre_data = {"name": "Test Genre"}
    genre_id = await GenreDAO.add(**genre_data)
    genre = await GenreDAO.find_one_or_none_by_id(genre_id)
    assert genre.name == "Test Genre"

@pytest.mark.asyncio
async def test_actor_dao(session):
    actor_data = {"name": "Test Actor", "surname": "Test Surname"}
    actor_id = await ActorDAO.add(**actor_data)
    actor = await ActorDAO.find_one_or_none_by_id(actor_id)
    assert actor.name == "Test Actor"
    assert actor.surname == "Test Surname"