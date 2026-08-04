# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂·可视化引擎协议 v1.0 · 附录A

> 性能基准测试 + 移动端适配 + WebWorker异步 + 离屏渲染 + PWA离线
> DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-ENGINE-APPENDIX-A-v1.0

---

## 附录A-1 · 性能基准测试

### A-1.1 测试环境

```
基准设备: Apple M4 Max (用户设备)
辅助设备: iPhone 15 Pro / 小米14 / iPad Pro M2 / 华为Mate X5
浏览器: Chrome 126 / Safari 17 / Firefox 127 / 微信内置浏览器
网络: 5G / WiFi-6 / 4G / 3G (四档)
测试工具: Lighthouse CI + WebPageTest + 自定义 FPS 计数器 + Memory Profiler
```

### A-1.2 渲染性能基准

| 图表类型 | 节点/数据量 | 首次渲染 | 交互帧率 | 内存占用 | 复杂度 | 目标 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **思维导图 V01** | 50节点 | < 500ms | 60fps | < 20MB | 低 | 🟢 |
| **思维导图 V01** | 200节点 | < 1.5s | 60fps | < 50MB | 中 | 🟢 |
| **思维导图 V01** | 1000节点 | < 3s | 30fps | < 100MB | 高 | 🟡 |
| **流程图 V02** | 20步骤 | < 300ms | 60fps | < 10MB | 低 | 🟢 |
| **流程图 V02** | 100步骤 | < 800ms | 60fps | < 30MB | 中 | 🟢 |
| **时序图 V03** | 10参与者 | < 400ms | 60fps | < 15MB | 低 | 🟢 |
| **时序图 V03** | 50参与者 | < 1.2s | 60fps | < 40MB | 中 | 🟢 |
| **状态图 V04** | 10状态 | < 300ms | 60fps | < 10MB | 低 | 🟢 |
| **状态图 V04** | 50状态 | < 1s | 60fps | < 35MB | 中 | 🟢 |
| **甘特图 V05** | 30任务 | < 500ms | 60fps | < 20MB | 低 | 🟢 |
| **甘特图 V05** | 200任务 | < 2s | 60fps | < 60MB | 中 | 🟡 |
| **饼图 V06** | 10扇区 | < 200ms | 60fps | < 10MB | 低 | 🟢 |
| **折线图 V07** | 1000数据点 | < 300ms | 60fps | < 15MB | 低 | 🟢 |
| **折线图 V07** | 10000数据点 | < 800ms | 60fps | < 30MB | 中 | 🟢 |
| **折线图 V07** | 100000数据点 | < 2s | 30fps | < 60MB | 高 | 🟡 |
| **散点图 V08** | 5000点 | < 500ms | 60fps | < 25MB | 中 | 🟢 |
| **散点图 V08** | 50000点 | < 2s | 30fps | < 80MB | 高 | 🟡 |
| **雷达图 V09** | 8维度 | < 300ms | 60fps | < 12MB | 低 | 🟢 |
| **热力图 V10** | 50×50网格 | < 400ms | 60fps | < 15MB | 低 | 🟢 |
| **热力图 V10** | 200×200网格 | < 1.5s | 60fps | < 50MB | 中 | 🟡 |
| **桑基图 V11** | 20节点 | < 500ms | 60fps | < 20MB | 低 | 🟢 |
| **树图 V12** | 100节点 | < 400ms | 60fps | < 15MB | 低 | 🟢 |
| **网络图 V13** | 50节点/100边 | < 600ms | 60fps | < 25MB | 中 | 🟢 |
| **网络图 V13** | 500节点/2000边 | < 3s | 30fps | < 120MB | 高 | 🟡 |
| **3D立体图 V14** | 简单模型(<1k面) | < 1s | 60fps | < 50MB | 中 | 🟢 |
| **3D立体图 V14** | 中等模型(10k面) | < 2s | 60fps | < 100MB | 中 | 🟢 |
| **3D立体图 V14** | 复杂模型(100k面) | < 5s | 30fps | < 200MB | 高 | 🟡 |
| **地理地图 V15** | 中国省级 | < 800ms | 60fps | < 30MB | 中 | 🟢 |
| **地理地图 V15** | 全球县级 | < 2s | 30fps | < 80MB | 高 | 🟡 |
| **词云 V16** | 100词 | < 400ms | 60fps | < 15MB | 低 | 🟢 |
| **仪表盘 V17** | 6指标 | < 300ms | 60fps | < 12MB | 低 | 🟢 |
| **动画时间轴 V18** | 20帧 | < 500ms | 60fps | < 20MB | 低 | 🟢 |

### A-1.3 性能降级策略（五级）

```
检测到性能瓶颈时，按优先级降级：
    │
    ├─ Level 1: 帧率 < 30fps → 关闭动画
    │   ├─ 禁用 CSS transitions/animations
    │   ├─ 禁用 SVG SMIL 动画
    │   ├─ 3D场景降至静态截图
    │   └─ 网络图关闭力导向动画
    │
    ├─ Level 2: 内存 > 100MB → 释放不可见资源
    │   ├─ 卸载屏幕外图表（IntersectionObserver）
    │   ├─ 释放 Three.js geometries/textures (dispose)
    │   ├─ ECharts dispose() 不可见图表
    │   ├─ 压缩纹理（3D场景纹理降为 512×512）
    │   └─ 大数据集启用分页/虚拟滚动
    │
    ├─ Level 3: 渲染 > 3s → 渐进式渲染
    │   ├─ 显示骨架屏（shimmer placeholder）
    │   ├─ Web Worker 后台异步渲染
    │   ├─ 先显示简化版（关键路径），再渐进细化
    │   ├─ 分批渲染：首屏→可视区→全量
    │   └─ 最终降级：生成静态 PNG 替代交互 SVG
    │
    ├─ Level 4: 网络慢(4G/3G) → 资源降级
    │   ├─ WebP 替代 PNG（体积减少 30%）
    │   ├─ 字体子集化（只加载渲染用到的字符）
    │   ├─ CDN 资源降级为本地缓存
    │   ├─ 延迟加载非首屏渲染器（code splitting）
    │   └─ 启用 Service Worker 离线缓存
    │
    └─ Level 5: 设备低端(M3) → 功能降级
        ├─ 3D → 静态PNG
        ├─ 网络图 → 简化版（≤50节点）
        ├─ 动画 → 全部禁用
        ├─ 交互 → 基础缩放/平移
        └─ 实时协作 → 禁用
```

