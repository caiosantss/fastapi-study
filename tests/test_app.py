from http import HTTPStatus

from fastapi.testclient import TestClient

from app.schemas import UserPublic


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


def test_create_user_conflict(client, user):
    payload = {
        'username': f'{user.username}',
        'email': f'{user.email}',
        'password': 'secret',
    }
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(obj=user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_id(client, user):
    user_schema = UserPublic.model_validate(obj=user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_id_not_found(client):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user):

    response = client.put(
        f'/users/{user.id}',
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


def test_update_user_conflict(client, user):
    client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@email.com',
            'password': 'newsecret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'alice@email.com',
            'password': 'newsecret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


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


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_token(client: TestClient, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token.keys()
    assert token['token_type'] == 'Bearer'
