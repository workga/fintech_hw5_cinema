from typing import Optional
from unicodedata import decimal
from attr import validate

from pydantic import BaseModel, constr, validator

# User
class UserBase(BaseModel):
    login: constr(min_length=1, max_length=50)
    name: constr(min_length=1, max_length=50)

class UserRead(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: constr(min_length=1, max_length=50)


# Movie
class MovieBase(BaseModel):
    title: constr(min_length=1, max_length=50)
    year: int

    @validator('year')
    def year_in_interval(cls, v):
        if v not in range(1900, 2100):
            raise ValueError('Year is incorrect')
        return v

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
    def round_rating(cls, v):
        return round(v, 2)

    class Config:
        orm_mode = True

# class MovieFilter(BaseModel):
#     substring: Optional[str] = None
#     year: Optional[int] = None
#     top: Optional[int] = None




# Review
class ReviewBase(BaseModel):
    text:constr(min_length=1)

class ReviewRead(ReviewBase):
    user_id: int
    movie_id: int
    
    class Config:
        orm_mode = True

class ReviewCreate(ReviewBase):
    pass


# Mark
class MarkBase(BaseModel):
    score: int

    @validator('score')
    def score_in_interval(cls, v):
        if v not in range(0, 11):
            raise ValueError('Score is incorrect')
        return v

class MarkRead(MarkBase):
    user_id: int
    movie_id: int
    
    class Config:
        orm_mode = True

class MarkCreate(MarkBase):
    pass