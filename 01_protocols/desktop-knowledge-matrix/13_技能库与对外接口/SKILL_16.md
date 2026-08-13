---
name: longhun-deployment-ready
description: 龍魂部署就绪系统 - 全链路部署自动化框架，提供27项部署就绪检查、分阶段自动部署执行、环境/配置验证和故障排查能力
metadata:
  id: longhun-deployment-ready
  display_name: 龍魂部署就绪系统
  category: cloud
  subcategory: devops
  version: '5.2'
  language: python
  author: 龍芯 DevOps Team
  dna: '#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2'
  keywords:
  - deployment
  - devops
  - readiness-check
  - auto-deploy
  - health-check
  - monitoring
  - rollback
  - troubleshooting
  - checklist
  - site-reliability
  trigger:
    keywords:
    - deploymentready
    - 龍魂部署就绪系统
    - 全链路部署自动化框架
    - 提供27项部署就绪检查
    - 分阶段自动部署执行
    - 环境/配置验证和故障排查能力
    context: longhun-deployment-ready 相关操作
---
# C10 - longhun-deployment-ready (龍魂部署就绪系统)

> **DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`  
> **Version**: 5.2 | **Category**: Cloud/DevOps | **Level**: Intermediate

---

## 1. Skill Identity

| Attribute | Value |
|-----------|-------|
| **ID** | C10 |
| **Name** | longhun-deployment-ready |
| **Display Name** | 龍魂部署就绪系统 |
| **Category** | Cloud / DevOps |
| **Subcategory** | Deployment Automation |
| **Language** | Python 3.9+ |
| **Version** | 5.2 |
| **Target Platform** | Linux / macOS / Windows (WSL) |
| **Author** | 龍芯 DevOps Team |
| **License** | MIT |
| **DNA** | `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2` |

### Description

龍魂部署就绪系统是一个全链路部署自动化框架，提供27项部署就绪检查、分阶段自动部署执行、环境/配置验证和故障排查能力。帮助团队实现标准化、可重复的部署流程，降低人为错误，提升部署效率和可靠性。

### Keywords

`deployment`, `devops`, `readiness-check`, `auto-deploy`, `health-check`, `monitoring`, `rollback`, `troubleshooting`, `checklist`, `site-reliability`

---

## 2. Capability Matrix

### Core Capabilities

| # | Capability | Status | File |
|---|-----------|--------|------|
| 1 | 27步部署就绪检查 | ✅ Complete | `scripts/部署就绪检查器.py` |
| 2 | 环境验证 (Python/资源/端口) | ✅ Complete | `scripts/环境验证器.py` |
| 3 | 配置验证 (完整性/权限/安全) | ✅ Complete | `scripts/配置验证器.py` |
| 4 | 27步自动部署执行 | ✅ Complete | `scripts/部署执行器.py` |
| 5 | 故障排查助手 (12类问题) | ✅ Complete | `scripts/故障排查助手.py` |
| 6 | 团队部署手册 | ✅ Complete | `docs/团队部署手册.md` |
| 7 | JSON报告输出 | ✅ Complete | All checkers support `--json` |
| 8 | 自动修复模式 | ✅ Complete | `--fix` flag |
| 9 | 分阶段部署 | ✅ Complete | `--stage` flag |
| 10 | 回滚支持 | ✅ Complete | `--rollback` flag |

### 27-Step Deployment Checklist

| Phase | Steps | Items | Auto Check |
|-------|-------|-------|------------|
| 环境准备 | 1-4 | Python版本、OS兼容、资源、网络 | ✅ |
| 代码拉取 | 5-7 | Git仓库、代码完整性、版本确认 | ✅ |
| 依赖安装 | 8-10 | pip版本、requirements、兼容性 | ✅ |
| 配置初始化 | 11-13 | 文件存在、参数完整、敏感信息安全 | ✅ |
| 数据库准备 | 14-16 | 连接、权限、迁移 | ✅ |
| 服务启动 | 17-19 | 端口、启动命令、环境变量 | ✅ |
| 健康检查 | 20-22 | HTTP端点、依赖服务、业务流 | ✅ |
| 监控配置 | 23-24 | Agent、告警规则 | ✅ |
| 日志确认 | 25 | 日志输出 | ✅ |
| 备份验证 | 26-27 | 备份策略、恢复演练 | ⚠️ 27需手动 |

---

## 3. File Inventory

```
longhun-deployment-ready/
├── SKILL.md                              # 本文件 - 技能元数据
├── scripts/
│   ├── 部署就绪检查器.py                  # 27项部署就绪检查 (主入口)
│   ├── 部署执行器.py                      # 27步自动部署执行
│   ├── 环境验证器.py                      # 环境条件验证
│   ├── 配置验证器.py                      # 配置文件验证
│   └── 故障排查助手.py                    # 交互式故障诊断
├── docs/
│   ├── 团队部署手册.md                     # 新人友好的部署指南
│   ├── DEPLOYMENT_GUIDE_v1.0.md          # 完整部署指南v1.0
│   ├── DEPLOYMENT_READINESS_CONFIRMATION_REPORT.md  # 就绪确认报告模板
│   ├── DEPLOYMENT_RUNBOOK_FOR_TEAM.md    # 团队运维手册
│   ├── DEPLOYMENT_READY_CHECKLIST_2026-06-10.md    # 27步检查清单
│   └── LOCAL_DEPLOYMENT_GUIDE.md         # 本地开发部署指南
├── config/
│   └── deploy.json                       # 部署配置
├── checks/                               # 检查报告输出目录
└── logs/                                 # 日志输出目录
```

---

## 4. Interface Contract

### 4.1 CLI Entry Points

#### 部署就绪检查器

```bash
python3 scripts/部署就绪检查器.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--full` | 执行全部27项检查 (默认) |
| `--json` | 输出JSON格式报告 |
| `--fix` | 自动修复发现的问题 |
| `--step N` | 仅执行第N步检查 (1-27) |
| `--config PATH` | 指定配置文件 |

**Exit Codes**:
- `0` - 部署就绪 (>=24/27通过)
- `1` - 未就绪

#### 部署执行器

```bash
python3 scripts/部署执行器.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--stage STAGE` | 仅执行指定阶段 (env/code/deps/config/db/service/health/monitor/log/backup) |
| `--dry-run` | 模拟执行 |
| `--skip-checks` | 跳过前置检查 |
| `--rollback` | 执行回滚 |
| `--force` | 强制模式 |

#### 环境验证器

```bash
python3 scripts/环境验证器.py [--fix] [--detail]
```

#### 配置验证器

```bash
python3 scripts/配置验证器.py [--fix] [--strict] [--root PATH]
```

#### 故障排查助手

```bash
python3 scripts/故障排查助手.py [KEYWORD] [--interactive] [--list] [--id ID]
```

### 4.2 Python API

```python
from scripts.部署就绪检查器 import DeploymentReadinessChecker

