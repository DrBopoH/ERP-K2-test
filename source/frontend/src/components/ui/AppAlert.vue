<script setup lang="ts">
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