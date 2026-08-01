import pytest
from fastapi.testclient import TestClient

from app.app import app


# Arrange
@pytest.fixture
def client():
    return TestClient(app=app)
