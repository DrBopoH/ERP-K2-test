

// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'

export default defineConfig({
	plugins: [vue()],
	resolve: {
		alias: { '@': fileURLToPath(new URL('./app', import.meta.url)) }
	},
	server: {
		proxy: {
			'/api': 'http://localhost:5000'
		}
	}
})