### A-1.4 Web Worker 异步渲染

```typescript
// ── Web Worker 渲染管线 ──
// 将重型渲染任务移出主线程，保证UI不卡顿

// main.ts — 主线程
class AsyncRenderer {
  private workers: Map<RendererId, Worker> = new Map();

  constructor() {
    // 为每种渲染器创建专用 Worker
    this.createWorker('mermaid',  new URL('./workers/mermaid.worker.ts', import.meta.url));
    this.createWorker('echarts',  new URL('./workers/echarts.worker.ts', import.meta.url));
    this.createWorker('markmap',  new URL('./workers/markmap.worker.ts', import.meta.url));
    this.createWorker('graphviz', new URL('./workers/graphviz.worker.ts', import.meta.url));
  }

  private createWorker(id: RendererId, url: URL): void {
    const worker = new Worker(url, { type: 'module' });
    this.workers.set(id, worker);

    worker.onmessage = (e: MessageEvent) => {
      const { requestId, result, error } = e.data;
      const pending = this.pendingRequests.get(requestId);
      if (pending) {
        if (error) pending.reject(new Error(error));
        else pending.resolve(result);
        this.pendingRequests.delete(requestId);
      }
    };

    worker.onerror = (err) => {
      console.error(`[Viz Worker] ${id} error:`, err);
    };
  }

  private pendingRequests = new Map<string, { resolve: Function; reject: Function }>();

  async render(id: RendererId, code: string, options: RenderOptions): Promise<RenderResult> {
    const worker = this.workers.get(id);
    if (!worker) {
      // 无 Worker → 回退主线程渲染
      return this.renderMainThread(id, code, options);
    }

    const requestId = crypto.randomUUID();
    const promise = new Promise<RenderResult>((resolve, reject) => {
      this.pendingRequests.set(requestId, { resolve, reject });
    });

    // 超时保护
    const timeout = new Promise<RenderResult>((_, reject) => {
      setTimeout(() => reject(new Error(`Worker render timeout for ${id}`)), options.timeout || 10000);
    });

    worker.postMessage({ requestId, code, options }, []);
    return Promise.race([promise, timeout]);
  }

  async renderMainThread(id: RendererId, code: string, options: RenderOptions): Promise<RenderResult> {
    const renderer = await loadRenderer(id);
    return renderer.render(code, options);
  }

  terminate(): void {
    this.workers.forEach(w => w.terminate());
    this.workers.clear();
  }
}

// workers/mermaid.worker.ts — Worker 线程
import mermaid from 'mermaid';

self.onmessage = async (e: MessageEvent) => {
  const { requestId, code, options } = e.data;
  try {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#6B46C1',
        primaryTextColor: '#E2E8F0',
        primaryBorderColor: '#D4AF37',
        lineColor: '#D4AF37',
        background: '#0F0F1A',
        mainBkg: '#1A1A2E',
      },
      securityLevel: 'sandbox',
      maxTextSize: 50000,
    });

    const { svg } = await mermaid.render('viz-worker-' + requestId, code);

    self.postMessage({
      requestId,
      result: {
        html: `<div class="code-box-preview">${svg}</div>`,
        svg,
        errors: [],
        warnings: [],
        metrics: { renderTimeMs: 0, nodeCount: 0, edgeCount: 0, memoryUsedMB: 0, complexityScore: 0 },
        dna: options.dna || ''
      }
    });
  } catch (err: any) {
    self.postMessage({ requestId, error: err.message });
  }
};
```

### A-1.5 Canvas 离屏渲染（OffscreenCanvas）

```typescript
// ── OffscreenCanvas 渲染 ──
// 在 Worker 中直接渲染 Canvas，完全不阻塞主线程

async function renderToOffscreenCanvas(
  rendererId: RendererId,
  code: string,
  width: number,
  height: number
): Promise<ImageBitmap> {
  // 创建 OffscreenCanvas
  const canvas = new OffscreenCanvas(width, height);

  switch (rendererId) {
    case 'echarts': {
      // ECharts 在 Worker 中渲染
      const chart = echarts.init(canvas as any, EChartsRenderer.LONGHUN_THEME, {
        renderer: 'canvas',
        devicePixelRatio: 2
      });
      const option = JSON.parse(code);
      chart.setOption(option);
      // 返回 ImageBitmap（可传递到主线程）
      return canvas.transferToImageBitmap();
    }

    case 'threejs': {
      // Three.js 在 OffscreenCanvas 上渲染（WebGL上下文可用）
      const gl = canvas.getContext('webgl2');
      if (!gl) throw new Error('OffscreenCanvas WebGL2 not available');
      // ... Three.js 渲染逻辑
      return canvas.transferToImageBitmap();
    }

    default:
      throw new Error(`OffscreenCanvas not supported for ${rendererId}`);
  }
}

// 主线程接收 ImageBitmap
async function renderInWorker(rendererId: RendererId, code: string): Promise<void> {
  const worker = new Worker('./workers/canvas-renderer.worker.ts', { type: 'module' });

  worker.postMessage({
    rendererId,
    code,
    width: 800,
    height: 600
  });

  worker.onmessage = (e) => {
    const bitmap: ImageBitmap = e.data;
    const mainCanvas = document.querySelector('#viz-output') as HTMLCanvasElement;
    const ctx = mainCanvas.getContext('2d')!;
    ctx.drawImage(bitmap, 0, 0);
    bitmap.close(); // 释放资源
  };
}
```

