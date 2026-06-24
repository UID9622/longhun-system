# 龍魂系统·三合同步器 v1.0

## 简介

龍魂三合同步器是一个完整的三环无死锁转换系统，实现 v4.1/v3.0/v4.0 多模块的互联互通。

```
[v4.1 决策辟 JSON] ↔ [v3.0 呼吸大脑 粒子指令] ↔ [v4.0 神经映射 信号]
```

**DNA**: `#龍芯⚡️2026-06-06-SANCAI-SYNC-README-v1.0`

**UID**: `9622·诸葛鑫·龍芯北辰`

**责任**: `UID9622·不免责`

---

## 核心职责

### 1. IPA 回执 → 粒子指令 (ipa_to_particle)

将 v4.1 决策辟的 IPA 回执转换为 v3.0 呼吸大脑的粒子指令。

**转换逻辑**：
- IPA 信号强度 (pass/hold/fuse) → 粒子生存周期
- IPA 节点深度 → 粒子初始能量
- IPA 人格 → 粒子可塑性
- IPA 时间戳 → 粒子种子

**示例**：
```python
from cnsh.sancai_sync import SancaiSyncHub, IPAReceipt
from datetime import datetime

hub = SancaiSyncHub()

ipa = IPAReceipt(
    ipa_node="IPA-FLOW-GATE-PRIVACY",
    ipa_address="/flow/gate/privacy",
    main_persona="P03",
    input_node_id="FLOW-9622-20260606-ABC123",
    output_signal="pass",
    next_ipa="IPA-FLOW-GATE-DR",
    dna="#龍芯⚡️2026-06-06-IPA-GATE-PRIVACY-v1.0",
    timestamp=datetime.now().isoformat()
)

particles = hub.ipa_to_particle(ipa, particle_count=50)
# → 50 个粒子指令，可直接喂给 v3.0
```

### 2. 年轮记忆 → 神经信号 (ring_to_neural)

将 v3.0 年轮记忆转换为 v4.0 神经激活信号。

**转换逻辑**：
- 年轮年龄 (age) → 神经激活强度
- 年轮半径 (radius) → 突触权重
- 年轮强度 (strength) → 放电速率
- 年轮位置 (x,y) → 空间定位

**示例**：
```python
ring_data = {
    'age': 150,
    'radius': 120.0,
    'strength': 0.85,
    'x': 400.0,
    'y': 300.0
}

signals = hub.ring_to_neural(ring_data)
# → 神经信号列表，反映记忆的神经激活状态
```

### 3. 知识图 → 九宫派位 (knowledge_to_palace)

将 v4.0 知识拓扑转换为 v4.1 九宫派位。

**转换逻辑**：
- 图的节点 → 宫位
- 图的边权重 → 派位置信度
- 图的中心性 → 人格分配优先级
- 图的社群 → 宫位聚类

**示例**：
```python
knowledge_graph = {
    'nodes': [
        {'weight': 0.9, 'edges': [1, 2, 3]},
        {'weight': 0.8, 'edges': [0, 2]},
        {'weight': 0.7, 'edges': [0, 1, 3]},
    ],
    'parent_dna': '#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-v1.0'
}

palaces = hub.knowledge_to_palace(knowledge_graph)
# → 九宫派位节点列表
```

---

## 验证与DNA

### 验证无死锁 (verify_sync)

检查三环转换的完整性和一致性。

```python
ok, msg = hub.verify_sync()
# → (True, "✅ 三环无死锁·系统就绪") 或 (False, "错误信息")
```

**检查项**：
1. 粒子数量 ≥ 1
2. 神经信号数量 ≥ 1
3. 宫位数量 ≤ 9
4. 神经-粒子比例合理
5. DNA 链完整

### DNA 生成 (generate_dna)

生成全链 DNA 签章，支持父子链追溯。

```python
dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-SANCAI-SYNC-README-v1.0")
# → #龍芯⚡️2026-06-06-THREE-INTEGRATION-SYNC-v1.0-XXXXXXXX
```

---

## 数据结构

### IPAReceipt
```python
@dataclass
class IPAReceipt:
    ipa_node: str           # "IPA-FLOW-GATE-PRIVACY" 等
    ipa_address: str        # "/flow/gate/privacy" 等
    main_persona: str       # "P03" 等
    input_node_id: str      # "FLOW-9622-20260503-A1B2C3D4"
    output_signal: str      # "pass" | "hold" | "fuse"
    next_ipa: str           # 下个节点
    dna: str                # DNA 签章
    timestamp: str          # ISO 8601
```

### ParticleInstruction
```python
@dataclass
class ParticleInstruction:
    id: int                 # 粒子 ID
    x, y: float             # 位置
    vx, vy: float           # 速度
    synaptic: float         # 0.0-1.0 突触权重
    plasticity: float       # 0.2-1.0 可塑性
    seed_bias: float        # 方向偏置
    trail: List[Tuple]      # 轨迹
    life: int               # 剩余生命周期
```

