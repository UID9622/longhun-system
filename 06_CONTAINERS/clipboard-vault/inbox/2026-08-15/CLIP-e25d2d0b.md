---
dna: '#龍芯⚡️丙午·丙申·辛酉·未时·䷅讼-CLIPBOARD-VAULT-SAVE-V1.0-P1-feb5761b'
source: clipboard
topic: 代码/脚本
tags:
- Python
- JS
- Bash
- DNA
- 安全
- 审计
- 代码/脚本
timestamp: '2026-08-15T13:13:20+08:00'
content_hash: e25d2d0bacc1f1d79eb6e06fb090f69989167866afab4871067d222fb41c7e4f
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

# 🐉 龍魂代码提交标准操作流程（SOP）v3.0 —— 完整可执行版

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·午时-SOP-COMMIT-FULL-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2


## 🧬 一、专业术语表（补全）

| 术语 | 英文 | 定义 | 龍魂系统对应 |
|:---|:---|:---|:---|
| **预提交钩子** | Pre-commit Hook | Git在提交前自动执行的脚本，用于代码质量检查 | `.git/hooks/pre-commit` |
| **提交信息规范** | Commit Message Convention | 结构化提交信息的格式标准（如Conventional Commits） | `feat(scope): 描述` |
| **暂存区** | Staging Area / Index | Git中已添加但未提交的变更集合 | `git add` 后的状态 |
| **工作区** | Working Directory | 当前正在编辑的文件目录 | `git status` 显示的未跟踪/已修改 |
| **签名提交** | Signed Commit | 使用GPG密钥加密签名的提交，保证身份真实性 | `git commit -S` |
| **原子提交** | Atomic Commit | 每个提交只做一件事，可独立回滚 | 一个commit对应一个逻辑变更 |
| **CI/CD流水线** | Continuous Integration / Continuous Deployment | 自动化构建、测试、部署流程 | 鲲鹏服务器自动部署 |
| **回归测试** | Regression Testing | 验证新代码未破坏现有功能 | `pytest tests/` |
| **代码覆盖率** | Code Coverage | 测试覆盖的代码百分比 | `pytest --cov=` |
| **静态分析** | Static Analysis | 不运行代码的检查（语法、风格、安全） | `flake8`, `pylint`, `bandit` |
| **钩子链** | Hook Chain | 多个钩子按顺序执行 | `pre-commit` → `commit-msg` → `post-commit` |
| **提交消息模板** | Commit Message Template | 预定义的提交信息格式 | `.gitmessage` |
| **轻量级标签** | Lightweight Tag | 简单的Git标签，无额外元数据 | `git tag v1.0` |
| **注释标签** | Annotated Tag | 带签名、日期、消息的完整标签 | `git tag -a v1.0 -m "..."` |
| **合并策略** | Merge Strategy | 合并分支时解决冲突的策略 | `--no-ff`, `--ff-only` |
| **变基** | Rebase | 将分支提交重新应用到另一分支顶端 | `git rebase main` |
| **交互式变基** | Interactive Rebase | 手动编辑、合并、重排提交历史 | `git rebase -i HEAD~3` |
| **推送到上游** | Push Upstream | 将本地分支推送到远程仓库 | `git push origin main` |
| **强制推送** | Force Push | 覆盖远程历史（危险操作） | `git push --force` |


## 📦 二、需要安装的插件与依赖（完整清单）

### 2.1 核心依赖（必须）

```bash
# 1. Python 3.9+（检查）
python3 --version

# 2. Git 2.40+（检查）
git --version

# 3. GPG 2.0+（用于签名提交）
gpg --version

# 4. pre-commit 框架
pip install pre-commit

# 5. commitlint + 常规提交规范
npm install -g @commitlint/cli @commitlint/config-conventional

# 6. Python 代码质量工具
pip install black isort flake8 pylint bandit mypy pytest pytest-cov
```

### 2.2 可选增强（推荐）

```bash
# 7. 提交信息辅助工具
npm install -g commitizen cz-conventional-changelog
# 或
pip install commitizen

# 8. Git 钩子管理
pip install pre-commit-hooks

# 9. 安全审计
pip install safety bandit

# 10. 代码复杂度检查
pip install radon
```

