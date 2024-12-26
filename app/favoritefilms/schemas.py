from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFavoriteFilm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int
    user_id: int

    

class SFavoriteFilmAdd(BaseModel):
    film_id: int
    user_id: int
    