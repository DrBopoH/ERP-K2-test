<script setup lang="ts">
	defineProps<{
		loading?: boolean
		variant?: 'primary' | 'danger'
	}>()
</script>

<template>
	<button :disabled="loading" :class="['btn', variant ?? 'primary']">
		<span v-if="loading">⏳</span>
		<slot v-else />
	</button>
</template>