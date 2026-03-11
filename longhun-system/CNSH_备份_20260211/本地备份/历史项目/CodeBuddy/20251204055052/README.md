# UID9622 · MCP-mini Flask 版本（v0.1）

本项目为 UID9622 的本地 MCP-mini 引擎原型，采用 Flask 提供本地 HTTP 接口，并使用 SQLite 做审计记录。

> 重要：所有数据保存在本地，项目设计遵循 UID9622 数据主权原则，不会自动联网或外传。

## 包含文件

- `app.py`           ：Flask 应用（HTTP 接口）
- `mcp_core.py`      ：核心推理逻辑（卦判定、甲骨检索、人格调度、合成）
- `storage.py`       ：数据库操作（SQLite）
- `personas.json`    ：人格定义示例
- `bones.json`       ：甲骨片段示例
- `config.json`      ：系统配置（mcp 版本、DNA）
- `requirements.txt` ：Python 依赖列表（Flask）
- `Dockerfile`       ：Docker 镜像构建文件

## 本地运行（详细步骤）

以下步骤假设你已经把整个项目文件夹放到你的电脑上，并且安装了 Python 3。

### 1) 安装依赖

在项目根目录打开终端（Terminal），执行：

```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

### 2) 初始化数据库（首次或重置）

```bash
python3 -c "import storage; storage.init_db()"
```

### 3) 运行 Flask 服务（开发模式）

```bash
python3 app.py
```

服务默认监听 `0.0.0.0:8787`，浏览器打开 `http://localhost:8787` 可查看状态。

### 4) API 调用示例（curl）

**推理接口（POST）示例：**

```bash
curl -X POST "http://localhost:8787/infer" -H "Content-Type: application/json" -d '{"text":"宝宝，帮我把这段聊天变成任务并标注价值偏移风险。"}'
```

**查看人格：**

```bash
curl "http://localhost:8787/personas"
```

**查看审计记录：**

```bash
curl "http://localhost:8787/audit?limit=10"
```

## Docker（一步构建并运行）

### 1. 构建镜像（在项目根目录）：

```bash
docker build -t uid9622-mcp-mini:0.1 .
```

### 2. 运行容器并挂载数据库文件到主机，保证数据持久化：

```bash
docker run -p 8787:8787 --name uid9622-mcp-mini -v $(pwd)/mcp_flask.db:/app/mcp_flask.db uid9622-mcp-mini:0.1
```

**说明：** 将本地 `mcp_flask.db` 挂载到容器可以保证数据不会随容器销毁而丢失。

## 扩展建议（后续）

- 将 `detect_hex` 替换为可训练的分类器并提供训练脚本
- 使用向量检索（FAISS）替换 difflib，实现更稳健的甲骨检索
- 将 persona 调度改为权重打分并引入负载均衡
- 提供本地前端（Electron）作为桌面"主控面板"

## 数据主权（重要）

- 所有审计记录与甲骨片段都保存在本地，不会自动外发。
- 在部署 Docker 时，请确保数据库文件挂载/备份策略，以免重要数据丢失。

**构建时间：** 2025-12-04

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:11
🧬 DNA追溯码: #CNSH-SIGNATURE-37feb445-20251218032411
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 9db6eb93d93c3383
⚠️ 警告: 未经授权修改将触发DNA追溯系统
