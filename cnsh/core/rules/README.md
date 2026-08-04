# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂规则引擎 (LongHun Rule Engine)

**DNA**:#龍芯⚡️2026-06-03-RULE-ENGINE-README-FILE1-v1.0
**状态**: 🟢 MAIN·可公开
**责任**: UID9622·不免责

---

## 概述

龍魂规则引擎是龍魂系统的 **业务规则执行器**，作为 P1-2 阶段的核心组件，负责：

- 将系统各类决策逻辑（审计、评估、调度）规则化、可配置化
- 复用已有的路由、审计、调度、DNA 基础设施
- 为工作流引擎（P2-1）提供原子化的决策单元
- 统一管理业务规则的生命周期和质量治理

### 核心特性

✅ **高效查找** - O(1) 内存字典查找
✅ **三色状态** - 🟢 ACTIVE / 🟡 TESTING / 🔴 DEPRECATED
✅ **DNA 追溯** - 每条规则绑定不可伪造的追溯码
✅ **Append-Only 持久化** - JSONL 格式，仅追加不覆盖
✅ **优先级队列** - 规则按优先级自动排序执行
✅ **自检能力** - 完整的 selftest 验证机制

---

## 快速开始

### 安装和导入

```python
from cnsh_core.rules import (
    get_rule_engine,      # 获取全局规则引擎实例
    Rule,                 # 规则数据类
    RuleType,             # 规则类型枚举
    RuleStatus,           # 规则状态枚举 (三色)
    RulePriority,         # 优先级枚举
)
```

### 获取规则引擎实例

```python
# 获取全局规则引擎（单例模式）
engine = get_rule_engine()

# 或者重置并获取新实例（仅用于测试）
from cnsh_core.rules import reset_rule_engine
reset_rule_engine()
engine = get_rule_engine()
```

### 注册规则

```python
from cnsh_core.rules import Rule, RuleType, RuleStatus, RulePriority

# 创建规则
rule = Rule(
    rule_id="RULE-CUSTOM-001",
    name="my_audit_rule",
    rule_type=RuleType.AUDIT,
    status=RuleStatus.ACTIVE,
    condition="'score' in context and context['score'] >= 50",
    action="three_color_judgment",
    priority=RulePriority.MEDIUM,
    dna="#龍芯⚡️2026-06-03-CUSTOM-RULE-v1.0",
    layer="L1_SEASONAL",
    description="我的自定义审计规则",
    tags=["custom", "audit"],
    dependencies=[],
    audit_required=True,
    confirm_required=False,
)

# 注册规则
success, msg = engine.register_rule(rule)
if success:
    print(f"✅ {msg}")
else:
    print(f"❌ {msg}")
```

### 执行规则

```python
# 执行单条规则
context = {"score": 85}  # 执行上下文
result = engine.execute_rule("RULE-CUSTOM-001", context)

print(f"执行结果:")
print(f"  - 成功: {result['success']}")
print(f"  - 颜色: {result['color']}")  # 🟢/🟡/🔴
print(f"  - 消息: {result['message']}")
print(f"  - 耗时: {result['execution_time']:.3f}s")
```

### 批量评估规则

```python
# 评估所有活跃的审计规则
context = {"score": 75, "operation": "sudo"}
results = engine.evaluate(
    context,
    rule_type=RuleType.AUDIT,  # 仅评估审计规则（可选）
    priority_min=RulePriority.HIGH  # 仅评估高优先级及以上（可选）
)

for result in results:
    print(f"{result['rule_id']}: {result['color']}")
```

### 列出和查找规则

```python
# 列出所有活跃的规则
active_rules = engine.list_rules(status=RuleStatus.ACTIVE)

# 列出所有审计规则
audit_rules = engine.list_rules(rule_type=RuleType.AUDIT)

# 查找特定规则（O(1)）
rule = engine.find_rule("RULE-AUDIT-001")
if rule:
    print(f"找到规则: {rule.name}")
```

---

## 规则数据模型

### RuleType（规则类型）

