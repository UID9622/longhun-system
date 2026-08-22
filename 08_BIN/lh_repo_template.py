#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·开源项目发布模板生成器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-模板生成-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
  1. 生成完整的 README.md（含徽章、目录、安装、使用、贡献、协议）
  2. 生成 CONTRIBUTING.md（贡献指南）
  3. 生成 CODE_OF_CONDUCT.md（行为准则）
  4. 生成 SECURITY.md（安全政策）
  5. 生成 CHANGELOG.md（变更日志）
  6. 生成 GitHub/Gitee Issue 模板
  7. 生成 PR 模板
  8. 生成 LICENSE（木兰PSL v2 + 主权附加条款）
  9. 生成 .gitignore
  10. 生成 pyproject.toml + requirements
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re


# ============================================================
# 一、配置
# ============================================================

DEFAULT_CONFIG = {
    "project_name": "longhun-system",
    "project_description": "龍魂系统 — 中国主权AI基础设施",
    "author": "UID9622 (龍芯北辰)",
    "author_email": "longhun@uid9622.com",
    "author_url": "https://uid9622.cn",
    "repo_url": "https://github.com/UID9622/longhun-system",
    "repo_gitee_url": "https://gitee.com/uid9622_admin/longhun-system-core",
    "license": "木兰宽松许可证 v2 (Mulan PSL v2)",
    "license_spdx": "MulanPSL-2.0",
    "year": "2026",
    "version": "1.0.0",
    "python_version": "3.10+",
    "dna": "#龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-模板生成-v1.0",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}


# ============================================================
# 二、徽章生成器
# ============================================================

class BadgeGenerator:
    """徽章生成器 - 生成 shields.io 风格的徽章"""

    @staticmethod
    def generate_all(config: Dict) -> List[str]:
        return [
            f"![License](https://img.shields.io/badge/license-{config['license_spdx']}-blue.svg)",
            f"![Version](https://img.shields.io/badge/version-{config['version']}-green.svg)",
            f"![Python](https://img.shields.io/badge/python-{config['python_version']}-blue.svg)",
            "![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)",
            "![Arch](https://img.shields.io/badge/arch-x86__64%20%7C%20ARM64-red.svg)",
            "![Code Check](https://img.shields.io/badge/code-checked-brightgreen.svg)",
            "![Tests](https://img.shields.io/badge/tests-brightgreen.svg)",
            "![Security Audit](https://img.shields.io/badge/security-audited-brightgreen.svg)",
            "![Sovereignty](https://img.shields.io/badge/sovereignty-China-red.svg)",
            f"![DNA](https://img.shields.io/badge/dna-UID9622·主权追溯-purple.svg)",
            "![Gitee](https://img.shields.io/badge/Gitee-mirror-orange.svg)",
            f"![GitHub stars](https://img.shields.io/github/stars/UID9622/{config['project_name']}.svg)",
        ]


# ============================================================
# 三、README 生成器
# ============================================================

