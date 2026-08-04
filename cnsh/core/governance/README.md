# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂治理层系统 (Governance Layer)

**DNA**: `#龍芯⚡️2026-06-03-GOVERNANCE-LAYER-FILE1-v1.0`

## 核心愿景

将龍魂系统的哲学原则转化为可执行的计算逻辑。

**核心命题**: “人永远是1”- Every human maintains sovereignty through measurable, mathematical proof.

## 已实装系统

### 1️⃣ 三才主权指数系统 (Three-Talent Sovereignty Index)

**文件**: `sovereignty_index.py` (410 行)

**原理**:
```
SI = 0.34·天(规则遵守) + 0.33·地(数据完整) + 0.33·人(创作权威)

SI ≥ 0.34 → 🟢 主权激活 (允许: 认知重建、决策制定、状态恢复)
SI < 0.34 → 🔴 主权失锚 (锁定: 只读存档、禁止决策)
```

**核心概念**:
- **天 (Tian/Heaven)**: Rule compliance & protocol adherence (规则遵守程度)
- **地 (Di/Earth)**: Resource control & data integrity (数据完整性和控制力)
- **人 (Ren/Human)**: Creator authority & decision rights (创作权威和决策权)

**功能**:
- ✅ 实时追踪三才评分
- ✅ 违规事件记录 (append-only JSONL)
- ✅ 可恢复/不可恢复违规区分
- ✅ 主权快照 (时间序列追踪)
- ✅ 访问权限矩阵 (谁能做什么)
- ✅ 等级判定 (完全主权 / 激活 / 削弱 / 失锚)

**使用例**:
```python
from cnsh_core.governance.sovereignty_index import get_sovereignty_index

si = get_sovereignty_index("UID9622")

# 记录违规
si.deduct_tian(
    reason="Attempted to bypass safety lock",
    amount=0.15,
    evidence="Security log: L7_FUSE_TRIGGER",
    recoverable=False
)

# 检查是否允许认知重建
if si.can_reconstruct_cognitive_state():
    restore_memory()
else:
    print(f"主权失锚: {si.lock_status()}")

# 取快照
snapshot = si.take_snapshot()
```

---

### 2️⃣ F1-F7七因子验证系统 (Seven-Factor Verification Framework)

**文件**: `f1_through_f7_verifier.py` (620 行)

**原理**: 行为密码学 (Behavioral Cryptography)

不是问“这是AI生成的吗？”
而是问“谁原创它，通过哪些规则，哪些人格，什么决策，修订过哪里，什么审计证据？”

**七个因子及权重**:
```
F1: 身份DNA验证 (Identity DNA) - 25%
    └─ UID + GPG指纹 + CONFIRM码 + DNA标记

F2: 时间锚定 (Temporal Anchor) - 15%
    └─ ISO8601 + 时辰(子丑寅卯) + 数字根(1-9)

F3: 规则追踪 (Rule Trace) - 15%
    └─ 应用的规则ID列表 + 规则链哈希 + 签名验证

F4: 人格路由 (Persona Routing) - 12%
    └─ 主要路由节点 + 权重分配 + 无虚伪词汇检测

F5: 保护词汇 (Protected Vocabulary) - 12%
    └─ 主权词汇正确使用 + 繁体保护 + 语义完整

F6: 风格向量 (Style Vector) - 11%
    └─ 写作风格一致性 (余弦相似度)

F7: 错误日志 (Mistake Ledger) - 10%
    └─ 持续错误历史 + 恢复率
```

**置信度计算**:
```
conf = ∏ s_i^{w_i}  (乘积形式·任何因子=0→整体=0)

硬失败规则: 任何因子 F_i = 0 → conf = 0 (不可救)
接纳阈值:
  - τ = 0.85 (预设·普通)
  - τ = 0.95 (高安全·敏感操作)

结果分级:
  conf = 0.00      → 🔴 硬失败
  conf < 0.70      → 🔴 不接纳
  0.70-0.85        → 🟡 需审核
  0.85-0.95        → 🟢 接纳
  conf ≥ 0.95      → 🟢 高信任
```

**功能**:
- ✅ 七因子独立验证
- ✅ 置信度计算 (乘积模型·硬失败机制)
- ✅ 详细分析报告
- ✅ 阈值设定 (灵活调整)

**使用例**:
```python
from cnsh_core.governance.f1_through_f7_verifier import SevenFactorVerifier, F1IdentityVerification, ...

verifier = SevenFactorVerifier()

# 构建七个因子
f1 = F1IdentityVerification(
    uid="9622",
    gpg_fingerprint="A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    gpg_prefix_marker="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    identity_dna="#龍芯⚡️2026-06-03-CREATOR-UID9622-v1.0",
    creation_timestamp="2025-05-20T10:00:00Z"
)

f2 = F2TemporalAnchor(...)
# ... F3-F7 ...

# 验证
result = verifier.verify(f1, f2, f3, f4, f5, f6, f7, threshold=0.85)

if result['passed']:
    print(f"✅ 通过验证 (conf={result['confidence']:.4f})")
else:
    print(f"❌ 未通过 (conf={result['confidence']:.4f})")
    if result['hard_failures']:
        print(f"硬失败: {result['hard_failures']}")
```

---

## 架构完整性检查

### 已实装 ✅

