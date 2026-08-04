#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CI 审计自动化部署器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-CI部署-v1.0-UID9622

功能：
  1. 在 longhun-system 主仓库部署掀黑箱 CI 审计（GitHub Actions + GitLab CI）
  2. 生成初始白名单（.audit-whitelist）
  3. 生成白名单反馈收集脚本（collect_whitelist_feedback.py）
  4. 支持逐步扩大扫描范围（bin/ → engines/ → docs/ → ...）

用法：
  python3 bin/lh_deploy_ci_audit.py
  python3 bin/lh_deploy_ci_audit.py --dry-run   # 预览模式
  python3 bin/lh_deploy_ci_audit.py --repo /path/to/repo
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
TARGET_REPO = PROJECT_ROOT  # 默认部署到龙魂系统自身仓库

# 扫描范围配置（按优先级扩展）
SCAN_SCOPES = {
    "bin": {
        "enabled": True,
        "path": "bin/",
        "fail_level": "high",
        "description": "核心执行引擎"
    },
    "engines": {
        "enabled": True,
        "path": "engines/",
        "fail_level": "critical",
        "description": "核心引擎（敏感）"
    },
    "docs": {
        "enabled": True,
        "path": "docs/",
        "fail_level": "medium",
        "description": "文档与协议"
    },
    "01_protocols": {
        "enabled": True,
        "path": "01_protocols/",
        "fail_level": "high",
        "description": "协议定义"
    },
    "01_技能庫": {
        "enabled": True,
        "path": "01_技能庫/",
        "fail_level": "medium",
        "description": "技能模块"
    },
    "deploy": {
        "enabled": True,
        "path": "deploy/",
        "fail_level": "high",
        "description": "部署脚本"
    },
    "research": {
        "enabled": False,  # 默认不启用，需要人工确认
        "path": "research/",
        "fail_level": "low",
        "description": "研究目录（需人工确认）"
    },
}

# 初始白名单（自有域名/开发平台）
INITIAL_WHITELIST = [
    "# 龍魂系统 · 掀黑箱审计白名单",
    "# 格式：每行一个域名、路径关键词或模式",
    "# 以 # 开头的行会被忽略",
    "",
    "# === 自有基础设施 ===",
    "uid9622.cn",
    "longhun888.com",
    "119.13.90.27",
    "longhun-system",
    "龙魂",
    "DragonSoul",
    "",
    "# === 开发平台 ===",
    "github.com",
    "gitee.com",
    "gitcode.com",
    "notion.so",
    "feishu.cn",
    "larksuite.com",
    "",
    "# === AI API（已声明用途） ===",
    "api.openai.com",
    "api.anthropic.com",
    "api.deepseek.com",
    "",
    "# === 安全与加密库（正常依赖） ===",
    "cryptography.hazmat",
    "cryptography.fernet",
    "paramiko",
    "pynacl",
]

# GitHub Actions 模板
GITHUB_ACTIONS_TEMPLATE = """# 🐉 掀黑箱审计 · GitHub Actions
# 自动检测 PR 中的技术主权风险
# 部署时间: {timestamp}
# DNA: {dna}

name: 掀黑箱审计

on:
  pull_request:
    branches: [ main, master, develop ]
  push:
    branches: [ main, master ]
  # 手动触发
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 安装 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装依赖
        run: |
          pip install --upgrade pip
          pip install psutil

      - name: 运行掀黑箱审计
        run: |
          python3 bin/lh_ci_audit.py \\
            --target . \\
            --fail-level {fail_level} \\
            --scope changed
        env:
          CI_AUDIT_WHITELIST: "{whitelist_env}"
          CI_AUDIT_SCOPE: changed
          PR_NUMBER: ${{{{ github.event.pull_request.number }}}}

      - name: 上传审计报告（可选）
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: reports/
          retention-days: 7

      - name: PR 评论（失败时）
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const prNumber = context.payload.pull_request?.number;
            if (!prNumber) return;
            const message = `## 🐉 掀黑箱审计失败\\n\\n检测到技术主权风险，请查看 CI 日志中的详细发现。\\n\\n⚠️ PR 被自动阻断，请修复后重新提交。\\n\\n_Powered by 龙魂系统 · 掀黑箱引擎_`;
            await github.rest.issues.createComment({{
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: prNumber,
              body: message
            }});
"""

