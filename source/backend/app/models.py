"""
Модуль моделей даних SQLAlchemy (ORM) для ERP системи.
Визначає структуру таблиць: клієнти, товари, замовлення та позиції замовлення.
"""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()



class Client(db.Model):
	"""
	Модель клієнта компанії.
	
	Атрибути:
		- id (int): Унікальний ідентифікатор клієнта (Primary Key).
		- name (str): Ім'я або назва компанії клієнта.
		- orders (list[Order]): Список усіх замовлень, пов'язаних з цим клієнтом.
	"""
	__tablename__: str = "clients"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	
	orders: Mapped[list["Order"]] = relationship(back_populates="client")

class Product(db.Model):
	"""
	Модель товару або послуги в системі.
	
	Атрибути:
		- id (int): Унікальний ідентифікатор товару (Primary Key).
		- name (str): Назва товару.
		- price (float): Поточна вартість товару в каталозі.
	"""
	__tablename__: str = "products"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	price: Mapped[float] = mapped_column(Float, nullable=False)

class Order(db.Model):
	"""
	Модель замовлення клієнта.
	
	Атрибути:
		- id (int): Унікальний ідентифікатор замовлення (Primary Key).
		- client_id (int): Ідентифікатор клієнта, що оформив замовлення (Foreign Key).
		- created_at (datetime): Дата та час створення замовлення (UTC).
		- client (Client): Об'єкт клієнта, прив'язаний до замовлення.
		- items (list[OrderItem]): Список конкретних позицій товарів у замовленні.
	"""
	__tablename__: str = "orders"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
	
	client: Mapped["Client"] = relationship(back_populates="orders")
	items: Mapped[list["OrderItem"]] = relationship(
		back_populates="order", cascade="all, delete-orphan"
	)

	@property
	def total_amount(self) -> float:
		"""
		Обчислювана властивість для розрахунку загальної вартості всього замовлення.
		
		Підсумовує вартість усіх позицій, базуючись на фіксованій ціні 
		на момент купівлі (quantity * price_at_moment).
		
		Повертає:
			- float: Загальна сума замовлення.
		"""
		return sum(item.quantity * item.price_at_moment for item in self.items)


class OrderItem(db.Model):
	"""
	Модель позиції товару в конкретному замовленні.
	Зберігає історичну ціну на момент оформлення для стабільності фінансових звітів.
	
	Атрибути:
		- id (int): Унікальний ідентифікатор позиції (Primary Key).
		- order_id (int): Ідентифікатор батьківського замовлення (Foreign Key).
		- product_id (int): Ідентифікатор купленого товару (Foreign Key).
		- quantity (int): Кількість замовлених одиниць товару.
		- price_at_moment (float): Фіксована ціна товару на момент створення замовлення.
		- order (Order): Об'єкт замовлення, до якого належить позиція.
		- product (Product): Об'єкт товару для отримання актуальних метаданих.
	"""
	__tablename__: str = "order_items"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
	product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
	
	price_at_moment: Mapped[float] = mapped_column(Float, nullable=False) 

	order: Mapped["Order"] = relationship(back_populates="items")
	product: Mapped["Product"] = relationship()