<script setup lang="ts">


	// app/pages/ClientsPage.vue
	import ClientForm from '@/components/ClientForm.vue'
	import ClientList from '@/components/ClientList.vue'
	import { ref } from 'vue'

	const listRef = ref<InstanceType<typeof ClientList> | null>(null)

	function handleClientCreated() {
		if (listRef.value) listRef.value.load()
	}
</script>

<template>
	<div class="page-layout">
		<div class="column">
			<ClientForm @created="handleClientCreated" />
		</div>
		<div class="column">
			<ClientList ref="listRef" />
		</div>
	</div>
</template>