from functools import wraps
from typing import Any, Callable, TypeVar, cast

from fastapi import HTTPException, status

from app.database import DatabaseError

F = TypeVar('F', bound=Callable[..., Any])


def handle_db_exception(crud_func: F) -> F:
    @wraps(crud_func)
    def wrapper(*args: int, **kwargs: int) -> Any:
        try:
            return crud_func(*args, **kwargs)
        except DatabaseError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from error

    return cast(F, wrapper)
