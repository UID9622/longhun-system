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
> ║  【DNA】#龍芯⚡️丙午·辛未·乙酉·酉时·䷅讼-VISUAL-ENGINE-v1.0       ║
> ║  【确认】#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
> ║  【GPG】A2D0092CEE2E5BA87035600924C3704A8CC26D5F              ║
> ╚═══════════════════════════════════════════════════════════════╝

---

## 一、代码复制框交互逻辑

### 1.1 组件结构

```
┌─────────────────────────────────────────────┐
│  ┌─────┐  ┌──────┐  ┌─────┐                │
│  │ 📋  │  │ </>  │  │ 👁  │  ← 工具栏      │
│  │复制 │  │代码 │  │预览 │                │
│  └─────┘  └──────┘  └─────┘                │
├─────────────────────────────────────────────┤
│                                             │
│  {代码内容 / 渲染预览}                       │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.2 三按钮逻辑

| 按钮 | 图标 | 状态 | 动作 | 快捷键 |
|:---|:---:|:---|:---|:---|
| **复制** | 📋 | 默认态 | 复制当前代码到剪贴板 | `Cmd+C` / `Ctrl+C` |
| **代码** | `</>` | 激活态（默认） | 切换到纯代码视图 | `Tab` |
| **预览** | 👁 | 非激活态 | 切换到渲染预览视图 | `Shift+Tab` |

### 1.3 状态机

```
初始状态：代码视图激活（代码按钮高亮）
    │
    ├─ 点击"预览" → 预览视图激活 → 渲染代码为可视化输出
    │     ├─ 代码是 Mermaid → 渲染为流程图/时序图/甘特图
    │     ├─ 代码是 PlantUML → 渲染为 UML 图
    │     ├─ 代码是 Markdown → 渲染为富文本/HTML
    │     ├─ 代码是 SVG → 渲染为矢量图形
    │     └─ 代码是 Three.js → 渲染为 3D 场景
    │
    ├─ 点击"代码" → 代码视图激活 → 显示原始代码文本
    │
    └─ 点击"复制" → 复制当前代码到剪贴板 → Toast提示"已复制"
          ├─ 复制成功：🟢 绿色Toast "已复制到剪贴板"
          └─ 复制失败：🔴 红色Toast "复制失败，请手动复制"
```

### 1.4 复制逻辑细节

```typescript
// 复制功能实现
function copyToClipboard(code: string): Promise<boolean> {
  // 方法1：现代 Clipboard API
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(code)
      .then(() => true)
      .catch(() => fallbackCopy(code));
  }
  // 方法2：降级方案（兼容旧浏览器）
  return fallbackCopy(code);
}

