

// vite.config.ts
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '')

	return {
		plugins: [vue()],
		resolve: {
			alias: {
				'@': fileURLToPath(new URL('./app', import.meta.url))
			}
		},
		server: {
			proxy: {
				'/api': env.VITE_API_URL ?? 'http://localhost:5000'
			}
		}
	}
})