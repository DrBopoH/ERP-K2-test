//
// app/types/index.ts

/** Сутність клієнта (ID та назва) */
export interface Client {
	id: number
	name: string
}

/** Сутність товару (ID, назва, актуальна ціна) */
export interface Product {
	id: number
	name: string
	price: number
}

/** Позиція товару для створення нового замовлення */
export interface OrderItem {
	product_id: number
	quantity: number
}

/** Повна структура замовлення, що повертається сервером */
export interface Order {
	id: number
	client_id: number
	total_amount: number
	created_at: string
	items: {
		product_id: number
		product_name: string
		quantity: number
		price_at_moment: number
	}[]
}
