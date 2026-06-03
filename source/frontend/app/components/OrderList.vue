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

	/** Завантажує історію замовлень для введеного ID клієнта, очищуючи попередні помилки */
	async function load() {
		if (!clientId.value) return
		loading.value = true
		error.value = ''
		try {
			const res = await api.getClientOrders(parseInt(clientId.value))
			if (res.error) throw new Error(res.error)
			orders.value = res
		} catch (e: unknown) {
			error.value = e.message
			orders.value = []
		} finally {
			loading.value = false
		}
	}
</script>

<template>
	<div class="form-card list-card">
		<h2>Замовлення клієнта</h2>
		<div class="row">
			<AppInput v-model="clientId" label="ID клієнта" type="number" placeholder="1" />
			<AppButton :loading="loading" @click="load">Показати</AppButton>
		</div>
		
		<AppAlert v-if="error" :message="error" type="error" />

		<div class="items-list">
			<div v-for="order in orders" :key="order.id" class="order-card item-row">
				<div class="order-header">
					<span class="order-id">Замовлення {{ order.id }}</span>
					<span class="order-date">{{ new Date(order.created_at).toLocaleDateString('uk-UA') }}</span>
				</div>
				
				<div class="order-items">
					<div v-for="(item, idx) in order.items" :key="idx" class="order-item-row">
						<span class="item-name">◾ {{ item.product_name }}</span>
						<span class="item-meta">
							{{ item.quantity }} шт × {{ item.price_at_moment }} ₴
						</span>
					</div>
				</div>
				
				<div class="order-total">
					<span>Загалом до сплати:</span>
					<span class="total-price">{{ order.total_amount }} ₴</span>
				</div>
			</div>
		</div>
	</div>
</template>