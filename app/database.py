from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.config import DB_URL, DB_URL_TESTING
from app.logger import get_logger

DatabaseError = SQLAlchemyError

Base: DeclarativeMeta = declarative_base()
SessionLocal = sessionmaker()


def init_db(testing: bool = False) -> Engine:
    url = DB_URL if not testing else DB_URL_TESTING
    engine = create_engine(url)
    SessionLocal.configure(bind=engine)

    # Import it here in order to avoid circular imports and create all tables correctly
    from app.cinema.models import (  # noqa # pylint: disable=C0415 disable=W0611
        Mark,
        Movie,
        Review,
        User,
    )

    Base.metadata.create_all(bind=engine)
    return engine


@contextmanager
def create_session(**kwargs: int) -> Session:
    try:
        session = SessionLocal(**kwargs)
        yield session
        session.commit()
    except DatabaseError as error:
        get_logger().error(error)
        session.rollback()
        raise
    finally:
        session.close()
