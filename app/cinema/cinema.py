from functools import wraps
from re import sub
from typing import Any, List, Callable, Optional

from fastapi import HTTPException, status

from select import select
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.cinema.pagination import Page, paginated_stmt
from app.cinema.schemas import UserCreate, MovieCreate, ReviewCreate, MarkCreate
from sqlalchemy.sql import func

from app.database import DatabaseError, create_session
from app.cinema.models import User, Movie, Review, Mark
from app.cinema.security import hash_password


def handle_db_exception(func) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except DatabaseError as error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from error
    return wrapper


# Users
@handle_db_exception
def get_user_by_login(login: str) -> Optional[User]:
    with create_session(expire_on_commit=False) as session:
        db_user = session.execute(
            select(User)
            .where(User.login == login)
        ).one_or_none()
        
        return db_user.User if db_user else None


@handle_db_exception
def get_users(page: Page) -> List[User]:
    with create_session(expire_on_commit=False) as session:
        db_users = session.execute(
            paginated_stmt(select(User), page, User)
        ).all()

        return [u.User for u in db_users]

@handle_db_exception
def create_user(user: UserCreate) -> User:
    with create_session(expire_on_commit=False) as session:
        if get_user_by_login(user.login):
            raise HTTPException(status_code=400, detail="Login already registered")

        user.password = hash_password(user.password)
        db_user = User(**user.dict())

        session.add(db_user)
            
        return db_user

# Movies
@handle_db_exception
def get_movies(
    page: Page,
    substring: Optional[str] = None,
    year: Optional[int] = None,
    top: Optional[int] = None,
) -> List[Movie]:
    with create_session(expire_on_commit=False) as session:
        stmt = select(Movie)
        if year is not None:
            stmt = stmt.where(Movie.year == year)
        if substring is not None:
            stmt = stmt.where(Movie.title.contains(substring))
        if top is not None:
            stmt = stmt.order_by(Movie.rating).limit(top)

        stmt = paginated_stmt(stmt, page, Movie)

        db_movies = session.execute(stmt).all()

        return [m.Movie for m in db_movies]

@handle_db_exception
def get_movie_stats(movie_id: int):
    with create_session(expire_on_commit=False) as session:
        db_movie = session.execute(
            select(Movie)
            .where(Movie.id == movie_id)
        ).one_or_none()

        if db_movie is None:
            raise HTTPException(status_code=400, detail="Movie doesn't exist")
        
        return db_movie.Movie


@handle_db_exception
def create_movie(movie: MovieCreate) -> Movie:
    with create_session(expire_on_commit=False) as session:
        db_movie = session.execute(
            select(Movie)
            .where(Movie.title == movie.title)
            .where(Movie.year == movie.year)
        ).one_or_none()

        if db_movie:
            raise HTTPException(status_code=400, detail="Movie already exists")

        db_movie = Movie(**movie.dict())

        session.add(db_movie)
            
        return db_movie


# Reviews
@handle_db_exception
def get_reviews(page: Page, user_id: Optional[int] = None, movie_id: Optional[int] = None) -> List[Review]:
    with create_session(expire_on_commit=False) as session:
        stmt = select(Review)
        if user_id is not None:
            stmt = stmt.where(Review.user_id == user_id)
        if movie_id is not None:
            stmt = stmt.where(Review.movie_id == movie_id)
        
        stmt = paginated_stmt(stmt, page, Review) 

        db_reviews = session.execute(stmt).all()

        return [r.Review for r in db_reviews]

@handle_db_exception
def create_review(user_id: int, movie_id: int, review: ReviewCreate) -> Review:
    with create_session(expire_on_commit=False) as session:
        db_movie = session.execute(
            select(Movie)
            .where(Movie.id == movie_id)
        ).one_or_none()

        if not db_movie:
            raise HTTPException(status_code=400, detail="Movie doesn't exist")

        db_user = session.execute(
            select(User)
            .where(User.id == user_id)
        ).one_or_none()

        if not db_user:
            raise HTTPException(status_code=400, detail="User doesn't exist")


        db_review = session.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .where(Review.movie_id == movie_id)
        ).one_or_none()

        if db_review:
            raise HTTPException(status_code=400, detail="Review already exists")

        db_review = Review(**review.dict(), user_id=user_id, movie_id=movie_id)
        session.add(db_review)
        db_movie.Movie.reviews_count += 1

        return db_review


# Marks
@handle_db_exception
def get_marks(page: Page, user_id: Optional[int] = None, movie_id: Optional[int] = None) -> List[Mark]:
    with create_session(expire_on_commit=False) as session:
        stmt = select(Mark)
        if user_id is not None:
            stmt = stmt.where(Mark.user_id == user_id)
        if movie_id is not None:
            stmt = stmt.where(Mark.movie_id == movie_id)
        
        stmt = paginated_stmt(stmt, page, Mark)
        db_movies = session.execute(stmt).all()

        return [r.Mark for r in db_movies]

@handle_db_exception
def create_mark(user_id: int, movie_id: int, mark: MarkCreate) -> Mark:
    with create_session(expire_on_commit=False) as session:
        db_movie = session.execute(
            select(Movie)
            .where(Movie.id == movie_id)
        ).one_or_none()

        if not db_movie:
            raise HTTPException(status_code=400, detail="Movie doesn't exist")

        db_user = session.execute(
            select(User)
            .where(User.id == user_id)
        ).one_or_none()

        if not db_user:
            raise HTTPException(status_code=400, detail="User doesn't exist")

        db_mark = session.execute(
            select(Mark)
            .where(Mark.user_id == user_id)
            .where(Mark.movie_id == movie_id)
        ).all()

        if db_mark:
            raise HTTPException(status_code=400, detail="Mark already exists")

        db_mark = Mark(**mark.dict(), user_id=user_id, movie_id=movie_id)
        session.add(db_mark)
        db_movie.Movie.marks_count += 1

        avg_mark = session.execute(
            select(func.avg(Mark.score).label('average'))
            .where(Mark.movie_id == movie_id)
        ).one().average

        db_movie.Movie.rating = avg_mark

        return db_mark