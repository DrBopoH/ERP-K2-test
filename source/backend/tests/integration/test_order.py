from flask.testing import FlaskClient


def test_create_order_success(client: FlaskClient):
	client.post("/api/clients", json={"name": "Іван"})
	client.post("/api/products", json={"name": "Ноутбук", "price": 1000.0})
	client.post("/api/products", json={"name": "Мишка", "price": 50.0})

	order_data = {
		"client_id": 1,
		"items": [
			{"product_id": 1, "quantity": 1},
			{"product_id": 2, "quantity": 2}
		]
	}
	response = client.post("/api/orders", json=order_data)
	assert response.status_code == 201
	
	data = response.get_json()
	assert data["total_amount"] == 1100.0
	assert data["items_count"] == 2


def test_create_order_client_not_found(client: FlaskClient):
	client.post("/api/products", json={"name": "Товар", "price": 10.0})
	order_data = {
		"client_id": 999,
		"items": [{"product_id": 1, "quantity": 1}]
	}
	response = client.post("/api/orders", json=order_data)
	assert response.status_code == 404
	assert "Клієнта з id 999 не знайдено" in response.get_json()["error"]


def test_create_order_product_not_found(client: FlaskClient):
	client.post("/api/clients", json={"name": "Олена"})
	order_data = {
		"client_id": 1,
		"items": [{"product_id": 999, "quantity": 1}]
	}
	response = client.post("/api/orders", json=order_data)
	assert response.status_code == 404


def test_create_order_invalid_quantity(client: FlaskClient):
	client.post("/api/clients", json={"name": "Олена"})
	client.post("/api/products", json={"name": "Товар", "price": 10.0})
	order_data = {
		"client_id": 1,
		"items": [{"product_id": 1, "quantity": 0}]
	}
	response = client.post("/api/orders", json=order_data)
	assert response.status_code == 400
	assert "Кількість товару має бути більшою за 0" in response.get_json()["error"]


def test_create_order_missing_fields(client: FlaskClient):
	response = client.post("/api/orders", json={})
	assert response.status_code == 400
	assert "client_id та непорожній масив items є обов'язковими" in response.get_json()["error"]

	response = client.post("/api/orders", json={"client_id": 1, "items": []})
	assert response.status_code == 400
	assert "client_id та непорожній масив items є обов'язковими" in response.get_json()["error"]



def test_get_client_orders_success(client: FlaskClient):
	client.post("/api/clients", json={"name": "Петро"})
	client.post("/api/products", json={"name": "Сік", "price": 40.0})
	
	client.post("/api/orders", json={
		"client_id": 1,
		"items": [{"product_id": 1, "quantity": 3}]
	})

	response = client.get("/api/clients/1/orders")
	assert response.status_code == 200
	data = response.get_json()
	assert len(data) == 1
	assert data[0]["total_amount"] == 120.0
	assert data[0]["items"][0]["product_name"] == "Сік"


def test_get_client_orders_404(client: FlaskClient):
	response = client.get("/api/clients/999/orders")
	assert response.status_code == 404