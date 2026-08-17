---
dna: '#龍芯⚡️丙午·丙申·壬戌·巳时·䷰革-CLIPBOARD-VAULT-SAVE-V1.0-P1-0c032b9b'
source: clipboard
topic: 安全/审计
tags:
- JS
- Bash
- DNA
- 安全
- 审计
- 安全/审计
timestamp: '2026-08-16T09:52:55+08:00'
content_hash: e967b8ea05861b5b8d4fd2c51f257b7c0d5fe2cad85e59e624e0337d29751f3a
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

# 🐉 龍魂 · 知识图谱节点文档系统

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥时-KG-DOCS-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过


## 📋 核心设计

> **知识图谱不是静态图，是活的导航系统。每个节点点击打开文档面板，呈现该节点的DNA追溯、协议描述、相关链接、关联模块。这才是真知识图谱——不是看，是用。**


## 🏛️ 一、架构设计

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         知识图谱 + 文档系统                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  用户点击节点                                                                                       │
│       │                                                                                             │
│       ▼                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                    文档详情面板                                              │   │
│  │                                                                                             │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │  🧬 DNA: #龍芯⚡️丙午·丙申·庚申·亥时-xxx-UID9622                                   │   │   │
│  │  │  📌 名称: 人格矩阵                                                                   │   │   │
│  │  │  📂 类别: 核心能力                                                                    │   │   │
│  │  │  📝 描述: 24人格协作底座，多Agent调度核心                                            │   │   │
│  │  │  ──────────────────────────────────────────────────────────────────────────────────   │   │   │
│  │  │  📖 详细文档                                                                         │   │   │
│  │  │  人格矩阵是龍魂系统的多智能体协作底座，包含24个人格...                               │   │   │
│  │  │  ──────────────────────────────────────────────────────────────────────────────────   │   │   │
│  │  │  🔗 相关链接                                                                         │   │   │
│  │  │    - 协议: 01_protocols/LH-PERSONA-MATRIX-v2.0.md                                   │   │   │
│  │  │    - 代码: 05_ENGINES/lh_persona_life.py                                             │   │   │
│  │  │    - 文档: https://blog.csdn.net/UID9622/persona                                    │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## 🧬 二、完整代码实现

