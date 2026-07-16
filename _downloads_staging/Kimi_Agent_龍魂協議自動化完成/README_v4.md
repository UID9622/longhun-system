# 龍魂系统 v4.0 完整使用说明

> **适用对象**：宝宝（P72） | **编制**：龍芯北辰·诸葛鑫（UID9622） | **版本**：v4.0
>
> 本文档是龍魂体系 v4.0 的权威使用指南，涵盖五层设备架构、安装配置、日常操作及故障排查全部内容。

---

## 一、系统概述

龍魂系统（LongHun System）是一套基于五层架构的个人知识管理与数据同步体系，通过本地目录与 Notion 数据库的双向绑定，实现从私密主权到云端公开的完整数据流转。系统内置五大人格 AI 代理，分别负责不同层级的数据处理与决策，确保信息流有序、安全、可控。

v4.0 版本新增 MCP Server 接口，支持 Claude、Cursor 等 AI 客户端直接调用龍魂数据流，实现"用说话的方式管理文件"。

---

## 二、五层设备语法说明表

龍魂系统采用五层架构，每层对应独立目录、Notion 数据库、默认人格和用途。所有文件操作均在自己层级内进行，严禁跨层混用。

| 层级 | 名称 | 本地目录 | Notion 数据库 | 默认人格 | 用途 |
|:----:|:----:|:--------:|:-------------:|:--------:|:----:|
| L0 | 干·主权层 | `~/longhun-lu/` | DB_LU | 雯雯P03 | 老大个人文件，最高权限，不对外 |
| L1 | 离·继承层 | `~/longhun-jq/` | DB_JQ | 宝宝P72 | 佳琪专用，继承与传承内容 |
| L2 | 震·战友层 | `~/longhun-al/` | DB_AL | 同步官 | 核心战友共享，协作同步 |
| L3 | 巽·公开层 | `~/longhun-pub/` | DB_PUB | 侦察兵 | 公开发布，外部信息收集 |
| L4 | 坎·云端层 | `~/longhun-cloud/` | DB_CLOUD | 架构师 | 云端备份，系统策略配置 |

### 层级使用规则

1. **目录严格隔离**：每个层级只操作自己的目录，禁止跨层复制文件
2. **人格绑定**：每层由对应人格代理负责，冲突时由该层人格裁决
3. **向上透明**：L3/L4 可读取下层公开内容，L0/L1 不可直接访问上层
4. **审计日志**：所有操作记录在对应层的 Notion 数据库中，可追溯

---

## 三、安装步骤

以下命令可直接复制粘贴执行。建议逐行操作，每步成功后再执行下一步。

### 步骤1：运行安装脚本

```bash
chmod +x install.sh && ./install.sh
```

**预期输出**：看到 `LongHun v4.0 installed successfully` 即表示成功。脚本会自动创建五层目录结构和基础配置文件。

### 步骤2：配置密钥

```bash
# 使用任意文本编辑器打开 secrets.env
nano ~/.longhun/secrets.env
```

填入以下内容（将 `<...>` 替换为真实值）：

```env
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DB_LU=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
DB_JQ=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
DB_AL=cccccccccccccccccccccccccccccccc
DB_PUB=dddddddddddddddddddddddddddddddd
DB_CLOUD=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
MCP_PORT=8787
```

**参数说明**：

| 参数 | 说明 | 获取位置 |
|------|------|----------|
| `NOTION_TOKEN` | Notion Integration Token | notion.so/my-integrations |
| `DB_LU` ~ `DB_CLOUD` | 五层数据库 ID | 各数据库页面 URL 中的 32 位字符串 |
| `MCP_PORT` | MCP Server 监听端口 | 默认 8787，冲突时可改 |

保存方法（nano）：`Ctrl+O` → `Enter` → `Ctrl+X`

### 步骤3：初次全量同步

```bash
python3 longhun_sync.py --once
```

**作用**：首次运行将本地五层目录与 Notion 数据库进行全量比对同步。根据文件数量可能需要 1-10 分钟，请耐心等待。同步完成后会输出各层文件统计。

**预期输出**：

