#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·自动对齐闭环调度器 v2.0
DNA: 由 bin/lh_dna_generator.py 生成（禁止手写时间戳格式）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：自动执行 检测→路由→修复→验证→归档→通知 闭环
全部在鲲鹏本地运行，不调用云端。

v2.0 修复清单：
  1. 新增文件锁，防止 cron 并发重入
  2. subprocess 全部加超时，检查器卡死不再拖死闭环
  3. classify_issues 补全 large_files / unused_imports（路由表不再是死代码）
  4. 修复报告统计中 duplicates 类型不一致（dict/list 兼容）
  5. 新增 --dry-run 干跑模式：只检测+给建议，不动任何文件
  6. 归档摘要健壮化，缺字段不再 KeyError
  7. 退出码规范化：0=通过 1=错误 2=仍有未修复项（方便 cron 监控）
"""

import argparse
import fcntl
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------- 配置 ----------
BASE_DIR = Path.home() / "longhun-system"
REPORT_DIR = BASE_DIR / "reports"
FIX_LOG_DIR = BASE_DIR / "logs" / "fixes"
ARCHIVE_DIR = BASE_DIR / "archive"          # 归档目录（P0：不删除只冻结）
LOCK_FILE = BASE_DIR / "logs" / ".align_daemon.lock"

CHECKER_TIMEOUT = 600     # 检查器最长运行 10 分钟
FIX_TIMEOUT = 300         # 单个修复脚本最长 5 分钟
MAX_FIX_ROUNDS = 3        # 修复-验证最多迭代 3 轮，防止死循环

for d in (REPORT_DIR, FIX_LOG_DIR, ARCHIVE_DIR, LOCK_FILE.parent):
    d.mkdir(parents=True, exist_ok=True)

# 人格路由规则（谁负责修复什么类型的问题）
PERSONA_ROUTING = {
    "duplicate_functions": "鲁班",      # 合并重复函数
    "similar_functions": "鲁班",         # 抽象相似函数
    "missing_dna": "司马迁",             # 补DNA签章
    "missing_confirm": "司马迁",         # 补确认码
    "large_files": "诸葛亮",             # 拆分大文件
    "unused_imports": "通心译",          # 清理无用导入
}

# 终端通知颜色
RED, GREEN, YELLOW, CYAN = '\033[91m', '\033[92m', '\033[93m', '\033[96m'
RESET, BOLD = '\033[0m', '\033[1m'


# ---------- 工具 ----------
def notify(message: str, level: str = "info") -> None:
    """终端彩色通知 + 写日志"""
    colors = {"info": CYAN, "success": GREEN, "warning": YELLOW, "error": RED}
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    color = colors.get(level, RESET)
    icon = icons.get(level, "📌")
    print(f"{color}{icon} {message}{RESET}")

    log_path = FIX_LOG_DIR / f"notifications_{datetime.now():%Y%m%d}.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] [{level}] {message}\n")


def run_script(path: Path, args: Optional[List[str]] = None,
               timeout: int = FIX_TIMEOUT) -> subprocess.CompletedProcess:
    """统一子进程调用：带超时、带异常兜底"""
    cmd = [sys.executable, str(path)] + (args or [])
    try:
        return subprocess.run(cmd, cwd=BASE_DIR, capture_output=True,
                              text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124,
                                           stdout="", stderr=f"超时({timeout}s)")


# ---------- 第一步：检测 ----------
def run_checker() -> Dict[str, Any]:
    """运行对齐检查器，返回报告 dict"""
    print(f"{CYAN}🔍 [检测] 运行对齐检查器...{RESET}")

    checker_path = BASE_DIR / "bin" / "lh_align_checker.py"
    if not checker_path.exists():
        return {"status": "error", "message": f"检查器不存在: {checker_path}"}

    result = run_script(checker_path, ["--no-print"], timeout=CHECKER_TIMEOUT)
    if result.returncode != 0:
        return {"status": "error",
                "message": f"检查器执行失败(rc={result.returncode}): {result.stderr[:300]}"}

    # 优先从 stdout 解析 JSON
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue

    # 兜底：读最新报告文件
    report_files = sorted(REPORT_DIR.glob("align_*.json"), reverse=True)
    if report_files:
        try:
            with open(report_files[0], "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            return {"status": "error", "message": f"报告文件损坏: {e}"}

    return {"status": "error", "message": "无法获取报告"}


# ---------- 第二步：分类 + 路由 ----------
def _as_list(value: Any) -> List:
    """报告字段兼容：dict 取 values 摊平，list 直接用，None 给空"""
    if value is None:
        return []
    if isinstance(value, dict):
        out: List = []
        for v in value.values():
            out.extend(v if isinstance(v, list) else [v])
        return out
    return value if isinstance(value, list) else [value]


def classify_issues(report: Dict) -> List[Dict]:
    """将报告中的问题分类，标记应由哪个人格处理"""
    issues: List[Dict] = []

    mapping = [
        ("duplicates",      "duplicate_functions", "high",   "组重复函数"),
        ("similar_pairs",   "similar_functions",   "medium", "对相似函数"),
        ("missing_dna",     "missing_dna",         "high",   "个文件缺失DNA"),
        ("missing_confirm", "missing_confirm",     "high",   "个文件缺失确认码"),
        ("large_files",     "large_files",         "medium", "个超大文件待拆分"),
        ("unused_imports",  "unused_imports",      "low",    "处无用导入"),
    ]
    for key, issue_type, severity, unit in mapping:
        items = _as_list(report.get(key))
        if items:
            issues.append({
                "type": issue_type,
                "severity": severity,
                "persona": PERSONA_ROUTING[issue_type],
                "data": items,
                "message": f"发现 {len(items)} {unit}",
            })
    return issues


# ---------- 第三步：修复 ----------
def generate_fix_suggestion(issue: Dict) -> str:
    suggestions = {
        "duplicate_functions": "建议合并同名函数，保留实现最完整的一个，或加前缀区分模块",
        "similar_functions": "建议抽象公共逻辑为独立函数，各调用处替换",
        "missing_dna": "自动补DNA：调用 bin/lh_dna_generator.py 生成干支+卦名格式（禁止手写）",
        "missing_confirm": "自动补确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "large_files": "建议按职能拆分为多个模块，单文件控制在 500 行内",
        "unused_imports": "建议删除未使用的 import（可用 autoflake 辅助）",
    }
    return suggestions.get(issue["type"], "建议人工复核该问题")


def fix_issue(issue: Dict, dry_run: bool = False) -> Dict:
    """调用对应修复脚本；dry-run 只给建议不动文件"""
    if dry_run:
        return {"status": "dry-run",
                "message": f"[干跑] 不执行修复: {issue['message']}",
                "suggestion": generate_fix_suggestion(issue)}

    fix_script = BASE_DIR / "bin" / f"lh_fix_{issue['type']}.py"
    if fix_script.exists():
        print(f"{CYAN}🔧 [修复] 调用 {fix_script.name} ...{RESET}")
        # 把待修复文件列表通过参数传给修复脚本
        file_args = [str(x) for x in issue["data"] if isinstance(x, str)][:200]
        result = run_script(fix_script, file_args)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "message": result.stdout[:300],
            "error": result.stderr[:300] if result.stderr else None,
        }

    return {"status": "suggested",
            "message": f"无专用修复脚本，转建议: {issue['message']}",
            "suggestion": generate_fix_suggestion(issue)}


# ---------- 第四步：验证 ----------
def verify_fix() -> Dict:
    print(f"{CYAN}🔍 [验证] 重新运行检查器...{RESET}")
    report = run_checker()
    if report.get("status") == "error":
        return {"status": "error", "message": f"验证失败: {report.get('message')}"}
    issues = classify_issues(report)
    if issues:
        return {"status": "incomplete",
                "message": f"仍有 {len(issues)} 类问题未修复",
                "remaining": issues}
    return {"status": "passed", "message": "所有问题已修复，对齐通过"}


# ---------- 第五步：归档 ----------
def archive_run(run_id: str, report: Dict, actions: List[Dict], result: Dict) -> Path:
    archive = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "report_summary": {
            "total_files": report.get("total_files", 0),
            "total_functions": report.get("total_functions", 0),
            "duplicates": len(_as_list(report.get("duplicates"))),
            "missing_dna": len(_as_list(report.get("missing_dna"))),
            "missing_confirm": len(_as_list(report.get("missing_confirm"))),
            "large_files": len(_as_list(report.get("large_files"))),
            "unused_imports": len(_as_list(report.get("unused_imports"))),
        },
        "actions": actions,
        "result": result,
    }
    archive_path = ARCHIVE_DIR / f"archive_{run_id}.json"
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)
    return archive_path


# ---------- 主调度器 ----------
def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂·自动对齐闭环调度器 v2.0")
    parser.add_argument("--dry-run", action="store_true",
                        help="干跑模式：只检测+给建议，不修改任何文件")
    args = parser.parse_args()

    # 文件锁：防 cron 并发重入
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"{YELLOW}⚠️ 上一个闭环还在运行，本次跳过{RESET}")
        return 0

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_tag = " [干跑模式]" if args.dry_run else ""
    notify(f"🐉 龍魂自动对齐闭环启动{mode_tag} (ID: {run_id})", "info")

    # ① 检测
    report = run_checker()
    if report.get("status") == "error":
        notify(f"检测失败: {report.get('message')}", "error")
        return 1

    issues = classify_issues(report)
    if not issues:
        notify("🎉 所有文件对齐良好，无需修复！", "success")
        archive_run(run_id, report, [], {"status": "passed"})
        return 0

    notify(f"发现 {len(issues)} 类问题，开始分配人格处理", "info")

    # ② 路由 + ③ 修复 + ④ 验证（最多迭代 MAX_FIX_ROUNDS 轮）
    actions: List[Dict] = []
    verify_result: Dict = {"status": "incomplete", "remaining": issues}
    for round_no in range(1, MAX_FIX_ROUNDS + 1):
        for issue in issues:
            persona = issue["persona"]
            notify(f"📤 [第{round_no}轮] 分配 {persona} 处理: {issue['message']}", "info")
            result = fix_issue(issue, dry_run=args.dry_run)
            actions.append({"round": round_no, "issue_type": issue["type"],
                            "persona": persona, "result": result})
            if result["status"] == "success":
                notify(f"✅ {persona} 修复完成", "success")
            elif result["status"] == "dry-run":
                notify(f"🔎 {persona} 干跑建议已生成", "info")
            else:
                notify(f"🟡 {persona} 需要人工介入: {result.get('message', '')}", "warning")

        if args.dry_run:
            verify_result = {"status": "dry-run", "message": "干跑模式跳过验证"}
            break

        verify_result = verify_fix()
        if verify_result["status"] != "incomplete":
            break
        issues = verify_result.get("remaining", [])
        if round_no < MAX_FIX_ROUNDS:
            notify(f"🔁 第{round_no}轮后仍有遗留，进入第{round_no + 1}轮", "info")

    # ⑤ 归档
    archive_path = archive_run(run_id, report, actions, verify_result)

    # ⑥ 最终通知
    status = verify_result.get("status", "error")
    if status == "passed":
        notify("🎉 修复验证通过！闭环完成。", "success")
    elif status == "dry-run":
        notify("🔎 干跑完成：建议已生成，未改动任何文件。", "info")
    else:
        notify(f"🟡 闭环未完全通过: {verify_result.get('message', '')}", "warning")

    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{CYAN}📊 闭环总结{RESET}")
    print(f"  运行ID:   {run_id}")
    print(f"  修复动作: {len(actions)} 次")
    print(f"  验证状态: {status}")
    print(f"  归档路径: {archive_path}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    return {"passed": 0, "dry-run": 0}.get(status, 2)


if __name__ == "__main__":
    sys.exit(main())
