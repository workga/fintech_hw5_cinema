from pydantic import BaseModel, constr


class ReviewBase(BaseModel):
    text: constr(min_length=1)  # type: ignore


class ReviewRead(ReviewBase):
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass
