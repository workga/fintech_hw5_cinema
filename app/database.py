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

    return engine


@contextmanager
def create_session(**kwargs: int) -> Session:
    session = None
    try:
        session = SessionLocal(**kwargs)
        yield session
        session.commit()
    except DatabaseError as error:
        get_logger().error(error)
        if session is not None:
            session.rollback()
        raise
    finally:
        if session is not None:
            session.close()


def recreate_db(testing: bool = False) -> None:
    engine = init_db(testing)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if not testing:
        get_logger().info('Database recreated')
