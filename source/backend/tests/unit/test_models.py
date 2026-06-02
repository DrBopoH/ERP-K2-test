from app.models import Order, OrderItem


def test_order_total_amount_calculation():
	order = Order()
	
	item1 = OrderItem(quantity=2, price_at_moment=150.0)
	item2 = OrderItem(quantity=1, price_at_moment=450.0)
	
	order.items = [item1, item2]
	
	assert order.total_amount == 750.0