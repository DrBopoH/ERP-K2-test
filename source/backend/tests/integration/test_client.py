"""
Інтеграційні тести для API управління клієнтами.
"""

# tests/integration/test_client.py
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_create_client_success(client: FlaskClient):
	"""Перевірка успішного створення клієнта через API."""
	response: TestResponse = client.post("/api/clients", json={
		"name": "ТОВ Тест"
	})
	assert response.status_code == 201
	
	data: Any = response.get_json()
	assert data["id"] == 1
	assert data["name"] == "ТОВ Тест"


def test_create_client_missing_name(client: FlaskClient):
	"""Перевірка помилки валідації, якщо не передано ім'я клієнта."""
	response: TestResponse = client.post("/api/clients", json={})
	
	assert response.status_code == 400
	assert "Поле 'name' є обов'язковим" in response.get_json()["error"]


def test_get_clients(client: FlaskClient):
	"""Перевірка отримання списку клієнтів."""
	client.post("/api/clients", json={
		"name": "Клієнт 1"
	})
	client.post("/api/clients", json={
		"name": "Клієнт 2"
	})
	
	response: TestResponse = client.get("/api/clients")
	
	assert response.status_code == 200
	assert len(response.get_json()) >= 2


def test_update_client_success(client: FlaskClient):
	"""Перевірка успішного оновлення клієнта."""
	client.post("/api/clients", json={
		"name": "Старе ім'я"
	})
	
	response: TestResponse = client.put("/api/clients/1", json={
		"name": "Нове ім'я"
	})
	
	assert response.status_code == 200
	assert response.get_json()["name"] == "Нове ім'я"


def test_update_client_not_found(client: FlaskClient):
	"""Перевірка оновлення неіснуючого клієнта."""
	response = client.put("/api/clients/999", json={
		"name": "Нове ім'я"
	})
	
	assert response.status_code == 404

def test_update_client_invalid_data(client: FlaskClient):
	"""Перевірка помилки 400 при оновленні клієнта без обов'язкових полів."""
	client.post("/api/clients", json={
		"name": "ТОВ Тест"
	})
	
	response: TestResponse = client.put("/api/clients/1", json={})
	
	assert response.status_code == 400
	assert "Поле 'name' є обов'язковим" not in response.get_json()["error"]


def test_delete_client_success(client: FlaskClient):
	"""Перевірка успішного видалення клієнта."""
	client.post("/api/clients", json={
		"name": "Для видалення"
	})
	
	response: TestResponse = client.delete("/api/clients/1")
	
	assert response.status_code == 200
	assert response.get_json()["success"] is True


def test_delete_client_not_found(client: FlaskClient):
	"""Перевірка видалення неіснуючого клієнта."""
	response: TestResponse = client.delete("/api/clients/999")
	
	assert response.status_code == 404