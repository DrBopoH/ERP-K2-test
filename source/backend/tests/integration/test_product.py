from flask.testing import FlaskClient


def test_create_product_success(client: FlaskClient):
	response = client.post("/api/products", json={"name": "Кава", "price": 120.5})
	assert response.status_code == 201
	data = response.get_json()
	assert data["id"] == 1
	assert data["price"] == 120.5


def test_create_product_invalid_price(client: FlaskClient):
	response = client.post("/api/products", json={"name": "Чай", "price": "безкоштовно"})
	assert response.status_code == 400
	assert "Ціна має бути числом" in response.get_json()["error"]


def test_create_product_missing_fields(client: FlaskClient):
	response = client.post("/api/products", json={"name": "Шоколад"})
	assert response.status_code == 400