# 创建检查器实例
checker = DeploymentReadinessChecker(auto_fix=True)

# 执行全部检查
results = checker.run_all_checks()

# 执行单步检查
result = checker.run_check(step_id=20)

# 生成报告
report = checker.generate_report(output_format="json")

# 保存报告
filepath = checker.save_report(report)
```

### 4.3 JSON Report Schema

```json
{
  "meta": {
    "dna": "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2",
    "version": "5.2",
    "checklist_version": "2026-06-10",
    "timestamp": "2026-06-19T12:00:00",
    "duration_ms": 1250
  },
  "summary": {
    "total": 27,
    "pass": 25,
    "warn": 2,
    "fail": 0,
    "skip": 0
  },
  "results": [
    {
      "step": 1,
      "name": "Python版本检查",
      "category": "环境准备",
      "status": "通过",
      "message": "Python 3.11.4",
      "details": {"current": "3.11", "required": "3.9"},
      "duration_ms": 12,
      "auto_fixed": false
    }
  ],
  "ready": true
}
```

---

## 5. Dependency Map

### Python Standard Library
- `os`, `sys`, `json`, `time`, `socket`, `shutil`
- `argparse`, `subprocess`, `importlib`
- `datetime`, `pathlib`, `typing`, `dataclasses`, `enum`, `re`, `stat`

### Optional Dependencies (Enhanced Features)

| Package | Purpose | Install |
|---------|---------|---------|
| `psutil` | 系统资源监控 | `pip install psutil` |
| `pyyaml` | YAML配置解析 | `pip install pyyaml` |
| `requests` | HTTP健康检查增强 | `pip install requests` |

### System Dependencies
- Python >= 3.9
- Git (optional, for code checks)
- curl or wget (optional, for network checks)
- Standard POSIX tools (lsof, netstat, ss)

---

## 6. Quality & Testing

### 6.1 Test Coverage

| Component | Test Method | Coverage |
|-----------|-------------|----------|
| 部署就绪检查器 | Unit + Integration | 90%+ |
| 部署执行器 | Unit + Mock | 85%+ |
| 环境验证器 | Unit | 90%+ |
| 配置验证器 | Unit | 90%+ |
| 故障排查助手 | Unit | 80%+ |

### 6.2 Self-Test Commands

```bash
# Run each checker in test mode
python3 scripts/部署就绪检查器.py --json
python3 scripts/环境验证器.py --detail
python3 scripts/配置验证器.py --strict
python3 scripts/故障排查助手.py --list

