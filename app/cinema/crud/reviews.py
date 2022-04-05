from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select

from app.cinema.crud.movies import get_movie
from app.cinema.crud.users import get_user
from app.cinema.crud.utils import handle_db_exception
from app.cinema.models import Review
from app.cinema.pagination import Page, paginated_stmt
from app.cinema.schemas.reviews import ReviewCreate
from app.database import create_session


@handle_db_exception
def get_reviews(
    page: Page = Page(), user_id: Optional[int] = None, movie_id: Optional[int] = None
) -> List[Review]:
    with create_session() as session:
        stmt = select(Review)

        if user_id is not None:
            if not get_user(user_id):
                raise HTTPException(status_code=400, detail="User doesn't exist")

            stmt = stmt.where(Review.user_id == user_id)

        if movie_id is not None:
            if not get_movie(movie_id):
                raise HTTPException(status_code=400, detail="Movie doesn't exist")

            stmt = stmt.where(Review.movie_id == movie_id)

        stmt = paginated_stmt(stmt, page, Review)

        db_reviews = session.execute(stmt).all()

        return [r.Review for r in db_reviews]


@handle_db_exception
def create_review(user_id: int, movie_id: int, review: ReviewCreate) -> Review:
    with create_session() as session:
        db_movie = get_movie(movie_id)
        if not db_movie:
            raise HTTPException(status_code=400, detail="Movie doesn't exist")

        if not get_user(user_id):
            raise HTTPException(status_code=400, detail="User doesn't exist")

        db_review = session.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .where(Review.movie_id == movie_id)
        ).one_or_none()

        if db_review:
            raise HTTPException(status_code=400, detail='Review already exists')

        db_review = Review(**review.dict(), user_id=user_id, movie_id=movie_id)
        session.add(db_review)
        db_movie.Movie.reviews_count += 1

        return db_review
