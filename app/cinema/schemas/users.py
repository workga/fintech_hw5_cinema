from pydantic import BaseModel, constr


class UserBase(BaseModel):
    # Because mypy doesn't know about constr type
    login: constr(min_length=1, max_length=50)  # type: ignore
    name: constr(min_length=1, max_length=50)  # type: ignore


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: constr(min_length=1, max_length=50)  # type: ignore