class ReadmeGenerator:
    """README.md 生成器"""

    @staticmethod
    def generate(config: Dict, badges: List[str]) -> str:
        return f"""# 🐉 {config['project_name']}

{config['project_description']}

## 📊 徽章

{' '.join(badges)}

---

## 📋 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [快速开始](#快速开始)
- [安装](#安装)
- [使用指南](#使用指南)
- [API 文档](#api-文档)
- [配置说明](#配置说明)
- [开发指南](#开发指南)
- [测试](#测试)
- [贡献指南](#贡献指南)
- [行为准则](#行为准则)
- [安全政策](#安全政策)
- [变更日志](#变更日志)
- [协议](#协议)
- [致谢](#致谢)

---

## 📖 项目简介

**{config['project_name']}** 是一个以中国法律为边界、数据主权为核心、AI 安全为底线的综合性 AI 基础设施系统。

### 🎯 愿景

打造全球首个**主权级 AI 系统** — 每一段代码皆有 DNA，每一次协作皆可追溯。

### 🧬 核心原则

| 原则 | 说明 |
|:---|:---|
| **中国法律是唯一边界** | 所有操作必须符合中华人民共和国法律 |
| **数据主权归中国** | 数据存储在中国境内，未经许可禁止出境 |
| **一票否决权 (UID9622)** | 创始人拥有最终否决权，不可撤销 |
| **系统在，协议在** | 协议与系统共存，永续有效 |
| **DNA 全链路追溯** | 每段代码·每次协作·每次交付均有 DNA 签名 |

---

## ✨ 核心特性

### 🔒 安全与主权

- ✅ **中国法律边界** — 所有功能运行在法律框架内
- ✅ **数据主权保护** — 数据加密存储，禁止非法出境
- ✅ **一票否决权** — UID9622 拥有最高权限
- ✅ **三色审计** — 🟢 通过 / 🟡 待审 / 🔴 熔断
- ✅ **DNA 追溯** — 每条记录带唯一追溯码
- ✅ **四级熔断** — L0伦理 > L1数据 > L2人格 > L3行为
- ✅ **GPG 签名** — 所有产出数字签名，防篡改

### 🤖 AI 能力

- ✅ **CNSH 中文编程** — 用中文写代码，中国人一看就懂
- ✅ **20人格矩阵** — 16核心 + 1安全 + 3子系统，职能路由
- ✅ **璇玑引擎** — 记忆溯源推演系统
- ✅ **通心译翻译** — 别人翻译语言，我们翻译灵魂
- ✅ **沙盒推演** — 时间推演 + 博弈对抗 + 平行宇宙

### 🛠️ 工具链

- ✅ **一体化命令引擎** (`lh-run`) — 自然语言→命令，四级匹配
- ✅ **浏览器史官** — 四道防线保护浏览数据
- ✅ **数字根计算** — 五行流场压缩核
- ✅ **链接解析引擎** — 任意 URL 深度解析
- ✅ **自动对齐闭环** — 代码自动检测→修复→验证→归档

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本要求 |
|:---|:---|
| Python | {config['python_version']} |
| 操作系统 | Linux / macOS / Windows |
| 架构 | x86_64 / ARM64 |
| 内存 | ≥ 8GB (推荐 16GB+) |
| 存储 | ≥ 50GB |

### 一键安装

```bash
# 克隆仓库 (GitHub)
git clone {config['repo_url']}
cd {config['project_name']}

# 或国内加速 (Gitee)
git clone {config['repo_gitee_url']}

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化系统
python3 bin/lh.py

# 验证安装
python3 bin/lh_run.py "健康检查" --dry-run
```

---

## 📦 安装

### 方式一：从 GitHub 安装

```bash
git clone {config['repo_url']}
```

### 方式二：从 Gitee 安装（国内加速）

```bash
git clone {config['repo_gitee_url']}
```

### 方式三：使用 pip（即将支持）

```bash
pip install longhun-system
```

---

## 💻 使用指南

### 基本用法

```bash
cd {config['project_name']}
source .venv/bin/activate

# 统一控制台
python3 bin/lh.py

# 自然语言命令执行
python3 bin/lh_run.py "健康检查"
python3 bin/lh_run.py "对齐复盘" --dry-run

# 一键审计
python3 bin/lh.py --audit

# 主权验证
python3 bin/lh_sovereignty_guard.py validate
```

---

## 📚 API 文档

### 核心模块

| 模块 | 路径 | 功能 |
|:---|:---|:---|
| 统一控制台 | `bin/lh.py` | 系统总入口·交互菜单 |
| 命令引擎 | `bin/lh_run.py` | 自然语言→命令·四级匹配 |
| 璇玑引擎 | `engines/lh_xuanji_engine.py` | 记忆溯源推演 |
| 通心译 | `bin/lh_tongxinyi_translator.py` | 文化锚点保护翻译 |
| 主权守护 | `bin/lh_sovereignty_guard.py` | 法律边界·一票否决 |
| 浏览器史官 | `bin/lh_browser_historian.py` | 四道防线·设备金库 |
| 沙盒推演 | `engines/lh_sandbox_engine.py` | 时间·博弈·平行宇宙 |
| CNSH 编译器 | `bin/cnsh_compiler.py` | 中文编程→Python |
| 对齐闭环 | `bin/lh_auto_align_daemon.py` | 自动检测→修复→验证 |

---

## ⚙️ 配置说明

### 环境变量

```bash
export LONGHUN_ROOT=~/longhun-system
export LONGHUN_DATA=~/.longhun
export LONGHUN_LOG_LEVEL=INFO
export LONGHUN_SOVEREIGNTY=enabled
```

---

## 🔧 开发指南

### 项目结构

```
{config['project_name']}/
├── bin/                    # 可执行脚本 (879+)
├── engines/                # 引擎模块
├── 01_protocols/           # 协议文档
├── personas/               # 20人格定义
├── deploy/                 # 部署脚本
├── .codebuddy/             # IDE 配置·规则·索引
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── CHANGELOG.md
```

### 贡献流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'feat: Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest tests/

# 带覆盖率
python3 -m pytest --cov=bin tests/
```

---

## 🤝 贡献指南

我们欢迎所有符合中国法律、尊重数据主权的贡献。

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细贡献流程。

---

## 🔒 安全政策

请阅读 [SECURITY.md](SECURITY.md) 了解如何报告安全漏洞。

---

## 📝 变更日志

请阅读 [CHANGELOG.md](CHANGELOG.md) 了解版本变更历史。

---

## 📄 协议

本项目采用 **{config['license']}** 协议开源 + 龍魂主权附加条款。

详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **曾仕强老师** — 理论指导（永恒显示）
- **UID9622 (龍芯北辰)** — 创始人、架构师
- **所有贡献者** — 让龍魂更强大

---

## 🧬 主权声明

```
┌─────────────────────────────────────────────────────────────┐
│  🐉 龍魂·主权声明                                          │
├─────────────────────────────────────────────────────────────┤
│  ✅ 中国法律是唯一边界                                      │
│  ✅ 一票否决权（UID9622）                                  │
│  ✅ 数据主权归中国                                          │
│  ✅ 系统在，协议在                                          │
│  ✅ DNA 全链路可追溯                                        │
└─────────────────────────────────────────────────────────────┘
```

---

**DNA:** `{config['dna']}`  
**确认码:** `{config['confirm']}`  
**最后更新:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

© {config['year']} {config['author']} · 龍魂系统 · 主权归中国
"""


