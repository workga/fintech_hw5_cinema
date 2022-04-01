from typing import Type, TypeVar

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.sql.selectable import Select

from app.cinema.config import PAGE_SIZE
from app.cinema.schemas import CinemaBaseModel

T = TypeVar('T', bound=Type[CinemaBaseModel])


class Page(BaseModel):
    limit: int = PAGE_SIZE
    last_id: int = 0


def pagination(
    limit: int = Query(PAGE_SIZE, ge=0), last_id: int = Query(0, ge=0)
) -> Page:
    return Page(limit=limit, last_id=last_id)


def paginated_stmt(stmt: Select, page: Page, ModelClass: T) -> Page:
    if not hasattr(ModelClass, 'id'):
        return stmt
    return (
        stmt.where(getattr(ModelClass, 'id') > page.last_id)
        .order_by(getattr(ModelClass, 'id'))
        .limit(page.limit)
    )
