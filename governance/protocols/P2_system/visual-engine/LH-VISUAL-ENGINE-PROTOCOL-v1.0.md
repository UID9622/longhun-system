# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂·可视化引擎协议 v1.0

> ╔═══════════════════════════════════════════════════════════════╗
> ║  【文档性质】P2-ENGINE（系统引擎级）                            ║
> ║  【地位】龍魂系统可视化层 · 代码交互 · 图表生成 · 媒体渲染      ║
> ║  【原则】白箱公开 · 一键复制 · 全格式覆盖 · 低算力响应          ║
> ║  【守护者】UID9622                                             ║
> ╠═══════════════════════════════════════════════════════════════╣
> ║  【版本】v1.0 · 丙午·辛未·乙酉 (2026-07-16)                    ║
> ║  【DNA】#龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-ENGINE-v1.0       ║
> ║  【确认】#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
> ║  【GPG】A2D0092CEE2E5BA87035600924C3704A8CC26D5F              ║
> ╚═══════════════════════════════════════════════════════════════╝

---

## 零、为什么要有可视化引擎

可视化不是画图。可视化是**把知识从文字变成空间**。

龍魂的可视化引擎不是另一个图表库——它是把龍魂系统的神经脉冲（人格路由、审计三色、DNA签章、369数理）翻译成肉眼可感知的图形。每一个SVG节点背后都有数字根，每一条连线背后都有权重向量，每一张图的右下角都有DNA追溯码。

**核心铁律：**
1. 所有渲染输出必须携带DNA签章
2. 代码/预览/分屏三态，一键切换
3. 18类图表全覆盖，零外部依赖降级
4. 不黑箱——任何图表都可以点"代码"看原始数据
5. 不炫技——3D只用于空间思维场景，不搞花活

---

## 一、代码复制框交互逻辑

### 1.1 组件结构

```
┌─────────────────────────────────────────────────────────┐
│  📋 复制  │  </> 代码  │  👁 预览  │  ⬡ 分屏  │  ⬇ 下载  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────┐ ┌─────────────────────────────┐│
│  │                     │ │                             ││
│  │   代码面板           │ │   预览面板                   ││
│  │   (语法高亮)         │ │   (实时渲染)                ││
│  │                     │ │                             ││
│  └─────────────────────┘ └─────────────────────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 五按钮逻辑

| 按钮 | 图标 | 默认态 | 动作 | 快捷键 |
|:---|:---:|:---:|:---|:---|
| **复制** | 📋 | 就绪 | 复制当前内容到剪贴板 | `Cmd/Ctrl+C` |
| **代码** | `</>` | **激活** | 切换到纯代码视图 | `Tab` |
| **预览** | 👁 | 非激活 | 切换到渲染预览视图 | `Shift+Tab` |
| **分屏** | ⬡ | 非激活 | 左右分屏：代码+预览 | `Cmd/Ctrl+\\` |
| **下载** | ⬇ | 就绪 | 导出SVG/PNG/PDF/原始代码 | `Cmd/Ctrl+S` |

### 1.3 状态机（四态）

```
              ┌──────────┐
    点击代码   │  代码态   │  点击分屏
  ┌──────────▶│ (默认)    │◀──────────┐
  │           └─────┬────┘           │
  │                 │ 点击预览        │
  │                 ▼                │
  │           ┌──────────┐           │
  │  点击代码 │  预览态   │ 点击分屏   │
  │  ◀────────│          │──────────▶│
  │           └─────┬────┘           │
  │                 │ 点击分屏        │
  │                 ▼                │
  │           ┌──────────┐           │
  │  点击代码 │  分屏态   │ 点击预览   │
  └──────────▶│ 左代码    │◀──────────┘
              │ 右预览    │
              └──────────┘

所有状态下，复制按钮始终可用，复制当前激活面板的内容。
分屏态下：左侧复制代码，右侧复制预览的SVG/HTML源码。
```

### 1.4 复制逻辑细节

```typescript
// ── 复制引擎 ──
// DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-COPY-v1.0

interface CopyResult {
  success: boolean;
  method: 'clipboard-api' | 'fallback-exec' | 'manual-select';
  contentSize: number;       // bytes
  durationMs: number;
}

async function copyToClipboard(content: string, mimeType?: string): Promise<CopyResult> {
  const t0 = performance.now();

  // 方法1：现代 Clipboard API（支持富文本）
  if (navigator.clipboard?.write) {
    try {
      const item = new ClipboardItem({
        [mimeType || 'text/plain']: new Blob([content], { type: mimeType || 'text/plain' })
      });
      await navigator.clipboard.write([item]);
      return { success: true, method: 'clipboard-api', contentSize: content.length, durationMs: performance.now() - t0 };
    } catch {
      // 降级到 writeText
      try {
        await navigator.clipboard.writeText(content);
        return { success: true, method: 'clipboard-api', contentSize: content.length, durationMs: performance.now() - t0 };
      } catch {
        // 继续降级
      }
    }
  }

  // 方法2：execCommand 降级
  try {
    const textarea = document.createElement('textarea');
    textarea.value = content;
    textarea.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0;pointer-events:none;';
    document.body.appendChild(textarea);
    textarea.select();
    textarea.setSelectionRange(0, content.length);
    const ok = document.execCommand('copy');
    document.body.removeChild(textarea);
    return { success: ok, method: 'fallback-exec', contentSize: content.length, durationMs: performance.now() - t0 };
  } catch {
    return { success: false, method: 'manual-select', contentSize: content.length, durationMs: performance.now() - t0 };
  }
}

