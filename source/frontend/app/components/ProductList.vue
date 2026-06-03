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

	onMounted(() => load())
	defineExpose({ load })
</script>

<template>
	<div class="form-card list-card">
		<h2>Довідник товарів</h2>
		<div v-if="loading" class="status-text">Завантаження...</div>
		
		<div class="items-list">
			<div v-for="product in products" :key="product.id" class="order-card item-row">
				
				<template v-if="editingId !== product.id">
					<div class="view-mode">
						<div class="info-group">
							<span class="item-id">#{{ product.id }}</span>
							<span class="item-name">{{ product.name }}</span>
						</div>
						<div class="action-group">
							<strong class="item-price">{{ product.price }} ₴</strong>
							
							<AppButton variant="icon" title="Редагувати" @click="startEdit(product)">
								<img 
									src="https://img.icons8.com/ios-glyphs/30/737373/edit.png" 
									alt="Ред" 
									class="edit-icon"
								/>
							</AppButton>
						</div>
					</div>
				</template>

				<template v-else>
					<div class="edit-mode">
						<div class="edit-inputs">
							<AppInput v-model="editForm.name" placeholder="Назва" class="input-grow" />
							<AppInput v-model="editForm.price" type="number" placeholder="Ціна" class="input-fixed" />
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