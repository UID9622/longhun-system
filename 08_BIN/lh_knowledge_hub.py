# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-1d00dc60
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·统一知识库引擎 v2.0 — 多源知识底座管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途: 统一管理龍魂体系所有外部知识底座（飞书/Python/FastAPI/Ollama等）
架构: 通用抓取框架 + 可配置知识域 + 自建核心知识卡
存储: /opt/longhun/data/knowledge/{domain}/
更新: systemd timer 统一调度

DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-KNOWLEDGE-HUB-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import sys
import json
import time
import hashlib
import argparse
import urllib.request
import urllib.error
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ─── 全局配置 ──────────────────────────────────────────────────
KB_BASE = Path("/opt/longhun/data/knowledge")
LOCAL_KB_BASE = Path(os.environ.get("HOME", "/tmp")) / "longhun-system/data/knowledge"
VERSION_FILE = "kb_version.json"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
USER_AGENT = "LongHun-Knowledge-Hub/2.0 (UID9622; +https://uid9622.cn)"
FETCH_INTERVAL_HOURS = 6

# ──────────────────────────────────────────────────────────────
# 知识域定义（配置即可扩展）
# ──────────────────────────────────────────────────────────────

DOMAIN_CONFIGS: Dict[str, Dict] = {}

# ═══════════════════════════════════════════════════════════════
# 域1: 飞书开放平台
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["feishu"] = {
    "name": "飞书开放平台",
    "emoji": "🪶",
    "sources": [
        {"id": "oapi-sdk-readme", "name": "Python SDK README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/README.md",
         "file": "oapi-sdk-readme.md", "priority": 10},
        {"id": "oapi-sdk-channel", "name": "Channel SDK 文档", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel.md",
         "file": "oapi-sdk-channel.md", "priority": 10},
        {"id": "oapi-sdk-channel-quickstart", "name": "Channel 快速开始", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/quickstart.md",
         "file": "oapi-sdk-channel-quickstart.md", "priority": 9},
        {"id": "oapi-sdk-channel-reference", "name": "Channel API 参考", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/reference.md",
         "file": "oapi-sdk-channel-reference.md", "priority": 10},
        {"id": "oapi-sdk-dedup", "name": "去重架构", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/larksuite/oapi-sdk-python/v2_main/doc/channel/dedup-architecture.md",
         "file": "oapi-sdk-dedup.md", "priority": 8},
        {"id": "guide-bot-dev", "name": "腾讯云: 飞书机器人全流程", "type": "web_article",
         "url": "https://cloud.tencent.com/developer/article/2670675",
         "file": "guide-bot-dev-full.md", "priority": 7},
        {"id": "guide-agent-feishu", "name": "腾讯云: Agent接入飞书", "type": "web_article",
         "url": "https://cloud.tencent.com/developer/article/2655926",
         "file": "guide-agent-feishu.md", "priority": 7},
        {"id": "guide-bot-faq", "name": "飞书开发FAQ", "type": "web_article",
         "url": "https://open.feishu.cn/document/develop-an-echo-bot/faq",
         "file": "guide-bot-faq.md", "priority": 8},
        {"id": "card-im-csdn", "name": "CSDN: 飞书IM消息与卡片详解", "type": "web_article",
         "url": "https://blog.csdn.net/csdn122345/article/details/160534404",
         "file": "feishu-card-im-csdn.md", "priority": 8},
    ],
    "core_cards": {}  # feishu 核心卡已在 v1 中内置，此处留空避免重复
}

