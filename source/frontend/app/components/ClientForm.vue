<script setup lang="ts">


	// app/components/ClientForm.vue
	import { ref } from 'vue'
	import { api } from '@/api/index'
	import AppInput from '@/components/ui/AppInput.vue'
	import AppButton from '@/components/ui/AppButton.vue'
	import AppAlert from '@/components/ui/AppAlert.vue'

	const emit = defineEmits<{ created: [] }>()

	const name = ref('')
	const loading = ref(false)
	const alert = ref({ message: '', type: 'success' as 'success' | 'error' })

	async function submit() {
		if (!name.value.trim()) return
		loading.value = true
		try {
			const res = await api.createClient(name.value.trim())
			if (res.error) throw new Error(res.error)
			alert.value = { message: `Клієнт "${res.name}" створений`, type: 'success' }
			name.value = ''
			emit('created')
		} catch (e: any) {
			alert.value = { message: e.message, type: 'error' }
		} finally {
			loading.value = false
		}
	}
</script>

<template>
	<div class="form-card">
		<h2>Новий клієнт</h2>
		<AppAlert v-bind="alert" />
		<AppInput v-model="name" label="Назва" placeholder="ТОВ Приклад" />
		<AppButton :loading="loading" @click="submit">Створити</AppButton>
	</div>
</template>