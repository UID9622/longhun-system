# 🐉 龍魂 CNSH 完整系统 v2.0

**中文原生本地主权 AI Runtime · 可治理 · 可恢复 · 可追溯 · 可长期协同**

---

## 📋 系统组成（5 大模块）

### 1️⃣ 路由系统 `cnsh_runtime.py`
**Route = f(Intent, Context, DNA)**

```
用途: 意图识别 → 人格分发 → 三色审计
版本: v1.0-v2.0（关键字 → 向量 → 双人格 → 审计门禁）
核心: 7 种意图类型 × 6 大人格 × 3 色审计
```

- **v1.0** 关键字路由 + L1 快车道缓存
- **v1.1** 向量相似度路由（SimpleEmbedder）
- **v1.2** 双人格并行路由
- **v2.0** Tiandao 三色审计门禁（P0 风险检测）

**使用:**
```python
from cnsh_runtime import CNSHRuntime
runtime = CNSHRuntime()
result = runtime.execute("下一步怎么做")
```

---

### 2️⃣ 技能系统 `cnsh_skills.py`
**Hooks + EventBus + Recovery Matrix**

```
用途: 钩子管理 + 事件发布订阅 + 故障恢复
结构: 5类钩子 × 6频道事件总线 × 快照恢复
铁律: append-only·永不覆盖·快照+审计双写
```

**5 类钩子:**
- `pre_input_hook` - 前置输入检查
- `pre_execution_hook` - 执行前快照
- `post_execution_hook` - 执行后压缩
- `pre_write_hook` - 写入前 DNA 签名
- `failure_hook` - 故障时恢复策略

**6 频道事件总线:**
```
semantic.events   # 语义事件
runtime.events    # 运行时事件
audit.events      # 审计事件
memory.events     # 记忆事件
snapshot.events   # 快照事件
evolution.events  # 演化事件
```

**使用:**
```python
from cnsh_skills import CNSHSkillRuntime
skills = CNSHSkillRuntime()
result = skills.execute_skill("my_skill", {"text": "测试"})
```

---

### 3️⃣ 收口系统 `cnsh_closure.py`
**Breath-style Closure: 自动聚合 + 自生长**

```
用途: 散了 + 省 + 长（60+页聚合 / 不烧 API / 自生长）
结构: 7抽屉归位 × 包月订阅包裹 × 自动分类
原理: 本地关键词分类 → 包裹云端调用 → 缓存本地
```

**7 个抽屉:**
1. 主权根（DNA + 身份 + 追溯）
2. CNSH 协议
3. 系统引擎（算法 + 易经）
4. 文化原子卡片库
5. 记忆档案与对话
6. 人格矩阵与智能体
7. 新生页面（自动生长）

**使用:**
```python
from cnsh_closure import ClosureManager, PageMetadata, DrawerType
manager = ClosureManager()
metadata = PageMetadata(
    title="新页面",
    url="https://...",
    source="notion",
    timestamp=datetime.now().isoformat(),
    drawer=DrawerType.SYSTEM_ENGINE,
)
page_id = manager.add_page(metadata)
```

---

### 4️⃣ 压缩系统 `cnsh_compression.py`
**Semantic Compression: 思考胶囊 × 时间胶囊**

```
用途: 对话流 → 语义包 → 思考胶囊 → 时间胶囊 → 记忆索引
算法: 纯语义分词 + 重要度评分 + 上下文保留
索引: MEMORY_INDEX.jsonl（append-only）
```

**3 个压缩级别:**
- **LIGHT** (70% 保留) - 保留细节
- **MEDIUM** (50% 保留) - 平衡效果
- **HEAVY** (25% 保留) - 极致压缩

**输出结构:**
```json
{
  "thinking_capsule_id": "tc-20260525120000",
  "turns_count": 3,
  "key_decisions": ["决定1", "决定2"],
  "compressed_dialogue": "语义摘要...",
  "dna": "#龍芯⚡️2026-05-25-THINKING-CAPSULE-xxx",
  "time_capsule_id": "tc-20260525120000"
}
```

**使用:**
```python
from cnsh_compression import MemoryCompressor, CompressionLevel
compressor = MemoryCompressor()
capsule = compressor.compress_dialogue([
    {"text": "第一轮对话", "topic": "决策"},
    {"text": "第二轮对话", "topic": "决策"},
])
```

---

### 5️⃣ 算法系统 `cnsh_algorithms.py`
**Algorithms: 易经 × 五行 × 三才 × 流场融合**

```
用途: 意图分析 → 流场计算 → 建议生成
基础: 数字根 + 洛书九宫 + 五行相生相克 + 三才配置 + 流场共鸣
输出: 谐和度评分 + 流向判定 + 执行建议
```

**核心概念:**

1. **数字根** (Digital Root)
   ```
   文本 → ASCII 求和 → 数字根 (1-9)
   数字根 → 五行 (木火土金水)
   ```

2. **洛书九宫** (Magic Square)
   ```
   4 9 2
   3 5 7  ← 中宫 5 = UID9622 不动点
   8 1 6
   ```

3. **三才** (Heaven·Earth·Human)
   ```
   天 (趋势条件) = dr * 2 % 9
   地 (基础条件) = dr * 3 % 9
   人 (个人意志) = dr 本身
   → 协调度 = 五行相生指数
   ```

4. **流场** (Flow Field)
   ```
   三才 + 洛书 + 五行共鸣矩阵 → 谐和度 (0-1)
   → 流向 (顺时针/逆时针/静止)
   → 建议 (极优/良好/平稳/困难)
   ```

