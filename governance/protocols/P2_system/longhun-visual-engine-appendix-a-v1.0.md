# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂·可视化引擎协议 v1.0 · 附录A

> 性能基准测试 + 移动端适配
> DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·䷅讼-VISUAL-ENGINE-APPENDIX-A-v1.0

---

## 附录A-1 · 性能基准测试

### A-1.1 测试环境

```
基准设备: Apple M4 Max (用户设备)
浏览器: Chrome 126 / Safari 17 / Firefox 127
网络: 5G / WiFi-6 / 4G (三档)
测试工具: Lighthouse CI + WebPageTest + 自定义 FPS 计数器
```

### A-1.2 渲染性能基准

| 图表类型 | 节点/数据量 | 首次渲染 | 交互帧率 | 内存占用 | 目标 |
|:---|:---|:---:|:---:|:---:|:---:|
| **思维导图 V01** | 50节点 | < 500ms | 60fps | < 20MB | 🟢 |
| **思维导图 V01** | 200节点 | < 1.5s | 60fps | < 50MB | 🟢 |
| **思维导图 V01** | 1000节点 | < 3s | 30fps | < 100MB | 🟡 |
| **流程图 V02** | 20步骤 | < 300ms | 60fps | < 10MB | 🟢 |
| **流程图 V02** | 100步骤 | < 800ms | 60fps | < 30MB | 🟢 |
| **时序图 V03** | 10参与者 | < 400ms | 60fps | < 15MB | 🟢 |
| **时序图 V03** | 50参与者 | < 1.2s | 60fps | < 40MB | 🟢 |
| **甘特图 V05** | 30任务 | < 500ms | 60fps | < 20MB | 🟢 |
| **甘特图 V05** | 200任务 | < 2s | 60fps | < 60MB | 🟡 |
| **饼图 V06** | 10扇区 | < 200ms | 60fps | < 10MB | 🟢 |
| **折线图 V07** | 1000数据点 | < 300ms | 60fps | < 15MB | 🟢 |
| **折线图 V07** | 10000数据点 | < 800ms | 60fps | < 30MB | 🟢 |
| **散点图 V08** | 5000点 | < 500ms | 60fps | < 25MB | 🟢 |
| **散点图 V08** | 50000点 | < 2s | 30fps | < 80MB | 🟡 |
| **雷达图 V09** | 8维度 | < 300ms | 60fps | < 12MB | 🟢 |
| **热力图 V10** | 50x50网格 | < 400ms | 60fps | < 15MB | 🟢 |
| **热力图 V10** | 200x200网格 | < 1.5s | 60fps | < 50MB | 🟡 |
| **桑基图 V11** | 20节点 | < 500ms | 60fps | < 20MB | 🟢 |
| **树图 V12** | 100节点 | < 400ms | 60fps | < 15MB | 🟢 |
| **网络图 V13** | 50节点/100边 | < 600ms | 60fps | < 25MB | 🟢 |
| **网络图 V13** | 500节点/2000边 | < 3s | 30fps | < 120MB | 🟡 |
| **3D立体图 V14** | 简单模型 | < 1s | 60fps | < 50MB | 🟢 |
| **3D立体图 V14** | 复杂模型(1万面) | < 3s | 30fps | < 150MB | 🟡 |
| **地理地图 V15** | 中国省级 | < 800ms | 60fps | < 30MB | 🟢 |
| **地理地图 V15** | 全球县级 | < 2s | 30fps | < 80MB | 🟡 |
| **词云 V16** | 100词 | < 400ms | 60fps | < 15MB | 🟢 |
| **仪表盘 V17** | 6指标 | < 300ms | 60fps | < 12MB | 🟢 |
| **动画时间轴 V18** | 20帧 | < 500ms | 60fps | < 20MB | 🟢 |

### A-1.3 性能降级策略

