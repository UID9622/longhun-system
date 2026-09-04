// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-a2f26a67
import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import { inspectAttr } from 'plugin-inspect-react-code'

// 可选插件：静默载入，未安装则不报错
const optionalPlugins: any[] = []
try {
  const pkg = await import('vite-plugin-compression')
  optionalPlugins.push(pkg.default({ algorithm: "gzip", threshold: 10240, deleteOriginFile: false }))
  optionalPlugins.push(pkg.default({ algorithm: "brotliCompress", threshold: 10240, deleteOriginFile: false }))
} catch { /* vite-plugin-compression 未安装 */ }

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  base: './',
  plugins: [
    inspectAttr(),
    react(),
    ...optionalPlugins,
  ],
  server: {
    port: 3000,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: "es2022",
    // 手动静态分块：把大依赖各自打成独立 vendor chunk
    rollupOptions: {
      output: {
        manualChunks: {
          "vendor-gsap": ["gsap"],
          "vendor-motion": ["framer-motion", "motion"],
          "vendor-lenis": ["lenis"],
          "vendor-radix": [
            "@radix-ui/react-accordion",
            "@radix-ui/react-dialog",
            "@radix-ui/react-select",
            "@radix-ui/react-tabs",
            "@radix-ui/react-visually-hidden",
          ],
          "vendor-markdown": ["react-markdown", "remark-gfm", "rehype-raw"],
        },
        // 资源命名规范化
        chunkFileNames: "js/[name]-[hash:8].js",
        assetFileNames: "assets/[name]-[hash:8][extname]",
      },
    },
    // 500KB 告警阈值
    chunkSizeWarningLimit: 500,
    // 启用 CSS 代码分割
    cssCodeSplit: true,
    // sourcemap 仅 prod 关闭
    sourcemap: mode !== "production",
  },
  css: {
    devSourcemap: true,
  },
}));
