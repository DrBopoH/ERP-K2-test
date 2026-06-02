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

<style scoped></style>