### A-1.6 WebGL 上下文丢失恢复

```typescript
// ── WebGL 上下文丢失自动恢复 ──
// Three.js 3D场景专属

class WebGLContextRecovery {
  private renderer: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.Camera;
  private animationId: number = 0;
  private lost: boolean = false;

  constructor(container: HTMLElement) {
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: true
    });
    container.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);

    // 监听上下文丢失
    this.renderer.domElement.addEventListener('webglcontextlost', this.onContextLost.bind(this));
    this.renderer.domElement.addEventListener('webglcontextrestored', this.onContextRestored.bind(this));
  }

  private onContextLost(event: Event): void {
    event.preventDefault(); // 允许恢复
    this.lost = true;
    cancelAnimationFrame(this.animationId);

    // 显示降级UI
    this.showFallbackUI('WebGL上下文丢失，正在恢复...');

    console.warn('[Viz] WebGL context lost, preventing render loop');
  }

  private onContextRestored(): void {
    this.lost = false;

    // 重新上传所有纹理和几何体
    this.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        obj.material.needsUpdate = true;
        obj.geometry.attributes.position.needsUpdate = true;
      }
    });

    // 恢复渲染循环
    this.hideFallbackUI();
    this.startRenderLoop();
    console.log('[Viz] WebGL context restored');
  }

  private showFallbackUI(message: string): void {
    const el = document.createElement('div');
    el.className = 'viz-webgl-fallback';
    el.innerHTML = `<span>⚠️</span> ${message}`;
    el.style.cssText = `
      position: absolute; inset: 0;
      display: flex; align-items: center; justify-content: center;
      background: var(--longhun-dark); color: var(--longhun-gold);
      font-family: var(--longhun-font-ui); font-size: 14px;
      z-index: 10;
    `;
    this.renderer.domElement.parentElement?.appendChild(el);
  }

  private hideFallbackUI(): void {
    const el = document.querySelector('.viz-webgl-fallback');
    el?.remove();
  }

  private startRenderLoop(): void {
    const animate = () => {
      if (this.lost) return;
      this.renderer.render(this.scene, this.camera);
      this.animationId = requestAnimationFrame(animate);
    };
    animate();
  }
}
```

### A-1.7 性能监控指标

```typescript
// ── 性能监控收集器 ──
interface PerformanceMetrics {
  // 渲染指标
  firstRender: number;       // 首次渲染耗时(ms)
  interactiveTime: number;   // 可交互时间(ms)
  fps: number;              // 平均帧率
  fpsHistory: number[];     // FPS历史（最近60帧）

  // 资源指标
  memoryUsage: number;      // 内存占用(MB)
  jsHeapSize: number;       // JS堆大小(MB)
  networkRequests: number;  // 网络请求数
  transferSize: number;     // 传输大小(KB)

  // 用户体验指标
  cls: number;              // 累积布局偏移 (Cumulative Layout Shift)
  lcp: number;              // 最大内容绘制 (Largest Contentful Paint)
  fid: number;              // 首次输入延迟 (First Input Delay)
  inp: number;              // 交互到下次绘制 (Interaction to Next Paint)
  ttfb: number;             // 首字节时间 (Time to First Byte)
}

// 性能预算阈值
const PERFORMANCE_BUDGET = {
  // 必须达标（超限→红色审计）
  firstRender: 1000,        // 首次渲染 < 1s
  interactiveTime: 2000,    // 可交互 < 2s
  minFPS: 30,               // 最低帧率 30fps
  maxMemory: 150,           // 最大内存 150MB

  // 警告阈值（超限→黄色审计）
  warnFirstRender: 800,
  warnInteractiveTime: 1500,
  warnFPS: 45,
  warnMemory: 100,

  // 传输预算
  maxTransfer: 500,         // 最大传输 500KB
  warnTransfer: 300,

  // Core Web Vitals
  cls: 0.1,                 // 布局偏移 < 0.1
  lcp: 2500,                // 最大绘制 < 2.5s
  fid: 100,                 // 输入延迟 < 100ms
  inp: 200,                 // 交互延迟 < 200ms
  ttfb: 800,                // 首字节 < 800ms
};

// FPS 监控器
class FPSMonitor {
  private frames: number[] = [];
  private lastTime = performance.now();
  private running = false;

  start(): void {
    this.running = true;
    this.tick();
  }

  stop(): void {
    this.running = false;
  }

  private tick(): void {
    if (!this.running) return;

    const now = performance.now();
    const delta = now - this.lastTime;
    this.lastTime = now;

    const fps = 1000 / delta;
    this.frames.push(fps);
    if (this.frames.length > 60) this.frames.shift(); // 保留最近60帧

    requestAnimationFrame(() => this.tick());
  }

  getAverageFPS(): number {
    if (this.frames.length === 0) return 0;
    return this.frames.reduce((a, b) => a + b, 0) / this.frames.length;
  }

  getMinFPS(): number {
    return Math.min(...this.frames);
  }

  getFPSHistory(): number[] {
    return [...this.frames];
  }
}

// 内存监控器
class MemoryMonitor {
  getMemoryInfo(): { jsHeapSize: number; totalJSHeapSize: number; jsHeapSizeLimit: number } | null {
    if ('memory' in performance) {
      const mem = (performance as any).memory;
      return {
        jsHeapSize: mem.usedJSHeapSize / 1024 / 1024,
        totalJSHeapSize: mem.totalJSHeapSize / 1024 / 1024,
        jsHeapSizeLimit: mem.jsHeapSizeLimit / 1024 / 1024
      };
    }
    return null;
  }

  isMemoryWarning(): boolean {
    const mem = this.getMemoryInfo();
    if (!mem) return false;
    return mem.jsHeapSize > PERFORMANCE_BUDGET.warnMemory;
  }

  isMemoryCritical(): boolean {
    const mem = this.getMemoryInfo();
    if (!mem) return false;
    return mem.jsHeapSize > PERFORMANCE_BUDGET.maxMemory;
  }
}
```