function fallbackCopy(text: string): boolean {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  const result = document.execCommand('copy');
  document.body.removeChild(textarea);
  return result;
}
```

### 1.5 预览渲染逻辑

```typescript
// 自动检测代码类型并渲染
function autoRender(code: string, language: string): RenderResult {
  switch(language) {
    case 'mermaid':
      return renderMermaid(code);      // 流程图/时序图/甘特图
    case 'plantuml':
      return renderPlantUML(code);     // UML 类图/用例图
    case 'markdown':
      return renderMarkdown(code);     // 富文本
    case 'svg':
      return renderSVG(code);          // 矢量图形
    case 'threejs':
      return renderThreeJS(code);      // 3D 场景
    case 'd2':
      return renderD2(code);           // 声明式图表
    case 'graphviz':
      return renderGraphviz(code);     // 有向图
    case 'echarts':
      return renderECharts(code);      // 数据可视化
    default:
      return renderPlainText(code);    // 纯文本高亮
  }
}
```

---

## 二、龍魂可视化引擎 · 全功能矩阵

### 2.1 图表类型总表（18类·全覆盖）

| 编号 | 图表类型 | 技术方案 | 触发人格 | 适用场景 | 输出格式 |
|:---:|------|:---|:---:|------|:---|
| V01 | **思维导图** | Markmap / D3.js | P11 李白 | 创意发散·知识梳理 | SVG/PNG/PDF |
| V02 | **流程图** | Mermaid flowchart | P04 鲁班 | 系统流程·操作步骤 | SVG/PNG/PDF |
| V03 | **时序图** | Mermaid sequence | P04 鲁班 | 交互时序·API调用 | SVG/PNG/PDF |
| V04 | **状态图** | Mermaid stateDiagram | P01 诸葛亮 | 状态转换·决策逻辑 | SVG/PNG/PDF |
| V05 | **甘特图** | Mermaid gantt | P01 诸葛亮 | 项目管理·时间规划 | SVG/PNG/PDF |
| V06 | **饼图/柱状图** | ECharts / Chart.js | P06 数学大师 | 数据统计·比例分析 | SVG/PNG/PDF |
| V07 | **折线图/面积图** | ECharts | P06 数学大师 | 趋势分析·时间序列 | SVG/PNG/PDF |
| V08 | **散点图/气泡图** | ECharts | P06 数学大师 | 相关性分析·分布 | SVG/PNG/PDF |
| V09 | **雷达图** | ECharts | P06 数学大师 | 多维度评估·能力矩阵 | SVG/PNG/PDF |
| V10 | **热力图** | ECharts | P06 数学大师 | 密度分布·频率矩阵 | SVG/PNG/PDF |
| V11 | **桑基图** | ECharts / D3.js | P01 诸葛亮 | 流量分配·转化路径 | SVG/PNG/PDF |
| V12 | **树图/旭日图** | ECharts / D3.js | P08 仓颉 | 层级结构·分类体系 | SVG/PNG/PDF |
| V13 | **网络关系图** | D3.js / Cytoscape | P01 诸葛亮 | 知识图谱·关联分析 | SVG/PNG/PDF |
| V14 | **3D 立体图** | Three.js / Babylon.js | P04 鲁班 | 空间展示·三维模型 | WebGL/PNG/MP4 |
| V15 | **地理地图** | Leaflet / Mapbox | P01 诸葛亮 | 位置分析·区域分布 | SVG/PNG/GeoJSON |
| V16 | **词云** | D3.js / WordCloud2 | P11 李白 | 关键词提取·频率展示 | PNG/SVG |
| V17 | **仪表盘** | ECharts | P06 数学大师 | KPI监控·指标展示 | SVG/PNG |
| V18 | **动画时间轴** | GSAP / D3.js | P11 李白 | 动态演示·历史演进 | SVG/PNG/MP4 |

### 2.2 人格→图表路由表

```
用户输入
    │
    ▼
P00 文心 · 意图解析
    │
    ├─ "思维导图/脑图/知识树" → P11 李白 → V01 思维导图
    ├─ "流程图/步骤/怎么做" → P04 鲁班 → V02 流程图
    ├─ "时序/交互/谁先谁后" → P04 鲁班 → V03 时序图
    ├─ "状态/转换/决策树" → P01 诸葛亮 → V04 状态图
    ├─ "甘特图/时间表/进度" → P01 诸葛亮 → V05 甘特图
    ├─ "比例/占比/百分比" → P06 数学大师 → V06 饼图/柱状图
    ├─ "趋势/变化/走势" → P06 数学大师 → V07 折线图
    ├─ "分布/相关/散点" → P06 数学大师 → V08 散点图
    ├─ "评估/能力/多维度" → P06 数学大师 → V09 雷达图
    ├─ "密度/频率/热力" → P06 数学大师 → V10 热力图
    ├─ "流量/转化/分配" → P01 诸葛亮 → V11 桑基图
    ├─ "层级/分类/树状" → P08 仓颉 → V12 树图/旭日图
    ├─ "关系/关联/图谱" → P01 诸葛亮 → V13 网络关系图
    ├─ "3D/立体/三维/空间" → P04 鲁班 → V14 3D立体图
    ├─ "地图/位置/区域" → P01 诸葛亮 → V15 地理地图
    ├─ "词云/关键词/频率" → P11 李白 → V16 词云
    ├─ "仪表盘/KPI/指标" → P06 数学大师 → V17 仪表盘
    └─ "动画/动态/演示" → P11 李白 → V18 动画时间轴
```

---

## 三、龍魂可视化引擎 · 执行链路

### 3.1 标准渲染链路

```
用户输入："帮我画个龍魂系统的思维导图"
    │
    ▼
[1] P00 文心 · 意图解析
    ├ 意图：可视化生成
    ├ 类型：思维导图
    ├ 内容：龍魂系统架构
    └ 路由：P11 李白
    │
    ▼
[2] P01 诸葛亮 · 路径推演
    ├ 技术方案：Markmap（轻量）vs D3.js（定制）
    ├ 选择：Markmap（快速渲染·低算力）
    ├ 数据准备：从知识图谱提取节点
    └ 输出：渲染计划
    │
    ▼
