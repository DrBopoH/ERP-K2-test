

// app/api/index.ts
import type { Client, Product, OrderItem, Order } from '@/types/index'

const BASE = (import.meta.env.VITE_API_URL ?? 'http://localhost:5000') + '/api'

export const api = {

	/** Створює нового клієнта */
	createClient: (name: string): Promise<Client> =>
		fetch(`${BASE}/clients`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name })
		}).then(r => r.json()),

	/** Отримує повний список усіх клієнтів */
	getClients: (): Promise<Client[]> => 
		fetch(`${BASE}/clients`).then(r => r.json()),
	
	/** Оновлює дані клієнта (назву) за його ID */
	updateClient: (id: number, name: string): Promise<Client> =>
		fetch(`${BASE}/clients/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name })
		}).then(r => r.json()),

	/** Видаляє клієнта за ID */
	deleteClient: (id: number): Promise<{ success: boolean }> => // или что там шлет бек
		fetch(`${BASE}/clients/${id}`, { method: 'DELETE' }).then(r => r.json()),

	/** Створює новий товар */
	createProduct: (name: string, price: number): Promise<Product> =>
		fetch(`${BASE}/products`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, price })
		}).then(r => r.json()),

	/** Отримує повний список усіх доступних товарів */
	getProducts: (): Promise<Product[]> => 
		fetch(`${BASE}/products`).then(r => r.json()),

	/** Оновлює дані існуючого товару (назву та ціну) за його ID */
	updateProduct: (id: number, name: string, price: number): Promise<Product> =>
		fetch(`${BASE}/products/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, price })
		}).then(r => r.json()),

	/** Видаляє товар за ID */
	deleteProduct: (id: number): Promise<{ success: boolean }> =>
		fetch(`${BASE}/products/${id}`, { method: 'DELETE' }).then(r => r.json()),

	/**
	 * Створює нове замовлення для вказаного клієнта.
	 * @param clientId ID клієнта-замовника
	 * @param items Масив товарів (ID та кількість)
	 * @returns Створене замовлення із розрахованою загальною вартістю
	 */
	createOrder: (client_id: number, items: OrderItem[]): Promise<Order> =>
		fetch(`${BASE}/orders`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ client_id, items })
		}).then(r => r.json()),

	/**
	 * Отримує історію всіх замовлень конкретного клієнта.
	 * @param clientId ID клієнта
	 * @returns Масив замовлень із деталізацією по кожному товару
	 */
	getClientOrders: (client_id: number): Promise<Order[]> =>
		fetch(`${BASE}/clients/${client_id}/orders`).then(r => r.json()),
}