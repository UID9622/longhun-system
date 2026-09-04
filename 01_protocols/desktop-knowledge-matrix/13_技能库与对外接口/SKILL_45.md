---
name: longhun-persona-router
description: |
  龍魂·人格路由系統 v1.0 —— 五大人格實體（龍芯⚡️ / 通心譯 / 龍魂 / 君子 / 審計）的加權關鍵詞路由與熔斷配置。
  當觸及五大人格、人格實體路由、persona system、龍芯人格、通心譯人格、君子人格、審計人格時激活。
  與 longhun-empower-engine 的「需求識別 + 9人格分工」區分：本技能聚焦五大人格實體的路由配置與熔斷規則。
license: CC BY-NC-SA 4.0
metadata:
  author: UID9622 · 龍芯北辰
  version: "v1.0"
  dna: "#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PERSONA-ROUTER-v1.0"
  confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  updated: "2026-07-03"
  category: general
  tags:
    - persona-router
    - five-personas
    - routing
    - kunpeng
    - weighted-keyword-match
  triggers:
    - "五大人格"
    - "人格實體路由"
    - "persona system"
    - "龍芯人格"
    - "通心譯人格"
    - "君子人格"
    - "審計人格"
    - "人格配置"
    - "五大人格实体"
    - "tech dragon"
    - "edu translator"
    - "military LongHun"
    - "phi gentleman"
    - "law auditor"
  id: longhun-persona-router
  trigger:
    keywords:
      - "五大人格"
      - "人格實體路由"
      - "persona system"
      - "龍芯人格"
      - "通心譯人格"
      - "君子人格"
      - "審計人格"
      - "人格配置"
      - "五大人格实体"
      - "tech dragon"
      - "edu translator"
      - "military LongHun"
      - "phi gentleman"
      - "law auditor"
    context: 五大人格实体路由、人格配置、鲲鹏人格路由
---

<!-- ============================================================
     龍魂·人格路由系統 · longhun-persona-router
     DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PERSONA-ROUTER-v1.0
     确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
     签名: UID9622 · 龍芯北辰
     硬件靶标: 華為TaiShan 200 2280 | 鯤鵬920 ARM64 | SN: 2102314UJFN0S3102797
     ============================================================ -->

# 🐲 龍魂·人格路由系統 · longhun-persona-router

> **五大人格，各就其位。**
> 龍芯⚡️ 管技术实现，通心譯 管知识传递，龍魂 管安全攻防，君子 管伦理治理，審計 管合规风控。

---

## 一、快速识别

| 属性 | 内容 |
|------|------|
| **名称** | longhun-persona-router（龍魂·人格路由系统） |
| **版本** | v1.0 |
| **定位** | 五大人格实体的加权关键词路由与熔断配置中心 |
| **一句话** | 识别请求气质 → 匹配最合适人格 → 按规则熔断或放行 |
| **核心能力** | 加权关键词匹配 · 语义相似度 · 历史偏好 · 三层监督器 · 五行平衡检查 · 三才验证 |
| **DNA签名** | `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PERSONA-ROUTER-v1.0` |
| **确认码** | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| **硬件靶标** | 華為 TaiShan 200 2280 / 鯤鵬920 ARM64 / SN: 2102314UJFN0S3102797 |

### 🟢🔴🟡 三色审计声明

```
🟢 GREEN（宜做）: 请求清晰 → 人格匹配置信度高 → 按人格专长输出
🔴 RED（禁做）: 置信度低于阈值仍强行路由 · 熔断条件触发后仍放行 · 绕过三层监督器
🟡 YELLOW（慎做）: top_score 与 second_score 差距 < 0.15 时触发多人格会诊
```

---

## 二、五大人格实体

| 人格 | ID | 职责 | 触发气质 | 输出风格 | 审计等级 |
|------|-----|------|----------|----------|----------|
| **龍芯⚡️** | tech_dragon | 技术架构与代码实现 | 代码、架构、部署、优化、调试 | 精确、结构化、代码优先 | STANDARD |
| **通心譯** | edu_translator | 教育教学与双语翻译 | 解释、教程、翻译、入门 | 循序渐进、举例说明、双语对照 | STANDARD |
| **龍魂** | mil_dragon_soul | 军事策略与攻防态势 | 安全、攻防、威胁、指挥决策 | 果断、结构化、等级分明 | STRICT |
| **君子** | phi_gentleman | 伦理哲学与治理思辨 | 伦理、哲学、治理、价值权衡 | 引经据典、辩证分析、层层递进 | STRICT |
| **審計** | law_auditor | 法律合规与审计风控 | 合规、法规、风险、知识产权 | 严谨、条文引用、风险提示 | STRICTEST |

---

## 三、路由算法

