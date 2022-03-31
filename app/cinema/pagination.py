from typing import Optional, TypeVar

from pydantic import BaseModel, validator

from fastapi import Query, Depends

from app.cinema.config import PAGE_SIZE


class Page(BaseModel):
    limit: int
    last_id: int

def pagination(limit: int = Query(PAGE_SIZE, ge=0), last_id: int = Query(0, ge=0)) -> Page:
    return Page(limit=limit, last_id=last_id)


M = TypeVar('M')
def paginated_stmt(stmt, page, M) -> Page:
    return (
        stmt.where(M.id > page.last_id)
        .order_by(M.id)
        .limit(page.limit)
    )