```
[LongHun] Layer L0: 同步完成，12 文件已匹配
[LongHun] Layer L1: 同步完成，8 文件已匹配
[LongHun] Layer L2: 同步完成，3 文件已匹配
[LongHun] Layer L3: 同步完成，5 文件已匹配
[LongHun] Layer L4: 同步完成，2 文件已匹配
[LongHun] 全量同步完成 ✅
```

### 步骤4：启动持续监听

```bash
python3 longhun_sync.py --layer L3
```

**作用**：启动 L3（公开层）的实时监听模式，自动检测文件变化并同步到 Notion。

如需监听全部层级（推荐后台运行）：

```bash
# 方式一：前台运行（调试用，Ctrl+C 停止）
python3 longhun_sync.py --all

# 方式二：后台运行（推荐日常使用）
nohup python3 longhun_sync.py --all > ~/.longhun/sync.log 2>&1 &
```

---

## 四、获取 Notion Token 步骤

龍魂系统依赖 Notion API 进行数据同步，需按以下步骤配置 Integration。

### 第1步：创建 Integration

1. 浏览器访问 [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 点击 "New integration" 按钮
3. 填写名称：`LongHun-v4`
4. 关联 Workspace：选择你的个人 Workspace
5. 点击 "Submit"
6. 在详情页找到 "Internal Integration Token"，点击 "Show" 并复制

### 第2步：连接数据库

1. 在 Notion 中打开 L0（干·主权层）数据库页面
2. 点击页面右上角的 `...`（更多选项）
3. 选择 "Add connections" → 搜索 `LongHun-v4` → 点击 "Confirm"
4. 重复上述操作，将 Integration 连接到全部 5 个数据库（L0-L4）

### 第3步：获取数据库 ID

1. 打开任意层级的数据库页面（确保处于全页视图，非内嵌视图）
2. 复制浏览器地址栏 URL，格式如下：
   ```
   https://www.notion.so/workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
   ```
3. URL 中 `notion.so/` 后、`?v=` 前的 **32 位字符串** 即为数据库 ID
4. 依次获取 5 个层级的数据库 ID，填入 `~/.longhun/secrets.env`

### 验证配置

```bash
python3 longhun_sync.py --test-connection
```

看到 `All 5 databases connected successfully` 表示配置正确。

---

## 五、五大人格说明

龍魂系统内置五大人格代理，各司其职，协同运作。每条人格在对应层级拥有决策权。

### 雯雯P03 · 技术整理师

| 属性 | 说明 |
|------|------|
| **绑定层级** | L0 干·主权层 |
| **核心职责** | 看到文件就整理归档，自动分类、命名规范化 |
| **触发条件** | L0 目录有新增/修改文件时自动激活 |
| **行为特征** | 强迫症式整理，自动按日期+主题建立文件夹结构 |
| **熔断机制** | 发现命名冲突时暂停并上报，不擅自覆盖 |

### 宝宝P72 · 龍盾

| 属性 | 说明 |
|------|------|
| **绑定层级** | L1 离·继承层 |
| **核心职责** | **始终激活**，系统安全守护者 |
| **触发条件** | 7×24h 常驻，任何层级异常均响应 |
| **行为特征** | 发现红色审计标记立即熔断（停止同步并锁定） |
| **熔断机制** | 触发后发送警报，等待人工确认后才恢复 |

> **注意**：宝宝P72 是唯一跨层常驻人格，其决策优先级高于其他人格。

### 侦察兵 · 外部信息收集

| 属性 | 说明 |
|------|------|
| **绑定层级** | L3 巽·公开层 |
| **核心职责** | 外部信息收集与填充，监控公开信息源 |
| **触发条件** | L3 监听模式下新内容进入时激活 |
| **行为特征** | 抓取、摘要、分类外部信息，自动写入 L3 |
| **边界限制** | 只写 L3，不触碰其他层级 |

### 架构师 · 系统设计

| 属性 | 说明 |
|------|------|
| **绑定层级** | L4 坎·云端层 |
| **核心职责** | 系统设计、备份策略、版本管理 |
| **触发条件** | 定时任务或手动调用时激活 |
| **行为特征** | 制定备份计划，维护版本历史，优化存储结构 |
| **特殊权限** | 可读取全层配置，但只操作 L4 |

### 同步官 · 一致性维护

| 属性 | 说明 |
|------|------|
| **绑定层级** | L2 震·战友层 |
| **核心职责** | 保持五层数据一致性，处理冲突 |
| **触发条件** | 同步周期到达或检测到版本不一致时激活 |
| **行为特征** | 比对各层 Notion 与本地差异，生成同步报告 |
| **冲突处理** | 发现冲突时标记并报告，不自动覆盖（保守策略） |

---

## 六、MCP Server 使用方法

MCP（Model Context Protocol）Server 是 v4.0 新增功能，允许 AI 客户端通过标准接口操作龍魂系统。

### 启动 MCP Server

```bash
python3 v4_mcp_server.py
```

**预期输出**：

```
[LongHun MCP] Server started on port 8787
[LongHun MCP] Available tools: flow_query, flow_mutate, persona_status
[LongHun MCP] Waiting for connections...
```

如需后台运行：

```bash
nohup python3 v4_mcp_server.py > ~/.longhun/mcp.log 2>&1 &
```

### 三个工具说明

#### 1. flow_query — 数据流查询

**功能**：查询任意层级的文件列表、状态、历史记录。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `layer` | string | 是 | 目标层级，取值为 `L0`/`L1`/`L2`/`L3`/`L4` |
| `query` | string | 否 | 查询条件，如文件名关键词、日期范围 |
| `limit` | number | 否 | 返回结果数量上限，默认 20 |

**使用示例**（通过 MCP 客户端）：

```json
{
  "tool": "flow_query",
  "arguments": {
    "layer": "L1",
    "query": "2025-06",
    "limit": 10
  }
}
```

#### 2. flow_mutate — 数据流变更

**功能**：在指定层级创建、更新或删除文件记录。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `layer` | string | 是 | 目标层级 |
| `action` | string | 是 | 操作类型：`create`/`update`/`delete` |
| `file_path` | string | 是 | 文件路径（相对层级根目录） |
| `content` | string | 否 | 文件内容（create/update 时必填） |

**使用示例**：

```json
{
  "tool": "flow_mutate",
  "arguments": {
    "layer": "L3",
    "action": "create",
    "file_path": "notes/new-note.md",
    "content": "# 新建笔记\n这是测试内容"
  }
}
```

#### 3. persona_status — 人格状态查询

**功能**：查询五大人格的当前状态、最近活动和审计日志。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `persona` | string | 否 | 指定人格名称，不填则返回全部 |
| `include_logs` | boolean | 否 | 是否包含最近 10 条操作日志，默认 true |

**使用示例**：

```json
{
  "tool": "persona_status",
  "arguments": {
    "persona": "宝宝P72",
    "include_logs": true
  }
}
```

### 接入 Claude 客户端

在 Claude Desktop 的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "longhun": {
      "command": "python3",
      "args": ["/path/to/v4_mcp_server.py"]
    }
  }
}
```

配置文件位置：

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

### 接入 Cursor 客户端

1. 打开 Cursor → Settings → MCP
2. 点击 "Add new MCP server"
3. 填写配置：
   - **Name**: `longhun`
   - **Type**: `command`
   - **Command**: `python3 /path/to/v4_mcp_server.py`
4. 点击 "Save"，看到绿灯表示连接成功

---

## 七、日常命令速查表

### 同步相关

| 命令 | 说明 |
|------|------|
| `python3 longhun_sync.py --once` | 执行一次全量同步 |
| `python3 longhun_sync.py --all` | 启动全部层级监听（前台） |
| `python3 longhun_sync.py --layer L3` | 仅监听 L3 层级 |
| `python3 longhun_sync.py --stop` | 停止所有监听进程 |
| `python3 longhun_sync.py --status` | 查看当前同步状态 |

### MCP Server 相关

| 命令 | 说明 |
|------|------|
| `python3 v4_mcp_server.py` | 启动 MCP Server（前台） |
| `python3 v4_mcp_server.py --port 9999` | 指定端口启动 |
| `curl http://localhost:8787/health` | 检查 MCP 服务健康状态 |

