from typing import Any

from pydantic import BaseModel, constr, validator


class CinemaBaseModel(BaseModel):
    pass


class UserBase(CinemaBaseModel):
    # Because mypy doesn't know about constr type
    login: constr(min_length=1, max_length=50)  # type: ignore
    name: constr(min_length=1, max_length=50)  # type: ignore


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: constr(min_length=1, max_length=50)  # type: ignore


class MovieBase(CinemaBaseModel):
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


class ReviewBase(CinemaBaseModel):
    text: constr(min_length=1)  # type: ignore


class ReviewRead(ReviewBase):
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class MarkBase(CinemaBaseModel):
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