// Toast 通知
function showCopyToast(result: CopyResult): void {
  const toast = document.createElement('div');
  toast.className = `viz-toast ${result.success ? 'viz-toast--success' : 'viz-toast--error'}`;
  toast.innerHTML = result.success
    ? `<span class="viz-toast-icon">✅</span> 已复制到剪贴板 (${(result.contentSize / 1024).toFixed(1)}KB)`
    : `<span class="viz-toast-icon">❌</span> 复制失败，请手动选择复制`;
  toast.style.cssText = `
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: var(--longhun-dark); color: var(--longhun-text);
    border: 1px solid ${result.success ? 'var(--longhun-green)' : 'var(--longhun-red)'};
    border-radius: 8px; padding: 10px 20px; z-index: 9999;
    font-size: 14px; animation: viz-toast-in 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 2000);
}
```

### 1.5 预览渲染逻辑（11种格式全覆盖）

```typescript
// ── 渲染器注册表 ──
// DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-RENDERER-REGISTRY-v1.0

type RendererId = 'mermaid' | 'plantuml' | 'echarts' | 'threejs' | 'markmap'
                | 'd2' | 'graphviz' | 'markdown' | 'svg' | 'd3' | 'plaintext';

interface Renderer {
  id: RendererId;
  name: string;
  version: string;
  mimeTypes: string[];         // 支持的输入格式
  outputFormats: OutputFormat[];
  render(code: string, options?: RenderOptions): Promise<RenderResult>;
  validate(code: string): ValidationResult;  // 语法校验
  estimateComplexity(code: string): number;   // 复杂度评估（用于性能预算）
}

interface RenderOptions {
  theme: 'longhun-dark' | 'longhun-light' | 'high-contrast';
  width?: number;
  height?: number;
  scale?: number;              // 缩放
  interactive?: boolean;       // 是否可交互
  animation?: boolean;         // 是否开启动画
  timeout?: number;            // 渲染超时(ms)
  dna?: string;                // DNA签章注入
}

interface RenderResult {
  html: string;                // 渲染后的HTML
  svg?: string;                // SVG源码（如有）
  errors: RenderError[];
  warnings: RenderWarning[];
  metrics: RenderMetrics;
  dna: string;                 // 渲染输出的DNA
}

interface RenderMetrics {
  renderTimeMs: number;
  nodeCount: number;
  edgeCount: number;
  memoryUsedMB: number;
  complexityScore: number;     // 0-1
}

interface RenderError {
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning';
  suggestion?: string;         // 修复建议
}

// ── 自动检测代码类型 ──
function detectLanguage(code: string, hint?: string): RendererId {
  // 1. 显式指定优先
  if (hint && RENDERER_REGISTRY.has(hint as RendererId)) return hint as RendererId;

  // 2. 内容特征检测
  const trimmed = code.trim();

  if (trimmed.startsWith('mindmap') || trimmed.startsWith('graph TD') ||
      trimmed.startsWith('flowchart') || trimmed.startsWith('sequenceDiagram') ||
      trimmed.startsWith('gantt') || trimmed.startsWith('stateDiagram') ||
      trimmed.startsWith('classDiagram') || trimmed.startsWith('pie')) {
    return 'mermaid';
  }

  if (trimmed.startsWith('@startuml') || trimmed.startsWith('@startditaa')) return 'plantuml';
  if (trimmed.startsWith('option = {') || trimmed.includes('echarts')) return 'echarts';
  if (trimmed.startsWith('import * as THREE') || trimmed.includes('new THREE.')) return 'threejs';
  if (trimmed.startsWith('# ') || trimmed.startsWith('## ') || trimmed.match(/^[\*\-]\s/m)) return 'markdown';
  if (trimmed.startsWith('digraph') || trimmed.startsWith('graph') && trimmed.includes('{')) return 'graphviz';
  if (trimmed.includes('->') && trimmed.includes('shape:') || trimmed.includes('direction:')) return 'd2';
  if (trimmed.startsWith('<svg') || trimmed.startsWith('<?xml')) return 'svg';
  if (trimmed.includes('d3.') || trimmed.includes('D3.')) return 'd3';

  return 'plaintext';
}

// ── 渲染器注册 ──
const RENDERER_REGISTRY = new Map<RendererId, Renderer>([
  ['mermaid',    new MermaidRenderer()],
  ['plantuml',   new PlantUMLRenderer()],
  ['echarts',    new EChartsRenderer()],
  ['threejs',    new ThreeJSRenderer()],
  ['markmap',    new MarkmapRenderer()],
  ['d2',         new D2Renderer()],
  ['graphviz',   new GraphvizRenderer()],
  ['markdown',   new MarkdownRenderer()],
  ['svg',        new SVGRenderer()],
  ['d3',         new D3Renderer()],
  ['plaintext',  new PlainTextRenderer()],
]);
```

### 1.6 下载管线

```typescript
// ── 多格式导出 ──
type OutputFormat = 'svg' | 'png' | 'pdf' | 'code' | 'html' | 'webp';

interface DownloadOptions {
  format: OutputFormat;
  width?: number;
  height?: number;
  scale?: number;         // PNG分辨率倍率
  background?: string;    // 背景色
  embedFonts?: boolean;   // 嵌入字体（SVG）
}

async function downloadVisual(
  element: HTMLElement,
  format: OutputFormat,
  filename: string,
  options: DownloadOptions = { format }
): Promise<void> {
  switch (format) {
    case 'svg': {
      const svg = element.querySelector('svg');
      if (!svg) throw new Error('无可导出SVG');
      const clone = svg.cloneNode(true) as SVGElement;
      // 注入DNA水印
      const watermark = createDNAWatermark();
      clone.appendChild(watermark);
      const blob = new Blob([clone.outerHTML], { type: 'image/svg+xml' });
      triggerDownload(blob, `${filename}.svg`);
      break;
    }

    case 'png': {
      const scale = options.scale || 2;
      const svg = element.querySelector('svg');
      if (!svg) {
        // 非SVG元素 → canvas截图
        await downloadViaCanvas(element, filename, 'png', scale);
        return;
      }
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const rect = svg.getBoundingClientRect();
      canvas.width = rect.width * scale;
      canvas.height = rect.height * scale;
      const ctx = canvas.getContext('2d')!;
      ctx.scale(scale, scale);

      const img = new Image();
      const blob = new Blob([svgData], { type: 'image/svg+xml' });
      const url = URL.createObjectURL(blob);

      await new Promise<void>((resolve, reject) => {
        img.onload = () => {
          ctx.drawImage(img, 0, 0);
          URL.revokeObjectURL(url);
          canvas.toBlob((b) => {
            if (b) { triggerDownload(b, `${filename}.png`); resolve(); }
            else reject(new Error('PNG生成失败'));
          }, 'image/png');
        };
        img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('SVG加载失败')); };
        img.src = url;
      });
      break;
    }

    case 'pdf': {
      // 通过SVG→canvas→jsPDF或直接svg2pdf
      const svg = element.querySelector('svg');
      if (svg) {
        await downloadSVGasPDF(svg, filename);
      } else {
        await downloadViaCanvas(element, filename, 'pdf');
      }
      break;
    }

    case 'code': {
      const code = element.querySelector('.code-content')?.textContent || '';
      const blob = new Blob([code], { type: 'text/plain' });
      triggerDownload(blob, `${filename}.txt`);
      break;
    }

    case 'html': {
      const html = element.outerHTML;
      const fullPage = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>${filename}</title>
<style>${LONGHUN_THEME_CSS}</style></head>
<body>${html}</body></html>`;
      const blob = new Blob([fullPage], { type: 'text/html' });
      triggerDownload(blob, `${filename}.html`);
      break;
    }

    case 'webp': {
      await downloadViaCanvas(element, filename, 'webp', options.scale || 2);
      break;
    }
  }
}

