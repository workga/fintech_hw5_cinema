from functools import wraps
from typing import Any, List, Callable, Optional

from fastapi import HTTPException, status

from select import select
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.cinema.schemas import UserCreate, MovieCreate, ReviewCreate, MarkCreate
from sqlalchemy.exc import IntegrityError

from app.database import DatabaseError, create_session
from app.cinema.models import User, Movie, Review, Mark
from app.cinema.security import hash_password

# from app.cinema.models import serialized


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
        result = session.execute(
            select(User)
            .where(User.login == login)
        ).one_or_none()
        
        return result.User if result else None


@handle_db_exception
def get_users() -> List[User]:
    with create_session(expire_on_commit=False) as session:
        result = session.execute(
            select(User)
        ).all()

        return [u.User for u in result]

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
def get_movies() -> List[Movie]:
    with create_session(expire_on_commit=False) as session:
        result = session.execute(
            select(Movie)
        ).all()

        return [m.Movie for m in result]

@handle_db_exception
def create_movie(movie: MovieCreate) -> Movie:
    with create_session(expire_on_commit=False) as session:
        result = session.execute(
            select(Movie)
            .where(Movie.title == movie.title)
            .where(Movie.year == movie.year)
        ).one_or_none()

        if result:
            raise HTTPException(status_code=400, detail="Movie already exists")

        db_movie = Movie(**movie.dict())

        session.add(db_movie)
            
        return db_movie


# Reviews
@handle_db_exception
def get_reviews(user_id: Optional[int] = None, movie_id: Optional[int] = None) -> List[Review]:
    with create_session(expire_on_commit=False) as session:
        stmt = select(Review)
        if user_id is not None:
            stmt = stmt.where(Review.user_id == user_id)
        if movie_id is not None:
            stmt = stmt.where(Review.movie_id == movie_id)
        
        result = session.execute(stmt).all()

        return [r.Review for r in result]

@handle_db_exception
def create_review(user_id: int, movie_id: int, review: ReviewCreate) -> Review:
    with create_session(expire_on_commit=False) as session:
        result = session.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .where(Review.movie_id == movie_id)
        ).all()

        if result:
            raise HTTPException(status_code=400, detail="Review already exists")

        db_review = Review(**review.dict(), user_id=user_id, movie_id=movie_id)

        session.add(db_review)

        return db_review


# Marks
@handle_db_exception
def get_marks(user_id: Optional[int] = None, movie_id: Optional[int] = None) -> List[Mark]:
    with create_session(expire_on_commit=False) as session:
        stmt = select(Mark)
        if user_id is not None:
            stmt = stmt.where(Mark.user_id == user_id)
        if movie_id is not None:
            stmt = stmt.where(Mark.movie_id == movie_id)
        
        result = session.execute(stmt).all()

        return [r.Mark for r in result]

@handle_db_exception
def create_mark(user_id: int, movie_id: int, mark: MarkCreate) -> Mark:
    with create_session(expire_on_commit=False) as session:
        result = session.execute(
            select(Mark)
            .where(Mark.user_id == user_id)
            .where(Mark.movie_id == movie_id)
        ).all()

        if result:
            raise HTTPException(status_code=400, detail="Mark already exists")

        db_mark = Mark(**mark.dict(), user_id=user_id, movie_id=movie_id)

        session.add(db_mark)

        return db_mark