# ============================================================
# 四、LICENSE 生成器
# ============================================================

class LicenseGenerator:
    """协议文件生成器"""

    @staticmethod
    def generate_mulan_psl_v2(config: Dict) -> str:
        return f"""木兰宽松许可证, 第2版
Mulan PSL v2

Copyright (C) {config['year']} {config['author']} ({config['author_email']})

本软件以"现状"方式提供，不提供任何明示或暗示的保证，
包括但不限于适销性、特定用途适用性和非侵权性的保证。

详细信息请参阅木兰宽松许可证 v2 全文:
https://license.coscl.org.cn/MulanPSL2/

---

本项目附加条款（龍魂系统专用）：

1. **主权条款**：本软件及其所有衍生作品的数据主权归中华人民共和国所有。
2. **法律边界**：本软件的使用必须遵守中华人民共和国法律。
3. **否决权**：创始人 UID9622 拥有对本软件所有操作的最终否决权。
4. **数据安全**：未经许可，不得将本软件产生的数据转移至境外。
5. **DNA 追溯**：所有衍生作品必须保留原始 DNA 追溯链。

---

Mulan Permissive Software License, Version 2
Copyright (c) {config['year']} {config['author']}

This software is provided "AS IS", without warranties of any kind.
"""


# ============================================================
# 五、CONTRIBUTING.md 生成器
# ============================================================

