from functools import wraps
from typing import Any, Callable, TypeVar, cast

from fastapi import HTTPException, status
from app.database import DatabaseError

F = TypeVar('F', bound=Callable[..., Any])

def handle_db_exception(cinema_func: F) -> F:
    @wraps(cinema_func)
    def wrapper(*args: int, **kwargs: int) -> Any:
        try:
            return cinema_func(*args, **kwargs)
        except DatabaseError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from error

    return cast(F, wrapper)