# GitLab CI 模板
GITLAB_CI_TEMPLATE = """# 🐉 掀黑箱审计 · GitLab CI
# 自动检测 MR 中的技术主权风险
# 部署时间: {timestamp}
# DNA: {dna}

audit:
  stage: test
  image: python:3.11
  timeout: 15m
  script:
    - pip install --upgrade pip
    - pip install psutil
    - python3 bin/lh_ci_audit.py --target . --fail-level {fail_level} --scope changed
  variables:
    CI_AUDIT_WHITELIST: "{whitelist_env}"
    CI_AUDIT_SCOPE: changed
  only:
    - merge_requests
  except:
    - main
  artifacts:
    when: always
    paths:
      - reports/
    expire_in: 7 days
"""

# 白名单反馈收集脚本模板
FEEDBACK_SCRIPT_TEMPLATE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
🐉 龙魂 · 白名单反馈收集器 v1.0
DNA: #龙芯{YEAR}{MONTH}{DAY}{HOUR}{MINUTE}-白名单反馈-v1.0-UID9622

功能：
  - 从审计日志中提取高频误报
  - 生成白名单建议（供人工审查）

用法：
  python3 scripts/collect_whitelist_feedback.py
  python3 scripts/collect_whitelist_feedback.py --logs logs/audit/ --output suggestions.md