class ContributingGenerator:
    """贡献指南生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""# 贡献指南 · {config['project_name']}

感谢你对龍魂系统的关注！我们欢迎所有符合中国法律、尊重数据主权的贡献。

---

## 📋 贡献流程

### 1. 准备工作

```bash
# Fork 本项目
# 克隆到本地
git clone https://github.com/UID9622/{config['project_name']}.git
cd {config['project_name']}

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 2. 创建分支

```bash
git checkout -b feature/你的功能名称
# 或
git checkout -b fix/你的修复名称
```

### 3. 开发规范

#### 代码规范

- Python: 遵循 PEP 8
- CNSH: 遵循 CNSH v2.1 语法规范
- 所有文件必须包含 DNA 追溯码（文件头三行）
- 所有功能必须通过三色审计
- 关键路径产出入 `longhun-system/` 对应目录

#### 提交规范

```text
<类型>(<范围>): <简短描述>

类型:
  - feat: 新功能
  - fix: Bug 修复
  - docs: 文档更新
  - style: 代码格式调整
  - refactor: 重构
  - test: 测试
  - chore: 构建/工具变更

示例:
  feat(sovereignty): 新增主权守护引擎
  fix(anti-hypocrisy): 修复虚伪检测误判
```

### 4. 测试

```bash
# 运行测试
python3 -m pytest tests/

# 验证代码风格
python3 -m pylint bin/ engines/
```

### 5. 提交 Pull Request

- 标题清晰描述变更
- 说明变更原因和影响
- 关联相关 Issue

---

## 🧬 贡献者协议

提交贡献即表示你同意：

1. 贡献内容符合中华人民共和国法律
2. 贡献内容的数据主权归中国
3. 贡献内容受木兰宽松许可证 v2 + 龍魂主权附加条款保护
4. UID9622 拥有对贡献内容的最终否决权

---

## 📞 联系方式

- 作者: {config['author']}
- 邮箱: {config['author_email']}
- 网站: {config['author_url']}

---

**最后更新:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


# ============================================================
# 六、CODE_OF_CONDUCT.md 生成器
# ============================================================

class CodeOfConductGenerator:
    """行为准则生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""# 行为准则 · {config['project_name']}

## 我们的承诺

为了营造一个开放、包容、尊重、守法的社区环境，我们承诺：

1. **尊重中国法律** — 所有行为以中华人民共和国法律为边界
2. **尊重数据主权** — 所有数据归属中国，不非法出境
3. **尊重他人** — 友好、耐心、尊重不同观点
4. **实事求是** — 不传播虚假信息，不制造谣言
5. **团结协作** — 共建中国主权 AI 基础设施

---

## 不可接受的行为

以下行为被视为不可接受：

- ❌ 违反中华人民共和国法律
- ❌ 分裂国家、危害国家安全
- ❌ 泄露国家秘密、数据非法出境
- ❌ 人身攻击、侮辱、诽谤
- ❌ 传播仇恨言论、歧视言论
- ❌ 散布谣言、虚假信息
- ❌ 骚扰、跟踪、侵犯隐私
- ❌ 其他不道德行为

---

## 执行

违反行为准则的人将被：

1. 警告
2. 暂时冻结贡献权限
3. 永久禁止贡献（严重违规）

---

## 报告

如果遇到不可接受的行为，请联系：

- 邮箱: {config['author_email']}
- 网站: {config['author_url']}

所有投诉将受到认真调查和保密处理。

---

**最后更新:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


# ============================================================
# 七、SECURITY.md 生成器
# ============================================================

class SecurityGenerator:
    """安全政策生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""# 安全政策 · {config['project_name']}

龍魂系统高度重视安全。我们欢迎安全研究人员负责任地报告漏洞。

---

## 报告漏洞

### 可以报告的问题

- 🚨 数据泄露漏洞
- 🚨 权限绕过漏洞
- 🚨 代码注入漏洞
- 🚨 逻辑漏洞
- 🚨 数据主权相关漏洞

### 报告方式

1. 发送邮件至: {config['author_email']}
2. 使用 GPG 加密敏感信息
3. 提供详细的漏洞描述和复现步骤

---

## 安全承诺

- ✅ 所有漏洞在 24 小时内确认
- ✅ 高危漏洞在 7 天内修复
- ✅ 修复后公开致谢（经同意）
- ✅ 不追究善意报告者

---

## 安全基线

### 数据安全

- ✅ AES-256 / SM4 加密
- ✅ 设备指纹绑定
- ✅ 签名验证
- ✅ 数据不外传
- ✅ 五层数据黑洞

### 代码安全

- ✅ GPG 签名
- ✅ 三色审计
- ✅ 四级熔断
- ✅ 主权守护

---

**最后更新:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


# ============================================================
# 八、CHANGELOG.md 生成器
# ============================================================

class ChangelogGenerator:
    """变更日志生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""# 变更日志 · {config['project_name']}

