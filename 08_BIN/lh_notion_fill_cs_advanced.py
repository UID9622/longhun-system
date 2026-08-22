#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_NOTION_FILL_CS_AD-39F445DC
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-NOTION-CS-ADVANCED-FILL-v1.0
"""
🐉 龍魂 · 计算机科学知识库填充（进阶/工程/前沿轻量版）
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
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CS-ADV-{h}-UID9622"


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
        "name": "OSI 七层模型",
        "desc": "开放式系统互联参考模型，将网络通信划分为物理层、数据链路层、网络层、传输层、会话层、表示层和应用层。是理解网络协议分层设计的基础框架。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L1 入门",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["HTTP/HTTPS", "系统设计", "学习/复习"],
        "hours": 3,
        "code": "# 七层速记口诀\n# 物数网传会表应\n# 请记住：每一层为上层提供服务，上层不感知下层细节",
        "formula": "上层数据 + 本层首部 = 本层 PDU",
        "misconception": "OSI 是理论模型，实际互联网以 TCP/IP 四层模型为主。",
    },
    {
        "name": "TLS/SSL 握手过程",
        "desc": "HTTPS 安全通信建立前的密钥协商过程。通过非对称加密交换对称密钥，后续通信使用对称加密，兼顾安全与效率。TLS 1.3 简化了握手，提升了性能。",
        "category": "安全与防护",
        "subcategory": "基础安全",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["安全防护"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["HTTP/HTTPS", "安全审计", "系统设计"],
        "hours": 4,
        "code": "# TLS 1.3 握手简化为 1-RTT（往返）\n# 客户端: ClientHello + 密钥共享\n# 服务器: ServerHello + 证书 + 确认\n# 双方派生会话密钥后开始加密通信",
        "formula": "前向安全 = 即使长期私钥泄露，历史会话密钥也无法推导",
        "misconception": "TLS 只加密数据；它同时提供身份认证和完整性校验。",
    },
    {
        "name": "OAuth 2.0 与 JWT",
        "desc": "OAuth 2.0 是授权框架，允许第三方应用在不获取用户密码的情况下访问资源。JWT 是一种自包含的令牌格式，常用于在授权后携带用户声明。",
        "category": "安全与防护",
        "subcategory": "基础安全",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["安全防护"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["API网关", "系统设计", "安全审计"],
        "hours": 4,
        "code": "# JWT 结构: header.payload.signature\n# 不要在 JWT 中放敏感明文；用 HTTPS 传输",
        "formula": "授权 ≠ 认证；OAuth 解决授权，OpenID Connect 解决认证",
        "misconception": "JWT 不是默认安全；密钥保管、过期时间和传输通道都决定安全性。",
    },
    {
        "name": "数据库事务隔离级别",
        "desc": "数据库为保证并发事务一致性而定义的隔离程度，从低到高为读未提交、读已提交、可重复读、串行化。隔离级别越高，并发性能通常越低。",
        "category": "数据与人工智能",
        "subcategory": "数据科学",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["数据库", "高并发后端", "系统设计"],
        "hours": 4,
        "code": "-- SQL 设置隔离级别\nSET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;",
        "formula": "脏读 < 不可重复读 < 幻读 | 隔离级别越高，锁越多",
        "misconception": "可重复读在某些数据库（如 MySQL InnoDB）下已能避免幻读，不依赖串行化。",
    },
    {
        "name": "CAP 定理",
        "desc": "分布式系统理论基石：一致性、可用性、分区容错性三者不可同时满足。网络分区必然发生时，系统只能在一致性和可用性之间做权衡。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "架构设计", "面试"],
        "hours": 2,
        "code": "# 分布式系统选型\n# CP: ZooKeeper, etcd\n# AP: Cassandra, DynamoDB\n# CA: 单机数据库（无分区场景）",
        "formula": "Consistency + Availability + Partition tolerance: 三者最多同时满足两个",
        "misconception": "CAP 不是非黑即白；实际系统通过延迟、重试和副本策略做连续权衡。",
    },
    {
        "name": "Raft 共识算法",
        "desc": "为易于理解而设计的分布式一致性算法。通过领导者选举、日志复制和安全性保证，在多数节点存活时保持一致。广泛应用于 etcd、Consul、TiKV 等系统。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L2-L3",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "架构设计", "面试"],
        "hours": 6,
        "code": "# Raft 核心状态\n# Follower -> Candidate -> Leader\n# 所有写请求由 Leader 处理并复制到多数 Follower",
        "formula": "多数派提交 = 至少 (N/2 + 1) 个节点确认",
        "misconception": "Raft 不是最快的共识算法；Paxos 变体在某些场景下性能更高但更复杂。",
    },
    {
        "name": "微服务架构",
        "desc": "将单一应用拆分为一组小型、独立部署的服务，每个服务围绕业务能力构建，通过轻量通信机制协作。优点是独立扩展和团队自治，缺点是分布式复杂性。",
        "category": "系统与网络",
        "subcategory": "网络技术",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["系统网络"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "架构设计", "高并发后端"],
        "hours": 4,
        "code": "# 微服务拆分原则\n# 单一职责、独立部署、独立数据库、API 契约、可观测性",
        "formula": "拆分收益 > 分布式成本 时才值得微服务化",
        "misconception": "微服务不是银弹；小团队或简单业务使用单体更合适。",
    },
    {
        "name": "容器与 Docker",
        "desc": "容器是轻量级的操作系统级虚拟化技术，共享主机内核但相互隔离。Docker 提供镜像构建、分发和运行标准，是现代 DevOps 和微服务部署的基础。",
        "category": "工具与实践",
        "subcategory": "运维实践",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["工具实践"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "高并发后端", "运维实践"],
        "hours": 4,
        "code": "# Dockerfile 示例\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"python3\", \"app.py\"]",
        "formula": "容器 = 镜像 + 运行时隔离（namespace + cgroup）",
        "misconception": "容器不是虚拟机；容器共享内核，更轻量但隔离性较弱。",
    },
    {
        "name": "Kubernetes 基础",
        "desc": "开源容器编排平台，用于自动化部署、扩展和管理容器化应用。核心概念包括 Pod、Deployment、Service、ConfigMap、Ingress 和 Namespace。",
        "category": "工具与实践",
        "subcategory": "运维实践",
        "difficulty": "L2-L3",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["工具实践"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "高并发后端", "运维实践"],
        "hours": 8,
        "code": "# 查看 Pod\nkubectl get pods -n longhun\n# 扩展副本数\nkubectl scale deployment longhun-api --replicas=3",
        "formula": "Pod 是最小调度单位 | Deployment 管理无状态副本 | Service 暴露访问入口",
        "misconception": "Kubernetes 不是部署平台本身；它需要容器运行时和集群基础设施。",
    },
    {
        "name": "CI/CD 持续集成/持续部署",
        "desc": "通过自动化流水线频繁集成代码、运行测试并部署到生产环境。CI 关注自动构建和测试，CD 关注自动发布和部署，目标是缩短反馈周期、降低发布风险。",
        "category": "工具与实践",
        "subcategory": "开发工具",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["工具实践"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "代码审查", "运维实践"],
        "hours": 3,
        "code": "# GitHub Actions 工作流骨架\nname: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pip install pytest\n      - run: pytest",
        "formula": "自动化程度越高，人为失误越少，发布越快",
        "misconception": "CI/CD 不只是自动化部署；测试和回滚策略同样关键。",
    },
    {
        "name": "设计模式 (Design Patterns)",
        "desc": "软件工程中针对常见问题的可复用解决方案。经典分类包括创建型（单例、工厂）、结构型（适配器、装饰器）、行为型（观察者、策略）。",
        "category": "编程与开发",
        "subcategory": "软件工程",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "代码审查", "架构设计"],
        "hours": 6,
        "code": "# Python 单例模式（简化）\nclass Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
        "formula": "模式 = 反复出现的问题 + 经过验证的解决方案 + 使用场景",
        "misconception": "设计模式不是代码模板；滥用模式会导致过度设计。",
    },
    {
        "name": "测试驱动开发 TDD",
        "desc": "先编写失败测试，再写最小实现让测试通过，最后重构代码。TDD 强调快速反馈和可测试设计，是提升代码质量和可维护性的实践方法。",
        "category": "编程与开发",
        "subcategory": "软件工程",
        "difficulty": "L1-L2",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["编程语言"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["所有编程", "代码审查", "学习/复习"],
        "hours": 4,
        "code": "# 红-绿-重构循环\n# 1. 写测试并确认失败\n# 2. 写最少代码让测试通过\n# 3. 重构保持测试通过",
        "formula": "TDD 周期 = 红（失败）→ 绿（通过）→ 重构",
        "misconception": "TDD 不保证无 bug；它通过快速反馈降低缺陷成本和提升设计。",
    },
    {
        "name": "机器学习评估指标",
        "desc": "衡量模型性能的量化标准，包括准确率、精确率、召回率、F1、ROC-AUC、混淆矩阵等。不同业务场景关注不同指标，如召回率对医疗诊断更重要。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L1-L2",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["数据分析/AI", "所有深度学习训练", "面试"],
        "hours": 4,
        "code": "from sklearn.metrics import precision_score, recall_score, f1_score\ny_true = [0, 1, 1, 0, 1]\ny_pred = [0, 1, 0, 0, 1]\nprint(f1_score(y_true, y_pred))",
        "formula": "F1 = 2 · Precision · Recall / (Precision + Recall)",
        "misconception": "准确率高不代表模型好；类别不平衡时准确率先失效。",
    },
    {
        "name": "深度学习优化器",
        "desc": "用于更新神经网络参数以最小化损失函数的算法。SGD、Momentum、AdaGrad、RMSprop、Adam 是主流优化器。Adam 因自适应学习率在实践中应用最广。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L2 进阶",
        "priority": "P0-必学",
        "core": "🔴 底座（必须）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["所有深度学习训练", "性能优化", "面试"],
        "hours": 5,
        "code": "import torch.optim as optim\noptimizer = optim.Adam(model.parameters(), lr=1e-3)\noptimizer.zero_grad()\nloss.backward()\noptimizer.step()",
        "formula": "θ = θ - α · m̂ / (√v̂ + ε)（Adam 更新规则）",
        "misconception": "Adam 不是永远最好；某些任务上 SGD + Momentum 泛化更优。",
    },
    {
        "name": "自然语言处理 NLP 基础",
        "desc": "让计算机理解、处理和生成人类语言的学科。从早期的词袋模型、TF-IDF、Word2Vec，到如今的预训练语言模型和 Transformer，NLP 已成为大模型核心。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L2 进阶",
        "priority": "P1-重要",
        "core": "🟡 插件（可选）",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["所有深度学习训练", "数据分析/AI", "面试"],
        "hours": 6,
        "code": "# 简单文本分词 + TF-IDF\nfrom sklearn.feature_extraction.text import TfidfVectorizer\ncorpus = ['龍魂系统', '龍芯主权']\nv = TfidfVectorizer()\nprint(v.fit_transform(corpus).toarray())",
        "formula": "TF-IDF = 词频 × 逆文档频率",
        "misconception": "NLP 不只是分词和情感分析；现代 NLP 核心是语义表示和生成。",
    },
    {
        "name": "计算机视觉 CV 基础",
        "desc": "让计算机从图像和视频中提取信息的学科。经典方法包括卷积神经网络 CNN、目标检测、图像分割、特征提取。ResNet、YOLO、ViT 是里程碑模型。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L2 进阶",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["数据AI"],
        "use_tags": ["🎨 视觉/渲染"],
        "scenes": ["数据分析/AI", "图像压缩", "学习/复习"],
        "hours": 6,
        "code": "import torch.nn as nn\n# 简单卷积层\nconv = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)\nprint(conv)",
        "formula": "卷积: 局部连接 + 权值共享 → 提取空间特征",
        "misconception": "CV 不只是图像分类；检测、分割、生成、3D 视觉都是核心方向。",
    },
    {
        "name": "强化学习 Reinforcement Learning",
        "desc": "智能体通过与环境交互、获取奖励信号来学习最优策略的范式。核心概念包括状态、动作、奖励、策略、价值函数。AlphaGo 和 ChatGPT 的 RLHF 都源于此。",
        "category": "数据与人工智能",
        "subcategory": "人工智能",
        "difficulty": "L3 专家",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["数据AI"],
        "use_tags": ["🧠 AI/模型"],
        "scenes": ["所有深度学习训练", "数据分析/AI", "面试"],
        "hours": 8,
        "code": "# RL 核心循环\n# for each step:\n#   action = policy(state)\n#   next_state, reward = env.step(action)\n#   update policy/value to maximize cumulative reward",
        "formula": "目标: 最大化累计折扣回报 G_t = Σ γ^k · R_{t+k+1}",
        "misconception": "强化学习不是监督学习；它从延迟、稀疏的奖励中学习。",
    },
    {
        "name": "边缘计算 Edge Computing",
        "desc": "将计算、存储和网络能力下沉到靠近数据源的边缘节点，以降低延迟、节省带宽并保护隐私。适用于物联网、自动驾驶、工业控制等场景。",
        "category": "前瞻交叉与主权技术",
        "subcategory": "交叉领域",
        "difficulty": "L2 进阶",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["交叉前瞻"],
        "use_tags": ["⚙️ 系统/底层"],
        "scenes": ["系统设计", "架构设计", "数据分析/AI"],
        "hours": 3,
        "code": "# 边缘 vs 云端权衡\n# 低延迟、数据隐私、离线运行 -> 边缘\n# 大算力、海量数据、集中训练 -> 云端",
        "formula": "延迟 = 传输延迟 + 处理延迟 + 返回延迟",
        "misconception": "边缘计算不是要替代云；而是云边端协同。",
    },
    {
        "name": "量子计算基础",
        "desc": "利用量子力学叠加和纠缠现象进行计算的新型计算范式。量子比特可同时处于 0 和 1 的叠加态，有望在密码学、药物发现、优化问题上实现指数级加速。",
        "category": "前瞻交叉与主权技术",
        "subcategory": "前沿技术",
        "difficulty": "L4 前沿",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["新兴领域"],
        "use_tags": ["⚛️ 量子/抽象"],
        "scenes": ["量子力学", "学习/复习", "架构设计"],
        "hours": 8,
        "code": "# Qubit 状态向量表示\n# |ψ⟩ = α|0⟩ + β|1⟩，其中 |α|² + |β|² = 1",
        "formula": "量子门 = 酉矩阵 | 测量 = 概率塌缩",
        "misconception": "量子计算机不是万能的；仅对特定问题有优势，且易受噪声影响。",
    },
    {
        "name": "区块链技术基础",
        "desc": "一种去中心化的分布式账本技术，通过密码学哈希、共识机制和链式结构保证数据不可篡改。比特币和以太坊是典型应用，也被用于溯源、存证和数字身份。",
        "category": "前瞻交叉与主权技术",
        "subcategory": "交叉领域",
        "difficulty": "L2 进阶",
        "priority": "P2-了解",
        "core": "⚪ 暂不需要",
        "tags": ["交叉前瞻"],
        "use_tags": ["🔐 安全/加密"],
        "scenes": ["安全审计", "学习/复习", "系统设计"],
        "hours": 4,
        "code": "import hashlib\n# 简单区块哈希链\ndata = 'block_1'\nprev_hash = '0'*64\nblock_hash = hashlib.sha256((data + prev_hash).encode()).hexdigest()\nprint(block_hash)",
        "formula": "区块 = 数据 + 前一区块哈希 + 时间戳 + Nonce",
        "misconception": "区块链不是绝对安全；51% 攻击和私钥丢失仍是风险。",
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
        "关联知识点": rich_text("分布式系统, 网络安全, 数据库, AI, DevOps, 前沿技术"),
        "关键词索引": multi_select(["分布式", "网络安全", "AI", "DevOps", "前沿"]),
        "学习状态": status("未开始"),
        "掌握程度": select("未掌握"),
    }
    return {
        "parent": {"database_id": DB_ID},
        "properties": properties,
    }


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始向 Notion 写入 {len(TOPICS)} 条进阶/工程/前沿知识点...")

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
