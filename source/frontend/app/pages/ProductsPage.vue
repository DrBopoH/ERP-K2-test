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
	<div class="page-layout">
		<div class="column">
			<ProductForm @created="handleProductCreated" />
		</div>
		<div class="column">
			<ProductList ref="listRef" />
		</div>
	</div>
</template>