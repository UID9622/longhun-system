#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-ANTI-BLOWOUT-GUARD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂反熔断守卫 · LongHun Anti-Blowout Guard v1.0

把任意操作包装成：
  1. 过载检查
  2. 执行操作
  3. 输出契约校验
  4. 审计日志记录

用法:
    python3 anti_blowout_guard.py --op autostart -- python3 ../bin/longhun-autostart.sh
    python3 anti_blowout_guard.py --op daily_review --evidence '{"artifact":"daily_review.py"}' -- python3 ../daily_review.py
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Import local modules
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "persona"))
from overload_guard import 龍魂过载守护
from output_contract import 龍魂输出契约
from audit_logger import 龍魂审计日志器


class 龍魂反熔断守卫:
    DNA = "#龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-LONGHUN-ANTI-BLOWOUT-GUARD-v1.0"

    def __init__(self):
        self.overload = 龍魂过载守护()
        self.contract = 龍魂输出契约()
        self.audit = 龍魂审计日志器()

    def 执行(
        self,
        op: str,
        cmd: List[str],
        evidence: Dict[str, Any] = None,
        expected_stats: List[str] = None,
        queue_depth: int = 0,
    ) -> Dict[str, Any]:
        start = time.time()
        result = {
            "op": op,
            "allowed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "",
            "contract_valid": False,
            "blocked_reasons": [],
            "audit_id": None,
        }

        # 1. 过载检查
        status = self.overload.请求检查(queue_depth)
        if not status.get("allowed"):
            result["blocked_reasons"].append(status.get("error", {}))
            self._审计(op, "failed", evidence, {"duration_ms": int((time.time() - start) * 1000)}, "SERVER_OVERLOADED")
            return result

        result["overload_status"] = status

        # 2. 执行命令
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )
            result["exit_code"] = proc.returncode
            result["stdout"] = proc.stdout
            result["stderr"] = proc.stderr
        except Exception as e:
            result["stderr"] = str(e)
            result["exit_code"] = -1

        duration_ms = int((time.time() - start) * 1000)

        # 3. 输出契约校验
        status_str = "success" if result["exit_code"] == 0 else "failed"
        stats = {"duration_ms": duration_ms, "exit_code": result["exit_code"]}

        # 如果命令输出包含完成声明但未通过契约，则拦截
        output_text = result["stdout"] + "\n" + result["stderr"]
        contract_result = self.contract.验证(op, status_str, evidence, stats, output_text)
        result["contract_valid"] = contract_result["valid"]
        result["contract_blocked"] = contract_result["blocked"]
        result["contract_violations"] = contract_result.get("violations", [])

        if contract_result["blocked"]:
            result["blocked_reasons"].extend(contract_result["violations"])
            status_str = "failed"

        # 4. 记录审计日志
        error_code = None if result["exit_code"] == 0 else f"EXIT_{result['exit_code']}"
        if result["contract_blocked"]:
            error_code = "OUTPUT_CONTRACT_VIOLATION"
        record = self._审计(op, status_str, evidence, stats, error_code)
        result["audit_id"] = record.get("id")

        return result

    def _审计(self, op, status, evidence, stats, error_code):
        return self.audit.记录(
            op=op,
            status=status,
            evidence=evidence or {},
            stats=stats,
            error_code=error_code,
            user_id=os.environ.get("USER", "system"),
        )


def main():
    parser = argparse.ArgumentParser(description="龍魂反熔断守卫")
    parser.add_argument("--op", required=True, help="操作类型")
    parser.add_argument("--evidence", default="{}", help="JSON evidence")
    parser.add_argument("--queue-depth", type=int, default=0)
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="要执行的命令（前面加 --）")
    args = parser.parse_args()

    if not args.cmd:
        print("用法: python3 anti_blowout_guard.py --op NAME -- command args...")
        sys.exit(1)

    if args.cmd[0] == "--":
        args.cmd = args.cmd[1:]

    ev = json.loads(args.evidence)
    guard = 龍魂反熔断守卫()
    result = guard.执行(args.op, args.cmd, evidence=ev, queue_depth=args.queue_depth)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"🛡️  反熔断守卫执行结果")
        print(f"   操作: {result['op']}")
        print(f"   退出码: {result['exit_code']}")
        print(f"   契约通过: {result['contract_valid']}")
        print(f"   审计ID: {result['audit_id']}")
        if result["blocked_reasons"]:
            print(f"   拦截原因: {result['blocked_reasons']}")
        if result["stdout"]:
            print("--- stdout ---")
            print(result["stdout"])
        if result["stderr"]:
            print("--- stderr ---")
            print(result["stderr"])

    sys.exit(0 if result["exit_code"] == 0 and not result.get("contract_blocked") else 1)


if __name__ == "__main__":
    main()
