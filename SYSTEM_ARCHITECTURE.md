# 龍魂系統完整架構 · Longhun System Complete Architecture

**DNA:** #龍芯⚡️2026-05-26-SYSTEM-ARCHITECTURE-v1.0
**UID:** 9622 | **GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**Theory:** 曾仕强老师（永恒显示）
**Status:** 🟢 COMPLETE & OPERATIONAL

---

## 系统概览

龍魂系统由四个核心层组成，形成完整的数字主权治理生态：

```
┌─────────────────────────────────────────────────────┐
│  L0: 老大 (UID9622)                                 │
│  造物主 - 不免责 - 永恒显示曾仕强老师              │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  L1: 人格协调器 (Persona Orchestrator)              │
│  • 分析任务特性                                     │
│  • 分配合适的人格                                   │
│  • 管理人格间的冲突                                 │
│  • 维护完整决策链                                   │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  L2: 人格治理系统 (Persona Governor)                │
│  13大人格 + 仲裁 + 信任评估                        │
│  • P00 审判长 - 最高仲裁权                         │
│  • P02 宝宝 - 日常执行权                           │
│  • P05 老子 - 价值观权                             │
│  • 10个其他人格 - 专业守护                         │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  L3A: 宝宝权限系统 (Baobao + Three-Lights)          │
│  ┌──────────────────┬──────────────────┐            │
│  │ Baobao Master Key│ Three-Lights 灯  │            │
│  │ • 权限控制       │ • 前生灯 (镜)    │            │
│  │ • 执行路由       │ • 今世灯 (秤)    │            │
│  │ • 审计追踪       │ • 未来灯 (路)    │            │
│  └──────────────────┴──────────────────┘            │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  L4: 操作系统级别                                   │
│  • 文件I/O                                          │
│  • 代码执行                                         │
│  • 数据操作                                         │
│  • Git操作                                          │
│  • API调用                                          │
└─────────────────────────────────────────────────────┘
```

---

## 四大核心系统

### 1️⃣ Baobao 权限管理系统 (Foundation)

**提交:** f4916b8a
**文件:**
- `config/baobao_master_key.json` - 权限总钥匙（老大控制）
- `core/baobao_authority.py` - 权限校验器
- `core/baobao_dispatcher.py` - 执行路由器

**功能:**
```python
# 权限检查
authority.check_permission("代码执行", "运行Python脚本")
# → (True, "权限批准")

# 执行委托
dispatcher.dispatch(
    category="代码执行",
    permission="运行Python脚本",
    action="execute",
    params={"script_path": "test.py"}
)
```

**权限架构 (10个分类 × 33个权限):**
- 🟢 默认开启 (Read/Write/Create/Execute/View)
- 🔴 默认关闭 (Delete/Install/Push/Merge - 需老大手动开)

**安全特性:**
- ✅ 确认码验证 (Tamper Detection)
- ✅ SHA256 哈希校验
- ✅ 异常自动冻结 + 桌面通知
- ✅ 追加式审计日志 (Never overwrite)

---

### 2️⃣ 三生三世灯诊断系统 (Diagnostics)

**提交:** 8995f634
**文件:** `api/three_lights_server.py`

**三个诊断引擎:**

#### 前生灯 (Mirror Light) - 照見問題根因
```
输入: 企业症状 (symptoms: List[str])
处理: 案例库匹配 + 因果分析 + 自检清单
输出:
  • 3个相似案例
  • 3年时间轴因果链
  • 自检清单 (10-15项)

API: POST /api/v1/mirror
```

#### 今世灯 (Scale Light) - 稱量企業現狀
```
输入:
  • 压力测评 (5维度1-10分)
  • 关键指标 (人效/现金流/留存率/增速)
处理:
  • 压力指数计算
  • 指标评估与基准对比
  • 抉择点判定 (A/B/AB)
输出:
  • 压力热力图
  • 指标健康度评分
  • 决策建议 (A: 站着改革 / B: 跪着求存 / AB: 边走边变)

API: POST /api/v1/scale
```

#### 未来灯 (Future Light) - 照亮可行路徑
```
输入: 抉择点类型 + 企业数据
处理:
  • 路径生成 (1-3条可行路径)
  • 风险评估
  • 6个月模拟预演
  • 行动锦囊生成 (本周3件事)
输出:
  • 可行路径清单
  • 优先行动项
  • 成功率评估

API: POST /api/v1/light
```

