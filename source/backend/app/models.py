from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Client(db.Model):
	__tablename__: str = "clients"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	
	orders: Mapped[list["Order"]] = relationship(back_populates="client")

class Product(db.Model):
	__tablename__: str = "products"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	price: Mapped[float] = mapped_column(Float, nullable=False)

class Order(db.Model):
	__tablename__: str = "orders"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	
	client: Mapped["Client"] = relationship(back_populates="orders")
	items: Mapped[list["OrderItem"]] = relationship(
		back_populates="order", cascade="all, delete-orphan"
	)

	@property
	def total_amount(self) -> float:
		return sum(item.quantity * item.price_at_moment for item in self.items)

class OrderItem(db.Model):
	__tablename__: str = "order_items"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
	product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
	
	price_at_moment: Mapped[float] = mapped_column(Float, nullable=False) 

	order: Mapped["Order"] = relationship(back_populates="items")
	product: Mapped["Product"] = relationship()