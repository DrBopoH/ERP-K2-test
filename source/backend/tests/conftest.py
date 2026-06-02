from flask.testing import FlaskClient
import pytest
from flask import Flask

from app.main import create_app
from app.models import db


@pytest.fixture
def app():
    _app: Flask = create_app()
    _app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()