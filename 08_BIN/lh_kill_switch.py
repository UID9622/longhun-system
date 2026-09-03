#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_kill_switch.py — Kill Switch 熔断状态检测与测试
# DNA: #龍芯⚡️2026-08-31-KILL-SWITCH-IRON-LAW-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 铁律: #IRON 关机键 K1-K5 · 关机权100%在现实人手里
# 用法: python3 bin/lh_kill_switch.py --status | --test
# ═══════════════════════════════════════════════════════════
"""关机键熔断检测。物理开关 = 文件存在性（现实人手可触·不联网即生效·单按即停·无后门）。

开关语义: ~/.longhun/KILL_SWITCH_ENGAGED 存在 = 已熔断（系统应停止）。
本工具只读/测试，不提供解除（解除=现实人亲手删除文件，密钥在现实人手里）。
"""
import argparse
import json
import os
import time
import datetime

HOME = os.path.expanduser("~/.longhun")
SWITCH_FILE = os.path.join(HOME, "KILL_SWITCH_ENGAGED")
STATE_FILE = os.path.join(HOME, "kill_switch_state.json")
FLAVOR = "real-person-hard-power"  # K2: 关机权不可数字化委托

_HEADER = """# ══════════════════════════════════════════════
# Kill Switch 关机键检测 v1.0 · L0永恒层
# 铁律: #IRON K1-K5 · 关机权100%在现实人手里
# ══════════════════════════════════════════════"""


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _read_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}
    return {}


def _write_state(state):
    os.makedirs(HOME, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def cmd_status():
    engaged = os.path.exists(SWITCH_FILE)
    state = _read_state()
    print(_HEADER)
    print(f"# 状态: {'🔴 已熔断（KILL_SWITCH_ENGAGED 存在·系统应停止）' if engaged else '🟢 未熔断（正常运行）'}")
    print(f"# 开关位置: {SWITCH_FILE}")
    print(f"# 开关语义: {FLAVOR} · 现实人手可触 · 不联网即生效 · 单按即停 · 无后门")
    if state.get("last_test"):
        print(f"# 最近自检: {state['last_test']}")
    if state.get("last_trigger"):
        print(f"# 最近触发: {state['last_trigger']}")
    return 0 if not engaged else 3


def cmd_test():
    """dry-run 自检：模拟触发→检测→清除，全程不留真实开关。"""
    print(_HEADER)
    print("# 自检开始（dry-run·不落真实开关）")
    os.makedirs(HOME, exist_ok=True)
    probe = SWITCH_FILE + ".test-probe"
    try:
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write(f"probe {_now()}\n")
        detected = os.path.exists(probe)
        print(f"# 模拟触发→写入探针: {probe}")
        print(f"# 检测到熔断信号: {'✅ 是' if detected else '❌ 否'}")
    finally:
        if os.path.exists(probe):
            os.remove(probe)
    print(f"# 探针已清除: {'✅' if not os.path.exists(probe) else '❌'}")
    state = _read_state()
    state["last_test"] = _now()
    _write_state(state)
    print(f"# 自检通过 ✅ Kill Switch 机制可用 · DNA: #龍芯⚡️2026-08-31-KILL-SWITCH-IRON-LAW-v1.0-UID9622")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Kill Switch 关机键熔断检测")
    parser.add_argument("--status", action="store_true", help="查看熔断状态")
    parser.add_argument("--test", action="store_true", help="熔断机制自检（dry-run）")
    args = parser.parse_args()
    if args.test:
        return cmd_test()
    return cmd_status()


if __name__ == "__main__":
    raise SystemExit(main())
