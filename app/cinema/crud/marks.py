from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.sql import func

from app.cinema.crud.movies import get_movie
from app.cinema.crud.users import get_user
from app.cinema.crud.utils import handle_db_exception
from app.cinema.models import Mark
from app.cinema.pagination import Page, paginated_stmt
from app.cinema.schemas.marks import MarkCreate
from app.database import create_session


@handle_db_exception
def get_marks(
    page: Page = Page(), user_id: Optional[int] = None, movie_id: Optional[int] = None
) -> List[Mark]:
    with create_session() as session:
        stmt = select(Mark)

        if user_id is not None:
            if not get_user(user_id):
                raise HTTPException(status_code=400, detail="User doesn't exist")

            stmt = stmt.where(Mark.user_id == user_id)

        if movie_id is not None:
            if not get_movie(movie_id):
                raise HTTPException(status_code=400, detail="Movie doesn't exist")

            stmt = stmt.where(Mark.movie_id == movie_id)

        stmt = paginated_stmt(stmt, page, Mark)
        db_movies = session.execute(stmt).all()

        return [r.Mark for r in db_movies]


@handle_db_exception
def create_mark(user_id: int, movie_id: int, mark: MarkCreate) -> Mark:
    with create_session() as session:
        db_movie = get_movie(movie_id)
        if not db_movie:
            raise HTTPException(status_code=400, detail="Movie doesn't exist")

        if not get_user(user_id):
            raise HTTPException(status_code=400, detail="User doesn't exist")

        db_mark = session.execute(
            select(Mark).where(Mark.user_id == user_id).where(Mark.movie_id == movie_id)
        ).all()

        if db_mark:
            raise HTTPException(status_code=400, detail='Mark already exists')

        db_mark = Mark(**mark.dict(), user_id=user_id, movie_id=movie_id)
        session.add(db_mark)
        db_movie.Movie.marks_count += 1

        avg_mark = (
            session.execute(
                select(func.avg(Mark.score).label('average')).where(
                    Mark.movie_id == movie_id
                )
            )
            .one()
            .average
        )

        db_movie.Movie.rating = avg_mark

        return db_mark
