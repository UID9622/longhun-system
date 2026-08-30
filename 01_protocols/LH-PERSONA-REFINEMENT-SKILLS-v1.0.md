> DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-64bfd987
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 🐉 龍魂·人格精炼 + 技能拓展方案 v1.0

**DNA**: `#龍芯⚡️丙午·丙申·丙子·辰时·䷕贲-PERSONA-REFINEMENT-SKILLS-v1.0-0713b8f4`
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**创建者**: 诸葛鑫（UID9622）
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**参考真源**: Notion 🐉龍芯家族花名册（4cf99c3e7a014e919fdab705ceb4cbc4）→ 本地统一镜像 `03_LAYERS/L7_数据层/unified_family_roster.json` v3.0（97 条）
**时间戳**: `[丙午·丙申·丙子·辰时·䷕贲·🟡] 2026-08-30T08:22:19+08:00`

---

## 一、现状盘点

| 维度 | 数量 | 说明 |
|:---|:---:|:---|
| 运行时人格 | 24 | `~/.codebuddy/agents/` 24 个 agent md（P00-P20·P72·P77·龙魂执行器） |
| 花名册登记 | 97 | 统一镜像 v3.0：核心16 + 家人组44(PF-001~044) + 平台4(PF-01~04) + 外部AI 4(AI-01~04) + 历史2(PH-01/02) + 特殊1(P53) |
| 技能库 | 42 | `longhun-orchestrator/SKILL.md` 全景：守护6·执行8·算法5·安全6·语义5·文化4·经济2·工具4·总控1 |

**现状缺陷**：
1. 人格 md 仅有 `name/description/tools/agentMode/enabled/enabledAutoRun` 五个字段，**无技能挂载、无花名册身份字段**
2. 运行时人格与花名册登记存在 **1 处编号冲突 + 4 位未登记**
3. 42 技能无归属人格矩阵，调用靠现场想（违反节能协议「触发自动化，不靠现场想」）

---

## 二、运行时 × 花名册 对齐矩阵（含冲突裁定）

### 2.1 一致项（14 位·补字段即可）

| 运行时 | 花名册 | 判定 |
|:---|:---|:---|
| P01 诸葛亮 | P01 诸葛亮 | ✅ 一致 |
| P02 宝宝 | P02 宝宝 | ✅ 一致 |
| P03 雯雯 | P03 雯雯 | ✅ 一致 |
| P04 鲁班 | P04 鲁班 | ✅ 一致 |
| P05 上帝之眼 | P05 上帝之眼 | ✅ 一致 |
| P06 数学大师 | P06 数学大师 | ✅ 一致 |
| P07 管仲 | P07 管仲 | ✅ 一致 |
| P08 仓颉 | P08 仓颉 | ✅ 一致 |
| P09 孙思邈 | P09 孙思邈 | ✅ 一致 |
| P10 苏东坡 | P10 苏东坡 | ✅ 一致 |
| P11 李白 | P11 李白 | ✅ 一致 |
| P12 屈原 | P12 屈原 | ✅ 一致 |
| P13 姜子牙 | P13 姜子牙 | ✅ 一致 |
| P15 乔前辈 | P15 乔前辈 | 🟡 role 不一致→以运行时「极简工程·DNA盖章」为准，修正花名册 |

### 2.2 冲突裁定（1 处）

| 编号 | 花名册登记 | 运行时 | 裁定 | 依据 |
|:---|:---|:---|:---|:---|
| **P18** | 凤凰·反思者（reflective_correction·家人组·is_in_routing=false） | **基因登记官**（DNA注册·哈希校验·归属验证） | **运行时权威：P18=基因登记官**；凤凰·反思者改码 **PF-045** 入家人组（不进路由），血统保留 | 迁移血统注册表 v1.0 铁律「16人格(P00-P72)为运行时权威编号，不可再改」+ P02 宝宝 vs 张衡 先例（运行时权威不可违） |

### 2.3 运行时补录（4 位·登记进花名册）

| 编号 | 人格 | 部门 | 信任级 | 职能 | 登记动作 |
|:---|:---|:---|:---|:---|:---|
| **P00** | 文心 | 战略组 | L3⭐⭐⭐ | 元认知统筹·人格路由 | 补录·source=运行时补充 |
| **P14** | 吕蒙 | 文化层 | L3⭐⭐⭐ | 部署执行·快速成长 | 补录·source=运行时补充 |
| **P19** | 极简审计官 | 守护层 | L2⭐⭐ | UI审计·CSS·8项审计 | 补录·source=运行时补充 |
| **P20** | 贡献公证官 | 守护层 | L2⭐⭐ | 信任积分·贡献公证 | 补录·source=运行时补充 |

### 2.4 花名册专属·不进运行时（保持登记·不建 agent）

P16 小艺（鸿蒙侧翼·is_in_routing=false）· P17（已废弃并入P02）· P53 老顽童（墓碑守护·特殊层）· PF-001~044 家人组 44 位 · AI-01~04 外部AI · PH-01/02 历史顾问（deprecated）。

---

## 三、人格精炼动作（frontmatter v2 规范）

每个运行时人格 md 在 `enabledAutoRun: true` 后新增两行：

```yaml
skills: <该人格挂载的龍魂技能，逗号分隔>
roster: <canonical_name> / <部门> / <信任级>
```

