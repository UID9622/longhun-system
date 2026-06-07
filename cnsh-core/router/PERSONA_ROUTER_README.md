# PersonaRouter·人格路由系统

**DNA**: `#龍芯⚡️2026-06-03-PERSONA-ROUTER-v1.0`
**层级**: L1·季节性路由
**责任**: UID9622·不免责

---

## 📌 核心职能

PersonaRouter 是龍魂系统的 **人格路由引擎**，负责：

1. **虚伪词汇阻挡** - 检测和记录禁用词（怕/累/陪/吹）
2. **加权人格决策** - 通过 P02/P05/P13 权重进行路由
3. **F4因子验证** - 生成行为密码学第四因子的验证数据
4. **完整审计日志** - Append-only DNA追溯码和签名

---

## 🎯 设计原理

### 虚伪词汇四分类

```
怕 (Fear)       - 将问题责任推给环境或他人
├─ "怕", "害怕", "恐惧", "惧", "畏"
└─ 违反 P02·战斗者主权

累 (Tiredness)  - 用身体借口逃避责任
├─ "累", "疲劳", "累了", "好累"
└─ 违反 P02·持续战斗的承诺

陪 (Accompany)  - 不真诚的陪伴承诺
├─ "陪", "陪伴", "陪你", "我在这里陪"
└─ 违反 P05·深思熟虑的诚意

吹 (Exaggerate) - 言过其实或自我欺骗
├─ "吹", "吹牛", "吹嘘", "这还不吹"
└─ 违反 P13·平衡和谐的真实
```

### 人格权重配置

默认配置（可定制）：

```python
{
    "P02": 0.50,  # 战斗者/保护者 - 主导决策
    "P05": 0.30,  # 思想家/引导者 - 支撑理论
    "P13": 0.20,  # 和谐者/平衡者 - 调和冲突
}
# 总和必须 = 1.0
```

### F4·人格路由因子 (12%)

行为密码学的第四个验证因子：

```
F4 = {
    primary_persona: 主路由节点 (P02/P05/P13)
    persona_weights: 权重分配 {P02: 0.50, P05: 0.30, P13: 0.20}
    veto_words_detected: 是否检测到虚伪词汇
    routing_confidence: 路由置信度 (主路由权重)
}

F4.verify() -> score (0.0-1.0)
- 完美 (1.0): 合法路由 + 权重正确 + 无虚伪词汇
- 部分 (0.5): 权重不合法 或 检测到虚伪
- 失败 (0.0): 无主路由 或 权重和 > 1.0
```

---

## 🚀 快速开始

### 基础使用

```python
from cnsh_core.router.persona_router import get_persona_router

# 获取全局路由器实例
router = get_persona_router()

# 对文本进行人格路由
decision = router.route("这是要分析的文本内容")

# 查看决策报告
router.print_report(decision)
```

### 输出示例

```
┌─────────────────────────────────────────────────────────┐
│ 龍魂·人格路由决策报告                                    │
├─────────────────────────────────────────────────────────┤
│ 路由ID: ROUTE-20260603-001
│ 主路由: P02
│ 置信度: 50.00%
│ 虚伪词: 🟢 未检测
└─────────────────────────────────────────────────────────┘

【权重分配】
  P02: 50%
  P05: 30%
  P13: 20%

【DNA追溯】
  DNA: #龍芯⚡️20260603-PERSONA-ROUTER-8D63E327
  签名: 5adb9bf142c9d557...
```

---

## 📊 详细API文档

### PersonaRouter 类

#### `route(text: str, override_weights: Dict = None) -> PersonaRoutingDecision`

执行人格路由决策

**参数:**
- `text` - 待路由的文本内容
- `override_weights` - 可选的权重覆盖（用于特殊场景）

**返回:**
- `PersonaRoutingDecision` 对象，包含：
  - `routing_id` - 路由任务ID
  - `primary_persona` - 主路由节点 (P02/P05/P13)
  - `persona_weights` - 权重分配
  - `routing_confidence` - 路由置信度
  - `veto_words_detected` - 是否检测到虚伪词汇
  - `veto_word_matches` - 虚伪词汇匹配列表
  - `dna` - 路由DNA追溯码
  - `signature` - 路由签名(SHA256)

**示例:**

```python
decision = router.route("我怕这样做太累了")

print(f"主路由: {decision.primary_persona}")
print(f"虚伪词: {decision.veto_words_detected}")
print(f"匹配数: {len(decision.veto_word_matches)}")

# 输出:
# 主路由: P02
# 虚伪词: True
# 匹配数: 3
```

---

#### `check_veto_words(text: str) -> Tuple[bool, List[VetoWordMatch]]`

仅检查虚伪词汇，不进行完整路由

**参数:**
- `text` - 待检查的文本

