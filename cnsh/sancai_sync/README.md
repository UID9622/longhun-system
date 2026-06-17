# 龍魂系統·三合同步器 v1.0

## 簡介

龍魂三合同步器是一個完整的三環無死鎖轉換系統，實現 v4.1/v3.0/v4.0 多模塊的互聯互通。

```
[v4.1 決策闢 JSON] ↔ [v3.0 呼吸大腦 粒子指令] ↔ [v4.0 神經映射 信號]
```

**DNA**: `#龍芯⚡️2026-06-06-THREE-INTEGRATION-SYNC-HUB-v1.0-FRAMEWORK`

**UID**: `9622·諸葛鑫·龍芯北辰`

**責任**: `UID9622·不免責`

---

## 核心職責

### 1. IPA 回執 → 粒子指令 (ipa_to_particle)

將 v4.1 決策闢的 IPA 回執轉換為 v3.0 呼吸大腦的粒子指令。

**轉換邏輯**：
- IPA 信號強度 (pass/hold/fuse) → 粒子生存週期
- IPA 節點深度 → 粒子初始能量
- IPA 人格 → 粒子可塑性
- IPA 時間戳 → 粒子種子

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
# → 50 個粒子指令，可直接餵給 v3.0
```

### 2. 年輪記憶 → 神經信號 (ring_to_neural)

將 v3.0 年輪記憶轉換為 v4.0 神經激活信號。

**轉換邏輯**：
- 年輪年齡 (age) → 神經激活強度
- 年輪半徑 (radius) → 突觸權重
- 年輪強度 (strength) → 放電速率
- 年輪位置 (x,y) → 空間定位

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
# → 神經信號列表，反映記憶的神經激活狀態
```

### 3. 知識圖 → 九宮派位 (knowledge_to_palace)

將 v4.0 知識拓撲轉換為 v4.1 九宮派位。

**轉換邏輯**：
- 圖的節點 → 宮位
- 圖的邊權重 → 派位置信度
- 圖的中心性 → 人格分配優先級
- 圖的社群 → 宮位聚類

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
# → 九宮派位節點列表
```

---

## 驗證與DNA

### 驗證無死鎖 (verify_sync)

檢查三環轉換的完整性和一致性。

```python
ok, msg = hub.verify_sync()
# → (True, "✅ 三環無死鎖·系統就緒") 或 (False, "錯誤信息")
```

**檢查項**：
1. 粒子數量 ≥ 1
2. 神經信號數量 ≥ 1
3. 宮位數量 ≤ 9
4. 神經-粒子比例合理
5. DNA 鏈完整

### DNA 生成 (generate_dna)

生成全鏈 DNA 簽章，支持父子鏈追溯。

```python
dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-SANCAI-SYNC-README-v1.0")
# → #龍芯⚡️2026-06-06-THREE-INTEGRATION-SYNC-v1.0-XXXXXXXX
```

---

## 數據結構

### IPAReceipt
```python
@dataclass
class IPAReceipt:
    ipa_node: str           # "IPA-FLOW-GATE-PRIVACY" 等
    ipa_address: str        # "/flow/gate/privacy" 等
    main_persona: str       # "P03" 等
    input_node_id: str      # "FLOW-9622-20260503-A1B2C3D4"
    output_signal: str      # "pass" | "hold" | "fuse"
    next_ipa: str           # 下個節點
    dna: str                # DNA 簽章
    timestamp: str          # ISO 8601
```

### ParticleInstruction
```python
@dataclass
class ParticleInstruction:
    id: int                 # 粒子 ID
    x, y: float             # 位置
    vx, vy: float           # 速度
    synaptic: float         # 0.0-1.0 突觸權重
    plasticity: float       # 0.2-1.0 可塑性
    seed_bias: float        # 方向偏置
    trail: List[Tuple]      # 軌跡
    life: int               # 剩餘生命週期
```

### NeuralSignal
```python
@dataclass
class NeuralSignal:
    neuron_id: str          # 神經元編碼
    activation: float       # 0.0-1.0 激活強度
    firing_rate: float      # 0.0-1.0 放電速率
    synapse_weight: float   # -1.0~1.0 突觸權重
    temporal_context: str   # 時間背景
    spatial_location: Tuple # 空間位置 (x, y)
