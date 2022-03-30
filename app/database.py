from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.config import DB_URL, DB_URL_TESTING
from app.logger import get_logger

DatabaseError = SQLAlchemyError

Base = declarative_base()
SessionLocal = sessionmaker()


def init_db(testing=False) -> None:
    url = DB_URL if not testing else DB_URL_TESTING
    engine = create_engine(url)
    SessionLocal.configure(bind=engine)

    # import model here in order to create them correctly
    from app.cinema.models import Mark, Movie, Review, User #noqa
    Base.metadata.create_all(bind=engine)


# def init_app(app: Flask) -> None:
#     app.cli.add_command(clear_db_command)


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


# def clear_db() -> None:
#     with create_session() as session:
#         for table in reversed(Base.metadata.sorted_tables):
#             session.execute(table.delete())
#     get_logger().info('Database cleared')


# @click.command('clear-db')
# @with_appcontext
# def clear_db_command() -> None:
#     '''
#     Clear database
#     '''
#     clear_db()
