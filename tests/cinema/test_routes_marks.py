import pytest

from app.cinema import cinema
from tests.conftest import set_auth_user


# get /movies/{movie_id}/marks
@pytest.mark.parametrize(
    ('movie_id', 'count'),
    [
        (1, 1),
        (5, 1),
    ],
)
def test_get_movies_mark_success(auth_client, movie_id, count):
    response = auth_client.get(f'/cinema/movies/{movie_id}/marks')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == count


@pytest.mark.parametrize('movie_id', [-1, 0])
def test_get_movies_mark_invalid_params(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/marks')

    assert response.status_code == 422


@pytest.mark.parametrize(
    'movie_id',
    [
        6,
        7,
    ],
)
def test_get_movies_mark_movie_not_found(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/marks')

    assert response.status_code == 400


# post /movies/{movie_id}/marks
@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'score'),
    [
        (1, 2, 0),
        (2, 1, 5),
    ],
)
def test_post_movies_marks_success(app, client, user_id, movie_id, score):
    user = cinema.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/marks',
        json={
            'score': score,
        },
    )

    assert response.status_code == 201


@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'score'),
    [
        (1, -1, 'Veridis Quo'),
        (2, 0, 'Disco Very'),
        (3, 1, -1),
        (3, 1, 11),
        (3, 1, None),
    ],
)
def test_post_movies_marks_invalid_params(app, client, user_id, movie_id, score):
    user = cinema.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/marks',
        json={
            'score': score,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'score'),
    [
        (1, 6, 5),
        (1, 1, 5),
        (2, 2, 5),
    ],
)
def test_post_movies_marks_failed(app, client, user_id, movie_id, score):
    user = cinema.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/marks',
        json={
            'score': score,
        },
    )

    assert response.status_code == 400


# get /cinema/users/{user_id}/marks
@pytest.mark.parametrize(
    ('user_id', 'count'),
    [
        (1, 1),
        (5, 1),
    ],
)
def test_get_users_mark_success(auth_client, user_id, count):
    response = auth_client.get(f'/cinema/users/{user_id}/marks')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == count


@pytest.mark.parametrize('user_id', [-1, 0])
def test_get_users_mark_invalid_params(auth_client, user_id):
    response = auth_client.get(f'/cinema/users/{user_id}/marks')

    assert response.status_code == 422


@pytest.mark.parametrize(
    'user_id',
    [
        6,
        7,
    ],
)
def test_get_users_mark_movie_not_found(auth_client, user_id):
    response = auth_client.get(f'/cinema/users/{user_id}/marks')

    assert response.status_code == 400
