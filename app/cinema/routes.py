from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, status

from app.cinema import cinema
from app.cinema.auth import auth_user
from app.cinema.models import Mark, Movie, Review, User
from app.cinema.pagination import Page, pagination
from app.cinema.schemas import (  # MovieFilter,
    MarkCreate,
    MarkRead,
    MovieCreate,
    MovieRead,
    MovieStats,
    ReviewCreate,
    ReviewRead,
    UserCreate,
    UserRead,
)

router = APIRouter()


# /users
@router.get('/users', dependencies=[Depends(auth_user)], response_model=List[UserRead])
def list_users(page: Page = Depends(pagination)) -> List[User]:
    db_users = cinema.get_users(page=page)

    return db_users


@router.post('/users', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> User:
    db_user = cinema.create_user(user)

    return db_user


@router.get(
    '/users/{user_id}/reviews',
    dependencies=[Depends(auth_user)],
    response_model=List[ReviewRead],
)
def list_user_reviews(
    user_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Review]:
    db_reviews = cinema.get_reviews(
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
    db_marks = cinema.get_marks(page=page, user_id=user_id)

    return db_marks


# /movies
@router.get(
    '/movies', dependencies=[Depends(auth_user)], response_model=List[MovieRead]
)
def list_movies(
    substring: Optional[str] = Query(None, min_length=1),
    year: Optional[int] = Query(None, ge=0),
    top: Optional[int] = Query(None, ge=0),
    page: Page = Depends(pagination),
) -> List[Movie]:
    db_movies = cinema.get_movies(page=page, substring=substring, year=year, top=top)

    return db_movies


@router.get(
    '/movies/{movie_id}/stats',
    dependencies=[Depends(auth_user)],
    response_model=MovieStats,
)
def show_movie_stats(movie_id: int = Path(..., ge=1)) -> Movie:
    movie = cinema.get_movie_stats(movie_id=movie_id)

    return movie


@router.post(
    '/movies',
    dependencies=[Depends(auth_user)],
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie: MovieCreate = Body(...)) -> Movie:
    db_movie = cinema.create_movie(movie)

    return db_movie


# /movies_reviews
@router.get(
    '/movies/{movie_id}/reviews',
    dependencies=[Depends(auth_user)],
    response_model=List[ReviewRead],
)
def list_movie_reviews(
    movie_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Review]:
    db_reviews = cinema.get_reviews(page=page, movie_id=movie_id)

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
    db_review = cinema.create_review(user.id, movie_id, review)

    return db_review


# /movies_marks
@router.get(
    '/movies/{movie_id}/marks',
    dependencies=[Depends(auth_user)],
    response_model=List[MarkRead],
)
def list_movie_marks(
    movie_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Mark]:
    db_marks = cinema.get_marks(page=page, movie_id=movie_id)

    return db_marks


@router.post(
    '/movies/{movie_id}/marks',
    response_model=MarkRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie_mark(
    movie_id: int = Path(..., ge=1),
    mark: MarkCreate = Body(...),
    user: User = Depends(auth_user),
) -> Mark:
    db_mark = cinema.create_mark(user.id, movie_id, mark)

    return db_mark
