import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    proxy: {
      // Forward all FastAPI routes through Vite dev server (avoids CORS)
      '/signals':  { target: 'http://localhost:8000', changeOrigin: true },
      '/prices':   { target: 'http://localhost:8000', changeOrigin: true },
      '/sentiment':{ target: 'http://localhost:8000', changeOrigin: true },
      '/health':   { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
})
