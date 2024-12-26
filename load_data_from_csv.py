import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database import DATABASE_URL
from app.films.models import Film
from app.directors.models import Director
from app.filmgenres.models import FilmGenre
from app.filmdirectors.models import FilmDirector
from app.actors.models import Actor
from app.genres.models import Genre
from app.filmactors.models import FilmActor
from app.users.models import User
from app.filmgrades.models import FilmGrade
from app.favoritefilms.models import FavoriteFilm
import asyncio
# Убедитесь, что путь к CSV файлу правильный
csv_file_path = '/Users/moses/Documents/cs/Python/db_kp/kp/data/filmgenres.csv'

# Чтение CSV файла
df = pd.read_csv(csv_file_path)

df = df.where(pd.notnull(df), None)

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Преобразование данных из DataFrame в объекты модели
# for index, row in df.iterrows():
#     film = Film(
#         title=row['title'],
#         film_link=row['film_link'],
#         description=row['description'],
#         vote_count=row['vote_count'],
#         average_rating=row['average_rating']
#     )
#     session.add(film)

async def load_genres():
    async with AsyncSessionLocal() as session:
        try:
            # Преобразование данных из DataFrame в объекты модели Genre
            for index, row in df.iterrows():
                genre = Genre(
                    id=int(row['id']) if row['id'] is not None else None,  # Используем существующий id
                    name=row['name']
                )
                session.add(genre)
            
            # Сохранение изменений в базе данных
            await session.commit()
            print("Данные о жанрах успешно загружены в базу данных.")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при загрузке данных: {e}")


async def load_films():
    async with AsyncSessionLocal() as session:
        try:
            # Преобразование данных из DataFrame в объекты модели Film
            for index, row in df.iterrows():
                film = Film(
                    id=int(row['id']) if row['id'] is not None else None,
                    title=row['title'],
                    film_link=row['film_link'] if row['film_link'] is not None else None,
                    description=row['description'] if row['description'] is not None else None,
                    vote_count=int(row['vote_count']) if row['vote_count'] is not None else 0,
                    average_rating=float(row['average_rating']) if row['average_rating'] is not None else 0.0
                )
                session.add(film)
            
            # Сохранение изменений в базе данных
            await session.commit()
            print("Данные о фильмах успешно загружены в базу данных.")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при загрузке данных: {e}")


async def load_filmgenres():
    async with AsyncSessionLocal() as session:
        try:
            # Преобразование данных из DataFrame в объекты модели FilmGenre
            for index, row in df.iterrows():
                film_genre = FilmGenre(
                    film_id=int(row['film_id']) if row['film_id'] is not None else None,
                    genre_id=int(row['genre_id']) if row['genre_id'] is not None else None
                )
                session.add(film_genre)
            
            # Сохранение изменений в базе данных
            await session.commit()
            print("Данные о связях фильмов и жанров успешно загружены в базу данных.")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при загрузке данных: {e}")


# Запуск асинхронной функции
async def main():
    await load_filmgenres()

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())