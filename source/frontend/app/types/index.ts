

// app/types/index.ts
export interface Client {
	id: number
	name: string
}

export interface Product {
	id: number
	name: string
	price: number
}

export interface OrderItem {
	product_id: number
	quantity: number
}

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