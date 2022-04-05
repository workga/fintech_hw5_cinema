from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.config import app_settings
from app.logger import get_logger

DatabaseError = SQLAlchemyError

Base: DeclarativeMeta = declarative_base()
SessionLocal = sessionmaker(expire_on_commit=False)


def init_db(testing: bool = False) -> Engine:
    url = app_settings.db_url if not testing else app_settings.db_url_testing
    engine = create_engine(url)
    SessionLocal.configure(bind=engine)

    return engine


@contextmanager
def create_session() -> Session:
    # BEcause pylint doesn't know about begin() method
    with SessionLocal.begin() as session:  # pylint: disable=E1101
        yield session


def recreate_db(testing: bool = False) -> None:
    engine = init_db(testing)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if not testing:
        get_logger().info('Database recreated')
