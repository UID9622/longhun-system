# 🌐 通心译 v1.3 × Notion 集成完全指南

**DNA**: `#龍芯⚡️2026-05-27-TONGXINYI-NOTION-INTEGRATION-GUIDE`
**版本**: v1.0
**创建时间**: 2026-05-27

---

## 📋 目录

1. [快速开始（5 分钟）](#快速开始5-分钟)
2. [详细设置步骤](#详细设置步骤)
3. [API 配置](#api-配置)
4. [数据库字段映射](#数据库字段映射)
5. [使用方式](#使用方式)
6. [工作流程](#工作流程)
7. [常见问题](#常见问题)
8. [故障排查](#故障排查)

---

## ⚡ 快速开始（5 分钟）

### 1️⃣ 前置要求

- ✅ Python 3.7+
- ✅ `requests` 库（`pip install requests`）
- ✅ Notion 账户
- ✅ 管理员权限创建 Integration

### 2️⃣ 三步启动

```bash
# Step 1: 安装依赖
pip install requests

# Step 2: 设置环境变量
export NOTION_TOKEN="ntn_your_token_here"
export NOTION_DATABASE_ID="your_database_id"

# Step 3: 运行集成
python _work/engines/engine/on_translate_notion_bridge.py
```

### 3️⃣ 预期结果

```
======================================================================
🌐 通心译 v1.3 × Notion 批量处理开始
======================================================================

[1/10] 处理消息...
   ✅ 页面 xxx 处理成功
   情绪: neutral
   意图: technical_execution
   Persona: ['P04', 'P12']
   DNA: #龍芯⚡️202605271234-PURE_COMMAND-a1b2c3d4

...（更多结果）

======================================================================
📊 处理完成
   总数: 10
   ✅ 成功: 10
   ❌ 失败: 0
======================================================================
```

---

## 🔧 详细设置步骤

### Step 1: 创建 Notion Integration

#### 打开 Notion Integration 管理页面

1. 访问 https://www.notion.so/my-integrations
2. 使用您的 Notion 账号登录

#### 创建新 Integration

1. 点击 **"+ New integration"** 按钮
2. 填写以下信息：
   - **名字**: `通心译 v1.3 Bridge`
   - **描述**: `智能消息处理和路由系统`
   - **关联工作空间**: 选择您的工作空间
   - **功能**: 勾选以下权限
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content

3. 点击 **"Submit"** 创建 Integration

#### 获取 Token

1. Integration 创建成功后，进入详情页
2. 找到 **"Internal Integration Token"** 部分
3. 点击 **"Show"** 显示完整 Token
4. **复制整个 Token**（格式: `ntn_xxxxxxxxxx...`）

**⚠️ 重要**: 妥善保管 Token，不要分享给他人！

---

### Step 2: 创建 Notion 数据库

#### 在 Notion 中创建表格

1. 打开任意 Notion 页面
2. 点击 **"+ 新增"**
3. 选择 **"数据库"** → **"表格"**
4. 命名为 **"🌐 通心译消息处理库"**

#### 添加必需的字段

##### 消息输入字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Title | Title | 消息标题（自动） |
| Content | Rich text | 原始消息内容 |
| Source | Select | 消息来源（CLI/Email/Chat/API） |

**添加方法**:
1. 点击最后一列的 **"+"** 符号
2. 输入字段名
3. 选择字段类型
4. 对于 Select 类型，添加选项值

##### 处理字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Processed | Checkbox | 是否已处理 |
| ProcessedTime | Date | 处理时间 |

##### 通心译输出字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| Scenario | Select | 被动触发场景（7 个选项） |
| Emotion | Select | 情绪识别（7 个选项） |
| Intent | Select | 意图识别（8 个选项） |
| Personas | Multi-select | Persona 推荐（15+ 个选项） |
| DNA | Rich text | DNA 签名 |
| Confidence | Number | 置信度（0-1） |
| Color | Select | 三色标注（🟢🟡🔴） |
| CulturalNote | Rich text | 文化校准备注 |
| Wuxing | Select | 五行属性（5 个选项） |

---

### Step 3: 授予数据库访问权限

#### 连接 Integration 到数据库

1. 打开创建的 Notion 数据库
2. 点击右上角的 **"..."** (三个点)
3. 选择 **"Connections"** 或 **"Add connections"**
4. 搜索 **"通心译 v1.3 Bridge"**
5. 点击选中，然后 **"Confirm"**

#### 复制数据库 ID

1. 打开数据库，复制浏览器 URL
2. URL 格式: `https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxx`
3. 那长串字符就是 **数据库 ID**
4. **复制数据库 ID**（不包括 `?v=` 后面的内容）

---

### Step 4: 配置环境变量

#### 创建 .env 文件

在项目根目录创建 `.env` 文件：

```bash
cd ~/longhun-system
cat > .env << EOF
# 通心译 × Notion 集成配置
NOTION_TOKEN=ntn_your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
LOG_LEVEL=INFO
EOF
```

#### 验证配置

```bash
# 检查 .env 是否正确
cat .env

# 输出应该显示您的 Token 和 Database ID
```

---

### Step 5: 运行集成

#### 命令行运行

```bash
# 方式 1：直接运行脚本
python _work/engines/engine/on_translate_notion_bridge.py

# 方式 2：导入使用
python -c "
from _work.engines.engine.on_translate_notion_bridge import TongxinyiNotionBridge
bridge = TongxinyiNotionBridge()
result = bridge.process_batch(limit=5)
print(f'成功: {result[\"success\"]}, 失败: {result[\"failed\"]}')
"
```

#### 预期输出

```
======================================================================
🌐 通心译 v1.3 × Notion 集成 · 使用演示
======================================================================

【步骤 1】配置 Notion API
----------------------------------------------------------------------
✅ Notion Token: ntn_xxx...
✅ Database ID: abc123...

【步骤 2】初始化集成
----------------------------------------------------------------------
✅ 通心译 × Notion 集成桥接已初始化

【步骤 3】处理消息
----------------------------------------------------------------------
2026-05-27 21:30:45 - __main__ - INFO - 开始查询 Notion 数据库 (最多 5 条)...
2026-05-27 21:30:46 - __main__ - INFO - 成功读取 3 条消息

[1/3] 处理消息...
   ✅ 页面 xxx 处理成功
   情绪: neutral
   意图: technical_execution
   Persona: ['P04', 'P12']
   DNA: #龍芯⚡️202605271234-PURE_COMMAND-xxx

...

【步骤 4】处理结果
----------------------------------------------------------------------

✅ 总处理数: 3
✅ 成功: 3
❌ 失败: 0

🎉 集成成功！
所有处理结果已写回 Notion 数据库
```

---

## 🔌 API 配置

### Notion API 基本信息

| 项目 | 值 |
|------|-----|
| 基础 URL | `https://api.notion.com/v1` |
| API 版本 | `2022-06-28` |
| 认证方式 | Bearer Token |
| 内容类型 | `application/json` |

### 必需的请求头

```python
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
```

### 主要 API 端点

```
查询数据库: POST /databases/{database_id}/query
获取页面: GET /pages/{page_id}
更新页面: PATCH /pages/{page_id}
创建页面: POST /pages
删除页面: DELETE /pages/{page_id}
```

---

## 📊 数据库字段映射

### 输入字段（用户提供）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| Content | Rich text | 原始消息 | `git push origin main` |
| Source | Select | 消息来源 | CLI |
| CreatedTime | Date | 创建时间 | 2026-05-27 |

### 输出字段（通心译生成）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| Scenario | Select | 检测场景 | pure_command |
| Emotion | Select | 情绪识别 | neutral |
| Intent | Select | 意图识别 | technical_execution |
| Personas | Multi-select | Persona 推荐 | P04, P12 |
| DNA | Rich text | DNA 签名 | #龍芯⚡️... |
| Confidence | Number | 置信度 | 0.95 |
| Color | Select | 三色标注 | 🟢 High |

### 控制字段

| 字段 | 类型 | 说明 | 值 |
|------|------|------|-----|
| Processed | Checkbox | 是否已处理 | true/false |
| ProcessedTime | Date | 处理完成时间 | 2026-05-27T21:30:00 |

---

## 💻 使用方式

### 方式 1：批量处理（一次性）

```python
from _work.engines.engine.on_translate_notion_bridge import TongxinyiNotionBridge

# 初始化
bridge = TongxinyiNotionBridge(
    notion_token='ntn_xxx...',
    database_id='xxx...'
)

# 处理最多 10 条消息
result = bridge.process_batch(limit=10)

# 查看结果
print(f"成功: {result['success']}, 失败: {result['failed']}")
```

### 方式 2：持续同步（自动）

```python
# 每 60 秒查询一次，无限循环
bridge.sync_continuous(interval=60)

# 或指定最大迭代次数
bridge.sync_continuous(interval=60, max_iterations=100)
```

### 方式 3：处理单条消息

```python
message = {
    'page_id': 'xxx...',
    'content': 'git push origin main'
}

success = bridge.process_message(message)
print("✅ 成功" if success else "❌ 失败")
```

---

## 🔄 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  用户在 Notion 中输入消息                                  │
│  [Content 字段填入文本]                                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  通心译 × Notion 桥接读取消息                              │
│  [query_database() 查询未处理消息]                        │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  通心译 v1.3 处理消息                                     │
│  [engine.process(content)]                              │
│  ├─ 被动触发检测 (Scenario)                              │
│  ├─ 情绪提取 (Emotion)                                    │
│  ├─ 意图识别 (Intent)                                     │
│  ├─ Persona 路由 (Personas)                              │
│  ├─ 不清识别 (UnclearType)                               │
│  └─ DNA 签名生成 (DNA)                                    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  写入结果到 Notion                                       │
│  [update_page() 更新所有字段]                             │
│  ├─ Scenario ← 检测场景                                   │
│  ├─ Emotion ← 情绪                                       │
│  ├─ Intent ← 意图                                        │
│  ├─ Personas ← Persona 列表                              │
│  ├─ DNA ← DNA 签名                                       │
│  ├─ Confidence ← 置信度                                   │
│  ├─ Processed ✓ ← 标记为已处理                           │
│  └─ ProcessedTime ← 处理时间                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
        ✅ 完成！用户在 Notion 中查看结果
```

---

## ❓ 常见问题

### Q1: 需要安装什么？

**A**: 只需要 `requests` 库：
```bash
pip install requests
```

其他依赖（通心译 v1.3）已包含在项目中。

### Q2: Token 和 Database ID 从哪里获取？

**A**: 参见 [Step 1](#step-1-创建-notion-integration) 和 [Step 3](#step-3-授予数据库访问权限)。

### Q3: 可以处理多少条消息？

**A**: 受 Notion API 速率限制约束（标准计划每秒 3 个请求）。建议：
- 单次批处理：≤ 100 条消息
- 间隔时间：≥ 1 秒
- 持续同步：间隔 ≥ 60 秒

### Q4: 支持中英混合吗？

**A**: **完全支持**。通心译 v1.3 自动识别和处理中英混合文本。

### Q5: 可以自定义处理逻辑吗？

**A**: **可以**。继承 `TongxinyiNotionBridge` 类并重写 `process_message()` 方法：

```python
class CustomBridge(TongxinyiNotionBridge):
    def process_message(self, message):
        # 您的自定义逻辑
        result = self.engine.process(message['content'])
        # ... 自定义处理
        return super().process_message(message)
```

### Q6: 数据安全吗？

**A**: **安全**。数据流向：
- 本地 → Notion API (HTTPS)
- Notion 数据库（加密存储）
- 不涉及第三方服务
- Token 仅用于 API 认证

### Q7: 可以离线使用吗？

**A**: **不能**。需要网络连接到 Notion API。

---

## 🔧 故障排查

### 错误 1: "NOTION_TOKEN 未设置"

**症状**:
```
WARNING - NOTION_TOKEN 未设置。请设置环境变量或传入参数。
```

**解决**:
```bash
# 方式 1: 设置环境变量
export NOTION_TOKEN='ntn_xxx...'

# 方式 2: 直接在代码中传入
bridge = TongxinyiNotionBridge(notion_token='ntn_xxx...', database_id='xxx...')
```

### 错误 2: "无法读取远程仓库"

**症状**:
```
ERROR - 查询数据库失败: 401 Unauthorized
```

**原因**: Token 无效或过期

**解决**:
1. 重新生成 Integration Token（见 Step 1）
2. 更新环境变量
3. 重新运行脚本

### 错误 3: "页面未找到"

**症状**:
```
ERROR - 更新页面失败: 404 Not Found
```

**原因**: Database ID 错误或权限不足

**解决**:
1. 确认数据库 ID 正确（见 Step 3）
2. 重新授予 Integration 访问权限
3. 检查 Integration 是否有 "Update content" 权限

### 错误 4: "字段不存在"

**症状**:
```
ERROR - 提取页面内容失败: KeyError: 'Content'
```

**原因**: 数据库中没有 "Content" 字段

**解决**:
1. 添加 "Content" Rich text 字段到数据库
2. 或修改脚本来适配您的字段名

### 错误 5: "请求速率限制"

**症状**:
```
ERROR - 查询数据库失败: 429 Too Many Requests
```

**原因**: API 请求过于频繁

**解决**:
```python
# 增加间隔时间
bridge.sync_continuous(interval=120)  # 改为 120 秒

# 或减少单次查询数
result = bridge.process_batch(limit=5)  # 改为 5 条
```

---

## 📈 监控和维护

### 查看日志

```bash
# 运行时实时查看日志
python _work/engines/engine/on_translate_notion_bridge.py 2>&1 | tee tongxinyi.log

# 或后台运行并保存日志
nohup python _work/engines/engine/on_translate_notion_bridge.py > tongxinyi.log 2>&1 &
```

### 检查处理情况

在 Notion 中查询已处理的消息：
1. 点击数据库的 **"Filter"**
2. 添加过滤条件: **Processed** `is` **Checked**
3. 查看已处理的消息和结果

### 性能优化

```python
# 并发处理（需要 ThreadPoolExecutor）
import concurrent.futures

def process_messages_parallel(messages, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(bridge.process_message, messages))
    return results
```

---

## 📞 技术支持

- **文档**: `docs/TONGXINYI_*.md`
- **代码**: `_work/engines/engine/on_translate_*.py`
- **日志**: 查看 stdout/stderr 输出

---

**DNA**: `#龍芯⚡️2026-05-27-TONGXINYI-NOTION-INTEGRATION-GUIDE`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

**现在您可以开始使用通心译 × Notion 集成了！🚀**
