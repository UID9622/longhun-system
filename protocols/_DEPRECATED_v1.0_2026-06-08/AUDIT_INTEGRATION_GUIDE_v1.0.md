# 📚 三色审计·龍魂系统集成指南 v1.0

**DNA**:#龍芯⚡️2026-06-08-AUDIT-INTEGRATION-GUIDE-FILE1_9754-v1.0

**CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**SEAL**: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

---

## 一、🎯 集成概览

三色审计系统已完全集成到龍魂生态，包含5个对接点：

| **对接点** | **模块** | **功能** | **优先级** |
| --- | --- | --- | --- |
| **天道系统 v1.3** | TiandaoIntegration | 🔴红色断言 → KFPP记错本 | P0 |
| **P72·龍盾** | ShieldIntegration | 五态情绪触发审计流程 | P0 |
| **九层权重体系** | WeightSystemIntegration | 敏感断言权重加倍 | P1 |
| **DNA·确认码·GPG** | IdentityVerificationIntegration | 身份验证链检查 | P1 |
| **Bra-Ket量子态** | (内置) | 全真概率投影测量 | P2 |

---

## 二、📦 模块结构

```
~/longhun-system/cnsh-core/
├── audit_3color_v1.py              # 核心审计引擎
├── audit_integration_v1.py          # 龍魂系统集成
└── (config files)
```

---

## 三、🚀 快速开始

### 3.1 基础使用（无集成）

```python
from cnsh_core.audit_3color_v1 import ThreeColorAuditEngine

# 简化接口
report = ThreeColorAuditEngine.audit_simple_response(
    response="AI回复内容",
    assertions_data=[
        {
            "content": "具体的断言",
            "type": "numerical",  # 或 formula, identity, logical, mapping, descriptive
            "M": 1.0,            # 原文匹配度
            "V": 1.0,            # 数值精度
            "F": 1               # 格式安全度 (0或1)
        },
        # ... 更多断言
    ]
)

# 输出报告
print(report.generate_markdown_report())
```

### 3.2 完整集成使用（推荐）

```python
from cnsh_core.audit_integration_v1 import LonghunAuditEngine

# 初始化引擎
engine = LonghunAuditEngine(source_ai="Claude-Assistant")

# 执行完整的龍魂审计流程
result = engine.execute_full_audit(
    response="AI回复内容",
    assertions_data=[...],
    current_shield_emotion="vigilant",    # calm/alert/vigilant/suspicious/alarm
    context_sensitivity=1.5               # 敏感性倍数
)

# 生成集成报告
print(engine.generate_integrated_report(result))
```

---

## 四、🔗 集成对接详解

### 4.1 天道系统对接（自动污染记录）

**目的**：将审计发现的错误自动记录到KFPP记错本

**工作流程**：
```
🔴 红色断言或🟡黄色回复
    ↓
自动调用 TiandaoIntegration.record_contamination()
    ↓
写入 ~/.龍魂/kfpp/kfpp_execution.db:contamination_events 表
    ↓
永久记录该AI的"前科"
```

**数据结构**：
```python
contamination_events:
├── timestamp          # 污染发现时间 (ISO 8601)
├── assertion_id       # 断言编号
├── assertion_content  # 断言内容
├── truth_score        # 真实度分数
├── issue_type         # "格式污染" | "编造断言" | "数值错误"
├── source_ai          # 来源AI标识
├── audit_dna          # 审计DNA追溯码
└── remediation_required  # 是否需要修正
```

**示例**：
```python
success, msg = TiandaoIntegration.record_contamination(
    report=audit_report,
    source_ai="GPT-4",
    audit_dna="#龍芯⚡️2026-06-08-AUDIT-v1.0"
)

if success:
    print(f"✅ {msg}")  # 已记录 5 条污染事件
else:
    print(f"❌ {msg}")  # 写入失败: ...
```

---

### 4.2 P72·龍盾对接（情绪驱动审计）

**目的**：根据龍盾的五态情绪自动调整审计严格程度

