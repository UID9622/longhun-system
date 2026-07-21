> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：协议 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-03-IPA-ROUTE-REGISTRY-LOCAL-FILE1-FILE1-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

{"node_id": "IPA-L1-006", "name": "downloads_inbox", "node_type": "ARCHIVAL", "status": "🟡", "local_path": "03_知識圖譜/downloads_inbox_index.md", "notion_url": null, "entry_point": "generate_downloads_inbox.py", "dna": "#龍芯⚡️2026-06-22-DOWNLOADS-INBOX-IPA-v1.0", "layer": "L1_SEASONAL", "description": "Downloads 顶层交付物收件箱：扫描未录入主干的文件包并生成可审计索引", "tags": ["L1", "inbox", "downloads", "knowledge_graph", "audit"], "dependencies": ["IPA-L0-004", "IPA-L1-001"], "created_at": "2026-06-22T12:49:49.427951", "updated_at": "2026-06-22T12:49:49.427958", "metadata": {"manifest": "03_知識圖譜/downloads_inbox_manifest.json", "source": "~/Downloads"}}
---

# 龍魂·IPA路由注册表 (Append-Only JSONL)
# DNA:#龍芯⚡️2026-06-03-IPA-ROUTE-REGISTRY-LOCAL-FILE1-v1.0
# 格式: JSONL（JSON Lines）- 仅追加，不覆盖
# 每行一条节点记录
# 开始时间: 2026-06-03T2026-06-03T15:03:09.562407
# ═══════════════════════════════════════════════════
{"node_id": "IPA-L0-001", "name": "constitution", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.constitution", "notion_url": null, "entry_point": "get_system_config", "dna": "#龍芯⚡️2026-06-03-PROTOCOL-REGISTRY-v1.0", "layer": "L0_ETERNAL", "description": "系统宪法和基础配置", "tags": ["L0", "config", "foundation"], "dependencies": [], "created_at": "2026-06-03T15:03:09.562464", "updated_at": "2026-06-03T15:03:09.562466", "metadata": {}}
{"node_id": "IPA-L0-002", "name": "identity", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.identity", "notion_url": null, "entry_point": "generate_identity_proof", "dna": "#龍芯⚡️2026-06-03-IDENTITY-v1.0", "layer": "L0_ETERNAL", "description": "三重身份验证系统", "tags": ["L0", "security", "authentication"], "dependencies": ["IPA-L0-001"], "created_at": "2026-06-03T15:03:09.562470", "updated_at": "2026-06-03T15:03:09.562471", "metadata": {}}
{"node_id": "IPA-L0-003", "name": "permissions", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.permissions", "notion_url": null, "entry_point": "get_rbac_system", "dna": "#龍芯⚡️2026-06-03-PERMISSIONS-v1.0", "layer": "L0_ETERNAL", "description": "RBAC权限控制系统", "tags": ["L0", "security", "governance"], "dependencies": ["IPA-L0-001", "IPA-L0-002"], "created_at": "2026-06-03T15:03:09.562473", "updated_at": "2026-06-03T15:03:09.562474", "metadata": {}}
{"node_id": "IPA-L0-004", "name": "dna", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.dna", "notion_url": null, "entry_point": "get_dna_generator", "dna": "#龍芯⚡️2026-06-03-DNA-v1.0", "layer": "L0_ETERNAL", "description": "DNA追溯码生成和验证", "tags": ["L0", "traceability", "identity"], "dependencies": ["IPA-L0-001"], "created_at": "2026-06-03T15:03:09.562475", "updated_at": "2026-06-03T15:03:09.562476", "metadata": {}}
{"node_id": "IPA-L0-005", "name": "logging", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.logging", "notion_url": null, "entry_point": "get_system_log", "dna": "#龍芯⚡️2026-06-03-LOGGING-v1.0", "layer": "L0_ETERNAL", "description": "Append-Only日志系统", "tags": ["L0", "audit", "storage"], "dependencies": ["IPA-L0-001", "IPA-L0-004"], "created_at": "2026-06-03T15:03:09.562478", "updated_at": "2026-06-03T15:03:09.562478", "metadata": {}}
{"node_id": "IPA-L0-006", "name": "mathematics", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.mathematics", "notion_url": null, "entry_point": "get_formula_executor", "dna": "#龍芯⚡️2026-06-03-MATHEMATICS-v1.0", "layer": "L0_ETERNAL", "description": "数学公式和算法核心", "tags": ["L0", "algorithm", "logic"], "dependencies": ["IPA-L0-001"], "created_at": "2026-06-03T15:03:09.562480", "updated_at": "2026-06-03T15:03:09.562481", "metadata": {}}
{"node_id": "IPA-L1-001", "name": "scheduler", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.scheduler", "notion_url": null, "entry_point": "get_scheduler", "dna": "#龍芯⚡️2026-06-03-SCHEDULER-v1.0", "layer": "L1_SEASONAL", "description": "执行调度和任务管理", "tags": ["L1", "scheduling", "automation"], "dependencies": ["IPA-L0-001", "IPA-L0-005"], "created_at": "2026-06-03T15:03:09.562482", "updated_at": "2026-06-03T15:03:09.562483", "metadata": {}}
{"node_id": "IPA-L1-002", "name": "rule_engine", "node_type": "GATE", "status": "🟢", "local_path": "cnsh_core.rules", "notion_url": null, "entry_point": "get_rule_engine", "dna": "#龍芯⚡️2026-06-03-RULE-ENGINE-v1.0", "layer": "L1_SEASONAL", "description": "规则引擎·守门人·业务规则执行器", "tags": ["L1", "rules", "gate", "decision"], "dependencies": ["IPA-L0-001", "IPA-L0-002", "IPA-L0-003", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-001"], "created_at": "2026-06-03T15:39:25.645837", "updated_at": "2026-06-03T15:39:25.645838", "metadata": {}}
{"node_id": "IPA-L1-003", "name": "cnsh_compiler", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh_core.compiler", "notion_url": null, "entry_point": "get_cnsh_compiler", "dna": "#龍芯⚡️2026-06-03-CNSH-COMPILER-v1.0", "layer": "L1_SEASONAL", "description": "CNSH编译器·计算逻辑赋能层·可参数化编译", "tags": ["L1", "compiler", "cnsh", "calculation"], "dependencies": ["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-001"], "created_at": "2026-06-03T23:31:21.437275", "updated_at": "2026-06-03T23:31:21.437276", "metadata": {}}
{"node_id": "IPA-L2-FLOW-CORE-001", "name": "cnsh_flow_decision_core", "node_type": "GATEWAY", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore.process_input", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-CORE-v4.1", "layer": "L2_DECISION", "description": "流场决策核·10道闸·27条硬闸·人格协作×IPA×DNA", "tags": ["L2", "decision", "flow", "gate", "persona"], "dependencies": ["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-002"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"personas": 9, "gates": 10, "hardlaws": 27, "ipa_nodes": 11}}
{"node_id": "IPA-L2-FLOW-GATE-SIGN-001", "name": "gate_sign", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_sign", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SIGN-v4.1", "layer": "L2_DECISION", "description": "签章闸·confirm+gpg验证·硬闸1-2", "tags": ["L2", "gate", "sign", "security"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 1, "main_persona": "P05", "hardlaws": [1, 2]}}
{"node_id": "IPA-L2-FLOW-GATE-PRIVACY-002", "name": "gate_privacy", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_privacy", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-PRIVACY-v4.1", "layer": "L2_DECISION", "description": "隐私闸·visibility+trace_mode·硬闸3,10", "tags": ["L2", "gate", "privacy"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 2, "main_persona": "P03", "hardlaws": [3, 10]}}
{"node_id": "IPA-L2-FLOW-GATE-DR-003", "name": "gate_digital_root", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "notion_url": null, "entry_point": "DigitalRootCalculator.calculate_dr", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-DR-v4.1", "layer": "L2_DECISION", "description": "数字根闸·四源优先级·explicit>dna>hash>raw>fallback", "tags": ["L2", "gate", "math", "dr"], "dependencies": ["IPA-L0-006", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3, "main_persona": "P06", "sources": 5}}
{"node_id": "IPA-L2-FLOW-WUXING-MAP-004", "name": "wuxing_mapping", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "notion_url": null, "entry_point": "DigitalRootCalculator.dr_to_wuxing", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-WUXING-v4.1", "layer": "L2_DECISION", "description": "五行映射·dr→金木水火土", "tags": ["L2", "gate", "wuxing", "mapping"], "dependencies": ["IPA-L2-FLOW-GATE-DR-003"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3.5}}
{"node_id": "IPA-L2-FLOW-GATE-AUDIT-005", "name": "gate_audit", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_audit", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-AUDIT-v4.1", "layer": "L2_DECISION", "description": "三色闸·🟢🟡🔴审计判定·硬闸7-8-9", "tags": ["L2", "gate", "audit", "color"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 5, "main_persona": "P05", "hardlaws": [7, 8, 9]}}
{"node_id": "IPA-L2-FLOW-GATE-SANCAI-006", "name": "gate_sancai", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_sancai", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SANCAI-v4.1", "layer": "L2_DECISION", "description": "三才闸·天0.35·地0.15·人≥0.34·硬闸6", "tags": ["L2", "gate", "sancai", "weight"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 6, "main_persona": "P00", "hardlaws": [6]}}
{"node_id": "IPA-L2-FLOW-GATE-SHENGKE-007", "name": "gate_shengke", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_shengke", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SHENGKE-v4.1", "layer": "L2_DECISION", "description": "生克闸·与父DNA五行关系计算", "tags": ["L2", "gate", "shengke"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 7, "main_persona": "P01"}}
{"node_id": "IPA-L2-FLOW-PALACE-ROUTER-008", "name": "palace_router", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_palace", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-PALACE-v4.1", "layer": "L2_DECISION", "description": "九宫派位·P13独占·铁律5", "tags": ["L2", "gate", "palace", "router"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 8, "main_persona": "P13", "ironlaw": 5}}
{"node_id": "IPA-L2-FLOW-SANDBOX-BUCKET-009", "name": "sandbox_bucket", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore._gate_sandbox", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-SANDBOX-v4.1", "layer": "L2_DECISION", "description": "沙盒分拣·🔴熔断·📝消化·🔒封存·🟢通过·🟡待审", "tags": ["L2", "gate", "sandbox"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 9, "main_persona": "P03", "buckets": 5}}
{"node_id": "IPA-L2-FLOW-DNA-CHAIN-010", "name": "dna_chain_archival", "node_type": "ARCHIVAL", "status": "🟢", "local_path": "cnsh.flow_decision.dna_chain_tracer", "notion_url": null, "entry_point": "DNAChainTracer.validate_dna_chain", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DNA-CHAIN-v4.1", "layer": "L2_DECISION", "description": "父子链落档·DNA追溯·多标签·销毁/封存证明·硬闸4-5", "tags": ["L2", "archival", "dna", "chain"], "dependencies": ["IPA-L0-004", "IPA-L0-005", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 10, "main_persona": "P15", "hardlaws": [4, 5], "proof_types": ["burn", "sealed"]}}
{"node_id": "IPA-L0-007", "name": "secret_vault", "node_type": "LOCAL", "status": "🟢", "local_path": "longhun.vault", "notion_url": null, "entry_point": "get_secret_vault", "dna": "#龍芯⚡️20260618-VAULT-IPA-v1.0", "layer": "L0_ETERNAL", "description": "age加密密钥库·API Key/Token统一托管·公开可审计·私钥本地持有", "tags": ["L0", "security", "vault", "age", "secret"], "dependencies": ["IPA-L0-001", "IPA-L0-002", "IPA-L0-004"], "created_at": "2026-06-18T19:41:59.238109", "updated_at": "2026-06-18T19:41:59.238109", "metadata": {"public_repo_ready": true, "encryption": "age", "private_key_path": "~/.cnsh/age.key"}}
{"node_id": "IPA-L0-008", "name": "cnsh_runtime_v9", "node_type": "LOCAL", "status": "🟢", "local_path": "cnsh.task_executor_v9_integrated", "notion_url": null, "entry_point": "main", "dna": "#龍芯⚡️2026-06-17-CNSH-MAIN-v1.0", "layer": "L0_ETERNAL", "description": "CNSH中文原生指令系统v9整合运行时（flow_decision + sancai_sync + task_executor）", "tags": ["L0", "cnsh", "runtime", "v9"], "dependencies": ["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-21T22:16:43.015005", "updated_at": "2026-06-21T22:16:43.015005", "metadata": {"source_path": "CNSH/", "launch_script": "CNSH/launch.sh"}}
{"node_id": "IPA-L1-004", "name": "longhun_v5_unified_launcher", "node_type": "LOCAL", "status": "🟢", "local_path": "bin.龍魂体系v5-一键启动", "notion_url": null, "entry_point": "main", "dna": "#龍芯⚡️2026-06-19-LONGHUN-v5-UNIFIED-LAUNCHER-v1.0", "layer": "L1_SEASONAL", "description": "龍魂体系v5一键启动入口：按依赖顺序启动全部服务", "tags": ["L1", "launcher", "automation"], "dependencies": ["IPA-L0-007", "IPA-L1-002", "IPA-L1-003", "IPA-L0-008"], "created_at": "2026-06-21T22:16:43.015005", "updated_at": "2026-06-21T22:16:43.015005", "metadata": {"script": "bin/龍魂体系v5-一键启动.py"}}
{"node_id": "IPA-L1-005", "name": "longhun_web_console_v2", "node_type": "LOCAL", "status": "🟢", "local_path": "web.龍魂操作台v2.0", "notion_url": null, "entry_point": "browser_open", "dna": "#龍芯⚡️2026-06-20-CONSOLE-v2.0", "layer": "L1_SEASONAL", "description": "龍魂操作台v2.0 · Web控制台HTML入口", "tags": ["L1", "web", "console", "ui"], "dependencies": ["IPA-L0-001"], "created_at": "2026-06-21T22:16:43.015005", "updated_at": "2026-06-21T22:16:43.015005", "metadata": {"file": "web/龍魂操作台v2.0.html"}}


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-06-03-IPA-ROUTE-REGISTRY-LOCAL-FILE1-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