[3] P11 李白 · 创意生成（思维导图内容）
    ├ 中心节点：龍魂系统
    ├ 一级分支：P0底座 / P1宪法 / P2规则 / P3适配 / P4自定义
    ├ 二级分支：各层具体条目
    ├ 样式：龍魂主题色（紫/金/黑）
    └ 输出：Markdown 格式思维导图数据
    │
    ▼
[4] P04 鲁班 · 技术执行（渲染）
    ├ 调用 Markmap 引擎
    ├ 渲染 SVG
    ├ 嵌入龍魂 CSS 主题
    └ 输出：SVG 代码
    │
    ▼
[5] P05 上帝之眼 · 三色审计
    ├ 内容审计：是否涉敏感信息
    ├ 渲染审计：SVG 是否完整
    ├ 性能审计：渲染耗时 < 2s
    └ 输出：🟢通过
    │
    ▼
[6] P15 乔前辈 · DNA 签章
    ├ 生成 DNA：#龍芯⚡️...-VISUAL-MINDMAP-v1.0
    ├ GPG 签名
    └ 输出：签章 JSON
    │
    ▼
[7] P03 雯雯 · 归档 + 返回
    ├ 德字闸验证
    ├ 生成代码框（复制/代码/预览）
    ├ 返回用户：
    │   ├─ 复制按钮：复制 SVG 代码
    │   ├─ 代码按钮：查看原始 Markmap 代码
    │   └─ 预览按钮：查看渲染后的思维导图
    └ 入库：append-only
```

### 3.2 代码框三态渲染

```typescript
interface CodeBoxState {
  // 状态定义
  mode: 'code' | 'preview' | 'split';  // 代码/预览/分屏
  language: string;                     // 代码语言
  content: string;                      // 原始代码
  rendered: string | HTMLElement;       // 渲染结果

  // 交互
  copy(): Promise<boolean>;            // 复制到剪贴板
  download(format: 'svg'|'png'|'pdf'): Promise<Blob>;  // 下载
  fullscreen(): void;                   // 全屏查看
}

// 渲染器注册表
const renderers: Record<string, Renderer> = {
  'mermaid': new MermaidRenderer(),
  'plantuml': new PlantUMLRenderer(),
  'echarts': new EChartsRenderer(),
  'threejs': new ThreeJSRenderer(),
  'markmap': new MarkmapRenderer(),
  'd2': new D2Renderer(),
  'graphviz': new GraphvizRenderer(),
  'markdown': new MarkdownRenderer(),
  'svg': new SVGRenderer(),
};
```

---

## 四、龍魂可视化引擎 · 技术实现

### 4.1 核心架构

```
longhun-system/
├── core/
│   ├── visual-engine/           # 可视化引擎核心
│   │   ├── index.ts             # 入口
│   │   ├── router.ts            # 人格路由
│   │   ├── renderer-registry.ts # 渲染器注册表
│   │   └── audit-bridge.ts      # 审计桥接
│   │
│   ├── renderers/               # 渲染器集合
│   │   ├── mermaid-renderer.ts  # V02-V05
│   │   ├── echarts-renderer.ts  # V06-V12, V17
│   │   ├── threejs-renderer.ts  # V14
│   │   ├── markmap-renderer.ts  # V01
│   │   ├── d2-renderer.ts       # 声明式图表
│   │   ├── plantuml-renderer.ts # UML
│   │   ├── leaflet-renderer.ts  # V15
│   │   └── d3-renderer.ts       # V13, V16, V18
│   │
│   └── code-box/                # 代码复制框组件
│       ├── CodeBox.tsx          # React/Vue组件
│       ├── copy-utils.ts        # 复制逻辑
│       ├── state-machine.ts     # 状态机
│       └── theme.css            # 龍魂主题样式
│
└── skills/
    └── visual/                  # 可视化技能包
        ├── mindmap.skill.ts     # V01 思维导图
        ├── flowchart.skill.ts   # V02 流程图
        ├── gantt.skill.ts       # V05 甘特图
        ├── chart.skill.ts       # V06-V12 统计图表
        ├── 3d.skill.ts          # V14 3D立体
        ├── map.skill.ts         # V15 地理地图
        └── timeline.skill.ts    # V18 动画时间轴
