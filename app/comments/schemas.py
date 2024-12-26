from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class SComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    film_id: int
    user_id: int
    comment_text: str = Field(None, description="Текст комментария")

    

class SCommentAdd(BaseModel):
    film_id: int
    user_id: int
    comment_text: str = Field(None, description="Текст комментария")
    