| 类型 | 说明 | 示例 |
|------|------|------|
| `CONDITION` | 条件规则 (if-then 判断) | 根据分数返回 🟢/🟡/🔴 |
| `ACTION` | 动作规则 | 发送通知、修改状态 |
| `WORKFLOW` | 工作流规则 (多步骤) | 顺序执行多个动作 |
| `FORMULA` | 公式规则 (数学计算) | 数字根判定、时间衰减 |
| `AUDIT` | 审计规则 | 质量评估、安全检查 |
| `VALIDATION` | 验证规则 | 合法性检查、格式验证 |
| `ROUTING` | 路由规则 | 决策分支、流程导向 |

### RuleStatus（规则状态）- 三色系统

| 状态 | 符号 | 含义 | 信心度 |
|------|------|------|--------|
| `ACTIVE` | 🟢 | 活跃·正常使用 | ≥ 85% |
| `TESTING` | 🟡 | 测试中·待验证 | 60-85% |
| `DEPRECATED` | 🔴 | 已废弃·禁止调用 | < 60% |

### RulePriority（优先级）

| 级别 | 范围 | 用途 |
|------|------|------|
| `CRITICAL` | 1-20 | 安全/身份/一票否决 |
| `HIGH` | 21-40 | 权限控制/审计检查 |
| `MEDIUM` | 41-70 | 业务规则/决策逻辑 |
| `LOW` | 71-100 | 日志/统计/通知 |

### Rule 数据类

```python
@dataclass
class Rule:
    # 基础信息
    rule_id: str                    # RULE-L1-001
    name: str                       # three_color_audit
    rule_type: RuleType             # RuleType.AUDIT
    status: RuleStatus              # RuleStatus.ACTIVE

    # 执行信息
    condition: str                  # Python 表达式
    action: str                     # 执行函数名
    priority: int = 50              # 优先级 (1-100)

    # 追溯信息
    dna: str = ""                   # DNA 追溯码
    layer: str = "L1_SEASONAL"      # 时间层级 (L0-L4)

    # 描述和元数据
    description: str = ""           # 规则描述
    tags: List[str] = []            # 标签列表
    dependencies: List[str] = []    # 依赖的规则

    # 审计和控制
    audit_required: bool = True     # 是否需要审计
    confirm_required: bool = False  # 是否需要确认

    # 时间戳
    created_at: str                 # ISO 格式创建时间
    updated_at: str                 # ISO 格式更新时间

    # 扩展
    metadata: Dict[str, Any] = {}   # 其他元数据
```

---

## 内置规则库

龍魂系统预装 4 条核心内置规则，在系统启动时自动加载：

### RULE-AUDIT-001: 三色审计

```python
规则ID: RULE-AUDIT-001
名称: three_color_audit
类型: AUDIT
优先级: HIGH (21)
DNA:#龍芯⚡️2026-06-03-THREE-COLOR-AUDIT-v1.0

条件: 'score' in context
动作: three_color_judgment

判定规则:
  score >= 80: 🟢 PASS (通过)
  50 <= score < 80: 🟡 REVIEW (待审)
  score < 50: 🔴 BLOCK (阻断)
```

使用示例：

```python
result = engine.execute_rule("RULE-AUDIT-001", {"score": 85})
# result['color'] = '🟢'
```

### RULE-VETO-001: 一票否决

```python
规则ID: RULE-VETO-001
名称: veto_alert
类型: AUDIT
优先级: CRITICAL (1)
DNA:#龍芯⚡️2026-06-03-VETO-ALERT-v1.0

触发词: 密钥、sudo、rm、push --force、token、私钥、.env 等高危操作

判定规则:
  - 如果 confirmed=True: 🟢 允许
  - 否则: 🔴 阻止
```

使用示例：

```python
# 检测到高危操作，一票否决
result = engine.execute_rule("RULE-VETO-001", {
    "operation": "sudo",
    "confirmed": False
})
# result['color'] = '🔴'
```

### RULE-FORMULA-001: 数字根判定

```python
规则ID: RULE-FORMULA-001
名称: digital_root_gate
类型: FORMULA
优先级: MEDIUM (41)
DNA:#龍芯⚡️2026-06-03-DR-GATE-v1.0

判定规则 (基于数字根):
  dr ∈ {3, 9}: 🔴 (阻断)
  dr = 6: 🟡 (待审)
  其他: 🟢 (通过)
```

