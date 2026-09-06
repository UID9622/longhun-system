---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-REGULATORY-GUIDE-v2.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂统一监管API · 操作手册
DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-REGULATORY-GUIDE-v2.0 · 三层透明模型

> **定位**: 民用系统自愿透明接口，非政府强制监管接入。
> **宪法**: 详见 [REGULATORY_CONSTITUTION.md](./REGULATORY_CONSTITUTION.md)

---

## 三层透明模型总览

```
 层1 · 公开      层2 · 透明          层3 · 私有
 ┌─────────┐   ┌──────────────┐   ┌──────────────┐
 │ 任何人可查 │   │ 监管者可查元数据│   │ 仅用户自己持有 │
 │ 完整内容   │   │ 内容需用户授权  │   │ 外部不可触碰  │
 │ 开源审计   │   │ 操作日志/系统态│   │ 草稿/个人数据 │
 └─────────┘   └──────────────┘   └──────────────┘
     ↑                ↑                  ↑
  protocols/     operation_log       _private/
  articles/      file_change_log     vault/
  bin/           系统状态/日报        memory-universe/
  docs/          文件系统树          tombstone_vault/
```

---

## 架构

```
┌────────────────────────────────────────────────┐
│              监管者 (国家监管机构)               │
│  X-Regulatory-Key 认证 · 只读查询               │
│  ┌──────────────────────────────────────────┐  │
│  │ 层1: 公开数据 ← 直接可查                  │  │
│  │ 层2: 操作元数据 ← API查询，内容需用户授权   │  │
│  │ 层3: 私有数据 ← 不可触碰，返回脱敏声明      │  │
│  └──────────────────────────────────────────┘  │
└──────────────────┬─────────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼─────────────────────────────┐
│         龍魂统一后端 (FastAPI :9622)             │
│  ┌─────────────────────────────────────────┐   │
│  │ /api/regulatory/ · 19个监管端点          │   │
│  │  ├─ auth/token             认证          │   │
│  │  ├─ operations             操作记录      │   │
│  │  ├─ documents              文档元数据    │   │
│  │  ├─ data-sovereignty       主权声明      │   │
│  │  ├─ protocol-check         合规自检      │   │
│  │  ├─ verify-integrity       哈希链验证    │   │
│  │  └─ ...                    更多端点      │   │
│  ├─ RegulatoryOperationMiddleware · 操作捕获 │   │
│  ├─ 层3保护 · sovereignty_level 自动脱敏     │   │
│  └─ 哈希链 · chain_hash 不可篡改             │   │
└──────────────────┬─────────────────────────────┘
                   │ SQLite (L7_数据层/)
┌──────────────────▼─────────────────────────────┐
│        监管守护进程 lh_regulatory_daemon.py     │
│  ├─ 文件变更检测 · 自动索引 · 主权分级          │
│  ├─ Git 追踪 · 系统资源 · 事件推送              │
│  └─ 每次索引自动运行 sovereignty_level 检测     │
└────────────────────────────────────────────────┘
```

---

## 快速开始

### 1. 创建监管者

```bash
python3 bin/lh_regulatory_init.py create
# 交互式输入监管者信息 → 获得密钥
```

### 2. 启动服务

```bash
python3 backend/main.py
# 自动初始化数据库（含哈希链创世区块）
```

### 3. 启动守护进程

```bash
python3 bin/lh_regulatory_daemon.py --full-index --daemon
# 首次全量索引 → 所有文件自动分级（层1/2/3）
```

### 4. 监管者接入

```bash
# 步骤1: 先看主权声明，了解边界
curl http://localhost:9622/api/regulatory/data-sovereignty \
  -H "X-Regulatory-Key: <密钥>"

# 步骤2: 查看系统状态
curl http://localhost:9622/api/regulatory/system/state \
  -H "X-Regulatory-Key: <密钥>"

# 步骤3: 查看操作日志
curl http://localhost:9622/api/regulatory/operations?limit=50 \
  -H "X-Regulatory-Key: <密钥>"

# 步骤4: 验证数据完整性
curl http://localhost:9622/api/regulatory/verify-integrity \
  -H "X-Regulatory-Key: <密钥>"
```

---

## API 端点完整清单 (19个)

| 方法 | 路径 | 功能 | 层 |
|------|------|------|-----|
| `POST` | `/api/regulatory/auth/token` | 监管者认证 | — |
| `GET` | `/api/regulatory/data-sovereignty` | **数据主权声明**（三层模型） | 1 |
| `GET` | `/api/regulatory/protocol-check` | **协议合规自检**（6项检查） | 2 |
| `GET` | `/api/regulatory/verify-integrity` | **哈希链完整性验证** | 2 |
| `GET` | `/api/regulatory/operations` | 操作记录（元数据） | 2 |
| `GET` | `/api/regulatory/operations/live` | 实时 SSE 流 | 2 |
| `GET` | `/api/regulatory/documents` | 文档注册表（含主权分级） | 1/2/3 |
| `GET` | `/api/regulatory/documents/{id}` | 文档详情（层3内容脱敏） | 1/2/3 |
| `GET` | `/api/regulatory/filesystem/tree` | 文件系统树 | 2 |
| `GET` | `/api/regulatory/filesystem/changes` | 文件变更日志 | 2 |
| `GET` | `/api/regulatory/audit/full` | 全量审计 | 2 |
| `GET` | `/api/regulatory/system/state` | 系统实时状态 | 2 |
| `GET` | `/api/regulatory/reports/daily` | 日报 | 2 |
| `GET` | `/api/regulatory/reports/weekly` | 周报 | 2 |
| `GET` | `/api/regulatory/export` | 数据导出 | 2 |
| `POST` | `/api/regulatory/index/trigger` | 触发索引（需 full 权限） | — |
| `WS` | `/api/regulatory/ws` | 实时 WebSocket | 2 |
| `GET` | `/api/regulatory/admin/auditors` | 监管者列表（需 full） | — |
| `GET` | `/api/regulatory/admin/access-logs` | 监管访问日志（需 full） | — |