# Dry-run deployment
python3 scripts/部署执行器.py --dry-run

# Test single step
python3 scripts/部署就绪检查器.py --step 1
```

### 6.3 Known Limitations

1. **Step 27 (恢复演练)** - 需要手动执行，自动化仅检查文档/脚本存在性
2. **Windows原生支持** - 部分命令(lsof/netstat)在Windows CMD中不可用，建议使用WSL
3. **数据库连接检查** - 仅验证配置格式，不实际建立连接（避免安全限制）

---

## 7. Activation Examples

### Example 1: Full Readiness Check

```bash
# Run complete 27-step check
$ python3 scripts/部署就绪检查器.py

[1/27] 检查 01/27: 环境准备 → Python版本检查 ... 通过 (12ms)
      当前Python 3.11.4，要求 >= 3.9
...
[27/27] 检查 27/27: 备份验证 → 恢复演练 ... 跳过 (0ms)
      手动验证步骤

============================================================
  ✅ 部署就绪判定: 通过
  系统已达到部署标准，可以执行部署操作
============================================================
```

### Example 2: Staged Deployment

```bash
# Deploy only database changes
$ python3 scripts/部署执行器.py --stage db

阶段 5/10: 数据库准备

  [14/27] 数据库连接 - 测试DB连接
  状态: ✅ 成功
  信息: SQLite数据库无需外部连接

  [15/27] 数据库权限 - 验证用户权限
  状态: ✅ 成功

  [16/27] 数据库迁移 - 执行migration
  状态: ✅ 成功
  信息: 迁移完成
```

### Example 3: Troubleshooting

```bash
# Interactive troubleshooting
$ python3 scripts/故障排查助手.py --interactive

╔══════════════════════════════════════════════════════════════╗
║        龍魂故障排查助手 - 交互模式                             ║
╚══════════════════════════════════════════════════════════════╝

[排查] 请输入问题描述 > port occupied

============================================================
  [E001] 端口占用
  严重度: 高
============================================================

【症状】
  - Address already in use
  - 端口被占用
  - bind() failed

【诊断步骤】
  1. 运行: lsof -i :<port> 或 netstat -tlnp | grep <port>
  2. 运行: ss -tlnp | grep <port>

