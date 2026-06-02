"""
Конфігурація тестування для pytest.
Визначає фікстури для створення ізольованого тестового клієнта Flask 
та бази даних в оперативній пам'яті (:memory:).
"""
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.main import create_app
from app.models import db


@pytest.fixture
def app() -> Generator[Flask, Any, None]:
	"""
	Ініціалізує екземпляр Flask-додатку в режимі тестування.
	Перемикає базу даних на SQLite в оперативній пам'яті.
	"""
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
	"""
    Створює тестовий HTTP-клієнт для відправки запитів до API.
    """
	return app.test_client()