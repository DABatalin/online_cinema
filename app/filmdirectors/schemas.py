from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFilmDirector(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int
    director_id: int

    

class SFilmDirectorAdd(BaseModel):
    film_id: int
    director_id: int
    