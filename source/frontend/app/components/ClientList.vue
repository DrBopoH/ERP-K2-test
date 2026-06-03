<script setup lang="ts">


	// app/components/ClientList.vue
	import { ref, onMounted } from 'vue'
	import { api } from '@/api/index'
	import AppInput from '@/components/ui/AppInput.vue'
	import AppButton from '@/components/ui/AppButton.vue'

	const clients = ref<any[]>([])
	const loading = ref(false)
	const editingId = ref<number | null>(null)
	const editForm = ref({ name: '' })

	async function load() {
		loading.value = true
		try {
			clients.value = await api.getClients()
		} catch (e) {
			console.error(e)
		} finally {
			loading.value = false
		}
	}

	function startEdit(client: any) {
		editingId.value = client.id
		editForm.value = { name: client.name }
	}

	async function saveEdit(id: number) {
		try {
			await api.updateClient(id, editForm.value.name)
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
		<h2>Список клієнтів</h2>
		<div v-if="loading" class="status-text">Завантаження...</div>
		
		<div class="items-list">
			<div v-for="client in clients" :key="client.id" class="order-card item-row">
				
				<template v-if="editingId !== client.id">
					<div class="view-mode">
						<div class="info-group">
							<span class="item-id">#{{ client.id }}</span>
							<span class="item-name">{{ client.name }}</span>
						</div>
						<AppButton variant="icon" title="Редагувати" @click="startEdit(client)">
							<img 
								src="https://img.icons8.com/ios-glyphs/30/737373/edit.png" 
								alt="Ред" 
								class="edit-icon"
							/>
						</AppButton>
					</div>
				</template>

				<template v-else>
					<div class="edit-mode">
						<div class="edit-inputs">
							<AppInput v-model="editForm.name" placeholder="Назва" class="input-full" />
						</div>
						<div class="edit-buttons">
							<AppButton variant="secondary" @click="editingId = null">Скасувати</AppButton>
							<AppButton @click="saveEdit(client.id)">Зберегти</AppButton>
						</div>
					</div>
				</template>

			</div>
		</div>
	</div>
</template>