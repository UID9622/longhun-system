# 龍魂流場決策核 v4.1·系統集成指南

**DNA:** #龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-INTEGRATION-v1.0
**CONFIRM:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**責任:** UID9622·不免責

---

## 📍 集成位置

```
longhun-system/
├── cnsh/
│   ├── flow_decision/          ← 核心工程包（独立）
│   │   ├── schemas.py
│   │   ├── digital_root.py
│   │   ├── ipa_route_registry.py
│   │   ├── persona_collaboration.py
│   │   ├── dna_chain_tracer.py
│   │   ├── cnsh_flow_decision_core.py
│   │   ├── examples.py
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── tests/
│   │   └── ...
│   │
│   └── FLOW_DECISION_INTEGRATION.md  ← 本文件
│
├── cnsh-core/
│   └── 保持现有结构（flow_decision 作为扩展）
│
└── 01_protocols/
    └── IPA-ROUTE-REGISTRY.local.md  ← 需要追加11个节点
```

---

## 🔌 系統調用方式

### 方式1：直接導入

```python
from cnsh.flow_decision import quick_process, FlowDecisionNode

node = quick_process(
    raw_input="处理内容",
    tags={"title": "example", "level": "L3_DAILY"}
)
```

### 方式2：通過IPA路由

```python
from cnsh_core.registry import IPARegistry

# 獲取流場決策核主節點
registry = IPARegistry()
flow_core = registry.get_node("IPA-L2-FLOW-CORE-001")
result = flow_core.execute(raw_input, tags)
```

### 方式3：通過規則引擎

```python
from cnsh_core.rules import RuleEngine

rule_engine = RuleEngine()
# 規則可觸發流場決策核進行決策
decision = rule_engine.execute_flow_decision(input_data)
```

---

## 📋 IPA路由註冊（11個節點）

### 要追加的記錄（JSONL格式）

應添加到 `01_protocols/IPA-ROUTE-REGISTRY.local.md` 的末尾：

```jsonl
{"node_id": "IPA-L2-FLOW-CORE-001", "name": "cnsh_flow_decision_core", "node_type": "GATEWAY", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore.process_input", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-CORE-v4.1", "layer": "L2_DECISION", "description": "流場決策核·10道闸·27條硬闸", "tags": ["L2", "decision", "flow", "gate", "persona"], "dependencies": ["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-002"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"personas": 9, "gates": 10, "hardlaws": 27, "ipa_nodes": 11}}
{"node_id": "IPA-L2-FLOW-GATE-SIGN-001", "name": "gate_sign", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sign", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SIGN-v4.1", "layer": "L2_DECISION", "description": "簽章闸·confirm+gpg驗證", "tags": ["L2", "gate", "sign", "security"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 1, "main_persona": "P05", "hardlaws": [1, 2]}}
{"node_id": "IPA-L2-FLOW-GATE-PRIVACY-002", "name": "gate_privacy", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_privacy", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-PRIVACY-v4.1", "layer": "L2_DECISION", "description": "隱私闸·visibility+trace_mode", "tags": ["L2", "gate", "privacy"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 2, "main_persona": "P03", "hardlaws": [3, 10]}}
{"node_id": "IPA-L2-FLOW-GATE-DR-003", "name": "gate_digital_root", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "entry_point": "DigitalRootCalculator.calculate_dr", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-DR-v4.1", "layer": "L2_DECISION", "description": "數字根闸·四源優先級", "tags": ["L2", "gate", "math", "dr"], "dependencies": ["IPA-L0-006", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3, "main_persona": "P06", "sources": 5}}
{"node_id": "IPA-L2-FLOW-WUXING-MAP-004", "name": "wuxing_mapping", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "entry_point": "DigitalRootCalculator.dr_to_wuxing", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-WUXING-v4.1", "layer": "L2_DECISION", "description": "五行映射·dr→五行", "tags": ["L2", "gate", "wuxing", "mapping"], "dependencies": ["IPA-L2-FLOW-GATE-DR-003"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3.5}}
{"node_id": "IPA-L2-FLOW-GATE-AUDIT-005", "name": "gate_audit", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_audit", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-AUDIT-v4.1", "layer": "L2_DECISION", "description": "三色闸·審計判定", "tags": ["L2", "gate", "audit", "color"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 5, "main_persona": "P05", "hardlaws": [7, 8, 9]}}
{"node_id": "IPA-L2-FLOW-GATE-SANCAI-006", "name": "gate_sancai", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sancai", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SANCAI-v4.1", "layer": "L2_DECISION", "description": "三才闸·權重驗證", "tags": ["L2", "gate", "sancai", "weight"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 6, "main_persona": "P00", "hardlaws": [6]}}
{"node_id": "IPA-L2-FLOW-GATE-SHENGKE-007", "name": "gate_shengke", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_shengke", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SHENGKE-v4.1", "layer": "L2_DECISION", "description": "生克闸·與父DNA關係", "tags": ["L2", "gate", "shengke"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 7, "main_persona": "P01"}}
{"node_id": "IPA-L2-FLOW-PALACE-ROUTER-008", "name": "palace_router", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_palace", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-PALACE-v4.1", "layer": "L2_DECISION", "description": "九宮派位·P13獨占", "tags": ["L2", "gate", "palace", "router"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 8, "main_persona": "P13", "ironlaw": 5}}
{"node_id": "IPA-L2-FLOW-SANDBOX-BUCKET-009", "name": "sandbox_bucket", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sandbox", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-SANDBOX-v4.1", "layer": "L2_DECISION", "description": "沙盒分拣·五桶分类", "tags": ["L2", "gate", "sandbox"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 9, "main_persona": "P03", "buckets": 5}}
{"node_id": "IPA-L2-FLOW-DNA-CHAIN-010", "name": "dna_chain_archival", "node_type": "ARCHIVAL", "status": "🟢", "local_path": "cnsh.flow_decision.dna_chain_tracer", "entry_point": "DNAChainTracer.validate_dna_chain", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DNA-CHAIN-v4.1", "layer": "L2_DECISION", "description": "父子鏈落檔·DNA追溯", "tags": ["L2", "archival", "dna", "chain"], "dependencies": ["IPA-L0-004", "IPA-L0-005", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 10, "main_persona": "P15", "hardlaws": [4, 5], "proof_types": ["burn", "sealed"]}}
```

