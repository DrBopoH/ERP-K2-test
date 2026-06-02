<script setup lang="ts">


	// app/components/ui/AppButton.vue
	defineProps<{
		loading?: boolean
		variant?: 'primary' | 'secondary' | 'danger' | 'icon'
	}>()
</script>

<template>
	<button :disabled="loading" :class="['btn', variant ?? 'primary']">
		<span v-if="loading">⏳</span>
		<slot v-else />
	</button>
</template>