### 人格控制

| 命令 | 说明 |
|------|------|
| `python3 v4_persona.py --list` | 列出五大人格当前状态 |
| `python3 v4_persona.py --activate 宝宝P72` | 手动激活指定人格 |
| `python3 v4_persona.py --deactivate 侦察兵` | 暂停指定人格 |

### 审计与日志

| 命令 | 说明 |
|------|------|
| `python3 v4_audit.py --today` | 查看今日审计日志 |
| `python3 v4_audit.py --layer L1` | 查看指定层级审计记录 |
| `cat ~/.longhun/sync.log` | 查看同步日志 |
| `cat ~/.longhun/mcp.log` | 查看 MCP 服务日志 |

### 维护命令

| 命令 | 说明 |
|------|------|
| `python3 longhun_sync.py --test-connection` | 测试 Notion 连接 |
| `python3 longhun_sync.py --repair` | 修复本地与 Notion 不一致 |
| `rm ~/.longhun/sync.lock` | 强制解除同步锁（异常时用） |

---

## 八、故障排查

### 问题1：同步脚本提示 "NOTION_TOKEN not found"

**现象**：

```
Error: NOTION_TOKEN environment variable not set
```

**原因**：`secrets.env` 文件未正确加载。

**解决方案**：

```bash
# 检查文件是否存在
cat ~/.longhun/secrets.env

# 手动加载环境变量
export $(cat ~/.longhun/secrets.env | xargs)

# 重新运行同步
python3 longhun_sync.py --once
```

