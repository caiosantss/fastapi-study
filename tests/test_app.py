from http import HTTPStatus


def test_read_root_retorna_ok_e_ola_mundo(client):

    # Act
    response = client.get('/')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Hello World'}


def test_page_retorna_html(client):
    response = client.get('/hello-world/')

    assert response.status_code == HTTPStatus.OK
    assert '<p>PA!</p>' in response.text


def test_create_user(client):
    payload = {
        'username': 'caio',
        'email': 'caio@email.com',
        'password': '123',
    }

    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'caio',
        'email': 'caio@email.com',
        'id': 1,
    }
