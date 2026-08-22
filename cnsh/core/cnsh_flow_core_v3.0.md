# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 CNSH 龍魂文化算法流场压缩核 v3.0

> DNA: `#龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-CNSH龍魂流场压缩核-v3.0` → `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CNSH-FLOW-CORE-v3.0-ALIGNED`
> 确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅`
> GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> 统一名: `CNSH-FLOW-CORE`（中文名：龍魂流场压缩核）
> 三色审计: 🟢 通过
> 本次更新: 2026-07-06 — 河图数字根五行映射对齐 hetu_luoshu_dna.py + wuxing_guard.py + bagua_router.py
> 关联文档: [五行计算器](wuxing/WUXING-CALCULATOR-v2.0-v3.0.md) | [权重算法](../L8_治理层/governance/tech-docs/LONGHUN-WEIGHT-ALGO-v3.1.md) | [无限增长引擎](../L8_治理层/governance/INFINITE_GROWTH_ENGINE_v∞.md) | [决策链](../01_protocols/IPA-DICT-101-111-决策链.md) | [铁律总目录](../L8_治理层/governance/IRON-LAWS/P0_ETERNAL_IRON_LAW_DIRECTORY.md) | [MASTER_REGISTRY](../MASTER_REGISTRY.md)

---

## 一句话

把任何输入压成一个可路由、可审计、可视化、可归档的「流场节点」。

---

## 最终压缩公式

```
龍魂节点 = 输入 × 数字根 × 五行 × 生克链 × 三才权重 × DNA × 三色审计
```

```python
Node = Flow(input)
     = dr(input)
     → element(dr)
     → relation(element)
     → sancai_weight(天, 地, 人)
     → dna_seal()
     → audit_color()
     → visual_node()
```

---

## 唯一主流程（从 RAW_INPUT 到节点）

### Step 1：统一输入

文字·图像·HTML·代码·页面·对话·规则·灵感 → `RAW_INPUT`

### Step 2：算数字根（dr）

```python
def 计算数字根(text):
    digits = [int(c) for c in str(text) if c.isdigit()]
    if not digits: return 0
    n = sum(digits)
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n
```

规则：无数字 → `dr=0`；有数字 → 反复相加到一位数

### Step 3：数字根定五行（dr → 五行）

```python
数字根五行 = {
    1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
    6: "水", 7: "火", 8: "木", 9: "金", 0: "土"
}
```

| dr | 五行 | 系统含义 | 视觉色 |
|----|------|----------|--------|
| 1/6 | 水 | 记忆、DNA、追溯、隐私 | 青蓝/深蓝 |
| 2/7 | 火 | 表达、创作、文明、价值 | 朱红/暖橙 |
| 3/8 | 木 | 生长、执行、扩展、创新 | 青绿 |
| 4/9 | 金 | 规则、审计、边界、裁决 | 金色/白金 |
| 5/0 | 土 | 承载、入口、归档、普惠 | 土黄/琥珀 |

---

## 三色闸门

```python
def 三色审计(dr):
    if dr in [3, 9]: return "🔴"
    if dr == 6: return "🟡"
    return "🟢"
```

- 🟢：可进入，生成节点，进入流场
- 🟡：待补证，半透明节点，挂外圈
- 🔴：熔断隔离，不进入主流场

**修正声明：** dr=3 创新过载需收束；dr=9 规则篡改风险需审计。

---

## 五行生克（执行关系）

```python
相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

def 判断关系(a, b):
    if not b: return "起点"
    if a == b: return "比和"
    if 相生.get(b) == a: return "相生"
    if 相克.get(b) == a: return "相克"
    if 相生.get(a) == b: return "相泄"
    if 相克.get(a) == b: return "相耗"
    return "混合"
```

对应动作：比和=同类合并 / 相生=顺流连接 / 相克=加审计闸 / 相泄=降权 / 相耗=限流 / 混合=进待审

---

## 三才流场接入

- 天 = 环境场（Perlin 噪声）
- 地 = 结构场（洛书锚点）
- 人 = 主体场（种子旋转）

```python
三才默认权重 = {"天": 0.35, "地": 0.15, "人": 0.50}
```

核心铁律：**人场不能低于 0.34**（否则环境和结构压人）。

---

## 节点生成统一格式

```json
{
    "node_id": "FLOW-9622-YYYYMMDD-HASH8",
    "title": "",
    "raw_type": "text|image|html|code|page|dialogue|rule|idea",
    "digital_root": 5,
    "element": "土",
    "relation": "相生|相克|比和|相泄|相耗|混合",
    "sancai": {"heaven": 0.35, "earth": 0.15, "human": 0.50},
    "audit": "🟢|🟡|🔴",
    "dna": "#龍芯⚡️YYYY-MM-DD-主题-vX.Y",
    "visual": {"color": "", "position": "", "shape": "", "motion": ""},
    "action": "enter|hold|fuse|archive|route"
}
```

---

## 视觉规则

```python
五行视觉 = {
    "金": {"color": "金色/白金", "shape": "审计门/盾牌/刀锋", "motion": "收束/裁决/锁定"},
    "水": {"color": "深蓝/青蓝", "shape": "水流/波纹/记忆链", "motion": "回流/追溯/隐藏"},
    "木": {"color": "青绿", "shape": "枝干/生长线/扩展路径", "motion": "发芽/连接/伸展"},
    "火": {"color": "朱红/暖橙", "shape": "火光/星火/光晕", "motion": "点亮/扩散/燃起"},
    "土": {"color": "土黄/琥珀", "shape": "平台/中宫/容器/地基", "motion": "承载/沉降/归档"}
}