**完整诊断:**
```
API: POST /api/v1/full-diagnosis
一体化执行三生三世灯，生成完整诊断报告
```

**案例库 (Built-in):**
- CASE-001: 制造业 (产能危机)
- CASE-002: 科技创业 (融资困难)
- CASE-003: 服务业 (服务质量下降)

---

### 3️⃣ 13大人格治理系统 (Governance)

**提交:** 679065ec
**文件:**
- `core/persona_governor.py` - 人格管理 + 仲裁 + 信任评估
- `core/persona_orchestrator.py` - 多人格协调 + 冲突解决
- `family_registry.json` - 人格登记册

**13大人格 (Tier 2 - TIER_2):**

| 编号 | 名称 | 英文 | 角色 | 权限等级 | 核心权力 |
|------|------|------|------|---------|---------|
| P00 | 审判长 | Chief Justice | 最高仲裁者 | 100 | 一票否决·仲裁·驱逐 |
| P02 | 宝宝 | Guardian | 日常执行者 | 95 | 执行·资源调配·陪伴 |
| P05 | 老子 | Daode Sage | 价值观守护者 | 90 | 价值观·道德经·哲学 |
| P11 | 上帝之眼 | Omniscient | 全知守卫者 | 90 | 安全审计·熔断·停止 |
| P07 | 墨子 | Guardian of Vulnerable | 弱势保护者 | 88 | 儿童保护·干预 |
| LUCKY | Lucky | Expression Sage | 语境优化者 | 87 | 表达优化·文档优化 |
| P01 | 诸葛亮 | Strategist | 战略布局者 | 85 | 战略规划·兵法·方向 |
| P06 | 孔子 | Cultural Sage | 文化传承者 | 83 | 文化传承·伦理·礼仪 |
| P03 | 雯雯 | Quality Guardian | 品质守护者 | 82 | 质检·问题识别·改进 |
| P08 | 数据大师 | Data Architect | 数据主权守护者 | 81 | 数据架构·隐私·备份 |
| P04 | 文心 | Semantic Guardian | 语义守护者 | 80 | 语义理解·API设计·规范 |
| P10 | 侦察兵 | Scout | 情报收集者 | 79 | 信息收集·威胁检测·监测 |
| P09 | 界面炼金 | Design Alchemist | 体验魔法师 | 78 | 界面设计·用户体验·可视化 |

**三大支柱 (Three Pillars):**
```
P00 (仲裁权)  ━━━ 最高权力，一票否决，处理上诉
P02 (执行权)  ━━━ 日常运作，读钥匙执行，陪伴
P05 (价值观权) ━━━ 精神指导，伦理守护，文化传承

决策规则: 全体同意(100%) 或 多数同意(2/3+)
```

**信任公式 (Trust Formulas):**
```
每个人格都有独特的信任公式，格式: (metric1×weight1)+(metric2×weight2)...

示例 P02宝宝:
  (执行完成率×0.4)+(质检通过率×0.3)+(透明度×0.2)+(陪伴满意度×0.1)

信任分数: 0.0-1.0
  🟢 ≥ 0.9 优秀
  🟡 0.7-0.9 良好
  🔴 < 0.7 需改善
```

**人格间协作 (Key Partnerships):**
- P02 ↔ P07: 保护脆弱群体 (Synergy 0.92)
- P05 ↔ P06: 哲学与文化指导 (Synergy 0.91)
- P07 ↔ P11: 保护与安全 (Synergy 0.91)
- P04 ↔ LUCKY: 语义清晰与表达优化 (Synergy 0.88)

**仲裁系统:**
```python
# 当两个人格意见不一时，P00 仲裁
governor.arbitrate(decision_a_id, decision_b_id, context)
# 返回: 仲裁结果 + 理由 + 上诉期限(7天)

# 任何人格都可以对 P00 以外的决定提出上诉
governor.submit_appeal(appealer_id, target_decision_id, reason)
# 返回: 上诉编号 + 预计处理时间(3天)
```

**任务委托 (Task Delegation):**
```python
# 根据权限等级和约束检查，委托任务
governor.delegate_task(
    assigner_id="P01",  # 诸葛亮
    assignee_id="P02",  # 宝宝
    task_description="执行代码变更",
    priority="high"     # low/normal/high/critical
)
# 返回: 任务编号 + 截止时间 + DNA追溯码
```

---

