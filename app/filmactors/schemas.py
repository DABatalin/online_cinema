from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFilmActor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int
    actor_id: int

    

class SFilmActorAdd(BaseModel):
    film_id: int
    actor_id: int
    