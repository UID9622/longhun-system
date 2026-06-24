# 龍魂流场决策核 v4.1·系统集成指南

**DNA:**#龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-INTEGRATION-v1.0
**CONFIRM:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**责任:** UID9622·不免责

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

## 🔌 系统调用方式

### 方式1：直接导入

```python
from cnsh.flow_decision import quick_process, FlowDecisionNode

node = quick_process(
    raw_input="处理内容",
    tags={"title": "example", "level": "L3_DAILY"}
)
```

### 方式2：通过IPA路由

```python
from cnsh_core.registry import IPARegistry

# 获取流场决策核主节点
registry = IPARegistry()
flow_core = registry.get_node("IPA-L2-FLOW-CORE-001")
result = flow_core.execute(raw_input, tags)
```

### 方式3：通过规则引擎

```python
from cnsh_core.rules import RuleEngine

rule_engine = RuleEngine()
# 规则可触发流场决策核进行决策
decision = rule_engine.execute_flow_decision(input_data)
```

---

## 📋 IPA路由注册（11个节点）

### 要追加的记录（JSONL格式）

应添加到 `01_protocols/IPA-ROUTE-REGISTRY.local.md` 的末尾：

```jsonl
{"node_id": "IPA-L2-FLOW-CORE-001", "name": "cnsh_flow_decision_core", "node_type": "GATEWAY", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "notion_url": null, "entry_point": "CNSHFlowDecisionCore.process_input", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-CORE-v4.1", "layer": "L2_DECISION", "description": "流场决策核·10道闸·27条硬闸", "tags": ["L2", "decision", "flow", "gate", "persona"], "dependencies": ["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-002"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"personas": 9, "gates": 10, "hardlaws": 27, "ipa_nodes": 11}}
{"node_id": "IPA-L2-FLOW-GATE-SIGN-001", "name": "gate_sign", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sign", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SIGN-v4.1", "layer": "L2_DECISION", "description": "签章闸·confirm+gpg验证", "tags": ["L2", "gate", "sign", "security"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 1, "main_persona": "P05", "hardlaws": [1, 2]}}
{"node_id": "IPA-L2-FLOW-GATE-PRIVACY-002", "name": "gate_privacy", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_privacy", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-PRIVACY-v4.1", "layer": "L2_DECISION", "description": "隐私闸·visibility+trace_mode", "tags": ["L2", "gate", "privacy"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 2, "main_persona": "P03", "hardlaws": [3, 10]}}
{"node_id": "IPA-L2-FLOW-GATE-DR-003", "name": "gate_digital_root", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "entry_point": "DigitalRootCalculator.calculate_dr", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-DR-v4.1", "layer": "L2_DECISION", "description": "数字根闸·四源优先级", "tags": ["L2", "gate", "math", "dr"], "dependencies": ["IPA-L0-006", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3, "main_persona": "P06", "sources": 5}}
{"node_id": "IPA-L2-FLOW-WUXING-MAP-004", "name": "wuxing_mapping", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.digital_root", "entry_point": "DigitalRootCalculator.dr_to_wuxing", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-WUXING-v4.1", "layer": "L2_DECISION", "description": "五行映射·dr→五行", "tags": ["L2", "gate", "wuxing", "mapping"], "dependencies": ["IPA-L2-FLOW-GATE-DR-003"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 3.5}}
{"node_id": "IPA-L2-FLOW-GATE-AUDIT-005", "name": "gate_audit", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_audit", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-AUDIT-v4.1", "layer": "L2_DECISION", "description": "三色闸·审计判定", "tags": ["L2", "gate", "audit", "color"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 5, "main_persona": "P05", "hardlaws": [7, 8, 9]}}
{"node_id": "IPA-L2-FLOW-GATE-SANCAI-006", "name": "gate_sancai", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sancai", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SANCAI-v4.1", "layer": "L2_DECISION", "description": "三才闸·权重验证", "tags": ["L2", "gate", "sancai", "weight"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 6, "main_persona": "P00", "hardlaws": [6]}}
{"node_id": "IPA-L2-FLOW-GATE-SHENGKE-007", "name": "gate_shengke", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_shengke", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-GATE-SHENGKE-v4.1", "layer": "L2_DECISION", "description": "生克闸·与父DNA关系", "tags": ["L2", "gate", "shengke"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 7, "main_persona": "P01"}}
{"node_id": "IPA-L2-FLOW-PALACE-ROUTER-008", "name": "palace_router", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_palace", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-PALACE-v4.1", "layer": "L2_DECISION", "description": "九宫派位·P13独占", "tags": ["L2", "gate", "palace", "router"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 8, "main_persona": "P13", "ironlaw": 5}}
{"node_id": "IPA-L2-FLOW-SANDBOX-BUCKET-009", "name": "sandbox_bucket", "node_type": "GATE", "status": "🟢", "local_path": "cnsh.flow_decision.cnsh_flow_decision_core", "entry_point": "CNSHFlowDecisionCore._gate_sandbox", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-SANDBOX-v4.1", "layer": "L2_DECISION", "description": "沙盒分拣·五桶分类", "tags": ["L2", "gate", "sandbox"], "dependencies": ["IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 9, "main_persona": "P03", "buckets": 5}}
{"node_id": "IPA-L2-FLOW-DNA-CHAIN-010", "name": "dna_chain_archival", "node_type": "ARCHIVAL", "status": "🟢", "local_path": "cnsh.flow_decision.dna_chain_tracer", "entry_point": "DNAChainTracer.validate_dna_chain", "dna": "#龍芯⚡️2026-06-06-CNSH-FLOW-DNA-CHAIN-v4.1", "layer": "L2_DECISION", "description": "父子链落档·DNA追溯", "tags": ["L2", "archival", "dna", "chain"], "dependencies": ["IPA-L0-004", "IPA-L0-005", "IPA-L2-FLOW-CORE-001"], "created_at": "2026-06-06T00:32:00.000000", "updated_at": "2026-06-06T00:32:00.000000", "metadata": {"gate_num": 10, "main_persona": "P15", "hardlaws": [4, 5], "proof_types": ["burn", "sealed"]}}
```

