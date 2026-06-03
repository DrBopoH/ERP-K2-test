"""
Інтеграційні тести для API управління каталогом товарів.
"""

# tests/integration/test_product.py
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_create_product_success(client: FlaskClient):
	"""Перевірка успішного створення товару."""
	response: TestResponse = client.post("/api/products", json={
		"name": "Кава", 
		"price": 120.5
	})
	assert response.status_code == 201
	
	data: Any = response.get_json()
	assert data["id"] == 1
	assert data["price"] == 120.5


def test_create_product_invalid_price(client: FlaskClient):
	"""Перевірка помилки, якщо ціна передана некоректним типом даних."""
	response: TestResponse = client.post("/api/products", json={
		"name": "Чай", 
		"price": "безкоштовно"
	})
	
	assert response.status_code == 400
	assert "Ціна має бути числом" in response.get_json()["error"]


def test_create_product_missing_fields(client: FlaskClient):
	"""Перевірка помилки при відсутності обов'язкових атрибутів товару."""
	response: TestResponse = client.post("/api/products", json={
		"name": "Шоколад"
	})
	
	assert response.status_code == 400


def test_get_products(client: FlaskClient):
	"""Перевірка отримання списку товарів."""
	client.post("/api/products", json={
		"name": "Товар 1", 
		"price": 100.0
	})
	
	response: TestResponse = client.get("/api/products")
	
	assert response.status_code == 200
	assert len(response.get_json()) >= 1


def test_update_product_success(client: FlaskClient):
	"""Перевірка успішного оновлення назви та ціни товару."""
	client.post("/api/products", json={
		"name": "Старий товар", 
		"price": 100.0
	})
	
	response: TestResponse = client.put("/api/products/1", json={
		"name": "   Нова назва товару   ", 
		"price": 150.0
	})
	
	assert response.status_code == 200
	
	data: Any = response.get_json()
	assert data["price"] == 150.0
	assert data["name"] == "Нова назва товару"


def test_update_product_not_found(client: FlaskClient):
	"""Перевірка оновлення неіснуючого товару."""
	response = client.put("/api/products/999", json={
		"price": 200.0
	})
	
	assert response.status_code == 404


def test_update_product_invalid_price(client: FlaskClient):
	"""Перевірка помилки 400 при оновленні товару з некоректним типом ціни."""
	client.post("/api/products", json={
		"name": "Монітор", 
		"price": 5000.0
	})
	
	response: TestResponse = client.put("/api/products/1", json={
		"price": "дуже дорого"
	})
	
	assert response.status_code == 400
	assert "Ціна має бути числом" in response.get_json()["error"]


def test_delete_product_success(client: FlaskClient):
	"""Перевірка успішного видалення товару."""
	client.post("/api/products", json={
		"name": "Стілець", 
		"price": 500.0
	})
	
	response: TestResponse = client.delete("/api/products/1")
	
	assert response.status_code == 200
	assert response.get_json()["success"] is True


def test_delete_product_not_found(client: FlaskClient):
	"""Перевірка видалення неіснуючого товару."""
	response: TestResponse = client.delete("/api/products/999")
	
	assert response.status_code == 404