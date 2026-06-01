from flask import Blueprint, request, jsonify
from app.models import db, Client, Product

api_bp = Blueprint("api", __name__)

@api_bp.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Поле 'name' є обов'язковим"}), 400
        
    client = Client(name=data["name"])
    db.session.add(client)
    db.session.commit()
    
    return jsonify({"id": client.id, "name": client.name}), 201

@api_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
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