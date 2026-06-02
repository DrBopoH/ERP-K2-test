<script setup lang="ts">
	import { ref } from 'vue'
	import { api } from '@/api/index'
	import type { OrderItem } from '@/types/index'
	import AppInput from '@/components/ui/AppInput.vue'
	import AppButton from '@/components/ui/AppButton.vue'
	import AppAlert from '@/components/ui/AppAlert.vue'

	const emit = defineEmits<{ created: [] }>()

	const clientId = ref('')
	const items = ref<OrderItem[]>([{ product_id: 0, quantity: 1 }])
	const loading = ref(false)
	const alert = ref({ message: '', type: 'success' as 'success' | 'error' })

	function addItem() {
		items.value.push({ product_id: 0, quantity: 1 })
	}

	function removeItem(i: number) {
		items.value.splice(i, 1)
	}

	async function submit() {
		if (!clientId.value) return
		loading.value = true
		try {
			const res = await api.createOrder(parseInt(clientId.value), items.value)
			if (res.error) throw new Error(res.error)
			alert.value = { message: `Замовлення #${res.id} на ${res.total_amount}₴ створено`, type: 'success' }
			clientId.value = ''
			items.value = [{ product_id: 0, quantity: 1 }]
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
		<h2>Нове замовлення</h2>
		<AppAlert v-bind="alert" />
		<AppInput v-model="clientId" label="ID клієнта" type="number" placeholder="1" />

		<div v-for="(item, i) in items" :key="i" class="order-item-row">
			<AppInput v-model="item.product_id" label="ID товару" type="number" />
			<AppInput v-model="item.quantity" label="Кількість" type="number" />
			<button v-if="items.length > 1" @click="removeItem(i)">✕</button>
		</div>

		<AppButton variant="primary" @click="addItem">+ Товар</AppButton>
		<AppButton :loading="loading" @click="submit">Створити замовлення</AppButton>
	</div>
</template>