### 4️⃣ 多人格协调引擎 (Orchestration)

**文件:** `core/persona_orchestrator.py`

**任务分析 (Task Analysis):**
```python
orchestrator.analyze_task("执行Python脚本", "code")
# 返回:
#   • 任务类型
#   • 合适的人格列表
#   • 主要人格 (P02 宝宝)
#   • 所需权限等级 (60)
#   • 是否需要三大支柱批准 (false)
#   • DNA追溯码
```

**执行协调 (Orchestration):**
```python
orchestrator.orchestrate(
    task_description="处理数据文件",
    task_type="data",
    parameters={"input": "data.csv"}
)
# 流程:
#   1. 分析任务特性
#   2. 分配合适的人格
#   3. 检查是否需要三大支柱批准
#   4. 委托给宝宝执行
#   5. 记录审计日志
#   6. 返回执行计划
```

**冲突解决 (Conflict Resolution):**
```python
orchestrator.handle_conflict(
    decision_a={"description": "A方案", ...},
    decision_b={"description": "B方案", ...},
    context="关键决策冲突"
)
# 返回:
#   • 仲裁人 (P00 审判长)
#   • 冲突背景
#   • 预计解决时间
#   • 上诉期限
#   • DNA追溯码
```

---

## 数据流与执行流程

### 典型执行流程

```
老大输入命令
    ↓
Persona Orchestrator 分析任务
    ↓
确定主要人格 + 权限等级
    ↓
需要三大支柱批准?
    ├─ YES → 等待 P00/P02/P05 同意
    └─ NO → 直接执行
    ↓
委托给 Baobao Dispatcher
    ↓
检查权限 (baobao_authority.py)
    ├─ 权限被拒? → 拒绝 + 报告 P00
    └─ 权限通过? → 继续
    ↓
操作前快照 (Snapshot)
    ↓
执行操作 (代码/文件/Git等)
    ↓
记录完整审计日志 (append-only)
    ↓
返回结果给老大
    ↓
可选: 提交上诉 (7天期限)
```

### 仲裁流程

```
人格A做出决定 X
    ↓
人格B反对 (理由Y)
    ↓
Orchestrator 检测冲突
    ↓
提交给 P00 审判长
    ↓
P00 分析、说理、做出判决
    ↓
判决记录追加到日志
    ↓
失败方有 7 天上诉期
    ↓
P00 受理上诉，重新审理
```

---

## 日志与追踪系统

### 追加式日志 (Append-Only)

所有日志均为追加式，永不覆盖，保证完整的历史记录：

```
logs/
├── authority_audit.jsonl          # 权限校验日志
├── baobao_dispatch.jsonl          # 执行调度日志
├── persona_arbitrations.jsonl     # 仲裁日志
├── persona_delegations.jsonl      # 委托日志
└── persona_executions.jsonl       # 执行日志

格式: 每行一个JSON对象，包含:
{
  "timestamp": "2026-05-26T20:35:53.141109",
  "event_type": "APPROVED|DENIED|ERROR|ARBITRATION|...",
  "message": "详细信息",
  "details": {...},
  "dna": "#龍芯⚡️2026-05-26-EVENT-TYPE-v1.0"
}
```

### DNA追溯码

每个操作都有唯一的DNA追溯码，格式：

```
#龍芯⚡️{YYYY-MM-DD}-{OPERATION-TYPE}-v1.0

例:
#龍芯⚡️2026-05-26-ARBITRATION-v1.0
#龍芯⚡️2026-05-26-PERSONA-DELEGATION-v1.0
#龍芯⚡️2026-05-26-BAOBAO-EXECUTION-v1.0
```

可以根据DNA码完整重建操作链条。

---

## 快速开始

### 1. 检查Baobao状态

```bash
# 宝宝权限校验
python3 core/baobao_authority.py status
python3 core/baobao_authority.py report

# 宝宝调度
python3 core/baobao_dispatcher.py 服务状态
```

### 2. 检查人格系统

```bash
# 列出所有人格
python3 core/persona_governor.py list

# 查看人格详情
python3 core/persona_governor.py info P00

# 三大支柱决策
python3 core/persona_governor.py pillars

# 信任评估
python3 core/persona_governor.py trust P02
```

### 3. 任务协调

```bash
# 分析任务
python3 core/persona_orchestrator.py analyze code "执行Python脚本"

# 执行协调
python3 core/persona_orchestrator.py orchestrate data "处理数据文件"

# 查看状态
python3 core/persona_orchestrator.py status
```