使用示例：

```python
result = engine.execute_rule("RULE-FORMULA-001", {"value": 123})
# 1+2+3=6, dr=6 → result['color'] = '🟡'
```

### RULE-FORMULA-002: 时间衰减

```python
规则ID: RULE-FORMULA-002
名称: time_decay
类型: FORMULA
优先级: MEDIUM (41)
DNA:#龍芯⚡️2026-06-03-TIME-DECAY-v1.0

衰减公式: L = L₀ * T^(-α_τ)

用于判断内容是否过期，基于时间层级 (L0-L4) 的衰减系数。
```

使用示例：

```python
result = engine.execute_rule("RULE-FORMULA-002", {
    "age_days": 30,
    "layer": "L2_DECENNIAL"
})
```

---

## 规则执行流程

规则执行遵循以下流程：

```
┌─────────────────────┐
│ 执行 execute_rule() │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 【第1步】评估条件   │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
  条件满足     条件不满足
    │             │
    │        返回 🟢 (skip)
    │
    ▼
┌─────────────────────┐
│ 【第2步】执行动作   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 【第3步】审计检查   │
│ (if audit_required) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 返回执行结果        │
│ (success/result/    │
│  color/message)     │
└─────────────────────┘
```

---

## API 参考

### RuleEngine 类

#### `register_rule(rule: Rule) -> Tuple[bool, str]`

注册新规则

```python
rule = Rule(...)
success, msg = engine.register_rule(rule)
```

#### `find_rule(rule_id: str) -> Optional[Rule]`

查找规则（O(1) 时间复杂度）

```python
rule = engine.find_rule("RULE-AUDIT-001")
```

#### `execute_rule(rule_id: str, context: Dict) -> Dict`

执行单条规则

```python
result = engine.execute_rule("RULE-AUDIT-001", {"score": 85})
# Returns: {
#     "success": True,
#     "result": {...},
#     "color": "🟢",
#     "message": "...",
#     "execution_time": 0.001
# }
```

#### `evaluate(context: Dict, rule_type: Optional[RuleType] = None, priority_min: int = 1) -> List[Dict]`

批量评估规则

```python
results = engine.evaluate({"score": 75}, rule_type=RuleType.AUDIT)
```

#### `list_rules(rule_type: Optional[RuleType] = None, status: Optional[RuleStatus] = None) -> List[Rule]`

列出规则（支持过滤）

```python
active_rules = engine.list_rules(status=RuleStatus.ACTIVE)
audit_rules = engine.list_rules(rule_type=RuleType.AUDIT)
```

#### `get_statistics() -> Dict`

获取统计信息

```python
stats = engine.get_statistics()
# {
#     "total_rules": 10,
#     "by_status": {"🟢": 8, "🟡": 1, "🔴": 1},
#     "by_type": {"audit": 3, "formula": 2, ...},
#     "rule_file": "...",
#     "executor_stats": {...}
# }
```

#### `selftest() -> Tuple[bool, List[str]]`

自检规则引擎

```python
all_pass, errors = engine.selftest()
if all_pass:
    print("✅ 自检通过")
else:
    for error in errors:
        print(f"❌ {error}")
```

### 全局函数

#### `get_rule_engine(rule_file: str = None) -> RuleEngine`

获取全局规则引擎实例（单例模式）

```python
engine = get_rule_engine()
```

#### `reset_rule_engine()`

重置规则引擎（用于测试）

```python
reset_rule_engine()
```

---

## 性能特性

| 操作 | 时间复杂度 | 实际性能 |
|------|-----------|---------|
| find_rule() | O(1) | < 1ms |
| register_rule() | O(1)* | ~10ms |
| execute_rule() | O(1) | ~5ms |
| evaluate() | O(n)** | ~50ms (10规则) |
| list_rules() | O(n) | ~50ms |
| selftest() | O(n) | ~100ms |

*: 包含文件 I/O
**: n = 活跃规则数

---

## 与启动器集成

规则引擎在系统启动时自动初始化（第 8 步）：

```
[8/8] 初始化规则引擎和加载内置规则...
   ✅ 规则引擎就绪 (已加载 4 条内置规则)
   ✅ 规则引擎已注册到路由表 (IPA-L1-002)
```