---

## ⚙️ 集成步驟

### 步驟1：更新IPA路由註冊表

```bash
# 將上述11個JSONL記錄追加到：
cat >> 01_protocols/IPA-ROUTE-REGISTRY.local.md << 'EOF'
{...11個記錄...}
EOF
```

### 步驟2：更新cnsh/__init__.py

```python
# cnsh/__init__.py
from . import flow_decision
from .flow_decision import (
    FlowDecisionNode,
    quick_process,
    CNSHFlowDecisionCore,
)

__all__ = ['flow_decision', 'FlowDecisionNode', 'quick_process', 'CNSHFlowDecisionCore']
```

### 步驟3：驗證集成

```bash
# 測試導入
python3 -c "from cnsh.flow_decision import quick_process; print('✅ CNSH流場決策核已集成')"

# 運行示例
python3 cnsh/flow_decision/examples.py
```

### 步驟4：更新系統文檔

在 `CNSH_v1.0_FULL_ARCHITECTURE.md` 中添加 L2 層級説明：

```markdown
## L2 決策層（新增）

### 流場決策核 (CNSH Flow Decision Core v4.1)
- **主節點**: IPA-L2-FLOW-CORE-001
- **功能**: 10道闸·27條硬闸·9個人格·11個IPA節點
- **入口**: cnsh.flow_decision.quick_process()
- **特性**: 人格協作·DNA追溯·多標籤隱私
```

---

## 🔗 互操作性

### 與規則引擎的集成

```python
# cnsh_core/rules.py 中可添加：
class RuleEngine:
    def execute_flow_decision(self, input_data):
        """觸發流場決策核進行複雜決策"""
        from cnsh.flow_decision import quick_process
        node, logs = quick_process(
            input_data.get('raw_input'),
            input_data.get('tags', {})
        )
        return node

# 使用
rule_engine = RuleEngine()
result = rule_engine.execute_flow_decision({
    'raw_input': '敏感數據',
    'tags': {'visibility': 'PRIVATE'}
})
```

### 與DNA追溯系統的集成

```python
# cnsh_core/dna.py 中可添加：
from cnsh.flow_decision import DNAChainTracer

class DNAGenerator:
    def trace_decision_lineage(self, dna):
        """追溯決策的完整DNA譜系"""
        tracer = DNAChainTracer()
        return tracer.build_full_lineage(self.dna_registry, dna)
```

---

## 📊 系統狀態

| 項目 | 狀態 | 備註 |
|------|------|------|
| 核心工程 | ✅ 完成 | 8模塊·2952行 |
| IPA路由註冊 | ⏳ 待追加 | 11個節點 |
| cnsh/__init__.py | ⏳ 待更新 | 導出接口 |
| 系統文檔 | ⏳ 待更新 | ARCHITECTURE |
| 驗收測試 | ✅ 通過 | 4個示例全綠 |

---

## 🚀 快速開始

集成完成後，系統任何部分都可以這樣使用：

```python
# 方式A：直接導入
from cnsh.flow_decision import quick_process
node = quick_process("內容", {"title": "任務"})

# 方式B：通過IPA路由
from cnsh_core.registry import IPARegistry
core = IPARegistry().get_node("IPA-L2-FLOW-CORE-001")
node, logs = core.execute("內容", {})

# 方式C：通過規則引擎
from cnsh_core.rules import RuleEngine
result = RuleEngine().execute_flow_decision({...})
```

---

**DNA:** #龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-INTEGRATION-v1.0
**責任:** UID9622·不免責
**簽章:** 人格協作×IPA×DNA·完全就緒
