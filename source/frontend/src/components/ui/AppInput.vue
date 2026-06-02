<script setup lang="ts">
defineProps<{
	modelValue: string | number
	label: string
	type?: string
	placeholder?: string
}>()

defineEmits<{
	'update:modelValue': [value: string]
}>()
</script>

<template>
	<div class="field">
		<label>{{ label }}</label>
		<input
			:type="type ?? 'text'"
			:value="modelValue"
			:placeholder="placeholder"
			@input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
		/>
	</div>
</template>