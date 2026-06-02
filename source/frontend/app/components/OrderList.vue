<script setup lang="ts">


	// app/components/OrderList.vue
	import { ref } from 'vue'
	import { api } from '@/api/index'
	import type { Order } from '@/types/index'
	import AppInput from '@/components/ui/AppInput.vue'
	import AppButton from '@/components/ui/AppButton.vue'

	const clientId = ref('')
	const orders = ref<Order[]>([])
	const loading = ref(false)
	const error = ref('')

	async function load() {
		if (!clientId.value) return
		loading.value = true
		error.value = ''
		try {
			const res = await api.getClientOrders(parseInt(clientId.value))
			if (res.error) throw new Error(res.error)
			orders.value = res
		} catch (e: any) {
			error.value = e.message
			orders.value = []
		} finally {
			loading.value = false
		}
	}
</script>

<template>
	<div class="form-card">
		<h2>Замовлення клієнта</h2>
		<div class="row">
			<AppInput v-model="clientId" label="ID клієнта" type="number" placeholder="1" />
			<AppButton :loading="loading" @click="load">Показати</AppButton>
		</div>
		<p v-if="error" class="alert error">{{ error }}</p>

		<div v-for="order in orders" :key="order.id" class="order-card">
			<div class="order-header">
				<span>#{{ order.id }}</span>
				<span>{{ new Date(order.created_at).toLocaleDateString('uk-UA') }}</span>
				<strong>{{ order.total_amount }} ₴</strong>
			</div>
			<div v-for="item in order.items" :key="item.product_id" class="order-item">
				{{ item.product_name }} × {{ item.quantity }} — {{ item.price_at_moment }} ₴
			</div>
		</div>

		<p v-if="!loading && orders.length === 0 && clientId">Замовлень не знайдено</p>
	</div>
</template>