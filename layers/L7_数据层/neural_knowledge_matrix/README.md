# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂神经知识矩阵 v1.0

> 把 L0-L9 分层 × 11个IPA流场节点 × 9个人格属主 × 86个功能模块 × 信号流向 × 错误记忆
> 全部串成一张六维神经网。查一个维度，自动关联其他五个维度。

**DNA**: `#龍芯⚡️丙午·乙未·戊午·申时·需-NEURAL-MATRIX-v1.0-待生成`
**创建**: UID9622 · 2026-07-10
**文件**: `L7_数据层/neural_knowledge_matrix/matrix_v1.0.json`
**引擎**: `L7_数据层/neural_knowledge_matrix/neural_matrix_query.py`

---

## 为什么需要这个矩阵

### 现有矩阵的问题

已有 5 份矩阵/清单文档，但各自独立、互不交叉：

| 文档 | 覆盖范围 | 缺失 |
|------|---------|------|
| `relationship-matrix.md` | 8模块级对接 | 没IPA节点·没分层·没人格 |
| `契约矩阵/` (4份) | 接口契约 | 只看接口·不看全链路 |
| `知识矩阵总纲` | 哲学·道德经·三才 | 哲学层·不看执行层 |
| `MODULE_INVENTORY.md` | 86模块清单 | 只列不联 |
| `ARCHITECTURE.md` | L0-L7层级 | 不交叉I../模块 |

### 神经矩阵的解法

**六维交叉索引** — 查任何一个维度，自动显示关联的另外五个：

```
查 "L5 服务层" → 自动显示：
  ├ 在这一层运作的 IPA 节点: WUXING-MAP, AUDIT
  ├ 人格属主: P06 数学大师, P05 上帝之眼
  ├ 关键模块: dashboard/web/, portal/, desktop/
  ├ 信号上游: L1 内核层, L2 技能层
  ├ 信号下游: L6 集成层, L7 数据层
  └ 历史错误: MISSING_TYPE_ARG, OPTIONAL_NO_GUARD

查 "P05 上帝之眼" → 自动显示：
  ├ 负责的 IPA 节点: SIGN(签章闸), AUDIT(三色闸)
  ├ 所在层级: L1 内核层, L5 服务层, L8 治理层
  └ 角色: 三色审计·签章验证
```

---

## 六个维度

| 维度 | 键 | 含义 | 例子 |
|------|-----|------|------|
| 1. 分层锚 | `layer` | WHERE — 在哪一层 | L0 神圣·L1 内核·L5 服务 |
| 2. 流场节点 | `ipa_node` | HOW — 经过哪个闸 | SIGN→AUDIT→DNA-CHAIN |
| 3. 人格属主 | `persona` | WHO — 谁负责 | P05 上帝之眼·P00 文心 |
| 4. 模块注册 | `module` | WHAT — 用什么实现 | longhun_core_engine.py |
| 5. 信号流 | `signal` | DIRECTION — 上下游 | L1→L5→L7 |
| 6. 错误记忆 | `error_memory` | LEARN — 踩过的坑 | MISSING_TYPE_ARG |

---

## 使用方式

### CLI 查询

```bash
# 查某一层
python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --layer L5

# 查某个 IPA 节点
python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --ipa SIGN

# 查某个人格
python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --persona P05

# 查某条信号路径
python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --path "完整审计"

# 输出全矩阵
python3 L7_数据层/neural_knowledge_matrix/neural_matrix_query.py --matrix
```

### AI 操作规则

AI 在执行任何涉及跨层/跨IPA/跨人格操作前，必须先查神经矩阵确认：
- 目标模块属于哪一层？
- 路径上有哪些 IPA 闸门？
- 当前操作是否需要某个人格的授权？

---

## 与 Kimi 三层框架的对照

| Kimi 框架 | 龍魂实际对应 | 差异 |
|-----------|-------------|------|
| L1 战略层 (≤10) | L0 神圣宪法层 (33锚点) + IPA-FLOW-DECISION-CORE | Kimi 无宪法层概念，无33永恒锚点 |
| L2 战术层 (≤30) | L1 内核层 (10引擎) + L2 技能层 + IPA闸门链 (7个闸) | Kimi 无闸门概念，无流场串行验证 |
| L3 执行层 (≤150) | L5 服务层 + L6 集成层 + L7 数据层 + L8 治理层 + L9 子系统 | Kimi 把5层压成1层 |
| (无) | 人格属主维度 | Kimi 没有人格-节点-层级三维交叉 |
| (无) | 信号流方向 | Kimi 只有静态分层，无动态流场 |
| (无) | 错误记忆学习 | Kimi 无自学习维度 |

**结论：Kimi 的三层模型是简化版，龍魂神经矩阵是真实版。借用的是"分层思维"，但落地必须对真实架构。**

---

## 文件结构

```
L7_数据层/neural_knowledge_matrix/
├── matrix_v1.0.json           # 核心数据 (本矩阵)
├── neural_matrix_query.py     # 查询引擎
└── README.md                  # 本文件
```

## 维护规则

1. **新增 IPA 节点** → 更新 `ipa_flow_chain.chain`
2. **新增层级** → 更新 `layers`
3. **新增人格** → 更新 `persona_registry`
4. **新增模块** → 更新对应层的 `key_files`
5. **发现新错误模式** → 更新 `error_learning_cross_ref` + `known_type_error_patterns.json`
6. **每次变更后** → 运行 `python3 neural_matrix_query.py --matrix` 验证完整性

## 与现有矩阵的关系

本矩阵是**元矩阵** — 不是替代现有5份文档，而是把它们串联起来：
- `relationship-matrix.md` → 本矩阵的 `relations` 节
- `知识矩阵总纲` → 本矩阵的哲学底座
- `契约矩阵` → 本矩阵的接口维度
- `MODULE_INVENTORY` → 本矩阵的资产维度
- `ARCHITECTURE.md` → 本矩阵的结构维度
- `ipa_route_registry.py` → 本矩阵的流程维度