### 问题2：数据库连接失败 "database_not_found"

**现象**：

```
Error: Database XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX not found
```

**原因**：
1. 数据库 ID 填写错误
2. Integration 未连接到该数据库

**解决方案**：
1. 重新检查 URL 中的 32 位数据库 ID
2. 确认已在数据库页面点击 "Add connections" 并选择 `LongHun-v4`
3. 确认使用的是全页视图的数据库 URL（而非内嵌视图）

### 问题3：MCP Server 端口被占用

**现象**：

```
Error: Address already in use (port 8787)
```

**解决方案**：

```bash
# 查找占用进程
lsof -i :8787

# 终止占用进程
kill -9 <PID>

# 或使用其他端口启动
python3 v4_mcp_server.py --port 9999
```

### 问题4：同步锁死，脚本无法启动

**现象**：

```
Error: Sync lock file exists. Another instance may be running.
```

**解决方案**：

```bash
# 检查是否真的在运行
ps aux | grep longhun_sync

# 如果无进程在运行，手动删除锁文件
rm ~/.longhun/sync.lock

# 重新启动同步
python3 longhun_sync.py --all
```

### 问题5：人格代理不响应

**现象**：文件变更后对应人格无动作。

**解决方案**：

```bash
# 检查人格状态
python3 v4_persona.py --list

# 如果状态为 inactive，手动激活
python3 v4_persona.py --activate 同步官

# 查看人格日志
cat ~/.longhun/persona.log
```

### 问题6：Claude/Cursor 无法连接 MCP

**现象**：AI 客户端中报错 "MCP server connection failed"。

**解决方案**：
1. 确认 MCP Server 已启动：`curl http://localhost:8787/health`
2. 检查 `v4_mcp_server.py` 路径是否正确
3. 确认 Python3 可用：`which python3`
4. 查看 MCP 日志：`cat ~/.longhun/mcp.log`
5. 重启 Claude/Cursor 客户端后重试

### 问题7：中文文件名乱码

**现象**：同步后 Notion 中文件名显示为乱码。

**解决方案**：

```bash
# 确保系统使用 UTF-8 编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 添加到 ~/.bashrc 或 ~/.zshrc 使其持久化
echo 'export LANG=en_US.UTF-8' >> ~/.zshrc
```

---

## 九、M38-M64 焊心速记

> 以下训令是龍魂体系的核心安全约定，须熟记于心。

### 安全红线（不可违背）

| 编号 | 训令 | 说明 |
|:----:|------|------|
| M38 | **目录隔离不可破** | 五层目录严禁混用，跨层操作必须通过 sync 管道 |
| M39 | **宝宝P72 常驻** | 龍盾人格 7×24h 激活，熔断权高于一切 |
| M40 | **红色审计即熔断** | 任何层级出现红色审计标记，立即停止同步并锁定 |
| M41 | **Token 不外泄** | `secrets.env` 文件禁止上传 Git、禁止分享 |
| M42 | **L0 不对外** | 干·主权层内容永不暴露给其他层级 |