| 功能 | 状态 | 文件 | 说明 |
|------|------|------|------|
| **三才主权指数** | ✅ | `sovereignty_index.py` | 完整实装 |
| **F1-F7验证** | ✅ | `f1_through_f7_verifier.py` | 完整实装 |
| **三色审计** | ✅ | (scripts/) | 已有实装 |
| **DNA追溯** | ✅ | (scripts/) | 已有实装 |
| **生态闭环** | ✅ | (scripts/) | 已有实装 |

### 待实装 (Next Priority) 🔄

| 功能 | 优先级 | 目的 |
|------|--------|------|
| **认知DNA粒子** | 🔴 HIGH | 完整的记忆/决策压缩恢复 |
| **时间锚定系统** | 🔴 HIGH | 时辰/数字根/农历路由 |
| **人格路由系统** | 🔴 HIGH | 加权决策路由 + 虚伪词汇阻挡 |
| **五行路由逻辑** | 🟡 MEDIUM | 金木水火土决策树 |
| **保护词汇验证** | 🟡 MEDIUM | 主权词汇语义锁定 |
| **边界执行系统** | 🟡 MEDIUM | L0/L1/L2边界 + L7熔断 |
| **证据日志系统** | 🟡 MEDIUM | 完整append-only + DNA链接 |
| **执行回执系统** | 🟠 LOW | 标准输出格式 + 时间评级 |

---

## 与其他系统的集成

### 与 `fulltext_compress.py` 的关系

**目前**: 简单的骨架提取 (problem/solution/key_points)

**改进方向**: 集成认知DNA粒子
```python
# 未来的实装
cognitive_particle = CognitiveDNAParticle(
    compressed_content="...",
    sovereign_index=si,  # 三才指数
    emotion_fold={...},  # 情绪折叠
    verification_factors={...},  # F1-F7验证
    decision_replay_basis="...",  # 决策回放
    dna_trace="#龍芯⚡️..."
)
```

### 与 `heaven_nonkill_audit.py` 的关系

**目前**: P0硬锁的三色判定

**改进方向**: 集成F1-F7验证
```python
# 在P0审计前先做F1-F7验证
f1_f7_result = verifier.verify(...)

if f1_f7_result['confidence'] < 0.7:
    return AuditResult(color=RiskColor.RED, ...)

# 然后再做P0规则审计
heaven_audit = HeavenNonKillAudit().check(...)
```

### 与 `longhun_integrated_system.py` 的关系

**目前**: 生态闭环的一次转译锁定

**改进方向**: 集成主权指数控制访问
```python
# 检查生态访问权限
si = get_sovereignty_index(user_uid)

if si.can_make_decisions():
    allow_code_translation()
else:
    archive_only_mode()
```

---

## 理论基础

### “人永远是1”的实现

**原则**: 每个人（UID）是一个完整的主权单位

**实装层次**:
1. **身份层**: 唯一的UID + GPG签名 (F1)
2. **时间层**: 不可重复的时刻点 (F2)
3. **决策层**: 规则链 + 人格权重 (F3/F4)
4. **语言层**: 主权词汇保护 (F5)
5. **风格层**: 写作风格识别 (F6)
6. **记忆层**: 错误历史连贯性 (F7)

### “三才”在代码中的体现

| 维度 | 代码体现 | 违规现象 |
|------|---------|--------|
| **天** | 规则遵守评分 | 违反P0协议、绕过安全锁 |
| **地** | 数据完整性评分 | 数据被篡改、源污染 |
| **人** | 创作权威评分 | 被冒认、决策权侵犯 |

主权激活 (SI ≥ 0.34) 的含义:
- ✅ 可以重建个人的认知状态
- ✅ 可以做出新的决策
- ✅ 可以修复自己的数据

### “行为密码学”的核心

**传统密码学**: 是否有密钥?
```
key ✅ → 放行
key ❌ → 拒绝
```

**行为密码学**: 谁、通过什么、留下了什么证据?
```
f1_verify() ✅  身份确认
f2_verify() ✅  时间一致
f3_verify() ✅  规则可追踪
f4_verify() ✅  人格路由合法
f5_verify() ✅  语言完整
f6_verify() ✅  风格一致
f7_verify() ✅  错误历史连贯

⇒ conf = 0.93 ✅ 信任
```

---

## 测试状态

### ✅ 已测试 (2026-06-03)

- [x] 三才主权指数: 初始化、违规记录、恢复、快照、报告生成
- [x] F1-F7验证: 七个因子验证、置信度计算、硬失败检测、报告生成

**测试命令**:
```bash
cd ~/longhun-system
python3 cnsh-core/governance/sovereignty_index.py
python3 cnsh-core/governance/f1_through_f7_verifier.py
```

**预期输出**:
- 三才系统: 违规记录、SI计算、主权等级判定
- F1-F7系统: 七个因子分数、置信度、验证结果分级

---

## 下一步行动

### 优先级 🔴 (高)

1. **认知DNA粒子系统** - 完整的记忆/决策状态压缩与恢复
2. **人格路由系统** - 加权决策节点 + 虚伪词汇阻挡

### 优先级 🟡 (中)

3. **时间锚定系统** - 时辰、数字根、农历路由
4. **五行路由逻辑** - 决策树映射

### 优先级 🟠 (低)

5. **边界执行系统** - L0/L1/L2边界 + L7熔断机制
6. **其他支撑系统**

---

**DNA**: `#龍芯⚡️2026-06-03-GOVERNANCE-LAYER-v1.0`
**责任**: UID9622·不免责·永久有效
**理论指导**: 曾仕强老师 · Steve Jobs · Open Source
