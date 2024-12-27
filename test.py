from fastapi.testclient import TestClient

from app.main import app
from app.films.dao import FilmDAO

client = TestClient(app)


def test_read_main():
	response = client.get('/')
	assert response.status_code == 200
	assert response.json() == {"message": "Привет, БД!"}


def test_add_film():
    film_data = {
        "title": "Тестовый фильм",
        "film_link": "string",
        "description": "Это тестовый фильм",
        "vote_count": 0,
        "average_rating": 10
    }
    
    response = client.post("/films/add/", json=film_data)
    
    assert response.status_code == 200
    
    assert response.json() == {
        "message": "Фильм успешно добавлен!",
        "film": film_data
    }
    
def test_add_film_error():
    film_data = {
        "description": "Это тестовый фильм"
    }
    
    response = client.post("/films/add/", json=film_data)
    
    assert response.status_code == 422