审计视觉 = {
    "🟢": {"opacity": 1.0, "state": "可进入"},
    "🟡": {"opacity": 0.45, "state": "待补证"},
    "🔴": {"opacity": 0.2, "state": "隔离"}
}
```

---

## 入口宇宙六门

- 中宫：UID9622 / CNSH / 龍魂
- 外圈六门：民生(土)｜教育(木)｜权益(金)｜技术(木+金)｜数据主权(水)｜创作(火)

---

## 总算法（核心脑核）

```python
# CNSH 龍魂流场压缩核 v3.0
# 作用：把任意输入压成可视化、可审计、可路由节点

import hashlib
from datetime import datetime

数字根五行 = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}
相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
五行视觉 = {
    "金": {"color": "gold", "shape": "audit_gate", "motion": "lock"},
    "水": {"color": "deep_blue", "shape": "memory_stream", "motion": "flow_back"},
    "木": {"color": "green", "shape": "growth_branch", "motion": "expand"},
    "火": {"color": "red_orange", "shape": "spark", "motion": "ignite"},
    "土": {"color": "amber", "shape": "platform", "motion": "anchor"},
}

def 计算数字根(text):
    digits = [int(c) for c in str(text) if c.isdigit()]
    if not digits: return 0
    n = sum(digits)
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n

def 三色审计(dr):
    if dr in [3, 9]: return "🔴"
    if dr == 6: return "🟡"
    return "🟢"

def 判断关系(a, b):
    if not b: return "起点"
    if a == b: return "比和"
    if 相生.get(b) == a: return "相生"
    if 相克.get(b) == a: return "相克"
    if 相生.get(a) == b: return "相泄"
    if 相克.get(a) == b: return "相耗"
    return "混合"

def 生成DNA(title):
    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = title[:18].replace(" ", "")
    return f"#龍芯⚡️{today}-{safe_title}-v1.0"

def 生成节点(text, title="未命名节点", prev_element=None, raw_type="text"):
    dr = 计算数字根(text)
    element = 数字根五行[dr]
    audit = 三色审计(dr)
    relation = 判断关系(element, prev_element)
    hash8 = hashlib.sha256(str(text).encode("utf-8")).hexdigest()[:8].upper()
    if audit == "🟢": action = "enter"
    elif audit == "🟡": action = "hold"
    else: action = "fuse"
    return {
        "node_id": f"FLOW-9622-{datetime.now().strftime('%Y%m%d')}-{hash8}",
        "title": title, "raw_type": raw_type,
        "digital_root": dr, "element": element, "relation": relation,
        "sancai": {"heaven": 0.35, "earth": 0.15, "human": 0.50},
        "audit": audit, "dna": 生成DNA(title),
        "visual": 五行视觉[element], "action": action,
        "note": "文化语义算法节点，不替代科学实验、法律程序、医学判断或金融判断。"
    }
