# 龍魂流场决策核 v4.1

**CNSH Flow Decision Core v4.1 - 人格协作 × IPA × DNA重铸增量包**

---

## 📋 概述

这是龍魂系统的核心决策引擎，集成了：
- **人格协作**：10道闸×主驻×辅助×硬闸×回执（6条铁律）
- **IPA路由**：11个节点全链可追溯（5条铁律）
- **DNA追溯**：多标签+四源数字根+父子链+销毁封存证明（6条铁律）

---

## 🏗️ 文件结构

```
cnsh/flow_decision/
├── __init__.py                      # 包入口
├── schemas.py                       # 38字段 FlowDecisionNode 完整定义
├── digital_root.py                  # 四源数字根计算（IPA-FLOW-GATE-DR）
├── ipa_route_registry.py            # 11个IPA节点注册表
├── persona_collaboration.py         # 人格协作框架（6条铁律）
├── dna_chain_tracer.py              # DNA父子链追踪（销毁/封存证明）
├── cnsh_flow_decision_core.py       # 主入口（10道闸流程）
├── examples.py                      # 4个完整示例（normal/burn/sealed/L0）
├── README.md                        # 本文件
├── tests/
│   ├── test_persona_collaboration.py
│   ├── test_ipa_chain.py
│   ├── test_dna_tracer.py
│   └── test_flow_decision_core.py
```

---

## 🚀 快速开始

### 安装

```bash
cd ~/longhun-system
# 无外部依赖，仅需Python 3.8+
```

### 基本用法

```python
from cnsh.flow_decision import quick_process, LevelEnum, VisibilityEnum

# 普通处理
tags = {
    "title": "系统日志",
    "dna": "#龍芯⚡️2026-05-03-TEST-v4.1",
}

node = quick_process("处理内容", tags)
print(f"最终状态: {node.result_status.value}")
print(f"分拣桶: {node.route.bucket.value}")
```

### 四个完整示例

```bash
cd cnsh/flow_decision
python examples.py
```

输出内容包含：
- ✅ 示例1：normal (普通内容，🟢 ENTER)
- ✅ 示例2：burn (临时数据，📝 销毁证明)
- ✅ 示例3：sealed (隐私数据，🔒 三签封存)
- ✅ 示例4：L0 (永恒规则，🟡 待确认)

---

## 🔧 10道闸流程

| # | 闸名 | 主驻人格 | 辅助人格 | 功能 | 硬闸 |
|---|------|---------|---------|------|------|
| 1 | 签章闸 | P05 | P72 | confirm/seal验证 | 1-2 |
| 2 | 隐私闸 | P03 | P05,P72 | 隐私等级读取 | 3,10 |
| 3 | 数字根闸 | P06 | — | 四源dr计算 | — |
| 3.5 | 五行映射 | P06 | — | dr→五行 | — |
| 4 | 三色闸 | P05 | — | 审计规则判定 | 7-8 |
| 5 | 三才闸 | P00 | P01 | 权重校验 | 6,9 |
| 6 | 生克闸 | P01 | — | 与parent五行关系 | — |
| 7 | 九宫派位 | P13 | P14 | 按trace/action派宫 | — |
| 8 | 沙盒分拣 | P03 | P15 | 按颜色入桶 | — |
| 9 | 父子链落档 | P15 | P05 | DNA写入+回执 | 4-5 |

---

## 🧬 27条硬闸规则

### v4.1原版10条（主流程检查）

1. 🔴 confirm_code缺失 → 熔断（P05）
2. 🔴 eternal_seal被改 → 熔断（P05+P72）
3. 🔴 privacy:sealed → 不读正文，只hash，三签缺一不可（P03+P05+P72）
4. 🔴 privacy:burn → 可临时读，生成destroy_proof（P03+P05）
5. 🔴 trace:no_external + action:export → 禁止外发（P72）
6. 🔴 human < 0.34 → 自动提升至0.34+🟡（P00）
7. 🔴 dr=3/9 + auto_execute=true → 禁止自动执行（P05+P06）
8. 🟡 dr=6 → 待审（P05）
9. 🟢 L0永恒 → need_uid_confirm=true（P00+老大）
10. 🔴 token/key/secret命中 → 强制sealed（P72自动）

### 人格协作6条（§1.1）

1. 一闸一主
2. 熔断独立（P05+P72）
3. L0必须文心+老大双签
4. sealed必须三签
5. 路由权姜子牙独占
6. 写档权乔前辈独占

### IPA 5条（§2.2）

1. 任何节点回执缺失 → 熔断
2. 熔断节点禁止外发
3. 节点超时500ms → 待审
4. 全链通过 → 自动写入草日志
5. IPA节点main_persona与花名册不一致 → 拒绝

### DNA 6条（§3.6）

1. confirm_code缺失 → 无效，熔断
2. eternal_seal被改 → 无效，熔断
3. parent_dna引用不存在 → 链断裂，熔断
4. child_dna重复 → 待审
5. 完整链+全字段 → 通过
6. sealed/burn节点raw_body=true → sealed优先，熔断

