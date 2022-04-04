from typing import List

from fastapi import Body, Depends, Path, status, APIRouter

from app.cinema import crud
from app.cinema.auth import auth_user
from app.cinema.models import Review, User
from app.cinema.pagination import Page, pagination
from app.cinema.schemas import (
    ReviewCreate,
    ReviewRead,
)

router = APIRouter()


@router.get(
    '/movies/{movie_id}/reviews',
    dependencies=[Depends(auth_user)],
    response_model=List[ReviewRead],
)
def list_movie_reviews(
    movie_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Review]:
    db_reviews = crud.reviews.get_reviews(page=page, movie_id=movie_id)

    return db_reviews


@router.post(
    '/movies/{movie_id}/reviews',
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie_review(
    movie_id: int = Path(..., ge=1),
    review: ReviewCreate = Body(...),
    user: User = Depends(auth_user),
) -> Review:
    db_review = crud.reviews.create_review(user.id, movie_id, review)

    return db_review
