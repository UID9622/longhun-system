#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·统一对齐入口 v1.0（道生一·一生二·二生三·三生万物）
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ALIGN-UNIFIED-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

哲学架构：
  道生一  → lh align（统一入口）
  一生二  → check（审计）/ fix（修复）
  二生三  → check / fix / status（三大主操作）
  三生万物 → 背后是对齐检查器·DNA修复·确认码修复·归档·人格路由

设计原则：
  - 不重复造轮子，每次调已有脚本
  - 先查缓存（最新报告），避免重复计算
  - 蚁群分布式：各脚本独立运行，统一入口只做路由和缓存

用法：
  lh align              → 等同于 lh align check（检查）
  lh align check        → 扫描对齐问题（不修改）
  lh align fix          → 自动修复（检测→修复→验证→归档闭环）
  lh align dry-run      → 干跑（只检测+给建议，不动文件）
  lh align status       → 查看最新对齐状态
  lh align history [N]  → 查看最近N次归档记录
  lh align clean-old    → 清理30天前的归档（压缩摘要·删除原始JSON）
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 配置 ──
BASE_DIR = Path.home() / "longhun-system"
BIN_DIR = BASE_DIR / "bin"
ARCHIVE_DIR = BASE_DIR / "archive"
REPORT_DIR = BASE_DIR / "reports"
STATE_FILE = BASE_DIR / "STATE.md"

CHECKER = BIN_DIR / "lh_align_checker.py"
DAEMON = BIN_DIR / "lh_auto_align_daemon.py"

RED, GREEN, YELLOW, CYAN, RESET, BOLD = '\033[91m', '\033[92m', '\033[93m', '\033[96m', '\033[0m', '\033[1m'


# ═══════════════════════════════════════════════════
#  道生一：统一入口
# ═══════════════════════════════════════════════════

def run_command(cmd: List[str], timeout: int = 300) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=BASE_DIR, capture_output=True,
                              text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, returncode=124,
                                           stdout="", stderr=f"超时({timeout}s)")

