<script setup lang="ts">


	// app/App.vue
	import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
	<div class="app-layout">
		<header class="app-header">
			<nav class="nav-menu">
				<RouterLink to="/" class="nav-link">Клієнти</RouterLink>
				<RouterLink to="/products" class="nav-link">Товари</RouterLink>
				<RouterLink to="/orders" class="nav-link">Замовлення</RouterLink>
			</nav>
		</header>

		<main class="app-content">
			<RouterView />
		</main>
	</div>
</template>

<style>
	.app-layout {
		max-width: 1200px;
		margin: 0 auto;
		padding: 20px;
	}

	.app-header {
		border-bottom: 1px solid var(--border);
		padding-bottom: 15px;
		margin-bottom: 30px;
	}

	.nav-menu {
		display: flex;
		gap: 10px;
	}

	.nav-link {
		text-decoration: none;
		color: var(--text);
		font-weight: 500;
		padding: 8px 16px;
		border-radius: 6px; 
		transition: background-color 0.15s ease;
	}

	.nav-link:hover {
		background-color: #e0e7ff;
	}

	.nav-link.router-link-exact-active {
		background-color: var(--primary);
		color: white;
	}

	.app-content {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
</style>