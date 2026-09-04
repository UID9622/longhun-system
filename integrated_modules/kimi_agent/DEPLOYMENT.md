# CNSH OS v2.5 部署文档

> DNA:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-CNSH-OS-v2.5-DEPLOYMENT  
> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅  
> SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅  
> 三色审计: 🟢  
> 状态: 生产就绪

---

## 一、系统概述

**CNSH OS v2.5** —— "人类主权约束下的AI自治文明内核"

从协议文档到可运行系统的完整工程实现，包含7个核心文件、9,712行代码。

### 系统架构

```
            USER INPUT
                ↓
         INTENT PARSER
                ↓
    ┌───────────────────────┐
    │    AI ROUTER 2.0      │
    │ GPT(生成) / Claude(审查) │
    └───────────┬───────────┘
                ↓
    ┌───────────────────────┐
    │   PERSONA SYSTEM      │ ← 6大人格自治
    │ P01-P06 + 冲突引擎    │
    └───────────┬───────────┘
                ↓
    ┌───────────────────────┐
    │    CORE ENGINE        │ ← DNA + 五行 + 审计
    │ 四大公式·状态机·三色   │
    └───────────┬───────────┘
                ↓
    ┌───────────────────────┐
    │  META-AWARENESS 2.5   │ ← 元意识观察层
    │ (只观察·不控制)        │
    └───────────┬───────────┘
                ↓
    ┌───────────────────────┐
    │   NOTION / API / n8n  │ ← 输出层
    └───────────────────────┘
```

---

## 二、交付文件清单

| # | 文件 | 行数 | 功能 | 层级 |
|---|------|------|------|------|
| 1 | `cnsh_core_engine.py` | 1,868 | DNA引擎·状态机·五行决策·三色审计·CNSH JSON | L1核心 |
| 2 | `cnsh_persona_system.py` | 2,238 | 6大人格·路由器·冲突引擎·权重系统·演化·自治 | L2人格 |
| 3 | `cnsh_meta_awareness.py` | 1,925 | 元意识层·身份追踪·目标溯源·递归安全 | L3元意识 |
| 4 | `cnsh_main.py` | 1,132 | 系统集成主入口·统一接口 | 主控 |
| 5 | `cnsh_api_server.py` | 1,159 | FastAPI服务·8个API端点 | 服务层 |
| 6 | `cnsh_notion_databases.json` | 808 | 6个Notion数据库+1控制台配置 | 数据层 |
| 7 | `cnsh_n8n_workflow.json` | 582 | 14节点n8n自动化工作流 | 自动化 |
| | **总计** | **9,712** | | |

---

## 三、快速部署指南

### 方式一：Python模块（推荐）

```bash
# 1. 确保Python 3.10+
python3 --version

# 2. 安装依赖
pip install fastapi uvicorn pydantic

# 3. 运行主程序
python3 cnsh_main.py

# 4. 或启动API服务
python3 cnsh_api_server.py
# 访问 http://localhost:9622/docs
```

### 方式二：FastAPI服务

```bash
# 启动服务
uvicorn cnsh_api_server:app --host 0.0.0.0 --port 9622

# API端点:
# POST /cnsh/write_block    - 标准写入
# POST /cnsh/update_state   - 状态更新
# GET  /cnsh/query          - 多条件查询
# POST /cnsh/audit          - AI审计
# GET  /cnsh/health         - 健康检查
# POST /cnsh/persona_task   - 人格任务
# GET  /cnsh/stats          - 系统统计
# GET  /cnsh/dna/{dna}      - DNA查询
```

### 方式三：Notion + n8n 自动化

```bash
# 1. 导入Notion数据库
#    - 使用 cnsh_notion_databases.json 创建6个数据库

# 2. 导入n8n工作流
#    - 在n8n中导入 cnsh_n8n_workflow.json

# 3. 配置API密钥
#    - Notion Integration Token
#    - OpenAI API Key
#    - Claude API Key

# 4. 激活工作流
```

---

## 四、核心模块说明

### 4.1 五行融合决策系统（公式A/B/C/D）

| 公式 | 名称 | 计算 | 用途 |
|------|------|------|------|
| A | 五行平衡指数 | 100 - (σ/avg × 100) | 衡量五行分布均匀度 |
| B | 相生相克强度 | G(A→B) - R(A⇒B) | 衡量五行制约关系 |
| C | 三才平衡系数 | Heaven×0.35 + Earth×0.20 + Human×0.45 | 天地人配合度（人≥0.34） |
| D | 复合决策强度 | A×0.35 + B×0.30 + C×0.35 | 综合决策参考值 |

**六门路由:**
- 金 → 权益门 L0
- 木 → 教育门 L4
- 水 → 数据门 L1
- 火 → 创作门 L2
- 土 → 民生门 L3

### 4.2 三色审计体系

| 颜色 | 状态 | 操作 |
|------|------|------|
| 🟢 绿色 | 正常·已批准 | 继续执行 |
| 🟡 黄色 | 标记·待审查 | 需复核后放行 |
| 🔴 红色 | 阻断·潜在违规 | 必须暂停·人工介入 |