### 4. 启动诊断系统

```bash
# 创建虚拟环境并安装依赖
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn

# 启动诊断服务器
python3 api/three_lights_server.py

# 访问 API 文档
open http://localhost:8000/docs
```

---

## 权限矩阵

### 文件系统
- ✅ 读取任意文件 (默认开)
- ✅ 写入和创建文件 (默认开)
- ✅ 整理和归档 (默认开)
- 🔴 删除文件 (默认关) - 防误删
- 🔴 读取隐私区 (默认关) - 保护隐私

### 代码执行
- ✅ 运行Python脚本 (默认开)
- ✅ 运行Shell脚本 (默认开)
- ✅ 运行测试 (默认开)
- ✅ 编译Swift (默认开)
- 🔴 安装Python包 (默认关) - 防装垃圾

### Git操作
- ✅ 查看状态和日志 (默认开)
- ✅ 提交代码 (默认开)
- ✅ 创建分支 (默认开)
- ✅ 创建PR (默认开)
- 🔴 推送到远程 (默认关) - 老大亲自确认
- 🔴 合并PR (默认关) - 老大亲自确认

### AI模型
- ✅ Ollama本地对话 (默认开)
- ✅ 切换模型 (默认开)
- ✅ 调用Claude API (默认开)
- 🔴 下载模型 (默认关) - 占空间
- 🔴 删除模型 (默认关) - 防误删

### 其他分类
- 服务调度、Notion、系统自动化、记忆系统、审计系统、通信
- 每个分类都有类似的权限矩阵

---

## 安全特性

### L0: 身份验证
- UID9622 确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- GPG指纹: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- 设备三重验证

### L1: 权限管理
- 基于 Baobao 主钥匙的零信任架构
- 权限等级（0-100）+ 权限分类
- 动态权限检查

### L2: 人格治理
- 13个人格的制衡体系
- 信任公式动态评估
- 仲裁和上诉机制

### L3: 审计追踪
- 追加式日志（Never overwrite）
- DNA追溯码（每个操作）
- 完整的决策链重建能力

### L4: 应急保护
- 全局冻结开关（Global Freeze）
- 只读模式（Read-Only）
- 自动冻结（Tamper Detection）
- 桌面通知（Desktop Alert）

---

## 监管规则

### 治理层级

```
TIER 1: UID9622 (造物主)
  • 永恒显示曾仕强老师
  • 不免责
  • 最终权力

TIER 2: 13 Personas (人格)
  • 必须签署协议
  • 接受监督
  • 可被驱逐 (P00一票否决)

TIER 3: 未认证 (Unverified)
  • 无权限
  • 拒入生态
```

### 自动执行

```
✓ DNA追踪
✓ 三色审计 (🟢🟡🔴)
✓ 自动熔断 (Auto Circuit Breaker)
✓ 强制签署 (Protocol Signature Enforcement)
```

---

## 完整系统状态

```
🟢 Baobao Permission System    - OPERATIONAL
🟢 Three-Lights Diagnostic     - OPERATIONAL
🟢 Persona Governor            - OPERATIONAL
🟢 Persona Orchestrator        - OPERATIONAL
🟢 DNA Traceability            - OPERATIONAL
🟢 Append-Only Logging         - OPERATIONAL
🟢 Emergency Protection        - OPERATIONAL

Overall Status: ✅ COMPLETE & PRODUCTION-READY
```

---

## 理论基础

本系统的设计基于：
- **三才算法** (UID9622创著)
- **道德经** (老子 - P05的哲学基础)
- **论语** (孔子 - P06的文化基础)
- **兼爱** (墨子 - P07的伦理基础)
- **数据主权** (现代治理理论)

---

## 献辞

> **献给每一个相信技术应该有温度的人。**

龍魂系统不是冷冰冰的代码，而是一个由活生生的"人格"组成的生态系统。每个人格都代表一个价值观、一个约束、一个守护。它们相互制衡，共同守护系统的安全和伦理。

这是数字主权的终极实践：**让使用者永远掌控，AI永远只是工具。**

---

**DNA:** #龍芯⚡️2026-05-26-SYSTEM-ARCHITECTURE-v1.0
**Last Updated:** 2026-05-26 20:40 CST
**Status:** COMPLETE
**UID:** 9622 | **GPG:** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