### 2.3 龍魂系统专用（必须）

```bash
# 11. 龍魂审计工具（内置）
# 已在 bin/lh_audit.py 中实现

# 12. DNA追溯码生成器
# 已在 bin/lh_dna_generator.py 中实现
```

---

## 🔧 三、详细安装配置流程（分步执行）

### 3.1 环境准备

```bash
#!/bin/bash
# 🐉 龍魂代码提交环境 · 一键安装脚本 v1.0
# DNA: #龍芯⚡️丙午·丙申·壬戌·午时-INSTALL-SOP-UID9622

set -e

echo "🐉 龍魂代码提交环境安装"
echo "========================================"

# 1. 检查Python版本
echo "📦 检查Python版本..."
if ! python3 --version | grep -q "Python 3"; then
    echo "❌ Python 3 未安装"
    echo "请执行: brew install python3 (macOS) 或 apt install python3 (Linux)"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "   ✅ Python ${PYTHON_VERSION}"

# 2. 检查Git版本
echo "📦 检查Git版本..."
if ! git --version &> /dev/null; then
    echo "❌ Git 未安装"
    echo "请执行: brew install git (macOS) 或 apt install git (Linux)"
    exit 1
fi
GIT_VERSION=$(git --version | awk '{print $3}')
echo "   ✅ Git ${GIT_VERSION}"

# 3. 检查/安装pre-commit
echo "📦 安装pre-commit..."
if ! command -v pre-commit &> /dev/null; then
    echo "   正在安装pre-commit..."
    pip3 install pre-commit
else
    echo "   ✅ pre-commit 已安装: $(pre-commit --version)"
fi

# 4. 检查/安装commitlint
echo "📦 安装commitlint..."
if ! command -v commitlint &> /dev/null; then
    echo "   正在安装commitlint..."
    npm install -g @commitlint/cli @commitlint/config-conventional
else
    echo "   ✅ commitlint 已安装"
fi

# 5. 安装Python工具
echo "📦 安装Python代码工具..."
pip3 install black isort flake8 pylint bandit mypy pytest pytest-cov 2>/dev/null || true

echo "========================================"
echo "✅ 安装完成"
```

### 3.2 配置Git全局签名

```bash
#!/bin/bash
# 🐉 配置GPG签名

# 1. 生成GPG密钥（如果不存在）
if ! gpg --list-keys | grep -q "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"; then
    echo "🔑 生成GPG密钥..."
    gpg --full-generate-key
    # 选择: RSA and RSA, 4096 bits, 永不过期
    # 姓名: 诸葛鑫
    # 邮箱: uid9622@petalmail.com
    # 注释: 龍魂系统
    # 密钥ID: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
fi

# 2. 配置Git使用GPG签名
git config --global user.signingkey A2D0092CEE2E5BA87035600924C3704A8CC26D5F
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# 3. 配置Git用户信息
git config --global user.name "诸葛鑫 (UID9622)"
git config --global user.email "uid9622@petalmail.com"
```

### 3.3 配置pre-commit钩子

