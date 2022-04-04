from typing import List

from fastapi import Depends, Path, status, APIRouter

from app.cinema import crud
from app.cinema.auth import auth_user
from app.cinema.models import Mark, Review, User
from app.cinema.pagination import Page, pagination
from app.cinema.schemas import (
    MarkRead,
    ReviewRead,
    UserCreate,
    UserRead,
)

router = APIRouter()

@router.get('/users', dependencies=[Depends(auth_user)], response_model=List[UserRead])
def list_users(page: Page = Depends(pagination)) -> List[User]:
    db_users = crud.users.get_users(page=page)

    return db_users


@router.post('/users', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> User:
    db_user = crud.users.create_user(user)

    return db_user


@router.get(
    '/users/{user_id}/reviews',
    dependencies=[Depends(auth_user)],
    response_model=List[ReviewRead],
)
def list_user_reviews(
    user_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Review]:
    db_reviews = crud.reviews.get_reviews(
        page=page,
        user_id=user_id,
    )

    return db_reviews


@router.get(
    '/users/{user_id}/marks',
    dependencies=[Depends(auth_user)],
    response_model=List[MarkRead],
)
def list_user_marks(
    user_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Mark]:
    db_marks = crud.marks.get_marks(page=page, user_id=user_id)

    return db_marks