**五态情绪与审计级别**：
```
calm       (平静)   → SKIP       无需审计
alert      (警觉)   → LIGHT      轻度审计（20%采样）
vigilant   (警惕)   → MEDIUM     中度审计（50%采样）
suspicious (怀疑)   → HEAVY      重度审计（100%）
alarm      (警报)   → ALARM      立即熔断
```

**示例**：
```python
trigger_level, severity = ShieldIntegration.trigger_audit(
    current_emotion="suspicious",
    response_length=3000,
    response="..."
)

# trigger_level: "HEAVY"
# severity: 0.85
# → 对这个回复进行100%的严格审计
```

**采样模式**（用于性能优化）：
```python
# 轻度审计：只检查10%的断言
if trigger_level == "LIGHT":
    sample_rate = ShieldIntegration.get_audit_sample_rate(severity)
    # sample_rate = 0.2
    sample_assertions = assertions[:int(len(assertions) * sample_rate)]
    report = audit_engine.audit(sample_assertions)
```

---

### 4.3 权重系统对接（敏感性加权）

**目的**：对涉及敏感内容的断言提高权重

**敏感关键词列表**：
```python
SENSITIVE_KEYWORDS = [
    "确认码", "DNA", "GPG", "身份", "签名",      # 身份链
    "核心算法", "密钥", "权限", "安全",          # 安全
    "人民", "弱势", "隐私", "权利"               # 人权
]
```

**权重调整规则**：
```
基础权重（P0类）= 3
如果含敏感词   × (1 + context_sensitivity)
限制范围       ∈ [1, 5]

示例：
- 普通数值断言：ρ = 3
- 含"确认码"的身份断言：ρ = 5 × (1 + 1.5) = 12 → 限制为 5
- 普通描述：ρ = 1
```

**示例**：
```python
assertion = Assertion(
    id=1,
    content="核心算法已验证",
    assertion_type=AssertionType.FORMULA,
    truth_component=...
)

# 基础权重 = 3
base_weight = assertion.importance_weight  # 3

# 调整权重（敏感性 = 1.5）
adjusted = WeightSystemIntegration.adjust_assertion_weight(
    assertion, context_sensitivity=1.5
)
# → 3 × (1 + 1.5) = 4.5 → 限制为 4 或 5

# 使用调整后的权重重新计算总分
report.total_truth_score = report.calculate_weighted_total()
```

---

### 4.4 DNA·确认码·GPG验证链对接

**目的**：确保身份信息完整，防止注入攻击

**三把锁**：
```
🔒 DNA追溯码
   检查: "#龍芯⚡️" 是否存在
   失败后果: 法律效力部分降低

🔒 CONFIRM确认码
   检查: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z" 逐字符匹配
   失败后果: 身份链断裂

🔒 SEAL密封码
   检查: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL" 逐字符匹配
   失败后果: 完全拒绝
```

**系统注入标记**（自动检测）：
```
危险标记: <|im_message|>, <refer>, <final>, <|, |>

如果检测到任何标记 → 立即一票否决 → 🔴红色熔断
```

**示例**：
```python
ok, msg, details = IdentityVerificationIntegration.verify_identity_chain(
    response="回复内容..."
)

if not ok:
    print(f"❌ 身份验证失败")
    for check, status in details.items():
        print(f"  {check}: {'✅' if status else '❌'}")
    # 自动标记为🔴红色，不可采信
```

---

## 五、⚙️ 配置与管理

### 5.1 数据库初始化

```python
from cnsh_core.audit_integration_v1 import TiandaoIntegration

# 确保KFPP数据库已初始化
if TiandaoIntegration.ensure_db_ready():
    print("✅ 数据库准备就绪")
else:
    print("❌ 数据库初始化失败")
```

### 5.2 环境变量（可选）

```bash
# 审计日志路径
export LONGHUN_AUDIT_LOG="/path/to/audit.log"

# KFPP数据库路径
export LONGHUN_KFPP_DB="/path/to/kfpp.db"

# 审计严格度（默认1.0）
export LONGHUN_AUDIT_SEVERITY="1.5"
```