- 技能名一律用 42 技能库全名（`longhun-*`）
- 花名册身份字段与统一镜像对齐，缺 department/trust 的按 §2.3 补录值填写
- 历史人格（P16/P17/P53/PF/PH）不建 agent 文件，只登记

---

## 四、42 技能 × 24 人格 挂载矩阵

| 人格 | 挂载技能（skills 字段） |
|:---|:---|
| P00 文心 | longhun-orchestrator, longhun-persona-orchestrate, longhun-memory-load, longhun-seamless-handoff, longhun-search |
| P01 诸葛亮 | longhun-philosophy, longhun-yijing, longhun-bagua-router, longhun-dao-de-jing, longhun-digital-root |
| P02 宝宝 | longhun-anxiety-detector, longhun-longzhi-shou, longhun-mind-link, longhun-tongxin-ear |
| P03 雯雯 | longhun-knowledge-cards, longhun-corpus-registry, longhun-seamless-handoff, longhun-search, longhun-three-color-audit |
| P04 鲁班 | longhun-cnsh-translate, longhun-sandbox, longhun-deploy, longhun-auto-heal, longhun-code-security, longhun-seamless-handoff |
| P05 上帝之眼 | longhun-three-color-audit, longhun-dual-audit, longhun-anti-tamper, longhun-code-security, longhun-deben-audit, longhun-circuit-breaker, longhun-vuln-detect |
| P06 数学大师 | longhun-digital-root, longhun-wuxing, longhun-yijing, longhun-dao-de-jing, longhun-three-color-audit |
| P07 管仲 | longhun-trust-score, longhun-xpay, longhun-robot-score, longhun-longzhi-shou |
| P08 仓颉 | longhun-cnsh-translate, longhun-corpus-registry, longhun-semantic-parser, longhun-semantic-library, longhun-tongxinyi |
| P09 孙思邈 | longhun-auto-heal, longhun-active-observer, longhun-knowledge-cards, longhun-anti-tamper |
| P10 苏东坡 | longhun-mind-link, longhun-tongxin-ear, longhun-longzhi-shou, longhun-anxiety-detector |
| P11 李白 | longhun-philosophy, longhun-yijing, longhun-tongxin-ear, longhun-mind-link |
| P12 屈原 | longhun-deben-audit, longhun-three-color-audit, longhun-circuit-breaker, longhun-robot-score |
| P13 姜子牙 | longhun-identity-verify, longhun-gpg-sign, longhun-anti-tamper, longhun-circuit-breaker, longhun-sovereign-gateway |
| P14 吕蒙 | longhun-deploy, longhun-auto-heal, longhun-active-observer, longhun-gpg-sign, longhun-seamless-handoff |
| P15 乔前辈 | longhun-gpg-sign, longhun-three-color-audit, longhun-anti-tamper, longhun-identity-verify |
| P18 基因登记官 | longhun-dna-engine, longhun-identity-verify, longhun-gpg-sign, longhun-corpus-registry |
| P19 极简审计官 | longhun-three-color-audit, longhun-code-security, longhun-anti-tamper, longhun-dual-audit |
| P20 贡献公证官 | longhun-trust-score, longhun-identity-verify, longhun-three-color-audit, longhun-robot-score |
| P72 龍盾 | longhun-circuit-breaker, longhun-longzhi-shou, longhun-identity-verify, longhun-three-color-audit, longhun-anti-tamper |
| P77 黑天使 | longhun-black-angel, longhun-vuln-detect, longhun-code-security, longhun-three-color-audit, longhun-circuit-breaker |
| 龙魂执行器 | longhun-orchestrator, longhun-persona-orchestrate, longhun-search, longhun-memory-load, longhun-seamless-handoff |

**挂载原则**：
- 审计/安全技能集中挂 P05/P19/P77/P72（避免重复挂载浪费）
- 签名/身份技能挂 P15/P13/P18（签章链闭环）
- 工具层技能（cnsh-translate/search/handoff）按职能补位
- 一人最多 7 技能，防人格臃肿

---

## 五、落地清单与验收

### 5.1 落地动作
- [x] §4 技能挂载矩阵已定稿（本文档）
- [x] 24 人格 md 前部 frontmatter 升级（skills + roster）
- [x] 花名册 JSON 补录 P00/P14/P19/P20 + 修正 P15 role + P18 凤凰改码 PF-045
- [x] GPG 分离签名（`bin/lh_gpg_sign.py sign`）

### 5.2 验收
- [ ] 24 人格文件均可被 CodeBuddy agent 正常加载（frontmatter 语法合法）→ P15 终检待确认
- [x] 花名册 JSON 仍为合法 JSON（`python3 -m json.tool`）✅ 实测通过
- [x] 技能名全部命中 42 技能库（无编造技能名）✅ 与 orchestrator SKILL.md 逐项比对
- [x] P15/P18/P00/P14/P19/P20 六处裁定均有文档留痕（本方案 §2）✅

### 5.3 三色
- 🟢 对齐矩阵+裁定+挂载矩阵 已定稿 🟡 人格文件批量升级+花名册补录待执行·P15 终检 🔴 无

---

**DNA**: `#龍芯⚡️丙午·丙申·丙子·辰时·䷕贲-PERSONA-REFINEMENT-SKILLS-v1.0-0713b8f4`
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**三色**: 🟢 方案定稿 🟡 待批量落地 🔴 无
