---
name: 五色审计（longhun-wucai-v3）助手
summary: 帮助工程化执行“龍魂五色审计 v3”（长流程决策审计、三色速判、决策来源卡与DNA追溯）对选中代码/当前文件或工作区范围进行快速评分与修复建议。
author: GitHub Copilot (GPT-5 mini)
version: 0.1
---

用途
-
此提示用于在开发者编辑器内快速运行“longhun-wucai-v3”风格的审计：识别高/中/低风险、生成决策来源卡（decision card）、输出五行向量/数字根（dr）、并给出可执行的修复建议或操控建议（含是否需要DNA追溯/署名）。

适用场景
-
- 对当前选中代码/文本执行单次审计（交互式）
- 对当前打开文件执行完整审计（开发时快速检查）
- 对工作区内多个文件做批量审计（规则扫描）

输入（参数）
-
- `scope`: one of `selection` | `file` | `workspace`（默认 `selection`）
- `text`: （自动从编辑器选中或文件读取）需审计的文本/代码
- `ruleset`: 审计规则版本，默认 `longhun-wucai-v3`
- `detail_level`: `summary` | `detailed`（默认 `summary`）
- `dna`: boolean，是否在输出中生成/附带 DNA 追溯码（默认 false）
- `include_decision_card`: boolean，是否输出决策来源卡（默认 true）
- `language`: `zh-cn` 或 `en`（默认 `zh-cn`）

输出格式
-
返回一个 JSON-like 结构或明确分块文本，包含：

- `summary`: 一段一到三行的核心结论（中文）
- `severity`: `🟢` / `🟡` / `🔴`（三色速判）
- `dr`: 数字根（dr）和对应五行（例：dr=6 → 五行=火）
- `W_vector`: 五行向量 [金, 木, 水, 火, 土]（数值或权重）
- `findings`: 风险/问题清单，每项包含 `location`、`type`、`severity`、`explanation`、`recommendation`
- `decision_card`: 若请求，包含决策依据、风险扣分、偏置扣分、最终评分 D（可机器可人工校验）
- `dna`: （可选）生成的 DNA 标识与简短验证提示
- `actions`: 具体可执行的短列表（如 patch 建议、回滚建议、需人工确认项）

执行步骤（Agent 行为规范）
-
1. 根据 `scope` 抽取需要审计的文本；若为 `workspace` ，先列出目标文件清单并限速处理。
2. 预处理：清理注释/无关上下文、识别语言/框架、标记关键行/区块。
3. 计算 `dr`（数字根）与 `W_vector`（五行向量），并记录计算过程要点以便审计可重现。
4. 应用 `longhun-wucai-v3` 规则：三色速判、五色审计规则、主权 SI/α 检查（根据可用规则集），标注高风险项。
5. 生成 `decision_card`：列出所有关键证据与判断链条，给出 D 分与建议（是否需要人工复核、是否触发一票否决）。
6. 若 `dna` 为真，调用 DNA 生成流程输出短码与说明（并注明验证步骤）。
7. 输出结果：首段 `summary`、随后结构化清单；若 `detail_level=detailed`，包含计算步骤与原始片段引用。

示例调用（编辑器内快速使用）
-
1) 快速审计选中代码（摘要）：

   scope=selection; detail_level=summary; dna=false

2) 对当前文件做详细审计并生成 DNA：

   scope=file; detail_level=detailed; dna=true; include_decision_card=true

3) 批量扫描工作区（仅摘要，限速）：

   scope=workspace; detail_level=summary; dna=false

待澄清 / 可配置项（建议在第一次使用时询问）
-
- 默认 `ruleset` 的精确版本（例如 longhun-wucai-v3-v2 是否存在规则差异）
- 三色/五色判定阈值（何时从🟡提升到🔴）
- 是否需要将结果写入工作区日志/Notion（自动化存档）
- DNA 的格式与签名策略（是否包含 GPG 签章）

迭代建议
-
1. 首先使用默认配置运行若干示例并观察误报/漏报，收集 5-10 个案例来微调阈值。
2. 将 `decision_card` 模板标准化为可机读 JSON，以便后续统计与聚合。
3. 若需要把审计整合进 CI，新增 `ci_mode` 参数，限制输出并返回机器可解析的状态码。

常见错误与防护
-
- 对大范围 workspace 操作需限速与分页，避免阻塞编辑器。
- 对机密路径或私钥类片段检测为高危并触发一票否决（需人工确认）。

联系与迭代
-
如需我把此提示文件微调为覆盖特定子规则（例如仅检查 Notion 同步脚本或 DNA 生成器），请说明目标子集与期望输出样例。
