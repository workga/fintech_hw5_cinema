from fastapi import FastAPI

from app.database import init_db
from app.logger import init_logger
from app.cinema.routes import routers as cinema_routers


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI()

    init_db(testing)
    init_logger()

    cinema_routers.include_to_app(app, prefix='/cinema')

    return app