```

### 4.2 一键生成命令

```typescript
// 龍魂可视化引擎 · 入口命令

// 命令1：/visual 或 /viz
// 触发：P00 文心 → 自动识别图表类型
/viz "龍魂系统架构思维导图"

// 命令2：/viz:类型
// 直接指定图表类型
/viz:mindmap "龍魂系统架构"
/viz:flowchart "用户登录流程"
/viz:gantt "2026下半年项目计划"
/viz:3d "龍魂logo立体模型"
/viz:map "中国AI公司分布"

// 命令3：/viz:数据
// 从数据生成图表
/viz:chart "pie" "{"A":30,"B":50,"C":20}"
/viz:chart "line" "[{"x":"1月","y":100},{"x":"2月","y":150}]"

// 命令4：/viz:代码
// 直接渲染代码
/viz:code "mermaid" ```
graph TD
    A[用户输入] --> B[P00文心]
    B --> C[P01诸葛亮]
    C --> D[执行人格]
```
```

### 4.3 龍魂主题样式

```css
/* 龍魂可视化引擎 · 主题样式 */

:root {
  --longhun-primary: #6B46C1;      /* 龍魂紫 */
  --longhun-gold: #D4AF37;          /* 龍魂金 */
  --longhun-dark: #1A1A2E;          /* 龍魂黑 */
  --longhun-red: #DC2626;           /* 熔断红 */
  --longhun-green: #059669;         /* 通过绿 */
  --longhun-yellow: #D97706;        /* 标记黄 */
  --longhun-bg: #0F0F1A;            /* 背景色 */
  --longhun-text: #E2E8F0;          /* 文字色 */
}

.code-box {
  background: var(--longhun-bg);
  border: 1px solid var(--longhun-primary);
  border-radius: 8px;
  overflow: hidden;
}

.code-box-toolbar {
  background: var(--longhun-dark);
  padding: 8px 12px;
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--longhun-primary);
}