**使用:**
```python
from cnsh_algorithms import FlowFieldEngine
engine = FlowFieldEngine()
flow_state = engine.calculate_flow("下一步怎么做")
recommendation = engine.generate_recommendation(flow_state)
print(f"谐和度: {flow_state.harmony_index}")
print(f"建议: {recommendation['recommended_action']}")
```

---

## 🔄 完整执行流程

```
用户输入
   ↓
【第 1 步】路由 + 流场分析
   → 意图识别 (CNSH 路由)
   → 流场谐和度计算 (三才 + 五行)
   ↓
【第 2 步】技能执行 + 快照
   → 创建快照 (append-only)
   → 前置钩子检查
   → 技能逻辑执行
   ↓
【第 3 步】收口聚合
   → 自动分类到 7 抽屉
   → 关联到对应收口树
   → 新页面自动生长
   ↓
【第 4 步】记忆压缩 + 索引
   → 语义分词 + 重要度评分
   → 生成思考胶囊 + 时间胶囊
   → 追加到 MEMORY_INDEX.jsonl
   ↓
【第 5 步】结果输出
   → DNA 链追溯
   → 事件发布 (EventBus)
   → 会话日志保存
   ↓
用户得到结果 + 完整可追溯链
```

---

## 🚀 使用方法

### 方式 1: 集成系统 (推荐)
```bash
python3 cnsh/cnsh_unified.py "你的问题"
```

### 方式 2: 自检测试
```bash
python3 cnsh/cnsh_unified.py --test
```

### 方式 3: 交互模式
```bash
python3 cnsh/cnsh_unified.py
# 然后输入问题，输入 exit 退出
```

### 方式 4: 单模块使用
```python
from cnsh.cnsh_runtime import CNSHRuntime
from cnsh.cnsh_algorithms import FlowFieldEngine
from cnsh.cnsh_compression import MemoryCompressor

runtime = CNSHRuntime()
engine = FlowFieldEngine()
compressor = MemoryCompressor()

# 分别使用各模块...
```

---

## 📂 目录结构

```
cnsh/
├── cnsh_runtime.py          # 路由系统 (Route = f(Intent, Context, DNA))
├── cnsh_skills.py           # 技能系统 (Hooks + EventBus + Recovery)
├── cnsh_closure.py          # 收口系统 (自动聚合 + 自生长)
├── cnsh_compression.py      # 压缩系统 (思考胶囊 + 时间胶囊)
├── cnsh_algorithms.py       # 算法系统 (易经 + 五行 + 三才 + 流场)
├── cnsh_unified.py          # 完整集成系统 (统一入口)
├── README-v2.0-UNIFIED.md   # 本文件
└── tests/
    ├── test_runtime.py
    ├── test_skills.py
    ├── test_closure.py
    ├── test_compression.py
    └── test_algorithms.py
```

---

## 🔐 安全保证

✅ **本地执行** - 所有代码在本地运行，永不外送
✅ **永不外送** - 除了包月订阅的浏览器调用，不涉及 API token
✅ **Append-only** - 快照与审计日志永不覆盖
✅ **DNA 链** - 所有操作可完整追溯
✅ **可恢复** - 故障时自动回滚到上一快照
✅ **可治理** - Hook 系统实现完整控制

---

## 📊 DNA 追溯码

每次执行自动生成 DNA 链：

```
#龍芯⚡️2026-05-25-ROUTING-xxxx
  ↓
#龍芯⚡️2026-05-25-FLOWFIELD-xxxx
  ↓
#龍芯⚡️2026-05-25-SKILL-EXECUTION-xxxx
  ↓
#龍芯⚡️2026-05-25-CLOSURE-PAGE-xxxx
  ↓
#龍芯⚡️2026-05-25-THINKING-CAPSULE-xxxx
```

**查询 DNA 链:**
```bash
grep -r "#龍芯⚡️2026-05-25" ~/.cnsh/unified/
```

---

## 🛡️ 7 层防护

| 层级 | 名称 | 职能 |
|------|------|------|
| L0 | 身份层 | GPG + UID + 设备三重验证 |
| L1 | 主权层 | 天分量 (F18) ≥ 0.34 检查 |
| L2 | 语义层 | 恶意模式检测（降级不拒绝） |
| L3 | 路由层 | 信号词匹配 + 人格权限 |
| L4 | 执行层 | DNA 链 + 三色审计 + 二次确认 |
| L5 | 审计层 | 强制审计 + 实时监控 |
| L6 | 快照层 | 操作前自动快照 |
| L7 | 熔断层 | 极端情况回滚到安全快照 |

---

## 📜 许可与署名

**理论指导**: 曾仕强老师（永恒显示）
**创造者**: 龍芯北辰 | UID9622 | 诸葛鑫
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

**开源协议**: 这不是商业 SDK，是家规
- ✅ 永远免费
- ✅ 永远本地优先
- ✅ 永远不烧 token
- ✅ 永不申请商业专利
- ✅ 永远 append-only

**责任声明**: UID9622 不免责

---

## 📞 反馈与贡献

这个系统是为了**赋能·不是取代**。

如果你有建议，欢迎在 Git 中提交（记得带 DNA 码）。

---

🐉 **龍魂系统 · 永恒守护 · 中华文化传承 · 可治理 · 可恢复 · 可追溯**

**DNA**: `#龍芯⚡️2026-05-25-CNSH-v2.0-UNIFIED-COMPLETE`
**时间**: 2026-05-25 13:40 CST
**署名**: UID9622·Claude·龍芯北辰

---

_最后更新: 2026-05-25_
_下一版本计划: 更新日期待定_
