#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CI 流水线审计集成器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-CI审计-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 自动检测 CI 环境（GitHub Actions、GitLab CI、Gitee、本地）
  - 获取 PR 变更文件列表（增量扫描）或全量扫描
  - 调用掀黑箱引擎进行审计
  - 根据风险级别决定 CI 是否失败（严重/高危 → 阻断）
  - 支持白名单配置（环境变量或 .audit-whitelist 文件）

使用方式（CI 配置）：
  # GitHub Actions
  - name: 审计 PR
    run: python3 bin/lh_ci_audit.py

  # 本地测试
  python3 bin/lh_ci_audit.py --pr 123 --target ./my-project

环境变量：
  CI_AUDIT_FAIL_LEVEL: critical|high|medium|low (默认 critical)
  CI_AUDIT_WHITELIST: 逗号分隔的域名或路径（白名单）
  CI_AUDIT_SCOPE: all|changed (默认 changed，仅扫描变更文件)
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
ENGINE_SCRIPT = PROJECT_ROOT / "bin" / "lh_掀黑箱.py"
CI_AUDIT_FAIL_LEVEL = os.environ.get("CI_AUDIT_FAIL_LEVEL", "critical")
CI_AUDIT_WHITELIST = os.environ.get("CI_AUDIT_WHITELIST", "")
CI_AUDIT_SCOPE = os.environ.get("CI_AUDIT_SCOPE", "changed")

# 风险等级顺序
RISK_ORDER = ["critical", "high", "medium", "low", "info"]
RISK_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
    "info": "ℹ️",
}

# ============================================================
# CI 环境检测
# ============================================================

def detect_ci_environment() -> Dict[str, Any]:
    """检测当前 CI 环境并返回上下文信息"""
    env = {
        "is_ci": False,
        "provider": "local",
        "pr_number": None,
        "target_branch": None,
        "source_branch": None,
        "repo_path": Path.cwd(),
    }

    # GitHub Actions
    if os.environ.get("GITHUB_ACTIONS") == "true":
        env["is_ci"] = True
        env["provider"] = "github"
        env["pr_number"] = os.environ.get("PR_NUMBER") or os.environ.get("GITHUB_REF_NAME")
        env["target_branch"] = os.environ.get("GITHUB_BASE_REF")
        env["source_branch"] = os.environ.get("GITHUB_HEAD_REF")
        env["repo_path"] = Path(os.environ.get("GITHUB_WORKSPACE", "."))

    # GitLab CI
    elif os.environ.get("GITLAB_CI") == "true":
        env["is_ci"] = True
        env["provider"] = "gitlab"
        env["pr_number"] = os.environ.get("CI_MERGE_REQUEST_IID") or os.environ.get("CI_COMMIT_REF_NAME")
        env["target_branch"] = os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
        env["source_branch"] = os.environ.get("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
        env["repo_path"] = Path(os.environ.get("CI_PROJECT_DIR", "."))

    # Gitee
    elif os.environ.get("GITEE_CI") == "true":
        env["is_ci"] = True
        env["provider"] = "gitee"
        env["pr_number"] = os.environ.get("GITEE_PR_ID")
        env["target_branch"] = os.environ.get("GITEE_TARGET_BRANCH")
        env["source_branch"] = os.environ.get("GITEE_SOURCE_BRANCH")
        env["repo_path"] = Path(os.environ.get("GITEE_WORKSPACE", "."))

    # 本地测试（手动指定）
    else:
        env["is_ci"] = False

    return env

# ============================================================
# 获取变更文件
# ============================================================

def get_changed_files(ci_env: Dict[str, Any]) -> List[str]:
    """获取 PR 中变更的文件列表（相对于仓库根目录）"""
    repo_path = ci_env["repo_path"]

    # 如果是 CI 环境且有 PR 信息，尝试用 git 获取
    if ci_env["is_ci"] and ci_env.get("pr_number"):
        # 尝试获取 target 分支（通常是 main/master）与当前分支的差异
        target_branch = ci_env.get("target_branch", "main")
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "diff", "--name-only", f"origin/{target_branch}..."],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
                return files
        except Exception:
            pass

    # 回退：没有变更信息，扫描整个项目（全量）
    print("⚠️ 无法获取变更文件列表，执行全量扫描")
    return []

# ============================================================
# 审计引擎调用
# ============================================================

