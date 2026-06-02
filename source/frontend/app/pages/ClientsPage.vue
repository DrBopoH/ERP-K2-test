<script setup lang="ts">


	// app/pages/ClientsPage.vue
	import ClientForm from '@/components/ClientForm.vue'

	function handleClientCreated() {
		console.log('Клієнт успішно створений!')
	}
</script>

<template>
	<div class="page-container">
		<ClientForm @created="handleClientCreated" />
	</div>
</template>

<style scoped>
	.page-container {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>