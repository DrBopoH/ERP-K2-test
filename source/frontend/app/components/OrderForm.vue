<script setup lang="ts">


	// app/components/OrderForm.vue
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

	/** Додає новий порожній рядок товару до форми замовлення */
	function addItem() {
		items.value.push({ product_id: 0, quantity: 1 })
	}

	/** Видаляє рядок товару з форми замовлення за його індексом */
	function removeItem(i: number) {
		items.value.splice(i, 1)
	}

	/** Валідує дані, відправляє запит на створення сутності та скидає форму в разі успіху */
	async function submit() {
		if (!clientId.value) return
		loading.value = true
		try {
			const res = await api.createOrder(parseInt(clientId.value), items.value)
			if (res.error) throw new Error(res.error)
			alert.value = { message: `Замовлення ${res.id} на ${res.total_amount}₴ створено`, type: 'success' }
			clientId.value = ''
			items.value = [{ product_id: 0, quantity: 1 }]
			emit('created')
		} catch (e: unknown) {
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

		<div class="items-grid-container">
			<div class="items-grid-header">
				<label>ID Товару</label>
				<label>Кількість</label>
				<div></div>
			</div>

			<div v-for="(item, i) in items" :key="i" class="items-grid-row">
				<AppInput v-model="item.product_id" type="number" placeholder="0" />
				<AppInput v-model="item.quantity" type="number" placeholder="1" min="1" />

				<AppButton 
					v-if="items.length > 1" 
					variant="icon" 
					title="Видалити товар"
					@click="removeItem(i)"
				>
					✕
				</AppButton>
				<div v-else class="btn-spacer"></div> 
			</div>
		</div>

		<div class="form-actions">
			<AppButton variant="secondary" @click="addItem">+ Товар</AppButton>
			<AppButton :loading="loading" @click="submit">Створити замовлення</AppButton>
		</div>
	</div>
</template>