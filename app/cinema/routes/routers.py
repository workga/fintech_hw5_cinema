from fastapi import FastAPI

from app.cinema.routes import marks, movies, reviews, users


def include_to_app(app: FastAPI, prefix: str) -> None:
    app.include_router(marks.router, prefix=prefix)
    app.include_router(movies.router, prefix=prefix)
    app.include_router(reviews.router, prefix=prefix)
    app.include_router(users.router, prefix=prefix)