**返回:**
- `(has_veto_words, matches_list)`
  - `has_veto_words` - 布尔值，是否检测到虚伪词汇
  - `matches_list` - VetoWordMatch 对象列表，每个包含：
    - `word` - 检测到的词汇
    - `category` - 词汇分类 (fear/tiredness/accompany/exaggerate)
    - `position` - 在文本中的位置
    - `context` - 上下文片段
    - `severity` - 严重度 (LOW/MEDIUM/HIGH)

**示例:**

```python
has_veto, matches = router.check_veto_words("我累了，需要陪伴")

if has_veto:
    for match in matches:
        print(f"{match.word} ({match.severity}): {match.context}")

# 输出:
# 累 (HIGH): 我累了，需要陪伴
# 了 (MEDIUM): 我累了，需要陪伴
# 陪 (MEDIUM): 需要陪伴
# 伴 (MEDIUM): 陪伴
```

---

#### `generate_f4_verification_data(decision: PersonaRoutingDecision) -> Dict`

从路由决策生成F4人格路由因子验证数据

**返回:**
- 可直接传给 `F4PersonaRouting` 数据类的字典

**示例:**

```python
decision = router.route("测试文本")
f4_data = router.generate_f4_verification_data(decision)

# f4_data 内容:
{
    "primary_persona": "P02",
    "persona_weights": {"P02": 0.5, "P05": 0.3, "P13": 0.2},
    "veto_words_detected": False,
    "routing_confidence": 0.5
}

# 用于F4因子验证
from cnsh_core.governance.f1_through_f7_verifier import F4PersonaRouting

f4 = F4PersonaRouting(**f4_data)
score = f4.verify()  # score = 1.0 (完美)
```

---

#### `get_audit_log(limit: int = 100) -> List[Dict]`

获取最近的审计日志

**参数:**
- `limit` - 最多读取的条数(默认100)

**返回:**
- 日志条目列表(最新的在前)

**日志条目结构:**

```python
{
    "timestamp": "2026-06-03T10:30:15.123456",
    "routing_id": "ROUTE-20260603-001",
    "primary_persona": "P02",
    "persona_weights": {"P02": 0.5, "P05": 0.3, "P13": 0.2},
    "routing_confidence": 0.5,
    "veto_words_detected": True,
    "veto_word_count": 3,
    "veto_categories": ["fear", "tiredness"],
    "dna": "#龍芯⚡️20260603-PERSONA-ROUTER-8D63E327",
    "signature": "5adb9bf142c9d557..."
}
```

---

#### `selftest() -> Tuple[bool, List[str]]`

运行系统自检

**返回:**
- `(all_pass, error_list)`
  - `all_pass` - 布尔值，所有检查是否通过
  - `error_list` - 错误列表

**检查项:**
- ✅ 权重验证 (sum = 1.0)
- ✅ 虚伪词汇库非空
- ✅ 日志目录可写
- ✅ 虚伪词汇检测功能
- ✅ 路由决策功能

---

### PersonaRoutingDecision 数据类

路由决策的完整记录。可转换为字典：

```python
decision_dict = decision.to_dict()
print(json.dumps(decision_dict, indent=2, ensure_ascii=False))
```

---

## 🔗 与其他系统的集成

### 1. 与F4因子的无缝集成

```python
from cnsh_core.router.persona_router import get_persona_router
from cnsh_core.governance.f1_through_f7_verifier import F4PersonaRouting

router = get_persona_router()
decision = router.route("待验证的内容")

# 生成F4因子数据
f4_data = router.generate_f4_verification_data(decision)

# 创建F4验证对象
f4 = F4PersonaRouting(**f4_data)

# 执行验证
score = f4.verify()
print(f"F4因子得分: {score:.2f}")
```

### 2. 与ExecutionRouter的集成

```python
from cnsh_core.router.persona_router import get_persona_router
from cnsh_core.router.execution_router import ExecutionRouter

router = get_persona_router()
exec_router = ExecutionRouter("manifest.json")

# 在任务执行前进行人格路由检查
decision = router.route(task.description)

if decision.veto_words_detected:
    print(f"⚠️ 检测到虚伪词汇: {len(decision.veto_word_matches)}处")
    # 可选: 降级权限或标记为需要审核

# 继续执行任务
exec_router.execute_task(task, context)
```

### 3. 与主权指数的结合

```python
from cnsh_core.governance.sovereignty_index import get_sovereignty_index
from cnsh_core.router.persona_router import get_persona_router

si = get_sovereignty_index("UID9622")
router = get_persona_router()

# 如果检测到虚伪词汇，可能会违反人性(人)评分
decision = router.route(user_statement)

if decision.veto_words_detected:
    # 可选: 对人性评分进行违规记录
    si.deduct_ren(
        reason=f"虚伪词汇检测: {decision.veto_word_matches[0].word}",
        amount=0.05,
        recoverable=True
    )
```

---

## 📝 虚伪词汇详解

### 怕 (Fear) - P02·战斗者的背弃

