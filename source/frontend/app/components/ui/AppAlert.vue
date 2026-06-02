<script setup lang="ts">


	// app/components/ui/AppAlert.vue
	defineProps<{
		message: string
		type?: 'success' | 'error'
	}>()
</script>

<template>
	<div v-if="message" :class="['alert', type ?? 'success']">
		{{ message }}
	</div>
</template>