```
检测到性能瓶颈时：
    │
    ├─ 帧率 < 30fps → 自动降级：
    │   ├─ 减少动画效果
    │   ├─ 降低渲染精度（3D模型减面）
    │   ├─ 启用虚拟滚动（大数据列表）
    │   └─ 降级为静态图片
    │
    ├─ 内存 > 100MB → 自动降级：
    │   ├─ 释放不可见区域内存
    │   ├─ 压缩纹理（3D场景）
    │   └─ 分页加载（大数据集）
    │
    ├─ 渲染 > 3s → 自动降级：
    │   ├─ 显示加载骨架屏
    │   ├─ 后台异步渲染
    │   ├─ 先显示简化版，再渐进细化
    │   └─ 最终降级：生成静态PNG替代交互SVG
    │
    └─ 网络慢(4G) → 自动降级：
        ├─ 压缩资源（WebP替代PNG）
        ├─ 延迟加载非首屏内容
        └─ 启用离线缓存
```

### A-1.4 性能监控指标

```typescript
interface PerformanceMetrics {
  // 渲染指标
  firstRender: number;      // 首次渲染耗时(ms)
  interactiveTime: number;  // 可交互时间(ms)
  fps: number;             // 平均帧率

  // 资源指标
  memoryUsage: number;     // 内存占用(MB)
  networkRequests: number; // 网络请求数
  transferSize: number;    // 传输大小(KB)

  // 用户体验指标
  cls: number;             // 累积布局偏移
  lcp: number;             // 最大内容绘制(ms)
  fid: number;             // 首次输入延迟(ms)
}

// 性能阈值
const PERFORMANCE_BUDGET = {
  firstRender: 1000,       // 首次渲染 < 1s
  interactiveTime: 2000,   // 可交互 < 2s
  minFPS: 30,              // 最低帧率 30fps
  maxMemory: 100,          // 最大内存 100MB
  maxTransfer: 500,        // 最大传输 500KB
  cls: 0.1,                // 布局偏移 < 0.1
  lcp: 2500,               // 最大绘制 < 2.5s
  fid: 100,                // 输入延迟 < 100ms
};
```

### A-1.5 性能测试脚本

```bash
#!/bin/bash
# longhun-visual-perf-test.sh
# 性能基准测试

echo "🐉 龍魂可视化引擎 · 性能基准测试"
echo "================================"

# 测试设备信息
echo "设备: $(uname -m)"
echo "浏览器: $(chrome --version 2>/dev/null || echo '未知')"

# 运行 Lighthouse
lighthouse http://localhost:3000/visual-test   --output=json   --output-path=./perf-results/lighthouse.json   --chrome-flags="--headless --no-sandbox"

# 运行 WebPageTest
wpt test http://localhost:3000/visual-test   --location "Dulles:Chrome"   --runs 3   --output ./perf-results/wpt.json

# 自定义 FPS 测试
node ./perf-tests/fps-counter.js   --chart-type mindmap   --node-count 50,200,1000   --output ./perf-results/fps-mindmap.json

# 生成报告
echo "================================"
echo "报告生成: ./perf-results/report.html"
```

---

## 附录A-2 · 移动端适配

### A-2.1 设备分级

| 分级 | 设备 | 屏幕 | 性能 | 适配策略 |
|:---:|------|:---|:---|:---|
| **M1** | 旗舰手机 | >6寸 / >120Hz | 骁龍8Gen3/A17Pro | 全功能·高画质 |
| **M2** | 中端手机 | 5.5-6寸 / 90Hz | 骁龍7Gen3/A15 | 标准功能·中画质 |
| **M3** | 入门手机 | <5.5寸 / 60Hz | 骁龍6系/A13 | 简化功能·低画质 |
| **M4** | 平板 | >8寸 / 120Hz | 骁龍8Gen3/M2 | 全功能·大屏优化 |
| **M5** | 折叠屏 | 展开>7寸 | 骁龍8Gen3 | 自适应布局 |

### A-2.2 响应式断点

