import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        proxy: {
            '/api': {
                target: 'https://automatic-test-case-g-eneratorand-e.vercel.app/',
                changeOrigin: true
            }
        }
    }
})