def run_audit(target_path: Path, files: Optional[List[str]] = None) -> Dict[str, Any]:
    """调用掀黑箱引擎进行审计，返回 JSON 结果"""
    if not ENGINE_SCRIPT.exists():
        print(f"❌ 审计引擎不存在: {ENGINE_SCRIPT}")
        sys.exit(1)

    cmd = ["python3", str(ENGINE_SCRIPT), str(target_path), "--json"]

    # 如果指定了文件列表，通过 stdin 传递（引擎需支持）
    # 暂时不支持文件列表，使用全量扫描
    # 未来可优化为增量

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            check=False,
        )
        if result.returncode != 0:
            print(f"⚠️ 审计引擎返回非零退出码: {result.returncode}")
            print(result.stderr[:500])
            return {"error": result.stderr[:500], "findings": []}

        # 解析 JSON
        # 引擎输出可能包含额外的终端信息，我们需要提取 JSON 部分
        output = result.stdout
        # 查找 JSON 开始位置
        try:
            idx = output.index("{")
            json_str = output[idx:]
            data = json.loads(json_str)
            return data
        except (ValueError, json.JSONDecodeError) as e:
            print(f"❌ 解析 JSON 失败: {e}")
            print(output[:500])
            return {"error": str(e), "findings": []}
    except subprocess.TimeoutExpired:
        print("❌ 审计超时")
        return {"error": "timeout", "findings": []}
    except Exception as e:
        print(f"❌ 运行审计失败: {e}")
        return {"error": str(e), "findings": []}

# ============================================================
# 白名单过滤
# ============================================================

def load_whitelist() -> Set[str]:
    """从环境变量或配置文件加载白名单"""
    whitelist = set()

    # 环境变量
    if CI_AUDIT_WHITELIST:
        for item in CI_AUDIT_WHITELIST.split(","):
            whitelist.add(item.strip())

    # 配置文件：项目根目录下的 .audit-whitelist
    whitelist_file = Path.cwd() / ".audit-whitelist"
    if whitelist_file.exists():
        with open(whitelist_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    whitelist.add(line)

    return whitelist

def is_whitelisted(evidence: str, whitelist: Set[str]) -> bool:
    """检查证据是否命中白名单"""
    evidence_lower = evidence.lower()
    for item in whitelist:
        if item.lower() in evidence_lower:
            return True
    return False

# ============================================================
# 风险评估与决策
# ============================================================

def evaluate_risk(findings: List[Dict], fail_level: str, whitelist: Set[str]) -> Dict[str, Any]:
    """评估风险并决定是否阻断 CI"""
    # 按严重级别分组
    grouped = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": [],
        "info": [],
    }

    for f in findings:
        severity = f.get("severity", "info")
        # 映射严重级别字符串到 key
        sev_key = severity.lower()
        if "严重" in severity:
            sev_key = "critical"
        elif "高危" in severity:
            sev_key = "high"
        elif "中危" in severity:
            sev_key = "medium"
        elif "低危" in severity:
            sev_key = "low"
        else:
            sev_key = "info"

        # 应用白名单
        evidence = f.get("evidence", "")
        if is_whitelisted(evidence, whitelist):
            sev_key = "info"  # 降级为信息
            f_copy = dict(f)
            f_copy["severity"] = "ℹ️ 信息（白名单）"
            grouped["info"].append(f_copy)
        else:
            grouped[sev_key].append(f)

    # 确定最高风险级别
    highest = "info"
    for level in RISK_ORDER:
        if grouped.get(level):
            highest = level
            break

    # 判断是否需要阻断
    fail_level_index = RISK_ORDER.index(fail_level)
    highest_index = RISK_ORDER.index(highest)
    should_fail = highest_index <= fail_level_index

    return {
        "grouped": grouped,
        "highest": highest,
        "should_fail": should_fail,
        "fail_level": fail_level,
    }

# ============================================================
# 报告输出
# ============================================================

