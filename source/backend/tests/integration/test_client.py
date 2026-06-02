"""
Інтеграційні тести для API управління клієнтами.
"""
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_create_client_success(client: FlaskClient):
	"""Перевірка успішного створення клієнта через API."""
	response: TestResponse = client.post("/api/clients", json={"name": "ТОВ Тест"})
	assert response.status_code == 201
	
	data: Any = response.get_json()
	assert data["id"] == 1
	assert data["name"] == "ТОВ Тест"


def test_create_client_missing_name(client: FlaskClient):
	"""Перевірка помилки валідації, якщо не передано ім'я клієнта."""
	response: TestResponse = client.post("/api/clients", json={})
	
	assert response.status_code == 400
	assert "Поле 'name' є обов'язковим" in response.get_json()["error"]