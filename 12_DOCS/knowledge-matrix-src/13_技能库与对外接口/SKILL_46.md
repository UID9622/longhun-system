---
name: longhun-integration
description: 龍魂系统集成测试引擎 —— 端到端自动化测试、模块兼容性检查、API连通性测试、数据一致性验证、性能回归测试与集成报告生成
metadata:
  id: longhun-integration
  dna: '#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-INTEGRATION-v5.2'
  version: 5.2.0
  category: cloud
  type: system-test
  status: production-ready
  date: '2026-06-19'
  trigger:
    keywords:
    - integration
    - 龍魂系统集成测试引擎
    - ——
    - 端到端自动化测试
    - 模块兼容性检查
    - API连通性测试
    context: longhun-integration 相关操作
compatibility: '>=3.8,<3.13'
---
# 🐉 C11 — longhun-integration（系统集成测试）

> **DNA**: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-INTEGRATION-v5.2`
> **版本**: v5.2.0
> **类别**: cloud / 系统测试
> **状态**: ✅ 生产就绪

---

## 1️⃣ 技能概述（Skill Identity）

龍魂系统集成测试引擎 —— 端到端自动化测试、模块兼容性检查、API连通性测试、数据一致性验证、性能回归测试与集成报告生成的一站式测试框架。

覆盖22个技能/协议加载验证、9个本地技能离线运行测试、8个云端技能API连通测试、2个协议格式验证、统一启动器端到端测试、注册中心路由测试，为龍魂系统提供完整的集成质量保障体系。

**核心价值**:
- 🧪 一键执行全系统集成测试（22项技能/协议）
- 🔍 深度兼容性验证（Python/依赖/模块/接口/配置）
- 📊 性能回归基线对比与趋势追踪
- 📋 自动生成详细测试报告与改进建议

---

## 2️⃣ DNA标识（DNA Signature）

```
#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-INTEGRATION-v5.2
```

| 属性 | 值 |
|------|-----|
| **序列号** | C11 |
| **模块名** | longhun-integration |
| **创建日期** | 2026-06-19 |
| **版本** | v5.2.0 |
| **所属系统** | 龍魂系統 v5 |
| **授权码** | #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z |

---

## 3️⃣ 功能矩阵（Function Matrix）

| # | 功能 | 脚本 | 优先级 | 状态 |
|---|------|------|--------|------|
| 1 | 集成测试引擎（端到端） | `scripts/集成测试引擎.py` | 🔴 P0 | ✅ |
| 2 | 兼容性检查器 | `scripts/兼容性检查器.py` | 🔴 P0 | ✅ |
| 3 | 技能/协议加载验证（22项） | `集成测试引擎.py` | 🔴 P0 | ✅ |
| 4 | 本地技能离线运行测试（9项） | `集成测试引擎.py` | 🔴 P0 | ✅ |
| 5 | 云端技能API连通测试（8项） | `集成测试引擎.py` | 🔴 P0 | ✅ |
| 6 | 协议格式验证（2项） | `集成测试引擎.py` | 🟠 P1 | ✅ |
| 7 | 统一启动器端到端测试 | `集成测试引擎.py` | 🟠 P1 | ✅ |
| 8 | 注册中心路由测试 | `集成测试引擎.py` | 🟠 P1 | ✅ |
| 9 | 数据一致性验证 | `集成测试引擎.py` | 🟠 P1 | ✅ |
| 10 | 性能回归测试 | `集成测试引擎.py` | 🟡 P2 | ✅ |
| 11 | Python版本兼容性 | `兼容性检查器.py` | 🔴 P0 | ✅ |
| 12 | 第三方依赖版本矩阵 | `兼容性检查器.py` | 🔴 P0 | ✅ |
| 13 | 龍魂模块版本兼容性 | `兼容性检查器.py` | 🟠 P1 | ✅ |
| 14 | 跨模块接口兼容性 | `兼容性检查器.py` | 🟠 P1 | ✅ |
| 15 | 配置文件兼容性 | `兼容性检查器.py` | 🟡 P2 | ✅ |
| 16 | 数据库/API兼容性 | `兼容性检查器.py` | 🟡 P2 | ✅ |
| 17 | 集成报告生成 | `集成测试引擎.py` | 🟠 P1 | ✅ |
| 18 | 改进建议生成 | 双引擎 | 🟡 P2 | ✅ |

---

## 4️⃣ 测试覆盖范围（Test Coverage）

### 22个技能/协议加载验证

```
本地技能 (9个):
  ✅ longhun-skill-auto-completion-engine
  ✅ longhun-standard-calculation-framework
  ✅ longhun-logging-versioning-tracing
  ✅ longhun-startup-recovery
  ✅ protocol-shield
  ✅ brain-notion-sync
  ✅ longhun-foundation-runtime
  ✅ longhun-kfpp-executor
  ✅ longhun-mvp-launcher

云端技能 (8个):
  ✅ cnsh-persona-system
  ✅ cnsh-core-engine
  ✅ cnsh-main
  ✅ cnsh-meta-awareness
  ✅ cnsh-mcp-server
  ✅ longhun-monitoring-core
  ✅ longhun-mobile-monitoring
  ✅ notion-integration