---

## 🎯 IPA 11个节点

| # | 节点ID | 地址 | 主人格 | 作用 |
|---|--------|------|--------|------|
| 0 | IPA-FLOW-DECISION-CORE-v4.1 | /flow/core | P00 | 核心入口 |
| 1 | IPA-FLOW-GATE-SIGN | /flow/gate/sign | P05 | 签章验证 |
| 2 | IPA-FLOW-GATE-PRIVACY | /flow/gate/privacy | P03 | 隐私读取 |
| 3 | IPA-FLOW-GATE-DR | /flow/gate/dr | P06 | 数字根计算 |
| 3.5 | IPA-FLOW-WUXING-MAP | /flow/wuxing | P06 | 五行映射 |
| 4 | IPA-FLOW-GATE-AUDIT | /flow/gate/audit | P05 | 三色判定 |
| 5 | IPA-FLOW-GATE-SANCAI | /flow/gate/sancai | P00 | 三才验证 |
| 6 | IPA-FLOW-GATE-SHENGKE | /flow/gate/shengke | P01 | 生克关系 |
| 7 | IPA-FLOW-PALACE-ROUTER | /flow/palace | P13 | 九宫派位 |
| 8 | IPA-FLOW-SANDBOX-BUCKET | /flow/sandbox | P03 | 沙盒分拣 |
| 末 | IPA-FLOW-DNA-CHAIN | /flow/dna | P15 | 父子链落档 |

---

## 📊 FlowDecisionNode 38字段

### 核心身份（5）
- title, node_id, confirm_code, gpg, dna

### 链接（2）
- parent_dna, child_dna

### 隐私与追溯（2）
- privacy (PrivacyConfig), dna_tags (DNATagPolicy)

### 数学层（3）
- math (MathConfig), digital_root (DigitalRootConfig)

### 审计层（2）
- audit (AuditConfig), gate_receipts (List[GateReceipt])

### 路由与派位（2）
- route (RouteConfig), ipa_chain (List[IPAReceipt])

### 存储配置（1）
- storage (StorageConfig)

### 结果与操作（3）
- result_status, result_operator, result_timestamp

### 内容与元数据（4）
- raw_input, raw_body, content_hash, tags

### 备注与回溯（2）
- remarks, trace_info

---

## ✅ 验收清单

- [x] 人格协作：10道闸全部有主驻+辅助+硬闸+回执格式
- [x] IPA：11个节点全部注册+回执统一+全链可追溯
- [x] DNA：多标签+四源数字根+父子链+销毁封存证明落地
- [x] 主语法核：中文CNSH能跑（已转Python）
- [x] 字段表：FlowDecisionNode完整38字段无遗漏
- [x] 硬闸：27条全部有人格背书+IPA回执+DNA签章

---

## 🧪 测试

```bash
pytest tests/ -v
```

每个模块都有独立的测试：
- `test_persona_collaboration.py`: 6条人格铁律
- `test_ipa_chain.py`: 11节点全链
- `test_dna_tracer.py`: 父子链+四源dr
- `test_flow_decision_core.py`: 端到端10道闸

---

## 📝 使用示例

### 示例1：普通处理

```python
from cnsh.flow_decision import quick_process

node = quick_process(
    "系统日常日志",
    {"title": "daily_log", "level": "L3_DAILY"}
)
# 结果: 🟢 ENTER
```

### 示例2：敏感数据销毁

```python
node = quick_process(
    "临时token: sk_live_xxx",
    {
        "title": "temp_token",
        "trace_mode": "LOCAL_ONLY",
        "level": "L5_TEMP"
    }
)
# 结果: 📝 内部消化 + burn_proof
```

### 示例3：隐私信息三签

```python
node = quick_process(
    "用户个人信息...",
    {
        "title": "user_private",
        "visibility": "PRIVATE",
        "trace_mode": "NO_EXTERNAL",
        "p0_touched": True
    }
)
# 结果: 🔒 sealed (P03+P05+P72三签)
```

### 示例4：L0永恒级规则

```python
node = quick_process(
    "铁律更新...",
    {
        "title": "L0_rule_update",
        "level": "L0_ETERNAL",
        "p0_touched": True
    }
)
# 结果: 🟡 待确认 (需要P00+UID9622双签)
```

---

## 🔐 安全特性

✅ **签章验证**：CONFIRM+GPG双验证
✅ **隐私保护**：sealed三签+burn销毁证明
✅ **人格熔断**：P05+P72独立熔断权
✅ **DNA可追溯**：父子链不可断
✅ **自动检测**：token/key等敏感词自动upgraded

---

## 📚 参考

- **DNA体系**：多标签+四源数字根+父子链
- **IPA路由**：11个节点，统一回执格式
- **人格协作**：10道闸，6条铁律
- **硬闸规则**：27条全覆盖

---

**DNA:** #龍芯⚡️2026-05-03-CNSH-FLOW-DECISION-CORE-v4.1-README
**CONFIRM:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**责任:** UID9622·不免责

---

© 2026 龍魂系统 | 数据主权归于人民
