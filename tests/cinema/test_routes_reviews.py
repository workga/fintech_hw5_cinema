import pytest

from app.cinema import crud
from tests.conftest import set_auth_user


@pytest.mark.parametrize(
    ('movie_id', 'count'),
    [
        (1, 1),
        (5, 1),
    ],
)
def test_get_movies_review_success(auth_client, movie_id, count):
    response = auth_client.get(f'/cinema/movies/{movie_id}/reviews')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == count


@pytest.mark.parametrize('movie_id', [-1, 0])
def test_get_movies_review_invalid_params(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/reviews')

    assert response.status_code == 422


@pytest.mark.parametrize(
    'movie_id',
    [
        6,
        7,
    ],
)
def test_get_movies_review_movie_not_found(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/reviews')

    assert response.status_code == 400


@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'text'),
    [
        (1, 2, 'Veridis Quo'),
        (2, 1, 'Disco Very'),
    ],
)
def test_post_movies_reviews_success(app, client, user_id, movie_id, text):
    user = crud.users.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/reviews',
        json={
            'text': text,
        },
    )

    assert response.status_code == 201


@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'text'),
    [
        (1, -1, 'Veridis Quo'),
        (2, 0, 'Disco Very'),
        (3, 1, ''),
        (3, 1, None),
    ],
)
def test_post_movies_reviews_invalid_params(app, client, user_id, movie_id, text):
    user = crud.users.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/reviews',
        json={
            'text': text,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ('user_id', 'movie_id', 'text'),
    [
        (1, 6, 'Veridis Quo'),
        (1, 1, 'Veridis Quo'),
        (2, 2, 'Veridis Quo'),
    ],
)
def test_post_movies_reviews_failed(app, client, user_id, movie_id, text):
    user = crud.users.get_user_by_id(user_id)
    set_auth_user(app, user)

    response = client.post(
        f'/cinema/movies/{movie_id}/reviews',
        json={
            'text': text,
        },
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    ('user_id', 'count'),
    [
        (1, 1),
        (5, 1),
    ],
)
def test_get_users_review_success(auth_client, user_id, count):
    response = auth_client.get(f'/cinema/users/{user_id}/reviews')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == count


@pytest.mark.parametrize('user_id', [-1, 0])
def test_get_users_review_invalid_params(auth_client, user_id):
    response = auth_client.get(f'/cinema/users/{user_id}/reviews')

    assert response.status_code == 422


@pytest.mark.parametrize(
    'user_id',
    [
        6,
        7,
    ],
)
def test_get_users_review_movie_not_found(auth_client, user_id):
    response = auth_client.get(f'/cinema/users/{user_id}/reviews')

    assert response.status_code == 400


@pytest.mark.parametrize('movie_id', [1, 5])
def test_get_movies_stats_success(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/stats')
    assert response.status_code == 200


@pytest.mark.parametrize('movie_id', [-1, 0])
def test_get_movies_stats_invalid_params(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/stats')
    assert response.status_code == 422


@pytest.mark.parametrize('movie_id', [6, 7])
def test_get_movies_stats_movie_not_found(auth_client, movie_id):
    response = auth_client.get(f'/cinema/movies/{movie_id}/stats')
    assert response.status_code == 400