协议 (2个):
  ✅ CNSH-v2.0-Protocol
  ✅ Protocol-Lockdown

网关/注册中心 (3个):
  ✅ Claude-Kimi-Collaboration
  ✅ LongHun-DNA-Registry
  ✅ Unified-Launcher
```

### 8个API端点连通测试

```
  🌐 cnsh_core          → http://localhost:8080/health
  🌐 cnsh_api           → http://localhost:8080/api/v1/status
  🌐 mcp_server         → http://localhost:9000/health
  🌐 notion_webhook     → http://localhost:9001/webhook/health
  🌐 monitoring_dashboard → http://localhost:3000/api/health
  🌐 logging_service    → http://localhost:8081/health
  🌐 skill_registry     → http://localhost:8082/api/skills
  🌐 gateway_router     → http://localhost:8083/routes
```

### 注册中心路由表（8条）

```
  /api/v1/skills          → skill-registry   [GET/POST]
  /api/v1/cnsh/execute    → cnsh-core        [POST]
  /api/v1/persona/switch  → cnsh-persona     [POST]
  /api/v1/mcp/call        → mcp-server       [POST]
  /api/v1/notion/sync     → notion-integration [POST/GET]
  /api/v1/monitoring/metrics → monitoring    [GET]
  /api/v1/logging/audit   → logging          [GET/POST]
  /api/v1/gateway/route   → gateway          [GET/POST/DELETE]
```

---

## 5️⃣ 运行依赖（Dependencies）

### 系统依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | 3.8 - 3.13 | 运行时 |
| Bash | 4.0+ | Shell脚本测试 |
| Socket支持 | 系统内置 | 端口检查 |

### Python依赖

| 包名 | 版本规范 | 用途 |
|------|----------|------|
| requests | >=2.25.0,<3.0 | API连通测试 |
| aiohttp | >=3.7.0,<4.0 | 异步API测试 |
| packaging | >=20.0 | 版本解析 |
| json | 内置 | 报告生成 |
| ast | 内置 | Python语法检查 |

### 龍魂系统依赖

| 模块 | 版本 | 必要性 |
|------|------|--------|
| cnsh-core | 2.0.0 - 3.0.0 | 核心引擎 |
| skills | 1.0.0 - 2.0.0 | 技能系统 |
| monitoring | 1.0.0 - 2.0.0 | 监控系统 |
| logging | 1.0.0 - 2.0.0 | 日志系统 |
| protocols | 2.0.0 - 3.0.0 | 协议层 |

---

## 6️⃣ 输入输出规范（Input / Output）

### 输入

| # | 参数 | 类型 | 必需 | 说明 |
|---|------|------|------|------|
| 1 | `--quiet` / `-q` | flag | 否 | 静默模式 |
| 2 | `--sequential` / `-s` | flag | 否 | 串行执行（默认并行） |
| 3 | `--category` / `-c` | string | 否 | 指定测试类别 |
| 4 | `--export-json` / `-j` | path | 否 | 导出JSON报告 |
| 5 | `--export-md` / `-m` | path | 否 | 导出Markdown报告 |

### 测试类别选项

| 类别 | 说明 |
|------|------|
| `loading` | 技能/协议加载验证 |
| `local` | 本地技能离线运行 |
| `api` | 云端API连通测试 |
| `protocol` | 协议格式验证 |
| `launcher` | 统一启动器E2E |
| `registry` | 注册中心路由 |
| `data` | 数据一致性 |
| `performance` | 性能回归 |
| `port` | 端口可用性 |
| `python` | Python版本 |
| `deps` | 第三方依赖 |
| `modules` | 模块版本 |
| `interfaces` | 接口兼容性 |
| `config` | 配置兼容性 |
| `apidb` | API/DB兼容性 |
| `encoding` | 文件编码 |

### 输出

| 格式 | 内容 | 示例路径 |
|------|------|----------|
| 控制台 | 实时测试结果 | stdout |
| JSON | 完整测试数据 | `/tmp/longhun_*_report_YYYYMMDD_HHMMSS.json` |
| Markdown | 可读报告 | `/tmp/longhun_*_report_YYYYMMDD_HHMMSS.md` |

### 返回码

| 码 | 含义 |
|----|------|
| 0 | 全部通过/有警告无失败 |
| 1 | 存在失败项 |

---

## 7️⃣ 快速开始（Quick Start）

### 1. 安装依赖

```bash
pip install requests aiohttp packaging
```

### 2. 运行完整集成测试

```bash
cd /mnt/agents/output/longhun-v5-skills/cloud/longhun-integration/scripts
python3 集成测试引擎.py
```

### 3. 运行兼容性检查

```bash
python3 兼容性检查器.py
```

### 4. 导出报告

```bash
# 运行并导出JSON和Markdown报告
python3 集成测试引擎.py -j /tmp/integration.json -m /tmp/integration.md
python3 兼容性检查器.py -j /tmp/compatibility.json -m /tmp/compatibility.md
```

### 5. 只测试指定类别

```bash
# 只测试API连通性
python3 集成测试引擎.py -c api