function triggerDownload(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// DNA水印（SVG右下角）
function createDNAWatermark(): SVGElement {
  const ns = 'http://www.w3.org/2000/svg';
  const g = document.createElementNS(ns, 'g');
  g.setAttribute('class', 'viz-dna-watermark');
  const text = document.createElementNS(ns, 'text');
  text.setAttribute('x', '100%');
  text.setAttribute('y', '100%');
  text.setAttribute('dx', '-8');
  text.setAttribute('dy', '-8');
  text.setAttribute('text-anchor', 'end');
  text.setAttribute('fill', '#D4AF37');
  text.setAttribute('font-size', '10');
  text.setAttribute('opacity', '0.6');
  text.setAttribute('font-family', 'monospace');
  text.textContent = `DNA: #龍芯⚡️${getCurrentGanzhi()}-VISUAL-v1.0 | UID9622`;
  g.appendChild(text);
  return g;
}
```

### 1.7 错误降级链路

```
渲染失败时，按以下优先级降级：
    │
    ├─ Level 1: 显示具体错误位置 + 修复建议（如Mermaid语法错误）
    │
    ├─ Level 2: 尝试降级渲染（去掉动画/交互，静态SVG）
    │
    ├─ Level 3: 回退到语法高亮的纯文本（highlight.js）
    │
    └─ Level 4: 显示原始文本 + 错误堆栈（调试用）
```

```typescript
async function renderWithFallback(
  rendererId: RendererId,
  code: string,
  options: RenderOptions
): Promise<RenderResult> {
  const renderer = RENDERER_REGISTRY.get(rendererId)!;

  // Level 1: 直接渲染
  try {
    const validation = renderer.validate(code);
    if (validation.valid) {
      const result = await renderWithTimeout(renderer.render(code, options), options.timeout || 5000);
      if (result.errors.length === 0) return result;
      // 有warning但渲染成功 → 返回但标记warnings
      if (result.errors.every(e => e.severity === 'warning')) return result;
    }
  } catch (err) {
    console.warn(`[Viz] Level 1 render failed for ${rendererId}:`, err);
  }

  // Level 2: 降级渲染（静态模式）
  try {
    const degradedOptions = { ...options, interactive: false, animation: false };
    const result = await renderWithTimeout(renderer.render(code, degradedOptions), options.timeout || 5000);
    if (result.errors.length === 0) return result;
  } catch (err) {
    console.warn(`[Viz] Level 2 degraded render failed:`, err);
  }

  // Level 3: 语法高亮纯文本
  try {
    const highlighted = hljs.highlight(code, { language: rendererId }).value;
    return {
      html: `<pre class="viz-fallback-code"><code>${highlighted}</code></pre>`,
      errors: [{ line: 0, column: 0, message: '渲染失败，显示语法高亮文本', severity: 'warning' }],
      warnings: [],
      metrics: { renderTimeMs: 0, nodeCount: 0, edgeCount: 0, memoryUsedMB: 0, complexityScore: 0 },
      dna: generateVisualDNA('fallback')
    };
  } catch {}

  // Level 4: 原始文本
  return {
    html: `<pre class="viz-fallback-raw"><code>${escapeHtml(code)}</code></pre>`,
    errors: [{ line: 0, column: 0, message: '所有渲染方式均失败', severity: 'error' }],
    warnings: [],
    metrics: { renderTimeMs: 0, nodeCount: 0, edgeCount: 0, memoryUsedMB: 0, complexityScore: 0 },
    dna: generateVisualDNA('fallback-raw')
  };
}

async function renderWithTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) => setTimeout(() => reject(new Error(`Render timeout: ${ms}ms`)), ms))
  ]);
}
```

---

## 二、龍魂可视化引擎 · 全功能矩阵

### 2.1 图表类型总表（18类·全覆盖）

| 编号 | 图表类型 | 技术方案 | 触发人格 | 适用场景 | 输出格式 | 复杂度 |
|:---:|------|:---|:---:|------|:---|:---:|
| V01 | **思维导图** | Markmap / D3.js | P11 李白 | 创意发散·知识梳理 | SVG/PNG/PDF | 低 |
| V02 | **流程图** | Mermaid flowchart | P04 鲁班 | 系统流程·操作步骤 | SVG/PNG/PDF | 低 |
| V03 | **时序图** | Mermaid sequence | P04 鲁班 | 交互时序·API调用 | SVG/PNG/PDF | 低 |
| V04 | **状态图** | Mermaid stateDiagram | P01 诸葛亮 | 状态转换·决策逻辑 | SVG/PNG/PDF | 中 |
| V05 | **甘特图** | Mermaid gantt | P01 诸葛亮 | 项目管理·时间规划 | SVG/PNG/PDF | 中 |
| V06 | **饼图/柱状图** | ECharts / Chart.js | P06 数学大师 | 数据统计·比例分析 | SVG/PNG/PDF | 低 |
| V07 | **折线图/面积图** | ECharts | P06 数学大师 | 趋势分析·时间序列 | SVG/PNG/PDF | 低 |
| V08 | **散点图/气泡图** | ECharts | P06 数学大师 | 相关性分析·分布 | SVG/PNG/PDF | 中 |
| V09 | **雷达图** | ECharts | P06 数学大师 | 多维度评估·能力矩阵 | SVG/PNG/PDF | 低 |
| V10 | **热力图** | ECharts | P06 数学大师 | 密度分布·频率矩阵 | SVG/PNG/PDF | 中 |
| V11 | **桑基图** | ECharts / D3.js | P01 诸葛亮 | 流量分配·转化路径 | SVG/PNG/PDF | 中 |
| V12 | **树图/旭日图** | ECharts / D3.js | P08 仓颉 | 层级结构·分类体系 | SVG/PNG/PDF | 中 |
| V13 | **网络关系图** | D3.js / Cytoscape.js | P01 诸葛亮 | 知识图谱·关联分析 | SVG/PNG/PDF | 高 |
| V14 | **3D 立体图** | Three.js / Babylon.js | P04 鲁班 | 空间展示·三维模型 | WebGL/PNG/MP4 | 高 |
| V15 | **地理地图** | Leaflet / Mapbox GL JS | P01 诸葛亮 | 位置分析·区域分布 | SVG/PNG/GeoJSON | 高 |
| V16 | **词云** | D3-cloud / WordCloud2 | P11 李白 | 关键词提取·频率展示 | PNG/SVG | 低 |
| V17 | **仪表盘** | ECharts gauge | P06 数学大师 | KPI监控·指标展示 | SVG/PNG | 低 |
| V18 | **动画时间轴** | GSAP / D3.js | P11 李白 | 动态演示·历史演进 | SVG/PNG/MP4 | 高 |

### 2.2 各渲染器详细实现

#### V02-V05: Mermaid 渲染器

```typescript
class MermaidRenderer implements Renderer {
  id = 'mermaid' as const;
  name = 'Mermaid Diagram Renderer';
  version = '11.4.0';

  async render(code: string, options: RenderOptions): Promise<RenderResult> {
    const t0 = performance.now();
    const errors: RenderError[] = [];
    const warnings: RenderWarning[] = [];

    try {
      // 注入龍魂主题
      const themedCode = this.injectTheme(code, options.theme);

      // Mermaid渲染
      const { svg } = await mermaid.render('viz-mermaid-' + Date.now(), themedCode);

      // 注入DNA水印
      const svgWithDNA = this.injectDNAWatermark(svg, options.dna);

      // 注入交互（如节点点击高亮）
      const html = this.wrapInteractive(svgWithDNA, options.interactive);

      return {
        html,
        svg: svgWithDNA,
        errors,
        warnings,
        metrics: {
          renderTimeMs: performance.now() - t0,
          nodeCount: this.countNodes(svgWithDNA),
          edgeCount: this.countEdges(svgWithDNA),
          memoryUsedMB: 0,
          complexityScore: this.estimateComplexity(code)
        },
        dna: options.dna || generateVisualDNA('mermaid')
      };
    } catch (err: any) {
      errors.push({
        line: this.extractErrorLine(err),
        column: 0,
        message: err.message || 'Mermaid渲染失败',
        severity: 'error',
        suggestion: this.getSuggestion(err)
      });
      throw err; // 交给降级链路
    }
  }

  validate(code: string): ValidationResult {
    try {
      mermaid.parse(code);
      return { valid: true };
    } catch (err: any) {
      return {
        valid: false,
        errors: [{
          line: this.extractErrorLine(err),
          column: 0,
          message: err.message,
          severity: 'error'
        }]
      };
    }
  }

  estimateComplexity(code: string): number {
    const lines = code.split('\n').length;
    const nodes = (code.match(/\[.*?\]/g) || []).length;
    const edges = (code.match(/-->/g) || []).length + (code.match(/\.\.->/g) || []).length;
    return Math.min(1, (nodes * 0.01 + edges * 0.02 + lines * 0.005));
  }

