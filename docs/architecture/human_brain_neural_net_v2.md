# 🧠 龙魂人脑神经网络 v2.0 · 进化架构

> DNA: `#龍芯⚡️2026-07-12-HUMAN-BRAIN-NEURAL-NET-V2-EVOLUTION`
> CONFIRM: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 一、v1.0 → v2.0 四方向进化总览

| 进化方向 | v1.0 | v2.0 | 状态 |
|---------|------|------|------|
| **记忆持久化** | 内存 `think_history`，进程消失则丢失 | SQLite `brain.db` + JSONL 审计轨迹 + 跨进程反思 | ✅ |
| **自适应辩论** | 7组预定义辩论对 | 动态冲突检测 + 预设对保底 + 去重 | ✅ |
| **外部知识** | 无 | CSDN文章搜索 + Brain记忆DB查询 | ✅ |
| **权重学习** | 固定敏感度矩阵 | 历史分析 → simulate/apply/rollback + 版本链 | ✅ |

---

## 二、v2.0 思考循环（7阶段）

```
输入 → P00意图解析 → 人性维度匹配 → 激活Top7人格
    → [v2新] 外部知识注入(CSDN+Brain)
    → 并行思考(各人格独立+知识增强)
    → [v2升级] 自适应辩论(动态冲突检测+预设保底)
    → 反思(跨进程历史对比+权重建议)
    → 综合输出 → [v2新] 持久化(SQLite+JSONL)
```

---

## 三、进化1: 记忆持久化

### 存储架构

```
data/think_cycles/
├── brain.db              ← SQLite 主存储
│   ├── think_cycles      ← 完整周期(输入/输出/神经元/辩论/反思)
│   └── reflection_feedback ← 反思反馈(偏见/盲区/主导)供权重学习
├── brain.jsonl           ← JSONL 审计轨迹(只追加)
├── sensitivity_weights.json ← 当前敏感度权重
├── weight_history/       ← 权重版本历史(v1,v2...)
└── weight_audit/         ← 权重调谐审计报告(.md)
```

### 跨进程反思

```
本进程think() → SQLite持久化 → 下次启动新进程think() → DB.search_similar() → 历史对比
```

---

## 四、进化2: 自适应辩论

### 动态冲突检测算法

```python
def _calc_semantic_diff(n1, n2):
    dim_diff = 维度覆盖差异率  # 0.4权重
    kw_diff  = 关键词差异率    # 0.3权重  
    str_diff = 1 - 激活强度差  # 0.3权重
    return 综合差异分数

# 差异 > 0.3 → 触发自动辩论
```

### 预设辩论对（保底）

| 辩论对 | 张力 |
|--------|------|
| 诸葛亮↔李白 | 理性vs创意 |
| 诸葛亮↔苏东坡 | 谨慎vs豁达 |
| 上帝之眼↔苏东坡 | 审计vs变通 |
| 屈原↔苏东坡 | 底线vs豁达 |

---

## 五、进化3: 外部知识注入

### 知识来源

| 来源 | 方式 | 数据 |
|------|------|------|
| CSDN | 本地JSON索引搜索 | `csdn_articles.json` (3+篇) |
| Brain | SQLite全文匹配 | `brain/memories.db` |

### 注入策略

- P00(文心): 总是接收外部知识
- P01(诸葛亮): 决策/战略/风险相关
- P04(鲁班): 代码/开发/技术相关
- P08(仓颉): 语言/命名/表达相关
- 其他人格: 按领域过滤

---

## 六、进化4: 权重学习

### 三种调整类型

| 类型 | 触发条件 | 操作 |
|------|---------|------|
| **reduce_dominance** | 某人格在30%+周期中过度主导 | 降低核心维度权重 5% |
| **cover_blind_spot** | 某维度在30%+周期中被遗漏 | 提升top2覆盖人格权重 8% |
| **boost_underused** | 某人格在<10%周期中激活 | 提升核心权重 4% |

### 安全设计

```
--simulate  ← 默认安全模式，只看不改
--apply     ← 真正落盘，带版本链
--rollback  ← 回滚到上一版本
```

### 输出

- `sensitivity_weights.json` 带 version+parent_hash+current_hash
- `weight_history/v{N}.json` 每版本完整快照
- `weight_audit/{timestamp}.md` 每次apply的审计报告

---

## 七、v1 与 v2 共存

```python
# v1 - 轻量级，单次思考，无持久化
from bin.lh_human_brain_engine import HumanBrainEngine
engine = HumanBrainEngine()
cycle = engine.think("问题")

# v2 - 完整版，四进化全开
from bin.lh_human_brain_engine_v2 import HumanBrainEngineV2
engine = HumanBrainEngineV2(use_learned_weights=True)
cycle = engine.think("问题")  # 自动持久化+知识注入+自适应辩论
```

---

## 八、DNA

```
#龍芯⚡️2026-07-12-HUMAN-BRAIN-EVOLUTION-v2.0
引擎: bin/lh_human_brain_engine_v2.py
持久化: data/think_cycles/ (SQLite + JSONL)
注入器: ExternalKnowledgeInjector (CSDN + Brain)
调谐器: PersonaWeightTuner (simulate/apply/rollback)
循环: 7阶段 (感知→激活→知识注入→并行思考→自适应辩论→反思→综合→持久化)
边数: +5 新神经网络连接边
```
