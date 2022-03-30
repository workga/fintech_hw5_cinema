from typing import List
from fastapi import APIRouter, Depends, Body

from app.cinema.auth import auth_user
from app.cinema.models import (
    User
)
from app.cinema.schemas import (
    UserRead,
    UserCreate,
    MovieCreate,
    MovieRead,
    ReviewRead,
    ReviewCreate,
    MarkRead,
    MarkCreate,
)
from app.cinema import cinema


router = APIRouter()


# /users
@router.get("/users", dependencies=[Depends(auth_user)], response_model=List[UserRead])
def list_users():
    db_users = cinema.get_users()

    return db_users

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    db_user = cinema.create_user(user)

    return db_user


@router.get("/users/{user_id}/reviews", dependencies=[Depends(auth_user)], response_model=List[ReviewRead])
def list_user_reviews(user_id: int):
    db_reviews = cinema.get_reviews(user_id=user_id)

    return db_reviews

@router.get("/users/{user_id}/marks", dependencies=[Depends(auth_user)], response_model=List[MarkRead])
def list_user_marks(user_id: int):
    db_marks = cinema.get_marks(user_id=user_id)

    return db_marks


# /movies
@router.get("/movies", dependencies=[Depends(auth_user)], response_model=List[MovieRead])
def list_movies():
    db_movies = cinema.get_movies()

    return db_movies

# Replace it with admin panel later
@router.post("/movies", dependencies=[Depends(auth_user)], response_model=MovieRead)
def create_movie(movie: MovieCreate = Body(...)):
    db_movie = cinema.create_movie(movie)

    return db_movie


# /movies_reviews
@router.get("/movies/{movie_id}/reviews", dependencies=[Depends(auth_user)], response_model=List[ReviewRead])
def list_movie_reviews(movie_id: int):
    db_reviews = cinema.get_reviews(movie_id=movie_id)

    return db_reviews

@router.post("/movies/{movie_id}/reviews", response_model=ReviewRead)
def create_movie_review(movie_id: int, review: ReviewCreate = Body(...), user: User = Depends(auth_user)):
    db_review = cinema.create_review(user.id, movie_id, review)

    return db_review

# /movies_marks
@router.get("/movies/{movie_id}/marks", dependencies=[Depends(auth_user)], response_model=List[MarkRead])
def list_movie_marks(movie_id: int):
    db_marks = cinema.get_marks(movie_id=movie_id)

    return db_marks

@router.post("/movies/{movie_id}/marks", response_model=MarkRead)
def create_movie_mark(movie_id: int, mark: MarkCreate = Body(...), user: User = Depends(auth_user)):
    db_mark = cinema.create_mark(user.id, movie_id, mark)

    return db_mark