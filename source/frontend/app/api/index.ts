

// app/api/index.ts
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:5000/api'

export const api = {
	createClient: (name: string) =>
		fetch(`${BASE}/clients`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name })
		}).then(r => r.json()),

	getClients: () => fetch(`${BASE}/clients`).then(r => r.json()),
	
	updateClient: (id: number, name: string) =>
		fetch(`${BASE}/clients/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name })
		}).then(r => r.json()),

	createProduct: (name: string, price: number) =>
		fetch(`${BASE}/products`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, price })
		}).then(r => r.json()),

	getProducts: () => fetch(`${BASE}/products`).then(r => r.json()),

	updateProduct: (id: number, name: string, price: number) =>
		fetch(`${BASE}/products/${id}`, {
			method: 'PUT',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, price })
		}).then(r => r.json()),

	createOrder: (client_id: number, items: any[]) =>
		fetch(`${BASE}/orders`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ client_id, items })
		}).then(r => r.json()),

	getClientOrders: (client_id: number) =>
		fetch(`${BASE}/clients/${client_id}/orders`).then(r => r.json()),
}