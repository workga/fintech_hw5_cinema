from fastapi import FastAPI

from app.cinema.routes import routers as cinema_routers
from app.database import init_db
from app.logger import init_logger


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI()

    init_db(testing)
    init_logger()

    cinema_routers.include_to_app(app, prefix='/cinema')

    return app
