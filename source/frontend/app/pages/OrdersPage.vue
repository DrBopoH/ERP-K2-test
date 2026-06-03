<script setup lang="ts">
//
// app/pages/OrdersPage.vue
import OrderForm from '@/components/OrderForm.vue'
import OrderList from '@/components/OrderList.vue'

function handleOrderCreated() {
	console.log('Замовлення створено!')
}
</script>

<template>
	<div class="page-layout">
		<div class="column">
			<OrderList />
		</div>

		<div class="column">
			<OrderForm @created="handleOrderCreated" />
		</div>
	</div>
</template>
