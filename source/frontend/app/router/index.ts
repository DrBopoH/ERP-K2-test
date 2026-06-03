//
// app/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import ClientsPage from '@/pages/ClientsPage.vue'
import ProductsPage from '@/pages/ProductsPage.vue'
import OrdersPage from '@/pages/OrdersPage.vue'

export default createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/', component: ClientsPage },
		{ path: '/products', component: ProductsPage },
		{ path: '/orders', component: OrdersPage },
	],
})