```css
/* 龍魂可视化引擎 · 移动端断点 */

/* M3 入门手机 */
@media (max-width: 360px) {
  .viz-container { padding: 8px; }
  .viz-chart { min-height: 200px; }
  .code-box-toolbar { flex-wrap: wrap; }
  .code-box-btn { padding: 4px 8px; font-size: 12px; }
}

/* M2 中端手机 */
@media (min-width: 361px) and (max-width: 480px) {
  .viz-container { padding: 12px; }
  .viz-chart { min-height: 250px; }
}

/* M1 旗舰手机 */
@media (min-width: 481px) and (max-width: 768px) {
  .viz-container { padding: 16px; }
  .viz-chart { min-height: 300px; }
}

/* M4 平板 / M5 折叠屏展开 */
@media (min-width: 769px) and (max-width: 1024px) {
  .viz-container { padding: 20px; }
  .viz-chart { min-height: 400px; }
  .viz-grid { grid-template-columns: 1fr 1fr; }
}

/* 桌面 */
@media (min-width: 1025px) {
  .viz-container { padding: 24px; max-width: 1200px; margin: 0 auto; }
  .viz-chart { min-height: 500px; }
  .viz-grid { grid-template-columns: 1fr 1fr 1fr; }
}

/* 暗黑模式（龍魂默认） */
@media (prefers-color-scheme: dark) {
  :root {
    --longhun-bg: #0F0F1A;
    --longhun-text: #E2E8F0;
  }
}

/* 高对比度 */
@media (prefers-contrast: high) {
  .viz-chart { border: 2px solid var(--longhun-gold); }
}

/* 减少动画（省电/无障碍） */
@media (prefers-reduced-motion: reduce) {
  .viz-animation { animation: none !important; transition: none !important; }
}
```

### A-2.3 触摸交互优化

```typescript
// 移动端触摸手势
interface TouchGestures {
  // 缩放
  pinchZoom: {
    enabled: true,
    minScale: 0.5,
    maxScale: 3,
    sensitivity: 1.2,
  };

  // 平移
  pan: {
    enabled: true,
    inertia: true,      // 惯性滑动
    boundary: 'clamp',  // 边界限制
  };

  // 旋转（3D场景）
  rotate: {
    enabled: true,
    axis: 'y',          // Y轴旋转
  };

  // 双击
  doubleTap: {
    enabled: true,
    action: 'resetZoom', // 重置缩放
  };

  // 长按
  longPress: {
    enabled: true,
    duration: 500,      // 500ms触发
    action: 'showContextMenu',
  };
}

// 手势识别实现
class TouchGestureHandler {
  private startDistance: number = 0;
  private startScale: number = 1;
  private lastTouch: Touch | null = null;

  onTouchStart(e: TouchEvent) {
    if (e.touches.length === 2) {
      // 双指缩放开始
      this.startDistance = this.getDistance(e.touches[0], e.touches[1]);
      this.startScale = this.currentScale;
    }
  }

  onTouchMove(e: TouchEvent) {
    if (e.touches.length === 2) {
      // 双指缩放中
      const distance = this.getDistance(e.touches[0], e.touches[1]);
      const scale = (distance / this.startDistance) * this.startScale;
      this.setScale(Math.max(0.5, Math.min(3, scale)));
    }
  }

  onTouchEnd(e: TouchEvent) {
    // 手势结束，应用惯性
    if (this.velocity > 0.1) {
      this.applyInertia();
    }
  }
}
```

### A-2.4 移动端功能降级

