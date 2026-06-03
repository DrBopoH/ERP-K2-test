<script setup lang="ts">


	// app/components/ProductList.vue
	import { ref, onMounted } from 'vue'
	import { api } from '@/api/index'
	import AppInput from '@/components/ui/AppInput.vue'
	import AppButton from '@/components/ui/AppButton.vue'

	const products = ref<any[]>([])
	const loading = ref(false)
	const editingId = ref<number | null>(null)
	const editForm = ref({ name: '', price: 0 })

	async function load() {
		loading.value = true
		try {
			products.value = await api.getProducts()
		} catch (e) {
			console.error(e)
		} finally {
			loading.value = false
		}
	}

	function startEdit(product: any) {
		editingId.value = product.id
		editForm.value = { name: product.name, price: product.price }
	}

	async function saveEdit(id: number) {
		try {
			await api.updateProduct(id, editForm.value.name, editForm.value.price)
			editingId.value = null
			await load()
		} catch (e) {
			alert('Помилка при збереженні')
		}
	}

	async function remove(id: number) {
		if (!confirm('Ви впевнені, що хочете видалити цей товар?')) return
		try {
			await api.deleteClient(id)
			await load()
		} catch (e) {
			alert('Помилка при видаленні')
		}
	}

	onMounted(() => load())
	defineExpose({ load })
</script>

<template>
	<div class="form-card">
		<h2>Довідник товарів</h2>
		<div v-if="loading" class="text-muted">Завантаження...</div>
		
		<div class="items-list">
			<div v-for="product in products" :key="product.id" class="item-row">
				
				<template v-if="editingId !== product.id">
					<div class="view-mode">
						<div class="info-group">
							<span class="item-id">#{{ product.id }}</span>
							<span class="item-name">{{ product.name }}</span>
						</div>
						<div class="action-group">
							<strong class="item-price">{{ product.price }} ₴</strong>
							
							<AppButton variant="icon" class="primary" title="Редагувати" @click="startEdit(product)">
								<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
										stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
									<path d="M12 20h9"></path>
									<path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
								</svg>
							</AppButton>

							<AppButton variant="icon" class="danger" title="Видалити" @click="remove(product.id)">
								<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
										stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
									<polyline points="3 6 5 6 21 6"></polyline>
									<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
								</svg>
							</AppButton>
						</div>
					</div>
				</template>

				<template v-else>
					<div class="edit-mode">
						<div class="edit-inputs">
							<AppInput v-model="editForm.name" placeholder="Назва" class="w-full" />
							<AppInput v-model="editForm.price" type="number" placeholder="Ціна" class="w-full" />
						</div>
						<div class="edit-buttons">
							<AppButton variant="secondary" @click="editingId = null">Скасувати</AppButton>
							<AppButton @click="saveEdit(product.id)">Зберегти</AppButton>
						</div>
					</div>
				</template>

			</div>
		</div>
	</div>
</template>