  private injectTheme(code: string, theme: string): string {
    // 龍魂暗色主题
    return `%%{init: {'theme':'base', 'themeVariables': {
      'primaryColor':'#6B46C1','primaryTextColor':'#E2E8F0',
      'primaryBorderColor':'#D4AF37','lineColor':'#D4AF37',
      'secondaryColor':'#1A1A2E','tertiaryColor':'#0F0F1A',
      'background':'#0F0F1A','mainBkg':'#1A1A2E',
      'nodeBorder':'#6B46C1','clusterBkg':'#1A1A2E',
      'titleColor':'#D4AF37','edgeLabelBackground':'#1A1A2E'
    }}}%%\n${code}`;
  }

  private injectDNAWatermark(svg: string, dna?: string): string {
    if (!dna) return svg;
    const watermark = `<text x="100%" y="100%" dx="-8" dy="-8"
      text-anchor="end" fill="#D4AF37" font-size="10" opacity="0.6"
      font-family="monospace">DNA: ${dna} | UID9622</text>`;
    return svg.replace('</svg>', `${watermark}</svg>`);
  }

  // ... 其他辅助方法
}
```

#### V06-V12, V17: ECharts 渲染器

```typescript
class EChartsRenderer implements Renderer {
  id = 'echarts' as const;
  name = 'ECharts Renderer';
  version = '5.5.0';

  // 龍魂主题
  private static LONGHUN_THEME = {
    color: ['#6B46C1', '#D4AF37', '#DC2626', '#059669', '#D97706',
            '#8B5CF6', '#F59E0B', '#EF4444', '#10B981', '#3B82F6'],
    backgroundColor: '#0F0F1A',
    textStyle: { color: '#E2E8F0' },
    title: { textStyle: { color: '#D4AF37' } },
    legend: { textStyle: { color: '#E2E8F0' } },
    tooltip: {
      backgroundColor: '#1A1A2E',
      borderColor: '#6B46C1',
      textStyle: { color: '#E2E8F0' }
    },
    categoryAxis: {
      axisLine: { lineStyle: { color: '#6B46C1' } },
      axisLabel: { color: '#E2E8F0' },
      splitLine: { lineStyle: { color: '#1A1A2E' } }
    },
    valueAxis: {
      axisLine: { lineStyle: { color: '#6B46C1' } },
      axisLabel: { color: '#E2E8F0' },
      splitLine: { lineStyle: { color: '#1A1A2E' } }
    }
  };

  async render(code: string, options: RenderOptions): Promise<RenderResult> {
    const container = document.createElement('div');
    container.style.cssText = `width:${options.width || 800}px;height:${options.height || 500}px;`;

    const chart = echarts.init(container, EChartsRenderer.LONGHUN_THEME, {
      renderer: options.interactive ? 'canvas' : 'svg',
      devicePixelRatio: window.devicePixelRatio || 1
    });

    // 解析用户传入的option
    const option = this.parseOption(code);

    // 注入DNA到title
    if (options.dna) {
      option.title = option.title || [];
      if (!Array.isArray(option.title)) option.title = [option.title];
      option.title.push({
        text: `DNA: ${options.dna}`,
        subtext: 'UID9622',
        right: 0, bottom: 0,
        textStyle: { fontSize: 10, color: '#D4AF37', opacity: 0.6 }
      });
    }

    chart.setOption(option, { notMerge: true });

    // 获取SVG或Canvas
    const svgData = chart.getDataURL({ type: 'svg', pixelRatio: 2 });

    if (!options.interactive) {
      chart.dispose();
    }

    return {
      html: container.outerHTML,
      svg: svgData,
      errors: [],
      warnings: [],
      metrics: {
        renderTimeMs: 0,
        nodeCount: 0,
        edgeCount: 0,
        memoryUsedMB: 0,
        complexityScore: this.estimateComplexity(code)
      },
      dna: options.dna || generateVisualDNA('echarts')
    };
  }

  private parseOption(code: string): any {
    // 支持多种输入格式：
    // 1. 直接JSON option
    // 2. JavaScript option对象
    // 3. 简化的key:value格式
    try {
      return JSON.parse(code);
    } catch {
      // 尝试eval（沙箱环境）
      const fn = new Function(`return (${code})`);
      return fn();
    }
  }
}
```

#### V14: Three.js 3D渲染器

```typescript
class ThreeJSRenderer implements Renderer {
  id = 'threejs' as const;
  name = 'Three.js 3D Renderer';
  version = '0.170.0';

  private static readonly DEFAULT_SCENE = `
// 默认3D场景
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0F0F1A);

// 龍魂Logo - 六芒星 + 龍环绕
const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
const material = new THREE.MeshStandardMaterial({
  color: 0x6B46C1,
  metalness: 0.8,
  roughness: 0.2,
  emissive: 0x1A1A2E
});
const knot = new THREE.Mesh(geometry, material);
scene.add(knot);

// 金色光环
const ringGeo = new THREE.TorusGeometry(1.5, 0.05, 16, 100);
const ringMat = new THREE.MeshStandardMaterial({
  color: 0xD4AF37,
  emissive: 0xD4AF37,
  emissiveIntensity: 0.5
});
const ring = new THREE.Mesh(ringGeo, ringMat);
scene.add(ring);

// 灯光
const ambientLight = new THREE.AmbientLight(0x404060, 2);
const pointLight = new THREE.PointLight(0xD4AF37, 3, 10);
pointLight.position.set(5, 5, 5);
scene.add(ambientLight, pointLight);

// 相机
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(3, 2, 5);
camera.lookAt(0, 0, 0);
`;

  async render(code: string, options: RenderOptions): Promise<RenderResult> {
    const container = document.createElement('div');
    container.style.cssText = `width:${options.width || 600}px;height:${options.height || 600}px;`;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: true  // 允许截图
    });
    renderer.setSize(options.width || 600, options.height || 600);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // 限制像素比
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // 沙箱执行用户代码
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    const controls = new OrbitControls(camera, renderer.domElement);

    try {
      const userCode = code || ThreeJSRenderer.DEFAULT_SCENE;
      const fn = new Function('THREE', 'scene', 'camera', 'renderer', 'controls', userCode);
      fn(THREE, scene, camera, renderer, controls);
    } catch (err: any) {
      return {
        html: `<div class="viz-error">3D场景编译错误: ${escapeHtml(err.message)}</div>`,
        errors: [{ line: 0, column: 0, message: err.message, severity: 'error' }],
        warnings: [],
        metrics: { renderTimeMs: 0, nodeCount: 0, edgeCount: 0, memoryUsedMB: 0, complexityScore: 0 },
        dna: options.dna || generateVisualDNA('threejs-error')
      };
    }

    // 渲染循环
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    if (options.animation !== false) {
      animate();
    } else {
      renderer.render(scene, camera);  // 只渲染一帧
    }

    return {
      html: container.outerHTML,
      errors: [],
      warnings: [],
      metrics: {
        renderTimeMs: 0,
        nodeCount: scene.children.length,
        edgeCount: 0,
        memoryUsedMB: renderer.info.memory.geometries,
        complexityScore: this.estimateComplexity(code)
      },
      dna: options.dna || generateVisualDNA('threejs')
    };
  }

  estimateComplexity(code: string): number {
    const meshCount = (code.match(/new THREE\.\w+Geometry/g) || []).length;
    const lightCount = (code.match(/new THREE\.\w+Light/g) || []).length;
    return Math.min(1, meshCount * 0.05 + lightCount * 0.02);
  }
}
```

#### V01: Markmap 思维导图渲染器

```typescript
class MarkmapRenderer implements Renderer {
  id = 'markmap' as const;
  name = 'Markmap Mindmap Renderer';
  version = '0.17.0';