def latest_report() -> Optional[Dict]:
    """读最新对齐报告（缓存优先）"""
    reports = sorted(REPORT_DIR.glob("align_*.json"), reverse=True)
    if reports:
        with open(reports[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def latest_archive() -> Optional[Dict]:
    """读最新归档"""
    archives = sorted(ARCHIVE_DIR.glob("archive_*.json"), reverse=True)
    if archives:
        with open(archives[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


# ═══════════════════════════════════════════════════
#  一生二：check + fix
# ═══════════════════════════════════════════════════

def cmd_check():
    """检查对齐（只用缓存·不重复扫描）"""
    report = latest_report()
    if report and report.get('total_files'):
        age = datetime.now() - datetime.fromisoformat(report.get('generated_at', '2000-01-01'))
        freshness = "新鲜" if age < timedelta(hours=1) else f"({age.seconds // 60}分钟前)"
        print(f"{CYAN}📋 对齐报告（缓存·{freshness}）{RESET}")
        _print_summary(report)
        print(f"\n{GREEN}💡 需要重新扫描？运行 lh align check --refresh{RESET}")
        return

    # 无缓存或强制刷新，跑检查器
    print(f"{CYAN}🔍 运行对齐检查器...{RESET}")
    result = run_command([sys.executable, str(CHECKER), "--json"], timeout=600)
    if result.returncode != 0:
        print(f"{RED}❌ 检查器失败: {result.stderr[:200]}{RESET}")
        return

    stdout = result.stdout.strip()
    json_start = stdout.find("{")
    if json_start >= 0:
        try:
            report = json.loads(stdout[json_start:])
            # 保存到 reports 目录，让 status/history/daemon 都能读到缓存
            REPORT_DIR.mkdir(parents=True, exist_ok=True)
            report_path = REPORT_DIR / f"align_{datetime.now():%Y%m%d_%H%M%S}.json"
            report_copy = {k: v for k, v in report.items() if k != "all_items"}
            report_copy["timestamp"] = datetime.now().isoformat()
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_copy, f, ensure_ascii=False, indent=2, default=str)
            print(f"{GREEN}💾 报告已缓存: {report_path.name}{RESET}")
            _print_summary(report)
            return
        except json.JSONDecodeError:
            pass
    print(f"{RED}❌ 无法解析报告{RESET}")
    if stdout:
        print(stdout[:500])

def _print_summary(report: Dict):
    """打印对齐报告摘要"""
    total = report.get('total_files', 0)
    funcs = report.get('total_functions', 0)

    def count(key):
        v = report.get(key)
        if v is None: return 0
        if isinstance(v, dict):
            # duplicates 的 key 是函数名，value 是出现该函数的文件列表
            # 报告应显示"多少组同名函数"，而非文件出现次数
            return len(v)
        if isinstance(v, list): return len(v)
        return 0

    dup = count('duplicates')
    sim = count('similar_pairs')
    no_dna = count('missing_dna')
    no_cfm = count('missing_confirm')
    big = count('large_files')
    unused = count('unused_imports')

    print(f"  {BOLD}文件: {total}  |  函数: {funcs}{RESET}")
    problems = []
    if dup: problems.append(f"{RED}{dup}组重复{RESET}")
    if sim: problems.append(f"{YELLOW}{sim}对相似{RESET}")
    if no_dna: problems.append(f"{RED}{no_dna}缺DNA{RESET}")
    if no_cfm: problems.append(f"{YELLOW}{no_cfm}缺确认码{RESET}")
    if big: problems.append(f"{YELLOW}{big}大文件{RESET}")
    if unused: problems.append(f"{YELLOW}{unused}无用导入{RESET}")

    if problems:
        print(f"  ⚠️ 问题: {', '.join(problems)}")
    else:
        print(f"  {GREEN}✅ 全部对齐{RESET}")

def cmd_fix(dry_run: bool = False):
    """执行修复闭环"""
    args = [sys.executable, str(DAEMON)]
    if dry_run:
        args.append("--dry-run")
    result = run_command(args, timeout=1800)
    print(result.stdout)
    if result.stderr:
        print(f"{RED}{result.stderr[:500]}{RESET}", file=sys.stderr)
    return result.returncode

def cmd_status():
    """查看最新对齐状态"""
    archive = latest_archive()
    report = latest_report()

    print(f"{BOLD}{'=' * 50}{RESET}")
    print(f"{CYAN}🐉 龍魂对齐状态{RESET}")

    if archive:
        rid = archive.get('run_id', '?')
        ts = archive.get('timestamp', '?')
        rst = archive.get('result', {}).get('status', '?')
        color = GREEN if rst == 'passed' else YELLOW
        print(f"  最后闭环: {color}{rid}{RESET} ({ts[:19]})")
        print(f"  验证状态: {color}{rst}{RESET}")

        summary = archive.get('report_summary', {})
        if summary:
            print(f"  {BOLD}报告摘要:{RESET}")
            for k, v in summary.items():
                if k in ('total_files', 'total_functions'): continue
                if v > 0:
                    print(f"    {k}: {RED if v > 0 else GREEN}{v}{RESET}")
    elif report:
        _print_summary(report)
    else:
        print(f"{YELLOW}  无对齐记录，运行 lh align check 首次检查{RESET}")

    print(f"{BOLD}{'=' * 50}{RESET}")

def cmd_history(n: int = 10):
    """查看历史归档"""
    archives = sorted(ARCHIVE_DIR.glob("archive_*.json"), reverse=True)[:n]
    if not archives:
        print(f"{YELLOW}无归档记录{RESET}")
        return

    print(f"{BOLD}{'=' * 70}{RESET}")
    print(f"{CYAN}📦 最近 {len(archives)} 次对齐归档{RESET}")
    print(f"{'时间':<20} {'ID':<20} {'状态':<12} {'说明'}")
    print("-" * 70)
    for a in archives:
        try:
            with open(a, 'r') as f:
                data = json.load(f)
            ts = data.get('timestamp', '?')[:19]
            rid = data.get('run_id', a.stem)
            status = data.get('result', {}).get('status', '?')
            summary = data.get('report_summary', {})
            desc_parts = []
            if summary.get('duplicates'): desc_parts.append(f"D:{summary['duplicates']}")
            if summary.get('missing_dna'): desc_parts.append(f"DNA:{summary['missing_dna']}")
            if summary.get('missing_confirm'): desc_parts.append(f"CFM:{summary['missing_confirm']}")
            desc = ' '.join(desc_parts) if desc_parts else '-'
            color = GREEN if status == 'passed' else YELLOW
            print(f"{ts}  {rid:<20} {color}{status:<12}{RESET} {desc}")
        except Exception:
            print(f"{'-':<20} {a.stem:<20} {'error':<12}")
    print(f"{BOLD}{'=' * 70}{RESET}")

def cmd_clean_old(days: int = 30):
    """清理旧归档（压缩摘要·不删数据）"""
    cutoff = datetime.now() - timedelta(days=days)
    archives = sorted(ARCHIVE_DIR.glob("archive_*.json"))

    old_count = 0
    summary = []
    for a in archives:
        try:
            with open(a, 'r') as f:
                data = json.load(f)
            ts = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
            if ts < cutoff:
                summary.append({
                    'run_id': data.get('run_id', a.stem),
                    'timestamp': data['timestamp'],
                    'status': data.get('result', {}).get('status', '?'),
                    'summary': data.get('report_summary', {}),
                    'actions_count': len(data.get('actions', [])),
                })
                old_count += 1
        except Exception:
            continue

    if old_count == 0:
        print(f"{GREEN}✅ 无超过{days}天的归档需要清理{RESET}")
        return

    # 写压缩摘要
    summary_path = ARCHIVE_DIR / f"alignment_history_{datetime.now():%Y%m%d}.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({'compressed_at': datetime.now().isoformat(),
                   'original_count': old_count,
                   'entries': summary}, f, ensure_ascii=False, indent=2)

    print(f"{GREEN}✅ 压缩 {old_count} 条归档 → {summary_path.name}{RESET}")
    print(f"{YELLOW}💡 原始归档文件保留在 archive/ 目录（P0：不删除只冻结）{RESET}")


# ═══════════════════════════════════════════════════
#  独立模式：python3 lh_align.py <目录> [--json]
#  用于 Git 钩子 / CI / 外部调用
# ═══════════════════════════════════════════════════

def standalone_scan(directory: str, json_output: bool = False) -> int:
    """独立扫描模式：直接跑检查器，返回退出码。
    退出码: 0=🟢全绿, 1=🟡仅有警告, 2=🔴有红线"""
    import shutil

    checker = Path(directory) / "bin" / "lh_align_checker.py"
    if not checker.exists():
        checker = BIN_DIR / "lh_align_checker.py"
    if not checker.exists():
        print(f"{RED}❌ 找不到 lh_align_checker.py{RESET}", file=sys.stderr)
        return 2

    dir_path = Path(directory).resolve()
    if not dir_path.is_dir():
        print(f"{RED}❌ 目录不存在: {directory}{RESET}", file=sys.stderr)
        return 2

    print(f"{CYAN}🔍 龍魂对齐扫描: {dir_path}{RESET}")
    result = run_command([sys.executable, str(checker), "--json"], timeout=600)

    if result.returncode != 0:
        # 检查器本身失败
        stderr = result.stderr[:500] if result.stderr else "未知错误"
        print(f"{RED}❌ 检查器执行失败 (exit={result.returncode}): {stderr}{RESET}")
        return 2

    stdout = result.stdout.strip()
    json_start = stdout.find("{")
    if json_start < 0:
        print(f"{RED}❌ 无法解析报告{RESET}")
        if stdout:
            print(stdout[:1000])
        return 2

    try:
        report = json.loads(stdout[json_start:])
    except json.JSONDecodeError as e:
        print(f"{RED}❌ JSON解析失败: {e}{RESET}")
        return 2

    # --- 评分 ---
    total = report.get('total_files', 0)
    funcs = report.get('total_functions', 0)

    def count(key):
        v = report.get(key)
        if v is None: return 0
        if isinstance(v, dict):
            # duplicates 的 key 是函数名，value 是出现该函数的文件列表
            # 报告应显示"多少组同名函数"，而非文件出现次数
            return len(v)
        if isinstance(v, list): return len(v)
        return 0

    dup = count('duplicates')
    sim = count('similar_pairs')
    no_dna = count('missing_dna')
    no_cfm = count('missing_confirm')

    # 🔴 红线检查
    red_items = []
    if no_dna > 0: red_items.append(f"{no_dna}个文件缺DNA")
    if dup > 100: red_items.append(f"{dup}组重复(>100阈值)")

    # 🟡 警告检查
    yellow_items = []
    if dup > 0 and dup <= 100: yellow_items.append(f"{dup}组重复")
    if sim > 0: yellow_items.append(f"{sim}对相似")
    if no_cfm > 0: yellow_items.append(f"{no_cfm}缺确认码")

    exit_code = 0
    overall = "🟢"

    if red_items:
        exit_code = 2
        overall = "🔴"
    elif yellow_items:
        exit_code = 1
        overall = "🟡"

    if json_output:
        result_json = {
            "overall": overall,
            "exit_code": exit_code,
            "total_files": total,
            "total_functions": funcs,
            "red": red_items,
            "yellow": yellow_items,
        }
        print(json.dumps(result_json, ensure_ascii=False, indent=2))
    else:
        print(f"\n  {BOLD}文件: {total}  |  函数: {funcs}{RESET}")
        if red_items:
            for r in red_items:
                print(f"  {RED}🔴 {r}{RESET}")
        if yellow_items:
            for y in yellow_items:
                print(f"  {YELLOW}🟡 {y}{RESET}")
        if not red_items and not yellow_items:
            print(f"  {GREEN}✅ 全部对齐{RESET}")
        print(f"\n  {BOLD}总体: {overall}  退出码: {exit_code}{RESET}")

    return exit_code


# ═══════════════════════════════════════════════════
#  三生万物：主入口
# ═══════════════════════════════════════════════════

def main():
    # ── 独立模式检测：第一个位置参数是目录路径（非子命令）──
    standalone_args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if standalone_args:
        first = standalone_args[0]
        if not first.startswith('-') and Path(first).exists():
            json_mode = '--json' in sys.argv
            sys.exit(standalone_scan(first, json_output=json_mode))

    parser = argparse.ArgumentParser(
        description="🐉 龍魂·统一对齐入口（道生一·一生二·二生三·三生万物）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh align                  检查对齐（查缓存，不重复扫描）
  lh align check --refresh  强制重新扫描
  lh align fix              自动修复闭环
  lh align dry-run          干跑（不动文件）
  lh align status           查看最新对齐状态
  lh align history          最近10次归档
  lh align clean-old        压缩30天前的归档

独立模式（用于 Git 钩子/CI）:
  python3 lh_align.py .          扫描当前目录·退出码 0/1/2
  python3 lh_align.py . --json   扫描·JSON输出
        """)
    sub = parser.add_subparsers(dest='command', help='子命令')

    p_check = sub.add_parser('check', help='检查对齐')
    p_check.add_argument('--refresh', action='store_true', help='强制重新扫描（不用缓存）')

    sub.add_parser('fix', help='自动修复闭环（检测→修复→验证→归档）')
    sub.add_parser('dry-run', help='干跑：只检测建议，不修改')
    sub.add_parser('status', help='查看最新对齐状态')
    p_hist = sub.add_parser('history', help='历史归档')
    p_hist.add_argument('-n', type=int, default=10, help='显示条数（默认10）')
    p_clean = sub.add_parser('clean-old', help='清理旧归档')
    p_clean.add_argument('-d', '--days', type=int, default=30, help='保留天数（默认30）')

    args = parser.parse_args()

    if args.command == 'check' and args.refresh:
        # 强制刷新：删除缓存报告（P0兼容：归档不删）
        for r in REPORT_DIR.glob("align_*.json"):
            r.unlink(missing_ok=True)
        print(f"{YELLOW}🔄 缓存已清除，重新扫描...{RESET}")

    cmd_map = {
        'check': cmd_check,
        'fix': cmd_fix,
        'dry-run': lambda: cmd_fix(dry_run=True),
        'status': cmd_status,
        'history': lambda: cmd_history(n=getattr(args, 'n', 10)),
        'clean-old': lambda: cmd_clean_old(days=getattr(args, 'days', 30)),
    }

    if args.command in cmd_map:
        cmd_map[args.command]()
    else:
        # 默认：检查（缓存优先）
        cmd_check()


if __name__ == "__main__":
    sys.exit(main() or 0)
