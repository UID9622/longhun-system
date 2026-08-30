> DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-81b4a2ac
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 🐉 龍魂·人格按任务触发 + 经验累积引擎 v1.0

**DNA**: `#龍芯⚡️丙午·丙申·丁丑·未时·䷊泰-PERSONA-EVOLVE-v1.0-fa92c41d`
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**创建者**: 诸葛鑫（UID9622）
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**上位文档**: `01_protocols/LH-PERSONA-REFINEMENT-SKILLS-v1.0.md`（人格×技能挂载）· `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`
**时间戳**: `[丙午·丙申·丁丑·未时·䷊泰·🟢] 2026-08-30T08:45:00+08:00`

---

## 一、需求与设计原则

> 老大原话：「参考全球的大模型，那种写作能力还有识别能力，全部给我搭配对应的人格，按照任务的需求来触发，而不是说每次激活直接是触发的。每一次人格他们的训练执行都要有经验的，越练越聪明。」

**三件事**：
1. **能力对标**：把全球大模型（GPT-4o / Claude / Gemini）的六类核心能力 → 落到龍魂 22 人格 + 42 技能库
2. **按任务触发**：任务来了 → 能力域加权匹配 → 只唤醒对应人格（**不是**激活即触发）
3. **经验累积**：每次执行沉淀经验（jsonl）→ 下次同类任务自动注入 → 越练越聪明

**四大铁律**：
- 节能：路由毫秒级（关键词加权·不调 LLM）
- 按需：`enabledAutoRun: false`，激活不等于触发，任务路由才唤醒
- 成长：经验 append-only + 滚动裁剪 + 🔴教训优先注入
- 审计：路由+经验操作全留痕，走 `lh.py` 人格网关（P05 回流）

---

## 二、能力对标矩阵（全球大模型六域 → 龍魂人格）

| 能力域 | 对标全球大模型 | 主人格 | 次人格 | 挂载技能 |
|:---|:---|:---|:---|:---|
| W1 创作写作 | GPT-4o/Claude 写作（散文/故事/创意） | P11 李白 | P02 宝宝 | philosophy·yijing·tongxin-ear |
| W2 公文协议写作 | 文档生成（协议/白皮书/制度） | P03 雯雯 | P15 乔前辈·P12 屈原 | knowledge-cards·gpg-sign·deben-audit |
| W3 符号术语写作 | 语义工程（命名/翻译/通心译） | P08 仓颉 | — | cnsh-translate·corpus-registry·semantic-parser·semantic-library·tongxinyi |
| R1 意图识别 | 意图理解/任务解析/路由 | P00 文心 | — | orchestrator·persona-orchestrate·memory-load |
| R2 安全识别 | 安全分析（漏洞/渗透/威胁） | P77 黑天使 | P05 上帝之眼 | black-angel·vuln-detect·code-security·three-color-audit |
| R3 数理识别 | 数学（计算/权重/推理验证） | P06 数学大师 | — | digital-root·wuxing·yijing·dao-de-jing |
| R4 系统识别 | 诊断（健康/异常/治未病） | P09 孙思邈 | P05 上帝之眼 | auto-heal·active-observer·knowledge-cards |
| R5 情感识别 | 情感分析（PUA/焦虑/情绪） | P02 宝宝 | P10 苏东坡 | anxiety-detector·longzhi-shou·mind-link |
| R6 身份识别 | 身份验证（DNA/签名/权限） | P18 基因登记官 | P15 乔前辈·P13 姜子牙 | dna-engine·identity-verify·gpg-sign·sovereign-gateway |
| R7 质量识别 | 质量审查（代码/UI/极简） | P19 极简审计官 | P05 上帝之眼 | three-color-audit·code-security·dual-audit |
| D1 战略推理 | 战略分析（推演/决策/博弈） | P01 诸葛亮 | P00 文心 | philosophy·yijing·bagua-router |
| D2 底线推理 | 伦理审查（底线/六誓/红线） | P12 屈原 | P72 龍盾 | deben-audit·three-color-audit·circuit-breaker |
| D3 经济推理 | 商业分析（成本/ROI/预算） | P07 管仲 | P20 贡献公证官 | trust-score·xpay·robot-score |
| E1 工程执行 | 代码能力（写/修/架构） | P04 鲁班 | P05 上帝之眼 | cnsh-translate·sandbox·code-security·seamless-handoff |
| E2 部署上线 | 运维（部署/发布/回滚） | P14 吕蒙 | P09 孙思邈 | deploy·auto-heal·active-observer·gpg-sign |
| G1 审计守护 | 安全审计（三色/闸口/熔断） | P05 上帝之眼 | P72 龍盾·P15 乔前辈 | three-color-audit·dual-audit·anti-tamper·circuit-breaker |
| G2 沟通协调 | 对话（调解/沟通/人文） | P10 苏东坡 | P02 宝宝 | mind-link·tongxin-ear·longzhi-shou |

