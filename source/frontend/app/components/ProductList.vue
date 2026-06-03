2<script setup lang="ts">


	// app/components/ProductForm.vue
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
	<div class="form-card">
		<h2>Довідник товарів</h2>
		<div v-if="loading">Завантаження...</div>
		
		<div class="order-items">
			<div v-for="product in products" :key="product.id" class="order-card">
				<template v-if="editingId !== product.id">
					<div class="row">
						<div>
							<span>#{{ product.id }}</span>
							<span>{{ product.name }}</span>
						</div>
						<div class="row">
							<strong>{{ product.price }} ₴</strong>
							<AppButton variant="secondary" @click="startEdit(product)">Ред.</AppButton>
						</div>
					</div>
				</template>

				<template v-else>
					<div class="row">
						<AppInput v-model="editForm.name" placeholder="Назва" />
						<AppInput v-model="editForm.price" type="number" placeholder="Ціна" />
					</div>
					<div class="row">
						<AppButton variant="secondary" @click="editingId = null">Скасувати</AppButton>
						<AppButton @click="saveEdit(product.id)">Зберегти</AppButton>
					</div>
				</template>
			</div>
		</div>
	</div>
</template>