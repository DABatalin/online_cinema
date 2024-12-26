# запустить эту программу, чтобы загрузить данные из Базы данных в ElasticSearch

import psycopg2
from elasticsearch import Elasticsearch
from typing import List, Dict

# Параметры подключения к PostgreSQL (заменить на свои!)
DB_CONFIG = {
    "host": "localhost",
    "database": "movies_db",
    "user": "postgres",
    "password": "qwerty",
}

# Параметры подключения к Elasticsearch
ES_HOSTS = ["http://localhost:9200/"]

def get_movies_from_postgres() -> List[tuple]:
    """Получает данные о фильмах из PostgreSQL."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT
            f.id,
            f.title,
            f.film_link,
            f.average_rating,
            f.description,
            f.vote_count,
            ARRAY_AGG(g.name) AS genres
        FROM films f
        LEFT JOIN film_genres fg ON f.id = fg.film_id
        LEFT JOIN genre g ON g.id = ANY(fg.genre_ids)
        GROUP BY f.id, f.title, f.film_link,f.average_rating, f.description,f.vote_count
    """)
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return movies


def prepare_data_for_es(movies: List[tuple]) -> List[Dict]:
    """Подготавливает данные для индексации в Elasticsearch."""
    documents = []
    for movie_id, title, film_link, average_rating, description, vote_count, genres in movies:
        doc = {
            "movieID": movie_id,
            "title": title,
            "film_link": film_link,
            "average_rating": average_rating,
            "description": description,
            "vote_count": vote_count,
            "genres": genres if genres else [],
        }
        documents.append(doc)
    return documents


def create_es_index(es_client: Elasticsearch, index_name: str):
    """Создает индекс в Elasticsearch."""
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    "movieID": {"type": "integer"}, # id из БД
                    "title": {"type": "text", "analyzer": "english", "search_analyzer": "english"},
                    "genres": {"type": "text", "analyzer": "standard"},
                     "vote_count": {"type": "float"},
                     "average_rating": {"type": "float"},
                     "film_link": {"type": "text"},
                     "description": {"type": "text", "analyzer": "english"}

                }
            },
        )


def index_movies_to_es(es_client: Elasticsearch, index_name: str, documents: List[Dict]):
    """Индексирует документы в Elasticsearch."""
    for doc in documents:
        es_client.index(index=index_name, document=doc)


if __name__ == '__main__':
    movies_from_db = get_movies_from_postgres()
    prepared_movies = prepare_data_for_es(movies_from_db)

    es_client = Elasticsearch(hosts=ES_HOSTS)
    index_name = "movies"
    create_es_index(es_client, index_name)
    index_movies_to_es(es_client, index_name, prepared_movies)
    print("Данные успешно проиндексированы в Elasticsearch!")