def print_ci_report(ci_env: Dict[str, Any], audit_result: Dict[str, Any], risk_eval: Dict[str, Any]):
    """输出 CI 友好的报告（彩色终端）"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    lines = []
    lines.append(f"\n{BOLD}{'='*70}{RESET}")
    lines.append(f"{BOLD}🐉 龙魂 · CI 流水线审计报告{RESET}")
    lines.append(f"{BOLD}{'='*70}{RESET}")

    # CI 上下文
    lines.append(f"  提供商: {ci_env['provider']}")
    if ci_env.get('pr_number'):
        lines.append(f"  PR: #{ci_env['pr_number']}")
    lines.append(f"  路径: {ci_env['repo_path']}")
    lines.append(f"  时间: {datetime.now().isoformat()}")

    # 审计摘要
    total_findings = len(audit_result.get("findings", []))
    if "error" in audit_result:
        lines.append(f"\n❌ 审计执行失败: {audit_result['error']}")
        lines.append(f"{BOLD}{'='*70}{RESET}")
        print("\n".join(lines))
        return

    lines.append(f"\n📊 审计摘要")
    g = risk_eval["grouped"]
    lines.append(f"  🔴 严重: {len(g['critical'])}")
    lines.append(f"  🟠 高危: {len(g['high'])}")
    lines.append(f"  🟡 中危: {len(g['medium'])}")
    lines.append(f"  🟢 低危: {len(g['low'])}")
    lines.append(f"  ℹ️ 信息: {len(g['info'])}")

    # 最高风险
    highest = risk_eval["highest"]
    emoji = RISK_EMOJI.get(highest, "ℹ️")
    if highest == "critical":
        color = RED
    elif highest == "high":
        color = YELLOW
    else:
        color = GREEN
    lines.append(f"\n  最高风险: {color}{emoji} {highest.upper()}{RESET}")
    lines.append(f"  阻断级别: {risk_eval['fail_level']}")

    # 决策
    if risk_eval["should_fail"]:
        lines.append(f"\n{RED}❌ 审计失败：存在 {highest.upper()} 级别风险，PR 将被阻断{RESET}")
    else:
        lines.append(f"\n{GREEN}✅ 审计通过：风险级别低于阻断阈值{RESET}")

    # 详细发现（仅展示前5条）
    if total_findings > 0:
        lines.append(f"\n{BOLD}🔍 发现详情（前5条）{RESET}")
        for i, f in enumerate(audit_result["findings"][:5], 1):
            sev = f.get("severity", "info")
            rule = f.get("rule", "未知")
            desc = f.get("description", "")
            evidence = f.get("evidence", "")
            lines.append(f"  {i}. {sev} {rule}")
            lines.append(f"     {desc}")
            lines.append(f"     📎 {evidence[:80]}{'...' if len(evidence) > 80 else ''}")
        if total_findings > 5:
            lines.append(f"  ... 还有 {total_findings - 5} 条")

    lines.append(f"{BOLD}{'='*70}{RESET}")
    print("\n".join(lines))

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龙魂 · CI 流水线审计集成器")
    parser.add_argument("--target", default=".", help="要审计的目标路径")
    parser.add_argument("--pr", type=int, help="PR 编号（手动指定）")
    parser.add_argument("--fail-level", default=CI_AUDIT_FAIL_LEVEL,
                        choices=RISK_ORDER, help="阻断阈值")
    parser.add_argument("--whitelist", default=CI_AUDIT_WHITELIST,
                        help="白名单（逗号分隔）")
    parser.add_argument("--scope", default=CI_AUDIT_SCOPE,
                        choices=["all", "changed"], help="审计范围")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")
    args = parser.parse_args()

    # 检测 CI 环境
    ci_env = detect_ci_environment()
    if args.pr:
        ci_env["pr_number"] = args.pr
    if args.target != ".":
        ci_env["repo_path"] = Path(args.target).resolve()

    # 白名单
    whitelist = load_whitelist()
    if args.whitelist:
        for item in args.whitelist.split(","):
            whitelist.add(item.strip())

    # 获取变更文件（如果使用增量模式）
    changed_files = []
    if args.scope == "changed" and ci_env["is_ci"]:
        changed_files = get_changed_files(ci_env)

    # 确定扫描路径
    target_path = ci_env["repo_path"]
    if not target_path.exists():
        print(f"❌ 目标路径不存在: {target_path}")
        sys.exit(1)

    # 执行审计
    print(f"🔍 开始审计: {target_path}")
    if changed_files:
        print(f"  增量模式: {len(changed_files)} 个变更文件")
    else:
        print(f"  全量模式")

    audit_result = run_audit(target_path, changed_files if changed_files else None)

    # 评估风险
    fail_level = args.fail_level
    risk_eval = evaluate_risk(audit_result.get("findings", []), fail_level, whitelist)

    # 输出报告
    print_ci_report(ci_env, audit_result, risk_eval)

    # 返回退出码
    sys.exit(1 if risk_eval["should_fail"] else 0)

if __name__ == "__main__":
    main()
