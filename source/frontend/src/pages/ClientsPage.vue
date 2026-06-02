<script setup lang="ts">
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

<style scoped></style>