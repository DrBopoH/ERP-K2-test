<script setup lang="ts">
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

<style scoped>
	.app-layout {
		max-width: 1200px;
		margin: 0 auto;
		padding: 20px;
		font-family: sans-serif;
	}
	.app-header {
		border-bottom: 1px solid #eee;
		padding-bottom: 15px;
		margin-bottom: 30px;
	}
	.nav-menu {
		display: flex;
		gap: 20px;
	}
	.nav-link {
		text-decoration: none;
		color: #2c3e50;
		font-weight: bold;
		padding: 5px 10px;
		border-radius: 4px;
	}
	.nav-link.router-link-exact-active {
		background-color: #42b983;
		color: white;
	}
	.app-content {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
</style>