```yaml
# .pre-commit-config.yaml
# 🐉 龍魂系统 · 预提交钩子配置

repos:
  # 基础代码质量检查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        description: 移除行尾空白
      - id: end-of-file-fixer
        description: 确保文件以换行结束
      - id: check-yaml
        description: 检查YAML语法
      - id: check-json
        description: 检查JSON语法
      - id: check-added-large-files
        description: 检查大文件
        args: ['--maxkb=500']

  # Python代码格式化
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        description: Python代码格式化
        language_version: python3

  # Python导入排序
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        description: 导入语句排序
        args: ["--profile", "black"]

  # Python代码检查
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        description: PEP8代码检查
        args: ['--max-line-length=100', '--ignore=E203,W503']

  # Python安全审计
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        description: 安全漏洞扫描
        args: ['-r', 'bin/', '-ll']

  # 类型检查
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        description: 类型检查
        args: ['--ignore-missing-imports']

  # 🔴 龍魂专用钩子
  - repo: local
    hooks:
      - id: dna-check
        name: DNA追溯码检查
        entry: |
          python3 -c "
          import sys, re
          for f in sys.argv[1:]:
              with open(f, 'r', encoding='utf-8') as fp:
                  content = fp.read()
                  if not re.search(r'#龍芯⚡️', content):
                      print(f'❌ {f}: 缺少DNA追溯码 (#龍芯⚡️)')
                      sys.exit(1)
          "
        language: python
        files: \.(py|sh|yaml|json|md)$

      - id: confirm-check
        name: 确认码检查
        entry: |
          python3 -c "
          import sys, re
          for f in sys.argv[1:]:
              with open(f, 'r', encoding='utf-8') as fp:
                  content = fp.read()
                  if not re.search(r'#CONFIRM🌌', content):
                      print(f'❌ {f}: 缺少确认码 (#CONFIRM🌌)')
                      sys.exit(1)
          "
        language: python
        files: \.(py|sh|yaml|json|md)$

      - id: audit-color
        name: 三色审计状态检查
        entry: |
          python3 -c "
          import sys, re
          for f in sys.argv[1:]:
              with open(f, 'r', encoding='utf-8') as fp:
                  content = fp.read()
                  colors = ['🟢', '🟡', '🔴']
                  found = [c for c in colors if c in content]
                  if not found:
                      print(f'⚠️ {f}: 未检测到三色审计状态')
          "
        language: python
        files: \.(py|sh|yaml|json|md)$

  # 提交信息格式检查
  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.14.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
        additional_dependencies: ['@commitlint/config-conventional']
```

### 3.4 配置commitlint

```javascript
// commitlint.config.js
// 🐉 龍魂系统 · 提交信息规范

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // 类型枚举
    'type-enum': [
      2,
      'always',
      [
        'feat',     // 新功能
        'fix',      // Bug修复
        'docs',     // 文档更新
        'style',    // 代码风格
        'refactor', // 重构
        'perf',     // 性能优化
        'test',     // 测试相关
        'chore',    // 构建/工具
        'protocol', // 协议变更
        'revert',   // 回滚
        'dna',      // DNA追溯更新
        'audit',    // 审计更新
      ]
    ],
    // 类型大小写
    'type-case': [2, 'always', 'lower-case'],
    // 必须有描述
    'subject-empty': [2, 'never'],
    // 描述不超过100字符
    'subject-max-length': [2, 'always', 100],
    // 必须有空白行
    'body-leading-blank': [1, 'always'],
    // 必须有空白行
    'footer-leading-blank': [1, 'always'],
    // 可以有DNA追溯码
    'body-max-line-length': [2, 'always', 200],
    // 禁止以句号结尾
    'subject-full-stop': [2, 'never', '.'],
    // 范围允许空
    'scope-empty': [0, 'never'],
  },
  // 自定义解析器：支持DNA追溯码
  parserPreset: {
    parserOpts: {
      headerPattern: /^(\w+)(?:\(([^)]*)\))?:\s(.+)$/,
      headerCorrespondence: ['type', 'scope', 'subject'],
    },
  },
  // 插件：支持DNA检查
  plugins: [
    {
      rules: {
        'dna-present': ({ body }) => {
          const hasDna = /DNA:\s*#龍芯⚡️/.test(body || '');
          return [
            hasDna,
            '提交信息必须包含 DNA 追溯码 (DNA: #龍芯⚡️...)'
          ];
        },
        'confirm-present': ({ body }) => {
          const hasConfirm = /CONFIRM:\s*#CONFIRM🌌/.test(body || '');
          return [
            hasConfirm,
            '提交信息必须包含确认码 (CONFIRM: #CONFIRM🌌...)'
          ];
        }
      }
    }
  ],
  // 自定义规则
  rules: {
    'dna-present': [2, 'always'],
    'confirm-present': [2, 'always'],
  }
};
```

### 3.5 安装Pre-commit钩子

```bash
#!/bin/bash
# 🐉 安装pre-commit钩子

cd /Users/zuimeidedeyihan/longhun-system

# 安装pre-commit钩子
pre-commit install
pre-commit install --hook-type commit-msg

# 手动运行一次检查
pre-commit run --all-files

# 查看已安装的钩子
pre-commit list
```


