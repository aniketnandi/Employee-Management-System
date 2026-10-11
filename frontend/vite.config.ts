import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// The dev server proxies /api to the backend, so the browser only ever talks to one origin.
// This works the same on localhost, in Docker Compose and in GitHub Codespaces.
const apiTarget = process.env.API_PROXY_TARGET ?? 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    allowedHosts: ['.app.github.dev'],
    proxy: {
      '/api': { target: apiTarget, changeOrigin: true },
    },
  },
})
