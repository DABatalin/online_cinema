from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFilmGenre(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int
    genre_id: int

    

class SFilmGenreAdd(BaseModel):
    film_id: int
    genre_id: int
    