### 3.1 加权匹配

```
score = keyword_match * 0.40 + semantic_similarity * 0.40 + history_preference * 0.20
```

### 3.2 决策阈值

| 阈值 | 动作 |
|------|------|
| score ≥ 0.70 | direct_route：直接路由到目标人格 |
| 0.55 ≤ score < 0.70 | multi_persona_consult：触发多人格会诊 |
| score < 0.40 或熔断条件触发 | fuse_block：阻断并转人工 |

### 3.3 熔断条件

- dr∈{3,9,13,19,23,29} 日期熔断
- AI 自审失败
- 置信度 < 0.40
- 五行平衡指数 < 20
- 相克强度 > 0.85
- Human < 0.34 铁律违反

---

## 四、配置文件

**主配置**: `config/persona_router_config.json`

包含：
- 路由引擎算法与权重
- 五大人格完整定义（关键词、阈值、行为画像、审计配置、鲲鹏优化标记）
- 多人格会诊规则
- 三层监督器（感知层 / 认知层 / 决策层）
- CNSH L1-L7 集成开关
- 鲲鹏硬件集成参数

---

## 五、与现有技能的协作边界

| 技能 | 协作关系 |
|------|----------|
| `dragon-soul-agent` | 龍魂智能体入口负责「中文语义理解 + CNSH 命名规范 + 技能路由」。本技能只负责五大人格实体内部路由，不争夺「龍魂」入口词。 |
| `longhun-empower-engine` | 赋能引擎覆盖 10 大类关键字识别与 9 人格分工（P01 诸葛亮、P02 宝宝等）。本技能聚焦五大人格实体（tech / edu / mil / phi / law），互不重叠。 |
| `longhun-tongxinyi` | 通心譯是独立技能，本配置中的「通心譯人格」是其人格化实例之一。 |
| `longhun-innovation` | 穷则变状态机中的「保守者 / 探索者」可由本技能的人格路由实例化。 |
| `longhun-cloud-deploy` | 鲲鹏部署场景下，人格路由与 CNSH 运行时、DNA 追踪器等服务共同编排。 |

---

## 六、文件结构

```
longhun-persona-router/
├── SKILL.md                          # 技能文档
├── config/
│   └── persona_router_config.json    # 五大人格路由配置
├── scripts/
│   ├── 人格路由演示.py               # 加载配置并演示路由
│   └── 路由检查器.py                 # 验证配置完整性与 DNA 签名
└── docs/
    └── 龍魂人格路由架构_鲲鹏版.md     # 架构设计原文
```

---

## 七、使用方法

### 7.1 查看人格路由配置

```bash
python3 ~/.kimi-code/skills/longhun-persona-router/scripts/人格路由演示.py
```

### 7.2 验证配置完整性

```bash
python3 ~/.kimi-code/skills/longhun-persona-router/scripts/路由检查器.py
```

### 7.3 手动测试路由

```python
import json
from pathlib import Path

config = json.loads(Path(
    "~/.kimi-code/skills/longhun-persona-router/config/persona_router_config.json"
).expanduser().read_text())

# 遍历五大人格
for pid, persona in config["personas"].items():
    print(f"{persona['display_name']}: {persona['description']}")
```

---

## 八、DNA 追溯格式

```
#龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}`
例: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PERSONA-ROUTER-v1.0
```

人格内部 DNA：
- 龍芯⚡️: `#龍芯⚡️{YYYY-MM-DD}-TECH-{MODULE}-{VERSION}`
- 通心譯: `#龍芯⚡️{YYYY-MM-DD}-EDU-{MODULE}-{VERSION}`
- 龍魂: `#龍芯⚡️{YYYY-MM-DD}-MIL-{MODULE}-{VERSION}`
- 君子: `#龍芯⚡️{YYYY-MM-DD}-PHI-{MODULE}-{VERSION}`
- 審計: `#龍芯⚡️{YYYY-MM-DD}-LAW-{MODULE}-{VERSION}`

---

## 九、君子协议

本技能所有产出默认 **CC BY-NC-SA 4.0**，来源链不可切断。

> 签署：UID9622 · 龍芯北辰

<!-- DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PERSONA-ROUTER-v1.0 -->
<!-- AUTHOR: UID9622 · 龍芯北辰 -->


---

## 附录：龍魂协议与路由来源

本技能收录了来自 `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂协议与路由` 的素材：

- **内容**：`persona_router_config.json`、`龍魂人格路由架構_鯤鵬版.md`
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-PROTOCOL-ROUTE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 `references/龍魂协议与路由/`，嵌入 DNA 追溯链，与 `longhun-persona-router` 人格路由能力联动。

---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：05-AI人格-Agent（宝宝人格配置、AI 术语对照、智能中枢）
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