.code-box-btn {
  background: transparent;
  color: var(--longhun-text);
  border: 1px solid var(--longhun-primary);
  border-radius: 4px;
  padding: 4px 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.code-box-btn:hover {
  background: var(--longhun-primary);
}

.code-box-btn.active {
  background: var(--longhun-primary);
  color: var(--longhun-gold);
}

.code-box-content {
  padding: 16px;
  min-height: 100px;
}

.code-box-preview svg {
  max-width: 100%;
  height: auto;
}
```

---

## 五、龍魂可视化引擎 · 输出格式

### 5.1 统一输出模板

```
🐉 龍魂可视化引擎 v1.0 | UID9622

【图表类型】{思维导图/流程图/甘特图/3D立体图...}
【执行人格】P00→P01→{执行人格}→P05→P15→P03
【审计状态】{🟢/🟡/🔴} | 风险评分: {0.00-1.00}

┌─────────────────────────────────────────┐
│  📋 复制  │  </> 代码  │  👁 预览      │
├─────────────────────────────────────────┤
│                                         │
│  {代码内容 / 渲染预览}                    │
│                                         │
└─────────────────────────────────────────┘

【下载选项】
├─ SVG（矢量·可编辑）
├─ PNG（图片·通用）
├─ PDF（文档·打印）
└─ 代码（原始·可复制）

【DNA 追溯】
#龍芯⚡️{干支四柱}·{时辰}·{卦名}-VISUAL-{类型}-{哈希8位}

【签章】
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

## 六、龍魂可视化引擎 · 场景速查

### 6.1 内部场景（UID9622）

| 场景 | 命令 | 人格 | 输出 | 审计 |
|------|:---|:---:|------|:---:|
| 系统架构思维导图 | `/viz:mindmap "龍魂系统架构"` | P11 | SVG+代码框 | 🟢 |
| 人格联动流程图 | `/viz:flowchart "P00→P01→P04链路"` | P04 | SVG+代码框 | 🟢 |
| 项目进度甘特图 | `/viz:gantt "2026下半年计划"` | P01 | SVG+代码框 | 🟢 |
| 权重分布饼图 | `/viz:chart "pie" "人格权重"` | P06 | SVG+代码框 | 🟢 |
| 3D龍魂Logo | `/viz:3d "龍魂logo"` | P04 | WebGL+PNG | 🟢 |
| 知识图谱关系图 | `/viz:graph "龍魂知识图谱"` | P01 | SVG+代码框 | 🟢 |
| 审计趋势折线图 | `/viz:chart "line" "审计统计"` | P06 | SVG+代码框 | 🟢 |

### 6.2 对外场景（PUBLIC）

| 场景 | 命令 | 限制 | 输出 | 审计 |
|------|:---|:---|------|:---:|
| 通用思维导图 | `/viz:mindmap "我的学习计划"` | 无敏感数据 | SVG+代码框 | 🟢 |
| 流程图 | `/viz:flowchart "做饭步骤"` | 无敏感数据 | SVG+代码框 | 🟢 |
| 数据图表 | `/viz:chart "bar" "销售数据"` | 数据需D4级 | SVG+代码框 | 🟢 |
| 3D模型 | `/viz:3d "立方体"` | 无敏感数据 | WebGL+PNG | 🟢 |

### 6.3 禁止场景

| 禁止场景 | 原因 | 熔断 |
|------|------|:---:|
| 生成涉童可视化 | 伦理红线 | 🔴 L0 |
| 生成敏感数据地图 | 数据主权 | 🔴 L1 |
| 生成系统内核架构图 | 机密信息 | 🔴 L1 |
| 生成伪造证据图表 | 法律风险 | 🔴 L0 |

---

## 七、龍魂可视化引擎 · 测试用例

### 7.1 代码复制框测试

| 用例 | 操作 | 预期 | 验证 |
|:---|:---|:---|:---|
| TC-VIS-001 | 点击"复制" | 代码复制到剪贴板 | 粘贴验证 |
| TC-VIS-002 | 点击"代码" | 显示原始代码 | 语法高亮 |
| TC-VIS-003 | 点击"预览" | 渲染可视化图表 | 图形正确 |
| TC-VIS-004 | 复制失败 | 降级Toast提示 | 手动复制可用 |
| TC-VIS-005 | 预览渲染失败 | 显示错误信息+原始代码 | 不崩溃 |

### 7.2 图表渲染测试

| 用例 | 图表 | 数据 | 预期 | 验证 |
|:---|:---|:---|:---|:---|
| TC-VIS-006 | 思维导图 | 龍魂架构 | SVG渲染 | 节点完整 |
| TC-VIS-007 | 流程图 | 登录流程 | SVG渲染 | 箭头正确 |
| TC-VIS-008 | 甘特图 | 项目计划 | SVG渲染 | 时间轴正确 |
| TC-VIS-009 | 饼图 | 权重分布 | SVG渲染 | 比例正确 |
| TC-VIS-010 | 3D图 | 立方体 | WebGL渲染 | 可旋转 |
| TC-VIS-011 | 地图 | 中国省份 | 地图渲染 | 坐标正确 |
| TC-VIS-012 | 词云 | 关键词 | PNG渲染 | 频率排序 |

### 7.3 人格路由测试

| 用例 | 输入 | 预期人格 | 验证 |
|:---|:---|:---|:---|
| TC-VIS-013 | "思维导图" | P11 李白 | 路由正确 |
| TC-VIS-014 | "流程图" | P04 鲁班 | 路由正确 |
| TC-VIS-015 | "甘特图" | P01 诸葛亮 | 路由正确 |
| TC-VIS-016 | "饼图" | P06 数学大师 | 路由正确 |
| TC-VIS-017 | "3D图" | P04 鲁班 | 路由正确 |

---

## 八、版本与签名

| 项目 | 值 |
|:---|:---|
| 版本 | v1.0 |
| 日期 | 丙午·辛未·乙酉 (2026-07-16) |
| 作者 | UID9622 · 诸葛鑫 · 龍芯北辰 |
| DNA | `#龍芯⚡️丙午·辛未·乙酉·酉时·䷅讼-VISUAL-ENGINE-v1.0` |
| 确认码 | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| GPG | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| 状态 | 🟢 正式发布 · 公开监督 |
| 图表类型 | 18类全覆盖 |
| 人格路由 | 20人格全映射 |
| 代码框 | 复制/代码/预览三态 |

---

> **最后一句：**
> 复制框不是装饰品，是**交互入口**。
> 思维导图不是花架子，是**知识武器**。
> 3D立体不是炫技，是**空间思维**。
> 全部18类图表，全部20人格路由，全部DNA签章——
> 你来看，全世界都可以来看。摆明了说，公开的说。