### A-1.8 性能测试脚本

```bash
#!/bin/bash
# longhun-visual-perf-test.sh
# DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-PERF-TEST-v1.0

echo "🐉 龍魂可视化引擎 · 性能基准测试"
echo "================================"
echo ""

# 设备信息
echo "【测试设备】"
echo "  OS: $(uname -sm)"
echo "  CPU: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo '未知')"
echo "  Memory: $(sysctl -n hw.memsize 2>/dev/null | awk '{print $1/1024/1024/1024 "GB"}' || echo '未知')"
echo ""

# 1. Lighthouse 性能审计
echo "【1/5】Lighthouse 审计..."
lighthouse http://localhost:3000/visual-test \
  --output=json \
  --output-path=./perf-results/lighthouse.json \
  --chrome-flags="--headless --no-sandbox --disable-gpu" \
  --only-categories=performance \
  --quiet 2>/dev/null

if [ $? -eq 0 ]; then
  score=$(jq '.categories.performance.score' ./perf-results/lighthouse.json)
  echo "  ✅ Lighthouse Score: $(echo "$score * 100" | bc)%"
else
  echo "  ⚠️ Lighthouse 未安装，跳过"
fi
echo ""

# 2. 自定义渲染性能测试
echo "【2/5】渲染性能测试..."
node ./perf-tests/render-benchmark.js \
  --charts mindmap,flowchart,gantt,pie,line,scatter,3d,network \
  --sizes small,medium,large \
  --runs 3 \
  --output ./perf-results/render-benchmark.json
echo ""

# 3. FPS 测试
echo "【3/5】FPS 测试..."
node ./perf-tests/fps-counter.js \
  --chart-type mindmap \
  --node-count 50,200,1000 \
  --duration 10 \
  --output ./perf-results/fps-mindmap.json

node ./perf-tests/fps-counter.js \
  --chart-type network \
  --node-count 50,200,500 \
  --duration 10 \
  --output ./perf-results/fps-network.json
echo ""

# 4. 内存泄漏检测
echo "【4/5】内存泄漏检测..."
node ./perf-tests/memory-profiler.js \
  --charts all \
  --cycles 10 \
  --output ./perf-results/memory-profile.json
echo ""

# 5. 移动端测试
echo "【5/5】移动端适配测试..."
node ./perf-tests/mobile-viewport.js \
  --devices "iPhone 15 Pro,iPhone 13,小米14,红米Note,iPad Pro,华为Mate X5" \
  --charts mindmap,flowchart,3d,network \
  --output ./perf-results/mobile-test.json
echo ""

# 生成汇总报告
echo "================================"
echo "📊 生成性能报告..."
node ./perf-tests/generate-report.js \
  --input ./perf-results/ \
  --output ./perf-results/report.html \
  --template longhun-dark

echo ""
echo "✅ 性能测试完成"
echo "   报告: ./perf-results/report.html"
```

---

## 附录A-2 · 移动端适配

### A-2.1 设备分级（五级）

| 分级 | 设备 | 屏幕 | 芯片 | 适配策略 |
|:---:|------|:---|:---|:---|
| **M1** | 旗舰手机 | >6寸 / 120Hz LTPO | 骁龙8Gen3 / A17Pro / 天玑9300 | 全功能·高画质·3D全开 |
| **M2** | 中端手机 | 5.5-6寸 / 90Hz | 骁龙7Gen3 / A15 / 天玑8200 | 标准功能·中画质·3D简化 |
| **M3** | 入门手机 | <5.5寸 / 60Hz | 骁龙6系 / A13 / 天玑7000 | 简化功能·低画质·3D→PNG |
| **M4** | 平板 | >8寸 / 120Hz | 骁龙8Gen3 / M2 / 天玑9300 | 全功能·大屏优化·分屏优先 |
| **M5** | 折叠屏 | 展开>7寸 / 120Hz | 骁龙8Gen3 / 麒麟9000S | 自适应·双屏联动·悬停模式 |

### A-2.2 设备检测与分级