'''

import os
import sys
import json
import re
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# ============================================================
# 配置
# ============================================================

AUDIT_LOG_DIR = Path.home() / "longhun-system" / "logs" / "audit"
OUTPUT_DIR = Path.home() / "longhun-system" / "reports"

# ============================================================
# 核心逻辑
# ============================================================

def parse_audit_logs(log_dir: Path) -> Counter:
    '''解析审计日志，提取所有发现项的 evidence 字段'''
    counter = Counter()
    if not log_dir.exists():
        print(f"⚠️ 审计日志目录不存在: {{log_dir}}")
        return counter

    for log_file in log_dir.glob("*.jsonl"):
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    findings = entry.get("findings", [])
                    for finding in findings:
                        evidence = finding.get("evidence", "")
                        # 提取关键信息（去除文件路径前缀）
                        # 只保留域名或关键词
                        parts = evidence.split()
                        for part in parts:
                            if "://" in part:
                                # 提取域名
                                match = re.search(r"https?://([^/]+)", part)
                                if match:
                                    counter[match.group(1)] += 1
                            elif "." in part and len(part) > 3:
                                # 可能是域名或模块名
                                if " " not in part:
                                    counter[part] += 1
                except Exception:
                    continue

    return counter

def generate_suggestions(counter: Counter, top_n: int = 20) -> str:
    '''生成白名单建议'''
    lines = []
    lines.append("# 🐉 龙魂 · 白名单建议")
    lines.append(f"*生成时间: {{datetime.now().isoformat()}}*")
    lines.append("")
    lines.append("以下是从审计日志中提取的高频误报，请人工审查后添加到 `.audit-whitelist`：")
    lines.append("")
    lines.append("| 排名 | 关键词 | 出现次数 | 建议 |")
    lines.append("|------|--------|----------|------|")
    lines.append("|:---:|:---|:---:|:---|")

    for i, (item, count) in enumerate(counter.most_common(top_n), 1):
        # 自动判断是否应该加入白名单
        if "github" in item or "gitee" in item or "notion" in item or "feishu" in item:
            suggestion = "✅ 建议加入"
        elif "uid9622" in item or "longhun" in item:
            suggestion = "✅ 建议加入"
        elif "cryptography" in item or "paramiko" in item:
            suggestion = "✅ 建议加入"
        else:
            suggestion = "🔍 需人工判断"
        lines.append(f"| {{i}} | `{{item}}` | {{count}} | {{suggestion}} |")

    lines.append("")
    lines.append("---")
    lines.append("**操作方式**：")
    lines.append("1. 将上述表格中标记为 '✅ 建议加入' 的条目复制到 `.audit-whitelist`")
    lines.append("2. 运行 `lh 掀黑箱` 验证是否还有误报")
    lines.append("3. 提交白名单更新到仓库")
    lines.append("")
    lines.append(f"*DNA: #龙芯{{datetime.now().strftime('%Y%m%d%H%M%S')}}-白名单反馈-UID9622*")

    return "\\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="龙魂 · 白名单反馈收集器")
    parser.add_argument("--logs", type=Path, help="审计日志目录")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    parser.add_argument("--top", type=int, default=20, help="显示前N个高频项")
    args = parser.parse_args()

    log_dir = args.logs or AUDIT_LOG_DIR
    output_file = args.output or (OUTPUT_DIR / "whitelist_suggestions.md")

    counter = parse_audit_logs(log_dir)
    if not counter:
        print("未找到审计日志，请先运行 `lh 掀黑箱` 生成日志")
        sys.exit(1)

    suggestions = generate_suggestions(counter, args.top)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(suggestions, encoding="utf-8")

    print(f"✅ 白名单建议已生成: {{output_file}}")
    print(f"  共提取 {{sum(counter.values())}} 条记录，{{len(counter)}} 个唯一项")

if __name__ == "__main__":
    main()
"""

# ============================================================
# 核心部署逻辑
# ============================================================

def generate_dna(prefix: str = "CI部署") -> str:
    """生成 DNA"""
    now = datetime.now()
    return f"#龍芯⚡️{now.strftime('%Y%m%d%H%M%S')}-{prefix}-UID9622"

def build_whitelist_env_str() -> str:
    """构建白名单环境变量字符串（逗号分隔的非注释行）"""
    items = []
    for w in INITIAL_WHITELIST:
        w = w.strip()
        if w and not w.startswith("#"):
            items.append(w)
    return ",".join(items)


def deploy_github_actions(repo_path: Path, whitelist_str: str, fail_level: str) -> bool:
    """部署 GitHub Actions"""
    workflow_dir = repo_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_file = workflow_dir / "audit.yml"

    content = GITHUB_ACTIONS_TEMPLATE.format(
        timestamp=datetime.now().isoformat(),
        dna=generate_dna("GitHubActions"),
        fail_level=fail_level,
        whitelist_env=whitelist_str,
    )

    workflow_file.write_text(content, encoding="utf-8")
    print(f"✅ GitHub Actions 已部署: {workflow_file}")
    return True


def deploy_gitlab_ci(repo_path: Path, whitelist_str: str, fail_level: str) -> bool:
    """部署 GitLab CI"""
    ci_file = repo_path / ".gitlab-ci.yml"
    # 如果文件已存在，检查是否已有审计配置
    if ci_file.exists():
        existing = ci_file.read_text(encoding="utf-8")
        if "掀黑箱审计" in existing:
            print(f"ℹ️  GitLab CI 已存在审计配置，跳过: {ci_file}")
            return True

    content = GITLAB_CI_TEMPLATE.format(
        timestamp=datetime.now().isoformat(),
        dna=generate_dna("GitLabCI"),
        fail_level=fail_level,
        whitelist_env=whitelist_str,
    )

    # 追加到现有文件
    if ci_file.exists():
        with open(ci_file, "a", encoding="utf-8") as f:
            f.write("\n\n" + content)
    else:
        ci_file.write_text(content, encoding="utf-8")

    print(f"✅ GitLab CI 已部署: {ci_file}")
    return True


def deploy_whitelist(repo_path: Path) -> bool:
    """部署初始白名单"""
    whitelist_file = repo_path / ".audit-whitelist"
    if whitelist_file.exists():
        print(f"ℹ️  白名单文件已存在，跳过: {whitelist_file}")
        return True

    whitelist_file.write_text("\n".join(INITIAL_WHITELIST) + "\n", encoding="utf-8")
    print(f"✅ 白名单已部署: {whitelist_file}")
    return True


def deploy_feedback_script(repo_path: Path) -> bool:
    """部署白名单反馈收集脚本"""
    scripts_dir = repo_path / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    script_file = scripts_dir / "collect_whitelist_feedback.py"

    now = datetime.now()
    content = FEEDBACK_SCRIPT_TEMPLATE.format(
        YEAR=now.strftime("%Y"),
        MONTH=now.strftime("%m"),
        DAY=now.strftime("%d"),
        HOUR=now.strftime("%H"),
        MINUTE=now.strftime("%M"),
    )

    script_file.write_text(content, encoding="utf-8")
    script_file.chmod(0o755)
    print(f"✅ 白名单反馈脚本已部署: {script_file}")
    return True


def deploy_audit_engine_check(repo_path: Path) -> bool:
    """确保掀黑箱引擎和 CI 集成器存在"""
    engine = repo_path / "bin" / "lh_掀黑箱.py"
    ci_integration = repo_path / "bin" / "lh_ci_audit.py"

    ok = True
    if not engine.exists():
        print(f"⚠️  掀黑箱引擎不存在: {engine}")
        print("   请先部署引擎到 bin/ 目录")
        ok = False

    if not ci_integration.exists():
        print(f"⚠️  CI 集成器不存在: {ci_integration}")
        print("   请先部署 CI 集成器到 bin/ 目录")
        ok = False

    if ok:
        print(f"✅ 审计引擎检查通过")
    return ok


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龙魂 · CI 审计自动化部署器")
    parser.add_argument("--repo", type=Path, default=TARGET_REPO, help="目标仓库路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入")
    parser.add_argument("--fail-level", default="critical",
                        choices=["critical", "high", "medium", "low"],
                        help="CI 阻断阈值")
    parser.add_argument("--whitelist-extra", default="", help="额外白名单条目（逗号分隔）")
    args = parser.parse_args()

    repo_path = args.repo.expanduser().resolve()
    if not repo_path.exists():
        print(f"❌ 仓库路径不存在: {repo_path}")
        sys.exit(1)

    print(f"🐉 龙魂 · CI 审计部署器")
    print(f"  目标仓库: {repo_path}")
    print(f"  阻断阈值: {args.fail_level}")
    print(f"  模式: {'预览' if args.dry_run else '实际部署'}")
    print()

    if args.dry_run:
        print("[预览模式] 将执行以下操作:")
        print("  - 创建 .github/workflows/audit.yml")
        print("  - 创建/追加 .gitlab-ci.yml")
        print("  - 创建 .audit-whitelist")
        print("  - 创建 scripts/collect_whitelist_feedback.py")
        print("  - 检查 bin/lh_掀黑箱.py 和 bin/lh_ci_audit.py")
        # 也显示白名单内容预览
        print("\n📋 初始白名单预览:")
        for line in INITIAL_WHITELIST:
            if line.strip() and not line.startswith("#"):
                print(f"    - {line}")
        return

    # 1. 检查引擎
    if not deploy_audit_engine_check(repo_path):
        print("\n❌ 前置条件不满足，部署中止")
        sys.exit(1)

    # 2. 构建白名单
    whitelist_str = build_whitelist_env_str()
    if args.whitelist_extra:
        whitelist_str += "," + args.whitelist_extra

    # 3. 部署 GitHub Actions
    deploy_github_actions(repo_path, whitelist_str, args.fail_level)

    # 4. 部署 GitLab CI
    deploy_gitlab_ci(repo_path, whitelist_str, args.fail_level)

    # 5. 部署白名单
    deploy_whitelist(repo_path)

    # 6. 部署反馈收集脚本
    deploy_feedback_script(repo_path)

    # 已启用的扫描范围
    enabled_scopes = [k for k, v in SCAN_SCOPES.items() if v["enabled"]]

    print("\n✅ 部署完成")
    print("\n📌 后续步骤:")
    print("  1. 检查生成的 CI 配置文件，确认无误后提交")
    print("  2. 触发一个 PR 测试审计流程")
    print("  3. 运行 scripts/collect_whitelist_feedback.py 收集高频误报")
    print("  4. 将高频误报加入 .audit-whitelist")
    print(f"\n📂 扫描范围已扩展到: {', '.join(enabled_scopes)}")


if __name__ == "__main__":
    main()
