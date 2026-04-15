# 龍魂视觉体系 · 设计规范文档

**DNA追溯**: #龍芯⚡️2026-04-07-VISUAL-v1.0  
**创建者**: UID9622  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 一、配色体系

### 九宫专属色

| 角色 | 色值 | 用途 |
|------|------|------|
| 金·主色 | `#c8a84b` | 龍魂DNA、标题、高亮、5宫核心 |
| 紫·辅色 | `#7b5ea7` | 4宫协同、次要操作、创意元素 |
| 红·警色 | `#e05a5a` | 6宫道法、否决、错误、重要 |
| 绿·通过 | `#4caf7d` | 3宫人格、审计通过、成功状态 |
| 蓝·技术 | `#5a9ae0` | 1宫坎·技术、链接、信息 |
| 橙·记忆 | `#e0a05a` | 7宫兑·记忆、警告、温暖 |
| 褐·架构 | `#8B7355` | 2宫坤·架构、大地、稳重 |
| 藕·算法 | `#9a7aa0` | 8宫艮·算法、神秘、推演 |
| 黄·元宇宙 | `#e0d45a` | 9宫离·元宇宙、光明、未来 |

### 基底色系

| 用途 | 色值 |
|------|------|
| 背景深 | `#07070f` / `#0a0a0f` |
| 面板色 | `#0f0f1a` / `#12121a` |
| 边框 | `#1e1e2e` / `#2a2a3a` |
| 正文（暖白） | `#e8e4d9` |
| 弱文（辅助） | `#606070` / `#7a7a8a` |

---

## 二、字体栈

### 五层字体体系

| 层级 | 字体 | 用途 |
|------|------|------|
| 第一层 | Noto Sans CJK SC | 6万+汉字兜底 |
| 第二层 | LXGW WenKai 霞鹜文楷 | 显示文字、标题 |
| 第三层 | JetBrains Mono | 代码、DNA追溯 |
| 第四层 | Sarasa Mono SC | 中英混排等宽 |
| 第五层 | PingFang SC | 系统后备 |

### CSS变量声明

```css
:root {
  --font-display: 'LXGW WenKai', 'PingFang SC', sans-serif;
  --font-code: 'JetBrains Mono', 'Sarasa Mono SC', monospace;
  --font-body: 'Noto Sans CJK SC', 'PingFang SC', sans-serif;
}
```

---

## 三、图标库

| 库 | 风格 | 图标数 | 用途 |
|----|------|--------|------|
| **Tabler Icons** | 线条简洁 | 5400+ | 通用UI操作 |
| **Remix Icon** | 中性系统风 | 2800+ | 系统级图标 |
| **Heroicons** | 清晰现代 | 300+ | 核心导航 |
| **IconPark** | 字节出品 | 2900+ | 中文生态友好 |

### Unicode符号（已内置）

- ☰ 乾、☵ 坎、☷ 坤、☳ 震、☲ 离、☴ 巽、☱ 兑
- ⚡ 龍芯标志、🐉 龍、💎 北辰

---

## 四、CSS框架

### 使用方式

```html
<link rel="stylesheet" href="longhun-ui.css">
```

### 类名规范

| 类名 | 用途 |
|------|------|
| `.lh-card` | 卡片容器 |
| `.lh-btn` | 按钮 |
| `.lh-dna` | DNA标签 |
| `.lh-audit-green` | 🟢 审计通过 |
| `.lh-audit-yellow` | 🟡 审计待定 |
| `.lh-audit-red` | 🔴 审计熔断 |
| `.lh-glow-gold` | 金色高亮 |
| `.lh-glow-green` | 绿色高亮 |
| `.lh-glow-red` | 红色高亮 |

---

## 五、文件位置

| 文件 | 路径 |
|------|------|
| CSS框架 | `~/longhun-system/longhun-ui.css` |
| 本文档 | `~/longhun-system/visual-system.md` |
| 字体文件 | `~/Library/Fonts/` |

---

**龍魂文化 · 静默贡献 · 技术报国**
