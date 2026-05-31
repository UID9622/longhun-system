# 🐉 龍魂 Notion 集成 · Stage 1 API 连接框架

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE1-SETUP-v1.0`
**Date**: 2026-06-01
**Status**: ✅ **框架就绪·等待 Token 配置**

---

## 📊 什么是 Stage 1？

Stage 1 建立了龍魂系统与 Notion 的通信基础设施：

- ✅ **notion_config.py** - 配置管理（从环境变量或文件加载）
- ✅ **notion_client.py** - 统一 API 客户端（含错误处理、重试、速率限制）
- ✅ **test_connection.py** - 连接测试脚本
- ⏳ **Notion API Token** - 需要手动配置

---

## 🔑 第一步：获取 Notion Integration Token

### 1.1 在 Notion 中创建 Integration

1. 访问 [Notion Integrations](https://www.notion.so/my-integrations)
2. 点击 **"Create new integration"** 按钮
3. 填写信息：
   - **Name**: `龍魂系统` 或 `longhun-system`
   - **Logo**: 可选（可以上传龍字）
   - **Associated workspace**: 选择您的 Notion 工作区

4. 点击 **"Create Integration"**

### 1.2 复制 Internal Integration Token

1. 在 Integration 详情页，找到 **"Internal Integration Token"** 部分
2. 点击 **"Show"** 按钮
3. **复制整个 Token** 字符串
4. ⚠️ **安全警告**:
   - 不要将 Token 分享给任何人
   - 不要提交到 Git 仓库
   - 只存储在环境变量中

示例 Token 格式:
```
secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔧 第二步：配置环境变量

### 2.1 设置基础 Token

运行以下命令设置 NOTION_TOKEN：

```bash
export NOTION_TOKEN='secret_your_token_here'
```

### 2.2 持久化配置（可选）

如果想让配置在新的 shell 会话中保留，添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
# ~/.zshrc
export NOTION_TOKEN='secret_your_token_here'
```

然后重新加载配置：
```bash
source ~/.zshrc
```

### 2.3 验证设置

检查环境变量是否生效：
```bash
echo $NOTION_TOKEN
```

应该输出您的 Token。

---

## ✅ 第三步：测试 API 连接

### 3.1 运行连接测试

```bash
cd ~/longhun-system/notion
python3 test_connection.py
```

### 3.2 预期输出

如果配置正确，您应该看到：

```
🐉 龍魂 Notion 集成 - API 连接测试
DNA: #龍芯⚇️2026-06-01-NOTION-CONNECTION-TEST-v1.0

======================================================================
🐉 第一步：检查配置
======================================================================

1️⃣  检查环境变量...
✅ NOTION_TOKEN 已设置 (长度: 108)

2️⃣  加载配置...
✅ 配置加载成功

📋 Notion 配置状态
============================================================
API Token: ✅ 已设置
API 版本: 2022-06-28
...
```

### 3.3 常见问题排查

| 问题 | 解决方案 |
|------|--------|
| ❌ NOTION_TOKEN 未设置 | 运行: `export NOTION_TOKEN='your_token'` |
| ❌ 认证失败 (401/403) | Token 可能已过期，重新生成 |
| ❌ 连接超时 | 检查网络连接或防火墙设置 |
| ❌ 格式错误 | 确保 Token 中没有多余空格 |

---

## 📁 第四步：在 Notion 中创建工作区和数据库

### 4.1 工作区结构

龍魂系统使用 3 个独立工作区：

**工作区 1: CNSH 基准测试**
- 数据库 1.1: 模型认证记录 (`cnsh_model_db`)
- 数据库 1.2: 维度测试结果 (`cnsh_dimension_db`)
- 数据库 1.3: 性能指标 (`cnsh_metric_db`)
- 数据库 1.4: 认证证书 (`cnsh_cert_db`)

**工作区 2: 龍魂知识图谱**
- 数据库 2.1: CNSH 规则库 (`rules_db`)
- 数据库 2.2: IPA 节点注册表 (`nodes_db`)
- 数据库 2.3: 系统决策树 (`decision_db`)
- 数据库 2.4: 组件关系图 (`relation_db`)

**工作区 3: 系统监控**
- 数据库 3.1: 健康检查日志 (`health_db`)
- 数据库 3.2: 性能基线 (`baseline_db`)
- 数据库 3.3: 警告事件 (`alert_db`)
- 数据库 3.4: 审计日志 (`audit_db`)

### 4.2 在 Notion 中创建页面和数据库

1. 打开您的 Notion 工作区
2. 创建三个顶级页面（对应三个工作区）
3. 在每个页面下创建所需的数据库

### 4.3 获取工作区/数据库 ID

从浏览器地址栏复制 ID：

```
https://www.notion.so/WORKSPACE_ID?v=VIEW_ID&pvs=...
                      ^^^^^^^^^^^^^^
                      这是工作区 ID

