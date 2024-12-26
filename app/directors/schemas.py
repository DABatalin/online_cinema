from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SDirector(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    surname: str = Field(..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")

    

class SDirectorAdd(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    surname: str = Field(..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")