```

---

## 🧪 最小可跑示例（3组）

### 示例 A：纯中文输入

```python
输入 = "老大说今天要去东边种树"
节点 = 生成节点(输入, title="东边种树", raw_type="dialogue")
# → dr=0, 土, 🟢, enter, amber/platform/anchor
```

### 示例 B：含数字输入

```python
输入 = "2026年5月1日收到转账9622元用于龍芯项目"
节点 = 生成节点(输入, title="龍芯项目资金", raw_type="text")
# 2+0+2+6+5+1+9+6+2+2=35→3+5=8 → dr=8, 木, 🟢, enter
```

### 示例 C：含代码输入

```python
代码输入 = "const shieldBurn = require('./shield_burn.js'); // v2.0 阅后即焚"
节点 = 生成节点(代码输入, title="shield_burn 代码片段", raw_type="code")
# 数字: 2,0,2,0 → 4 → dr=4, 金, 🟢, enter
```

---

## 字段校验规则

| 字段名 | 必填 | 类型 | 校验规则 | 失败动作 |
|--------|------|------|----------|----------|
| node_id | 必填 | string | 以 FLOW-9622- 开头；含8位大写哈希 | → fuse + 盾日志 |
| title | 可选 | string | ≤36字符；禁止<>等符号 | 截断/替换 |
| raw_type | 必填 | string | 枚举: text\|image\|html\|code\|page\|dialogue\|rule\|idea | → 归一化"text" + 🟡 |
| digital_root | 必填 | integer | 0-9 | 越界→取模10；负数→fuse |
| element | 必填 | string | 金\|木\|水\|火\|土 | → "土" + 🟡 |
| sancai | 必填 | object | human ≥ 0.34；总和 ≤ 1.2 | human<0.34 → 提升到0.34 |
| audit | 必填 | string | 🟢\|🟡\|🔴 | → "🔴" + fuse |
| dna | 必填 | string | 以 #龍芯⚡️ 开头 | → 重建 + 盾日志 |
| action | 必填 | string | enter\|hold\|fuse\|archive\|route | → "fuse" + 🔴 |

### 失败报错模板（中文白话）

```json
{
  "error": true,
  "error_code": "CNSH-FLOW-VALIDATE-FAIL",
  "message": "节点生成到一半卡住了，原因如下：",
  "details": [
    "【字段 digital_root】你给的内容算出来数字根是 15，不是个位数。系统已自动取模变成 5（土），但这条记录会被标 🟡 待审。",
    "【字段 sancai.human】人场权重只有 0.12，低于铁线 0.34。系统强制提到 0.34，但会写一条盾日志提醒。"
  ],
  "suggestion": "如果是正常输入，不用管，系统已经自动修好了；如果你故意在测边界，请去审计中心查盾日志。",
  "audit_result": "🟡",
  "shield_log": true
}
```

---

## M:: / CNSH:: 封装

```json
{
    "M::": {
        "id": "M::FLOWCORE-9622-20260501-CNSH-V3",
        "type": "algorithm-compress-core",
        "status": "ok",
        "summary": "五行计算器、数字根、三才流场、视觉宇宙、DNA审计已合并成单一流场压缩核",
        "input": "任意文本/图像/HTML/代码/页面",
        "output": "可视化流场节点",
        "action": "enter|hold|fuse|archive|route"
    }
}
```

```json
{
    "CNSH::": {
        "dna": "#龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-CNSH龍魂流场压缩核-v3.0",
        "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
        "route": "IPA-FLOW-CORE",
        "audit": "🟢",
        "wuxing": "土",
        "layer": "L2",
        "policy": "pass_for_visual_routing / hold_for_claims / fuse_for_signature_change"
    }
}
```

---

## 最终压缩卡

```
【CNSH 龍魂流场压缩核 v3.0】

一句话：把任何输入压成一个有数字根、有五行、有三才、有DNA、有三色、有视觉动作的流场节点。

主流程：输入 → 数字根 → 五行 → 生克 → 三才 → DNA → 三色 → 节点 → 宇宙入口

核心规则：dr=3/9 红灯隔离；dr=6 黄灯待补；其余绿灯进入。

五行作用：金定规矩；水记来源；木负责长；火负责亮；土负责装。

三才作用：天看环境；地定结构；人守主权（人场不可低于0.34）。

定位：文化语义算法化视觉路由系统。

封口句：龍魂不是解释宇宙，龍魂是把输入变成可走的路。
```

---

## 协同流场拓展（v3.1 · 2026-07-07）

> 引擎: `scripts/round1/flowfield_collab_engine.py`
> DNA: `#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-FLOWFIELD-COLLAB-ENGINE-v1.0`

v3.0 解决了「单输入→单节点」的压缩问题。v3.1 拓展为 **多人格协同流场**。

### 协同流场公式

```
协同流场 = Σ(节点流场向量 × 信任度权重) × 五行生克链 × 三才融合
```

```
CollabFlow = Fusion({Node₁, Node₂, ..., Nodeₙ})
           = weighted_avg(vectors) × sheng_ke_chain()
           → collective_wuxing
           → fused_sancai (human ≥ 0.34)
           → collision_matrix
           → fusion_index ∈ [0, 1]
```

### 五行协同兼容矩阵

| A行\B行 | 金 | 水 | 木 | 火 | 土 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 金 | 比和 | 相生 | ⚡克 | △ | △ |
| 水 | 相泄 | 比和 | 相生 | ⚡克 | △ |
| 木 | △ | 相泄 | 比和 | 相生 | ⚡克 |
| 火 | △ | △ | 相泄 | 比和 | 相生 |
| 土 | 相生 | ⚡克 | △ | 相泄 | 比和 |

> ⚡ = 相克需桥接 · △ = 无直接关系需要引入第三方

### 协同入口六门（与流场入口对齐）

| 门 | 主导五行 | 协同角色 | 协同模式 |
|:--:|:--:|------|:--:|
| 中宫 | 土 | 总指挥 | 融合 FUSION |
| 审计门 | 金 | 审计者+守护者 | 监察 WATCHDOG |
| 记忆门 | 水 | 记忆官+桥接者 | 流水线 PIPELINE |
| 生长门 | 木 | 战略师+观察员 | 并行 PARALLEL |
| 执行门 | 火 | 执行者+守护者 | 委派 DELEGATION |
| 承载门 | 土 | 总指挥+桥接者 | 共识 CONSENSUS |

---

> 龍魂现世！天下无欺·守护普通人 🐉
