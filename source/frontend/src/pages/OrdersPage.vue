<script setup lang="ts">
	import OrderForm from '@/components/OrderForm.vue'
	import OrderList from '@/components/OrderList.vue'

	function handleOrderCreated() {
		console.log('Замовлення створено!')
	}
</script>

<template>
	<div class="orders-page">
		<div class="column">
			<OrderForm @created="handleOrderCreated" />
		</div>
		<div class="column">
			<OrderList />
		</div>
	</div>
</template>

<style scoped>
	.orders-page {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 30px;
		align-items: start;
	}

	@media (max-width: 768px) {
		.orders-page {
			grid-template-columns: 1fr;
		}
	}
</style>