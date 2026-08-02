from http import HTTPStatus


def test_create_user(client):
    payload = {
        'username': 'caio',
        'email': 'caio@email.com',
        'password': 'secret',
    }

    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'caio',
        'email': 'caio@email.com',
        'id': 1,
    }


def test_get_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'caio',
                'email': 'caio@email.com',
                'id': 1,
            }
        ]
    }


def test_get_user_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
                'username': 'caio',
                'email': 'caio@email.com',
                'id': 1
                }


def test_get_user_id_not_found(client):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@email.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/10',
        json={
            'username': 'everton',
            'email': 'everton@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@email.com',
        'id': 1,
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
