##龍芯⚡️2026-06-21-ENGINE-VITE-CONFIG-FILE1-v1.0-2
# 君子協議: 本文件受龍魂DNA追溯保護

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
  },
  server: {
    port: 5173,
    strictPort: false,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