```typescript
// ── 设备能力检测 ──
interface DeviceCapability {
  tier: 'M1' | 'M2' | 'M3' | 'M4' | 'M5';
  screenWidth: number;
  screenHeight: number;
  pixelRatio: number;
  isFoldable: boolean;
  isTablet: boolean;
  webgl2Support: boolean;
  offscreenCanvasSupport: boolean;
  workerSupport: boolean;
  touchSupport: boolean;
  memoryGB?: number;
  cpuCores?: number;
}

function detectDeviceCapability(): DeviceCapability {
  const ua = navigator.userAgent;
  const screen = window.screen;
  const width = Math.min(screen.width, screen.height);
  const height = Math.max(screen.width, screen.height);
  const pixelRatio = window.devicePixelRatio || 1;

  // WebGL2检测
  const canvas = document.createElement('canvas');
  const webgl2 = !!canvas.getContext('webgl2');

  // OffscreenCanvas检测
  const offscreen = typeof OffscreenCanvas !== 'undefined';

  // Worker检测
  const worker = typeof Worker !== 'undefined';

  // 折叠屏检测
  const isFoldable = 'segments' in window || width / height > 1.5;

  // 平板判定：屏幕>7寸且非手机UA
  const isTablet = width > 768 && !/Mobile/.test(ua);

  // 芯片性能估算（通过navigator.hardwareConcurrency）
  const cpuCores = navigator.hardwareConcurrency || 4;

  // 内存估算（Chrome only）
  let memoryGB: number | undefined;
  if ('deviceMemory' in navigator) {
    memoryGB = (navigator as any).deviceMemory;
  }

  // 分级判定
  let tier: DeviceCapability['tier'];
  if (isTablet) {
    tier = 'M4';
  } else if (isFoldable) {
    tier = 'M5';
  } else if (pixelRatio >= 3 && cpuCores >= 8 && memoryGB && memoryGB >= 8) {
    tier = 'M1';
  } else if (pixelRatio >= 2 && cpuCores >= 6) {
    tier = 'M2';
  } else {
    tier = 'M3';
  }

  return {
    tier, screenWidth: width, screenHeight: height, pixelRatio,
    isFoldable, isTablet,
    webgl2Support: webgl2, offscreenCanvasSupport: offscreen, workerSupport: worker,
    touchSupport: 'ontouchstart' in window,
    memoryGB, cpuCores
  };
}

// 根据设备能力调整渲染配置
function getRenderConfigForDevice(cap: DeviceCapability): RenderOptions {
  switch (cap.tier) {
    case 'M1': case 'M4':
      return {
        theme: 'longhun-dark',
        interactive: true,
        animation: true,
        scale: 2,
        timeout: 10000
      };
    case 'M2': case 'M5':
      return {
        theme: 'longhun-dark',
        interactive: true,
        animation: cap.isFoldable, // 折叠屏展开时允许动画
        scale: 2,
        timeout: 8000
      };
    case 'M3':
      return {
        theme: 'longhun-dark',
        interactive: true,
        animation: false,
        scale: 1,
        timeout: 5000,
        // 3D自动降级为静态PNG
      };
  }
}
```

### A-2.3 响应式断点（完整版）

```css
/* ── 龍魂可视化引擎 · 移动端断点 v1.0 ── */

/* === M3 入门手机 (<=360px) === */
@media (max-width: 360px) {
  .viz-container { padding: 8px; }
  .viz-chart { min-height: 200px; }

  .code-box { border-radius: 4px; font-size: 12px; }
  .code-box-toolbar { padding: 4px 6px; gap: 2px; flex-wrap: wrap; }
  .code-box-btn { padding: 3px 6px; font-size: 11px; min-width: 40px; }
  .code-box-btn .btn-text { display: none; }        /* 只显示图标 */
  .code-box-btn .btn-shortcut { display: none; }    /* 隐藏快捷键 */
  .code-box-content { padding: 8px; max-height: 300px; }

  .code-box-split {
    grid-template-columns: 1fr;                     /* 单列 */
    grid-template-rows: auto auto;
  }

  .download-menu { right: auto; left: 0; min-width: 140px; }
  .download-menu__item { padding: 6px 12px; font-size: 12px; }

  /* 3D降级为占位提示 */
  .viz-3d-placeholder {
    display: flex;
  }
}

/* === M2 中端手机 (361-480px) === */
@media (min-width: 361px) and (max-width: 480px) {
  .viz-container { padding: 10px; }
  .viz-chart { min-height: 250px; }

  .code-box-btn { padding: 4px 8px; font-size: 12px; }
  .code-box-btn .btn-shortcut { display: none; }
  .code-box-content { max-height: 400px; }

  .code-box-split {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
}

/* === M1 旗舰手机 (481-768px) === */
@media (min-width: 481px) and (max-width: 768px) {
  .viz-container { padding: 14px; }
  .viz-chart { min-height: 300px; }

  .code-box-btn .btn-text { display: inline; }
  .code-box-btn .btn-shortcut { display: none; }

  .code-box-split {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;
  }
}

/* === M4 平板 / M5 折叠屏展开 (769-1024px) === */
@media (min-width: 769px) and (max-width: 1024px) {
  .viz-container { padding: 20px; }
  .viz-chart { min-height: 400px; }
  .viz-grid { grid-template-columns: 1fr 1fr; }
}

/* === 桌面 (1025px+) === */
@media (min-width: 1025px) {
  .viz-container {
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
  }
  .viz-chart { min-height: 500px; }
  .viz-grid { grid-template-columns: 1fr 1fr 1fr; }
}

/* === 折叠屏特殊适配 === */
@media (screen-fold-posture: laptop) {
  /* 华为Mate X5 悬停模式 */
  .viz-container {
    display: flex;
    flex-direction: row;
  }
  .viz-chart { flex: 1; }
  .viz-controls {
    width: 300px;
    flex-shrink: 0;
    border-left: 1px solid var(--longhun-border);
    padding-left: 16px;
  }
}

/* === 横屏优化 === */
@media (max-width: 768px) and (orientation: landscape) {
  .viz-container {
    display: flex;
    flex-direction: row;
  }
  .viz-sidebar {
    width: 180px;
    flex-shrink: 0;
    overflow-y: auto;
  }
  .viz-chart {
    flex: 1;
    min-height: auto;
  }
}

/* === 暗黑模式（龍魂默认） === */
@media (prefers-color-scheme: dark) {
  :root {
    --longhun-bg: #0F0F1A;
    --longhun-text: #E2E8F0;
  }
}

/* 亮色模式（用户主动切换） */
@media (prefers-color-scheme: light) {
  .viz-theme--light {
    --longhun-bg: #FAFAFA;
    --longhun-text: #1A1A2E;
    --longhun-dark: #F0F0F0;
    --longhun-surface: #FFFFFF;
    --longhun-border: #E0E0E0;
  }
}

/* === 高对比度（无障碍） === */
@media (prefers-contrast: high) {
  .viz-chart { border: 2px solid var(--longhun-gold); }
  .code-box { border-width: 2px; }
}

/* === 减少动画（省电/无障碍/ vestibular disorders） === */
@media (prefers-reduced-motion: reduce) {
  .viz-animation { animation: none !important; transition: none !important; }
  .viz-chart * { animation-duration: 0s !important; transition-duration: 0s !important; }
}
```

