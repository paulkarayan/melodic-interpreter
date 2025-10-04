import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 5173,
    proxy: {
      '/generate': 'http://localhost:8000',
      '/feeling-lucky': 'http://localhost:8000',
      '/analyze-session': 'http://localhost:8000',
      '/transform-styles': 'http://localhost:8000',
      '/health': 'http://localhost:8000'
    }
  }
})