### 2.1 带文档的知识图谱 `knowledge_with_docs.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂 · 知识图谱 + 文档</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐉</text></svg>">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js">
    </script>

    <style>
        /* ===== 全局 ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #0a0a14;
            color: #e0e0e0;
            min-height: 100vh;
        }

        /* ===== 导航栏 ===== */
        .navbar {
            background: rgba(10, 10, 20, 0.95);
            backdrop-filter: blur(20px);
            padding: 16px 40px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .navbar .logo {
            font-size: 24px;
            font-weight: 700;
            color: #d4af37;
            text-decoration: none;
        }
        .navbar .logo span {
            color: #8a8a9a;
            font-weight: 400;
            font-size: 14px;
        }
        .navbar .nav-links {
            display: flex;
            gap: 32px;
            list-style: none;
        }
        .navbar .nav-links a {
            color: rgba(255, 255, 255, 0.6);
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s;
        }
        .navbar .nav-links a:hover {
            color: #d4af37;
        }
        .navbar .nav-links a.active {
            color: #d4af37;
        }

        /* ===== 布局 ===== */
        .graph-container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 24px 40px 40px;
        }

        .graph-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }
        .graph-header h1 {
            color: #d4af37;
            font-size: 28px;
            font-weight: 700;
        }
        .graph-header h1 .sub {
            color: rgba(255, 255, 255, 0.3);
            font-size: 16px;
            font-weight: 400;
        }

        /* ===== 图谱+文档 ===== */
        .main-layout {
            display: flex;
            gap: 24px;
            min-height: 600px;
        }

        .graph-wrapper {
            flex: 2;
            min-width: 0;
        }

        #knowledge-graph {
            width: 100%;
            height: 600px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(212, 175, 55, 0.1);
            border-radius: 16px;
            overflow: hidden;
        }

        /* ===== 文档面板 ===== */
        .doc-panel {
            flex: 1;
            min-width: 340px;
            max-width: 480px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(212, 175, 55, 0.1);
            border-radius: 16px;
            padding: 24px;
            overflow-y: auto;
            max-height: 600px;
            transition: all 0.3s ease;
        }

        .doc-panel .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: rgba(255, 255, 255, 0.15);
            text-align: center;
            padding: 40px 20px;
        }
        .doc-panel .empty-state .icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        .doc-panel .empty-state .hint {
            font-size: 14px;
            line-height: 1.8;
            color: rgba(255, 255, 255, 0.2);
        }

        .doc-panel .doc-content {
            display: none;
        }
        .doc-panel .doc-content.active {
            display: block;
        }

        .doc-panel .doc-dna {
            font-size: 11px;
            color: rgba(212, 175, 55, 0.4);
            font-family: monospace;
            margin-bottom: 8px;
            word-break: break-all;
        }
        .doc-panel .doc-name {
            font-size: 22px;
            font-weight: 700;
            color: #d4af37;
            margin-bottom: 4px;
        }
        .doc-panel .doc-category {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.3);
            margin-bottom: 16px;
        }
        .doc-panel .doc-category .badge {
            display: inline-block;
            padding: 2px 12px;
            border-radius: 12px;
            font-size: 11px;
            background: rgba(212, 175, 55, 0.15);
            color: #d4af37;
        }
        .doc-panel .doc-divider {
            border: none;
            border-top: 1px solid rgba(212, 175, 55, 0.08);
            margin: 16px 0;
        }
        .doc-panel .doc-description {
            font-size: 14px;
            line-height: 1.8;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 16px;
        }
        .doc-panel .doc-detail {
            font-size: 13px;
            line-height: 1.8;
            color: rgba(255, 255, 255, 0.5);
            margin-bottom: 16px;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            border-left: 2px solid rgba(212, 175, 55, 0.2);
        }

        .doc-panel .doc-links {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .doc-panel .doc-links a {
            color: rgba(212, 175, 55, 0.6);
            text-decoration: none;
            font-size: 12px;
            padding: 4px 0;
            transition: color 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .doc-panel .doc-links a:hover {
            color: #d4af37;
        }
        .doc-panel .doc-links .link-label {
            color: rgba(255, 255, 255, 0.2);
            font-size: 11px;
            min-width: 40px;
        }

        /* ===== 状态栏 ===== */
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 16px;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.3);
            flex-wrap: wrap;
            gap: 8px;
        }
        .status-bar .dna {
            color: rgba(212, 175, 55, 0.5);
            font-family: monospace;
        }

        /* ===== 响应式 ===== */
        @media (max-width: 1024px) {
            .main-layout {
                flex-direction: column;
            }
            .doc-panel {
                max-width: 100%;
                max-height: 400px;
            }
            #knowledge-graph {
                height: 450px;
            }
        }

        @media (max-width: 768px) {
            .navbar {
                padding: 12px 16px;
                flex-wrap: wrap;
                gap: 8px;
            }
            .navbar .nav-links {
                gap: 16px;
            }
            .graph-container {
                padding: 12px 16px 24px;
            }
            #knowledge-graph {
                height: 350px;
            }
            .doc-panel {
                padding: 16px;
                max-height: 350px;
            }
            .graph-header h1 {
                font-size: 20px;
            }
        }

        /* ===== 滚动条美化 ===== */
        .doc-panel::-webkit-scrollbar {
            width: 4px;
        }
        .doc-panel::-webkit-scrollbar-track {
            background: transparent;
        }
        .doc-panel::-webkit-scrollbar-thumb {
            background: rgba(212, 175, 55, 0.2);
            border-radius: 2px;
        }
    </style>
