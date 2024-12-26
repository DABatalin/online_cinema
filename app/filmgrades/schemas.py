from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SFilmGrade(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    film_id: int
    user_id: int
    grade: int = Field(..., ge=1, le=10, description="Оценка должен быть в диапазоне от 1 до 10")

    

class SFilmGradeAdd(BaseModel):
    film_id: int
    user_id: int
    grade: int = Field(..., ge=1, le=10, description="Оценка должен быть в диапазоне от 1 до 10")
    