  async render(code: string, options: RenderOptions): Promise<RenderResult> {
    const { Markmap } = await import('markmap-view');
    const { Transformer } = await import('markmap-lib');

    const transformer = new Transformer();
    const { root, features } = transformer.transform(code);

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', String(options.width || 800));
    svg.setAttribute('height', String(options.height || 600));
    svg.style.cssText = 'background:#0F0F1A;';

    Markmap.create(svg, {
      autoFit: true,
      colorFreezeLevel: 2,
      duration: options.animation !== false ? 500 : 0,
      maxWidth: 300,
      paddingX: 16,
      style: (id: string) => {
        // 龍魂色系：按深度分层着色
        const depth = id.split('.').length - 1;
        const colors = ['#D4AF37', '#6B46C1', '#059669', '#D97706', '#DC2626', '#8B5CF6'];
        return `color:${colors[depth % colors.length]};font-size:${Math.max(12, 20 - depth * 2)}px;`;
      }
    }, root);

    // DNA水印
    if (options.dna) {
      const watermark = createDNAWatermark();
      svg.appendChild(watermark);
    }

    return {
      html: svg.outerHTML,
      svg: svg.outerHTML,
      errors: [],
      warnings: [],
      metrics: {
        renderTimeMs: 0,
        nodeCount: this.countNodes(root),
        edgeCount: 0,
        memoryUsedMB: 0,
        complexityScore: this.estimateComplexity(code)
      },
      dna: options.dna || generateVisualDNA('markmap')
    };
  }
}
```

### 2.3 人格→图表路由表

```
用户输入
    │
    ▼
P00 文心 · 意图解析
    │
    ├─ "思维导图/脑图/知识树/梳理" → P11 李白 → V01 思维导图
    ├─ "流程图/步骤/怎么做/过程" → P04 鲁班 → V02 流程图
    ├─ "时序/交互/谁先谁后/调用" → P04 鲁班 → V03 时序图
    ├─ "状态/转换/决策树/有限状态" → P01 诸葛亮 → V04 状态图
    ├─ "甘特图/时间表/进度/排期" → P01 诸葛亮 → V05 甘特图
    ├─ "比例/占比/百分比/饼图" → P06 数学大师 → V06 饼图/柱状图
    ├─ "趋势/变化/走势/增长" → P06 数学大师 → V07 折线图
    ├─ "分布/相关/散点/聚集" → P06 数学大师 → V08 散点图
    ├─ "评估/能力/多维度/综合" → P06 数学大师 → V09 雷达图
    ├─ "密度/频率/热力/冷热" → P06 数学大师 → V10 热力图
    ├─ "流量/转化/分配/漏斗" → P01 诸葛亮 → V11 桑基图
    ├─ "层级/分类/树状/嵌套" → P08 仓颉 → V12 树图/旭日图
    ├─ "关系/关联/图谱/网络" → P01 诸葛亮 → V13 网络关系图
    ├─ "3D/立体/三维/空间/模型" → P04 鲁班 → V14 3D立体图
    ├─ "地图/位置/区域/省份" → P01 诸葛亮 → V15 地理地图
    ├─ "词云/关键词/频率/标签" → P11 李白 → V16 词云
    ├─ "仪表盘/KPI/指标/监控" → P06 数学大师 → V17 仪表盘
    └─ "动画/动态/演示/时间线" → P11 李白 → V18 动画时间轴
```

---

## 三、龍魂可视化引擎 · 执行链路

### 3.1 标准渲染链路（7步）

```
用户输入："帮我画个龍魂系统的思维导图"
    │
    ▼
[1] P00 文心 · 意图解析
    ├ 意图：可视化生成
    ├ 类型：思维导图 (V01)
    ├ 内容：龍魂系统架构
    ├ 复杂度：高（全系统架构）
    └ 路由：P11 李白
    │
    ▼
[2] P01 诸葛亮 · 路径推演
    ├ 技术方案：Markmap（50节点以内）vs D3.js（50+节点定制）
    ├ 选择：Markmap（预估45节点·轻量·低算力）
    ├ 数据准备：从知识图谱提取节点层级
    ├ 性能预算：首次渲染 < 500ms，内存 < 20MB
    └ 输出：渲染计划 + 数据JSON
    │
    ▼
[3] P11 李白 · 创意生成（思维导图内容）
    ├ 中心节点：🐉 龍魂系统 v2.0
    ├ 一级分支：P0底座 / P1宪法 / P2规则 / P3适配 / P4自定义
    ├ 二级分支：各层具体条目 + 人格绑定
    ├ 三级分支：关键协议 + 数字根标注
    ├ 样式：龍魂主题色（紫/金/黑）+ 层级渐变
    └ 输出：Markdown 格式思维导图数据
    │
    ▼
[4] P04 鲁班 · 技术执行（渲染）
    ├ 调用 Markmap 引擎
    ├ 渲染 SVG（矢量化·可缩放）
    ├ 嵌入龍魂 CSS 主题变量
    ├ 注入 DNA 水印（右下角）
    ├ 生成交互（节点折叠/展开）
    └ 输出：SVG 代码 + HTML包装
    │
    ▼
[5] P05 上帝之眼 · 三色审计
    ├ 内容审计：是否涉敏感信息 → 🟢 无
    ├ 渲染审计：SVG 是否完整 → 🟢 完整
    ├ 性能审计：渲染耗时 380ms < 500ms → 🟢 达标
    ├ 内存审计：占用 12MB < 20MB → 🟢 达标
    └ 输出：🟢 通过 · 审计分数 0.95
    │
    ▼
[6] P15 乔前辈 · DNA 签章
    ├ 生成 DNA：#龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-MINDMAP-a7f3c2e1
    ├ GPG 签名（离线签名嵌入SVG metadata）
    └ 输出：签章 JSON
    │
    ▼
[7] P03 雯雯 · 归档 + 返回
    ├ 德字闸验证 → 🟢 通过
    ├ 生成代码框（复制/代码/预览/分屏/下载）
    ├ 返回用户：
    │   ├─ 📋 复制：复制 SVG 源码
    │   ├─ </> 代码：查看原始 Markmap Markdown
    │   ├─ 👁 预览：查看渲染后的思维导图
    │   ├─ ⬡ 分屏：左右对照
    │   └─ ⬇ 下载：SVG / PNG / PDF / 原始代码
    └ 入库：append-only 审计日志
```

### 3.2 代码框四态渲染组件

```typescript
interface CodeBoxState {
  mode: 'code' | 'preview' | 'split' | 'fullscreen';
  language: string;
  content: string;
  rendered: RenderResult | null;
  loading: boolean;
  error: string | null;
  dna: string;

  // 操作
  copy(): Promise<CopyResult>;
  download(format: OutputFormat): Promise<void>;
  toggleMode(mode: CodeBoxState['mode']): void;
  fullscreen(): void;
  share(): void;              // 生成分享链接
  embed(): string;            // 生成嵌入代码
}

