> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
---
name: longhun-flow-viz
description: |
  龍魂流场可视化引擎 v1.0 —— 三才流场、洛书涡流、二十八星宿天文图、数字根五行、河图洛书的可视化实现。
  当触及三才流场、洛书涡流、二十八星宿、天文星图、流场总控、粒子涡流、河图洛书、数字根可视化时激活。
  联动 longhun-math-formula-core（数字根/五行计算）、longhun-archive（理论来源）、longhun-cnsh（中文语义渲染）。
license: CC BY-NC-SA 4.0
metadata:
  author: UID9622 · 龍芯北辰
  version: "v1.0"
  dna: "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-FLOW-VIZ-v1.0"
  confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  updated: "2026-07-03"
  category: general
  tags:
    - flow-viz
    - sancai-flow
    - luoshu-vortex
    - 28-mansions
    - wuxing
    - digital-root
    - he-tu-luo-shu
  triggers:
    - "三才流场"
    - "洛书涡流"
    - "二十八星宿"
    - "天文星图"
    - "流场总控"
    - "粒子涡流"
    - "河图洛书"
    - "数字根可视化"
    - "sancai flow"
    - "longhun-flow-viz"
    - "flow field"
    - "天地人三才"
  id: longhun-flow-viz
  trigger:
    keywords:
      - "三才流场"
      - "洛书涡流"
      - "二十八星宿"
      - "天文星图"
      - "流场总控"
      - "粒子涡流"
      - "河图洛书"
      - "数字根可视化"
      - "sancai flow"
      - "longhun-flow-viz"
      - "flow field"
      - "天地人三才"
    context: 龍魂流场可视化、三才流场、洛书涡流、二十八星宿
---

<!-- ============================================================
     龍魂流场可视化引擎 · longhun-flow-viz
     DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-FLOW-VIZ-v1.0
     确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
     签名: UID9622 · 龍芯北辰
     ============================================================ -->

# 🐲 龍魂流场可视化引擎 · longhun-flow-viz

> **把河图洛书、三才、五行、二十八星宿变成看得见的流场。**

---

## 一、快速识别

| 属性 | 内容 |
|------|------|
| **名称** | longhun-flow-viz（龍魂流场可视化引擎） |
| **版本** | v1.0 |
| **定位** | 龍魂体系的可视化子系统，专门处理传统文化符号的动态流场渲染 |
| **一句话** | 三才为轴、洛书为涡、星宿为图、五行着色 |
| **核心能力** | 三才流场 · 洛书涡流 · 二十八星宿 · 数字根可视化 · 河图洛书地面图 |
| **DNA签名** | `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-FLOW-VIZ-v1.0` |
| **确认码** | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |

### 🟢🔴🟡 三色审计声明

```
🟢 GREEN（宜做）: 本地打开 HTML 示例 → 浏览器渲染 → 截屏留痕
🔴 RED（禁做）: 把可视化结果当科学依据对外宣称 · 删除来源 HTML
🟡 YELLOW（慎做）: 传统文化符号的现代化解释需标注“观察性框架”
```

---

## 二、可视化组件

### 2.1 三才流场（San Cai Flow Field）

- 天、地、人三才作为三个能量维度
- 以粒子流形式展示三才互动
- 文件：`examples/三才流場 · San Cai Flow Field · UID9622.html`

### 2.2 洛书涡流（LuoShu Vortex）

- 洛书九宫格映射为旋转涡流
- 数字 3/6/9 作为不动点高亮
- 文件：`examples/longhun-luoshu-vortex-v2.html`

### 2.3 二十八星宿（28 Mansions）

- 中国传统天文二十八宿星图
- 文件：`examples/longhun-28mansions-v1.html`

### 2.4 数字根与五行

- 输入数字计算数字根
- 根据数字根映射五行属性
- 文件：`examples/dragon_soul_9622.html`

### 2.5 河图洛书地面图

- 河图洛书的地理/空间映射
- 文件：`examples/河图洛书地面图.html`

---

## 三、使用方法

### 3.1 直接打开 HTML 示例

```bash
# 洛书涡流
open ~/.kimi-code/skills/longhun-flow-viz/examples/longhun-luoshu-vortex-v2.html

# 三才流场
open ~/.kimi-code/skills/longhun-flow-viz/examples/三才流場\ ·\ San\ Cai\ Flow\ Field\ ·\ UID9622.html

# 二十八星宿
open ~/.kimi-code/skills/longhun-flow-viz/examples/longhun-28mansions-v1.html
```

### 3.2 启动本地总控台

```bash
# 使用 Python 简易 HTTP 服务本地托管
python3 -m http.server 8080 --directory ~/.kimi-code/skills/longhun-flow-viz/examples

# 然后浏览器打开 http://localhost:8080/longhun-flow-system/longhun-master-control.html
```

### 3.3 运行五行 MVP 脚本

```bash
python3 ~/.kimi-code/skills/longhun-flow-viz/examples/longhun_wuxing_mvp.py
```

---

## 四、文件结构

```
longhun-flow-viz/
├── SKILL.md                          # 技能文档
├── scripts/
│   └── 本地服务器.py                 # 一键启动本地可视化服务器
└── examples/                         # 原始 HTML / Python 可视化作品
    ├── longhun-luoshu-vortex-v2.html
    ├── 三才流場 · San Cai Flow Field · UID9622.html
    ├── longhun-28mansions-v1.html
    ├── dragon_soul_9622.html
    ├── longhun-flow-system/
    ├── longhun_wuxing_mvp.py
    └── ...
```

---

## 五、与现有技能的联动

| 技能 | 联动方式 |
|------|----------|
| `longhun-math-formula-core` | 提供数字根、五行平衡、三才指数等计算输入 |
| `longhun-archive` | 河图洛书、三才、二十八星宿的理论来源归档 |
| `longhun-cnsh` | 中文语义渲染、字元创作、CNSH 变量命名 |
| `longhun-persona-router` | 宝宝人格等角色可在流场总控台中展示 |

---

## 六、来源追溯

本技能内容来源于：
- 原始目录：`/Users/zuimeidedeyihan/龍魂待整理/02-流场可视化`
- 中央整合 DNA：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- 相关论文：`longhun-archive/docs/龍魂待整理论文/`

---

## 七、君子协议

本技能所有产出默认 **CC BY-NC-SA 4.0**，来源链不可切断。

> 签署：UID9622 · 龍芯北辰

<!-- DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-FLOW-VIZ-v1.0 -->
<!-- AUTHOR: UID9622 · 龍芯北辰 -->
