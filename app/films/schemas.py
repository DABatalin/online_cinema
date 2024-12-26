from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFilm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str = Field(..., min_length=1, max_length=100, description="Название фильма, от 1 до 100 символов")
    film_link: Optional[str] = Field(None, max_length=1000, description="Ссылка на фильм")
    description: Optional[str] = Field(None, max_length=100000, description="Описание фильма")
    vote_count: int = Field(..., description="Количество оценок")
    average_rating: float = Field(..., ge=0, le=10, description="Рейтинг от 1 до 5")
    

class SFilmAdd(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название фильма, от 1 до 100 символов")
    film_link: str = Field(..., min_length=1, max_length=1000, description="Ссылка на фильм")
    description: Optional[str] = Field(None, max_length=100000, description="Описание фильма")
    vote_count: int = Field(..., description="Количество оценок")
    average_rating: float = Field(..., ge=0, le=10, description="Рейтинг от 1 до 5")