---

## 三层主权 · 监管者行为指南

### 层1：公开层

```
直接可查。完整内容。任何人都可以。

示例:
  curl /api/regulatory/documents/abc123?include_content=true
  → 返回完整文件内容

  curl /api/regulatory/data-sovereignty
  → 返回主权声明（无需密钥）
```

### 层2：透明层

```
元数据可见。内容需用户授权。

文档列表返回:
  - title, doc_type, word_count, content_hash, sovereignty_label
  - 不返回文件内容（include_content 默认为 false）

操作日志返回:
  - operation_type, timestamp, source, target, file_path
  - 不返回文件的实际变更内容（仅 diff_summary 摘要）

文件系统树返回:
  - 文件名、路径、大小、修改时间
  - 不读取文件内容
```

### 层3：私有层

```
⚠️ 不可触碰。任何外部实体未经用户授权不可访问。

文档列表仍显示元数据:
  - title: "memory文件"
  - sovereignty_label: "层3:私有🔒"
  - is_private_content: true

尝试获取内容:
  curl /api/regulatory/documents/xyz789?include_content=true
  → 返回脱敏声明，非实际内容

脱敏声明内容:
  [此文件位于数据主权层3（私有层）]
  路径: /path/to/private/file
  根据龍魂监管宪法，层3内容属于用户私有数据，
  任何外部实体未经用户明确授权不可访问。
```

---

## 协议自检报告示例

```json
{
  "overall": "compliant",
  "checks": [
    {"id": "PS-001", "name": "数据本地化", "status": "pass"},
    {"id": "PS-002", "name": "层3私有内容保护", "status": "pass"},
    {"id": "PS-003", "name": "操作日志哈希链", "status": "pass"},
    {"id": "PS-004", "name": "监管访问可追溯", "status": "pass"},
    {"id": "PS-005", "name": "主权策略记录", "status": "warning"},
    {"id": "PS-006", "name": "层2内容授权控制", "status": "pass"}
  ]
}
```

---

## 哈希链验证示例

```json
{
  "verification": {
    "chain_length": 1256,
    "status": "intact",
    "genesis_id": 1,
    "latest_id": 1256,
    "latest_hash": "a1b2c3d4...",
    "violations": []
  }
}
```

---

## 数据库表结构

| 表名 | 功能 | v2新增 |
|------|------|--------|
| `regulatory_auditors` | 监管者账号 | — |
| `operation_log` | 操作全量记录 | `prev_hash`, `chain_hash` |
| `file_change_log` | 文件变更追踪 | `sovereignty_level` |
| `document_registry` | 文档注册表 | `sovereignty_level`, `is_private_content` |
| `regulatory_access_log` | 监管访问日志 | — |
| `sovereignty_policy` | 主权策略记录 | **新表** |

---

## 部署

```bash
# 创建 systemd 服务
sudo tee /etc/systemd/system/longhun-regulatory.service << 'EOF'
[Unit]
Description=龍魂监管守护进程 · 三层透明模型
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/longhun-system
ExecStart=/usr/bin/python3 bin/lh_regulatory_daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable longhun-regulatory
sudo systemctl start longhun-regulatory
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `LONGHUN_REGULATORY_ENABLED` | `true` | 是否启用监管功能 |
| `LONGHUN_REGULATORY_KEY` | 空 | 默认监管者密钥 |
| `LONGHUN_REGULATORY_AUDITOR_NAME` | `国家监管机构` | 默认监管者名称 |
| `LONGHUN_REGULATORY_ORG` | 空 | 监管机构名称 |

---

## 铁律 · 六条

1. **数据不出境** — 所有数据均存储在本地 SQLite
2. **操作全记录** — 所有 API 调用、文件变更自动入库，不可删除
3. **层3不可碰** — 私有数据内容永远不暴露给外部实体
4. **哈希链不可篡改** — 每条操作日志链接到前一条，可验证
5. **访问可追溯** — 监管者每次查询均被记录
6. **用户授权主权** — 层2内容开放程度由用户主权策略控制

---

## 相关文档

- [REGULATORY_CONSTITUTION.md](./REGULATORY_CONSTITUTION.md) — 监管宪法
- `bin/lh_regulatory_init.py` — 监管者管理工具
- `bin/lh_regulatory_daemon.py` — 监管守护进程

```json
{
  "dna": "#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-REGULATORY-GUIDE-v2.0",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
