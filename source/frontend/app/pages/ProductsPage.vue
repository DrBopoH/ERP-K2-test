<script setup lang="ts">


	// app/pages/ProductsPage.vue
	import ProductForm from '@/components/ProductForm.vue'

	function handleProductCreated() {
		console.log('Товар успішно створений!')
	}
</script>

<template>
	<div class="page-container">
		<ProductForm @created="handleProductCreated" />
	</div>
</template>

<style scoped>
	.page-container {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>