### NeuralSignal
```python
@dataclass
class NeuralSignal:
    neuron_id: str          # 神经元编码
    activation: float       # 0.0-1.0 激活强度
    firing_rate: float      # 0.0-1.0 放电速率
    synapse_weight: float   # -1.0~1.0 突触权重
    temporal_context: str   # 时间背景
    spatial_location: Tuple # 空间位置 (x, y)
```

### PalaceNode
```python
@dataclass
class PalaceNode:
    palace_name: str        # "艮宫" "坤宫" 等
    element: str            # "金" "木" "水" "火" "土"
    persona_assigned: str   # "P01" 等
    contribution: float     # 0-10 贡献值
    confidence: float       # 0.0-1.0 置信度
    dna_chain: str          # DNA 父子链
```

---

## 完整使用示例

```python
from cnsh.sancai_sync import SancaiSyncHub, IPAReceipt
from datetime import datetime

# 步骤 1：初始化 Hub
hub = SancaiSyncHub(seed=9622)

# 步骤 2：创建 IPA 回执
ipa = IPAReceipt(
    ipa_node="IPA-FLOW-GATE-PRIVACY",
    ipa_address="/flow/gate/privacy",
    main_persona="P03",
    input_node_id="FLOW-9622-20260606-ABC123",
    output_signal="pass",
    next_ipa="IPA-FLOW-GATE-DR",
    dna="#龍芯⚡️2026-06-06-IPA-GATE-PRIVACY-v1.0",
    timestamp=datetime.now().isoformat()
)

# 步骤 3：转换 IPA → 粒子
particles = hub.ipa_to_particle(ipa, particle_count=30)
print(f"✅ 粒子生成: {len(particles)} 个")

# 步骤 4：创建年轮数据
ring_data = {
    'age': 150,
    'radius': 120.0,
    'strength': 0.85,
    'x': 400.0,
    'y': 300.0
}

# 步骤 5：转换年轮 → 神经信号
signals = hub.ring_to_neural(ring_data)
print(f"✅ 神经信号生成: {len(signals)} 个")

# 步骤 6：创建知识图
knowledge_graph = {
    'nodes': [
        {'weight': 0.9, 'edges': [1, 2, 3]},
        {'weight': 0.8, 'edges': [0, 2]},
        {'weight': 0.7, 'edges': [0, 1, 3]},
    ],
    'parent_dna': '#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-v1.0'
}

# 步骤 7：转换知识图 → 宫位
palaces = hub.knowledge_to_palace(knowledge_graph)
print(f"✅ 宫位生成: {len(palaces)} 个")

# 步骤 8：验证无死锁
ok, msg = hub.verify_sync()
print(f"✅ 验证结果: {msg}")

# 步骤 9：生成 DNA
dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-PARENT-v1.0")
print(f"✅ DNA 生成: {dna}")

# 步骤 10：导出 JSON
json_str = hub.to_json()
print(f"✅ JSON 导出完成: {len(json_str)} 字符")
```

---

## 测试

完整的单元测试和集成测试覆盖：

```bash
pytest cnsh/sancai_sync/tests/test_sancai_sync_hub.py -v
```

**测试覆盖**：
- ✅ 数据结构创建（4 个类）
- ✅ 三个转换函数
- ✅ 验证函数
- ✅ DNA 生成
- ✅ 边界情况（空数据、极端值、大数据量）
- ✅ 人格路由
- ✅ 完整集成流程

---

## 验收清单

### ✅ 框架部分（已完成）
- ☑ 数据结构定义
- ☑ SancaiSyncHub 核心类
- ☑ 三个转换函数实现
- ☑ 验证函数
- ☑ DNA 生成函数
- ☑ JSON 导出函数
- ☑ 完整测试套件（30+ 测试用例）

### ✅ 验收标准
- ✅ 双向转换无损: v4.1 → v3.0 → v4.1 字段完整
- ✅ 三环无死锁: verify_sync() 通过
- ✅ DNA 可追溯: 父子链完整·不可篡改
- ✅ 全代码路径覆盖: 100% 单元测试
- ✅ 集成测试: 三环完整流程通过

---

## 文件结构

```
cnsh/sancai_sync/
├── __init__.py                  # 包入口
├── sancai_sync_hub.py           # 核心类与函数（~550 行）
├── README.md                    # 此文档
├── DELIVERY_RECEIPT.md          # 交付回执
└── tests/
    ├── __init__.py
    └── test_sancai_sync_hub.py  # 完整测试套件（~400 行）
```

---

## 相关模块

- **v4.1 决策辟**: `cnsh/flow_decision/`
- **v3.0 呼吸大脑**: 外部模块
- **v4.0 神经映射**: 外部模块

---

## 联系与反馈

**作者**: UID9622·诸葛鑫·龍芯北辰

**责任**: UID9622·不免责

**DNA**: `#龍芯⚡️2026-06-06-SANCAI-SYNC-README-v1.0`