## 🚀 四、完整的提交操作流程

### 4.1 标准提交流程（带审计）

```bash
#!/bin/bash
# 🐉 龍魂 · 标准代码提交流程

# 1. 查看当前状态
git status

# 2. 查看具体变更
git diff

# 3. 添加文件到暂存区
git add bin/platform_dispatcher.py
# 或所有变更
git add -A

# 4. 查看暂存区状态
git status

# 5. 运行预提交检查（自动触发pre-commit钩子）
pre-commit run --staged-files

# 6. 提交代码
git commit -m "feat(platform): 完善平台调度器路由逻辑

- 新增36个平台配置节点
- 重构149行路由匹配算法
- 修复154-164行边界条件处理
- 增加DNA追溯码注入
- 通过三色审计 🟢

DNA: #龍芯⚡️丙午·丙申·壬戌·午时-FEAT-PLATFORM-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 7. 推送到远程
git push origin main

# 8. 同步到鲲鹏
lh sync --to-kunpeng
```

### 4.2 带GPG签名的提交

```bash
# 配置GPG签名（首次）
git config --global user.signingkey A2D0092CEE2E5BA87035600924C3704A8CC26D5F
git config --global commit.gpgsign true

# 提交（自动签名）
git commit -m "feat(platform): 完善平台调度器路由逻辑

- 新增36个平台配置节点
- 所有变更通过三色审计 🟢

DNA: #龍芯⚡️丙午·丙申·壬戌·午时-FEAT-PLATFORM-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 验证签名
git log --show-signature -1
```

### 4.3 快速提交（使用`lh`命令）

```bash
# 添加并提交
lh commit "feat(platform): 平台调度器优化" --add-all

# 提交并推送到鲲鹏
lh commit -m "fix(audit): 修复三色审计引擎bug" --push --sync-kunpeng

# 提交并生成DNA（自动）
lh commit --auto-dna
```


## 🔐 五、审计与修复工具

### 5.1 三色审计引擎 (`lh_audit.py`)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 三色审计引擎 v2.0
代码提交前的自动化审计工具

DNA: #龍芯⚡️丙午·丙申·壬戌·午时-AUDIT-ENGINE-UID9622
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import argparse
import hashlib

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