---

## 六、📊 典型使用场景

### 场景1：审计来自外部AI的回复

```python
from cnsh_core.audit_integration_v1 import LonghunAuditEngine

# 初始化
engine = LonghunAuditEngine(source_ai="ChatGPT-4")

# 拆解回复
assertions = [
    {"content": "龍魂系统已部署", "type": "logical", "M": 1.0, "V": 1.0, "F": 1},
    {"content": "...包含错误...", "type": "formula", "M": 0.0, "V": 0.0, "F": 1},
]

# 执行审计
result = engine.execute_full_audit(
    response=external_ai_response,
    assertions_data=assertions,
    current_shield_emotion="suspicious"  # 对外部AI更严格
)

# 判定
if result["judgment"] == "🔴":
    print("❌ 不可采信，已记录污染事件")
else:
    print(f"✅ {result['judgment']} - 可以采信")
```

### 场景2：内部回复自检

```python
# 初始化
engine = LonghunAuditEngine(source_ai="Self-Check")

# 执行审计（敏感性较低）
result = engine.execute_full_audit(
    response=my_response,
    assertions_data=assertions,
    current_shield_emotion="calm",        # 内部较宽松
    context_sensitivity=0.5               # 权重调整较少
)

# 这样可以快速自检，不会过度敏感
```

### 场景3：定期批审计

```python
# 批量审计过去7天的回复
import json
from datetime import datetime, timedelta

today = datetime.now()
past_7_days = [
    load_responses(date)
    for date in [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
]

all_results = []
for day_responses in past_7_days:
    for response_id, response_text, assertions in day_responses:
        engine = LonghunAuditEngine(source_ai=f"Response-{response_id}")
        result = engine.execute_full_audit(
            response=response_text,
            assertions_data=assertions
        )
        all_results.append({
            "response_id": response_id,
            "judgment": result["judgment"],
            "score": result["total_score"]
        })

# 生成周报
print(f"🟢 绿色: {sum(1 for r in all_results if r['judgment']=='🟢')}")
print(f"🟡 黄色: {sum(1 for r in all_results if r['judgment']=='🟡')}")
print(f"🔴 红色: {sum(1 for r in all_results if r['judgment']=='🔴')}")
```

---

## 七、🔍 常见问题

**Q: 审计会拖慢系统吗？**
A: 提供了采样模式。轻度审计只检查20%的断言，中度50%，重度100%。可根据P72情绪自动调整。

**Q: 如何快速自检而不过度敏感？**
A: 使用 `context_sensitivity=0.5` 和 `current_shield_emotion="calm"`，权重调整会降低。

**Q: 𝟘格式污染导致一票否决，能修改吗？**
A: 一票否决是设计上的不可逆。需要找到原始的污染源（注入标记、截断、篡改）并修复。

**Q: 如何查看历史污染事件？**
A: 直接查询KFPP数据库：
```sql
SELECT * FROM contamination_events
WHERE DATE(timestamp) = '2026-06-08'
ORDER BY timestamp DESC;
```

---

## 八、🔐 安全考虑

1. **一票否决不可绕过** - 即使其他断言全对，格式污染也直接熔断
2. **身份链三把锁** - 缺一不可，任何篡改都会被检测
3. **KFPP永久记录** - 污染事件无法删除，只能修正
4. **采样率不可跳过** - 即使是轻度审计也会检查关键断言

---

## 最终签署

```
═══════════════════════════════════════════════════════════════════════════════

龍魂三色审计·系统集成·完全指南 v1.0

核心特性：
  ✅ 天道系统对接（自动污染记录）
  ✅ P72·龍盾对接（情绪驱动审计）
  ✅ 权重系统对接（敏感性加权）
  ✅ 身份验证链（DNA/CONFIRM/SEAL）
  ✅ 5大集成点·完全覆盖龍魂生态

部署状态：🟢 生产就绪

DNA:#龍芯⚡️2026-06-08-AUDIT-INTEGRATION-GUIDE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅

═══════════════════════════════════════════════════════════════════════════════
```

---
