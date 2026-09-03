#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-EXTERNAL-CALLS-LOG-V1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
📜 龍魂外部调用记录查看 v1.0 — lh logs [--tail 100] [--json]

数据源: ~/.longhun/logs/external_calls.log（网关 lh_api 归一回流自动写入·只记非本机）
过滤规则: 127.0.0.1 本机调用不记录（审计外部调用·防剽窃溯源）
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

EXTERNAL_LOG = Path.home() / ".longhun" / "logs" / "external_calls.log"


def load_records(tail: int) -> list[dict]:
    if not EXTERNAL_LOG.exists():
        return []
    records: list[dict] = []
    try:
        with EXTERNAL_LOG.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError as e:
        return [{"error": str(e)}]
    return records[-tail:] if tail > 0 else records


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh logs", description="外部调用记录·归一审计")
    ap.add_argument("--tail", type=int, default=20, help="显示最近 N 条 (默认 20)")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--all", action="store_true", help="全部记录（忽略 --tail）")
    args = ap.parse_args()

    tail = -1 if args.all else args.tail
    records = load_records(tail)

    if args.json:
        print(json.dumps({
            "status": "ok",
            "log": str(EXTERNAL_LOG),
            "count": len(records),
            "records": records,
        }, ensure_ascii=False, indent=2))
        return 0

    if not records:
        print("📜 暂无外部调用记录")
        print("  说明: 网关默认只监听 127.0.0.1（本机调用不记录·节能）")
        print("  要审计外部调用: lh api --host 0.0.0.0 对外开放后自动写入")
        return 0

    print(f"📜 外部调用记录 ({len(records)} 条 · {EXTERNAL_LOG})")
    print("-" * 96)
    print(f"{'时间':<26} {'IP':<16} {'耗时':>5} {'审计':<2} {'code':>4}  命令")
    print("-" * 96)
    for r in reversed(records):
        t = str(r.get("time", "?"))[:19]
        ip = str(r.get("ip", "?"))[:15]
        ms = r.get("ms")
        ms_s = f"{ms}ms" if ms is not None else "-"
        audit = r.get("audit", "-") or "-"
        code = r.get("code", "?")
        cmd = str(r.get("command", ""))[:70]
        print(f"{t:<26} {ip:<16} {ms_s:>5} {audit:<2} {code:>4}  {cmd}")
    print("-" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
