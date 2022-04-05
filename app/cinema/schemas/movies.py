from typing import Any

from pydantic import BaseModel, constr, validator


class MovieBase(BaseModel):
    title: constr(min_length=1, max_length=50)  # type: ignore
    year: int

    @validator('year')
    def year_in_interval(cls: Any, year: int) -> int:
        if year not in range(1900, 2100):
            raise ValueError('Year is incorrect')
        return year


class MovieRead(MovieBase):
    id: int

    class Config:
        orm_mode = True


class MovieCreate(MovieBase):
    pass


class MovieStats(MovieBase):
    id: int

    reviews_count: int
    marks_count: int
    rating: float

    @validator('rating')
    def round_rating(cls: Any, value: float) -> float:
        return round(value, 2)

    class Config:
        orm_mode = True
