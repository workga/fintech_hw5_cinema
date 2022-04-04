from fastapi import FastAPI
from app.cinema.routes import (
    marks,
    movies,
    reviews,
    users,
)

def include_to_app(app: FastAPI, *args: int, **kwargs: int) -> None:
    app.include_router(marks.router, *args, **kwargs)
    app.include_router(movies.router, *args, **kwargs)
    app.include_router(reviews.router, *args, **kwargs)
    app.include_router(users.router, *args, **kwargs)