from fastapi import FastAPI

from app.cinema.routes import router as cinema_router
from app.database import init_db
from app.logger import init_logger


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI()

    init_db(testing)
    init_logger()

    app.include_router(cinema_router, prefix='/cinema')

    return app
