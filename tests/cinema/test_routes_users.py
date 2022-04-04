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
def test_get_users_success(auth_client, limit, last_id):
    response = auth_client.get(
        '/cinema/users', params={'limit': limit, 'last_id': last_id}
    )

    data = response.json()

    length = limit if limit is not None else 3
    first_id = last_id + 1 if last_id is not None else 1

    assert response.status_code == 200
    assert len(data) == length
    if length:
        assert data[0]['id'] == first_id


@pytest.mark.parametrize(
    ('limit', 'last_id'),
    [
        (-1, 3),
        (2, -1),
    ],
)
def test_get_users_invalid_params(auth_client, limit, last_id):
    response = auth_client.get(
        '/cinema/users', params={'limit': limit, 'last_id': last_id}
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ('name', 'login', 'password'),
    [
        ('Flora', 'flora', 'flora'),
    ],
)
def test_post_users_success(auth_client, name, login, password):
    response = auth_client.post(
        '/cinema/users',
        json={
            'name': name,
            'login': login,
            'password': password,
        },
    )
    assert response.status_code == 201

    response = auth_client.get('/cinema/users', params={'limit': 1, 'last_id': 5})
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == 6


@pytest.mark.parametrize(
    ('name', 'login', 'password'),
    [
        ('', 'flora', 'flora'),
        (None, 'flora', 'flora'),
        ('Flora', '', 'flora'),
        ('Flora', None, 'flora'),
        ('Flora', 'flora', ''),
        ('Flora', 'flora', None),
    ],
)
def test_post_users_invalid_params(auth_client, name, login, password):
    response = auth_client.post(
        '/cinema/users',
        json={
            'name': name,
            'login': login,
            'password': password,
        },
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    ('name', 'login', 'password'),
    [
        ('Annet', 'annet', 'annet'),
    ],
)
def test_post_users_user_exists(auth_client, name, login, password):
    response = auth_client.post(
        '/cinema/users',
        json={
            'name': name,
            'login': login,
            'password': password,
        },
    )
    assert response.status_code == 400
