# 算法公式 ↔ IPA ↔ Skill 对齐总表 v1.1（补全草案）

> 用途：给 Notion「45公式对照表」补空位。  
> 原则：已知写实装；冲突写冲突；缺资料写「待校验」，不冒充完成。  
> 父表：`cnsh-core/规范/算法公式IPA对齐总表_v1.0.md`

DNA: `#龍芯⚡️2026-05-16-IPA-MATH-FORMULA-ALIGN-v1.1-DRAFT`  
确认: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 一、先说清楚：两套编号别混

| 口径 | 人话 |
|---|---|
| `F01-F45` | 数学公式总册里的公式编号 |
| `公式01/02/10/11/12...` | 技能/协议里常说的功能公式编号 |

所以表里有些地方会出现：`F02 不动点` 和 `公式02 贡献值` 同时存在。  
这不是你搞错，是两套编号历史上叠在一起了；本表先**对账**，后面再决定是否统一重编号。

---

## 二、45公式对照表（可粘贴到 Notion）

| F号 | 公式/模块名 | 一句话用途 | IPA / 路由建议 | 本地落点 / skill | 状态 |
|---|---|---|---|---|---|
| F01 | 数字根 `dr(n)` | 把数字压到 1-9，给闸门/五行用 | `[IPA-FLOW-GATE-DR]` | `gate_v3` / `wuxing-check` | 🟢 已对齐 |
| F02 | 不动点 `f(x*)=x*` | 判断系统是否收敛到稳定点 | `[IPA-FLOW-DECISION-CORE]` | 洛书/守恒类内部触发 | 🟡 待挂 skill |
| F03 | 洛书矩阵 | 九宫派位骨架 | `[IPA-FLOW-PALACE-ROUTER]` | `洛书守恒检查()` | 🟢 已实装 |
| F04 | 洛书守恒 15 | 行列对角守恒 | `[IPA-FLOW-PALACE-ROUTER]` | `洛书守恒检查()` | 🟢 已实装 |
| F05 | 三才向量 | 天/地/人加权评分 | `[IPA-FLOW-GATE-SANCAI]` | `sancai_vector()` | 🟢 已实装 |
| F06 | Perlin 多频噪声 | 流场可视化/扰动模拟 | `[LOCAL-FLOW-VISUAL]` | widget 有，算法层待补 | 🟡 待算法层 |
| F07 | 369 共振 | 369 节律/共振判断 | `[IPA-FLOW-RESONANCE-369]` | 待写 `resonance_369()` | 🟡 待实装 |
| F08 | 时间衰减 | 判断内容还剩多少有效性 | `[META-THEORY-v1.0]` | `time-decay` | 🟢 已对齐 |
| F09 | 余弦相似度 | 判断两段内容像不像 | `[IPA-SIMILARITY-CHECK]` | 待装 `similarity-check` | 🟡 待 skill |
| F10 | 三色风险 | 绿/黄/红风险判定 | `[GATE-04]` / `[IPA-FLOW-GATE-AUDIT]` | `veto-alert` / CNSW | 🟢 已对齐 |
| F11 | 守恒分数 S | 判断窗口/任务还稳不稳 | `[CENTER-AUDIT]` | `shouheng-check` | 🟢 已对齐 |
| F12 | 决策路径 D / 加权评分 | 给方案选择打分 | `[IPA-FLOW-DECISION-CORE-v4.1]` | `decision-card` | 🟢 已对齐 |
| F13 | 人性偏置 H | 识别人性/情绪偏置扣分 | `[IPA-FLOW-DECISION-CORE-v4.1]` | `decision-card` | 🟢 已对齐 |
| F14 | 数字根三色闸 | `dr=3/9` 红，`6` 黄，其余绿 | `[IPA-FLOW-GATE-DR]` | `gate_v3.gate_color()` | 🟢 已实装 |
| F15 | DNA SHA-256 | 给内容生成追溯身份证 | `[LOCAL-DNA-GEN-V2]` | `dna-gen` / `dna_generator_v2` | 🟢 已对齐 |
| F16 | 父子链 / 链式留痕 | 把前后记录串起来 | `[IPA-FLOW-DNA-CHAIN]` | `chain_hash.jsonl` / `dna_chain_tracer` | 🟡 待统一 |
| F17 | 人格叠加 `|Ψ⟩` | 多人格并存的状态表达 | `[LOCAL-PERSONA-SCHEDULER]` | 待装 `persona-scheduler` | 🟡 孤儿公式 |
| F18 | 人格选择 / 三才主权 SI | **命名冲突**：引擎里是 `P*`，论文里是 `SI` | `[IPA-FLOW-GATE-SANCAI]` / `[PERSONA]` | `sancai_score()` / 待拆名 | 🟡 需定名 |
| F19 | 五行对冲 H / 印记主权 ISI | **命名冲突**：对冲指数 vs H武器 ISI | `[IPA-FLOW-GATE-SHENGKE]` / `[LOCAL-WATERMARK]` | `计算五行对冲指数()` / `dna_imprint_renderer.py` | 🟡 需拆名 |
| F20 | 五行向量 W(x) | 把文本打成金木水火土向量 | `[IPA-FLOW-WUXING-MAP]` | `wuxing-check` / `五行向量签名()` | 🟢 已对齐 |
| F21 | 生克关系 | 判断五行相生/相克 | `[IPA-FLOW-GATE-SHENGKE]` | `shengke_relation.py` | 🟢 有模块 |
| F22 | 路径信息量 24bit | 衡量路径/链路信息含量 | `[IPA-ROUTE-REGISTRY]` | 文档有，算法待补 | 🟡 待实装 |
| F23 | 沙盒分拣 | 把输入分桶，不直接进核心 | `[IPA-FLOW-SANDBOX-BUCKET]` | `sandbox_bucket.py` | 🟢 有模块 |
| F24 | 宫位路由 | 把任务派到九宫/宫位 | `[IPA-FLOW-PALACE-ROUTER]` | `palace_router.py` | 🟢 有模块 |
| F25 | 审计门 | 输入/输出先过审计 | `[IPA-FLOW-GATE-AUDIT]` | `audit_gate.py` / CNSW | 🟢 有模块 |
| F26 | 路由注册表 | 编号查地址 | `[IPA-ROUTE-REGISTRY]` | `ipa_route_registry.py` / `route-find` | 🟢 有模块 |
| F27 | 砂箱权重 / 分流权重 | 判断东西进哪一桶 | `[IPA-FLOW-SANDBOX-BUCKET]` | 待统一到分桶引擎 | 🟡 待整理 |
| F28 | 贡献值 C | 判断规则/文件值不值得留 | `[IPA-FLOW-DNA-CHAIN]` | `contrib-eval` | 🟢 已对齐 |
| F29 | 时间层级 L0-L4 | 判断保存期限/衰减层 | `[META-THEORY-v1.0]` | `time-decay` | 🟢 已对齐 |
| F30 | 迭代收敛 `x_{t+1}=F(x_t)` | 判断系统会不会收束 | `[IPA-FLOW-DECISION-CORE]` | `公式对准引擎.py` 速查有 | 🟡 待挂 |
| F31 | 五行签名·金 | 规则/结构维度签名 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F32 | 五行签名·木 | 生长/扩展维度签名 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F33 | 五行签名·水 | 流动/上下文维度签名 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F34 | 五行签名·火 | 执行/触发维度签名 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F35 | 五行签名·土 | 承载/归档维度签名 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F36 | 五行评分串 | 把五行向量压成可比对字符串 | `[LOCAL-WATERMARK]` | `五行向量签名()` | 🟢 已实装 |
| F37 | 五行 DNA 联动 | 五行签名接 DNA 追溯 | `[LOCAL-WATERMARK]` / `[LOCAL-DNA-GEN-V2]` | `dna-gen` 联动 | 🟢 已实装 |
| F38 | 民主回复六维 | 检查 AI 回复是否守主权/边界 | `[CENTER-UNDERSTAND]` | `民主回复校验()` | 🟢 已实装 |
| F39 | 责任卡完整度 | 检查触发/依据/备选/选择/责任是否齐 | `[LOCAL-DECISION-CARD]` | `cnsh/decision_cards` | 🟢 新增骨架 |
| F40 | CNSW 漂移分 | 判断输出是否被话术/钩子带偏 | `[CNSW-HOOK-SCAN]` | `scan_output()` | 🟢 已实装 |
| F41 | 余弦相似度 | `sim(a,b)` 内容相似度 | `[IPA-SIMILARITY-CHECK]` | `公式对准引擎.py` 速查有 | 🟡 待 skill |
| F42 | 伪代码审计 | 检查代码块是不是未标注草稿/留白 | `[CNSW-PSEUDOCODE-AUDIT]` | `pseudocode_audit.py` | 🟢 已实装 |
| F43 | 本地模型记忆镜像 | 对账 Ollama / 仓库 Modelfile / 模型列表 | `[LOCAL-MODEL-MEMORY]` | `sync_ollama_memory_export.py` | 🟢 已实装 |
| F44 | 鲁班绿闸提交 | staged diff + CNSW + dr 通过后本地 commit | `[P04-LUBAN-GREEN-COMMIT]` | `luban_commit.py` | 🟢 已实装 |
| F45 | 双视角封装 M:: × CNSH:: | M 验收，CNSH 路由归属 | `[IPA-DICTIONARY]` / `[M-CNSH-DUAL-VIEW]` | 协议待落代码 | 🟡 待落字段 |

---

## 三、需要你定盘的 3 个冲突

| 冲突点 | 现在情况 | 建议 |
|---|---|---|
| F18 | 引擎里是人格选择，论文/压缩里是三才主权 SI | 拆成 `F18A 人格选择`、`F18B 三才主权 SI`，或把其中一个改到 F46 |
| F19 | 既是五行对冲 H，又是 H武器印记主权 ISI | 拆名：`F19-H 五行对冲`、`F19-ISI 印记主权` |
| F31-F37 | 目前被五行签名占用，Notion 若另有通心译应用层定义会冲突 | 先保留本地已实装口径；Notion 真源出现后再重排 |

---

## 四、可直接贴在 Notion 表下面的短说明

```text
补全说明：
本表先按“本地已实装 + IPA路由 + skill触发”补齐 45 行。
🟢 = 已有本地实现或明确 skill；
🟡 = 有公式/文档/模块，但还缺统一命名、skill 或算法层；
🔴 = 暂无可执行落点。

F18/F19 存在历史命名冲突，暂不强行定死，等 UID9622 定盘后拆名或重编号。
```

