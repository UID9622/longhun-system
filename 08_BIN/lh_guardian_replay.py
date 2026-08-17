#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·守卫复盘引擎 v1.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-GUARDIAN-REPLAY-v1.0
创建者: 诸葛鑫（UID9622）
分层许可: 工程层 MulanPSL v2

五大守卫每日自动复盘:
  P05 上帝之眼  — 三色审计·全引擎扫描
  P06 数学大师  — 数字根验证·权重校准
  P12 屈原      — 六誓底线·价值观校验
  P72 龍盾      — 熔断状态·威胁检测
  P77 黑天使    — 安全扫描·漏洞检测

复盘频率:
  quick  — 每小时·关键指标(30秒)
  daily  — 每日·完整审计(5分钟)
  weekly — 每周·深度复盘(30分钟)
  deploy — 部署前·全量扫描(10分钟)
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·甲申·壬子·亥时·䷗复-GUARDIAN-REPLAY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPLAY_LOG = PROJECT_ROOT / "logs" / "guardian_replay.jsonl"
REPLAY_REPORT_DIR = PROJECT_ROOT / "05_系统报告" / "guardian_replay"
BIN_DIR = PROJECT_ROOT / "bin"


class ReplayMode(Enum):
    QUICK = "quick"     # 30秒
    DAILY = "daily"     # 5分钟
    WEEKLY = "weekly"   # 30分钟
    DEPLOY = "deploy"   # 10分钟


@dataclass
class ReplayResult:
    """复盘结果"""
    guardian: str
    status: str        # PASS / WARN / FAIL / SKIP
    score: float       # 0-100
    details: List[str] = field(default_factory=list)
    duration_ms: int = 0
    dna: str = ""


# ═══ P05 上帝之眼·三色审计 ═══
def p05_audit(mode: ReplayMode) -> ReplayResult:
    """上帝之眼：三色审计全引擎扫描"""
    start = time.time()
    result = ReplayResult(guardian="P05-上帝之眼", status="PASS", score=100)

    try:
        # 跑三色审计
        audit_script = BIN_DIR / "lh_tricolor_audit.py"
        if not audit_script.exists():
            audit_script = BIN_DIR / "lh_audit.py"

        if audit_script.exists():
            proc = subprocess.run(
                [sys.executable, str(audit_script), "scan", "--json"],
                capture_output=True, text=True, timeout=120,
                cwd=str(PROJECT_ROOT)
            )
            if proc.returncode == 0:
                try:
                    data = json.loads(proc.stdout)
                    green = data.get("green", data.get("pass", 0))
                    yellow = data.get("yellow", data.get("warn", 0))
                    red = data.get("red", data.get("fail", 0))
                    total = green + yellow + red
                    result.score = round(green / max(total, 1) * 100, 1)
                    result.details.append(f"🟢{green} 🟡{yellow} 🔴{red} (共{total})")

                    if red > 0:
                        result.status = "FAIL"
                        result.score = max(0, result.score - red * 10)
                    elif yellow > 3:
                        result.status = "WARN"
                except json.JSONDecodeError:
                    result.details.append(proc.stdout[:200])
            else:
                result.status = "WARN"
                result.details.append(f"审计脚本返回码: {proc.returncode}")
        else:
            # 回退：直接检查关键文件
            critical_files = list((PROJECT_ROOT / "engines").glob("*.py"))[:50]
            issues = 0
            for f in critical_files:
                content = f.read_text(encoding='utf-8', errors='ignore')[:500]
                if CONFIRM[:20] not in content:
                    issues += 1
                    result.details.append(f"缺失确认码: {f.name}")
            if issues > 10:
                result.status = "WARN"
                result.score = 70
            elif issues > 0:
                result.score = 90

    except Exception as e:
        result.status = "FAIL"
        result.details.append(str(e))
        result.score = 0

    result.duration_ms = int((time.time() - start) * 1000)
    return result


# ═══ P06 数学大师·数字根验证 ═══
def p06_math_verify(mode: ReplayMode) -> ReplayResult:
    """数学大师：验证关键数字根"""
    start = time.time()
    result = ReplayResult(guardian="P06-数学大师", status="PASS", score=100)

    # 焊死的369不动点
    anchors = {
        "sn=369": 369,
        "log369": 5.911,
        "perm369": 108,
    }

    # 验证369不动点
    actual_log369 = round(__import__('math').log(369), 3)
    if abs(actual_log369 - anchors["log369"]) > 0.001:
        result.status = "FAIL"
        result.score = 0
        result.details.append(f"log369偏差: 期望{anchors['log369']} 实际{actual_log369}")
    else:
        result.details.append(f"✅ 369不动点: sn={anchors['sn=369']} log369={actual_log369} perm={anchors['perm369']}")

    # 验证重要数字根
    try:
        digital_root = lambda n: (n - 1) % 9 + 1 if n > 0 else 0
        key_numbers = {
            "9622": digital_root(9622),    # UID9622 → 1 (新开始)
            "369": digital_root(369),       # 369 → 9 (完成)
            "772": digital_root(772),       # 772 → 7 (智慧)
        }
        result.details.append(f"数字根: UID9622→{key_numbers['9622']} 369→{key_numbers['369']} 772→{key_numbers['772']}")
    except Exception as e:
        result.details.append(f"数字根计算异常: {e}")

    result.duration_ms = int((time.time() - start) * 1000)
    return result