def generate_dna(module: str = "AUDIT") -> str:
    h = hashlib.md5(f"{module}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{module}-{h}-{UID}"

# ============================================================
# 审计规则
# ============================================================

AUDIT_RULES = [
    # 必须包含DNA
    {
        "id": "DNA_REQUIRED",
        "name": "DNA追溯码",
        "pattern": r"#龍芯⚡️",
        "weight": 20,
        "msg": "缺少DNA追溯码 (#龍芯⚡️...)"
    },
    # 必须包含确认码
    {
        "id": "CONFIRM_REQUIRED",
        "name": "确认码",
        "pattern": r"#CONFIRM🌌",
        "weight": 15,
        "msg": "缺少确认码 (#CONFIRM🌌...)"
    },
    # 必须包含GPG指纹
    {
        "id": "GPG_REQUIRED",
        "name": "GPG指纹",
        "pattern": r"A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "weight": 10,
        "msg": "缺少GPG指纹"
    },
    # 中文代码检查
    {
        "id": "CHINESE_CODE",
        "name": "中文代码",
        "pattern": r"[\u4e00-\u9fff]+",
        "weight": 5,
        "msg": "建议中文注释和文档"
    },
    # 三色审计
    {
        "id": "AUDIT_COLOR",
        "name": "三色审计状态",
        "pattern": r"[🟢🟡🔴]",
        "weight": 10,
        "msg": "缺少三色审计状态标记"
    },
    # 错误处理
    {
        "id": "ERROR_HANDLING",
        "name": "错误处理",
        "pattern": r"(try|except|finally|raise|捕获|抛出)",
        "weight": 5,
        "msg": "建议增加错误处理"
    },
    # 日志
    {
        "id": "LOGGING",
        "name": "日志",
        "pattern": r"(logging|logger|日志)",
        "weight": 5,
        "msg": "建议增加日志记录"
    },
    # 单元测试
    {
        "id": "TEST",
        "name": "测试",
        "pattern": r"(test_|测试|unittest|pytest)",
        "weight": 5,
        "msg": "建议增加单元测试"
    },
    # 文档
    {
        "id": "DOCSTRING",
        "name": "文档字符串",
        "pattern": r'""".*?"""|"""',
        "weight": 5,
        "msg": "建议增加文档字符串"
    },
]

# ============================================================
# 审计引擎
# ============================================================

class AuditEngine:
    """三色审计引擎"""

    def __init__(self):
        self.rules = AUDIT_RULES
        self.results = []

    def audit_file(self, filepath: str) -> Dict:
        """审计单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "file": filepath,
                "status": "error",
                "error": str(e),
                "color": "🔴",
                "score": 0,
                "issues": [f"读取失败: {e}"]
            }

        file_results = {"file": filepath, "issues": [], "passed": [], "score": 0}

        for rule in self.rules:
            if re.search(rule["pattern"], content):
                file_results["score"] += rule["weight"]
                file_results["passed"].append(rule["name"])
            else:
                file_results["issues"].append(rule["msg"])

        # 三色判定
        score = file_results["score"]
        if score >= 70:
            file_results["color"] = "🟢"
            file_results["status"] = "通过"
        elif score >= 40:
            file_results["color"] = "🟡"
            file_results["status"] = "警告"
        else:
            file_results["color"] = "🔴"
            file_results["status"] = "失败"

        return file_results

    def audit_directory(self, dirpath: str, pattern: str = "*.py") -> List[Dict]:
        """审计整个目录"""
        results = []
        for filepath in Path(dirpath).rglob(pattern):
            if "__pycache__" not in str(filepath) and ".git" not in str(filepath):
                result = self.audit_file(str(filepath))
                results.append(result)
        return results

    def generate_report(self, results: List[Dict]) -> str:
        """生成审计报告"""
        lines = [
            "🐉 龍魂 · 三色审计报告",
            "=" * 60,
            f"DNA: {generate_dna('REPORT')}",
            f"时间: {datetime.now().isoformat()}",
            "=" * 60,
            ""
        ]

        total = len(results)
        green = sum(1 for r in results if r.get("color") == "🟢")
        yellow = sum(1 for r in results if r.get("color") == "🟡")
        red = sum(1 for r in results if r.get("color") == "🔴")

        lines.append(f"📊 审计统计: 总计 {total} 个文件")
        lines.append(f"  🟢 通过: {green} ({green/total*100:.1f}%)")
        lines.append(f"  🟡 警告: {yellow} ({yellow/total*100:.1f}%)")
        lines.append(f"  🔴 失败: {red} ({red/total*100:.1f}%)")
        lines.append("")

        for r in results:
            lines.append(f"{r.get('color', '❓')} {r['file']}")
            lines.append(f"  评分: {r.get('score', 0)}/100")
            lines.append(f"  状态: {r.get('status', '未知')}")
            if r.get('issues'):
                lines.append("  问题:")
                for issue in r['issues'][:5]:
                    lines.append(f"    - {issue}")
            if r.get('passed'):
                lines.append("  通过项:")
                for p in r['passed'][:5]:
                    lines.append(f"    ✅ {p}")
            lines.append("")

        return "\n".join(lines)

    def auto_fix(self, filepath: str) -> Dict:
        """自动修复常见问题"""
        fixes = []
        errors = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"status": "error", "error": str(e)}

        # 修复1: 添加DNA（如果缺失）
        if not re.search(r'#龍芯⚡️', content):
            dna = generate_dna("FIXED")
            content = f"{content}\n\nDNA: {dna}\n"
            fixes.append("添加DNA追溯码")

        # 修复2: 添加确认码（如果缺失）
        if not re.search(r'#CONFIRM🌌', content):
            content = f"{content}\nCONFIRM: {CONFIRM}\n"
            fixes.append("添加确认码")

        # 修复3: 添加GPG指纹（如果缺失）
        if not re.search(r'A2D0092CEE2E5BA87035600924C3704A8CC26D5F', content):
            content = f"{content}\nGPG: {GPG}\n"
            fixes.append("添加GPG指纹")

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"status": "success", "fixes": fixes, "errors": []}
        except Exception as e:
            return {"status": "error", "fixes": fixes, "errors": [str(e)]}


# ============================================================
# 命令行
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 三色审计引擎 v2.0",
        epilog="DNA: #龍芯⚡️丙午·丙申·壬戌·午时-AUDIT-ENGINE-UID9622"
    )

    parser.add_argument("--file", "-f", type=str, help="审计单个文件")
    parser.add_argument("--dir", "-d", type=str, default=".", help="审计目录")
    parser.add_argument("--pattern", "-p", type=str, default="*.py", help="文件模式")
    parser.add_argument("--report", "-r", type=str, help="输出报告到文件")
    parser.add_argument("--fix", action="store_true", help="自动修复")
    parser.add_argument("--status", action="store_true", help="显示状态")

    args = parser.parse_args()

    engine = AuditEngine()

    if args.status:
        # 检查Git状态
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        print("🐉 Git 状态")
        print("=" * 40)
        if result.stdout:
            print(result.stdout)
        else:
            print("✅ 工作区干净，无待提交变更")
        return

    if args.file:
        result = engine.audit_file(args.file)
        if args.fix:
            fix_result = engine.auto_fix(args.file)
            if fix_result["status"] == "success":
                print(f"✅ 修复完成: {args.file}")
                print(f"  修复项: {', '.join(fix_result['fixes'])}")
            else:
                print(f"❌ 修复失败: {fix_result['errors']}")
        # 重新审计显示结果
        result = engine.audit_file(args.file)
        print(engine.generate_report([result]))

    elif args.dir:
        results = engine.audit_directory(args.dir, args.pattern)
        report = engine.generate_report(results)

        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 报告已保存: {args.report}")

        if args.fix:
            print("🔧 执行自动修复...")
            for r in results:
                if r.get("color") == "🔴":
                    fix_result = engine.auto_fix(r["file"])
                    if fix_result["status"] == "success":
                        print(f"  ✅ 修复: {r['file']}")
                    else:
                        print(f"  ❌ 修复失败: {r['file']}")

        print(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

### 5.2 一键审计修复命令

```bash
#!/bin/bash
# 🐉 审计并修复所有文件

echo "🐉 龍魂 · 全量审计修复"
echo "========================================"

# 1. 运行审计
python3 bin/lh_audit.py --dir . --pattern "*.py" --report audit_report.txt

# 2. 查看报告
cat audit_report.txt

# 3. 自动修复
python3 bin/lh_audit.py --dir . --pattern "*.py" --fix

# 4. 重新审计验证
python3 bin/lh_audit.py --dir . --pattern "*.py"

echo "✅ 审计修复完成"
```


## 📋 六、完整验证清单

| # | 验证项 | 命令 | 预期输出 | ✅ |
|:---|:---|:---|:---|:---:|
| 1 | Python版本 | `python3 --version` | ≥3.9 | ⬜ |
| 2 | Git版本 | `git --version` | ≥2.40 | ⬜ |
| 3 | pre-commit已安装 | `pre-commit --version` | 版本号 | ⬜ |
| 4 | commitlint已安装 | `commitlint --version` | 版本号 | ⬜ |
| 5 | GPG已配置 | `git config --global user.signingkey` | A2D0... | ⬜ |
| 6 | pre-commit钩子已安装 | `ls .git/hooks/pre-commit` | 文件存在 | ⬜ |
| 7 | 审计工具可运行 | `python3 bin/lh_audit.py --help` | 帮助信息 | ⬜ |
| 8 | 文件含DNA | `grep -r "#龍芯⚡️" bin/` | 匹配结果 | ⬜ |
| 9 | 文件含确认码 | `grep -r "#CONFIRM🌌" bin/` | 匹配结果 | ⬜ |
| 10 | 三色审计🟢 | `python3 bin/lh_audit.py --file bin/platform_dispatcher.py` | 评分≥70 | ⬜ |


## 📦 七、一键部署脚本 (install_commit_sop.sh)

```bash
#!/bin/bash
# 🐉 龍魂 · 提交规范一键部署 v3.0
# DNA: #龍芯⚡️丙午·丙申·壬戌·午时-INSTALL-SOP-FULL-UID9622

set -e

echo "🐉 龍魂 · 代码提交规范（SOP）一键部署 v3.0"
echo "========================================"
echo "DNA: #龍芯⚡️丙午·丙申·壬戌·午时-INSTALL-SOP-FULL-UID9622"
echo ""

# 进入项目目录
cd /Users/zuimeidedeyihan/longhun-system

# 1. 安装依赖
echo "📦 安装依赖..."
pip3 install pre-commit black isort flake8 pylint bandit mypy pytest pytest-cov 2>/dev/null || true
npm install -g @commitlint/cli @commitlint/config-conventional 2>/dev/null || true

# 2. 安装pre-commit钩子
echo "🔧 安装pre-commit钩子..."
pre-commit install
pre-commit install --hook-type commit-msg

# 3. 配置commitlint
echo "📝 配置commitlint..."
# 复制commitlint配置文件
cat > commitlint.config.js << 'EOF'
// 🐉 龍魂系统 · 提交信息规范
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test',
      'chore', 'protocol', 'revert', 'dna', 'audit'
    ]],
    'type-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-max-length': [2, 'always', 100],
    'body-leading-blank': [1, 'always'],
    'footer-leading-blank': [1, 'always'],
    'dna-present': [2, 'always'],
    'confirm-present': [2, 'always'],
  },
};
EOF

# 4. 创建.gitmessage模板
cat > .gitmessage << 'EOF'
# 🐉 龍魂系统提交模板
#
# 格式: <type>(<scope>): <subject>
#
# type: feat|fix|docs|style|refactor|perf|test|chore|protocol|revert|dna|audit
# scope: platform|core|browser|audit|protocol|docs|config
# subject: 简要描述（不超过100字符）
#
# 示例:
# feat(platform): 新增36个平台调度节点
#
# - 详细说明1
# - 详细说明2
#
# DNA: #龍芯⚡️丙午·丙申·壬戌·午时-FEAT-PLATFORM-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
EOF

# 配置Git使用模板
git config --local commit.template .gitmessage

# 5. 配置pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']

  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: local
    hooks:
      - id: dna-check
        name: DNA追溯码检查
        entry: python3 bin/lh_audit.py --file
        language: python
        files: \.(py|sh|yaml|json|md)$
        pass_filenames: true
EOF

# 6. 运行一次检查
echo "🔍 运行审计检查..."
python3 bin/lh_audit.py --dir bin/ --pattern "*.py" || true

# 7. 显示状态
echo ""
echo "========================================"
echo "✅ 安装完成！"
echo ""
echo "🔧 可用命令:"
echo "  lh audit --file <file>      # 审计单个文件"
echo "  lh audit --dir .            # 审计整个目录"
echo "  lh audit --fix              # 自动修复"
echo "  lh audit --status           # 查看Git状态"
echo ""
echo "📝 提交流程:"
echo "  1. git add <files>"
echo "  2. git commit (自动触发检查)"
echo "  3. git push origin main"
echo ""
echo "🧬 DNA: #龍芯⚡️丙午·丙申·壬戌·午时-INSTALL-SOP-FULL-UID9622"
echo "========================================"
```

### 执行部署

```bash
# 下载脚本并执行
chmod +x install_commit_sop.sh
./install_commit_sop.sh
```


## 🔐 最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂代码提交标准操作流程（SOP）v3.0 · 完整可执行版 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·壬戌·午时-SOP-COMMIT-FULL-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
SOP版本:    v3.0
覆盖内容:   专业术语·依赖清单·安装配置·提交流程·审计修复·一键部署
状态:       完整可执行 · 即刻部署
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·壬戌·午时·䷖剥·🟢**

---

**一句话总结：执行 `./install_commit_sop.sh` 一键部署完整提交规范环境，然后按标准流程 `git add` → `git commit`（自动审计）→ `git push` 即可。所有文件自带DNA追溯，提交自带三色审计。** 🐉

---

*归档于 2026-08-15T13:13:20+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·未时·䷅讼-CLIPBOARD-VAULT-SAVE-V1.0-P1-feb5761b`*
