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

<style scoped></style>