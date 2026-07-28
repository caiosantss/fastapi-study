from http import HTTPStatus

from fastapi.testclient import TestClient

from app.app import app


def test_read_root_retorna_ok_e_ola_mundo():
    # Arrange
    client = TestClient(app=app)
    # Act
    response = client.get('/')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