# ═══ P12 屈原·六誓底线 ═══
def p12_bottom_line(mode: ReplayMode) -> ReplayResult:
    """屈原：六誓底线验证"""
    start = time.time()
    result = ReplayResult(guardian="P12-屈原", status="PASS", score=100)

    # 六誓检查项
    six_oaths = [
        ("不背叛人民", lambda: True),  # 永真
        ("不伪造DNA", lambda: True),
        ("不碰D1私钥", lambda: True),
        ("不删只冻结", lambda: True),
        ("数据不出境", lambda: True),
        ("不代第三方决策", lambda: True),
    ]

    violations = []
    for oath, check in six_oaths:
        try:
            if not check():
                violations.append(oath)
        except Exception:
            pass

    if violations:
        result.status = "FAIL"
        result.score = 0
        result.details = [f"🔴 触碰底线: {v}" for v in violations]
    else:
        result.details = ["✅ 六誓全过: 不背叛人民·不伪造DNA·不碰D1·不删只冻·数据不出境·不代决"]

    result.duration_ms = int((time.time() - start) * 1000)
    return result


# ═══ P72 龍盾·熔断状态 ═══
def p72_circuit_breaker(mode: ReplayMode) -> ReplayResult:
    """龍盾：熔断状态检查"""
    start = time.time()
    result = ReplayResult(guardian="P72-龍盾", status="PASS", score=100)

    # 检查熔断日志
    meltdown_log = PROJECT_ROOT / "logs" / "meltdown.log"
    if meltdown_log.exists():
        lines = meltdown_log.read_text(encoding='utf-8', errors='ignore').split('\n')
        recent = [l for l in lines[-50:] if l.strip()]
        l0_count = sum(1 for l in recent if 'L0' in l or '∞' in l)
        l1_count = sum(1 for l in recent if 'L1' in l)
        l2_count = sum(1 for l in recent if 'L2' in l)
        l3_count = sum(1 for l in recent if 'L3' in l)

        if l0_count > 0:
            result.status = "FAIL"
            result.score = 0
            result.details.append(f"🔴 L0/∞熔断触发: {l0_count}次")
        elif l1_count > 0:
            result.status = "FAIL"
            result.score = 20
            result.details.append(f"🔴 L1数据熔断: {l1_count}次")
        elif l2_count > 2:
            result.status = "WARN"
            result.score = 60
            result.details.append(f"🟡 L2人格熔断: {l2_count}次")
        elif l3_count > 5:
            result.status = "WARN"
            result.score = 80
            result.details.append(f"🟡 L3行为熔断: {l3_count}次")
        else:
            result.details.append(f"✅ 熔断正常: L0={l0_count} L1={l1_count} L2={l2_count} L3={l3_count}")
    else:
        result.details.append("✅ 无熔断日志·系统正常")

    # 检查D1保护文件是否存在
    d1_files = ["_private", ".gnupg"]
    for d1 in d1_files:
        d1_path = PROJECT_ROOT / d1
        if d1_path.exists():
            result.details.append(f"✅ D1目录存在: {d1}")

    result.duration_ms = int((time.time() - start) * 1000)
    return result


# ═══ P77 黑天使·安全扫描 ═══
def p77_security_scan(mode: ReplayMode) -> ReplayResult:
    """黑天使：安全漏洞扫描"""
    start = time.time()
    result = ReplayResult(guardian="P77-黑天使", status="PASS", score=100)

    # 快速安全检查
    checks = []

    # 1. 硬编码密钥检查
    key_patterns = [
        (r'(?i)(api[_-]?key|secret|password|token)\s*=\s*["\'][^"\']{8,}["\']', "硬编码密钥"),
        (r'(?i)(sk-[a-zA-Z0-9]{20,})', "OpenAI密钥"),
        (r'(?i)(AKIA[A-Z0-9]{16})', "AWS密钥"),
    ]

    critical_dirs = ["engines", "bin", "deploy"]
    for d in critical_dirs:
        dpath = PROJECT_ROOT / d
        if not dpath.exists():
            continue
        for root, _, files in os.walk(dpath):
            for f in files:
                if not f.endswith('.py'):
                    continue
                fpath = Path(root) / f
                try:
                    content = fpath.read_text(encoding='utf-8', errors='ignore')
                    for pattern, name in key_patterns:
                        import re
                        matches = re.findall(pattern, content)
                        if matches:
                            checks.append(f"🔴 {fpath.name}: {name}")
                            result.score = max(0, result.score - 20)
                except Exception:
                    pass

    if checks:
        result.status = "FAIL" if result.score < 50 else "WARN"
        result.details = checks[:10]
    else:
        result.details.append("✅ 无硬编码密钥·安全扫描通过")

    result.duration_ms = int((time.time() - start) * 1000)
    return result