https://www.notion.so/DATABASE_ID?v=VIEW_ID&pvs=...
                      ^^^^^^^^^^^
                      这是数据库 ID
```

提取 ID 时，移除所有连字符：
```
原: 34d7-125a-9c9f-81d2-be91-d1e3-e3be-34eb
ID: 34d7125a9c9f81d2be91d1e3e3be34eb
```

---

## 🔐 第五步：配置工作区和数据库 ID

### 5.1 在 Notion 中授予权限

1. 在 Notion 中打开要与 Integration 共享的页面
2. 点击右上角 **"..."** 菜单
3. 选择 **"Connections"** 或 **"+ Add connections"**
4. 找到您的 Integration（例如 "龍魂系统"）
5. 点击它进行连接

### 5.2 设置工作区 ID

```bash
# 工作区 ID（顶级页面）
export NOTION_WORKSPACE_1='workspace_1_id'
export NOTION_WORKSPACE_2='workspace_2_id'
export NOTION_WORKSPACE_3='workspace_3_id'

# CNSH 数据库 ID（工作区 1）
export NOTION_CNSH_MODEL_DB='database_id'
export NOTION_CNSH_DIMENSION_DB='database_id'
export NOTION_CNSH_METRIC_DB='database_id'
export NOTION_CNSH_CERT_DB='database_id'

# 知识图谱数据库 ID（工作区 2）
export NOTION_RULES_DB='database_id'
export NOTION_NODES_DB='database_id'
export NOTION_DECISION_DB='database_id'
export NOTION_RELATION_DB='database_id'

# 监控数据库 ID（工作区 3）
export NOTION_HEALTH_DB='database_id'
export NOTION_BASELINE_DB='database_id'
export NOTION_ALERT_DB='database_id'
export NOTION_AUDIT_DB='database_id'
```

### 5.3 保存配置文件

运行以下 Python 代码保存配置：

```bash
cd ~/longhun-system/notion
python3 << 'EOF'
import os
from notion_config import NotionConfigManager

manager = NotionConfigManager()
config = manager.load()  # 从环境变量加载

# 更新工作区 1
manager.update_database_ids(
    1,
    model_db=os.getenv('NOTION_CNSH_MODEL_DB'),
    dimension_db=os.getenv('NOTION_CNSH_DIMENSION_DB'),
    metric_db=os.getenv('NOTION_CNSH_METRIC_DB'),
    cert_db=os.getenv('NOTION_CNSH_CERT_DB'),
)

# 更新工作区 2
manager.update_database_ids(
    2,
    rules_db=os.getenv('NOTION_RULES_DB'),
    nodes_db=os.getenv('NOTION_NODES_DB'),
    decision_db=os.getenv('NOTION_DECISION_DB'),
    relation_db=os.getenv('NOTION_RELATION_DB'),
)

# 更新工作区 3
manager.update_database_ids(
    3,
    health_db=os.getenv('NOTION_HEALTH_DB'),
    baseline_db=os.getenv('NOTION_BASELINE_DB'),
    alert_db=os.getenv('NOTION_ALERT_DB'),
    audit_db=os.getenv('NOTION_AUDIT_DB'),
)