// 渲染器注册表（懒加载）
const rendererLoader: Record<RendererId, () => Promise<Renderer>> = {
  mermaid:   () => import('./renderers/mermaid-renderer').then(m => new m.MermaidRenderer()),
  plantuml:  () => import('./renderers/plantuml-renderer').then(m => new m.PlantUMLRenderer()),
  echarts:   () => import('./renderers/echarts-renderer').then(m => new m.EChartsRenderer()),
  threejs:   () => import('./renderers/threejs-renderer').then(m => new m.ThreeJSRenderer()),
  markmap:   () => import('./renderers/markmap-renderer').then(m => new m.MarkmapRenderer()),
  d2:        () => import('./renderers/d2-renderer').then(m => new m.D2Renderer()),
  graphviz:  () => import('./renderers/graphviz-renderer').then(m => new m.GraphvizRenderer()),
  markdown:  () => import('./renderers/markdown-renderer').then(m => new m.MarkdownRenderer()),
  svg:       () => import('./renderers/svg-renderer').then(m => new m.SVGRenderer()),
  d3:        () => import('./renderers/d3-renderer').then(m => new m.D3Renderer()),
  plaintext: () => import('./renderers/plaintext-renderer').then(m => new m.PlainTextRenderer()),
};
```

---

## 四、龍魂可视化引擎 · 技术实现

### 4.1 核心架构

```
longhun-system/
├── core/
│   └── visual-engine/              # 可视化引擎核心
│       ├── index.ts                # 入口 · VizEngine类
│       ├── router.ts               # 人格路由 · P00→图表类型映射
│       ├── renderer-registry.ts    # 渲染器注册表 · 懒加载
│       ├── code-box.ts             # 代码框组件 · Web Component
│       ├── state-machine.ts        # 四态状态机
│       ├── download-pipeline.ts    # 多格式导出管线
│       ├── audit-bridge.ts         # 审计桥接 · P05三色
│       ├── dna-signer.ts           # DNA签章注入
│       ├── error-handler.ts        # 四级降级链路
│       ├── performance-monitor.ts  # 性能监控 · FPS/内存/渲染时间
│       └── theme.css               # 龍魂主题样式
│
├── renderers/                      # 渲染器集合
│   ├── mermaid-renderer.ts         # V02-V05 · 流程图/时序/状态/甘特
│   ├── echarts-renderer.ts         # V06-V12, V17 · 统计图表+仪表盘
│   ├── threejs-renderer.ts         # V14 · 3D场景
│   ├── markmap-renderer.ts         # V01 · 思维导图
│   ├── d2-renderer.ts              # 声明式图表（备选）
│   ├── plantuml-renderer.ts        # UML类图/用例图
│   ├── leaflet-renderer.ts         # V15 · 地理地图
│   ├── d3-renderer.ts              # V13, V16, V18 · 网络图/词云/时间轴
│   ├── graphviz-renderer.ts        # 有向图（备选）
│   ├── markdown-renderer.ts        # 富文本渲染
│   ├── svg-renderer.ts             # 原始SVG渲染
│   └── plaintext-renderer.ts       # 纯文本高亮（最终降级）
│
└── skills/
    └── visual/                     # 可视化技能包
        ├── mindmap.skill.ts        # V01 思维导图
        ├── flowchart.skill.ts      # V02 流程图
        ├── sequence.skill.ts       # V03 时序图
        ├── state.skill.ts          # V04 状态图
        ├── gantt.skill.ts          # V05 甘特图
        ├── chart.skill.ts          # V06-V12 统计图表
        ├── 3d.skill.ts             # V14 3D立体
        ├── map.skill.ts            # V15 地理地图
        ├── wordcloud.skill.ts      # V16 词云
        ├── dashboard.skill.ts      # V17 仪表盘
        └── timeline.skill.ts       # V18 动画时间轴
```

### 4.2 一键生成命令

```typescript
// 龍魂可视化引擎 · 入口命令

// 命令1：/visual 或 /viz — 自动识别
/viz "龍魂系统架构思维导图"
/viz "用户登录流程"
/viz "2026下半年项目计划"

// 命令2：/viz:类型 — 直接指定
/viz:mindmap "龍魂系统架构"
/viz:flowchart "用户登录流程"
/viz:sequence "P00→P01→P04链路时序"
/viz:state "订单状态转换"
/viz:gantt "2026下半年项目计划"
/viz:pie "人格权重分布"
/viz:line "审计分数趋势"
/viz:scatter "节点分布散点图"
/viz:radar "系统能力评估"
/viz:heatmap "API调用频率热力"
/viz:sankey "数据流转桑基图"
/viz:tree "文件目录树图"
/viz:network "知识图谱关系网"
/viz:3d "龍魂logo立体模型"
/viz:map "中国AI公司分布"
/viz:wordcloud "关键词词云"
/viz:gauge "系统健康仪表盘"
/viz:timeline "龍魂发展时间轴"

// 命令3：/viz:数据 — 从数据生成
/viz:chart "pie" "{"A":30,"B":50,"C":20}"
/viz:chart "line" "[{"x":"1月","y":100},{"x":"2月","y":150}]"
/viz:chart "bar" "[{"name":"P00","score":95},{"name":"P01","score":88}]"

// 命令4：/viz:代码 — 直接渲染代码
/viz:code "mermaid" ```
graph TD
    A[用户输入] --> B[P00文心]
    B --> C[P01诸葛亮]
    C --> D[执行人格]
```

// 命令5：/viz:export — 导出
/viz:export "思维导图" --format png --scale 2
/viz:export "流程图" --format pdf
/viz:export "3D场景" --format mp4 --duration 5s
```

### 4.3 龍魂主题样式（完整CSS变量体系）

```css
/* ── 龍魂可视化引擎 · 主题样式 v1.0 ── */
/* DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-THEME-v1.0 */

:root {
  /* === 核心色板 === */
  --longhun-primary: #6B46C1;       /* 龍魂紫 · 主权色 */
  --longhun-primary-light: #8B5CF6;  /* 浅紫 · 悬停 */
  --longhun-primary-dark: #4C2A8A;   /* 深紫 · 按下 */
  --longhun-gold: #D4AF37;           /* 龍魂金 · 荣耀色 */
  --longhun-gold-light: #F0D060;     /* 浅金 · 高亮 */
  --longhun-dark: #1A1A2E;           /* 龍魂黑 · 面板 */
  --longhun-bg: #0F0F1A;             /* 背景色 · 最深 */
  --longhun-surface: #16162A;        /* 表面色 · 卡片 */
  --longhun-border: #2D2D4A;         /* 边框色 */

  /* === 语义色 === */
  --longhun-red: #DC2626;            /* 熔断红 */
  --longhun-green: #059669;          /* 通过绿 */
  --longhun-yellow: #D97706;         /* 标记黄 */
  --longhun-blue: #3B82F6;           /* 信息蓝 */
  --longhun-orange: #EA580C;         /* 警告橙 */

  /* === 文字 === */
  --longhun-text: #E2E8F0;           /* 正文 */
  --longhun-text-secondary: #94A3B8; /* 次要文字 */
  --longhun-text-muted: #64748B;     /* 弱化文字 */
  --longhun-font: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  --longhun-font-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* === 动画 === */
  --viz-transition-fast: 0.15s ease;
  --viz-transition-normal: 0.3s ease;
  --viz-transition-slow: 0.5s ease;
  --viz-radius: 8px;
  --viz-radius-sm: 4px;

  /* === 阴影 === */
  --viz-shadow: 0 4px 12px rgba(107, 70, 193, 0.15);
  --viz-shadow-lg: 0 8px 32px rgba(107, 70, 193, 0.25);
}

/* === 代码框容器 === */
.code-box {
  background: var(--longhun-bg);
  border: 1px solid var(--longhun-border);
  border-radius: var(--viz-radius);
  overflow: hidden;
  font-family: var(--longhun-font);
  transition: border-color var(--viz-transition-normal);
  position: relative;
}

