import pytest
from fastapi.testclient import TestClient

from app.app import create_app
from app.cinema import crud
from app.cinema.auth import auth_user
from app.cinema.models import User
from app.cinema.schemas.marks import MarkCreate
from app.cinema.schemas.movies import MovieCreate
from app.cinema.schemas.reviews import ReviewCreate
from app.cinema.schemas.users import UserCreate
from app.database import DatabaseError, recreate_db


@pytest.fixture(autouse=True, name='app')
def fixture_app():
    return create_app(testing=True)


def mocked_auth_user() -> User:
    user = User('annet', 'Annet', 'annet')
    user.id = 1
    return user


def set_auth_user(app, user):
    def auth_func():
        return user

    app.dependency_overrides[auth_user] = auth_func


@pytest.fixture(name='client')
def fixture_client(app):
    return TestClient(app)


@pytest.fixture
def auth_client(app, client):
    app.dependency_overrides[auth_user] = mocked_auth_user
    yield client
    app.dependency_overrides = {}


def mock_db_exception(mocker):
    mocker.patch('sqlalchemy.orm.Session', side_effect=DatabaseError)


@pytest.fixture(autouse=True)
def fill_db():
    recreate_db(testing=True)

    crud.users.create_user(UserCreate(login='annet', name='Annet', password='annet'))
    crud.users.create_user(UserCreate(login='bella', name='Bella', password='bella'))
    crud.users.create_user(UserCreate(login='clare', name='Clare', password='clare'))
    crud.users.create_user(UserCreate(login='diana', name='Diana', password='diana'))
    crud.users.create_user(UserCreate(login='elena', name='Elena', password='elena'))

    crud.movies.create_movie(MovieCreate(title='Mama', year=2000))
    crud.movies.create_movie(MovieCreate(title='Nana', year=2001))
    crud.movies.create_movie(MovieCreate(title='Obob', year=2003))
    crud.movies.create_movie(MovieCreate(title='Papa', year=2004))
    crud.movies.create_movie(MovieCreate(title='Ququ', year=2005))

    crud.reviews.create_review(1, 1, ReviewCreate(text='Amazing!'))
    crud.reviews.create_review(2, 2, ReviewCreate(text='Boring!'))
    crud.reviews.create_review(3, 3, ReviewCreate(text='Cool!'))
    crud.reviews.create_review(4, 4, ReviewCreate(text='Deep!'))
    crud.reviews.create_review(5, 5, ReviewCreate(text='Excellent'))

    crud.marks.create_mark(1, 1, MarkCreate(score=0))
    crud.marks.create_mark(2, 2, MarkCreate(score=1))
    crud.marks.create_mark(3, 3, MarkCreate(score=5))
    crud.marks.create_mark(4, 4, MarkCreate(score=9))
    crud.marks.create_mark(5, 5, MarkCreate(score=10))