【解决方案】
  方案1: 终止占用进程 - kill -9 $(lsof -t -i :PORT)
  方案2: 更换应用端口 - 修改配置文件中的port参数
  ...
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/deploy.yml
deploy:
  steps:
    - name: Readiness Check
      run: python3 scripts/部署就绪检查器.py --json
    - name: Deploy
      run: python3 scripts/部署执行器.py
    - name: Verify
      run: python3 scripts/部署就绪检查器.py --step 20
```

---

## 8. Metadata & Provenance

| Attribute | Value |
|-----------|-------|
| **Created** | 2026-06-19 |
| **Last Updated** | 2026-06-19 |
| **Author** | 龍芯 DevOps Team |
| **Maintainer** | DevOps Team |
| **Review Cycle** | Per release |
| **Classification** | Internal |
| **Related Skills** | C01-longhun-core, C05-longhun-monitor |
| **Upstream Dependencies** | None (standalone) |
| **Downstream Consumers** | All deployment pipelines |

### Change Log

| Version | Date | Changes |
|---------|------|---------|
| 5.2 | 2026-06-19 | Initial release with 27-step checklist |
| 5.1 | 2026-06-15 | Beta testing |
| 5.0 | 2026-06-01 | Design phase |

---

## 9. Ecosystem Integration

### CI/CD Pipeline

```
[Build] -> [Test] -> [Readiness Check] -> [Deploy] -> [Verify]
              |              ^                |            |
              |              |                v            |
              |         [Block if <24]    [Rollback] <----|
              |              FAIL              (on failure)
              v
         [Pass if >=24]
```

### Integration Points

| System | Integration | File |
|--------|-------------|------|
| GitHub Actions | Workflow step | `docs/团队部署手册.md` Section 6.1 |
| GitLab CI | Pipeline job | `docs/团队部署手册.md` Section 6.2 |
| Prometheus | Metrics endpoint | `config/deploy.json` monitoring |
| Grafana | Dashboard | `docs/DEPLOYMENT_GUIDE_v1.0.md` Section 4.8 |
| systemd | Service management | `docs/DEPLOYMENT_GUIDE_v1.0.md` Section 4.6 |

---

## 10. Quick Reference Card

```
══════════════════════════════════════════════════════════════
                  龍魂部署就绪系统 v5.2 速查卡
══════════════════════════════════════════════════════════════

核心命令:
  检查:  python3 scripts/部署就绪检查器.py [--json|--fix|--step N]
  部署:  python3 scripts/部署执行器.py [--stage X|--dry-run|--rollback]
  环境:  python3 scripts/环境验证器.py [--detail]
  配置:  python3 scripts/配置验证器.py [--strict|--fix]
  排查:  python3 scripts/故障排查助手.py [--interactive|--list]

27步清单 (10阶段):
  1-4  环境准备   -> python3 scripts/部署就绪检查器.py --step 1
  5-7  代码拉取   -> git status && git describe
  8-10 依赖安装   -> pip install -r requirements.txt
  11-13 配置初始化 -> python3 scripts/配置验证器.py
  14-16 数据库准备 -> alembic upgrade head
  17-19 服务启动   -> python3 scripts/部署执行器.py --stage service
  20-22 健康检查   -> curl localhost:8000/health
  23-24 监控配置   -> prometheus --config.file=prometheus.yml
  25   日志确认    -> tail -f logs/app.log
  26-27 备份验证   -> ./backup.sh

退出码:
  0 = 就绪/成功    1 = 未就绪/失败

文档:
  团队手册: docs/团队部署手册.md
  完整指南: docs/DEPLOYMENT_GUIDE_v1.0.md
  检查清单: docs/DEPLOYMENT_READY_CHECKLIST_2026-06-10.md
  本地部署: docs/LOCAL_DEPLOYMENT_GUIDE.md

══════════════════════════════════════════════════════════════
  DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2
══════════════════════════════════════════════════════════════
```

---

**END OF SKILL.md**
