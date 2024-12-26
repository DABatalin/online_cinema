# Основной файл для запуска программы

from typing import List, Dict
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch
from es_utils import get_movies_from_postgres, prepare_data_for_es, create_es_index, index_movies_to_es

# Параметры подключения к Elasticsearch
ES_HOSTS = ["http://localhost:9200/"]

app = FastAPI()
es_client = Elasticsearch(hosts=ES_HOSTS)
INDEX_NAME = "movies"

templates = Jinja2Templates(directory="templates")  # Указываем на папку с шаблонами


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """Отображает форму поиска."""
    return templates.TemplateResponse("search.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search_movies(request: Request, query: str = Form(...)):
    """Выполняет поиск фильмов и возвращает результаты."""
    results = []
    if query:
        es_query = {
            "size": 20,
            "query": {
                "bool": {
                    "should": [
                         {
                            "match_phrase": { # Точное совпадение названия, наивысший приоритет
                                "title": {
                                  "query": query,
                                  "boost": 1000  # Даем максимальный приоритет
                                }
                            }
                        },
                        {
                            "multi_match": {  # Частичное совпадение с хорошим приоритетом
                                "query": query,
                                "fields": ["title^5"],
                                 "boost": 20
                             }
                         },
                       {
                            "multi_match": {
                                "query": query,
                                "fields": ["genres^1"],  # Приоритет по жанрам
                                  "boost": 1
                            }
                        },
                    ],
                    "filter": {
                        "exists": {
                            "field": "vote_count"
                        }
                    },
                    "minimum_should_match": 1
                }
            },
           "sort": [
                 {
                   "_score": { # Сначала сортируем по релевантности (что даст приоритет точному соответствию)
                        "order": "desc"
                    }
                },
                 {
                    "vote_count": { # За тем по голосам
                        "order": "desc",
                        "unmapped_type": "float"
                    }
                 },
                 {
                    "average_rating": { # И затем по рейтингу
                        "order": "desc",
                        "unmapped_type": "float"
                    }
                 },
                 
            ]
        }
        es_results = es_client.search(index=INDEX_NAME, body=es_query)
        results = [hit["_source"] for hit in es_results["hits"]["hits"]]
    return templates.TemplateResponse("search.html", {"request": request, "results": results, "query": query})


if __name__ == "__main__":
    # Индексация при запуске
    # movies_from_db = get_movies_from_postgres()
    # prepared_movies = prepare_data_for_es(movies_from_db)
    # create_es_index(es_client, INDEX_NAME)
    # index_movies_to_es(es_client, INDEX_NAME, prepared_movies)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
