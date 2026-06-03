<script setup lang="ts">


	// app/pages/ProductsPage.vue
	import ProductForm from '@/components/ProductForm.vue'
	import ProductList from '@/components/ProductList.vue'
	import { ref } from 'vue'

	const listRef = ref<InstanceType<typeof ProductList> | null>(null)

	function handleProductCreated() {
		if (listRef.value) listRef.value.load()
	}
</script>

<template>
	<div class="layout-grid">
		<div class="column"><ProductForm @created="handleProductCreated" /></div>
		<div class="column"><ProductList ref="listRef" /></div>
	</div>
</template>

<style scoped>
	.layout-grid { 
		display: grid; 
		grid-template-columns: 1fr 1fr; 
		gap: 30px; 
		align-items: start; 
		max-width: 1000px; 
		margin: 0 auto; 
	}
	
	@media (max-width: 768px) { 
		.layout-grid { 
			grid-template-columns: 1fr; 
		} 
	}
</style>