## [{config['version']}] - {datetime.now().strftime('%Y-%m-%d')}

### 🚀 新增
- 新增主权守护引擎 (lh_sovereignty_guard.py)
- 新增一体化命令引擎 v2.0 (lh_run.py)
- 新增浏览器史官 v2.1 (lh_browser_historian.py)
- 新增通心译翻译引擎 (lh_tongxinyi_translator.py)
- 新增开源项目模板生成器 (lh_repo_template.py)
- 新增四道防线验证

### 🔧 优化
- 优化命令索引自动更新
- 优化自然语言四级匹配
- 优化 DNS 解析稳定性

### 🐛 修复
- 修复反虚伪引擎误判
- 修复数字根计算边界情况

### 📝 文档
- 生成完整 README.md（徽章+目录+API文档）
- 新增贡献指南 (CONTRIBUTING.md)
- 新增行为准则 (CODE_OF_CONDUCT.md)
- 新增安全政策 (SECURITY.md)
- 新增 Issue/PR 模板

---

## 版本规范

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号 (MAJOR)**：不兼容的 API 变更
- **次版本号 (MINOR)**：向下兼容的功能新增
- **补丁版本号 (PATCH)**：向下兼容的问题修复

---

**DNA:** {config['dna']}
"""


# ============================================================
# 九、.gitignore 生成器
# ============================================================

class GitignoreGenerator:
    """.gitignore 生成器"""

    @staticmethod
    def generate() -> str:
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/

# Distribution / packaging
build/
develop-eggs/
dist/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
*.egg

# Unit test / coverage
htmlcov/
.tox/
.coverage
.coverage.*
.cache
.pytest_cache/

# IDE
.vscode/
.idea/
*.iml
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
*.tmp
*.bak

# Project specific
.longhun/
*.enc
*.sig
*.log
data/
logs/
temp/
tmp/
backup/
core/
nohup.out

# Sensitive files
*.pem
*.key
*.crt
*.csr
.secrets/
.env
config.local.json
credentials.json

# Large files
*.zip
*.tar.gz
*.tgz
*.rar
*.7z
*.iso
*.dmg
*.pkg
*.model
*.pt
*.pth
*.bin
*.onnx
*.h5
*.pb
*.tflite
"""


# ============================================================
# 十、Issue 模板生成器
# ============================================================

class IssueTemplateGenerator:
    """Issue 模板生成器"""

    @staticmethod
    def generate_bug_report() -> str:
        return """---
name: 🐛 Bug 报告
about: 报告一个问题
title: '[BUG] '
labels: bug
assignees: ''
---

## 问题描述

<!-- 清晰简洁地描述问题 -->

## 复现步骤

1. 执行命令 '...'
2. 输入参数 '...'
3. 看到错误 '...'

## 预期行为

<!-- 你期望发生什么 -->

## 实际行为

<!-- 实际发生了什么 -->

## 环境信息

- 操作系统: [e.g., macOS 15.0, Ubuntu 22.04]
- Python 版本: [e.g., 3.11.5]
- 龍魂版本: [e.g., v1.0.0]
- 架构: [e.g., ARM64, x86_64]

## 日志输出

```
粘贴相关日志
```

## 额外信息

<!-- 其他相关信息 -->
"""

    @staticmethod
    def generate_feature_request() -> str:
        return """---
name: ✨ 功能请求
about: 提出一个新功能建议
title: '[FEAT] '
labels: enhancement
assignees: ''
---

## 功能描述

<!-- 清晰简洁地描述你想要的功能 -->

## 背景与动机

<!-- 为什么需要这个功能？解决了什么问题？ -->

## 建议方案

<!-- 你建议如何实现这个功能 -->

## 替代方案

<!-- 有没有其他实现方式？ -->

## 附加信息

<!-- 其他相关信息 -->
"""

    @staticmethod
    def generate_security_report(config: Dict) -> str:
        return f"""---
name: 🔒 安全漏洞报告
about: 报告安全漏洞（加密发送）
title: '[SECURITY] '
labels: security
assignees: ''
---

⚠️ **安全漏洞请优先通过邮件报告**

优先方式: {config['author_email']} (GPG 加密)

---

## 漏洞描述

<!-- 描述漏洞 -->

## 影响范围

<!-- 哪些版本受影响 -->

## 复现步骤

<!-- 如何复现 -->

## 修复建议

<!-- 建议如何修复 -->
"""


