from fastapi import FastAPI, HTTPException
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Загрузка модели и данных
with open('model_02_30.pkl', 'rb') as file:
    knn_model = pickle.load(file)

rating_small = pd.read_csv('clear_rt.csv')

def prepare_data(rating_df):
    user_movie_matrix = rating_df.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    sparse_matrix = csr_matrix(user_movie_matrix)
    return sparse_matrix, user_movie_matrix.index, user_movie_matrix.columns

sparse_matrix, movie_indices, user_indices = prepare_data(rating_small)

class MovieList(BaseModel):
    movie_ids: List[int]

def recommend_movies_for_new_user(favorite_movies, knn_model, sparse_matrix, movie_indices, top_n=20):
    movie_id_to_index = {movie: idx for idx, movie in enumerate(movie_indices)}
    favorite_indices = [movie_id_to_index[movie] for movie in favorite_movies if movie in movie_id_to_index]

    similarity_scores = []
    for idx in favorite_indices:
        distances, indices = knn_model.kneighbors(sparse_matrix[idx], n_neighbors=top_n + len(favorite_movies))
        similarity_scores.extend(indices.flatten())

    recommendation_counts = pd.Series(similarity_scores).value_counts()
    recommendation_counts = recommendation_counts[~recommendation_counts.index.isin(favorite_indices)]
    
    recommended_indices = recommendation_counts.nlargest(top_n).index
    recommended_movies = [int(movie_indices[i]) for i in recommended_indices]  # Преобразуем в int
    return recommended_movies

@app.post("/recommend/")
async def recommend(movies: MovieList):
    try:
        recommended_movies = recommend_movies_for_new_user(movies.movie_ids, knn_model, sparse_matrix, movie_indices, top_n=30)
        return {"recommended_movies": recommended_movies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))