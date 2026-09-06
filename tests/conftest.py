from contextlib import contextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.app import app
from app.models import table_registry

fuso_br = ZoneInfo('America/Sao_Paulo')


# Arrange
@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
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
