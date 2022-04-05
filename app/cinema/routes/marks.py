from typing import List

from fastapi import APIRouter, Body, Depends, Path, status

from app.cinema.auth import auth_user
from app.cinema.crud import marks
from app.cinema.models import Mark, User
from app.cinema.pagination import Page, pagination
from app.cinema.schemas.marks import MarkCreate, MarkRead

router = APIRouter()


@router.get(
    '/movies/{movie_id}/marks',
    dependencies=[Depends(auth_user)],
    response_model=List[MarkRead],
)
def list_movie_marks(
    movie_id: int = Path(..., ge=1), page: Page = Depends(pagination)
) -> List[Mark]:
    db_marks = marks.get_marks(page=page, movie_id=movie_id)

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
    db_mark = marks.create_mark(user.id, movie_id, mark)

    return db_mark
