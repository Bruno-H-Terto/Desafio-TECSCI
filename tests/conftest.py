import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from config.database import get_session
from src.app import models
from src.app.main import app
from src.app.models import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def plants(session):
    session.bulk_save_objects(PlantFactory.create_batch(5))
    session.commit()


class PlantFactory(factory.Factory):
    class Meta:
        model = models.Plant

    plant_name = factory.Sequence(lambda n: f'US-{n + 1}')