### A-2.4 触摸交互优化

```typescript
// ── 移动端触摸手势引擎 ──
interface TouchGestureConfig {
  pinchZoom: {
    enabled: boolean;
    minScale: number;
    maxScale: number;
    sensitivity: number;    // 1.0 = 默认
  };
  pan: {
    enabled: boolean;
    inertia: boolean;
    friction: number;       // 惯性摩擦系数
    boundary: 'clamp' | 'bounce' | 'none';
  };
  rotate: {
    enabled: boolean;       // 3D场景旋转
    axis: 'x' | 'y' | 'free';
    sensitivity: number;
  };
  doubleTap: {
    enabled: boolean;
    action: 'zoomIn' | 'resetZoom' | 'toggleFullscreen';
    maxDelay: number;       // 两次点击最大间隔(ms)
  };
  longPress: {
    enabled: boolean;
    duration: number;       // 触发长按所需时间(ms)
    action: 'showContextMenu' | 'startDrag' | 'select';
  };
  swipe: {
    enabled: boolean;
    threshold: number;      // 最小滑动距离(px)
    actions: {
      left?: () => void;
      right?: () => void;
      up?: () => void;
      down?: () => void;
    };
  };
}

class TouchGestureHandler {
  private config: TouchGestureConfig;
  private currentScale = 1;
  private currentTranslate = { x: 0, y: 0 };
  private currentRotation = { x: 0, y: 0 };

  // 惯性
  private velocity = { x: 0, y: 0 };
  private lastTouchTime = 0;
  private inertiaAnimationId = 0;

  // 双击检测
  private lastTapTime = 0;
  private lastTapPosition = { x: 0, y: 0 };
  private readonly DOUBLE_TAP_THRESHOLD = 30; // px

  // 长按
  private longPressTimer: number | null = null;

  constructor(config: Partial<TouchGestureConfig> = {}) {
    this.config = this.mergeConfig(config);
  }

  private mergeConfig(partial: Partial<TouchGestureConfig>): TouchGestureConfig {
    return {
      pinchZoom:   { enabled: true, minScale: 0.5, maxScale: 3, sensitivity: 1.2, ...partial.pinchZoom },
      pan:         { enabled: true, inertia: true, friction: 0.95, boundary: 'clamp', ...partial.pan },
      rotate:      { enabled: true, axis: 'free', sensitivity: 1.0, ...partial.rotate },
      doubleTap:   { enabled: true, action: 'resetZoom', maxDelay: 300, ...partial.doubleTap },
      longPress:   { enabled: true, duration: 500, action: 'showContextMenu', ...partial.longPress },
      swipe:       { enabled: true, threshold: 50, ...partial.swipe }
    };
  }

  onTouchStart(e: TouchEvent): void {
    const now = Date.now();

    // 双击检测
    if (e.touches.length === 1 && this.config.doubleTap.enabled) {
      const touch = e.touches[0];
      const dx = touch.clientX - this.lastTapPosition.x;
      const dy = touch.clientY - this.lastTapPosition.y;
      const dt = now - this.lastTapTime;

      if (Math.abs(dx) < this.DOUBLE_TAP_THRESHOLD &&
          Math.abs(dy) < this.DOUBLE_TAP_THRESHOLD &&
          dt < this.config.doubleTap.maxDelay) {
        this.handleDoubleTap();
        e.preventDefault();
        return;
      }
      this.lastTapTime = now;
      this.lastTapPosition = { x: touch.clientX, y: touch.clientY };
    }

    // 双指缩放/旋转
    if (e.touches.length === 2 && this.config.pinchZoom.enabled) {
      this.startDistance = this.getDistance(e.touches[0], e.touches[1]);
      this.startScale = this.currentScale;
      this.startRotation = this.getAngle(e.touches[0], e.touches[1]);
    }

    // 长按检测
    if (e.touches.length === 1 && this.config.longPress.enabled) {
      this.longPressTimer = window.setTimeout(() => {
        this.handleLongPress(e.touches[0]);
      }, this.config.longPress.duration);
    }

    // 惯性停止
    if (this.inertiaAnimationId) {
      cancelAnimationFrame(this.inertiaAnimationId);
      this.inertiaAnimationId = 0;
    }
  }

  private startDistance = 0;
  private startScale = 1;
  private startRotation = 0;
  private lastCenter = { x: 0, y: 0 };

  onTouchMove(e: TouchEvent): void {
    // 取消长按
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    if (e.touches.length === 2) {
      // 双指缩放
      if (this.config.pinchZoom.enabled) {
        const distance = this.getDistance(e.touches[0], e.touches[1]);
        const scale = (distance / this.startDistance) * this.startScale * this.config.pinchZoom.sensitivity;
        this.setScale(Math.max(this.config.pinchZoom.minScale,
                      Math.min(this.config.pinchZoom.maxScale, scale)));
      }

      // 双指旋转（3D场景）
      if (this.config.rotate.enabled) {
        const angle = this.getAngle(e.touches[0], e.touches[1]);
        const delta = angle - this.startRotation;
        this.applyRotation(delta * this.config.rotate.sensitivity);
      }
    }

    if (e.touches.length === 1 && this.config.pan.enabled) {
      const touch = e.touches[0];
      // 计算速度（用于惯性）
      const now = Date.now();
      const dt = now - this.lastTouchTime;
      if (dt > 0) {
        this.velocity.x = (touch.clientX - this.lastCenter.x) / dt;
        this.velocity.y = (touch.clientY - this.lastCenter.y) / dt;
      }
      this.lastTouchTime = now;
      this.lastCenter = { x: touch.clientX, y: touch.clientY };

      this.applyPan(touch.clientX - this.lastCenter.x, touch.clientY - this.lastCenter.y);
    }

    e.preventDefault();
  }

  onTouchEnd(e: TouchEvent): void {
    // 惯性动画
    if (this.config.pan.inertia && (Math.abs(this.velocity.x) > 0.1 || Math.abs(this.velocity.y) > 0.1)) {
      this.applyInertia();
    }

    // 滑动手势
    if (this.config.swipe.enabled && e.changedTouches.length === 1) {
      this.checkSwipe(e.changedTouches[0]);
    }
  }

  private applyInertia(): void {
    const animate = () => {
      this.velocity.x *= this.config.pan.friction;
      this.velocity.y *= this.config.pan.friction;

      if (Math.abs(this.velocity.x) < 0.01 && Math.abs(this.velocity.y) < 0.01) {
        this.velocity = { x: 0, y: 0 };
        return;
      }

      this.applyPan(this.velocity.x, this.velocity.y);
      this.inertiaAnimationId = requestAnimationFrame(animate);
    };
    this.inertiaAnimationId = requestAnimationFrame(animate);
  }

  private getDistance(a: Touch, b: Touch): number {
    return Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY);
  }

  private getAngle(a: Touch, b: Touch): number {
    return Math.atan2(b.clientY - a.clientY, b.clientX - a.clientX);
  }

  private setScale(scale: number): void { /* 实现缩放 */ }
  private applyRotation(delta: number): void { /* 实现旋转 */ }
  private applyPan(dx: number, dy: number): void { /* 实现平移 */ }
  private handleDoubleTap(): void { /* 双击处理 */ }
  private handleLongPress(touch: Touch): void { /* 长按处理 */ }
  private checkSwipe(touch: Touch): void { /* 滑动检测 */ }
}
```