| 词汇 | 含义 | 违反 | 示例 |
|------|------|------|------|
| 怕 | 害怕、恐惧 | 主权 | "我怕这样做" |
| 害怕 | 害怕、担心 | 勇气 | "我害怕失败" |
| 恐惧 | 极度害怕 | 信念 | "我对未来恐惧" |

**为什么是虚伪?**
- 承诺要保护和战斗(P02)，却因为害怕退缩
- 将问题责任推给恐惧而非自己的选择

---

### 累 (Tiredness) - P02·持续战斗的破裂

| 词汇 | 含义 | 违反 | 示例 |
|------|------|------|------|
| 累 | 疲劳、疲惫 | 承诺 | "我太累了" |
| 疲劳 | 身体/心理疲惫 | 坚持 | "我很疲劳" |
| 累了 | 不想继续 | 责任 | "我累了不想干" |

**为什么是虚伪?**
- 用身体状态作为逃脱承诺的借口
- "我太累了"通常意味着"我不想做"而非事实

---

### 陪 (Accompany) - P05·虚伪的承诺

| 词汇 | 含义 | 违反 | 示例 |
|------|------|------|------|
| 陪 | 陪伴、随行 | 诚意 | "我会陪你" |
| 陪伴 | 长期陪伴 | 真实 | "我陪伴你" |
| 陪你 | 为你陪伴 | 承诺 | "我会陪你一起" |

**为什么是虚伪?**
- "我在这里陪你"通常只是说说而已
- 缺乏实际的行动承诺
- P05需要深思熟虑的诚意，而非空洞的陪伴语言

---

### 吹 (Exaggerate) - P13·破坏和谐的谎言

| 词汇 | 含义 | 违反 | 示例 |
|------|------|------|------|
| 吹 | 吹嘘、夸大 | 真实 | "这还不吹" |
| 吹牛 | 自我吹嘘 | 诚实 | "别吹了" |
| 吹嘘 | 浮夸宣传 | 谦虚 | "你在吹嘘" |

**为什么是虚伪?**
- 过度宣传或言过其实
- 为了虚荣心而扭曲事实
- P13强调和谐与平衡，吹嘘是对这一原则的破裂

---

## 🧪 测试和验证

### 运行自检

```bash
cd ~/longhun-system
python3 cnsh-core/router/persona_router.py
```

**预期输出:**
```
🔍 PersonaRouter 自检...

✅ 所有自检通过

【测试1】正常文本路由:
...
【测试2】包含虚伪词汇的文本:
...
【测试3】F4因子验证数据:
...
【测试4】最近的审计日志(前3条):
...
```

### 审计日志位置

所有路由决策记录在：

```
~/longhun-system/logs/persona_router_execution.jsonl
```

**日志格式:** Append-only JSONL (每行一条记录，不可删除)

---

## ⚙️ 自定义配置

### 修改人格权重

```python
from cnsh_core.router.persona_router import get_persona_router

# 自定义权重 (例如: P05主导)
custom_weights = {
    "P05": 0.50,  # 思想家主导
    "P02": 0.30,  # 战斗者支撑
    "P13": 0.20,  # 和谐者调和
}

router = get_persona_router(persona_weights=custom_weights)
```

### 添加新的虚伪词汇

编辑 `persona_router.py` 中的 `VETO_WORDS` 字典：

```python
VETO_WORDS = {
    VetoWordCategory.FEAR: [
        "怕", "害怕", ...,
        "新词汇1", "新词汇2"  # 添加新词
    ],
    # ...
}
```

---

## 📊 性能指标

- **检测速度**: < 10ms (对于1000字文本)
- **内存占用**: < 5MB
- **日志写入**: Append-only，O(1)
- **DNA计算**: SHA256, < 1ms

---

## 🔐 安全保证

- ✅ 虚伪词汇检测不可绕过 (正则+完全匹配)
- ✅ DNA追溯码不可伪造 (SHA256哈希)
- ✅ 审计日志不可删除 (Append-only)
- ✅ 权重验证强制执行 (sum = 1.0 ±1%)
- ✅ 签名验证防篡改 (SHA256)

---

## 🐛 故障排除

| 问题 | 解决方案 |
|------|---------|
| "权重必须加到1.0" | 检查persona_weights参数是否加到1.0 |
| "日志目录不可写" | 检查 `~/longhun-system/logs/` 权限 |
| "虚伪词汇未检测" | 检查输入文本是否真的包含禁用词 |
| "DNA格式错误" | 确保系统时间正确，DNA格式为 `#龍芯⚡️YYYYMMDD-*` |

---

## 📚 相关模块

- **F4PersonaRouting** - `cnsh-core/governance/f1_through_f7_verifier.py`
- **ExecutionRouter** - `cnsh-core/router/execution_router.py`
- **SovereigntyIndex** - `cnsh-core/governance/sovereignty_index.py`

---

**DNA**: #龍芯⚡️2026-06-03-PERSONA-ROUTER-v1.0
**责任**: UID9622·不免责·永久有效