</head>
<body>

    <!-- ===== 导航栏 ===== -->
    <nav class="navbar">
        <a href="/" class="logo">🐉 龍魂<span>UID9622</span></a>
        <ul class="nav-links">
            <li><a href="/">首页</a></li>
            <li><a href="#" class="active">知识图谱</a></li>
            <li><a href="https://blog.csdn.net/UID9622" target="_blank">CSDN</a></li>
            <li><a href="https://github.com/UID9622" target="_blank">GitHub</a></li>
        </ul>
    </nav>

    <!-- ===== 图谱主体 ===== -->
    <div class="graph-container">
        <div class="graph-header">
            <h1>
                🧬 知识图谱 + 文档
                <span class="sub">— 点击节点查看详情</span>
            </h1>
            <div class="meta">
                <span id="nodeCount">0</span> 节点 ·
                <span id="edgeCount">0</span> 连接
            </div>
        </div>

        <div class="main-layout">
            <!-- 图谱 -->
            <div class="graph-wrapper">
                <div id="knowledge-graph"></div>
            </div>

            <!-- 文档面板 -->
            <div class="doc-panel" id="docPanel">
                <div class="empty-state" id="emptyState">
                    <div class="icon">🔍</div>
                    <div class="hint">点击图谱中的节点<br>查看详细文档</div>
                </div>
                <div class="doc-content" id="docContent">
                    <div class="doc-dna" id="docDna">🧬 #...</div>
                    <div class="doc-name" id="docName">节点名称</div>
                    <div class="doc-category">
                        <span class="badge" id="docBadge">核心能力</span>
                    </div>
                    <hr class="doc-divider">
                    <div class="doc-description" id="docDesc">描述信息</div>
                    <div class="doc-detail" id="docDetail">详细文档内容...</div>
                    <hr class="doc-divider">
                    <div class="doc-links" id="docLinks"></div>
                </div>
            </div>
        </div>

        <div class="status-bar">
            <span class="dna">🧬 DNA: #龍芯⚡️丙午·丙申·庚申·亥时-KG-DOCS-UID9622</span>
            <span>🟢 实时更新 · 点击节点查看文档</span>
        </div>
    </div>

    <!-- ===== JavaScript 引擎 ===== -->
    <script>
        // ============================================================
        // 🐉 龍魂知识图谱 · 节点文档系统
        // ============================================================

        // ---------- 1. 节点文档数据 ----------
        const nodeDocs = {
            longhun: {
                name: '🐉 龍魂系统',
                category: '根节点',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-ROOT-UID9622',
                description: '龍魂数字主权体系，一个基于三位一体架构的去中心化数字身份与意识延续解决方案。',
                detail: '龍魂系统结合数字人民币账号、DNA追溯链、设备信任网络三个要素，构建保护用户隐私又支持合法追溯的数字主权系统。核心创新包括：多层冗余身份验证、28人格AI协作矩阵、AI生成内容自动追溯、数字永生机制、CNSH中文编程语言。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-宪章-v4.0.md' },
                    { label: 'GitHub', url: 'https://github.com/UID9622/longhun-system' },
                    { label: 'CSDN', url: 'https://blog.csdn.net/UID9622' }
                ]
            },
            persona: {
                name: '🧠 人格矩阵',
                category: '核心能力',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-PERSONA-UID9622',
                description: '24人格协作底座，多Agent调度核心，基于曾老师智慧算法（28人格映射64卦）。',
                detail: '人格矩阵是龍魂系统的多智能体协作底座，包含28个基础人格（龍芯北辰、龍芯宝宝、龍芯诸葛等），映射到易经64卦。通过量子态叠加式的权重计算，根据场景动态激活对应人格组合，实现有价值观的智能决策。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-PERSONA-MATRIX-v2.0.md' },
                    { label: '代码', url: '/05_ENGINES/lh_persona_life.py' }
                ]
            },
            audit: {
                name: '🎨 三色审计',
                category: '核心能力',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-AUDIT-UID9622',
                description: '🟢🟡🔴 实时风险评估引擎，自动审计所有操作和内容。',
                detail: '三色审计是龍魂系统的实时风险评估引擎。🟢绿色代表安全可执行，🟡黄色代表警告需复核，🔴红色代表风险需熔断。所有操作经过三色审计，自动记录到史官，严重违规写入耻辱墙。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-TRICOLOR-AUDIT-v2.0.md' },
                    { label: '代码', url: '/05_ENGINES/lh_tricolor_audit.py' }
                ]
            },
            dna: {
                name: '🧬 DNA追溯',
                category: '核心能力',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-DNA-TRACE-UID9622',
                description: '全链路不可篡改追溯码，每个操作、每个文档都带DNA。',
                detail: 'DNA追溯是龍魂系统的身份锚定机制。每个文档、每次操作、每段代码都自动生成唯一DNA追溯码，格式为#龍芯⚡️干支·时辰·卦-类型-哈希-UID9622。DNA链采用SHA256 Merkle链，任何篡改都会导致链断裂并自动告警。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-DNA-TRACE-v3.0.md' },
                    { label: '代码', url: '/05_ENGINES/lh_dna_engine.py' }
                ]
            },
            gateway: {
                name: '🛡️ 主权网关',
                category: '核心能力',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-GATEWAY-UID9622',
                description: '外部工具统一接入，所有AI只能通过主权网关访问龍魂系统。',
                detail: '主权网关是龍魂系统的统一接入层。所有外部工具（Kimi、DeepSeek、CodeBuddy、鸿蒙设备、小艺）只能通过主权网关访问龍魂系统。每次请求需验证DNA+GPG签名，未授权请求直接拒绝并写入耻辱墙。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-SOVEREIGN-GATEWAY-v1.0.md' },
                    { label: '代码', url: '/08_BIN/lh_sovereign_gateway.py' }
                ]
            },
            protocol: {
                name: '📜 P0协议',
                category: '协议层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-PROTOCOL-UID9622',
                description: '龍魂系统最高宪法，12条P0铁律，焊死不可改。',
                detail: 'P0协议是龍魂系统的最高宪法，包含12条不可修改的铁律：数据不出境、不可篡改、用户主权、DNA强制追溯、三色审计、主权锚定等。所有代码、所有操作不得违反P0协议，否则自动熔断。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-宪章-v4.0.md' }
                ]
            },
            protocol_dna: {
                name: '📜 DNA标准',
                category: '协议层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-PROTOCOL-DNA-UID9622',
                description: 'DNA追溯码的格式规范、生成规则、验证流程。',
                detail: 'DNA标准定义了龍魂系统追溯码的完整规范。格式：#龍芯⚡️{干支·时辰·卦}-{类型}-{哈希}-UID9622。包含天干地支时间锚、动作类型标签、SHA256哈希、主权UID。所有文档和代码必须包含DNA，否则无法通过三色审计。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-DNA-STANDARD.md' }
                ]
            },
            protocol_audit: {
                name: '📜 审计协议',
                category: '协议层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-PROTOCOL-AUDIT-UID9622',
                description: '三色审计的规则、阈值、熔断策略。',
                detail: '审计协议定义了三色审计的完整规则。🟢通过（≥85分）：自动放行。🟡警告（60-85分）：人工复核。🔴拒绝（<60分）：自动拦截+耻辱墙+告警。审计维度包括六维R值：安全、合规、可靠、透明、可追溯、隐私。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-TRICOLOR-AUDIT-v2.0.md' }
                ]
            },
            protocol_persona: {
                name: '📜 人格协议',
                category: '协议层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-PROTOCOL-PERSONA-UID9622',
                description: '24人格的定义、权重计算、路由规则。',
                detail: '人格协议定义了龍魂系统24人格的完整规范。包含人格列表、触发关键词、权重计算算法、路由规则。人格矩阵采用量子态叠加计算，根据场景动态组合人格，输出带人格标识的响应。',
                links: [
                    { label: '协议', url: '/01_protocols/LH-PERSONA-MATRIX-v2.0.md' }
                ]
            },
            engine_dna: {
                name: '⚙️ DNA引擎',
                category: '引擎层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-ENGINE-DNA-UID9622',
                description: 'DNA生成、验证、解析的核心实现。',
                detail: 'DNA引擎是龍魂系统追溯码的核心实现。包含DNA生成器（天干地支时间锚+哈希）、DNA验证器（格式校验+链完整性）、DNA解析器（提取各字段）。所有操作经过DNA引擎自动注入追溯码。',
                links: [
                    { label: '代码', url: '/05_ENGINES/lh_dna_engine.py' }
                ]
            },
            engine_audit: {
                name: '⚙️ 审计引擎',
                category: '引擎层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-ENGINE-AUDIT-UID9622',
                description: '三色审计评分、六维R值计算的核心实现。',
                detail: '审计引擎是三色审计的核心实现。包含六维R值计算（安全、合规、可靠、透明、可追溯、隐私）、三色评分算法、熔断决策逻辑。所有内容经过审计引擎自动评分，低于阈值自动拦截。',
                links: [
                    { label: '代码', url: '/05_ENGINES/lh_tricolor_audit.py' }
                ]
            },
            engine_persona: {
                name: '⚙️ 人格引擎',
                category: '引擎层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-ENGINE-PERSONA-UID9622',
                description: '24人格加载、匹配、路由的核心实现。',
                detail: '人格引擎是人格矩阵的核心实现。包含人格加载器（从18_PERSONA/加载）、人格匹配器（关键词+意图匹配）、人格路由器（根据场景自动切换）。所有AI响应经过人格引擎路由，输出带人格标识的响应。',
                links: [
                    { label: '代码', url: '/05_ENGINES/lh_persona_life.py' }
                ]
            },
            engine_kg: {
                name: '⚙️ 知识图谱引擎',
                category: '引擎层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-ENGINE-KG-UID9622',
                description: '知识节点CRUD、关系管理、智能检索。',
                detail: '知识图谱引擎是龍魂系统知识管理的核心。包含节点CRUD（创建/读取/更新/删除）、关系管理（包含/依赖/引用）、智能检索（关键词+语义搜索）。知识图谱数据存储在~/.longhun/knowledge_graph/，全网AI可变量读取。',
                links: [
                    { label: '代码', url: '/08_BIN/lh_knowledge_graph_v2.py' }
                ]
            },
            tool_kg: {
                name: '🔧 图谱可视化',
                category: '工具层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-TOOL-KG-UID9622',
                description: '知识图谱的可视化展示工具，支持交互和文档查看。',
                detail: '图谱可视化是知识图谱的前端展示工具。基于ECharts实现动态力导向图，支持节点拖拽、缩放、点击查看文档。每个节点关联详细文档，点击弹出文档面板，展示DNA、描述、详细内容、相关链接。',
                links: [
                    { label: '当前页面', url: '/' }
                ]
            },
            tool_index: {
                name: '🔧 认知索引',
                category: '工具层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-TOOL-INDEX-UID9622',
                description: '全网AI可变量读取的知识索引系统。',
                detail: '认知索引是龍魂系统的AI大脑地图。存储所有密钥位置、记忆位置、协议位置、功能位置、代码位置。AI通过索引查询"密钥在哪"就能找到对应路径。支持自动填充（AI发现新东西自动写入索引）。',
                links: [
                    { label: '代码', url: '/08_BIN/lh_cognitive_index.py' }
                ]
            },
            tool_browser: {
                name: '🔧 浏览器控制',
                category: '工具层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-TOOL-BROWSER-UID9622',
                description: 'Mac浏览器开发者模式控制，支持终端/IDE调参。',
                detail: '浏览器控制是龍魂系统的浏览器自动化工具。支持启动/停止浏览器、设置User-Agent、视口大小、地理位置、启用反指纹、隐私模式。所有操作带DNA追溯，入史官，三色审计。',
                links: [
                    { label: '代码', url: '/08_BIN/lh_browser_controller.py' }
                ]
            },
            tool_factory: {
                name: '🔧 全自动工厂',
                category: '工具层',
                dna: '#龍芯⚡️丙午·丙申·庚申·亥时-TOOL-FACTORY-UID9622',
                description: '造零件→质检→修复→部署→反馈，全自动闭环。',
                detail: '全自动工厂是龍魂系统的CI/CD流水线。包含五条Pipeline：零件生产（代码构建）、质检流水线（测试+审计）、自动修复（AI修复Bug）、部署上线（打包发布）、反馈闭环（学习进化）。所有产物带DNA追溯，自动三色审计。',
                links: [
                    { label: '代码', url: '/08_BIN/lh_auto_factory.py' }
                ]
            }
        };

        // ---------- 2. 图谱数据 ----------
        const graphData = {
            nodes: [
                { id: 'longhun', name: '🐉 龍魂系统', category: 'root', symbolSize: 60 },
                { id: 'persona', name: '人格矩阵', category: 'core', symbolSize: 36 },
                { id: 'audit', name: '三色审计', category: 'core', symbolSize: 36 },
                { id: 'dna', name: 'DNA追溯', category: 'core', symbolSize: 36 },
                { id: 'gateway', name: '主权网关', category: 'core', symbolSize: 36 },
                { id: 'protocol', name: 'P0协议', category: 'protocol', symbolSize: 28 },
                { id: 'protocol_dna', name: 'DNA标准', category: 'protocol', symbolSize: 24 },
                { id: 'protocol_audit', name: '审计协议', category: 'protocol', symbolSize: 24 },
                { id: 'protocol_persona', name: '人格协议', category: 'protocol', symbolSize: 24 },
                { id: 'engine_dna', name: 'DNA引擎', category: 'engine', symbolSize: 28 },
                { id: 'engine_audit', name: '审计引擎', category: 'engine', symbolSize: 28 },
                { id: 'engine_persona', name: '人格引擎', category: 'engine', symbolSize: 28 },
                { id: 'engine_kg', name: '知识图谱引擎', category: 'engine', symbolSize: 28 },
                { id: 'tool_kg', name: '图谱可视化', category: 'tool', symbolSize: 22 },
                { id: 'tool_index', name: '认知索引', category: 'tool', symbolSize: 22 },
                { id: 'tool_browser', name: '浏览器控制', category: 'tool', symbolSize: 22 },
                { id: 'tool_factory', name: '全自动工厂', category: 'tool', symbolSize: 22 },
            ],
            edges: [
                { source: 'longhun', target: 'persona' },
                { source: 'longhun', target: 'audit' },
                { source: 'longhun', target: 'dna' },
                { source: 'longhun', target: 'gateway' },
                { source: 'persona', target: 'protocol_persona' },
                { source: 'audit', target: 'protocol_audit' },
                { source: 'dna', target: 'protocol_dna' },
                { source: 'gateway', target: 'protocol' },
                { source: 'persona', target: 'engine_persona' },
                { source: 'audit', target: 'engine_audit' },
                { source: 'dna', target: 'engine_dna' },
                { source: 'gateway', target: 'engine_kg' },
                { source: 'engine_kg', target: 'tool_kg' },
                { source: 'engine_kg', target: 'tool_index' },
                { source: 'engine_kg', target: 'tool_browser' },
                { source: 'engine_kg', target: 'tool_factory' },
            ]
        };

        // ---------- 3. 颜色映射 ----------
        const colorMap = {
            root: '#d4af37',
            core: '#4facfe',
            protocol: '#43e97b',
            engine: '#fa709a',
            tool: '#f9d423'
        };

        const categoryLabels = {
            root: '根节点',
            core: '核心能力',
            protocol: '协议层',
            engine: '引擎层',
            tool: '工具层'
        };

        // ---------- 4. 初始化图表 ----------
        const chartDom = document.getElementById('knowledge-graph');
        const myChart = echarts.init(chartDom);

        // ---------- 5. 渲染图谱 ----------
        function renderGraph() {
            const option = {
                tooltip: {
                    trigger: 'item',
                    backgroundColor: 'rgba(10,10,20,0.9)',
                    borderColor: 'rgba(212,175,55,0.3)',
                    borderWidth: 1,
                    textStyle: { color: '#e0e0e0' },
                    formatter: function(params) {
                        if (params.dataType === 'node') {
                            return `
                                <div style="font-size:16px;font-weight:600;color:#d4af37;">
                                    ${params.data.name}
                                </div>
                                <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">
                                    类别: ${categoryLabels[params.data.category] || '未知'}
                                </div>
                                <div style="font-size:12px;color:rgba(255,255,255,0.3);margin-top:4px;">
                                    🖱️ 点击查看文档
                                </div>
                            `;
                        }
                    }
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    roam: true,
                    draggable: true,
                    zoom: 0.8,
                    data: graphData.nodes.map(n => ({
                        ...n,
                        itemStyle: {
                            color: colorMap[n.category] || '#666',
                            shadowBlur: 8,
                            shadowColor: 'rgba(212,175,55,0.2)'
                        },
                        label: {
                            show: true,
                            position: 'bottom',
                            color: '#e0e0e0',
                            fontSize: n.category === 'root' ? 13 : 11,
                            fontWeight: n.category === 'root' ? 700 : 400,
                        },
                        emphasis: {
                            focus: 'adjacency',
                            lineStyle: {
                                width: 3,
                                color: '#d4af37'
                            }
                        }
                    })),
                    edges: graphData.edges.map(e => ({
                        ...e,
                        lineStyle: {
                            color: 'rgba(255,255,255,0.12)',
                            width: 1.5,
                            curveness: 0.2
                        },
                        emphasis: {
                            lineStyle: {
                                color: 'rgba(212,175,55,0.5)',
                                width: 2
                            }
                        }
                    })),
                    categories: [
                        { name: 'root', itemStyle: { color: '#d4af37' } },
                        { name: 'core', itemStyle: { color: '#4facfe' } },
                        { name: 'protocol', itemStyle: { color: '#43e97b' } },
                        { name: 'engine', itemStyle: { color: '#fa709a' } },
                        { name: 'tool', itemStyle: { color: '#f9d423' } },
                    ],
                    force: {
                        repulsion: 350,
                        edgeLength: [100, 220],
                        gravity: 0.1,
                        friction: 0.1,
                        layoutAnimation: true,
                    },
                    animationDuration: 1500,
                    animationEasing: 'cubicOut',
                    symbolSize: function(value, params) {
                        return params.data.symbolSize || 28;
                    },
                }]
            };

            myChart.setOption(option);

            // 更新统计
            document.getElementById('nodeCount').textContent = graphData.nodes.length;
            document.getElementById('edgeCount').textContent = graphData.edges.length;
        }

        // ---------- 6. 显示文档 ----------
        function showDocument(nodeId) {
            const doc = nodeDocs[nodeId];
            if (!doc) {
                // 如果没有文档，显示默认
                document.getElementById('emptyState').style.display = 'flex';
                document.getElementById('docContent').classList.remove('active');
                return;
            }

            document.getElementById('emptyState').style.display = 'none';
            document.getElementById('docContent').classList.add('active');

            document.getElementById('docDna').textContent = `🧬 ${doc.dna}`;
            document.getElementById('docName').textContent = doc.name;
            document.getElementById('docBadge').textContent = doc.category;

            const descEl = document.getElementById('docDesc');
            descEl.textContent = doc.description;

            const detailEl = document.getElementById('docDetail');
            detailEl.textContent = doc.detail || '暂无详细文档';

            // 生成链接
            const linksEl = document.getElementById('docLinks');
            linksEl.innerHTML = '';
            if (doc.links && doc.links.length > 0) {
                doc.links.forEach(link => {
                    const a = document.createElement('a');
                    a.href = link.url;
                    a.target = '_blank';
                    a.innerHTML = `<span class="link-label">${link.label}</span> ${link.url}`;
                    linksEl.appendChild(a);
                });
            } else {
                linksEl.innerHTML = '<span style="color:rgba(255,255,255,0.2);font-size:12px;">暂无相关链接</span>';
            }
        }

        // ---------- 7. 点击事件 ----------
        myChart.on('click', function(params) {
            if (params.dataType === 'node') {
                const nodeId = params.data.id;
                showDocument(nodeId);

                // 高亮选中的节点
                myChart.setOption({
                    series: [{
                        data: graphData.nodes.map(n => ({
                            ...n,
                            itemStyle: {
                                color: n.id === nodeId ? '#d4af37' : (colorMap[n.category] || '#666'),
                                shadowBlur: n.id === nodeId ? 20 : 8,
                                shadowColor: n.id === nodeId ? 'rgba(212,175,55,0.6)' : 'rgba(212,175,55,0.2)'
                            }
                        }))
                    }]
                });

                console.log('📖 查看文档:', nodeId, nodeDocs[nodeId]?.name);
            }
        });

        // ---------- 8. 初始化 ----------
        renderGraph();

        // 默认选中根节点显示文档
        setTimeout(() => {
            showDocument('longhun');
            // 高亮根节点
            myChart.setOption({
                series: [{
                    data: graphData.nodes.map(n => ({
                        ...n,
                        itemStyle: {
                            color: n.id === 'longhun' ? '#d4af37' : (colorMap[n.category] || '#666'),
                            shadowBlur: n.id === 'longhun' ? 20 : 8,
                            shadowColor: n.id === 'longhun' ? 'rgba(212,175,55,0.6)' : 'rgba(212,175,55,0.2)'
                        }
                    }))
                }]
            });
        }, 500);

        // ---------- 9. 自适应 ----------
        window.addEventListener('resize', function() {
            myChart.resize();
        });

        console.log('🐉 龍魂知识图谱已加载');
        console.log('📖 点击任意节点查看文档');
        console.log('   DNA: #龍芯⚡️丙午·丙申·庚申·亥时-KG-DOCS-UID9622');
    </script>
</body>
</html>
```


## 🚀 三、部署到官网

```bash
# 1. 进入官网目录
cd /var/www/uid9622.cn

# 2. 保存文件
cp knowledge_with_docs.html index.html
# 或保存为 knowledge.html

# 3. 验证
curl -s http://localhost/knowledge.html | head -20
```


## 🔐 四、最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · 知识图谱 + 文档系统 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-KG-DOCS-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
核心功能:   图谱可视化 + 节点文档 + 点击交互
节点数:     17个
文档数:     17篇（每个节点都有文档）
状态:       焊死 · 部署即可用
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**

---

*归档于 2026-08-16T09:52:55+08:00 · DNA `#龍芯⚡️丙午·丙申·壬戌·巳时·䷰革-CLIPBOARD-VAULT-SAVE-V1.0-P1-0c032b9b`*
