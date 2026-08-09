import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: true, // <--- เพิ่ม 3 บรรทัดนี้เข้าไปครับ
  }
})