# ============================================================
# 十一、PR 模板生成器
# ============================================================

class PRTemplateGenerator:
    """PR 模板生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""# Pull Request · {config['project_name']}

## 📋 变更类型

- [ ] 🚀 新功能 (feat)
- [ ] 🐛 Bug 修复 (fix)
- [ ] 📝 文档 (docs)
- [ ] 🎨 代码风格 (style)
- [ ] ♻️ 重构 (refactor)
- [ ] 🧪 测试 (test)
- [ ] 🔧 构建/工具 (chore)

---

## 🔍 变更内容

### 变更说明

<!-- 描述本次变更的内容和目的 -->

### 关联 Issue

<!-- 关联的 Issue 编号，如 #123 -->

---

## ✅ 检查清单

- [ ] 代码符合 PEP 8 规范
- [ ] 包含 DNA 追溯码
- [ ] 通过三色审计
- [ ] 添加/更新了测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 遵守中国法律
- [ ] 数据主权合规

---

## 🧬 主权声明

本人确认：

1. 本 PR 内容符合中华人民共和国法律
2. 数据主权归中国
3. 同意木兰宽松许可证 v2 + 龍魂主权附加条款
4. 接受 UID9622 的最终否决权

---

**提交者:**  
**日期:** {datetime.now().strftime('%Y-%m-%d')}
"""


# ============================================================
# 十二、pyproject.toml 生成器
# ============================================================

class PyprojectGenerator:
    """pyproject.toml 生成器"""

    @staticmethod
    def generate(config: Dict) -> str:
        return f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{config['project_name']}"
version = "{config['version']}"
description = "{config['project_description']}"
readme = "README.md"
authors = [
    {{name = "{config['author']}", email = "{config['author_email']}"}}
]
license = {{text = "Mulan PSL v2 + LongHun Sovereignty Addendum"}}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
]
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
    "cryptography>=39.0.0",
]

