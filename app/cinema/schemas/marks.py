from typing import Any

from pydantic import BaseModel, validator


class MarkBase(BaseModel):
    score: int

    @validator('score')
    def score_in_interval(cls: Any, value: int) -> int:
        if value not in range(0, 11):
            raise ValueError('Score is incorrect')
        return value


class MarkRead(MarkBase):
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True


class MarkCreate(MarkBase):
    pass
