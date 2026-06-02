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
	test_config = {
		"TESTING": True,
		"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
	}
	_app = create_app(test_config)

	with _app.app_context():
		yield _app
		
		db.session.remove()
		db.drop_all()
		db.engine.dispose()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
	"""
	Створює тестовий HTTP-клієнт для відправки запитів до API.
	"""
	return app.test_client()