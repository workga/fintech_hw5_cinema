from typing import Type, TypeVar

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.sql.selectable import Select

from app.cinema.config import cinema_settings

T = TypeVar('T', bound=Type[BaseModel])


class Page(BaseModel):
    limit: int = cinema_settings.page_size
    last_id: int = 0


def pagination(
    limit: int = Query(cinema_settings.page_size, ge=0), last_id: int = Query(0, ge=0)
) -> Page:
    return Page(limit=limit, last_id=last_id)


def paginated_stmt(stmt: Select, page: Page, model_class: T) -> Page:
    if not hasattr(model_class, 'id'):
        return stmt
    return (
        stmt.where(getattr(model_class, 'id') > page.last_id)
        .order_by(getattr(model_class, 'id'))
        .limit(page.limit)
    )