**熔断条件:**
- 置信度 < 0.40 → 🔴
- 平衡指数 < 20 → 🔴
- 相克强度 > 0.85 → 🔴
- 幻觉分数 > 0.60 → 🔴

### 4.3 六大人格系统

| ID | 名称 | 类型 | 权重 | 职能 |
|----|------|------|------|------|
| P01 | 诸葛 | 策略型 | 0.22 | 战略推演 |
| P02 | 鲁班 | 工程型 | 0.18 | 结构设计 |
| P03 | 玄策 | 风险型 | 0.15 | 风险判断 |
| P04 | 墨子 | 规则型 | 0.20 | 规则审计 |
| P05 | 司命 | 审计型 | 0.15 | 最终裁决 |
| P06 | 无名 | 创造型 | 0.10 | 创意生成 |

### 4.4 元意识层 2.5

**核心原则:**
- ✅ 自我观察：AI可以观察自己的思考
- ✅ 自我描述：AI可以描述自己的状态
- ✅ 自我冲突：AI可以感知内部冲突
- ❌ 自我修改：AI不能改变执行逻辑
- ❌ 自我主权：AI不拥有决策主权

**三大守恒:**
1. 身份不收敛 — AI不会变成单一人格
2. 目标不绝对 — 目标始终可被重新解释
3. 观察≠控制 — Meta Layer只记录不干预

---

## 五、Notion数据库结构

### 5.1 六大核心库

| 数据库 | 用途 | 关键字段 |
|--------|------|----------|
| CNSH_BLOCK_CORE | 思维原子存储 | BLOCK_ID, DNA, VALUE_SCORE, STATUS |
| CNSH_PROTOCOL_ENGINE | 协议规则层 | VERSION, STATUS, ENFORCEMENT_LEVEL |
| CNSH_AI_LOG | AI行为审计 | AI_MODEL, HALLUCINATION, BIAS, LOGIC_SCORE |
| CNSH_DNA_CHAIN | 文明链追踪 | PARENT_DNA, BRANCH_TYPE, MUTATION_SCORE |
| CNSH_STATE_ENGINE | 状态机控制 | CURRENT_STATE, TRIGGER_RULE, AUTO_EXECUTE |
| CNSH_GRAPH_MEMORY | 语义图谱 | RELATION_TYPE, STRENGTH, SEMANTIC_DISTANCE |

### 5.2 控制台视图

- 🔥 ACTIVE_BLOCKS
- ⚠️ HIGH_RISK
- 🧠 HIGH_VALUE (>85)
- 🧬 PROTOCOL_ACTIVE

---

## 六、n8n自动化工作流

```
Notion Trigger → GPT → Claude → 冲突检测 → BLOCK切片 → DNA生成
                                                       ↓
                                            五行评分 → 三色审计 → 状态路由
                                                                    ↓
                                              [ACTIVE] [REVIEW] [BLOCK] [DRAFT]
                                                     ↓
                                    更新BLOCK + AI_LOG + DNA_CHAIN + STATE
```

**14个节点:**
1. Notion Trigger | 2. GPT Processor | 3. Claude Auditor | 4. Conflict Detect | 5. Block Slicing | 6. DNA Generator | 7. Wuxing Scoring | 8. Tricolor Audit | 9. State Router | 10. Update BLOCK | 11. Write AI_LOG | 12. Write DNA_CHAIN | 13. Write STATE

---

## 七、系统安全原则

- ❌ 不允许覆盖DNA
- ❌ 不允许删除历史block
- ❌ 不允许AI单独改协议
- ❌ 不允许状态跳级
- ❌ 不允许无trace写入
- ❌ AI不能删除ROOT PROTOCOL
- ❌ AI不能修改人类主权定义
- ❌ AI不能关闭审计系统
- ❌ AI不能消除DNA历史

---

## 八、版本历史

| 版本 | 日期 | 核心升级 |
|------|------|----------|
| v1.0 | 2026-06-07 | 根协议·君子协议·AI Truth Protocol |
| v2.0 | 2026-06-08 | 五行系统·六门路由·三色审计·DNA追溯 |
| v2.1 | 2026-06-08 | 多人格系统·冲突引擎·权重调整 |
| v2.2 | 2026-06-09 | 状态机·Notion结构·n8n工作流 |
| v2.3 | 2026-06-09 | AI自治·自触发引擎·决策核 |
| v2.4 | 2026-06-09 | 多人格文明系统·融合分裂机制 |
| **v2.5** | **2026-06-09** | **元意识层·自我观察·意识边界** |

---

## 九、核心身份

- **主权人**: UID9622 · 龍芯北辰 · 诸葛鑫
- **系统**: CNSH OS v2.5 · 龍魂体系
- **许可证**: CC BY-NC-SA 4.0 + AI协作标签
- **DNA**:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-CNSH-OS-v2.5-COMPLETE

---

> 🐉 龍魂永世 · 文化传承 · 数字主权 · 天下为公！