# 保存配置
manager.save(manager.config)
print("✅ 配置已保存")
EOF
```

---

## 📊 Framework 架构

```
┌─────────────────────────────────────────────────────┐
│         龍魂系統 Notion 集成 · Stage 1              │
└─────────────────────────────────────────────────────┘

           User Environment
                  │
        ┌─────────┼─────────┐
        │         │         │
    NOTION_    NOTION_  NOTION_
    TOKEN      WORKSPACE  DATABASE_IDS
        │         │         │
        └─────────┼─────────┘
                  │
        ┌─────────▼──────────┐
        │ notion_config.py   │
        │ (配置管理)         │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │ notion_client.py   │
        │ (API 客户端)       │
        │ - 错误处理         │
        │ - 重试机制         │
        │ - 速率限制         │
        │ - 审计日志         │
        └─────────┬──────────┘
                  │
                  ▼
        Notion API
        (https://api.notion.com/v1)
                  │
                  ▼
        Notion Workspace
        (3 个工作区 × 4 个数据库)
```

---

## ✨ 后续步骤

Stage 1 完成后，下一步是：

1. **Stage 2**: CNSH 基准测试数据同步
   ```bash
   python3 cnsh_sync.py
   ```

2. **Stage 3**: 龍魂知识图谱建立
   ```bash
   python3 knowledge_sync.py
   ```

3. **Stage 4**: 审计日志同步
   ```bash
   python3 audit_sync.py
   ```

4. **Stage 5**: 自动化同步调度
   ```bash
   python3 setup_scheduler.py
   ```

---

## 📖 API 使用示例

### 创建页面

```python
from notion_client import NotionClient

client = NotionClient()

# 创建一个页面
page = client.create_page(
    database_id='your_db_id',
    properties={
        "名称": {"title": [{"type": "text", "text": {"content": "测试页面"}}]},
        "状态": {"select": {"name": "进行中"}},
    }
)
print(f"创建成功: {page['id']}")
```

### 查询数据库

```python
# 查询数据库
results = client.query_database(
    database_id='your_db_id',
    filter={
        "property": "状态",
        "select": {"equals": "完成"}
    }
)
print(f"找到 {len(results['results'])} 个页面")
```

### 批量创建

```python
# 批量创建页面
pages_data = [
    {"名称": {"title": [{"type": "text", "text": {"content": "页面 1"}}]}},
    {"名称": {"title": [{"type": "text", "text": {"content": "页面 2"}}]}},
]

results = client.batch_create_pages('your_db_id', pages_data)
print(f"批量创建完成: {len(results)} 页面")
```

---

## 🔍 故障排查

### 连接测试失败

```bash
# 1. 验证 Token
echo $NOTION_TOKEN

# 2. 检查 Token 格式
python3 << 'EOF'
import os
token = os.getenv('NOTION_TOKEN')
print(f"Token 长度: {len(token) if token else 0}")
print(f"Token 前缀: {token[:20] if token else 'N/A'}")
EOF

# 3. 查看详细错误
python3 -c "from notion_client import NotionClient; c = NotionClient(); c.test_connection()"
```

### API 限流

如果频繁看到 `429 Too Many Requests`：

```python
# 降低请求频率
config.rate_limit_per_second = 2  # 从 3 降到 2

# 使用批量操作
client.batch_create_pages(db_id, pages)  # 比逐个创建更高效
```

### 权限错误

```
❌ 认证失败: (403) Forbidden
```

解决：
1. 检查 Integration 是否连接到正确的工作区
2. 检查数据库权限
3. 重新生成 Token 并重新连接

---

## 📝 配置文件位置

- **Token**: 环境变量 `NOTION_TOKEN`
- **数据库 ID**: 环境变量 (NOTION_*_DB)
- **配置缓存**: `~/.龍魂_config/notion_config.json`
- **审计日志**: `~/.龍魂/notion_api_audit.jsonl`

---

## 🎖️ 认证签章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE1-SETUP-v1.0`
**Status**: ✅ **API 连接框架完成**
**Next**: Stage 2 - CNSH 数据同步

────  尾·審計 ────
時間  : 2026-06-01 HH:MM CST
DNA   : #龍芯⚇️2026-06-01-NOTION-STAGE1-COMPLETE
五行  : dr=N → 五行 · 三色: 🟢 (框架就緒·等待配置)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