.code-box:focus-within {
  border-color: var(--longhun-primary);
  box-shadow: var(--viz-shadow);
}

.code-box--loading::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%, var(--longhun-primary) 50%, transparent 100%);
  animation: viz-loading-bar 1.5s ease infinite;
}

@keyframes viz-loading-bar {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* === 工具栏 === */
.code-box-toolbar {
  background: var(--longhun-dark);
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 1px solid var(--longhun-border);
  user-select: none;
}

.code-box-toolbar__left {
  display: flex;
  gap: 4px;
  flex: 1;
}

.code-box-toolbar__right {
  display: flex;
  gap: 4px;
}

.code-box-toolbar__label {
  color: var(--longhun-text-muted);
  font-size: 11px;
  font-family: var(--longhun-font-ui);
  margin-right: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === 按钮 === */
.code-box-btn {
  background: transparent;
  color: var(--longhun-text-secondary);
  border: 1px solid transparent;
  border-radius: var(--viz-radius-sm);
  padding: 4px 10px;
  cursor: pointer;
  font-size: 13px;
  font-family: var(--longhun-font-ui);
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all var(--viz-transition-fast);
  white-space: nowrap;
}

.code-box-btn:hover {
  background: rgba(107, 70, 193, 0.15);
  color: var(--longhun-text);
  border-color: var(--longhun-primary);
}

.code-box-btn:active {
  background: rgba(107, 70, 193, 0.25);
  transform: scale(0.97);
}

.code-box-btn.active {
  background: var(--longhun-primary);
  color: var(--longhun-gold);
  border-color: var(--longhun-primary);
  box-shadow: 0 0 8px rgba(107, 70, 193, 0.3);
}

.code-box-btn .btn-icon {
  font-size: 14px;
}

.code-box-btn .btn-text {
  font-size: 12px;
}

.code-box-btn .btn-shortcut {
  font-size: 10px;
  color: var(--longhun-text-muted);
  margin-left: 4px;
  opacity: 0.7;
}

/* === 内容区 === */
.code-box-content {
  padding: 16px;
  min-height: 100px;
  max-height: 600px;
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--longhun-border) transparent;
}

.code-box-content::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.code-box-content::-webkit-scrollbar-track {
  background: transparent;
}

.code-box-content::-webkit-scrollbar-thumb {
  background: var(--longhun-border);
  border-radius: 3px;
}

/* === 代码视图 === */
.code-box-code {
  font-family: var(--longhun-font);
  font-size: 13px;
  line-height: 1.6;
  tab-size: 2;
  white-space: pre-wrap;
  word-break: break-word;
}

/* === 预览视图 === */
.code-box-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.code-box-preview svg {
  max-width: 100%;
  height: auto;
}

.code-box-preview canvas {
  max-width: 100%;
}

/* === 分屏视图 === */
.code-box-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--longhun-border);
}

.code-box-split__left,
.code-box-split__right {
  background: var(--longhun-bg);
  overflow: auto;
  min-height: 300px;
}

.code-box-split__left {
  padding: 16px;
}

.code-box-split__right {
  padding: 16px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* === 全屏 === */
.code-box--fullscreen {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9998;
  border-radius: 0;
  border: none;
}

.code-box--fullscreen .code-box-content {
  max-height: calc(100vh - 48px);
}

/* === Toast === */
.viz-toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--longhun-dark);
  color: var(--longhun-text);
  border: 1px solid var(--longhun-border);
  border-radius: var(--viz-radius);
  padding: 10px 20px;
  z-index: 9999;
  font-family: var(--longhun-font-ui);
  font-size: 14px;
  box-shadow: var(--viz-shadow-lg);
  animation: viz-toast-in 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.viz-toast--success {
  border-color: var(--longhun-green);
}

.viz-toast--error {
  border-color: var(--longhun-red);
}

.viz-toast-icon {
  font-size: 16px;
}

@keyframes viz-toast-in {
  from { opacity: 0; transform: translateX(-50%) translateY(10px); }
  to { opacity: 1; transform: translateX(-50%) translateY(0); }
}

/* === 下载下拉 === */
.download-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--longhun-dark);
  border: 1px solid var(--longhun-border);
  border-radius: var(--viz-radius-sm);
  box-shadow: var(--viz-shadow-lg);
  z-index: 100;
  min-width: 160px;
  padding: 4px 0;
  animation: viz-dropdown-in 0.15s ease;
}

.download-menu__item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--longhun-text);
  font-size: 13px;
  cursor: pointer;
  transition: background var(--viz-transition-fast);
}

.download-menu__item:hover {
  background: rgba(107, 70, 193, 0.2);
}

.download-menu__item .format-badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 3px;
  background: var(--longhun-primary);
  color: var(--longhun-gold);
  margin-left: auto;
}