```

### PalaceNode
```python
@dataclass
class PalaceNode:
    palace_name: str        # "艮宮" "坤宮" 等
    element: str            # "金" "木" "水" "火" "土"
    persona_assigned: str   # "P01" 等
    contribution: float     # 0-10 貢獻值
    confidence: float       # 0.0-1.0 置信度
    dna_chain: str          # DNA 父子鏈
```

---

## 完整使用示例

```python
from cnsh.sancai_sync import SancaiSyncHub, IPAReceipt
from datetime import datetime

# 步驟 1：初始化 Hub
hub = SancaiSyncHub(seed=9622)

# 步驟 2：創建 IPA 回執
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

# 步驟 3：轉換 IPA → 粒子
particles = hub.ipa_to_particle(ipa, particle_count=30)
print(f"✅ 粒子生成: {len(particles)} 個")

# 步驟 4：創建年輪數據
ring_data = {
    'age': 150,
    'radius': 120.0,
    'strength': 0.85,
    'x': 400.0,
    'y': 300.0
}

# 步驟 5：轉換年輪 → 神經信號
signals = hub.ring_to_neural(ring_data)
print(f"✅ 神經信號生成: {len(signals)} 個")

# 步驟 6：創建知識圖
knowledge_graph = {
    'nodes': [
        {'weight': 0.9, 'edges': [1, 2, 3]},
        {'weight': 0.8, 'edges': [0, 2]},
        {'weight': 0.7, 'edges': [0, 1, 3]},
    ],
    'parent_dna': '#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-v1.0'
}

# 步驟 7：轉換知識圖 → 宮位
palaces = hub.knowledge_to_palace(knowledge_graph)
print(f"✅ 宮位生成: {len(palaces)} 個")

# 步驟 8：驗證無死鎖
ok, msg = hub.verify_sync()
print(f"✅ 驗證結果: {msg}")

# 步驟 9：生成 DNA
dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-PARENT-v1.0")
print(f"✅ DNA 生成: {dna}")

# 步驟 10：導出 JSON
json_str = hub.to_json()
print(f"✅ JSON 導出完成: {len(json_str)} 字符")
```

---

## 測試

完整的單元測試和集成測試覆蓋：

```bash
pytest cnsh/sancai_sync/tests/test_sancai_sync_hub.py -v
```

**測試覆蓋**：
- ✅ 數據結構創建（4 個類）
- ✅ 三個轉換函數
- ✅ 驗證函數
- ✅ DNA 生成
- ✅ 邊界情況（空數據、極端值、大數據量）
- ✅ 人格路由
- ✅ 完整集成流程

---

## 驗收清單

### ✅ 框架部分（已完成）
- ☑ 數據結構定義
- ☑ SancaiSyncHub 核心類
- ☑ 三個轉換函數實現
- ☑ 驗證函數
- ☑ DNA 生成函數
- ☑ JSON 導出函數
- ☑ 完整測試套件（30+ 測試用例）

### ✅ 驗收標準
- ✅ 雙向轉換無損: v4.1 → v3.0 → v4.1 字段完整
- ✅ 三環無死鎖: verify_sync() 通過
- ✅ DNA 可追溯: 父子鏈完整·不可篡改
- ✅ 全代碼路徑覆蓋: 100% 單元測試
- ✅ 集成測試: 三環完整流程通過

---

## 文件結構

```
cnsh/sancai_sync/
├── __init__.py                  # 包入口
├── sancai_sync_hub.py           # 核心類與函數（~550 行）
├── README.md                    # 此文檔
├── DELIVERY_RECEIPT.md          # 交付回執
└── tests/
    ├── __init__.py
    └── test_sancai_sync_hub.py  # 完整測試套件（~400 行）
```

---

## 相關模塊

- **v4.1 決策闢**: `cnsh/flow_decision/`
- **v3.0 呼吸大腦**: 外部模塊
- **v4.0 神經映射**: 外部模塊

---

## 聯繫與反饋

**作者**: UID9622·諸葛鑫·龍芯北辰

**責任**: UID9622·不免責

**DNA**: `#龍芯⚡️2026-06-06-SANCAI-SYNC-README-v1.0`
