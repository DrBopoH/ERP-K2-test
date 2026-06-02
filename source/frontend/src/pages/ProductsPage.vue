<script setup lang="ts">
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

<style scoped></style>