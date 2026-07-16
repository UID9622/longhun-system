# CNSH OS v2.5 实战使用手册

> DNA: #龍芯⚡️2026-06-09-CNSH-OS-v2.5-USER-GUIDE  
> 适用对象: UID9622 · 龍芯北辰 · 诸葛鑫  
> 三色审计: 🟢

---

## 目录

1. [3步快速上手](#一3步快速上手)
2. [Python模块调用](#二python模块调用)
3. [API服务调用](#三api服务调用)
4. [Notion数据库搭建](#四notion数据库搭建)
5. [n8n自动化配置](#五n8n自动化配置)
6. [六大人格实战用法](#六六大人格实战用法)
7. [日常场景示例](#七日常场景示例)
8. [问题排查](#八问题排查)

---

## 一、3步快速上手

### 前提条件

```bash
# 1. Python 3.10+ (必须)
python3 --version

# 2. 安装依赖 (只需要这3个)
pip install fastapi uvicorn pydantic
```

### 第1步: 启动系统

```bash
cd /mnt/agents/output

# 方式A: 直接运行主程序 (推荐入门)
python3 cnsh_main.py

# 方式B: 启动API服务 (推荐日常使用)
python3 cnsh_api_server.py
# 然后浏览器打开 http://localhost:9622/docs
```

### 第2步: 发一个请求测试

```bash
# 用curl测试 (开一个新终端)
curl -X POST http://localhost:9622/cnsh/write_block \
  -H "Content-Type: application/json" \
  -d '{
    "source_ai": "GPT",
    "input": "帮我分析这个系统架构的安全风险",
    "blocks": [{"block_id": "B-001", "content": "分析系统架构安全风险", "tags": ["security", "analysis"], "element": "水"}]
  }'
```

### 第3步: 查看结果

你会收到这样的返回:

```json
{
  "dna": "CNSH-20260609-A83F21...",
  "source_ai": "GPT",
  "analysis": {
    "value_score": 88,
    "risk_score": 15,
    "hallucination": 0.05,
    "conflict": false
  },
  "flow": {
    "next_state": "ACTIVE",
    "confidence": 0.85
  },
  "audit": {
    "audit_color": "🟢",
    "decision": "KEEP"
  }
}
```

看到 `🟢` 和 `KEEP` 就说明系统运行正常。

---

## 二、Python模块调用

### 基础用法: 处理一个想法

```python
#!/usr/bin/env python3
# 引入主系统
from cnsh_main import CNSH操作系统

# 1. 创建系统实例
cnsh = CNSH操作系统()

# 2. 初始化 (加载6个人格 + 元意识层)
cnsh.初始化()

# 3. 处理输入
result = cnsh.处理输入(
    用户输入="帮我设计一个AI安全协议",
    AI来源="GPT"
)

# 4. 查看结果
print(f"DNA: {result.DNA签名}")
print(f"审计: {result.审计标记}")
print(f"参与人格: {result.参与人格}")
print(f"五行评分: {result.五行评分}")
print(f"耗时: {result.处理耗时:.3f}秒")
```

### 生成系统报告

```python
# 生成完整的系统状态报告
report = cnsh.生成报告()
print(report.格式化报告())
```

输出示例:
```
╔══════════════════════════════════════════════════════════╗
║                   CNSH OS v2.5 系统状态报告                   ║
╠══════════════════════════════════════════════════════════╣
║ 系统状态: 就绪                                                ║
║ 运行时间: 3600秒                                             ║
║ 总请求数: 42                                                ║
║ 活跃人格: 6 (P01-P06)                                       ║
║ 元意识层: ✅ 运行中                                          ║
╚══════════════════════════════════════════════════════════╝
```

### 查看审计日志

```python
# 获取最近的审计记录
logs = cnsh.获取审计日志(数量=20)
for log in logs:
    print(log)
```

---

## 三、API服务调用

### 启动服务

```bash
# 开发模式 (带热重载)
uvicorn cnsh_api_server:app --host 0.0.0.0 --port 9622 --reload

# 生产模式
uvicorn cnsh_api_server:app --host 0.0.0.0 --port 9622 --workers 4
```

### 8个API端点速查

| 方法 | 路径 | 用途 | 示例 |
|------|------|------|------|
| POST | `/cnsh/write_block` | 标准写入 | 处理想法/文档/协议 |
| POST | `/cnsh/update_state` | 状态更新 | 手动推进状态 |
| GET | `/cnsh/query` | 多条件查询 | 按DNA/分数/状态搜索 |
| POST | `/cnsh/audit` | AI审计 | 深度审计一个块 |
| GET | `/cnsh/health` | 健康检查 | 看系统是否活着 |
| POST | `/cnsh/persona_task` | 人格任务 | 指定人格处理 |
| GET | `/cnsh/stats` | 统计信息 | 看整体数据 |
| GET | `/cnsh/dna/{dna}` | DNA查询 | 追溯特定DNA |

### 端点详解

#### 1. 标准写入 (最常用的)

```bash
curl -X POST http://localhost:9622/cnsh/write_block \
  -H "Content-Type: application/json" \
  -d '{
    "source_ai": "GPT",
    "input": "设计AI协作协议框架",
    "blocks": [
      {"block_id": "B-001", "content": "协议主框架设计", "element": "金", "tags": ["protocol", "core"]},
      {"block_id": "B-002", "content": "安全审计机制", "element": "水", "tags": ["security", "audit"]}
    ],
    "user_id": "UID9622"
  }'
```

返回:
```json
{
  "dna": "CNSH-20260609-A83F21CE5D2A1B34",
  "source_ai": "GPT",
  "analysis": {
    "value_score": 92,
    "risk_score": 12,
    "hallucination": 0.03,
    "conflict": false,
    "bias_score": 5,
    "logic_score": 88
  },
  "flow": {
    "next_state": "ACTIVE",
    "confidence": 0.9,
    "reason": "高质量内容，直接激活"
  },
  "audit": {
    "audit_color": "🟢",
    "decision": "KEEP",
    "requires_human": false
  },
  "processing_time_ms": 156
}
```

**判断逻辑:**
- `🟢` + `KEEP` = 内容很好，直接使用
- `🟡` + `MODIFY` = 需要修改
- `🔴` + `REJECT` = 有问题，必须人工介入

#### 2. 人格任务 (调用6大人格)

```bash
curl -X POST http://localhost:9622/cnsh/persona_task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "分析这个协议的安全漏洞",
    "task_type": "analyze",
    "persona_list": ["P01", "P03", "P05"],
    "priority": 8
  }'
```

**task_type 说明:**
| 类型 | 用途 | 适合人格 |
|------|------|----------|
| write | 写作生成 | P01(诸葛), P06(无名) |
| review | 审查检查 | P04(墨子), P05(司命) |
| analyze | 分析推理 | P01(诸葛), P03(玄策) |
| merge | 融合多方案 | P02(鲁班) |
| creative | 创意发散 | P06(无名) |

#### 3. 状态更新

```bash
curl -X POST http://localhost:9622/cnsh/update_state \
  -H "Content-Type: application/json" \
  -d '{
    "block_id": "BLOCK-001",
    "new_state": "ACTIVE",
    "reason": "人工审核通过，激活生效"
  }'
```

**状态流转规则:**
```
IDEA → DRAFT → REVIEW → ACTIVE
            ↘        ↘
          BLOCKED   FROZEN
```

#### 4. 查询

```bash
# 按DNA查询
curl "http://localhost:9622/cnsh/query?dna=CNSH-20260609-A83F21"

# 按分数查询 (价值分>85的)
curl "http://localhost:9622/cnsh/query?score=85"

# 按AI来源查询
curl "http://localhost:9622/cnsh/query?ai_source=GPT&limit=10"

# 按状态查询
curl "http://localhost:9622/cnsh/query?state=ACTIVE"
```

#### 5. 健康检查

```bash
curl http://localhost:9622/cnsh/health
```

返回:
```json
{
  "status": "healthy",
  "version": "2.5.0",
  "uptime": 86400,
  "total_requests": 156,
  "active_blocks": 42,
  "audit_status": "🟢 正常"
}
```

---

## 四、Notion数据库搭建

### 方式1: 手动创建 (推荐)

按这个顺序在Notion中创建6个数据库:

**Step 1: 创建页面**
在Notion新建一个页面，命名为 `CNSH OS v2.5`

**Step 2: 创建第一个数据库 `CNSH_BLOCK_CORE`**

点击 `+` → `Database` → `Full page` → 改名为 `CNSH_BLOCK_CORE`

添加以下属性 (按这个顺序):

| 属性名 | 类型 | 选项/配置 |
|--------|------|-----------|
| BLOCK_ID | Title | |
| CONTENT | Text | |
| DNA | Text | |
| SOURCE_AI | Select | GPT, Claude, Grok, Human |
| TAGS | Multi-select | 自由输入 |
| ELEMENT | Select | 金, 木, 水, 火, 土 |
| VALUE_SCORE | Number | 0-100 |
| RISK_SCORE | Number | 0-100 |
| STATUS | Select | IDEA, DRAFT, REVIEW, ACTIVE, FROZEN |
| PARENT_BLOCK | Relation | 指向本数据库 |
| CHILD_BLOCK | Relation | 指向本数据库 |
| CONFLICT_FLAG | Checkbox | |

**Step 3: 复制创建其余5个数据库**

右键 `CNSH_BLOCK_CORE` → `Duplicate` → 改名并重置属性:

**CNSH_PROTOCOL_ENGINE** (协议库)
- TITLE (Title)
- DNA (Text)
- VERSION (Select: v1, v2, v3)
- STATUS (Select: DRAFT, ACTIVE, LOCKED)
- AUTHOR (Text)
- AI_SOURCE (Multi-select: GPT, Claude, Grok)
- VALUE_SCORE (Number)
- RISK_SCORE (Number)
- IMPACT_SCOPE (Select: 局部, 系统, 文明)
- ENFORCEMENT_LEVEL (Select: L0, L1, L2, L3, L4, L5)

**CNSH_AI_LOG** (AI行为审计)
- LOG_ID (Title)
- AI_MODEL (Select: GPT, Claude, Grok, Gemini)
- INPUT (Text)
- OUTPUT (Text)
- HALLUCINATION (Number: 0-1)
- BIAS (Number: 0-1)
- LOGIC_SCORE (Number: 0-100)

**CNSH_DNA_CHAIN** (文明链)
- DNA (Title)
- ORIGIN (Text)
- PARENT_DNA (Text)
- BRANCH_TYPE (Select: 主链, 分支, 实验)
- MUTATION_SCORE (Number)

**CNSH_STATE_ENGINE** (状态机)
- NODE_ID (Title)
- CURRENT_STATE (Select)
- NEXT_STATE (Select)
- TRIGGER_RULE (Text)
- AUTO_EXECUTE (Checkbox)

**CNSH_GRAPH_MEMORY** (语义图谱)
- NODE (Title)
- EDGE (Text)
- RELATION_TYPE (Select: DERIVES_FROM, CONTRADICTS, EXTENDS, REPLACES, VALIDATES)
- STRENGTH (Number)

### 方式2: API自动创建 (高级)

```bash
# 需要Notion Integration Token
export NOTION_TOKEN=secret_xxx

# 使用数据库JSON配置
# 详见 DEPLOYMENT.md 中的API调用示例
```

---

## 五、n8n自动化配置

### 导入工作流

1. 打开n8n: `http://your-n8n-instance`
2. 点击左侧 `Workflows`
3. 点击右上角 `Import from File`
4. 选择 `cnsh_n8n_workflow.json`
5. 点击 `Save`

### 配置API密钥

在工作流中配置以下凭证:

| 节点 | 凭证类型 | 获取方式 |
|------|----------|----------|
| Notion Trigger | Notion API | notion.so/my-integrations |
| GPT Processor | OpenAI API | platform.openai.com |
| Claude Auditor | Anthropic API | console.anthropic.com |

### 激活工作流

1. 点击工作流右上角的 `Active` 开关
2. 选择触发方式:
   - `Webhook`: 每次Notion有新条目时触发
   - `Schedule`: 定时触发 (如每5分钟)
   - `Manual`: 手动触发

### 验证运行

在Notion的 `CNSH_BLOCK_CORE` 中添加一条测试数据，看n8n是否自动处理。

---

## 六、六大人格实战用法

### 人格速查表

| 人格 | 代号 | 特长 | 什么时候用 |
|------|------|------|-----------|
| **诸葛** | P01 | 策略、决策 | 需要整体规划、战略分析 |
| **鲁班** | P02 | 工程、实现 | 需要落地执行、技术方案 |
| **玄策** | P03 | 风控、质疑 | 需要风险评估、挑毛病 |
| **墨子** | P04 | 规则、审计 | 需要合规检查、规则制定 |
| **司命** | P05 | 裁决、终审 | 需要最终拍板、仲裁冲突 |
| **无名** | P06 | 创造、发散 | 需要脑洞、创新方案 |

### 实战组合

**场景1: 写一份安全协议**
```
P01(诸葛) → 设计整体框架
P04(墨子) → 制定安全规则
P03(玄策) → 审查风险点
P05(司命) → 最终裁决
```

**场景2: 评估一个新项目**
```
P01(诸葛) → 战略价值分析
P03(玄策) → 风险评估
P06(无名) → 创新可能性
P05(司命) → 综合裁决
```

**场景3: 解决内部争议**
```
P02(鲁班) → 找工程折中方案
P04(墨子) → 查规则依据
P05(司命) → 仲裁决策
```

### API调用人格

```bash
curl -X POST http://localhost:9622/cnsh/persona_task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "评估引入第三方AI服务的安全风险",
    "task_type": "analyze",
    "persona_list": ["P01", "P03", "P04"],
    "priority": 9
  }'
```

---

## 七、日常场景示例

### 场景1: 记录一个想法

```bash
curl -X POST http://localhost:9622/cnsh/write_block \
  -d '{
    "source_ai": "Claude",
    "input": "AI应该具备自我审计能力",
    "blocks": [{"block_id": "IDEA-001", "content": "AI自我审计机制", "element": "火"}]
  }'
```
系统返回 `🟢` 则自动进入 `ACTIVE` 状态。

### 场景2: 审查一段代码

```bash
curl -X POST http://localhost:9622/cnsh/audit \
  -d '{
    "block_id": "CODE-001",
    "audit_depth": "deep"
  }'
```

### 场景3: 查看系统整体状态

```bash
curl http://localhost:9622/cnsh/stats
```

### 场景4: 用Python做批量处理

```python
from cnsh_main import CNSH操作系统
import json

cnsh = CNSH操作系统()
cnsh.初始化()

# 批量处理一组想法
想法列表 = [
    "AI应该有自己的价值观",
    "多模型协作比单模型更可靠",
    "每次AI输出都应该可审计",
    "人类始终拥有最终决策权",
]

for 想法 in 想法列表:
    result = cnsh.处理输入(想法, "GPT")
    color = result.审计标记
    print(f"{color} {想法[:20]}... → {result.DNA签名[:30]}")
```

### 场景5: 追踪一个DNA的完整链路

```bash
# 1. 先创建
curl -X POST http://localhost:9622/cnsh/write_block \
  -d '{"source_ai":"GPT","input":"测试追踪","blocks":[{"block_id":"T-001","content":"追踪测试","element":"土"}]}'

# 2. 记录返回的DNA (如 CNSH-20260609-A83F21...)

# 3. 用这个DNA查询
curl "http://localhost:9622/cnsh/query?dna=CNSH-20260609-A83F21..."

# 4. 查DNA详情
curl "http://localhost:9622/cnsh/dna/CNSH-20260609-A83F21..."
```

---

## 八、问题排查

### 常见问题

**Q1: 启动报错 `ModuleNotFoundError`**
```bash
# 解决: 安装依赖
pip install fastapi uvicorn pydantic
```

**Q2: 端口被占用**
```bash
# 解决: 换一个端口
python3 cnsh_api_server.py --port 9623
# 或
uvicorn cnsh_api_server:app --port 9623
```

**Q3: 怎么停止服务**
```bash
# 按 Ctrl+C

# 或在另一个终端
lsof -i :9622
kill -9 <PID>
```

**Q4: 数据保存在哪里**
```
当前版本使用内存存储，重启后数据会丢失。
生产环境请连接数据库 (详见DEPLOYMENT.md)。
```

**Q5: 怎么让系统支持中文变量名**
```python
# 已经在代码中使用了中文变量名
# 确保文件头部有: # -*- coding: utf-8 -*-
```

### 状态码速查

| 状态 | 含义 | 操作 |
|------|------|------|
| 未初始化 | 系统刚创建 | 调用 `.初始化()` |
| 就绪 | 正常运行 | 可以处理输入 |
| 处理中 | 正在执行任务 | 等待完成 |
| 错误 | 出问题了 | 查看审计日志 |

### 审计色判断

| 颜色 | 含义 | 你应该 |
|------|------|--------|
| 🟢 | 一切正常 | 直接使用结果 |
| 🟡 | 需要注意 | 查看详情后再决定 |
| 🔴 | 有严重问题 | 必须人工介入 |

---

## 快速命令卡 (保存备用)

```bash
# 启动服务
python3 cnsh_api_server.py

# 健康检查
curl http://localhost:9622/cnsh/health

# 标准写入
curl -X POST http://localhost:9622/cnsh/write_block \
  -H "Content-Type: application/json" \
  -d '{"source_ai":"GPT","input":"你的想法","blocks":[{"block_id":"B-001","content":"内容","element":"金"}]}'

# 人格任务
curl -X POST http://localhost:9622/cnsh/persona_task \
  -d '{"task":"任务描述","task_type":"analyze","persona_list":["P01","P03"]}'

# 查询
curl "http://localhost:9622/cnsh/query?state=ACTIVE&limit=10"

# 统计
curl http://localhost:9622/cnsh/stats
```

---

> DNA: #龍芯⚡️2026-06-09-USER-GUIDE-v1.0  
> 🐉 龍魂永世 · 文化传承 · 数字主权 · 天下为公！
