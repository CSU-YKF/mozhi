import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "@/styles/element/index.scss";    
          @import "@/styles/var.scss";    
        `,
      },
    },
  },
  server: {
    historyApiFallback: true,
    host: '0.0.0.0',
    port: 80,
  },
  build:{
    outDir: '../dist',
    assetsDir: 'assets',
    publicPath: './',
  },
})