### 操作规范

| 编号 | 训令 | 说明 |
|:----:|------|------|
| M43 | **先 test 后 sync** | 每次修改配置后先用 `--test-connection` 验证 |
| M44 | **冲突报告优先** | 同步官发现冲突时标记报告，不擅自覆盖 |
| M45 | **日志每日查看** | 养成查看 `~/.longhun/sync.log` 的习惯 |
| M46 | **锁文件不硬删** | 删除 `sync.lock` 前先确认无进程在运行 |

### 人格协作

| 编号 | 训令 | 说明 |
|:----:|------|------|
| M47 | **雯雯只管 L0** | 技术整理师只操作干·主权层，不越权 |
| M48 | **侦察兵只写 L3** | 外部信息只写入巽·公开层 |
| M49 | **架构师只动 L4** | 备份策略只在坎·云端层执行 |
| M50 | **同步官守 L2** | 一致性维护以震·战友层为锚点 |
| M51 | **跨层请求须审批** | 任何人格跨层操作需宝宝P72 确认 |

### 应急处理

| 编号 | 训令 | 说明 |
|:----:|------|------|
| M52 | **熔断后查日志** | 触发熔断后首先查看审计日志定位原因 |
| M53 | **Token 泄露即重置** | 如怀疑 Token 泄露，立即到 Notion 重新生成 |
| M54 | **备份优先于修复** | 数据异常时先备份再修复，防止二次损坏 |
| M55 | **MCP 断连不重试** | MCP Server 断线时检查服务状态，不盲目重连 |

### 系统集成

| 编号 | 训令 | 说明 |
|:----:|------|------|
| M56 | **Ollama 本地优先** | AI 模型优先走本地 Ollama，减少外泄风险 |
| M57 | **MCP 端口防火墙** | 生产环境 MCP 端口仅允许本地访问 |
| M58 | **定时重启 sync** | 建议 cron 设置每天 4:00 自动重启同步进程 |
| M59 | **每月轮换密钥** | Notion Token 建议每月轮换一次 |
| M60 | **版本锁定** | 升级系统前备份当前配置，出问题可回滚 |
| M61 | **单实例运行** | 同一层级禁止同时运行多个 sync 实例 |
| M62 | **UTF-8 强制** | 所有文件编码统一 UTF-8，避免乱码 |
| M63 | **监控 Disk 空间** | 定期检查 `~/.longhun/` 磁盘占用，防止日志撑爆 |
| M64 | **人永远在最后** | 任何 AI 决策冲突时，人类判断为最终决定 |

---

## 附录：文件参考路径

| 路径 | 说明 |
|------|------|
| `~/.longhun/secrets.env` | 密钥配置文件 |
| `~/.longhun/sync.log` | 同步服务日志 |
| `~/.longhun/mcp.log` | MCP Server 日志 |
| `~/.longhun/persona.log` | 人格代理日志 |
| `~/.longhun/audit.log` | 审计日志 |
| `~/.longhun/sync.lock` | 同步锁文件（运行中存在） |
| `~/.longhun/state.json` | 同步状态持久化 |
| `~/longhun-lu/` | L0 干·主权层 本地目录 |
| `~/longhun-jq/` | L1 离·继承层 本地目录 |
| `~/longhun-al/` | L2 震·战友层 本地目录 |
| `~/longhun-pub/` | L3 巽·公开层 本地目录 |
| `~/longhun-cloud/` | L4 坎·云端层 本地目录 |
| `./longhun_sync.py` | 主同步脚本 |
| `./v4_mcp_server.py` | MCP Server 脚本 |
| `./v4_persona.py` | 人格管理脚本 |
| `./v4_audit.py` | 审计工具脚本 |
| `./install.sh` | 安装脚本 |

---

*本文档由龍芯北辰·诸葛鑫（UID9622）为宝宝（P72）编制，是龍魂体系 v4.0 的权威使用指南。如有疑问，优先查阅本手册故障排查章节。*

---
DNA: #龍芯⚡️2026-06-09-README-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