### A-2.5 移动端功能降级矩阵

| 功能 | M1旗舰 | M2中端 | M3入门 | M4平板 | M5折叠 |
|:---|:---:|:---:|:---:|:---:|:---:|
| 思维导图 V01 | ✅全功能 | ✅全功能 | ⚠️简化节点 | ✅全功能 | ✅自适应 |
| 流程图 V02 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 时序图 V03 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 状态图 V04 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 甘特图 V05 | ✅全功能 | ✅全功能 | ⚠️简化任务 | ✅全功能 | ✅自适应 |
| 饼图 V06 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 折线图 V07 | ✅全功能 | ✅全功能 | ⚠️简化数据点 | ✅全功能 | ✅自适应 |
| 散点图 V08 | ✅全功能 | ⚠️减少点数 | ⚠️减少点数 | ✅全功能 | ✅自适应 |
| 雷达图 V09 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 热力图 V10 | ✅全功能 | ⚠️降低分辨率 | ⚠️降低分辨率 | ✅全功能 | ✅自适应 |
| 桑基图 V11 | ✅全功能 | ⚠️简化节点 | ❌静态图 | ✅全功能 | ✅自适应 |
| 树图 V12 | ✅全功能 | ✅全功能 | ⚠️折叠深层 | ✅全功能 | ✅自适应 |
| 网络关系图 V13 | ✅全功能 | ⚠️≤100节点 | ❌静态图 | ✅全功能 | ✅自适应 |
| **3D立体图 V14** | ✅WebGL全开 | ⚠️简化模型 | ❌静态PNG | ✅WebGL全开 | ✅自适应 |
| 地理地图 V15 | ✅全功能 | ⚠️简化图层 | ⚠️基础图层 | ✅全功能 | ✅自适应 |
| 词云 V16 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 仪表盘 V17 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| **动画时间轴 V18** | ✅全功能 | ⚠️减少帧数 | ❌静态图 | ✅全功能 | ✅自适应 |
| 实时协作 | ✅支持 | ✅支持 | ❌不支持 | ✅支持 | ✅支持 |
| 手势交互 | ✅全手势 | ✅基础手势 | ✅基础手势 | ✅全手势 | ✅全手势+悬停 |
| Web Worker渲染 | ✅ | ✅ | ⚠️降级主线程 | ✅ | ✅ |
| OffscreenCanvas | ✅ | ✅ | ❌不支持 | ✅ | ✅ |
| PWA离线 | ✅ | ✅ | ✅ | ✅ | ✅ |

### A-2.6 移动端代码框适配

```css
/* ── 移动端代码框专属样式 ── */
@media (max-width: 768px) {
  .code-box {
    border-radius: 4px;
    font-size: 13px;
    margin: 8px 0;
  }

  .code-box-toolbar {
    padding: 6px 8px;
    gap: 4px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;  /* 隐藏滚动条 */
  }

  .code-box-toolbar::-webkit-scrollbar { display: none; }

  .code-box-btn {
    padding: 3px 8px;
    font-size: 12px;
    min-width: 44px;       /* iOS最小触摸目标 */
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .code-box-btn .btn-icon { display: inline-block; }
  .code-box-btn .btn-text { display: none; }
  .code-box-btn .btn-shortcut { display: none; }

  .code-box-content {
    padding: 10px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    max-height: 50vh;       /* 不超过半屏 */
  }

  /* 预览模式 */
  .code-box-preview svg {
    max-width: 100%;
    height: auto;
    touch-action: manipulation; /* 禁用双击缩放 */
  }

  /* 下载按钮组 */
  .download-options {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    padding: 8px;
  }

  .download-btn {
    flex: 1;
    min-width: 60px;
    min-height: 44px;
    padding: 6px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
}

/* iOS Safari 特殊处理 */
@supports (-webkit-touch-callout: none) {
  .code-box-content {
    /* iOS Safari 滚动优化 */
    -webkit-overflow-scrolling: touch;
  }

  .code-box-btn {
    /* 防止iOS上的蓝色高亮 */
    -webkit-tap-highlight-color: transparent;
  }
}

/* 微信内置浏览器适配 */
@media screen and (max-width: 768px) {
  /* 微信浏览器特有的底部导航栏高度补偿 */
  .viz-toast {
    bottom: calc(24px + env(safe-area-inset-bottom));
  }

  .code-box--fullscreen {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
```

