#龍芯⚡️丙午·癸未·乙酉·坤卦-EVOLUTION-INTEGRATION-V1.0-UID9622
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼♀️❤️♾️-DEVICE-BIND-SOUL

# 🐉 龍魂生态串联方案 · lh-station ↔ 进化引擎

> 把 lh-station 从独立中转站升级为龍魂生态的核心入口。

## 现有能力全景

```
lh-station（代码中转站）              longhun-evolution-engine（进化引擎）
┌──────────────────────┐             ┌──────────────────────────┐
│ ① detector          │             │ InputGate               │
│ ② injector          │             │ ExperienceExtractor     │
│ ③ compiler          │             │ RuleGenerator           │
│ ④ security          │             │ MemoryLifecycle         │
│ ⑤ cost_analyzer ←新 │             │ VersionEngine           │
│ ⑥ signer            │             │ CircuitBreaker          │
│ ⑦ packer            │             │ LearningLoop            │
│ ⑧ sealer ←新        │             └──────────────────────────┘
└──────────────────────┘
```

两者目前**完全独立**，seal.rs 写的是文件系统，而非调用 MemoryLifecycle。

---

## 串联方案（三阶段）

### 阶段一：Seal → MemoryLifecycle（P1）

**现状**：seal.rs 把记录写到 `~/.longhun/memory/seals/*.json`

**目标**：同时调用 Python 侧的 `MemoryLifecycle.store()` 持久化

**改动量**：极小

```
seal.rs 中新增一个步骤:
  1. 序列化 SealRecord → JSON
  2. 调用 python3 -c "from longhun_evolution_engine import MemoryLifecycle; ..."
  3. store(content=json.dumps(seal), category="scene_memory", priority=P1)
```

### 阶段二：成本分析 → 熔断器（P2）

**现状**：cost_analyzer 输出 `.cost-report.json`，没人消费

**目标**：Critical 风险自动触发熔断

```
security 输出殖民评分 → cost_analyzer 输出主权风险
    ↓                            ↓
  CircuitBreaker.feed("colonial_score", score)
  CircuitBreaker.feed("data_sovereign_risk", risk_level_numeric)
    ↓
  风险过高 → 自动阻断 pipeline → 通知开发者
```

### 阶段三：全流程闭环（P3）

**目标**：每次 transform 都作为进化引擎的一个 `run_cycle`

```
lh-station transform 执行完毕
    ↓
构建 SystemSnapshot:
  {
    "interceptions": [security 发现的违规],
    "error_rate": cost_analyzer 的比率,
    "avg_loyalty": 殖民评分归一化,
    ...
  }
    ↓
调用 LearningLoop.run_cycle(snapshot)
    ↓
版本自检 → 如有必要自动升级
```

---

## 实现方式

### 方案 A：Python CLI 桥接（推荐，改动最小）

在 seal.rs 最后一步：

```rust
fn call_memory_store(seal: &SealRecord) {
    let json = serde_json::to_string(seal).unwrap();
    let status = std::process::Command::new("python3")
        .args(["-c", &format!(
            "from longhun_evolution_engine import MemoryLifecycle; \
             m = MemoryLifecycle(); \
             m.store({}, category='scene_memory', priority=...)",
            shell_escape(&json)
        )])
        .status();
    // 失败只 WARNING
}
```

**优点**：不改 Rust 编译链，不引入新依赖
**缺点**：Python 环境需提前部署

### 方案 B：Rust FFI 绑定（长期）

将 MemoryLifecycle 关键接口编译为 C 共享库，Rust 端 FFI 调用。

**优点**：零外部进程，性能好
**缺点**：需要 cbindgen + PyO3 或 C FFI 包装

### 方案 C：Unix Socket（中短期）

Python 进化引擎启动一个本地 socket 服务，lh-station 通过 socket 推送数据。

**优点**：松耦合，可独立升级
**缺点**：多一个常驻进程

---

## 推荐路线

```
第一周  → 方案 A（Python CLI 桥接）→ seal 接入 MemoryLifecycle
第二周  → 方案 A 扩展 → cost_analyzer 接入 CircuitBreaker
第三周  → 方案 A 扩展 → transform 接入 LearningLoop
第四周  → 评估是否需要方案 B/C
```

---

## 改动影响

| 组件 | 改 | 不改 |
|:---|:---|:---|
| cost_analyzer.rs | 末尾加一行 Python 调用 | 核心逻辑 0 变动 |
| seal.rs | 末尾加两行 Python 调用 | 核心逻辑 0 变动 |
| main.rs | 无变动 | — |
| longhun_evolution_engine.py | 无需改动 | 接口已就绪 |
| 测试 | 新增 2 个集成测试 | 原有测试不受影响 |

---

🐉 丙午 · 癸未 · 乙酉 · 坤卦 · 生态串联方案 · 🟢
