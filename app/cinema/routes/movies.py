from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, status

from app.cinema.auth import auth_user
from app.cinema.crud import movies
from app.cinema.models import Movie
from app.cinema.pagination import Page, pagination
from app.cinema.schemas.movies import MovieCreate, MovieRead, MovieStats

router = APIRouter()


@router.get(
    '/movies', dependencies=[Depends(auth_user)], response_model=List[MovieRead]
)
def list_movies(
    substring: Optional[str] = Query(None, min_length=1),
    year: Optional[int] = Query(None, ge=0),
    top: Optional[int] = Query(None, ge=0),
    page: Page = Depends(pagination),
) -> List[Movie]:
    db_movies = movies.get_movies(page=page, substring=substring, year=year, top=top)

    return db_movies


@router.get(
    '/movies/{movie_id}/stats',
    dependencies=[Depends(auth_user)],
    response_model=MovieStats,
)
def show_movie_stats(movie_id: int = Path(..., ge=1)) -> Movie:
    movie = movies.get_movie_stats(movie_id=movie_id)

    return movie


@router.post(
    '/movies',
    dependencies=[Depends(auth_user)],
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie: MovieCreate = Body(...)) -> Movie:
    db_movie = movies.create_movie(movie)

    return db_movie
