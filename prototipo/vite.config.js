import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',  // URL del tuo backend Flask
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // Riscrivi il percorso, se necessario
      }
    }
  }
})