| 功能 | M1旗舰 | M2中端 | M3入门 | M4平板 | M5折叠 |
|:---|:---:|:---:|:---:|:---:|:---:|
| 思维导图 V01 | ✅全功能 | ✅全功能 | ⚠️简化节点 | ✅全功能 | ✅自适应 |
| 流程图 V02 | ✅全功能 | ✅全功能 | ✅全功能 | ✅全功能 | ✅自适应 |
| 3D立体图 V14 | ✅WebGL | ⚠️简化模型 | ❌静态PNG | ✅WebGL | ✅自适应 |
| 动画时间轴 V18 | ✅全功能 | ⚠️减少帧数 | ❌静态图 | ✅全功能 | ✅自适应 |
| 网络关系图 V13 | ✅全功能 | ⚠️减少节点 | ❌静态图 | ✅全功能 | ✅自适应 |
| 地理地图 V15 | ✅全功能 | ⚠️简化图层 | ⚠️基础图层 | ✅全功能 | ✅自适应 |
| 实时协作 | ✅支持 | ✅支持 | ❌不支持 | ✅支持 | ✅支持 |
| 手势交互 | ✅全手势 | ✅基础手势 | ✅基础手势 | ✅全手势 | ✅全手势 |

### A-2.5 移动端代码框适配

```css
/* 移动端代码框 */
@media (max-width: 768px) {
  .code-box {
    border-radius: 4px;
    font-size: 13px;
  }

  .code-box-toolbar {
    padding: 6px 8px;
    gap: 4px;
  }

  .code-box-btn {
    padding: 3px 8px;
    font-size: 12px;
    min-width: 60px;
  }

  .code-box-btn .btn-icon {
    display: inline-block;  /* 显示图标 */
  }

  .code-box-btn .btn-text {
    display: none;  /* 隐藏文字，省空间 */
  }

  .code-box-content {
    padding: 10px;
    overflow-x: auto;  /* 横向滚动 */
    -webkit-overflow-scrolling: touch;  /* 惯性滚动 */
  }

  /* 预览模式优化 */
  .code-box-preview svg {
    max-width: 100%;
    height: auto;
    touch-action: pan-y;  /* 允许垂直滚动 */
  }

  /* 下载按钮 */
  .download-options {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }

  .download-btn {
    flex: 1;
    min-width: 80px;
    padding: 6px;
    font-size: 12px;
  }
}

/* 横屏优化 */
@media (max-width: 768px) and (orientation: landscape) {
  .viz-container {
    display: flex;
    flex-direction: row;
  }

  .viz-sidebar {
    width: 200px;
    flex-shrink: 0;
  }

  .viz-chart {
    flex: 1;
    min-height: auto;
  }
}
```

### A-2.6 离线支持（PWA）

```typescript
// Service Worker 离线缓存
const CACHE_NAME = 'longhun-visual-v1';
const STATIC_ASSETS = [
  '/visual-engine.css',
  '/visual-engine.js',
  '/renderers/mermaid.min.js',
  '/renderers/echarts.min.js',
  '/themes/longhun-dark.css',
  '/fonts/LonghunFont-Regular.otf',
];

// 安装时缓存静态资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
});

// 运行时缓存图表数据
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/visual/')) {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request).then((fetchResponse) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      })
    );
  }
});

// 离线提示
function showOfflineToast() {
  if (!navigator.onLine) {
    toast('🌙 离线模式：部分功能受限，已启用本地缓存');
  }
}
```

### A-2.7 移动端测试矩阵

| 测试项 | iPhone 15 Pro | iPhone 13 | 小米14 | 红米Note | iPad Pro | 华为Mate X5 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 首次渲染 | < 500ms | < 800ms | < 600ms | < 1.2s | < 400ms | < 600ms |
| 交互帧率 | 60fps | 60fps | 60fps | 30fps | 60fps | 60fps |
| 手势响应 | < 16ms | < 16ms | < 16ms | < 33ms | < 16ms | < 16ms |
| 内存占用 | < 50MB | < 80MB | < 60MB | < 100MB | < 80MB | < 70MB |
| 离线可用 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 暗黑模式 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 折叠适配 | N/A | N/A | N/A | N/A | N/A | ✅ |

---

## 附录A-3 · 一键测试命令

```bash
# 性能测试
npm run test:perf

# 移动端测试
npm run test:mobile

# 全量测试
npm run test:visual -- --coverage --mobile --perf

# 生成报告
npm run report:visual
```

---

> DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·䷅讼-VISUAL-ENGINE-APPENDIX-A-v1.0
> 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