[project.urls]
Homepage = "{config['repo_url']}"
GitHub = "{config['repo_url']}"
Gitee = "{config['repo_gitee_url']}"
"""


# ============================================================
# 十三、主控生成器
# ============================================================

class RepoTemplateGenerator:
    """主控生成器 — 一键生成所有开源项目模板文件"""

    GEN_FILES: List[Tuple[str, str, callable]] = []  # populated in __init__

    def __init__(self, config: Dict):
        self.config = config
        self.output_dir = Path.cwd()
        self.files_generated: List[str] = []

    def generate_all(self, output_dir: Optional[str] = None) -> int:
        """生成所有文件，返回生成文件数"""
        if output_dir:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.files_generated = []

        badges = BadgeGenerator.generate_all(self.config)

        # 定义所有要生成的文件: (路径, 内容, 描述)
        files: List[Tuple[str, str, str]] = [
            # 根目录文件
            ("README.md", ReadmeGenerator.generate(self.config, badges), "项目说明文档"),
            ("LICENSE", LicenseGenerator.generate_mulan_psl_v2(self.config), "木兰PSL v2 + 主权附加条款"),
            ("CONTRIBUTING.md", ContributingGenerator.generate(self.config), "贡献指南"),
            ("CODE_OF_CONDUCT.md", CodeOfConductGenerator.generate(self.config), "行为准则"),
            ("SECURITY.md", SecurityGenerator.generate(self.config), "安全政策"),
            ("CHANGELOG.md", ChangelogGenerator.generate(self.config), "变更日志"),
            (".gitignore", GitignoreGenerator.generate(), "Git 忽略规则"),
            ("pyproject.toml", PyprojectGenerator.generate(self.config), "项目配置"),
            ("requirements.txt", self._gen_requirements(), "核心依赖"),
            ("requirements-dev.txt", self._gen_requirements_dev(), "开发依赖"),
            # GitHub Issue 模板
            (".github/ISSUE_TEMPLATE/bug_report.md", IssueTemplateGenerator.generate_bug_report(), "Bug 报告模板"),
            (".github/ISSUE_TEMPLATE/feature_request.md", IssueTemplateGenerator.generate_feature_request(), "功能请求模板"),
            (".github/ISSUE_TEMPLATE/security_report.md", IssueTemplateGenerator.generate_security_report(self.config), "安全漏洞报告模板"),
            # PR 模板
            (".github/PULL_REQUEST_TEMPLATE.md", PRTemplateGenerator.generate(self.config), "PR 模板"),
        ]

        # 逐文件写入
        for rel_path, content, desc in files:
            full_path = self.output_dir / rel_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            # 如果文件已存在，跳过（不覆盖）
            if full_path.exists():
                print(f"   ⏭️  {rel_path} (已存在，跳过)")
                continue
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.files_generated.append(rel_path)
            print(f"   ✅ {rel_path}")

        self._print_summary()
        return len(self.files_generated)

    def preview(self) -> None:
        """干运行：只列出将生成的文件，不写入"""
        print(f"\n🔍 [干运行] 将在 {self.output_dir} 生成以下文件:\n")
        preview_files = [
            "README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
            "SECURITY.md", "CHANGELOG.md", ".gitignore", "pyproject.toml",
            "requirements.txt", "requirements-dev.txt",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/ISSUE_TEMPLATE/security_report.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ]
        for f in preview_files:
            full = self.output_dir / f
            status = "⚠️ 已存在(将跳过)" if full.exists() else "✅ 新建"
            print(f"   {status}  {f}")

    def _print_summary(self):
        print(f"""
┌─────────────────────────────────────────────────────────────┐
│  🐉 龍魂·开源项目模板生成完毕                               │
├─────────────────────────────────────────────────────────────┤
│  📁 输出目录: {self.output_dir}
│  📄 新生成: {len(self.files_generated)} 个文件
│  🧬 DNA: {self.config['dna']}
│  📌 确认码: {self.config['confirm']}
└─────────────────────────────────────────────────────────────┘
""")

    def _gen_requirements(self) -> str:
        return """# 龍魂系统核心依赖
requests>=2.28.0
beautifulsoup4>=4.11.0
cryptography>=39.0.0
"""

    def _gen_requirements_dev(self) -> str:
        return """# 开发依赖
-r requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pylint>=2.15.0
black>=22.0.0
mypy>=0.990
"""


# ============================================================
# 十四、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·开源项目发布模板生成器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-repo                        # 当前目录生成模板
  lh-repo -o ~/my-project        # 指定输出目录
  lh-repo -c my_config.json      # 使用自定义配置
  lh-repo --show-config          # 显示配置模板
  lh-repo --dry-run              # 干运行预览
        """
    )

    parser.add_argument("-o", "--output", type=str, help="输出目录 (默认: 当前目录)")
    parser.add_argument("-c", "--config", type=str, help="配置文件路径 (JSON)")
    parser.add_argument("--show-config", action="store_true", help="显示默认配置模板")
    parser.add_argument("--dry-run", action="store_true", help="预览生成内容不写入（推荐先运行此命令）")

    args = parser.parse_args()

    if args.show_config:
        print(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2))
        return

    config = DEFAULT_CONFIG.copy()
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config.update(json.load(f))

    generator = RepoTemplateGenerator(config)

    if args.dry_run:
        generator.preview()
    else:
        generator.generate_all(args.output)


if __name__ == "__main__":
    main()