### A-2.7 离线支持（PWA）

```typescript
// ── Service Worker 离线缓存 ──
// sw.ts

const CACHE_NAME = 'longhun-visual-v1';
const RUNTIME_CACHE = 'longhun-visual-runtime';

// 静态资源（安装时预缓存）
const STATIC_ASSETS = [
  '/',
  '/visual-engine.css',
  '/visual-engine.js',
  '/code-box.js',
  '/themes/longhun-dark.css',
  '/fonts/LonghunFont-Regular.woff2',
  '/favicon.svg',
];

// 渲染器资源（按需缓存）
const RENDERER_ASSETS: Record<string, string[]> = {
  mermaid:  ['/renderers/mermaid.min.js'],
  echarts:  ['/renderers/echarts.min.js'],
  threejs:  ['/renderers/three.min.js', '/renderers/OrbitControls.js'],
  markmap:  ['/renderers/markmap-view.js', '/renderers/markmap-lib.js'],
  leaflet:  ['/renderers/leaflet.js', '/renderers/leaflet.css'],
  d3:       ['/renderers/d3.min.js'],
};

// 安装：预缓存核心静态资源
self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static assets...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => {
      return (self as any).skipWaiting();
    })
  );
});

// 激活：清理旧缓存
self.addEventListener('activate', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME && name !== RUNTIME_CACHE)
          .map(name => caches.delete(name))
      );
    }).then(() => {
      return (self as any).clients.claim();
    })
  );
});

// 请求拦截：缓存优先 + 网络回退
self.addEventListener('fetch', (event: FetchEvent) => {
  const { request } = event;
  const url = new URL(request.url);

  // API 请求：网络优先，缓存回退
  if (url.pathname.startsWith('/api/visual/')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // 渲染器资源：缓存优先
  if (url.pathname.includes('/renderers/')) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // 静态资源：缓存优先
  if (STATIC_ASSETS.some(a => url.pathname.endsWith(a))) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // 其他：网络优先
  event.respondWith(networkFirst(request));
});

// 缓存优先策略
async function cacheFirst(request: Request): Promise<Response> {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('Offline - Resource not available', { status: 503 });
  }
}

// 网络优先策略
async function networkFirst(request: Request): Promise<Response> {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || new Response('Offline', { status: 503 });
  }
}

// 离线提示
function showOfflineIndicator(): void {
  const indicator = document.createElement('div');
  indicator.className = 'viz-offline-indicator';
  indicator.innerHTML = '🌙 离线模式 · 部分功能受限 · 已启用本地缓存';
  indicator.style.cssText = `
    position: fixed; top: 0; left: 0; right: 0;
    background: var(--longhun-yellow); color: var(--longhun-dark);
    text-align: center; padding: 6px; z-index: 9999;
    font-family: var(--longhun-font-ui); font-size: 13px;
  `;
  document.body.prepend(indicator);

  // 5秒后自动消失
  setTimeout(() => indicator.remove(), 5000);
}

// 监听网络状态
window.addEventListener('online', () => {
  document.querySelector('.viz-offline-indicator')?.remove();
  console.log('[Viz] Back online');
});

window.addEventListener('offline', () => {
  showOfflineIndicator();
  console.log('[Viz] Offline mode');
});
```

### A-2.8 移动端测试矩阵

| 测试项 | iPhone 15 Pro | iPhone 13 | 小米14 | 红米Note | iPad Pro | 华为Mate X5 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **分级** | M1 | M1 | M1 | M3 | M4 | M5 |
| 首次渲染 | < 500ms | < 800ms | < 600ms | < 1.2s | < 400ms | < 600ms |
| 交互帧率 | 60fps | 60fps | 60fps | 30fps | 60fps | 60fps |
| 手势响应 | < 16ms | < 16ms | < 16ms | < 33ms | < 16ms | < 16ms |
| 内存占用 | < 50MB | < 80MB | < 60MB | < 100MB | < 80MB | < 70MB |
| Web Worker | ✅ | ✅ | ✅ | ⚠️降级 | ✅ | ✅ |
| OffscreenCanvas | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| WebGL2 | ✅ | ✅ | ✅ | ⚠️有限 | ✅ | ✅ |
| PWA离线 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 暗黑模式 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 折叠适配 | N/A | N/A | N/A | N/A | N/A | ✅悬停模式 |
| 微信内置浏览器 | ✅ | ✅ | ✅ | ✅ | N/A | ✅ |

---

## 附录A-3 · 一键测试命令

```bash
# 性能测试（全部图表·三档数据量）
npm run test:perf

# 移动端测试（六设备·关键图表）
npm run test:mobile

# Web Worker 测试
npm run test:workers

# PWA离线测试
npm run test:pwa

# 全量测试（性能+移动+Worker+PWA）
npm run test:visual -- --coverage --mobile --perf --workers --pwa

# 生成HTML报告
npm run report:visual

# 持续性能监控（CI/CD）
npm run test:visual:ci -- --threshold 90
```

---

> DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-ENGINE-APPENDIX-A-v1.0
> 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 性能等级: 5级降级 · Web Worker异步 · OffscreenCanvas · PWA离线 · 五设备分级