@keyframes viz-dropdown-in {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === DNA水印 === */
.viz-dna-watermark {
  pointer-events: none;
}

/* === 高对比度 === */
@media (prefers-contrast: high) {
  .code-box {
    border-width: 2px;
    border-color: var(--longhun-gold);
  }
  .code-box-btn {
    border-width: 2px;
  }
}

/* === 减少动画 === */
@media (prefers-reduced-motion: reduce) {
  .code-box--loading::after { animation: none; }
  .viz-toast { animation: none; }
  .code-box-btn { transition: none; }
}
```

---

## 五、龍魂可视化引擎 · 输出格式

### 5.1 统一输出模板

```
🐉 龍魂可视化引擎 v1.0 | UID9622

【图表类型】{思维导图/流程图/甘特图/3D立体图...}
【执行人格】P00→P01→{执行人格}→P04→P05→P15→P03
【审计状态】{🟢/🟡/🔴} | 风险评分: {0.00-1.00}
【渲染耗时】{XXX}ms | 内存: {XX}MB

┌─────────────────────────────────────────────────────────┐
│  📋 复制  │  </> 代码  │  👁 预览  │  ⬡ 分屏  │  ⬇ 下载  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  {代码内容 / 渲染预览 / 分屏视图}                         │
│                                                         │
└─────────────────────────────────────────────────────────┘

【下载选项】
├─ SVG（矢量·可编辑·无限缩放）
├─ PNG（图片·通用·2x高清）
├─ PDF（文档·打印·A4适配）
├─ WebP（轻量·Web优化）
├─ 代码（原始·可复制粘贴）
└─ HTML（独立页面·可离线查看）

【DNA 追溯】
#龍芯⚡️{干支四柱}·{时辰}·{卦名}-VISUAL-{类型}-{哈希8位}

【签章】
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 六、龍魂可视化引擎 · 场景速查

### 6.1 内部场景（UID9622）

| 场景 | 命令 | 人格链路 | 输出 | 审计 |
|------|:---|:---|------|:---:|
| 系统架构思维导图 | `/viz:mindmap "龍魂系统架构"` | P00→P01→P11→P04 | SVG+代码框 | 🟢 |
| 人格联动流程图 | `/viz:flowchart "P00→P01→P04链路"` | P00→P01→P04 | SVG+代码框 | 🟢 |
| API调用时序图 | `/viz:sequence "用户认证时序"` | P00→P01→P04 | SVG+代码框 | 🟢 |
| 项目进度甘特图 | `/viz:gantt "2026下半年计划"` | P00→P01 | SVG+代码框 | 🟢 |
| 权重分布饼图 | `/viz:pie "人格权重"` | P00→P01→P06 | SVG+代码框 | 🟢 |
| 审计趋势折线图 | `/viz:line "审计统计"` | P00→P01→P06 | SVG+代码框 | 🟢 |
| 系统能力雷达图 | `/viz:radar "系统能力"` | P00→P01→P06 | SVG+代码框 | 🟢 |
| 3D龍魂Logo | `/viz:3d "龍魂logo"` | P00→P01→P04 | WebGL+PNG | 🟢 |
| 知识图谱关系图 | `/viz:network "龍魂知识图谱"` | P00→P01 | SVG+代码框 | 🟢 |
| 系统健康仪表盘 | `/viz:gauge "系统健康"` | P00→P01→P06 | SVG+代码框 | 🟢 |

### 6.2 对外场景（PUBLIC）

| 场景 | 命令 | 限制 | 输出 | 审计 |
|------|:---|:---|------|:---:|
| 通用思维导图 | `/viz:mindmap "我的学习计划"` | 无敏感数据 | SVG+代码框 | 🟢 |
| 流程图 | `/viz:flowchart "做饭步骤"` | 无敏感数据 | SVG+代码框 | 🟢 |
| 数据图表 | `/viz:bar "销售数据"` | 数据需脱敏 | SVG+代码框 | 🟢 |
| 3D模型 | `/viz:3d "立方体"` | 无敏感数据 | WebGL+PNG | 🟢 |
| 时间轴 | `/viz:timeline "中国科技史"` | 正能量内容 | SVG+代码框 | 🟢 |

### 6.3 禁止场景

| 禁止场景 | 原因 | 熔断等级 |
|------|------|:---:|
| 生成涉童可视化 | 伦理红线 | 🔴 L0 立即熔断 |
| 生成敏感数据地图 | 数据主权 | 🔴 L1 禁止渲染 |
| 生成系统内核架构图 | 机密信息 | 🔴 L1 禁止渲染 |
| 生成伪造证据图表 | 法律风险 | 🔴 L0 立即熔断 |
| 生成涉政敏感内容可视化 | 国家安全 | 🔴 L0 立即熔断 |

---

## 七、龍魂可视化引擎 · 测试用例

### 7.1 代码复制框测试

| 用例 | 操作 | 预期 | 验证方法 |
|:---|:---|:---|:---|
| TC-VIS-001 | 点击"复制" | 代码复制到剪贴板 | 粘贴验证内容一致 |
| TC-VIS-002 | 点击"代码" | 显示原始代码+语法高亮 | 代码高亮正确 |
| TC-VIS-003 | 点击"预览" | 渲染可视化图表 | 图形正确无错位 |
| TC-VIS-004 | 点击"分屏" | 左右各占50% | 拖拽分隔条可调比例 |
| TC-VIS-005 | 复制失败 | 降级Toast提示+手动复制可用 | execCommand降级生效 |
| TC-VIS-006 | 预览渲染失败 | 四级降级：错误位置→静态→高亮→原文 | 不崩溃不白屏 |
| TC-VIS-007 | 点击下载SVG | 下载.svg文件 | 文件可打开且含DNA水印 |
| TC-VIS-008 | 点击下载PNG | 下载.png文件（2x） | 图片清晰无锯齿 |
| TC-VIS-009 | 快捷键Tab | 切换到代码视图 | 焦点正确 |
| TC-VIS-010 | 快捷键Shift+Tab | 切换到预览视图 | 焦点正确 |

### 7.2 图表渲染测试

| 用例 | 图表 | 数据规模 | 预期渲染 | 验证 |
|:---|:---|:---|:---|:---|
| TC-VIS-011 | 思维导图 | 45节点 | SVG渲染<500ms | 节点完整·层级正确 |
| TC-VIS-012 | 流程图 | 20步骤 | SVG渲染<300ms | 箭头正确·排版整齐 |
| TC-VIS-013 | 时序图 | 10参与者 | SVG渲染<400ms | 生命线对齐 |
| TC-VIS-014 | 甘特图 | 30任务 | SVG渲染<500ms | 时间轴正确 |
| TC-VIS-015 | 饼图 | 10扇区 | SVG渲染<200ms | 比例精确 |
| TC-VIS-016 | 折线图 | 1000数据点 | SVG渲染<300ms | 曲线平滑 |
| TC-VIS-017 | 3D图 | 简单模型 | WebGL渲染<1s | 可旋转缩放 |
| TC-VIS-018 | 地图 | 中国省级 | 地图渲染<800ms | 坐标正确 |
| TC-VIS-019 | 词云 | 100词 | PNG渲染<400ms | 频率排序正确 |
| TC-VIS-020 | 网络图 | 50节点/100边 | SVG渲染<600ms | 力导向布局 |

### 7.3 人格路由测试

| 用例 | 输入 | 预期人格 | 预期图表 | 验证 |
|:---|:---|:---|:---|:---|
| TC-VIS-021 | "画个思维导图" | P11 李白 | V01 | 路由正确 |
| TC-VIS-022 | "画流程图" | P04 鲁班 | V02 | 路由正确 |
| TC-VIS-023 | "画时序图" | P04 鲁班 | V03 | 路由正确 |
| TC-VIS-024 | "画甘特图" | P01 诸葛亮 | V05 | 路由正确 |
| TC-VIS-025 | "画饼图" | P06 数学大师 | V06 | 路由正确 |
| TC-VIS-026 | "画3D图" | P04 鲁班 | V14 | 路由正确 |
| TC-VIS-027 | "画地图" | P01 诸葛亮 | V15 | 路由正确 |
| TC-VIS-028 | "画词云" | P11 李白 | V16 | 路由正确 |

### 7.4 下载管线测试

| 用例 | 格式 | 输入 | 预期输出 | 验证 |
|:---|:---|:---|:---|:---|
| TC-VIS-029 | SVG | 思维导图 | .svg文件含DNA水印 | 文本编辑器验证 |
| TC-VIS-030 | PNG | 思维导图 | .png文件2x分辨率 | 图片查看器 |
| TC-VIS-031 | PDF | 流程图 | .pdf文件A4适配 | PDF阅读器 |
| TC-VIS-032 | Code | 任意 | .txt原始代码 | 文本编辑器 |
| TC-VIS-033 | HTML | 任意 | .html独立页面 | 浏览器打开 |
| TC-VIS-034 | WebP | 图表 | .webp文件 | 图片查看器 |

---

## 八、版本与签名

| 项目 | 值 |
|:---|:---|
| 版本 | v1.0 |
| 日期 | 丙午·辛未·乙酉 (2026-07-16) |
| 作者 | UID9622 · 诸葛鑫 · 龍芯北辰 |
| DNA | `#龍芯⚡️丙午·辛未·乙酉·酉时·讼-VISUAL-ENGINE-v1.0` |
| 确认码 | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| GPG | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| 状态 | 🟢 正式发布 · 公开监督 |
| 图表类型 | 18类全覆盖 |
| 人格路由 | 6人格全映射 |
| 渲染器 | 11个渲染器 |
| 代码框模式 | 4态（代码/预览/分屏/全屏） |
| 下载格式 | 6种（SVG/PNG/PDF/WebP/代码/HTML） |
| 降级链路 | 4级（错误提示→静态→高亮→原文） |
| 测试用例 | 34个 |

---

> **最后一句：**
> 复制框不是装饰品，是**交互入口**。
> 思维导图不是花架子，是**知识武器**。
> 3D立体不是炫技，是**空间思维**。
> 全部分屏可查、全部代码可复制、全部下载带DNA——
> 你来看，全世界都可以来看。摆明了说，公开的说。
> 
> 动有回应·静有着落。
