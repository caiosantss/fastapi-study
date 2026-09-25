from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from app.app import app
from app.database import get_session
from app.models import table_registry


# Arrange
@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    # FastApi, at this client context, change the session dependency that I used in the app.py with Depends(get_session) to the test session here
    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client

    # Undo
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@contextmanager
def _mock_db_time(
    *,
    model,
    time=datetime(2026, 1, 1),  # noqa: DTZ001
):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at') and hasattr(target, 'updated_at'):
            target.created_at = time
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)