---

## ⚙️ 集成步骤

### 步骤1：更新IPA路由注册表

```bash
# 将上述11个JSONL记录追加到：
cat >> 01_protocols/IPA-ROUTE-REGISTRY.local.md << 'EOF'
{...11个记录...}
EOF
```

### 步骤2：更新cnsh/__init__.py

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

### 步骤3：验证集成

```bash
# 测试导入
python3 -c "from cnsh.flow_decision import quick_process; print('✅ CNSH流场决策核已集成')"

# 运行示例
python3 cnsh/flow_decision/examples.py
```

### 步骤4：更新系统文档

在 `CNSH_v1.0_FULL_ARCHITECTURE.md` 中添加 L2 层级说明：

```markdown
## L2 决策层（新增）

### 流场决策核 (CNSH Flow Decision Core v4.1)
- **主节点**: IPA-L2-FLOW-CORE-001
- **功能**: 10道闸·27条硬闸·9个人格·11个IPA节点
- **入口**: cnsh.flow_decision.quick_process()
- **特性**: 人格协作·DNA追溯·多标签隐私
```

---

## 🔗 互操作性

### 与规则引擎的集成

```python
# cnsh_core/rules.py 中可添加：
class RuleEngine:
    def execute_flow_decision(self, input_data):
        """触发流场决策核进行复杂决策"""
        from cnsh.flow_decision import quick_process
        node, logs = quick_process(
            input_data.get('raw_input'),
            input_data.get('tags', {})
        )
        return node

# 使用
rule_engine = RuleEngine()
result = rule_engine.execute_flow_decision({
    'raw_input': '敏感数据',
    'tags': {'visibility': 'PRIVATE'}
})
```

### 与DNA追溯系统的集成

```python
# cnsh_core/dna.py 中可添加：
from cnsh.flow_decision import DNAChainTracer

class DNAGenerator:
    def trace_decision_lineage(self, dna):
        """追溯决策的完整DNA谱系"""
        tracer = DNAChainTracer()
        return tracer.build_full_lineage(self.dna_registry, dna)
```

---

## 📊 系统状态

| 项目 | 状态 | 备注 |
|------|------|------|
| 核心工程 | ✅ 完成 | 8模块·2952行 |
| IPA路由注册 | ⏳ 待追加 | 11个节点 |
| cnsh/__init__.py | ⏳ 待更新 | 导出接口 |
| 系统文档 | ⏳ 待更新 | ARCHITECTURE |
| 验收测试 | ✅ 通过 | 4个示例全绿 |

---

## 🚀 快速开始

集成完成后，系统任何部分都可以这样使用：

```python
# 方式A：直接导入
from cnsh.flow_decision import quick_process
node = quick_process("内容", {"title": "任务"})

# 方式B：通过IPA路由
from cnsh_core.registry import IPARegistry
core = IPARegistry().get_node("IPA-L2-FLOW-CORE-001")
node, logs = core.execute("内容", {})

# 方式C：通过规则引擎
from cnsh_core.rules import RuleEngine
result = RuleEngine().execute_flow_decision({...})
```

---

**DNA:**#龍芯⚡️2026-06-06-CNSH-FLOW-DECISION-INTEGRATION-v1.0
**责任:** UID9622·不免责
**签章:** 人格协作×IPA×DNA·完全就绪
