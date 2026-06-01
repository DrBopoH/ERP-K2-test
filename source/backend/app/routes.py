from typing import Any, List

from flask import Blueprint, jsonify, request

from app.models import Client, Order, OrderItem, Product, db

api_bp = Blueprint("api", __name__)



@api_bp.route("/clients", methods=["POST"])
def create_client():
	data: Any = request.get_json()
	if not data or "name" not in data:
		return jsonify({"error": "Поле 'name' є обов'язковим"}), 400
		
	client = Client(name=data["name"])
	db.session.add(client)
	db.session.commit()
	
	return jsonify({"id": client.id, "name": client.name}), 201

@api_bp.route("/products", methods=["POST"])
def create_product():
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
def create_order():
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
		quantity: Any = item_data.get("quantity", 1)
		
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
def get_client_orders(client_id):
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