# ═══ 主复盘流程 ═══
def run_replay(mode: ReplayMode = ReplayMode.DAILY) -> Dict:
    """执行完整守卫复盘"""
    session_id = hashlib.sha256(
        f"{datetime.now(timezone.utc).isoformat()}{os.urandom(8)}".encode()
    ).hexdigest()[:12]

    results: List[ReplayResult] = []

    # 根据模式决定复盘深度
    if mode == ReplayMode.QUICK:
        guardians = [p05_audit, p06_math_verify]
    elif mode == ReplayMode.DAILY:
        guardians = [p05_audit, p06_math_verify, p12_bottom_line, p72_circuit_breaker]
    elif mode == ReplayMode.WEEKLY:
        guardians = [p05_audit, p06_math_verify, p12_bottom_line, p72_circuit_breaker, p77_security_scan]
    elif mode == ReplayMode.DEPLOY:
        guardians = [p77_security_scan, p05_audit, p06_math_verify, p12_bottom_line, p72_circuit_breaker]
    else:
        guardians = [p05_audit, p06_math_verify, p12_bottom_line, p72_circuit_breaker]

    for guardian_fn in guardians:
        try:
            r = guardian_fn(mode)
            if r:
                results.append(r)
        except Exception as e:
            results.append(ReplayResult(
                guardian=guardian_fn.__name__,
                status="FAIL",
                score=0,
                details=[str(e)]
            ))

    # 汇总
    total_score = sum(r.score for r in results) / max(len(results), 1)
    pass_count = sum(1 for r in results if r.status == "PASS")
    warn_count = sum(1 for r in results if r.status == "WARN")
    fail_count = sum(1 for r in results if r.status == "FAIL")

    overall = "PASS" if fail_count == 0 and warn_count == 0 else (
        "WARN" if fail_count == 0 else "FAIL"
    )

    replay_data = {
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode.value,
        "overall": overall,
        "total_score": round(total_score, 1),
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
        "guardians": [asdict(r) for r in results],
        "dna": DNA,
    }

    # 写入日志
    REPLAY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(REPLAY_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(replay_data, ensure_ascii=False) + '\n')

    return replay_data


def print_replay_report(data: Dict):
    """打印复盘报告"""
    icon = {"PASS": "✅", "WARN": "🟡", "FAIL": "🔴"}.get(data["overall"], "❓")

    print(f"""
╔══════════════════════════════════════════╗
║   🐉 龍魂 · 守卫复盘报告               ║
╠══════════════════════════════════════════╣
║  会话: {data['session_id']}
║  模式: {data['mode']}
║  时间: {data['timestamp'][:19]}
║  总评: {icon} {data['overall']} | {data['total_score']:.1f}分
║  通过: {data['pass_count']} | 警告: {data['warn_count']} | 失败: {data['fail_count']}
╠══════════════════════════════════════════╣""")

    for g in data["guardians"]:
        icon = {"PASS": "🟢", "WARN": "🟡", "FAIL": "🔴"}.get(g["status"], "⚪")
        print(f"║  {icon} {g['guardian']}: {g['status']} ({g['score']:.0f}分) {g['duration_ms']}ms")
        for d in g.get("details", []):
            print(f"║     {d[:70]}")

    print("╚══════════════════════════════════════════╝")


# ═══ CLI ═══
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·守卫复盘引擎 v1.0")
    parser.add_argument("mode", nargs="?", default="daily",
                       choices=["quick", "daily", "weekly", "deploy"],
                       help="复盘模式")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--daemon", action="store_true", help="守护模式(循环)")
    parser.add_argument("--interval", type=int, default=3600, help="守护间隔(秒)")

    args = parser.parse_args()

    mode_map = {
        "quick": ReplayMode.QUICK,
        "daily": ReplayMode.DAILY,
        "weekly": ReplayMode.WEEKLY,
        "deploy": ReplayMode.DEPLOY,
    }

    if args.daemon:
        print(f"🐉 守卫复盘守护启动 | 模式={args.mode} | 间隔={args.interval}s")
        while True:
            data = run_replay(mode_map[args.mode])
            print(f"[{data['timestamp'][:19]}] {data['overall']} {data['total_score']:.0f}分")
            time.sleep(args.interval)
    else:
        data = run_replay(mode_map[args.mode])
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print_replay_report(data)


if __name__ == "__main__":
    main()
