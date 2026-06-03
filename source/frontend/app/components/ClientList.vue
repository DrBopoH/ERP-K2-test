<script setup lang="ts">
//
// app/components/ClientList.vue
import { ref, onMounted } from 'vue'
import { api } from '@/api/index'
import type { Client } from '@/types/index'
import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'

const clients = ref<Client[]>([])
const loading = ref(false)
const editingId = ref<number | null>(null)
const editForm = ref({ name: '' })

/** Отримує актуальний список записів із сервера та оновлює стан компонента */
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

/** Переводить обраний запис у режим редагування, копіюючи його поточні дані у локальну форму */
function startEdit(client: Client) {
	editingId.value = client.id
	editForm.value = { name: client.name }
}

/** Відправляє оновлені дані на сервер, вимикає режим редагування та перезавантажує список */
async function saveEdit(id: number) {
	try {
		await api.updateClient(id, editForm.value.name)
		editingId.value = null
		await load()
	} catch {
		alert('Помилка при збереженні')
	}
}

async function remove(id: number) {
	if (!confirm('Ви впевнені, що хочете видалити цього клієнта?')) return
	try {
		await api.deleteProduct(id)
		await load()
	} catch {
		alert('Помилка при видаленні')
	}
}

onMounted(() => load())
defineExpose({ load })
</script>

<template>
	<div class="form-card">
		<h2>Список клієнтів</h2>
		<div v-if="loading" class="text-muted">Завантаження...</div>

		<div class="items-list">
			<div v-for="client in clients" :key="client.id" class="item-row">
				<template v-if="editingId !== client.id">
					<div class="view-mode">
						<div class="info-group">
							<span class="item-id">#{{ client.id }}</span>
							<span class="item-name">{{ client.name }}</span>
						</div>
						<div class="action-group">
							<AppButton
								variant="icon"
								class="primary"
								title="Редагувати"
								@click="startEdit(client)"
							>
								<svg
									width="18"
									height="18"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<path d="M12 20h9"></path>
									<path
										d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
									></path>
								</svg>
							</AppButton>

							<AppButton
								variant="icon"
								class="danger"
								title="Видалити"
								@click="remove(client.id)"
							>
								<svg
									width="18"
									height="18"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
								>
									<polyline points="3 6 5 6 21 6"></polyline>
									<path
										d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
									></path>
								</svg>
							</AppButton>
						</div>
					</div>
				</template>

				<template v-else>
					<div class="edit-mode">
						<div class="edit-inputs">
							<AppInput
								v-model="editForm.name"
								placeholder="Назва"
								class="input-full"
							/>
						</div>
						<div class="edit-buttons">
							<AppButton variant="secondary" @click="editingId = null"
								>Скасувати</AppButton
							>
							<AppButton @click="saveEdit(client.id)">Зберегти</AppButton>
						</div>
					</div>
				</template>
			</div>
		</div>
	</div>
</template>
