#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_FILL_CS_SY-D4F36685
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-NOTION-CS-SYSTEMS-FILL-v1.0
"""
🐉 龍魂 · 计算机科学知识库填充（系统/网络/安全/AI 轻量版）

向 Notion 数据库「计算机科学知识库」批量写入操作系统、计算机网络、数据库、并发、安全与 AI 基础条目。
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path

import requests


NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"
DB_ID = "3367125a9c9f808a9692f0c6752e92fa"


def get_token() -> str:
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "notion_config.json"
    data = json.load(open(cfg_path, encoding="utf-8"))
    return data.get("notion_token") or data.get("token")


def headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def guard(text: str) -> str:
    return text.replace("龙", "龍")


def dna(name: str) -> str:
    h = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CS-SYS-{h}-UID9622"


def rich_text(text: str):
    return {"rich_text": [{"text": {"content": guard(text)}}]}


def title(text: str):
    return {"title": [{"text": {"content": guard(text)}}]}


def select(name: str):
    return {"select": {"name": name}}


def status(name: str):
    return {"status": {"name": name}}


def multi_select(names: list):
    return {"multi_select": [{"name": n} for n in names]}


def number(val: float):
    return {"number": val}


TOPICS = [
    {
        "name": "进程与线程 (Process & Thread)",
        "desc": "进程是操作系统资源分配的基本单位，拥有独立地址空间；线程是 CPU 调度的基本单位，共享进程资源。理解二者区别是并发编程和系统调优的根基。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "性能优化", "所有编程"],
        "hours": 4,
        "code": "import threading, os\n\ndef worker():\n    print(f'thread in pid {os.getpid()}')\n\nt = threading.Thread(target=worker)\nt.start()\nt.join()",
        "formula": "上下文切换: 线程 < 进程 | 通信: 线程共享内存，进程需 IPC",
        "misconception": "多线程在 Python GIL 下不能实现真正并行计算；计算密集应使用多进程。",
    },
    {
        "name": "CPU 调度算法 (CPU Scheduling)",
        "desc": "操作系统决定哪个进程/线程在 CPU 上运行的策略。常见算法包括先来先服务、短作业优先、时间片轮转、多级反馈队列等，直接影响系统响应和吞吐量。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "性能优化", "OS"],
        "hours": 3,
        "code": "# 时间片轮转伪代码\nqueue = [p1, p2, p3]\nwhile queue:\n    p = queue.pop(0)\n    run(p, time_quantum)\n    if not p.done:\n        queue.append(p)",
        "formula": "周转时间 = 完成时间 - 到达时间 | 等待时间 = 周转时间 - 执行时间",
        "misconception": "调度算法不是越公平越好；实时系统更关注确定性响应。",
    },
    {
        "name": "内存管理 (Memory Management)",
        "desc": "操作系统通过虚拟内存、分页、分段、段页式机制为进程提供隔离且连续的地址空间。页表、TLB、缺页中断是其核心概念。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "性能优化", "内存调试"],
        "hours": 5,
        "code": "# 查看 Linux 进程内存映射\n# cat /proc/<pid>/maps",
        "formula": "虚拟地址 → 页表 → 物理地址 | 缺页时触发 Page Fault",
        "misconception": "虚拟内存不是无限内存；过度使用会导致 swap 抖动。",
    },
    {
        "name": "文件系统 (File System)",
        "desc": "操作系统用于组织、存储、检索和管理持久数据的机制。常见文件系统包括 ext4、NTFS、APFS。关键概念包括 inode、目录项、块、日志和权限。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "所有编程", "运维实践"],
        "hours": 3,
        "code": "# Python 路径与文件操作\nfrom pathlib import Path\np = Path('/tmp/test.txt')\np.write_text('龍魂')\nprint(p.read_text())",
        "formula": "inode 存储元数据 | 目录项映射文件名 → inode",
        "misconception": "删除文件只是删除目录项；磁盘数据可能仍存在直到覆盖。",
    },
    {
        "name": "TCP/IP 协议栈 (TCP/IP Stack)",
        "desc": "互联网通信的基础协议族，分为应用层、传输层、网络层、链路层。TCP 提供可靠连接，IP 负责寻址和路由。理解它是后端开发和网络排查的根基。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有TCP连接", "HTTP/HTTPS", "系统设计"],
        "hours": 6,
        "code": "import socket\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.connect(('example.com', 80))\ns.sendall(b'GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n')\nprint(s.recv(1024).decode())\ns.close()",
        "formula": "TCP 三次握手建立连接 | 四次挥手释放连接",
        "misconception": "TCP 可靠不等于不会断连；应用层仍需处理超时和重连。",
    },
    {
        "name": "HTTP/HTTPS 协议",
        "desc": "应用层最主流的请求-响应协议。HTTP 无状态，依靠方法（GET/POST/PUT/DELETE）、状态码、头部实现语义。HTTPS 在 HTTP 下加入 TLS/SSL 加密。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["HTTP/HTTPS", "Web服务器", "API调用前置检查"],
        "hours": 4,
        "code": "import requests\nr = requests.get('https://api.github.com')\nprint(r.status_code, r.headers.get('content-type'))",
        "formula": "请求 = 方法 + URI + 头部 + 正文 | 响应 = 状态码 + 头部 + 正文",
        "misconception": "GET 请求体在标准中无意义；参数应放 URL，敏感信息用 POST + HTTPS。",
    },
    {
        "name": "DNS 域名解析",
        "desc": "将人类可读的域名转换为 IP 地址的分布式系统。解析过程涉及浏览器缓存、系统缓存、递归解析器和各级权威 DNS 服务器。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L1 入门",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["HTTP/HTTPS", "Web服务器", "系统设计"],
        "hours": 2,
        "code": "import socket\nprint(socket.gethostbyname('example.com'))",
        "formula": "递归查询: 客户端 → 递归解析器 → 根 → 顶级域 → 权威域",
        "misconception": "DNS 不是单次查询；缓存和 TTL 对性能与安全都至关重要。",
    },
    {
        "name": "负载均衡 (Load Balancing)",
        "desc": "将请求分发到多台服务器的技术，用于提升可用性、扩展性和性能。常见策略包括轮询、加权轮询、最少连接、一致性哈希等。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["高并发后端", "系统设计", "性能优化"],
        "hours": 3,
        "code": "# 一致性哈希伪代码\nservers = ['A', 'B', 'C']\nrequest_hash = hash(request_id)\nserver = servers[request_hash % len(servers)]",
        "formula": "可用性 = MTBF / (MTBF + MTTR) | 理想负载均匀分布",
        "misconception": "负载均衡不是无限的；后端容量和会话一致性仍需设计。",
    },
    {
        "name": "数据库索引 (Database Index)",
        "desc": "加速数据库查询的数据结构，常见实现为 B+ 树和哈希索引。索引能显著减少磁盘 I/O，但会增加写操作开销和存储空间。",
        "category": "数据与人工智能",
        "subcategory": "数据科学",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["数据库", "性能优化", "系统设计"],
        "hours": 4,
        "code": "-- SQL 创建索引示例\nCREATE INDEX idx_user_email ON users(email);\nSELECT * FROM users WHERE email = 'test@example.com';",
        "formula": "B+ 树索引: 查询 O(log n) | 哈希索引: 等值查询 O(1) 平均",
        "misconception": "索引不是越多越好；写少读多的场景才适合大量索引。",
    },
    {
        "name": "SQL 与关系型数据库",
        "desc": "使用结构化查询语言管理的关系型数据存储系统，如 MySQL、PostgreSQL。核心概念包括表、行、列、主键、外键、事务和 ACID。",
        "category": "数据与人工智能",
        "subcategory": "数据科学",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["数据库", "所有编程", "系统设计"],
        "hours": 5,
        "code": "-- 事务示例\nBEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;",
        "formula": "ACID: 原子性、一致性、隔离性、持久性",
        "misconception": "SQL 数据库不适合所有场景；高并发写和灵活 schema 可考虑 NoSQL。",
    },
    {
        "name": "锁与并发控制 (Locking & Concurrency)",
        "desc": "多线程/多进程环境下协调资源访问的机制。常见锁包括互斥锁、读写锁、自旋锁；数据库中还有乐观锁和悲观锁。并发控制不当会导致死锁、竞态条件和数据不一致。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["高并发后端", "数据库", "所有编程"],
        "hours": 5,
        "code": "import threading\nlock = threading.Lock()\ncounter = 0\n\ndef inc():\n    global counter\n    with lock:\n        counter += 1",
        "formula": "互斥锁: 同一时间只有一个线程进入临界区 | 死锁四条件: 互斥、占有等待、不可剥夺、循环等待",
        "misconception": "加锁不是越多越好；粒度太粗会降低并行度，太细易死锁。",
    },
    {
        "name": "缓存策略 (Caching)",
        "desc": "用更快但容量更小的存储层暂存热点数据，降低后端压力和延迟。常见策略包括 LRU、LFU、TTL，常见工具包括 Redis、Memcached。",
        "category": "系统与网络",
        "subcategory": "系统管理",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["缓存", "性能优化", "高并发后端"],
        "hours": 3,
        "code": "from functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)",
        "formula": "缓存命中率 = 命中次数 / 总请求次数 | 缓存失效三大问题: 穿透、击穿、雪崩",
        "misconception": "缓存不能替代数据库；强一致性场景必须设计缓存更新策略。",
    },
    {
        "name": "对称加密与非对称加密",
        "desc": "对称加密使用同一密钥加解密，速度快，适合大数据量；非对称加密使用公钥/私钥对，适合密钥交换和数字签名。现代安全通信常结合二者，如 TLS。",
        "category": "安全与防护",
        "subcategory": "基础安全",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["安全防护"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["安全审计", "HTTP/HTTPS", "系统设计"],
        "hours": 5,
        "code": "# Python 非对称签名示例（概念）\nfrom cryptography.hazmat.primitives import hashes, serialization\nfrom cryptography.hazmat.primitives.asymmetric import padding, rsa\nkey = rsa.generate_private_key(public_exponent=65537, key_size=2048)",
        "formula": "对称: 加密快、密钥分发难 | 非对称: 加密慢、无需共享私钥",
        "misconception": "非对称加密不是无条件安全；密钥长度和随机数质量决定安全性。",
    },
    {
        "name": "哈希函数与数字签名",
        "desc": "哈希函数将任意长度输入映射为固定长度摘要，具有单向性和抗碰撞性。数字签名结合哈希与非对称加密，用于验证消息完整性和身份。",
        "category": "安全与防护",
        "subcategory": "基础安全",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["安全防护"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["安全审计", "API调用前置检查", "系统设计"],
        "hours": 4,
        "code": "import hashlib\nh = hashlib.sha256(b'龍魂系统').hexdigest()\nprint(h)",
        "formula": "数字签名 = 私钥加密(哈希(消息)) | 验证 = 公钥解密后对比哈希",
        "misconception": "哈希不是加密；哈希不可逆，不能从摘要恢复原文。",
    },
    {
        "name": "Web 安全基础 (OWASP Top 10)",
        "desc": "开放 Web 应用安全项目总结的十大常见风险，包括注入、失效身份验证、敏感数据泄露、XML 外部实体、访问控制失效、安全配置错误、跨站脚本 XSS 等。",
        "category": "安全与防护",
        "subcategory": "基础安全",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["安全防护"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["安全审计", "代码审查", "Web服务器"],
        "hours": 4,
        "code": "# 防 SQL 注入：使用参数化查询\nimport sqlite3\nconn = sqlite3.connect(':memory:')\ncur = conn.cursor()\nuser_input = \"'; DROP TABLE users; --\"\ncur.execute('SELECT * FROM users WHERE name = ?', (user_input,))",
        "formula": "最小权限原则 + 输入验证 + 输出编码 = 基础防御",
        "misconception": "前端校验不能替代后端校验；恶意请求可绕过浏览器。",
    },
    {
        "name": "机器学习基础 (Machine Learning Basics)",
        "desc": "让计算机从数据中自动学习规律的学科。主要分为监督学习、无监督学习和强化学习。核心流程包括数据收集、特征工程、模型训练、评估和部署。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["数据分析/AI", "所有深度学习训练", "面试"],
        "hours": 6,
        "code": "# scikit-learn 线性回归示例\nfrom sklearn.linear_model import LinearRegression\nX = [[1], [2], [3], [4]]\ny = [2, 4, 6, 8]\nmodel = LinearRegression().fit(X, y)\nprint(model.predict([[5]]))",
        "formula": "模型 = 假设函数 + 损失函数 + 优化算法",
        "misconception": "机器学习不是魔法；模型质量高度依赖数据和特征。",
    },
    {
        "name": "神经网络与反向传播",
        "desc": "神经网络由多层神经元组成，通过激活函数引入非线性。反向传播算法利用链式法则高效计算损失函数对各参数的梯度，是深度学习训练的基石。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["深度学习特征提取", "所有深度学习训练", "面试"],
        "hours": 8,
        "code": "import torch\n# 定义一个简单的全连接层\nlayer = torch.nn.Linear(10, 5)\nx = torch.randn(2, 10)\ny = layer(x)\nprint(y.shape)",
        "formula": "前向: y = f(Wx + b) | 反向: ∂L/∂W = ∂L/∂y · ∂y/∂W",
        "misconception": "层数越深不一定越好；过深会导致梯度消失/爆炸和过拟合。",
    },
    {
        "name": "Transformer 架构",
        "desc": "基于自注意力机制的序列建模架构，摒弃了循环和卷积，能高效并行处理长序列。GPT、BERT、T5 等主流大模型均基于 Transformer。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L2-L3",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["所有深度学习训练", "自然语言处理", "系统设计"],
        "hours": 8,
        "code": "import torch.nn as nn\n# PyTorch 多头注意力\nmha = nn.MultiheadAttention(embed_dim=64, num_heads=8)\nquery = torch.rand(10, 2, 64)  # (seq, batch, embed)\noutput, attn = mha(query, query, query)",
        "formula": "Attention(Q,K,V) = softmax(QK^T / √d_k) V",
        "misconception": "Transformer 不是无限制长序列；自注意力复杂度为 O(n²)。",
    },
    {
        "name": "版本控制 Git",
        "desc": "分布式版本控制系统，用于跟踪代码变更、支持多人协作和分支管理。核心概念包括 commit、branch、merge、rebase、remote 和工作区/暂存区/仓库。",
        "category": "工具与实践",
        "subcategory": "开发工具",
        "difficulty": "L1 入门",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["工具实践"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "代码审查", "学习/复习"],
        "hours": 4,
        "code": "# 常用 Git 工作流\ngit checkout -b feature/new-thing\ngit add .\ngit commit -m \"feat: add new thing\"\ngit push -u origin feature/new-thing",
        "formula": "commit 是不可变快照 | branch 是指向 commit 的指针",
        "misconception": "Git 不是备份工具；误操作仍可丢失工作，需理解 reflog。",
    },
    {
        "name": "正则表达式 (Regular Expression)",
        "desc": "用于描述字符串模式的强大工具。广泛应用于文本搜索、替换、校验和解析。掌握元字符、量词、分组和回溯是基础。",
        "category": "编程与开发",
        "subcategory": "编程语言",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "代码审查", "学习/复习"],
        "hours": 3,
        "code": "import re\n# 匹配邮箱\npattern = r'[\\w.-]+@[\\w.-]+\\.\\w+'\nprint(re.findall(pattern, 'contact@example.com'))",
        "formula": "正则引擎: NFA/DFA | 最坏回溯可指数级 O(2^n)",
        "misconception": "正则可以解决一切文本问题；复杂解析应使用专用解析器。",
    },
    {
        "name": "RESTful API 设计",
        "desc": "基于 HTTP 协议的资源化接口设计风格。通过 URL 定位资源、HTTP 方法表达操作、状态码反馈结果，是现代 Web 服务的主流设计范式。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["API网关", "Web服务器", "系统设计"],
        "hours": 3,
        "code": "# RESTful 路由示例（Flask 风格）\n# GET    /users       -> 列出用户\n# POST   /users       -> 创建用户\n# GET    /users/{id}  -> 查询用户\n# PUT    /users/{id}  -> 更新用户\n# DELETE /users/{id}  -> 删除用户",
        "formula": "资源 = URI | 操作 = HTTP Method | 结果 = Status Code + Representation",
        "misconception": "REST 不是严格标准；它是一种架构风格和约束集合。",
    },
]


def create_page(topic: dict) -> dict:
    properties = {
        "知识点名称": title(topic["name"]),
        "描述": rich_text(topic["desc"]),
        "分类": select(topic["category"]),
        "子分类": select(topic["subcategory"]),
        "学习优先级": select(topic["priority"]),
        "难度等级": select(topic["difficulty"]),
        "是否核心": select(topic["core"]),
        "标签": multi_select(topic["tags"]),
        "用途标签": multi_select(topic["use_tags"]),
        "应用场景": multi_select(topic["scenes"]),
        "预计学习时长（小时）": number(topic["hours"]),
        "PY代码示例": rich_text(topic["code"]),
        "核心公式": rich_text(topic["formula"]),
        "常见误区": rich_text(topic["misconception"]),
        "DNA追溯": rich_text(dna(topic["name"])),
        "来源/参考": rich_text("龍魂系统 · 计算机科学知识库填充脚本 v1.0"),
        "关联知识点": rich_text("进程, 线程, 网络, 数据库, 加密, 机器学习, Git, 缓存, 负载均衡"),
        "关键词索引": multi_select(["系统", "网络", "安全", "AI", "数据库", "并发"]),
        "学习状态": status("未开始"),
        "掌握程度": select("未掌握"),
    }
    return {
        "parent": {"database_id": DB_ID},
        "properties": properties,
    }


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始向 Notion 写入 {len(TOPICS)} 条系统/网络/安全/AI 知识点...")

    created = 0
    failed = 0
    for topic in TOPICS:
        payload = create_page(topic)
        r = requests.post(f"{API_BASE}/pages", headers=headers(), json=payload)
        if r.status_code == 200:
            created += 1
            print(f"  ✅ {topic['name']}")
        else:
            failed += 1
            print(f"  ❌ {topic['name']}: {r.status_code} {r.text[:100]}")
        time.sleep(0.3)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 完成: {created} 条成功, {failed} 条失败")


if __name__ == "__main__":
    main()
