##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ENGINE-VITE-CONFIG-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

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
