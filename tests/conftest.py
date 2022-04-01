import json
from typing import Any, Dict, List

import pytest
from fastapi.testclient import TestClient

from app import create_app
from app.cinema import cinema
from app.cinema.auth import auth_user
from app.cinema.models import User
from app.cinema.schemas import MarkCreate, MovieCreate, ReviewCreate, UserCreate
from app.database import DatabaseError, recreate_db


@pytest.fixture(autouse=True, name='app')
def fixture_app():
    return create_app(testing=True)


def set_auth_user(app, user):
    def auth_func():
        return user

    app.dependency_overrides[auth_user] = auth_func


def mocked_auth_user() -> User:
    user = User('annet', 'Annet', 'annet')
    user.id = 1
    return user


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
    # mocker.patch('sqlalchemy.orm.Session.add', side_effect=DatabaseError)
    # mocker.patch('sqlalchemy.orm.Query.all', side_effect=DatabaseError)
    # mocker.patch('sqlalchemy.orm.Query.one', side_effect=DatabaseError)
    # mocker.patch('sqlalchemy.orm.Query.first', side_effect=DatabaseError)
    # mocker.patch('sqlalchemy.orm.Query.one_or_none', side_effect=DatabaseError)


@pytest.fixture(scope='session', autouse=True, name='data')
def fixture_data():
    with open('tests/cinema/data_testing.json', 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    data_models = models_from_json(data_json)

    return data_models


@pytest.fixture(autouse=True)
def db(data):
    recreate_db(testing=True)
    fill_db(data)
    yield
    recreate_db(testing=True)


def fill_db(data):
    for u in data['users']:
        cinema.create_user(u)
    for m in data['movies']:
        cinema.create_movie(m)
    for r in data['reviews']:
        cinema.create_review(*r)
    for m in data['marks']:
        cinema.create_mark(*m)


def models_from_json(data_json):
    data_models: Dict[str, List[Any]] = {
        'users': [],
        'movies': [],
        'reviews': [],
        'marks': [],
    }
    for u in data_json['users']:
        data_models['users'].append(UserCreate.parse_obj(u))
    for m in data_json['movies']:
        data_models['movies'].append(MovieCreate.parse_obj(m))
    for r in data_json['reviews']:
        data_models['reviews'].append(
            (r['user_id'], r['movie_id'], ReviewCreate.parse_obj(r))
        )
    for m in data_json['marks']:
        data_models['marks'].append(
            (m['user_id'], m['movie_id'], MarkCreate.parse_obj(m))
        )
    return data_models
