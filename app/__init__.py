from fastapi import FastAPI, Request

from app.database import init_db
from app.logger import init_logger

from app.cinema.routes import router as cinema_router


def create_app(testing=False) -> FastAPI:
    app = FastAPI()

    init_db(testing)
    init_logger()

    app.include_router(cinema_router, prefix='/cinema')

    return app