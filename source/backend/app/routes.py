"""
Модуль маршрутизації (роутингу) API для ERP системи.
Визначає ендпоінти для управління клієнтами, товарами та замовленнями.
Обробляє HTTP-запити, виконує валідацію вхідних даних та взаємодіє з базою даних.
"""

from typing import Any, List, Tuple

from flask import Blueprint, Response, jsonify, request

from app.models import Client, Order, OrderItem, Product, db

api_bp = Blueprint("api", __name__)



@api_bp.route("/clients", methods=["POST"])
def create_client() -> Tuple[Response, int]:
	"""
	Створення нового клієнта.
	
	Очікує JSON у форматі:
	{
		"name": "string"
	}
	
	Повертає:
		JSON з даними створеного клієнта (id, name) та HTTP статус 201 (Created).
		У разі відсутності обов'язкових полів повертає HTTP статус 400.
	"""
	data: Any = request.get_json()
	if not data or "name" not in data:
		return jsonify({"error": "Поле 'name' є обов'язковим"}), 400
		
	client = Client(name=data["name"])
	db.session.add(client)
	db.session.commit()
	
	return jsonify({"id": client.id, "name": client.name}), 201

@api_bp.route("/products", methods=["POST"])
def create_product() -> Tuple[Response, int]:
	"""
	Створення нового товару.
	
	Очікує JSON у форматі:
	{
		"name": "string",
		"price": float
	}
	
	Повертає:
		JSON з даними створеного товару (id, name, price) та HTTP статус 201.
		У разі помилки валідації повертає HTTP статус 400.
	"""
	data: Any = request.get_json()
	if not data or "name" not in data or "price" not in data:
		return jsonify({"error": "Поля 'name' та 'price' є обов'язковими"}), 400
		
	try:
		price = float(data["price"])
	except ValueError:
		return jsonify({"error": "Ціна має бути числом"}), 400
		
	product = Product(name=data["name"], price=price)
	db.session.add(product)
	db.session.commit()
	
	return jsonify({"id": product.id, "name": product.name, "price": product.price}), 201

@api_bp.route("/orders", methods=["POST"])
def create_order() -> Tuple[Response, int]:
	"""
	Створення замовлення для клієнта з автоматичним розрахунком суми.
	
	Очікує JSON у форматі:
	{
		"client_id": int,
		"items": [
			{
				"product_id": int, 
				"quantity": int
			}
		]
	}
	
	Повертає:
		JSON з підсумками замовлення (id, client_id, total_amount, items_count) та HTTP статус 201.
		
		У разі порушення бізнес-правил (клієнт/товар не знайдено, хибна кількість) 
		повертає 400 або 404 та відкочує транзакцію.
	"""
	data: Any = request.get_json()
	
	if not data or "client_id" not in data or not data.get("items"):
		return jsonify({"error": "client_id та непорожній масив items є обов'язковими"}), 400
		
	client: Client | None = db.session.get(Client, data["client_id"])
	if not client:
		return jsonify({"error": f"Клієнта з id {data['client_id']} не знайдено"}), 404
		
	order = Order(client_id=client.id)
	db.session.add(order)
	
	total_amount: float = 0.0
	
	for item_data in data["items"]:
		product_id: Any = item_data.get("product_id")
		quantity: int = item_data.get("quantity", 1)
		
		if quantity <= 0:
			db.session.rollback()
			return jsonify({"error": "Кількість товару має бути більшою за 0"}), 400
			
		product: Product | None = db.session.get(Product, product_id)
		if not product:
			db.session.rollback()
			return jsonify({"error": f"Товар з id {product_id} не знайдено"}), 404
			
		order_item = OrderItem(
			order=order,
			product_id=product.id,
			quantity=quantity,
			price_at_moment=product.price
		)
		db.session.add(order_item)
		total_amount += product.price * quantity
		
	db.session.commit()
	
	return jsonify({
		"id": order.id,
		"client_id": order.client_id,
		"total_amount": total_amount,
		"items_count": len(data["items"])
	}), 201


@api_bp.route("/clients/<int:client_id>/orders", methods=["GET"])
def get_client_orders(client_id: int) -> Tuple[Response, int]:
	"""
	Отримання списку замовлень конкретного клієнта.
	
	Параметри шляху:
	- client_id (int): ID клієнта в базі.
	
	Повертає:
		Масив JSON-об'єктів (замовлень), де кожен об'єкт містить деталі замовлення, 
		загальну суму (total_amount) та розгорнутий список придбаних товарів.
	"""
	client: Client | None = db.session.get(Client, client_id)
	if not client:
		return jsonify({"error": "Клієнта не знайдено"}), 404
		
	orders_data: List = []
	for order in client.orders:
		orders_data.append({
			"id": order.id,
			"created_at": order.created_at.isoformat(),
			"total_amount": order.total_amount, 
			"items": [
				{
					"product_id": item.product_id,
					"product_name": item.product.name,
					"quantity": item.quantity,
					"price_at_moment": item.price_at_moment
				} for item in order.items
			]
		})
		
	return jsonify(orders_data), 200