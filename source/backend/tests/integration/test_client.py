from flask.testing import FlaskClient


def test_create_client_success(client: FlaskClient):
	response = client.post("/api/clients", json={"name": "ТОВ Тест"})
	assert response.status_code == 201
	data = response.get_json()
	assert data["id"] == 1
	assert data["name"] == "ТОВ Тест"


def test_create_client_missing_name(client: FlaskClient):
	response = client.post("/api/clients", json={})
	assert response.status_code == 400
	assert "Поле 'name' є обов'язковим" in response.get_json()["error"]