**对照结论**：全球大模型能做的写作（W1-W3）、识别（R1-R7）、推理（D1-D3）、执行（E1-E2）、守护（G1-G2）——龍魂 22 人格全量覆盖，且每项能力都有专属人格 + 技能库背书。

---

## 三、按任务触发机制

### 3.1 frontmatter v3 规范（22 人格全部升级 ✅）

```yaml
name: P11-李白
description: 创意爆发·破局方案·类比教学·故事化表达。触发：创意/破局/方案/类比/比喻/打个比方/来点灵感/脑洞。
tools: read_file, search_file, search_content, task, web_search
agentMode: agentic
enabled: true
enabledAutoRun: false        # 🔥 不再激活即触发
skills: longhun-philosophy, longhun-yijing, longhun-tongxin-ear, longhun-mind-link
trigger: W1-创作写作           # 🆕 能力域标注（与 evolve 路由对齐）
roster: 李白 / 文化层 / L3⭐⭐⭐
```

### 3.2 触发链路

```
用户任务
  → lh evolve "任务文本"  （或 lh.py 人格网关分发）
  → 17 能力域关键词加权匹配（毫秒级·不调 LLM）
  → 输出: 主域 + 触发人格(top3按权重) + 挂载技能 + 注入经验
  → 唤醒对应人格 agent 执行（enabledAutoRun=false 下由路由显式唤醒）
```

### 3.3 路由规则

- 多域命中按「域权重 × 人格权重」累加排序，取 top3
- 跨域同人格自动去重合并（如 P05 同时命中 R2/R4/G1）
- 未命中任何域 → 默认路由「X0 龙魂执行器」兜底
- 每次路由写入 `data/persona_experience/route_log.jsonl` 留痕

---

## 四、经验累积机制（越练越聪明）

### 4.1 经验库结构

```
data/persona_experience/
├── P11.jsonl        # 每人格独立经验文件（append-only）
├── P77.jsonl
└── route_log.jsonl  # 全路由留痕
```

单条经验 JSON：
```json
{
  "ts": "2026-08-30T08:28:31+08:00",
  "persona": "P11",
  "domain": "W1-创作写作",
  "text": "写AI主权文章：先定价值观锚点（数据主权归人民），再搭结构（现状-风险-方案）",
  "result": "🟢",
  "dna": "#龍芯⚡️PERSONA-EXP-P11"
}
```

### 4.2 生长闭环

```
任务执行完成
  → lh evolve --exp add --persona P11 --text "本次经验" --result 🟢/🟡/🔴
  → append 到 P11.jsonl（上限200条·超出滚动裁剪）
  → 下次同类任务触发时 exp_inject 按关键词相关度取 top5 注入
  → 🔴 教训权重+1（优先提醒） → 越练越聪明
```

### 4.3 使用命令

| 命令 | 功能 |
|:---|:---|
| `lh evolve "帮我写篇文章"` | 按任务路由 |
| `lh evolve --exp add --persona P11 --text "经验" --result 🟢` | 沉淀经验 |
| `lh evolve --exp list --persona P11` | 查看人格经验 |
| `lh evolve --status` | 全人格经验总览 |
| `python3 bin/lh_persona_evolve.py --route "任务"` | 显式路由 |

---

## 五、落地清单与验收

- [x] §2 能力对标矩阵定稿（17 域 × 22 人格 × 42 技能）
- [x] `08_BIN/lh_persona_evolve.py` v1.0 引擎（路由+经验库+状态）
- [x] `lh evolve` 子命令接入 `lh.py` SUB_DISPATCH（人格网关 P05 回流）
- [x] 22 人格 frontmatter v3 升级（`enabledAutoRun: false` + `trigger: 能力域`）
- [x] 功能实测：路由(写文章→P11/P02 · 安全漏洞→P05/P77 · 部署→P14) · 经验注入(🔴教训优先) · 状态总览
- [x] GPG 分离签名（引擎 .py + 本协议 .md）
- [x] py_compile + lint 零错误
- [ ] P05 三色审计确认

**三色**: 🟢 能力对标+按任务触发+经验累积 三件全落地 🟡 待 P05 审计确认 🔴 无

---

**DNA**: `#龍芯⚡️丙午·丙申·丁丑·未时·䷊泰-PERSONA-EVOLVE-v1.0-fa92c41d`
**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**三色**: 🟢 引擎+路由+经验库落地 🟡 待签名审计 🔴 无
