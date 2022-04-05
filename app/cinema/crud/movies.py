from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine.row import Row

from app.cinema.crud.utils import handle_db_exception
from app.cinema.models import Movie
from app.cinema.pagination import Page, paginated_stmt
from app.cinema.schemas.movies import MovieCreate
from app.database import create_session


def get_movie(movie_id: int) -> Row:
    with create_session() as session:
        db_movie = session.execute(
            select(Movie).where(Movie.id == movie_id)
        ).one_or_none()

        return db_movie


@handle_db_exception
def get_movies(
    page: Page = Page(),
    substring: Optional[str] = None,
    year: Optional[int] = None,
    top: Optional[int] = None,
) -> List[Movie]:
    with create_session() as session:
        stmt = select(Movie)
        if year is not None:
            stmt = stmt.where(Movie.year == year)
        if substring is not None:
            stmt = stmt.where(Movie.title.contains(substring))
        if top is not None:
            stmt = stmt.order_by(Movie.rating).limit(top)

        if top is None or top > page.limit:
            stmt = paginated_stmt(stmt, page, Movie)

        db_movies = session.execute(stmt).all()

        return [m.Movie for m in db_movies]


@handle_db_exception
def get_movie_stats(movie_id: int) -> Movie:
    db_movie = get_movie(movie_id)

    if db_movie is None:
        raise HTTPException(status_code=400, detail="Movie doesn't exist")

    return db_movie.Movie


@handle_db_exception
def create_movie(movie: MovieCreate) -> Movie:
    with create_session() as session:
        db_movie = session.execute(
            select(Movie)
            .where(Movie.title == movie.title)
            .where(Movie.year == movie.year)
        ).one_or_none()

        if db_movie:
            raise HTTPException(status_code=400, detail='Movie already exists')

        db_movie = Movie(**movie.dict())

        session.add(db_movie)

        return db_movie