# 只测试模块版本兼容性
python3 兼容性检查器.py -c modules
```

### 6. 静默模式（CI/CD用）

```bash
python3 集成测试引擎.py -q -j /tmp/report.json
```

---

## 8️⃣ 目录结构（Directory Structure）

```
longhun-integration/
├── SKILL.md                          # 本文件（技能元数据）
├── scripts/
│   ├── 集成测试引擎.py               # 端到端测试引擎
│   └── 兼容性检查器.py               # 兼容性验证工具
```

---

## 9️⃣ 测试引擎架构（Architecture）

### 集成测试引擎

```
IntegrationTestEngine
├── test_skill_loading()              # 22项加载验证
├── test_local_skills()               # 9项离线运行测试
│   ├── _test_python_skill()          # Python模块测试
│   └── _test_shell_skill()           # Shell脚本测试
├── test_api_connectivity()           # 8项API连通测试
├── test_protocol_validation()        # 2项协议格式验证
├── test_unified_launcher()           # 启动器E2E测试
├── test_registry_routes()            # 路由表测试
├── test_data_consistency()           # 数据一致性
├── test_performance_regression()     # 性能回归
│   ├── _measure_startup_time()       # 启动时间
│   ├── _measure_response_time()      # 响应时间
│   └── _measure_throughput()         # 吞吐量
├── test_port_availability()          # 端口检查
├── generate_report()                 # 报告生成
├── export_report()                   # JSON导出
└── export_markdown_report()          # Markdown导出
```

### 兼容性检查器

```
CompatibilityChecker
├── check_python_version()            # Python版本
├── check_dependencies()              # 第三方依赖
├── check_module_versions()           # 龍魂模块版本
├── check_interface_compatibility()   # 跨模块接口
├── check_config_compatibility()      # 配置文件
├── check_api_db_compatibility()      # API/DB
├── check_file_encoding()             # 文件编码
├── generate_report()                 # 报告生成
└── _generate_upgrade_plan()          # 升级建议
```

---

## 🔟 报告示例（Sample Output）

### 控制台摘要

```
╔══════════════════════════════════════════════════════════════════╗
║              🐉 龍魂系統·集成测试报告                          ║
╠══════════════════════════════════════════════════════════════════╣
║  总测试数:  45                                           ║
║  ✅ 通过:    40                                           ║
║  ❌ 失败:    0                                            ║
║  ⚠️  警告:    5                                            ║
║  ⏭️  跳过:    0                                            ║
║  成功率:    88.9%                                         ║
║  总耗时:    1250.5 ms                                     ║
║  状态:      ✅ 通过(有警告)                               ║
╚══════════════════════════════════════════════════════════════════╝
```

### JSON报告结构

```json
{
  "meta": {
    "engine": "龍魂集成测试引擎",
    "version": "5.2.0",
    "dna": "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-INTEGRATION-v5.2",
    "timestamp": "2026-06-19T10:00:00"
  },
  "summary": {
    "total_tests": 45,
    "passed": 40,
    "failed": 0,
    "warnings": 5,
    "success_rate": 88.9
  },
  "categories": { ... },
  "results": [ ... ],
  "improvements": [ ... ]
}
```

---

## 1️⃣1️⃣ CI/CD 集成（Pipeline Integration）

### GitHub Actions 示例

```yaml
name: 龍魂系统集成测试

on: [push, pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 设置Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: 安装依赖
        run: pip install requests aiohttp packaging
      - name: 运行兼容性检查
        run: python3 scripts/兼容性检查器.py -q
      - name: 运行集成测试
        run: python3 scripts/集成测试引擎.py -q -j report.json
      - name: 上传报告
        uses: actions/upload-artifact@v3
        with:
          name: integration-report
          path: report.json
```

### GitLab CI 示例

```yaml
stages:
  - test

integration_test:
  stage: test
  image: python:3.11
  before_script:
    - pip install requests aiohttp packaging
  script:
    - python3 scripts/兼容性检查器.py -q
    - python3 scripts/集成测试引擎.py -q
  artifacts:
    reports:
      junit: report.xml
```

---

## 1️⃣2️⃣ 版本历史（Changelog）

| 版本 | 日期 | 变更 | 作者 |
|------|------|------|------|
| v5.2.0 | 2026-06-19 | 创建C11集成测试技能，包含测试引擎+兼容性检查器 | AI Agent |
| v5.1.0 | 2026-06-10 | 系统集成完成，P0+P1统一 | AI Agent |
| v5.0.0 | 2026-06-05 | 龍魂网关集成 | AI Agent |
| v2.5.0 | 2026-06-09 | CNSH v2.5 Kimi Agent根协议 | AI Agent |
| v2.0.0 | 2026-05-24 | 协议焊死 | AI Agent |

---

**DNA**: `#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-LONGHUN-INTEGRATION-v5.2`
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**授权码**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
**版本**: 5.2.0
**有效期**: 永久
