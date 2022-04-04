import pytest


@pytest.mark.parametrize(
    ('limit', 'last_id'),
    [
        (0, 0),
        (2, 2),
        (None, 2),
        (2, None),
        (None, None),
    ],
)
def test_get_movies_success(auth_client, limit, last_id):
    response = auth_client.get(
        '/cinema/movies', params={'limit': limit, 'last_id': last_id}
    )

    data = response.json()

    length = limit if limit is not None else 3
    first_id = last_id + 1 if last_id is not None else 1

    assert response.status_code == 200
    assert len(data) == length
    if length:
        assert data[0]['id'] == first_id


@pytest.mark.parametrize(
    ('substring', 'year', 'top', 'count'),
    [
        ('Mama', None, None, 1),
        (None, 2000, None, 1),
        (None, None, 3, 3),
    ],
)
def test_get_movies_filters(auth_client, substring, year, top, count):
    response = auth_client.get(
        '/cinema/movies',
        params={
            'substring': substring,
            'year': year,
            'top': top,
            'limit': 5,
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == count


@pytest.mark.parametrize(
    ('limit', 'last_id', 'substring', 'year', 'top'),
    [
        (-1, 1, 'Mama', 2000, 3),
        (3, -1, 'Mama', 2000, 3),
        (3, 1, '', 2000, 3),
        (3, 1, 'Mama', -1, 3),
        (3, 1, 'Mama', 2000, -1),
    ],
)
def test_get_movies_invalid_params(auth_client, limit, last_id, substring, year, top):
    response = auth_client.get(
        '/cinema/movies',
        params={
            'substring': substring,
            'year': year,
            'top': top,
            'limit': limit,
            'last_id': last_id,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(('title', 'year'), [('Real', 2005)])
def test_post_movies_success(auth_client, title, year):
    response = auth_client.post('/cinema/movies', json={'title': title, 'year': year})
    assert response.status_code == 201

    response = auth_client.get('/cinema/movies', params={'limit': 1, 'last_id': 5})
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == 6


@pytest.mark.parametrize(
    ('title', 'year'), [('', 2000), (None, 2000), ('Real', -1), ('Real', None)]
)
def test_post_movies_invalid_params(auth_client, title, year):
    response = auth_client.post('/cinema/movies', json={'title': title, 'year': year})
    assert response.status_code == 422


@pytest.mark.parametrize(
    ('title', 'year'),
    [
        ('Mama', 2000),
    ],
)
def test_post_movies_movie_exists(auth_client, title, year):
    response = auth_client.post('/cinema/movies', json={'title': title, 'year': year})
    assert response.status_code == 400