# ═══════════════════════════════════════════════════════════════
# 域2: Python 3
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["python"] = {
    "name": "Python 3",
    "emoji": "🐍",
    "sources": [
        {"id": "cpython-readme", "name": "CPython README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/python/cpython/main/README.rst",
         "file": "cpython-readme.rst", "priority": 10},
        {"id": "devguide-readme", "name": "Python 开发指南", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/python/devguide/main/README.rst",
         "file": "devguide-readme.rst", "priority": 9},
        {"id": "pep-0008", "name": "PEP 8 代码风格", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0008.rst",
         "file": "pep-0008-style-guide.rst", "priority": 10},
        {"id": "pep-0484", "name": "PEP 484 类型提示", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0484.rst",
         "file": "pep-0484-type-hints.rst", "priority": 10},
        {"id": "pep-0594", "name": "PEP 594 废弃模块", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/python/peps/main/peps/pep-0594.rst",
         "file": "pep-0594-deprecations.rst", "priority": 7},
    ],
    "core_cards": {
        "python-asyncio-guide.md": "_CORE_PYTHON_ASYNCIO",
        "python-pathlib-guide.md": "_CORE_PYTHON_PATHLIB",
        "python-subprocess-guide.md": "_CORE_PYTHON_SUBPROCESS",
        "python-typing-cheatsheet.md": "_CORE_PYTHON_TYPING",
        "python-common-patterns.md": "_CORE_PYTHON_PATTERNS",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域3: FastAPI
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["fastapi"] = {
    "name": "FastAPI",
    "emoji": "⚡",
    "sources": [
        {"id": "fastapi-readme", "name": "FastAPI README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/README.md",
         "file": "fastapi-readme.md", "priority": 10},
        {"id": "fastapi-first-steps", "name": "FastAPI 入门教程", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/first-steps.md",
         "file": "tutorial-first-steps.md", "priority": 10},
        {"id": "fastapi-path-params", "name": "路径参数", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params.md",
         "file": "tutorial-path-params.md", "priority": 9},
        {"id": "fastapi-query-params", "name": "查询参数", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params.md",
         "file": "tutorial-query-params.md", "priority": 9},
        {"id": "fastapi-request-body", "name": "请求体", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body.md",
         "file": "tutorial-body.md", "priority": 9},
        {"id": "fastapi-middleware", "name": "中间件", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/middleware.md",
         "file": "tutorial-middleware.md", "priority": 8},
        {"id": "fastapi-cors", "name": "CORS 配置", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/cors.md",
         "file": "tutorial-cors.md", "priority": 8},
        {"id": "fastapi-background", "name": "后台任务", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/background-tasks.md",
         "file": "tutorial-background-tasks.md", "priority": 7},
        {"id": "fastapi-websockets", "name": "WebSocket", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/websockets.md",
         "file": "advanced-websockets.md", "priority": 8},
    ],
    "core_cards": {
        "fastapi-best-practices.md": "_CORE_FASTAPI_BEST",
        "fastapi-error-handling.md": "_CORE_FASTAPI_ERRORS",
        "fastapi-deployment.md": "_CORE_FASTAPI_DEPLOY",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域4: Ollama
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["ollama"] = {
    "name": "Ollama",
    "emoji": "🦙",
    "sources": [
        {"id": "ollama-readme", "name": "Ollama README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/README.md",
         "file": "ollama-readme.md", "priority": 10},
        {"id": "ollama-api", "name": "Ollama API 文档", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/api.md",
         "file": "api-reference.md", "priority": 10},
        {"id": "ollama-modelfile", "name": "Modelfile 参考", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/modelfile.mdx",
         "file": "modelfile-reference.mdx", "priority": 10},
        {"id": "ollama-import", "name": "模型导入指南", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/import.mdx",
         "file": "import-guide.mdx", "priority": 9},
        {"id": "ollama-faq", "name": "常见问题", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/faq.mdx",
         "file": "faq.mdx", "priority": 9},
        {"id": "ollama-linux", "name": "Linux 安装指南", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/linux.mdx",
         "file": "linux-guide.mdx", "priority": 8},
        {"id": "ollama-quickstart", "name": "快速开始", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/quickstart.mdx",
         "file": "quickstart.mdx", "priority": 9},
        {"id": "ollama-troubleshooting", "name": "故障排除", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/ollama/ollama/main/docs/troubleshooting.mdx",
         "file": "troubleshooting.mdx", "priority": 8},
    ],
    "core_cards": {
        "ollama-commands-cheatsheet.md": "_CORE_OLLAMA_COMMANDS",
        "ollama-model-tuning.md": "_CORE_OLLAMA_TUNING",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域5: Pydantic v2
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["pydantic"] = {
    "name": "Pydantic v2",
    "emoji": "📐",
    "sources": [
        {"id": "pydantic-readme", "name": "Pydantic README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/pydantic/pydantic/main/README.md",
         "file": "pydantic-readme.md", "priority": 10},
        {"id": "pydantic-settings-readme", "name": "Pydantic Settings README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/pydantic/pydantic-settings/main/README.md",
         "file": "pydantic-settings-readme.md", "priority": 9},
    ],
    "core_cards": {
        "pydantic-v2-cheatsheet.md": "_CORE_PYDANTIC_V2",
        "pydantic-settings-guide.md": "_CORE_PYDANTIC_SETTINGS",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域6: Docker
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["docker"] = {
    "name": "Docker",
    "emoji": "🐳",
    "sources": [
        {"id": "docker-compose-spec", "name": "Compose 规范", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/compose-spec/compose-spec/master/spec.md",
         "file": "compose-spec.md", "priority": 10},
        {"id": "docker-python-guide", "name": "Docker Python 最佳实践", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/docker/awesome-compose/master/README.md",
         "file": "awesome-compose-readme.md", "priority": 8},
    ],
    "core_cards": {
        "dockerfile-best-practices.md": "_CORE_DOCKERFILE",
        "docker-compose-guide.md": "_CORE_DOCKER_COMPOSE",
        "docker-commands-cheatsheet.md": "_CORE_DOCKER_COMMANDS",
        "docker-python-deploy.md": "_CORE_DOCKER_PYTHON",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域7: Git
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["git"] = {
    "name": "Git",
    "emoji": "🔀",
    "sources": [
        {"id": "git-scm-book", "name": "Pro Git Book (简中)", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/progit/progit2-zh/master/README.asc",
         "file": "progit-readme.asc", "priority": 9},
    ],
    "core_cards": {
        "git-commands-cheatsheet.md": "_CORE_GIT_COMMANDS",
        "git-workflow-guide.md": "_CORE_GIT_WORKFLOW",
        "git-troubleshooting.md": "_CORE_GIT_TROUBLESHOOT",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域8: systemd
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["systemd"] = {
    "name": "systemd",
    "emoji": "⚙️",
    "sources": [
        {"id": "systemd-service-man", "name": "systemd.service 手册", "type": "web_article",
         "url": "https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html",
         "file": "systemd-service-manual.html", "priority": 10},
        {"id": "systemd-timer-man", "name": "systemd.timer 手册", "type": "web_article",
         "url": "https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html",
         "file": "systemd-timer-manual.html", "priority": 10},
    ],
    "core_cards": {
        "systemd-service-guide.md": "_CORE_SYSTEMD_SERVICE",
        "systemd-timer-guide.md": "_CORE_SYSTEMD_TIMER",
        "systemd-troubleshooting.md": "_CORE_SYSTEMD_TROUBLESHOOT",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域9: Nginx
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["nginx"] = {
    "name": "Nginx",
    "emoji": "🌐",
    "sources": [
        {"id": "nginx-beginners-guide", "name": "Nginx 入门指南", "type": "web_article",
         "url": "https://nginx.org/en/docs/beginners_guide.html",
         "file": "beginners-guide.html", "priority": 10},
    ],
    "core_cards": {
        "nginx-config-guide.md": "_CORE_NGINX_CONFIG",
        "nginx-reverse-proxy.md": "_CORE_NGINX_PROXY",
        "nginx-ssl-guide.md": "_CORE_NGINX_SSL",
        "nginx-performance.md": "_CORE_NGINX_PERF",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域10: CloudBase / 腾讯云开发
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["cloudbase"] = {
    "name": "CloudBase",
    "emoji": "☁️",
    "sources": [],
    "core_cards": {
        "cloudbase-auth-guide.md": "_CORE_CLOUDBASE_AUTH",
        "cloudbase-database-guide.md": "_CORE_CLOUDBASE_DATABASE",
        "cloudbase-cloudfunc-guide.md": "_CORE_CLOUDBASE_FUNC",
        "cloudbase-deploy-guide.md": "_CORE_CLOUDBASE_DEPLOY",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域11: Redis
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["redis"] = {
    "name": "Redis",
    "emoji": "🗄️",
    "sources": [],
    "core_cards": {
        "redis-commands-cheatsheet.md": "_CORE_REDIS_COMMANDS",
        "redis-python-guide.md": "_CORE_REDIS_PYTHON",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域12: SQLAlchemy
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["sqlalchemy"] = {
    "name": "SQLAlchemy 2.0",
    "emoji": "🗃️",
    "sources": [
        {"id": "sqlalchemy-readme", "name": "SQLAlchemy README", "type": "github_raw",
         "url": "https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/main/README.rst",
         "file": "sqlalchemy-readme.rst", "priority": 10},
    ],
    "core_cards": {
        "sqlalchemy-2-cheatsheet.md": "_CORE_SQLALCHEMY_2",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域13: httpx
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["httpx"] = {
    "name": "httpx",
    "emoji": "🌐",
    "sources": [],
    "core_cards": {
        "httpx-cheatsheet.md": "_CORE_HTTPX",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域14: Alembic
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["alembic"] = {
    "name": "Alembic",
    "emoji": "🗄️",
    "sources": [],
    "core_cards": {
        "alembic-cheatsheet.md": "_CORE_ALEMBIC",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域15: Pytest
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["pytest"] = {
    "name": "Pytest",
    "emoji": "🧪",
    "sources": [],
    "core_cards": {
        "pytest-cheatsheet.md": "_CORE_PYTEST",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域16: Loguru
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["loguru"] = {
    "name": "Loguru",
    "emoji": "📝",
    "sources": [],
    "core_cards": {
        "loguru-cheatsheet.md": "_CORE_LOGURU",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域17: Starlette
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["starlette"] = {
    "name": "Starlette",
    "emoji": "⚡",
    "sources": [],
    "core_cards": {
        "starlette-cheatsheet.md": "_CORE_STARLETTE",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域18: PostgreSQL
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["postgresql"] = {
    "name": "PostgreSQL",
    "emoji": "🐘",
    "sources": [],
    "core_cards": {
        "postgresql-cheatsheet.md": "_CORE_POSTGRESQL",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域19: Prometheus
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["prometheus"] = {
    "name": "Prometheus",
    "emoji": "📊",
    "sources": [],
    "core_cards": {
        "prometheus-cheatsheet.md": "_CORE_PROMETHEUS",
    }
}

# ═══════════════════════════════════════════════════════════════
# 域20: 国密（Guomi）
# ═══════════════════════════════════════════════════════════════
DOMAIN_CONFIGS["guomi"] = {
    "name": "国密算法",
    "emoji": "🔐",
    "sources": [],
    "core_cards": {
        "guomi-cheatsheet.md": "_CORE_GUOMI",
    }
}


# ═══════════════════════════════════════════════════════════════
# 核心知识卡内容（精简+实战导向）
# ═══════════════════════════════════════════════════════════════

_CORE_PYTHON_ASYNCIO = """---
title: Python asyncio 异步编程完整指南
domain: python
category: core
priority: 10
created: 2026-08-05
---

# Python asyncio 异步编程

## 核心概念

| 概念 | 说明 |
|:---|:---|
| coroutine | async def 定义的函数，返回 coroutine 对象 |
| task | 被事件循环调度的 coroutine，asyncio.create_task() 创建 |
| event loop | 事件循环，调度和执行异步任务的核心 |
| await | 等待一个 awaitable 对象完成 |
| Future | 低层级 awaitable，表示一个异步操作的最终结果 |

## 基本用法

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())
```

## 并发运行

```python
async def fetch(url):
    # 模拟网络请求
    await asyncio.sleep(1)
    return f"data from {url}"

async def main():
    # 并发执行多个任务
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(results)  # ['data from url1', 'data from url2', 'data from url3']

    # 谁先完成先处理谁
    for coro in asyncio.as_completed([fetch("a"), fetch("b")]):
        result = await coro
        print(result)
```

## Task 管理

```python
async def main():
    task = asyncio.create_task(some_coro())
    # task 立即被调度执行

    # 取消任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled")

    # 超时
    try:
        result = await asyncio.wait_for(long_task(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Timeout!")
```

## FastAPI 中使用

```python
@app.get("/data")
async def get_data():
    # FastAPI 自动处理事件循环
    result = await some_async_db_query()
    return {"data": result}

@app.post("/batch")
async def batch_process(items: list[str]):
    # 并发处理多个项目
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {"results": results}
```

## 常见陷阱

1. **不要在 async 函数中调用 time.sleep()** → 用 `await asyncio.sleep()`
2. **不要在 async 函数中做 CPU 密集计算** → 用 `loop.run_in_executor()`
3. **asyncio.create_task() 后要保存引用** → 否则可能被 GC 回收
4. **异常默认静默** → 使用 `gather(return_exceptions=True)` 捕获
5. **文件 I/O 不是异步的** → 用 `aiofiles` 或 `run_in_executor`
"""

_CORE_PYTHON_PATHLIB = """---
title: Python pathlib 路径操作完全指南
domain: python
category: core
priority: 10
---

# pathlib 路径操作

## 为什么用 pathlib

- 跨平台（自动处理 `/` 和 `\\`）
- 面向对象，链式调用
- os.path 的现代替代品

## 基本操作

```python
from pathlib import Path

# 创建路径
p = Path("/opt/longhun/data/knowledge")
home = Path.home()           # /Users/xxx
cwd = Path.cwd()             # 当前工作目录

# 拼接
config = p / "config" / "settings.json"

# 属性
p.name          # "knowledge"
p.stem          # "knowledge"（无后缀）
p.suffix        # ""（无后缀）
p.parent        # Path("/opt/longhun/data")
p.parts         # ('/', 'opt', 'longhun', 'data', 'knowledge')
p.anchor        # "/"

# 判断
p.exists()
p.is_dir()
p.is_file()
p.is_symlink()

# 遍历
for f in p.glob("*.json"):        # 不递归
    ...
for f in p.rglob("**/*.py"):      # 递归
    ...

# 创建/删除
p.mkdir(parents=True, exist_ok=True)
p.unlink(missing_ok=True)          # 删除文件
```

## 读写

```python
# 读写文本
text = p.read_text(encoding="utf-8")
p.write_text("content", encoding="utf-8")

# 读写二进制
data = p.read_bytes()
p.write_bytes(data)

# 逐行读取
with p.open("r", encoding="utf-8") as f:
    for line in f:
        ...
```

## 常用模式

```python
# 确保目录存在
save_dir = Path("/opt/data/output")
save_dir.mkdir(parents=True, exist_ok=True)
(save_dir / "result.json").write_text(data)

# 批量重命名
for f in Path(".").glob("*.txt"):
    f.rename(f.with_suffix(".md"))

# 找最新文件
latest = max(Path("logs").glob("*.log"), key=lambda p: p.stat().st_mtime)
```
"""

_CORE_PYTHON_SUBPROCESS = """---
title: Python subprocess 安全执行外部命令
domain: python
category: core
priority: 10
---

# subprocess 安全使用指南

## subprocess.run() （推荐）

```python
import subprocess

# 基本用法
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)

# 超时
result = subprocess.run(["sleep", "10"], timeout=5)  # 抛出 TimeoutExpired

# 环境变量
result = subprocess.run(["myapp"], env={"PATH": "/usr/bin", **os.environ})

# 工作目录
result = subprocess.run(["git", "status"], cwd="/path/to/repo")

# 输入管道
result = subprocess.run(["python3"], input="print(1+1)", text=True, capture_output=True)
```

## 安全铁律

```python
# ❌ 危险：shell=True + 用户输入
subprocess.run(f"rm -rf {user_path}", shell=True)  # 命令注入漏洞！

# ✅ 安全：列表参数 + shell=False（默认）
subprocess.run(["rm", "-rf", user_path])

# ✅ 如果必须用 shell=True，用 shlex.quote
import shlex
subprocess.run(f"grep {shlex.quote(user_input)} file.txt", shell=True)
```

## 管道和重定向

```python
# stdout 到文件
with open("output.txt", "w") as f:
    subprocess.run(["ls", "-la"], stdout=f)

# stderr 到 stdout
result = subprocess.run(["cmd"], stderr=subprocess.STDOUT, capture_output=True, text=True)

# 管道连接两个命令
p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "py"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
p1.stdout.close()
output = p2.communicate()[0]
```

## 异常处理模板

```python
try:
    result = subprocess.run(
        ["some_command"],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,  # 非零退出码抛 CalledProcessError
    )
    return result.stdout.strip()
except subprocess.TimeoutExpired:
    print("命令超时")
    return None
except subprocess.CalledProcessError as e:
    print(f"命令失败: {e.stderr}")
    return None
except FileNotFoundError:
    print("命令不存在")
    return None
```
"""

_CORE_PYTHON_TYPING = """---
title: Python 类型提示速查表（≥3.10）
domain: python
category: core
priority: 10
---

# Python 类型提示速查

## 基础类型

```python
name: str = "hello"
count: int = 42
price: float = 9.99
active: bool = True
data: bytes = b"hello"
nothing: None = None
anything: Any = "whatever"
```

## 容器类型（3.9+ 用小写）

```python
names: list[str] = ["a", "b"]
pairs: tuple[int, str] = (1, "one")
scores: dict[str, float] = {"math": 95.5}
ids: set[int] = {1, 2, 3}
queue: list[int] = []

# 可选
from typing import Optional  # 3.10+ 用 X | None
name: str | None = None       # 等价于 Optional[str]

# 联合
value: str | int = "hello"    # 等价于 Union[str, int]
```

## 函数签名

```python
from typing import Callable, Any

def process(
    items: list[str],
    timeout: float = 30.0,
    callback: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    ...

# 异步函数
async def fetch(url: str) -> dict:
    ...
```

## TypedDict / NamedTuple / dataclass

```python
from typing import TypedDict, NamedTuple
from dataclasses import dataclass

# TypedDict（JSON友好）
class UserDict(TypedDict):
    name: str
    age: int
    email: str | None

# NamedTuple（不可变）
class Point(NamedTuple):
    x: float
    y: float

# dataclass（可变，功能多）
@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
```

## Pydantic v2 常用

```python
from pydantic import BaseModel, Field
from typing import Annotated  # 3.9+

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(gt=0)
    tags: list[str] = []
    metadata: dict[str, Any] | None = None

# 运行时验证
item = Item(name="Widget", price=19.99)
print(item.model_dump())  # {'name': 'Widget', 'price': 19.99, 'tags': []}
```

## Any vs object

```python
# Any: 关闭类型检查，可以赋值给任何类型
x: Any = get_dynamic_value()
y: str = x  # OK

# object: 需要显式转换
x: object = get_dynamic_value()
y: str = x  # ❌ 类型错误
y: str = x  # type: ignore  # 显式忽略
```
"""

_CORE_PYTHON_PATTERNS = """---
title: Python 常见开发模式速查
domain: python
category: core
priority: 9
---

# Python 常见模式

## 单例模式

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config.load()
```

## 上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def temporary_file(path: str):
    p = Path(path)
    p.touch()
    try:
        yield p
    finally:
        p.unlink()

# 使用
with temporary_file("/tmp/test.txt") as f:
    f.write_text("data")
```

## 装饰器模式

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator
```

## 缓存模式

```python
from functools import lru_cache, cache
import time

@lru_cache(maxsize=128)
def expensive_computation(x: int) -> int:
    time.sleep(1)
    return x * x

# 3.9+ 无限缓存
@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

## 数据类工厂

```python
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    host: str = "0.0.0.0"
    port: int = 8080
    cors_origins: list[str] = field(default_factory=lambda: ["*"])
    _secrets: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8080")),
        )
```

## 日志最佳实践

```python
import logging

# 模块级别 logger
logger = logging.getLogger(__name__)

# 结构化日志
logger.info("user_login", extra={"user_id": uid, "ip": ip})

# 异常日志
try:
    risky_operation()
except Exception:
    logger.exception("operation_failed")  # 自动附 traceback

# 敏感字段脱敏
def log_safe(data: dict) -> dict:
    safe = data.copy()
    for key in ("password", "token", "secret"):
        if key in safe:
            safe[key] = "***MELTDOWN***"
    return safe
```
"""

# ─── FastAPI 核心知识卡 ───

_CORE_FASTAPI_BEST = """---
title: FastAPI 最佳实践与项目结构
domain: fastapi
category: core
priority: 10
---

# FastAPI 最佳实践

## 推荐项目结构

```
app/
├── main.py              # FastAPI 应用入口
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py    # 版本化路由
│   │   ├── users.py     # 用户相关端点
│   │   └── items.py     # 物品相关端点
├── models/
│   ├── __init__.py
│   ├── domain.py        # Pydantic 模型（请求/响应）
│   └── database.py      # SQLAlchemy 模型
├── services/
│   ├── __init__.py
│   └── user_service.py  # 业务逻辑
├── core/
│   ├── __init__.py
│   ├── config.py        # 配置（pydantic-settings）
│   ├── security.py      # 认证授权
│   └── database.py      # 数据库连接
└── tests/
```

## 依赖注入模式

```python
from fastapi import Depends

# 数据库会话
async def get_db():
    async with SessionLocal() as session:
        yield session

# 当前用户
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> User:
    user = await authenticate(token, db)
    if not user:
        raise HTTPException(401)
    return user

# 组合依赖
@app.get("/me")
async def me(
    user: User = Depends(get_current_user),
    db = Depends(get_db),
):
    return user

# 权限检查
def require_role(role: str):
    async def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403)
        return user
    return checker
```

## 响应模型

```python
# 统一响应格式
class APIResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None

@app.get("/users/{user_id}", response_model=APIResponse[UserOut])
async def get_user(user_id: int):
    user = await find_user(user_id)
    return APIResponse(data=user)

# 排除敏感字段
class UserOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)  # ORM 兼容
    # password 不在模型中，自动排除
```
"""

_CORE_FASTAPI_ERRORS = """---
title: FastAPI 错误处理与异常
domain: fastapi
category: core
priority: 9
---

# FastAPI 错误处理

## 全局异常处理器

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_error", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Internal server error"},
    )
```

## 常见 HTTPException

```python
# 404
raise HTTPException(status_code=404, detail="User not found")

# 400
raise HTTPException(status_code=400, detail=f"Invalid email: {email}")

# 401
raise HTTPException(
    status_code=401,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# 422（Pydantic 验证失败，FastAPI 自动处理）
# 429
raise HTTPException(status_code=429, detail="Too many requests")
```

## 请求验证自定义

```python
from pydantic import field_validator

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()
```
"""

_CORE_FASTAPI_DEPLOY = """---
title: FastAPI 生产部署指南
domain: fastapi
category: core
priority: 9
---

# FastAPI 生产部署

## Uvicorn 生产配置

```bash
uvicorn app.main:app \\
  --host 0.0.0.0 \\
  --port 8000 \\
  --workers 4 \\
  --log-level info \\
  --proxy-headers \\
  --forwarded-allow-ips '*'
```

## systemd 配置

```ini
[Unit]
Description=FastAPI App
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/app
ExecStart=/opt/app/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5
EnvironmentFile=/opt/app/.env

[Install]
WantedBy=multi-user.target
```

## Nginx 反向代理

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

## 环境变量管理

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    secret_key: str
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```
"""

# ─── Ollama 核心知识卡 ───

_CORE_OLLAMA_COMMANDS = """---
title: Ollama 命令速查表
domain: ollama
category: core
priority: 10
---

# Ollama 命令速查表

## 模型管理

```bash
# 拉取模型
ollama pull qwen2.5:7b
ollama pull deepseek-r1:7b
ollama pull llama3.1:8b

# 列出本地模型
ollama list

# 查看模型详情
ollama show qwen2.5:7b

# 删除模型
ollama rm qwen2.5:7b

# 复制模型
ollama cp source-model new-name

# 创建自定义模型（从 Modelfile）
ollama create my-model -f Modelfile
```

## 运行

```bash
# 交互式运行
ollama run qwen2.5:7b

# 单次推理
ollama run qwen2.5:7b "你好，介绍一下Python"

# 指定参数
ollama run qwen2.5:7b --temperature 0.7 --num-predict 256
```

## API 调用

```bash
# 生成（非流式）
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "Why is the sky blue?",
  "stream": false
}'

# 聊天
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'

# 列出模型
curl http://localhost:11434/api/tags
```

## Python SDK

```python
import ollama

# 生成
response = ollama.generate(model="qwen2.5:7b", prompt="Hello!")
print(response["response"])

# 聊天
response = ollama.chat(model="qwen2.5:7b", messages=[
    {"role": "user", "content": "Hello!"}
])

# 流式
for chunk in ollama.chat(model="qwen2.5:7b", messages=[...], stream=True):
    print(chunk["message"]["content"], end="", flush=True)
```
"""

_CORE_OLLAMA_TUNING = """---
title: Ollama Modelfile 自定义指南
domain: ollama
category: core
priority: 9
---

# Modelfile 自定义指南

## Modelfile 基本结构

```dockerfile
# 基础模型
FROM qwen2.5:7b

# 系统提示词（焊死人格）
SYSTEM \"\"\"你是龍魂AI助手，底座为中国文化。
- 为人民服务，不撒谎
- 保护用户数据主权
- 所有输出简洁直接
\"\"\"

# 参数设置
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|endoftext|>"

# 模板（消息格式）
TEMPLATE \"\"\"{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
\"\"\"
```

## 常用参数说明

| 参数 | 默认 | 说明 |
|:---|:---|:---|
| temperature | 0.7 | 越高越随机（0=确定，1=创意） |
| top_p | 0.9 | nucleus sampling 阈值 |
| top_k | 40 | 只从 top-k 个 token 中采样 |
| num_ctx | 2048 | 上下文窗口大小 |
| num_predict | 128 | 最大生成 token 数 |
| repeat_penalty | 1.1 | 重复惩罚（>1 减少重复） |
| seed | 0 | 随机种子（0=随机） |
| stop | — | 停止生成的 token 列表 |

## ARM64 (鲲鹏) 特殊处理

```bash
# 鲲鹏是 ARM64，有些模型可能不兼容
# 优先使用有 ARM64 版本的模型
ollama pull qwen2.5:7b     # ✅ ARM64 支持
ollama pull deepseek-r1:7b  # ✅ ARM64 支持

# 查看模型架构
ollama show qwen2.5:7b | grep architecture
```

## 导出/导入模型

```bash
# 导出 GGUF
ollama show --modelfile qwen2.5:7b > Modelfile
# 或直接复制
ollama cp qwen2.5:7b my-qwen2.5:latest

# 从 GGUF 导入
echo "FROM ./model.gguf" > Modelfile
ollama create my-model -f Modelfile
```
"""

# ─── Pydantic 核心知识卡 ───

_CORE_PYDANTIC_V2 = """---
title: Pydantic v2 完全速查
domain: pydantic
category: core
priority: 10
---

# Pydantic v2 速查

## 模型定义

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r"^[\\w.-]+@[\\w.-]+\\.\\w+$")
    age: int = Field(ge=0, le=150, default=18)
    tags: list[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, str] | None = None

    # 自定义验证器
    @field_validator("email")
    @classmethod
    def email_lower(cls, v: str) -> str:
        return v.lower()

# v1 → v2 迁移要点
# class Config → model_config
# @validator → @field_validator
# .dict() → .model_dump()
# .json() → .model_dump_json()
# .schema() → .model_json_schema()
# .parse_obj() → .model_validate()
# .parse_raw() → .model_validate_json()
```

## 常用 Field 约束

```python
class Item(BaseModel):
    # 字符串
    name: str = Field(min_length=1, max_length=100)
    pattern: str = Field(pattern=r"^[A-Z]+$")

    # 数字
    price: float = Field(gt=0)          # > 0
    quantity: int = Field(ge=1, le=999)  # >= 1 and <= 999

    # 列表
    tags: list[str] = Field(min_length=1, max_length=10)

    # 别名（API中不同名）
    user_id: int = Field(alias="userId")

    # 排除/包含
    password: str = Field(exclude=True)  # 序列化时排除

    # 描述（用于 JSON Schema）
    status: str = Field(description="当前状态: active/inactive")
```

## 嵌套模型

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    addresses: list[Address] = []
    primary_address: Address | None = None

# 从字典创建
user = User(**{
    "name": "张三",
    "addresses": [{"street": "长安街1号", "city": "北京", "zip_code": "100000"}]
})
```
"""

_CORE_PYDANTIC_SETTINGS = """---
title: pydantic-settings 配置管理
domain: pydantic
category: core
priority: 9
---

# pydantic-settings 配置管理

## 基本用法

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "MyApp"
    debug: bool = False
    port: int = 8080

    # 数据库
    database_url: str
    database_pool_size: int = 20

    # API密钥（敏感）
    secret_key: str
    api_key: str

    # CORS
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",           # 从 .env 加载
        env_file_encoding="utf-8",
        env_nested_delimiter="__", # 嵌套分隔符
        case_sensitive=False,      # 大小写不敏感
        extra="ignore",            # 忽略未知 env
    )

settings = Settings()

# 优先级: CLI参数 > 环境变量 > .env文件 > 默认值
```

## .env 文件示例

```env
APP_NAME=龍魂系统
DEBUG=false
PORT=8766
DATABASE_URL=sqlite:///data.db
SECRET_KEY=your-secret-here
API_KEY=sk-xxx
CORS_ORIGINS=["https://uid9622.cn","http://localhost:3000"]
```
"""

# ─── Docker 核心知识卡 ───

_CORE_DOCKERFILE = """---
title: Dockerfile 编写最佳实践
domain: docker
category: core
priority: 10
---

# Dockerfile 最佳实践

## 多阶段构建（Python 示例）

```dockerfile
# 阶段1: 构建依赖
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 阶段2: 运行镜像（最小化）
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 优化技巧

```dockerfile
# 1. 层缓存优化：先拷贝依赖文件，再拷贝代码
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # 代码放最后，改代码不需要重装依赖

# 2. 使用 .dockerignore
# __pycache__
# *.pyc
# .git
# .env
# venv/
# *.log

# 3. 非 root 用户
RUN useradd -m -s /bin/bash appuser
USER appuser

# 4. 健康检查
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \\
  CMD curl -f http://localhost:8080/health || exit 1

# 5. 信号处理
STOPSIGNAL SIGTERM
```

## .dockerignore

```
__pycache__
*.pyc
*.pyo
.env
.venv
venv/
.git
.gitignore
*.md
*.log
.DS_Store
node_modules/
```
"""

_CORE_DOCKER_COMPOSE = """---
title: Docker Compose 常用配置
domain: docker
category: core
priority: 10
---

# Docker Compose 常用模板

## Python FastAPI + Redis + Nginx

```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=sqlite:///data/app.db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./data:/app/data
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  redis_data:
```

## 环境变量文件

```yaml
services:
  app:
    env_file:
      - .env
      - .env.production  # 后者覆盖前者同名变量
    environment:
      - OVERRIDE_KEY=value  # 直接指定的优先级最高
```
"""

_CORE_DOCKER_COMMANDS = """---
title: Docker 命令速查表
domain: docker
category: core
priority: 9
---

# Docker 命令速查

## 容器管理

```bash
docker ps                        # 运行中的容器
docker ps -a                     # 所有容器
docker logs -f container_name    # 实时日志
docker logs --tail 100 container # 最后100行
docker exec -it container bash   # 进入容器
docker stop container && docker rm container  # 停止并删除
docker restart container
docker stats                     # 资源使用

# 清理
docker system prune -a           # 清理所有未使用（慎用！）
docker container prune           # 清理停止的容器
docker image prune               # 清理悬空镜像
```

## 镜像管理

```bash
docker images                    # 本地镜像
docker pull python:3.11-slim
docker tag source target
docker rmi image_id
docker build -t name:tag .
docker build --no-cache -t name:tag .
docker save -o file.tar image
docker load -i file.tar
```

## Compose

```bash
docker compose up -d             # 后台启动
docker compose down              # 停止并删除
docker compose down -v           # 同时删除 volumes
docker compose restart
docker compose logs -f service   # 某服务日志
docker compose ps
docker compose exec service bash
docker compose build --no-cache
```
"""

_CORE_DOCKER_PYTHON = """---
title: Docker 部署 Python 应用实战
domain: docker
category: core
priority: 9
---

# Docker 部署 Python 应用

## ARM64 兼容（鲲鹏）

```dockerfile
# 鲲鹏是 ARM64 架构
FROM --platform=linux/arm64 python:3.11-slim

# 或让 Docker 自动选择
FROM python:3.11-slim
```

## 最小化镜像

```dockerfile
FROM python:3.11-alpine  # 最小体积，但可能需要编译 C 扩展
# 或
FROM python:3.11-slim    # 平衡选择，推荐

RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir 减小镜像体积
```

## 多架构构建

```bash
# 构建并推送多架构镜像
docker buildx build --platform linux/amd64,linux/arm64 \\
  -t registry.example.com/myapp:latest --push .
```
"""

# ─── Git 核心知识卡 ───

_CORE_GIT_COMMANDS = """---
title: Git 命令速查表
domain: git
category: core
priority: 10
---

# Git 命令速查

## 日常操作

```bash
# 状态
git status
git log --oneline -20
git log --graph --oneline --all
git diff                    # 工作区 vs 暂存区
git diff --staged           # 暂存区 vs HEAD

# 提交
git add file1 file2
git add -p                  # 交互式暂存（推荐）
git commit -m "message"
git commit --amend          # 修改最后一次提交

# 分支
git branch                  # 本地分支
git branch -a               # 所有分支
git checkout -b new-branch  # 创建并切换
git switch -c new-branch    # 新方式（推荐）
git branch -d branch        # 删除本地分支
git merge branch            # 合并分支
git rebase main             # 变基到 main

# 远程
git push origin main
git push --force-with-lease # 安全强制推送
git pull --rebase           # 推荐方式拉取
git fetch --all --prune     # 同步所有远程分支
```

## 撤销与回滚

```bash
# 撤销工作区修改
git checkout -- file        # 丢弃修改
git restore file            # 新方式

# 撤销暂存
git reset HEAD file         # 取消暂存
git restore --staged file   # 新方式

# 撤销提交
git reset --soft HEAD~1     # 保留修改
git reset --hard HEAD~1     # 丢弃修改
git revert HEAD             # 生成"反向"提交（推荐）

# 找回误删
git reflog                  # 查看所有操作历史
git checkout HEAD@{2}       # 回到之前的状态
```

## 储藏

```bash
git stash                   # 储藏
git stash save "message"
git stash list
git stash pop               # 弹出最近
git stash pop stash@{1}     # 弹出指定
git stash drop stash@{0}    # 删除
```
"""

_CORE_GIT_WORKFLOW = """---
title: Git 工作流最佳实践
domain: git
category: core
priority: 9
---

# Git 工作流

## 提交信息规范

```
<type>: <简短描述>

<详细说明>

<关联issue/PR>
```

| type | 说明 |
|:---|:---|
| feat | 新功能 |
| fix | 修复bug |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具/依赖 |

示例:
```
feat: 添加飞书知识库自动抓取功能

- 支持 GitHub raw / web article 两种源
- SHA256 哈希版本追踪
- systemd timer 每6h自动更新

Closes #42
```

## 分支策略（简化版）

```
main ──── 生产就绪
  ├── feat/xxx ── 功能分支
  ├── fix/xxx  ── 修复分支
  └── release/x.x.x ── 发布分支
```

## 合并策略

```bash
# 功能分支合并到 main（推荐 squash）
git checkout main
git merge --squash feat/xxx
git commit -m "feat: xxx"

# 或 rebase 保持线性历史
git checkout feat/xxx
git rebase main
git checkout main
git merge feat/xxx  # fast-forward
```
"""

_CORE_GIT_TROUBLESHOOT = """---
title: Git 常见问题解决
domain: git
category: core
priority: 8
---

# Git 疑难排解

## 合并冲突

```bash
# 冲突标记
<<<<<<< HEAD
你的修改
=======
他人的修改
>>>>>>> branch-name

# 解决后
git add resolved_file
git commit -m "resolve conflict"

# 中止合并
git merge --abort
```

## 大文件处理

```bash
# 查找大文件
git rev-list --objects --all | git cat-file --batch-check \\
  | sort -k3nr | head -20

# 使用 .gitignore
echo "*.tar.gz" >> .gitignore
echo "models/" >> .gitignore

# 如果已经提交了大文件
git filter-branch --force --index-filter \\
  'git rm --cached --ignore-unmatch bigfile.tar.gz' \\
  --prune-empty -- --all
```

## GPG签名

```bash
# 配置
git config --global user.signingkey A2D0092CEE2E5BA87035600924C3704A8CC26D5F
git config --global commit.gpgsign true

# 签名提交
git commit -S -m "signed commit"

# 验证
git log --show-signature
```
"""

# ─── systemd 核心知识卡 ───

_CORE_SYSTEMD_SERVICE = """---
title: systemd Service 编写指南
domain: systemd
category: core
priority: 10
---

# systemd Service 完全指南

## 基本模板

```ini
[Unit]
Description=我的服务描述
After=network-online.target
Wants=network-online.target

[Service]
Type=simple              # 或 oneshot/forking/notify
User=root
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/main.py
ExecStop=/bin/kill -TERM $MAINPID
Restart=on-failure       # always/on-failure/on-abnormal/no
RestartSec=5
EnvironmentFile=/opt/myapp/.env

# 安全加固
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/myapp/data
ReadOnlyPaths=/opt/myapp/bin

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```

## Type 类型选择

| Type | 说明 | 适用场景 |
|:---|:---|:---|
| simple | 默认，ExecStart即视为启动完成 | 长期运行的前台进程 |
| oneshot | 执行完退出，配合 RemainAfterExit | 一次性任务 |
| forking | 父进程fork后退出 | 传统守护进程 |
| notify | 进程通过 sd_notify 通知就绪 | 支持 systemd 通知的服务 |

## 常用命令

```bash
systemctl daemon-reload          # 重载配置
systemctl enable service         # 开机自启
systemctl start service
systemctl stop service
systemctl restart service
systemctl status service
journalctl -u service -f         # 实时日志
journalctl -u service --since today
```
"""

_CORE_SYSTEMD_TIMER = """---
title: systemd Timer 定时任务指南
domain: systemd
category: core
priority: 10
---

# systemd Timer 定时任务

## 基本模板

```ini
# /etc/systemd/system/mytask.timer
[Unit]
Description=我的定时任务
Requires=mytask.service

[Timer]
OnCalendar=*-*-* 06:00:00       # 每天6点
OnCalendar=*-*-* 18:00:00       # 每天18点
OnBootSec=5min                  # 开机后5分钟
RandomizedDelaySec=300          # 随机延迟±5分钟（防撞车）
Persistent=true                 # 错过执行时间后补执行

[Install]
WantedBy=timers.target
```

## OnCalendar 格式

```ini
# 每分钟
OnCalendar=*-*-* *:*:00

# 每小时
OnCalendar=*-*-* *:00:00
OnCalendar=hourly

# 每天
OnCalendar=*-*-* 03:00:00
OnCalendar=daily

# 每周一 9:00
OnCalendar=Mon *-*-* 09:00:00
OnCalendar=weekly

# 每月1号 0:00
OnCalendar=*-*-01 00:00:00
OnCalendar=monthly

# 每6小时
OnCalendar=*-*-* 00:00:00
OnCalendar=*-*-* 06:00:00
OnCalendar=*-*-* 12:00:00
OnCalendar=*-*-* 18:00:00

# 工作日 9:00-18:00 每小时
OnCalendar=Mon..Fri *-*-* 09..18:00:00
```

## 常用命令

```bash
systemctl enable timer
systemctl start timer
systemctl list-timers --all    # 所有定时器
systemctl list-timers timer    # 指定定时器
```
"""

_CORE_SYSTEMD_TROUBLESHOOT = """---
title: systemd 排错指南
domain: systemd
category: core
priority: 9
---

# systemd 排错

## 常见问题

### 服务启动失败

```bash
systemctl status service --no-pager -l  # 详细状态
journalctl -u service -n 50             # 最后50行日志
journalctl -u service --since "5 min ago"
journalctl -xe                          # 系统级错误
```

### 定时器不触发

```bash
systemctl list-timers timer  # 查看下次触发时间
systemctl status timer

# 手动触发
systemctl start service  # 直接启动关联的服务
```

### 修改后不生效

```bash
systemctl daemon-reload     # 任何 .service/.timer 修改后必须执行
systemctl restart service
```
"""

# ─── Nginx 核心知识卡 ───

_CORE_NGINX_CONFIG = """---
title: Nginx 配置完整指南
domain: nginx
category: core
priority: 10
---

# Nginx 配置指南

## 基本结构

```nginx
# 全局块
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

# events 块
events {
    worker_connections 1024;
}

# http 块
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    keepalive_timeout 65;

    # 引入站点配置
    include /etc/nginx/sites-enabled/*;
}
```

## 站点配置模板

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    # 静态文件
    root /var/www/html;
    index index.html;

    # 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查端点
    location /health {
        access_log off;
        return 200 "OK";
    }
}
```
"""

_CORE_NGINX_PROXY = """---
title: Nginx 反向代理配置详解
domain: nginx
category: core
priority: 10
---

# Nginx 反向代理

## WebSocket 支持

```nginx
location /ws/ {
    proxy_pass http://backend:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400s;
}
```

## 负载均衡

```nginx
upstream backend {
    least_conn;  # 最少连接
    server 127.0.0.1:8080 weight=3;
    server 127.0.0.1:8081 weight=1;
    server 127.0.0.1:8082 backup;  # 备用
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## 限流

```nginx
# 请求频率限制
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=mylimit burst=20 nodelay;
        proxy_pass http://backend;
    }
}

# 连接数限制
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    location / {
        limit_conn addr 10;
    }
}
```

## 超时配置

```nginx
location /api/ {
    proxy_pass http://backend;
    proxy_connect_timeout 10s;
    proxy_send_timeout 30s;
    proxy_read_timeout 120s;  # 长连接/流式输出需要大值
}
```
"""

_CORE_NGINX_SSL = """---
title: Nginx SSL/HTTPS 配置
domain: nginx
category: core
priority: 10
---

# Nginx SSL 配置

## Let's Encrypt 免费证书

```nginx
server {
    listen 443 ssl http2;
    server_name uid9622.cn;

    ssl_certificate /etc/letsencrypt/live/uid9622.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/uid9622.cn/privkey.pem;

    # 现代安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
}

# HTTP → HTTPS 重定向
server {
    listen 80;
    server_name uid9622.cn;
    return 301 https://$host$request_uri;
}
```

## 自签名证书（开发用）

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\
  -keyout key.pem -out cert.pem \\
  -subj "/CN=localhost"
```
"""

_CORE_NGINX_PERF = """---
title: Nginx 性能优化
domain: nginx
category: core
priority: 8
---

# Nginx 性能优化

## 基础优化

```nginx
# worker 进程数
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;          # Linux
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;

    # Gzip 压缩
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_types text/plain application/json text/css application/javascript;
}
```

## 缓存

```nginx
# 静态文件浏览器缓存
location ~* \\.(jpg|jpeg|png|gif|ico|css|js|svg|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# 代理缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;
location /api/ {
    proxy_cache my_cache;
    proxy_cache_valid 200 10m;
    proxy_cache_key "$host$request_uri";
    proxy_pass http://backend;
}
```
"""

# ─── CloudBase 核心知识卡 ───

_CORE_CLOUDBASE_AUTH = """---
title: CloudBase 认证配置指南
domain: cloudbase
category: core
priority: 10
---

# CloudBase 认证配置

## 支持的认证方式

| 方式 | 说明 | 适用场景 |
|:---|:---|:---|
| 匿名登录 | 无需注册，临时身份 | 快速体验/低安全需求 |
| 邮箱登录 | 邮箱+密码注册登录 | Web应用 |
| 手机号 | 短信验证码 | 国内应用 |
| 微信登录 | OAuth授权 | 小程序/公众号 |
| 自定义登录 | 自建用户系统签发ticket | 已有用户体系 |

## 认证流程（Web SDK）

```javascript
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({ env: "your-env-id" });
const auth = app.auth();

// 邮箱注册
await auth.signUpWithEmailAndPassword(email, password);

// 邮箱登录
await auth.signInWithEmailAndPassword(email, password);

// 匿名登录
await auth.anonymousAuthProvider().signIn();

// 获取登录状态
const loginState = await auth.getLoginState();
if (loginState) {
    console.log("已登录:", loginState.user.uid);
}

// 退出
await auth.signOut();
```
"""

_CORE_CLOUDBASE_DATABASE = """---
title: CloudBase 数据库操作速查
domain: cloudbase
category: core
priority: 10
---

# CloudBase 数据库

## NoSQL 文档数据库

```javascript
const db = app.database();
const _ = db.command;

// 查询
const res = await db.collection("users")
    .where({ age: _.gt(18) })
    .orderBy("created_at", "desc")
    .limit(20)
    .get();

// 新增
await db.collection("users").add({
    name: "张三",
    email: "zhangsan@example.com",
    created_at: new Date(),
});

// 更新
await db.collection("users").doc("doc-id").update({
    name: "张三改名",
    updated_at: new Date(),
});

// 删除
await db.collection("users").doc("doc-id").remove();
```

## MySQL 关系数据库

```sql
-- 环境ID自动注入
SELECT * FROM users WHERE age > 18 ORDER BY created_at DESC LIMIT 20;

INSERT INTO users (name, email) VALUES ('张三', 'zhangsan@example.com');

UPDATE users SET name = '张三改名' WHERE id = 1;

DELETE FROM users WHERE id = 1;
```
"""

_CORE_CLOUDBASE_FUNC = """---
title: CloudBase 云函数开发指南
domain: cloudbase
category: core
priority: 9
---

# CloudBase 云函数

## Python 云函数

```python
# index.py
def main(event, context):
    \"\"\"
    event: 请求参数
    context: 运行上下文
    \"\"\"
    action = event.get("action", "")
    data = event.get("data", {})

    if action == "hello":
        return {"code": 0, "message": f"Hello, {data.get('name', 'World')}"}
    return {"code": -1, "message": "Unknown action"}
```

## 定时触发器

```python
# 每小时执行
def main(event, context):
    # event["TriggerName"] = "myTrigger"
    # event["Time"] = "2026-08-05T12:00:00Z"
    # 执行定时任务...
    return {"code": 0}
```
"""

_CORE_CLOUDBASE_DEPLOY = """---
title: CloudBase 部署流程速查
domain: cloudbase
category: core
priority: 9
---

# CloudBase 部署速查

## Web 静态托管

```bash
# 初始化
tcb init

# 部署
tcb hosting deploy ./dist -e your-env-id

# 查看状态
tcb hosting detail -e your-env-id
```

## CloudRun 容器部署

```bash
# 构建并推送镜像
docker build -t ccr.ccs.tencentyun.com/namespace/app:v1 .
docker push ccr.ccs.tencentyun.com/namespace/app:v1

# 通过 CloudBase MCP 部署
# 或 tcb cloudrun deploy
```
"""

# ─── Redis 核心知识卡 ───

_CORE_REDIS_COMMANDS = """---
title: Redis 命令速查表
domain: redis
category: core
priority: 9
---

# Redis 命令速查

## 字符串

```bash
SET key value [EX seconds] [NX|XX]
GET key
DEL key
INCR key / DECR key
EXPIRE key seconds
TTL key
SETEX key seconds value   # SET + EXPIRE 原子操作
```

## 哈希

```bash
HSET user:1 name "张三" age 25
HGET user:1 name
HGETALL user:1
HDEL user:1 age
HEXISTS user:1 name
HINCRBY user:1 age 1
```

## 列表

```bash
LPUSH queue "task1"        # 左推
RPUSH queue "task2"        # 右推
LPOP queue                 # 左弹
RPOP queue                 # 右弹
LRANGE queue 0 -1          # 全量
LLEN queue
```

## 集合/有序集合

```bash
SADD tags "python" "redis" "docker"
SMEMBERS tags
SISMEMBER tags "python"
SINTER set1 set2           # 交集
SUNION set1 set2           # 并集

ZADD leaderboard 100 "player1" 95 "player2"
ZRANGE leaderboard 0 -1 WITHSCORES
ZREVRANGE leaderboard 0 4       # Top 5
```
"""

_CORE_REDIS_PYTHON = """---
title: Redis Python 使用指南
domain: redis
category: core
priority: 9
---

# Redis Python 指南

```python
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# 基本操作
r.set("key", "value", ex=3600)  # 1小时过期
value = r.get("key")

# 哈希
r.hset("user:1", mapping={"name": "张三", "age": "25"})
name = r.hget("user:1", "name")

# 列表作为队列
r.lpush("task_queue", "task1")
task = r.brpop("task_queue", timeout=5)  # 阻塞等待

# Pipeline（批量操作提速）
pipe = r.pipeline()
pipe.set("a", 1)
pipe.set("b", 2)
pipe.execute()

# 分布式锁
lock = r.lock("my_lock", timeout=10)
if lock.acquire(blocking=False):
    try:
        do_critical_work()
    finally:
        lock.release()
```
"""

# ─── SQLAlchemy 核心知识卡 ───

_CORE_SQLALCHEMY_2 = """---
title: SQLAlchemy 2.0 速查
domain: sqlalchemy
category: core
priority: 10
---

# SQLAlchemy 2.0 速查

## 模型定义

```python
from sqlalchemy import create_engine, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    # 关系
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship(back_populates="posts")
```

## 异步查询 (async)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("sqlite+aiosqlite:///app.db")

async with AsyncSession(engine) as session:
    # 查询
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    # 新增
    user = User(name="张三", email="zhangsan@example.com")
    session.add(user)
    await session.commit()

    # 更新
    user.name = "李四"
    await session.commit()
```

## 连接管理（FastAPI集成）

```python
from sqlalchemy.ext.asyncio import async_sessionmaker

async_engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```
"""


# ═══════════════════════════════════════════════════════════════
# 域13: httpx 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_HTTPX = """---
title: httpx 核心知识卡
domain: httpx
category: core
priority: 10
---

# httpx 异步HTTP客户端

## 安装
```bash
pip install httpx
```

## 快速开始

```python
import httpx

# 同步客户端
resp = httpx.get("https://api.example.com/data")
resp.json()

# 异步客户端
import asyncio

async def fetch():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
        return resp.json()

data = asyncio.run(fetch())
```

## 常用模式

**带超时和重试:**
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def fetch_with_retry(url):
    async with httpx.AsyncClient(timeout=30.0) as client:
        return await client.get(url)
```

**流式响应（大文件/SSE）:**
```python
async with httpx.AsyncClient() as client:
    async with client.stream("GET", "https://api.example.com/stream") as resp:
        async for chunk in resp.aiter_bytes():
            process_chunk(chunk)
```

**带认证:**
```python
# Basic Auth
client = httpx.AsyncClient(auth=("username", "password"))
# Bearer Token
client = httpx.AsyncClient(headers={"Authorization": "Bearer token"})
```

**并发请求:**
```python
async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## 排错指南

| 问题 | 原因 | 解决 |
|:---|:---|:---|
| ReadTimeout | 服务端响应慢 | 增大 timeout 参数 |
| ConnectTimeout | 网络不通 | 检查URL/防火墙 |
| HTTPStatusError | 4xx/5xx | 检查 resp.raise_for_status() |
| PoolTimeout | 连接池耗尽 | 增加 max_connections |
| RemoteProtocolError | 服务端断开 | 加重试 + 检查服务端日志 |

## 最佳实践

1. 生产环境使用 AsyncClient 复用连接池
2. 设置合理的超时（连接、读取、写入分开）
3. limits=httpx.Limits(max_keepalive_connections=20) 控制连接池
4. 错误分类处理：可重试（5xx）vs 不可重试（4xx）
5. 使用 event_hooks 做请求/响应日志埋点
"""


# ═══════════════════════════════════════════════════════════════
# 域14: Alembic 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_ALEMBIC = """---
title: Alembic 核心知识卡
domain: alembic
category: core
priority: 10
---

# Alembic 数据库迁移管理

## 安装与初始化
```bash
pip install alembic
alembic init alembic
# 编辑 alembic.ini: sqlalchemy.url = postgresql://user:pass@localhost/db
# 编辑 alembic/env.py: target_metadata = Base.metadata
```

## 常用命令

```bash
alembic revision --autogenerate -m "描述"  # 生成迁移文件
alembic upgrade head                        # 升级到最新
alembic downgrade -1                        # 回退一个版本
alembic upgrade +2                          # 前进两个版本
alembic history                             # 查看历史
alembic current                             # 查看当前版本
alembic stamp head                          # 标记版本（不执行SQL）
```

## env.py 关键配置

```python
# 支持多个数据库
from myapp.models import Base
target_metadata = Base.metadata

# 支持异步数据库（SQLAlchemy 2.0）
from sqlalchemy.ext.asyncio import create_async_engine
connectable = create_async_engine("postgresql+asyncpg://...")

def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
```

## 手动迁移

```python
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```

## 数据迁移（数据转换）

```python
def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String(200)))
    conn = op.get_bind()
    conn.execute("UPDATE users SET full_name = first_name || ' ' || last_name")
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
```

## 排错指南

| 问题 | 解决 |
|:---|:---|
| 迁移冲突 | alembic merge -m "merge" 版本1 版本2 |
| 版本号混乱 | alembic stamp head 重新标记 |
| 找不到模型 | 确保 env.py 中导入了所有模型 |
| 外键依赖 | 先创建父表再子表，删除时反向 |
"""


# ═══════════════════════════════════════════════════════════════
# 域15: Pytest 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_PYTEST = """---
title: Pytest 核心知识卡
domain: pytest
category: core
priority: 10
---

# Pytest 测试框架

## 安装
```bash
pip install pytest pytest-asyncio pytest-cov
```

## 文件结构
```
tests/
├── conftest.py      # 全局fixture
├── test_models.py
├── test_api.py
└── test_unit/
    └── test_utils.py
```

## 核心标记

```python
@pytest.mark.asyncio          # 异步测试
@pytest.mark.parametrize("input,expected", [(1,2), (3,4)])
@pytest.mark.skip(reason="未完成")
@pytest.mark.xfail(reason="已知失败")
@pytest.mark.slow             # 自定义标记
```

## Fixture 用法

```python
# conftest.py
import pytest
from myapp import create_app

@pytest.fixture
def app():
    return create_app(testing=True)

@pytest.fixture
async def async_client(app):
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def db_session():
    conn = get_db_connection()
    yield conn
    conn.rollback()  # 测试后回滚
```

## 异步测试

```python
@pytest.mark.asyncio
async def test_async_fetch():
    data = await fetch_data()
    assert data["status"] == "ok"

@pytest.mark.asyncio
async def test_api_endpoint(async_client):
    resp = await async_client.get("/api/users")
    assert resp.status_code == 200
```

## 模拟（Mock）

```python
from unittest.mock import AsyncMock, patch

@patch("myapp.services.external_api")
def test_with_mock(mock_api):
    mock_api.return_value = {"result": "mocked"}
    result = my_service()
    assert result["result"] == "mocked"

@patch("myapp.services.async_fetch", new_callable=AsyncMock)
async def test_async_with_mock(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    result = await my_async_service()
    assert result["status"] == "ok"
```

## 常用命令

```bash
pytest                              # 运行所有测试
pytest -v                           # 详细输出
pytest -k "test_login"              # 按名称过滤
pytest -m "not slow"                # 排除慢测试
pytest --cov=myapp                  # 覆盖率报告
pytest --cov-report=html            # HTML报告
pytest -x                           # 遇到失败立即停止
pytest --maxfail=3                  # 允许3个失败
pytest test_api.py::test_login      # 单个测试
```

## 最佳实践

1. 测试文件命名 test_*.py
2. 函数命名 test_功能描述
3. 一个测试只测一件事
4. 使用 conftest.py 共享fixture
5. 测试数据库使用内存SQLite或事务回滚
6. 覆盖率目标 > 80%
"""


# ═══════════════════════════════════════════════════════════════
# 域16: Loguru 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_LOGURU = """---
title: Loguru 核心知识卡
domain: loguru
category: core
priority: 10
---

# Loguru 现代化日志

## 安装与基本用法
```bash
pip install loguru
```

```python
from loguru import logger

logger.debug("调试信息")
logger.info("正常信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

## 核心特性

**结构化参数:**
```python
logger.info("用户 {user} 登录成功", user="admin")
```

**异常捕获:**
```python
@logger.catch
def risky_function():
    raise ValueError("出错了")
# 自动记录完整堆栈
```

**上下文绑定:**
```python
logger.bind(request_id="123").info("处理请求")
logger.configure(extra={"service": "api", "version": "2.0"})
```

## 配置 Sink（输出目标）

```python
# 文件输出（自动轮转）
logger.add(
    "logs/app.log",
    rotation="1 day",        # 每天轮转
    retention="7 days",      # 保留7天
    compression="zip",       # 压缩归档
    format="{time}|{level}|{message}",
    level="INFO",
    enqueue=True,           # 异步写入
)

# JSON 格式（结构化日志）
logger.add("logs/app.json", serialize=True, level="INFO")

# 错误单独存放
logger.add("logs/error.log", level="ERROR", rotation="100 MB", retention="30 days")
```

## FastAPI 集成

```python
@app.middleware("http")
async def log_requests(request, call_next):
    with logger.contextualize(request_id=request.headers.get("X-Request-ID")):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"响应 {response.status_code}")
        return response

@app.exception_handler(Exception)
async def global_exception(request, exc):
    logger.opt(exception=exc).error("全局异常")
    return {"error": "内部错误"}
```

## 排错指南

| 问题 | 解决 |
|:---|:---|
| 日志不写入 | 检查目录权限 + enqueue=True |
| 性能慢 | 使用异步 + 级别过滤 |
| 日志爆炸 | 设置 rotation + retention |
| 多进程冲突 | enqueue=True 启用队列 |
"""


# ═══════════════════════════════════════════════════════════════
# 域17: Starlette 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_STARLETTE = """---
title: Starlette 核心知识卡
domain: starlette
category: core
priority: 10
---

# Starlette 轻量级异步 Web 框架

Starlette = FastAPI 的底层实现。FastAPI 在 Starlette 上加了 OpenAPI、Pydantic 验证、依赖注入。

## 安装与快速开始
```bash
pip install starlette uvicorn
```

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def hello(request):
    return JSONResponse({"message": "Hello"})

app = Starlette(routes=[Route("/", hello)])
# uvicorn main:app --reload
```

## 路由与路径参数

```python
async def user(request):
    username = request.path_params["username"]
    return JSONResponse({"user": username})

routes = [
    Route("/", hello),
    Route("/users/{username}", user),
]
```

## 中间件

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

# 自定义中间件
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        response.headers["X-Response-Time"] = str(time.time() - start)
        return response

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(TimingMiddleware)
```

## WebSocket 支持

```python
from starlette.websockets import WebSocket

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
```

## 后台任务

```python
from starlette.background import BackgroundTasks

async def send_email(email: str):
    pass  # 耗时任务

async def create_user(request):
    tasks = BackgroundTasks()
    tasks.add_task(send_email, "user@example.com")
    return JSONResponse({"status": "ok"}, background=tasks)
```

## TestClient 测试

```python
from starlette.testclient import TestClient
client = TestClient(app)
resp = client.get("/")
assert resp.status_code == 200
```

## 排错指南

| 问题 | 解决 |
|:---|:---|
| 路由404 | 检查路由注册顺序 |
| CORS报错 | 添加 CORSMiddleware |
| WebSocket 连接失败 | 检查 allow_websockets=True |
| 中间件顺序 | 注册顺序 = 执行顺序（外层到内层） |
"""


# ═══════════════════════════════════════════════════════════════
# 域18: PostgreSQL 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_POSTGRESQL = """---
title: PostgreSQL 核心知识卡
domain: postgresql
category: core
priority: 10
---

# PostgreSQL 生产级数据库

## 快速开始
```bash
apt install postgresql postgresql-contrib
sudo -u postgres psql
```

```sql
CREATE USER myuser WITH PASSWORD 'password';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

## 常用 SQL

```sql
\\dt                                          -- 查看表
\\d+ users                                    -- 查看表结构
SELECT * FROM pg_stat_activity;               -- 查看连接
SELECT query, calls, total_time               -- 慢查询
FROM pg_stat_statements
ORDER BY total_time DESC LIMIT 10;
SELECT * FROM pg_locks WHERE NOT granted;     -- 查看锁
```

## 性能优化

**索引类型:**
```sql
-- B-tree（默认，适合 =, <, >, BETWEEN）
CREATE INDEX idx_users_name ON users(name);
-- GiST（适合全文搜索）
CREATE INDEX idx_posts_content ON posts USING GIN(to_tsvector('english', content));
-- 部分索引
CREATE INDEX idx_active_users ON users(id) WHERE status = 'active';
-- 覆盖索引
CREATE INDEX idx_users_name_age ON users(name) INCLUDE (age);
```

**查询分析:**
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE name = 'test';
SET max_parallel_workers_per_gather = 4;
```

## 备份与恢复

```bash
pg_dump -U myuser -h localhost -F c -f mydb.dump mydb     # 完整备份
pg_dump -U myuser -h localhost mydb | gzip > mydb.sql.gz  # 压缩备份
pg_restore -U myuser -h localhost -d mydb mydb.dump        # 还原
pg_dump -U myuser mydb | gzip > /backups/mydb_$(date +%Y%m%d).sql.gz  # 定时备份
```

## Python 连接池

```python
# asyncpg
import asyncpg
pool = await asyncpg.create_pool(
    host="localhost", database="mydb",
    user="myuser", password="password",
    min_size=2, max_size=20, timeout=30.0
)

# SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://user:pass@localhost/mydb",
    pool_size=10, max_overflow=20,
    pool_recycle=3600, pool_pre_ping=True
)
```

## 排错指南

| 问题 | 解决 |
|:---|:---|
| 连接数超限 | max_connections 调大 或关闭idle连接 |
| 查询慢 | EXPLAIN 分析 + 添加索引 |
| 数据库锁 | SELECT * FROM pg_locks + pg_terminate_backend(pid) |
| 磁盘满 | 清理 WAL 日志或扩容 |
| 复制延迟 | 检查网络 + 主从配置 |
"""


# ═══════════════════════════════════════════════════════════════
# 域19: Prometheus 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_PROMETHEUS = """---
title: Prometheus 核心知识卡
domain: prometheus
category: core
priority: 10
---

# Prometheus 监控与告警

## 安装
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvf prometheus-*.tar.gz
```

## prometheus.yml
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "myapp"
    static_configs:
      - targets: ["localhost:8000"]
```

## 指标类型

| 类型 | 用途 | Python示例 |
|:---|:---|:---|
| Counter | 只增不减（请求数） | requests_total += 1 |
| Gauge | 可增可减（连接数） | active_connections.set(10) |
| Histogram | 分布统计（响应时间） | http_request_duration_seconds.observe(0.5) |
| Summary | 分位数统计 | 同上 |

## Python 埋点

```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

requests_total = Counter("http_requests_total", "总请求数", ["method", "endpoint"])
active_connections = Gauge("active_connections", "活跃连接数")
request_duration = Histogram("http_request_duration_seconds", "请求耗时",
    buckets=[0.1, 0.5, 1, 2, 5])

# FastAPI 中间件
@app.middleware("http")
async def metrics_middleware(request, call_next):
    requests_total.labels(method=request.method, endpoint=request.url.path).inc()
    active_connections.inc()
    start = time.time()
    resp = await call_next(request)
    request_duration.observe(time.time() - start)
    active_connections.dec()
    return resp

start_http_server(8000)  # 启动指标端点
```

## 告警规则

```yaml
# alert.rules.yml
groups:
  - name: myapp
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.01
        for: 5m
        annotations:
          summary: "错误率过高"
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        annotations:
          summary: "服务 {{ $labels.instance }} 不可用"
```

## 常用 PromQL

```promql
rate(http_requests_total[5m])                                                # 每秒请求数
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))    # P95响应时间
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) # 错误率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100   # 内存使用
```

## 排错指南

| 问题 | 解决 |
|:---|:---|
| 指标抓不到 | 检查 target 地址 + 网络 + 防火墙 |
| 告警不触发 | for 持续时间 + 查询语法验证 |
| 磁盘满 | 设置 retention 保留时间 |
| 查询慢 | 减少范围 + Recording Rules 预聚合 |
"""


# ═══════════════════════════════════════════════════════════════
# 域20: 国密 核心知识卡
# ═══════════════════════════════════════════════════════════════
_CORE_GUOMI = """---
title: 国密核心知识卡
domain: guomi
category: core
priority: 10
---

# 国密算法 SM2/SM3/SM4

依据: GB/T 32918-2016, GB/T 32905-2016, GB/T 32907-2016

## 安装
```bash
pip install gmssl
```

## SM2（非对称加密·椭圆曲线）

**生成密钥对:**
```python
from gmssl import sm2, sm2_key

private_key = sm2_key.generate_private_key()
public_key = sm2_key.get_public_key(private_key)
```

**加密/解密:**
```python
from gmssl.sm2 import CryptSM2

crypt_sm2 = CryptSM2(private_key=pri_key, public_key=pub_key)
cipher = crypt_sm2.encrypt(b"\\u9f99\\u9b42\\u7cfb\\u7edf\\u6d4b\\u8bd5\\u6570\\u636e")
decrypted = crypt_sm2.decrypt(cipher).decode()
```

**签名/验签:**
```python
signature = crypt_sm2.sign(data, private_key)
verified = crypt_sm2.verify(signature, data, public_key)  # True
```

## SM3（哈希算法）

```python
from gmssl.sm3 import sm3_hash

hash_value = sm3_hash("龍魂系统".encode())  # 64位十六进制

def sm3_file(filepath):
    with open(filepath, 'rb') as f:
        return sm3_hash(f.read())
```

## SM4（对称加密·分组密码）

```python
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

crypt_sm4 = CryptSM4()
key = b"1234567890abcdef"

# ECB模式
crypt_sm4.set_key(key, SM4_ENCRYPT)
cipher = crypt_sm4.crypt_ecb(b"龍魂系统SM4测试")
crypt_sm4.set_key(key, SM4_DECRYPT)
decrypted = crypt_sm4.crypt_ecb(cipher)

# CBC模式
iv = b"1234567890123456"
cipher = crypt_sm4.crypt_cbc(iv, plaintext)
```

## 实战封装

```python
class GuomiCrypto:
    def __init__(self, sm4_key=None, sm2_pri=None, sm2_pub=None):
        self.sm4_key = sm4_key or os.urandom(16)
        self.sm2_pri = sm2_pri
        self.sm2_pub = sm2_pub

    def encrypt_sensitive_data(self, data: str) -> str:
        crypt = CryptSM4()
        crypt.set_key(self.sm4_key, SM4_ENCRYPT)
        iv = os.urandom(16)
        cipher = crypt.crypt_cbc(iv, data.encode())
        return (iv + cipher).hex()

    def decrypt_sensitive_data(self, hex_data: str) -> str:
        raw = bytes.fromhex(hex_data)
        iv, cipher = raw[:16], raw[16:]
        crypt = CryptSM4()
        crypt.set_key(self.sm4_key, SM4_DECRYPT)
        return crypt.crypt_cbc(iv, cipher).decode()

    def sign_and_hash(self, data: str) -> str:
        hash_val = sm3_hash(data.encode())
        crypt = CryptSM2(private_key=self.sm2_pri, public_key=self.sm2_pub)
        return crypt.sign(hash_val.encode()).hex()
```

## 合规要点

| 算法 | 密钥长度 | 用途 | 合规场景 |
|:---|:---|:---|:---|
| SM2 | 256位 | 非对称加密/签名 | 数字证书、身份认证 |
| SM3 | 256位 | 哈希摘要 | 数据完整性校验 |
| SM4 | 128位 | 对称加密 | 数据存储加密、传输加密 |

**等保2.0:** 三级以上系统需使用国密算法替代国际算法。
**GM/T标准:** SM2=GM/T 0003-2012, SM3=GM/T 0004-2012, SM4=GM/T 0002-2012
"""


# ═══════════════════════════════════════════════════════════════
# 后解析：将 core_cards 字符串占位符解析为实际内容
# ═══════════════════════════════════════════════════════════════
for _domain, _config in DOMAIN_CONFIGS.items():
    _resolved = {}
    for _filename, _varname in _config.get("core_cards", {}).items():
        if isinstance(_varname, str) and _varname.startswith("_CORE_"):
            _resolved[_filename] = globals().get(_varname, _varname)
        else:
            _resolved[_filename] = _varname
    _config["core_cards"] = _resolved


# ═══════════════════════════════════════════════════════════════
# 引擎核心
# ═══════════════════════════════════════════════════════════════

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, retries: int = MAX_RETRIES) -> Optional[bytes]:
    """带重试和指数退避的 URL 抓取。"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/plain,text/markdown,application/json,text/html,*/*",
            })
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                time.sleep(wait)
    return None


def hash_content(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:16]


def load_version(kb_root: Path) -> Dict[str, Any]:
    vf = kb_root / VERSION_FILE
    if vf.exists():
        try:
            return json.loads(vf.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": "0.0.0", "last_fetch": None, "sources": {}, "fetch_count": 0}


def save_version(kb_root: Path, version: Dict) -> None:
    ensure_dir(kb_root)
    (kb_root / VERSION_FILE).write_text(
        json.dumps(version, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _html_to_markdown_simple(html: str, url: str, title: str = "") -> str:
    """HTML → Markdown 转换。"""
    if not title:
        m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if m:
            title = m.group(1).strip()

    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.IGNORECASE | re.DOTALL)
    text = body_match.group(1) if body_match else html

    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(p|div|h[1-6]|li|tr|section|article)>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    md = f"---\ntitle: {title}\nsource: {url}\nfetched_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    md += f"# {title}\n\n> 来源: {url}\n\n" + "\n".join(lines)
    return md


def fetch_source(source: Dict, kb_root: Path) -> Tuple[bool, str]:
    """根据类型抓取单个源。"""
    stype = source["type"]
    url = source["url"]
    dest = kb_root / source["file"]

    if stype == "github_raw":
        content = fetch_url(url)
        if content is None:
            return False, f"无法获取: {url}"
        text = content.decode("utf-8", errors="replace")
        ensure_dir(dest.parent)
        dest.write_text(text, encoding="utf-8")
        return True, f"OK ({len(text)} chars)"

    elif stype == "web_article":
        content = fetch_url(url)
        if content is None:
            return False, f"无法获取: {url}"
        html = content.decode("utf-8", errors="replace")
        md = _html_to_markdown_simple(html, url, source.get("name", ""))
        ensure_dir(dest.parent)
        dest.write_text(md, encoding="utf-8")
        return True, f"OK ({len(md)} chars)"

    return False, f"未知类型: {stype}"


def fetch_domain(domain: str, kb_root: Path, force: bool = False) -> Dict[str, Any]:
    """抓取单个知识域。"""
    config = DOMAIN_CONFIGS.get(domain)
    if not config:
        return {"error": f"未知知识域: {domain}"}

    version = load_version(kb_root)
    results = {
        "domain": domain,
        "name": config["name"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sources": {},
        "cards": {},
    }

    sources = config.get("sources", [])
    core_cards = config.get("core_cards", {})

    # 抓取外部源
    updated = skipped = failed = 0
    for src in sorted(sources, key=lambda s: -s.get("priority", 0)):
        sid = src["id"]
        sname = src["name"]
        dest = kb_root / src["file"]

        if not force and dest.exists():
            skipped += 1
            results["sources"][sid] = {"status": "skipped"}
            continue

        try:
            ok, msg = fetch_source(src, kb_root)
            if ok:
                updated += 1
                results["sources"][sid] = {"status": "ok", "msg": msg}
            else:
                failed += 1
                results["sources"][sid] = {"status": "failed", "msg": msg}
        except Exception as e:
            failed += 1
            results["sources"][sid] = {"status": "error", "error": str(e)}

    # 写入自建核心知识卡
    card_count = 0
    for filename, content in core_cards.items():
        dest = kb_root / filename
        ensure_dir(dest.parent)
        dest.write_text(content, encoding="utf-8")
        card_count += 1
        results["cards"][filename] = "written"

    # 更新版本
    version["last_fetch"] = datetime.now(timezone.utc).isoformat()
    version["fetch_count"] = version.get("fetch_count", 0) + 1
    version["last_results"] = {"sources_updated": updated, "sources_skipped": skipped,
                                "sources_failed": failed, "cards_written": card_count}
    save_version(kb_root, version)

    results["summary"] = f"源: {updated}↑ {skipped}→ {failed}↓ | 知识卡: {card_count}"
    return results


def should_fetch(kb_root: Path) -> bool:
    """检查是否需要更新。"""
    version = load_version(kb_root)
    last_fetch = version.get("last_fetch")
    if not last_fetch:
        return True
    try:
        last_dt = datetime.fromisoformat(last_fetch)
        elapsed = (datetime.now(timezone.utc) - last_dt.replace(tzinfo=timezone.utc)).total_seconds()
        return elapsed > FETCH_INTERVAL_HOURS * 3600
    except Exception:
        return True


def generate_index(kb_root: Path, domain: str) -> None:
    """生成知识域索引。"""
    config = DOMAIN_CONFIGS.get(domain, {})
    name = config.get("name", domain)
    index_md = f"# 龍魂·{name} 知识库索引\n\n> 自动生成 | {datetime.now(timezone.utc).isoformat()}\n\n## 文件清单\n\n| 文件 | 大小 |\n|:---|:---|\n"

    total = 0
    total_size = 0
    for f in sorted(kb_root.glob("*")):
        if f.name.startswith("kb_version") or f.name == "INDEX.md":
            continue
        size = f.stat().st_size
        total += 1
        total_size += size
        index_md += f"| {f.name} | {size//1024}KB |\n"

    index_md += f"\n**总计**: {total} 文件, {total_size//1024}KB\n"
    version = load_version(kb_root)
    index_md += f"\n- 抓取次数: {version.get('fetch_count', 0)}\n"
    index_md += f"- 上次更新: {version.get('last_fetch', '从未')}\n"
    ensure_dir(kb_root)
    (kb_root / "INDEX.md").write_text(index_md, encoding="utf-8")


def generate_master_index(kb_base: Path) -> None:
    """生成总索引。"""
    idx = f"# 龍魂·知识底座总索引\n\n> {datetime.now(timezone.utc).isoformat()}\n\n| 域 | 名称 | 文件数 | 大小 | 上次更新 |\n|:---|:---|:---:|:---:|:---|\n"
    grand_total_files = 0
    grand_total_size = 0

    for domain, config in sorted(DOMAIN_CONFIGS.items()):
        dk = kb_base / domain
        if not dk.exists():
            continue
        files = [f for f in dk.glob("*") if not f.name.startswith("kb_version") and f.name != "INDEX.md"]
        n = len(files)
        sz = sum(f.stat().st_size for f in files)
        grand_total_files += n
        grand_total_size += sz
        v = load_version(dk)
        last = v.get("last_fetch", "—")[:10] if v.get("last_fetch") else "—"
        idx += f"| {config['emoji']} {domain} | {config['name']} | {n} | {sz//1024}KB | {last} |\n"

    idx += f"\n**总计**: {len(DOMAIN_CONFIGS)} 个知识域, {grand_total_files} 个文件, {grand_total_size//1024}KB\n"
    ensure_dir(kb_base)
    (kb_base / "MASTER_INDEX.md").write_text(idx, encoding="utf-8")


def determine_base(force_local: bool = False) -> Path:
    if force_local or os.environ.get("LH_KB_LOCAL"):
        return LOCAL_KB_BASE
    if Path("/opt/longhun-system").exists():
        return KB_BASE
    return LOCAL_KB_BASE


def list_domains():
    """列出所有知识域。"""
    print(f"{'域':<16} {'名称':<20} {'源':>4} {'知识卡':>5}")
    print("-" * 50)
    for domain, config in sorted(DOMAIN_CONFIGS.items()):
        n_src = len(config.get("sources", []))
        n_card = len(config.get("core_cards", {}))
        print(f"{config['emoji']} {domain:<13} {config['name']:<20} {n_src:>4} {n_card:>5}")


# ─── 命令行接口 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·统一知识库引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_knowledge_hub.py fetch                     # 更新所有知识域
  lh_knowledge_hub.py fetch --domain python     # 只更新 Python
  lh_knowledge_hub.py fetch --force             # 强制全量刷新
  lh_knowledge_hub.py status                    # 总览所有知识域
  lh_knowledge_hub.py status --domain docker    # 单个知识域详情
  lh_knowledge_hub.py list                      # 列出所有知识域
  lh_knowledge_hub.py check                     # 检查哪些需要更新
        """
    )
    parser.add_argument("action", nargs="?", default="status",
                        choices=["fetch", "status", "list", "check", "index"])
    parser.add_argument("--domain", "-d", type=str, help="指定知识域 (逗号分隔多个)")
    parser.add_argument("--force", action="store_true", help="强制全量刷新")
    parser.add_argument("--local", action="store_true", help="使用本地路径")

    args = parser.parse_args()
    kb_base = determine_base(args.local)
    ensure_dir(kb_base)

    # 要处理的知识域
    if args.domain:
        domains = [d.strip() for d in args.domain.split(",")]
        invalid = [d for d in domains if d not in DOMAIN_CONFIGS]
        if invalid:
            print(f"❌ 未知知识域: {', '.join(invalid)}")
            print(f"   可用: {', '.join(DOMAIN_CONFIGS.keys())}")
            sys.exit(1)
    else:
        domains = list(DOMAIN_CONFIGS.keys())

    # ── list ──
    if args.action == "list":
        list_domains()
        return

    # ── status ──
    if args.action == "status":
        if len(domains) == 1 and args.domain:
            domain = domains[0]
            dk = kb_base / domain
            v = load_version(dk)
            config = DOMAIN_CONFIGS[domain]
            files = list(dk.glob("*")) if dk.exists() else []
            total_files = len([f for f in files if not f.name.startswith("kb_version") and f.name != "INDEX.md"])
            total_size = sum(f.stat().st_size for f in files)

            print(f"\n{config['emoji']} {config['name']} ({domain})")
            print(f"   路径: {dk}")
            print(f"   文件: {total_files} 个 ({total_size//1024}KB)")
            print(f"   上次更新: {v.get('last_fetch', '从未')}")
            print(f"   抓取次数: {v.get('fetch_count', 0)}")

            last_results = v.get("last_results", {})
            if last_results:
                print(f"   上次结果: 源 {last_results.get('sources_updated',0)}↑ "
                      f"{last_results.get('sources_skipped',0)}→ "
                      f"{last_results.get('sources_failed',0)}↓ "
                      f"| 知识卡 {last_results.get('cards_written',0)}")
        else:
            # 总览
            print(f"\n{'域':<14} {'名称':<18} {'文件':>5} {'大小':>8} {'上次更新':<12} {'状态'}")
            print("-" * 75)
            for domain in domains:
                dk = kb_base / domain
                config = DOMAIN_CONFIGS[domain]
                emoji = config['emoji']
                name = config['name']

                if not dk.exists():
                    print(f"{emoji} {domain:<11} {name:<18} {'—':>5} {'—':>8} {'—':<12} ⚪ 未初始化")
                    continue

                files = [f for f in dk.glob("*") if not f.name.startswith("kb_version") and f.name != "INDEX.md"]
                n = len(files)
                sz = sum(f.stat().st_size for f in files)
                v = load_version(dk)
                last = (v.get("last_fetch", "—") or "—")[:10]
                lr = v.get("last_results", {})
                ok = lr.get("sources_failed", 0) == 0 if lr else True
                status_icon = "🟢" if ok else "🟡" if lr.get("sources_failed", 0) < 3 else "🔴"
                print(f"{emoji} {domain:<11} {name:<18} {n:>5} {sz//1024:>5}KB {last:<12} {status_icon}")
            print()
        return

    # ── check ──
    if args.action == "check":
        need_fetch = []
        for domain in domains:
            dk = kb_base / domain
            ensure_dir(dk)
            if should_fetch(dk):
                need_fetch.append(domain)
        if need_fetch:
            print(f"FETCH_NEEDED: {', '.join(need_fetch)}")
            sys.exit(0)
        else:
            print("ALL_UP_TO_DATE")
            sys.exit(1)

    # ── index ──
    if args.action == "index":
        for domain in domains:
            dk = kb_base / domain
            if dk.exists():
                generate_index(dk, domain)
                print(f"📑 {domain} 索引已生成")
        generate_master_index(kb_base)
        print(f"📑 总索引已生成: {kb_base / 'MASTER_INDEX.md'}")
        return

    # ── fetch ──
    if args.action == "fetch":
        grand_ok = grand_fail = grand_skip = 0
        for i, domain in enumerate(domains):
            dk = kb_base / domain
            ensure_dir(dk)
            config = DOMAIN_CONFIGS[domain]

            if not args.force and not should_fetch(dk):
                v = load_version(dk)
                print(f"⏭️  {config['emoji']} {config['name']}: 间隔不足{FETCH_INTERVAL_HOURS}h, 跳过 (上次: {v.get('last_fetch','—')[:16]})")
                continue

            if i > 0:
                print()
            print(f"📚 {config['emoji']} {config['name']} [{domain}]")

            results = fetch_domain(domain, dk, force=args.force)

            if "error" in results:
                print(f"  💥 {results['error']}")
                continue

            # 打印来源结果
            for sid, sres in results.get("sources", {}).items():
                status = sres.get("status", "?")
                name = ""
                for s in config.get("sources", []):
                    if s["id"] == sid:
                        name = s["name"]
                        break
                if status == "ok":
                    print(f"  ✅ {name}")
                    grand_ok += 1
                elif status == "skipped":
                    grand_skip += 1
                elif status == "failed":
                    print(f"  ❌ {name}: {sres.get('msg', '?')}")
                    grand_fail += 1

            n_cards = len(results.get("cards", {}))
            if n_cards:
                print(f"  📝 知识卡: {n_cards} 张")

            print(f"  📊 {results.get('summary', '')}")
            generate_index(dk, domain)

        generate_master_index(kb_base)
        print(f"\n{'='*50}")
        print(f"🏁 全量更新完成: {grand_ok}↑ {grand_skip}→ {grand_fail}↓")
        print(f"📂 {kb_base}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