规则引擎在路由表中注册为：

```
节点ID: IPA-L1-002
名称: rule_engine
类型: GATE
状态: 🟢 ACTIVE
入口: cnsh_core.rules.get_rule_engine
DNA:#龍芯⚡️2026-06-03-RULE-ENGINE-v1.0
```

---

## 故障排查

### 规则找不到

```python
rule = engine.find_rule("RULE-UNKNOWN")
# None

# 解决: 列出所有规则
all_rules = engine.list_rules()
for rule in all_rules:
    print(rule.rule_id)
```

### 规则注册失败

```python
# 错误: "依赖规则不存在: RULE-DEPENDENCY"

# 解决: 先注册依赖规则
dep_rule = Rule(rule_id="RULE-DEPENDENCY", ...)
engine.register_rule(dep_rule)

# 再注册主规则
main_rule = Rule(
    rule_id="MY-RULE",
    dependencies=["RULE-DEPENDENCY"],
    ...
)
engine.register_rule(main_rule)
```

### 条件评估失败

```python
# 如果条件中的变量不存在或语法错误，规则会返回 🟢（安全策略）

# 解决: 检查条件表达式
rule = engine.find_rule("MY-RULE")
print(f"条件: {rule.condition}")
# 确保条件中的所有变量都在 context 中
```

---

## 最佳实践

### 1. 规则 ID 命名规范

```python
# 格式: RULE-[LAYER]-[NUMBER]
# 例子:
RULE-L0-001  # L0 (Eternal) 层规则
RULE-L1-001  # L1 (Seasonal) 层规则
RULE-L2-001  # L2 (Decennial) 层规则
```

### 2. DNA 追溯码格式

```python
dna = "#龍芯⚡️2026-06-03-RULE-NAME-v1.0"
#      ├─ 龍芯标识
#      ├─ 日期
#      ├─ 规则名称
#      └─ 版本号
```

### 3. 条件表达式最佳实践

```python
# ❌ 不好: 复杂的条件
condition = "context.get('a', 0) > 5 and context.get('b', False) or context.get('c') == 'test'"

# ✅ 好: 清晰、简单的条件
condition = "context.get('score', 0) >= 50"

# ✅ 好: 配合上下文使用
context = {
    "score": 85,
    "age_days": 30,
    "operation": "sudo"
}
result = engine.execute_rule("RULE-AUDIT-001", context)
```

### 4. 依赖管理

```python
# 规则可以依赖其他规则
rule = Rule(
    rule_id="RULE-COMPOSED-001",
    dependencies=["RULE-AUDIT-001", "RULE-VALIDATION-001"],
    ...
)

# 注册时会自动检查依赖
success, msg = engine.register_rule(rule)
# 如果依赖不存在会失败
```

### 5. 日志记录

```python
# 规则执行会自动记录到系统日志
result = engine.execute_rule("RULE-AUDIT-001", {"score": 85})

# 查看规则执行日志
# ~/longhun-system/logs/system_log.jsonl
```

---

## 未来扩展（P2/P3 阶段）

### P2-1 工作流引擎

工作流将由多个规则组成的有向无环图（DAG）：

```python
workflow = [
    ("RULE-VALIDATION-001", "验证输入"),
    ("RULE-AUDIT-001", "审计检查"),
    ("RULE-ACTION-001", "执行动作"),
]
```

### P3 可视化管理界面

- 规则图形化编辑
- 执行历史追踪
- 性能监控仪表板

---

## 许可和责任

**DNA**:#龍芯⚡️2026-06-03-RULE-ENGINE-README-v1.0
**作者**: UID9622 · 诸葛鑫 · 龍芯北辰
**状态**: 🟢 MAIN·可公开
**责任**: UID9622·不免责

---

## 相关资源

- 启动器集成: `cnsh-core/core_system_launcher.py`
- 规则注册表: `02_rules/RULE-REGISTRY.local.jsonl`
- 路由注册表: `01_protocols/IPA-ROUTE-REGISTRY.local.md`
- 内置规则: `cnsh-core/rules/builtin_rules.py`
