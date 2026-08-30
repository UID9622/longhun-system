#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 功能: 龍魂 AI 助手三通道统一熔断闸门 v1.0（P72 龍盾·三通道共用）
# DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·䷳艮-CHANNEL-GATE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 上位: 01_protocols/LH-AI-ASSISTANT-CHANNELS-v1.0.md §2
"""
龍魂 AI 助手三通道统一熔断闸门 v1.0

P0 网站 / P1 公众号 / P2 GitHub 机器人 三通道共用一把闸门。
任一通道异常 → 熔断该通道，其余通道照常（分层熔断，降级矩阵 L3 行为级）。

状态机: CLOSED →(连续失败≥阈值)→ OPEN →(冷却到期)→ HALF_OPEN →(探测成功)→ CLOSED
参数:   失败阈值 3 · 冷却窗口 300s · 半开探测 1 次
持久化: _work/channel_gate_state.json（含审计链）

用法:
  lh_channel_gate.py status                # 查看三通道闸门状态
  lh_channel_gate.py check P0             # 检查 P0 是否可放行（CLOSED/HALF_OPEN→放行）
  lh_channel_gate.py fail P0 <原因>       # 记录一次失败（连续失败达阈值→OPEN）
  lh_channel_gate.py success P0           # 记录一次成功（HALF_OPEN 下 1 次即恢复）
  lh_channel_gate.py reset P0             # 人工重置该通道（L2+ 需审计）
  lh_channel_gate.py json P0              # 输出该通道状态 JSON（供引擎内嵌调用）
"""

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "_work" / "channel_gate_state.json"

CHANNELS = {
    "P0": {"name": "自有网站 AI 对话", "fail_threshold": 3, "cooldown": 300, "probe_success": 1},
    "P1": {"name": "微信公众号 AI 助手", "fail_threshold": 3, "cooldown": 300, "probe_success": 1},
    "P2": {"name": "GitHub 开源机器人", "fail_threshold": 3, "cooldown": 300, "probe_success": 1},
}


def _default_state():
    return {c: {"state": "CLOSED", "fail_count": 0, "open_at": 0,
                "half_open_at": 0, "last_event": "", "history": []}
            for c in CHANNELS}


def load_state():
    if STATE_FILE.exists():
        try:
            d = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            # 补齐缺失通道
            for c in CHANNELS:
                d.setdefault(c, _default_state()[c])
            return d
        except Exception:
            pass
    return _default_state()


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _audit(state, ch, evt, reason=""):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "channel": ch, "event": evt,
           "reason": reason, "state": state[ch]["state"], "fail_count": state[ch]["fail_count"]}
    state[ch]["history"].append(rec)
    state[ch]["last_event"] = f"{evt} @{rec['ts']}"
    if len(state[ch]["history"]) > 50:      # 审计链限长
        state[ch]["history"] = state[ch]["history"][-50:]


def cmd_check(state, ch):
    """检查通道是否可放行。CLOSED/HALF_OPEN → 放行；OPEN → 拦截"""
    cfg = CHANNELS[ch]
    s = state[ch]
    now = time.time()
    if s["state"] == "OPEN" and now - s["open_at"] >= cfg["cooldown"]:
        s["state"] = "HALF_OPEN"
        s["half_open_at"] = now
        _audit(state, ch, "OPEN→HALF_OPEN", "冷却窗口到期，进入半开探测")
    return s["state"] in ("CLOSED", "HALF_OPEN")


def cmd_fail(state, ch, reason):
    cfg = CHANNELS[ch]
    s = state[ch]
    if s["state"] == "OPEN":
        _audit(state, ch, "FAIL_IGNORED", f"已 OPEN，忽略失败计数: {reason}")
    else:
        s["fail_count"] += 1
        if s["fail_count"] >= cfg["fail_threshold"]:
            s["state"] = "OPEN"
            s["open_at"] = time.time()
            _audit(state, ch, "OPEN", f"连续失败{s['fail_count']}次达阈值: {reason}")
        else:
            _audit(state, ch, "FAIL", f"失败{s['fail_count']}/{cfg['fail_threshold']}: {reason}")
    save_state(state)
    return s["state"]


def cmd_success(state, ch):
    cfg = CHANNELS[ch]
    s = state[ch]
    if s["state"] == "HALF_OPEN":
        s["state"] = "CLOSED"
        s["fail_count"] = 0
        _audit(state, ch, "CLOSED", "半开探测成功，恢复正常")
        save_state(state)
    elif s["state"] == "OPEN":
        _audit(state, ch, "SUCCESS_IN_OPEN", "OPEN 期间的成功不计数")
    else:
        s["fail_count"] = 0
        _audit(state, ch, "SUCCESS", "成功，失败计数清零")
        save_state(state)
    return s["state"]


def cmd_reset(state, ch):
    s = state[ch]
    s["state"] = "CLOSED"
    s["fail_count"] = 0
    s["open_at"] = 0
    s["half_open_at"] = 0
    _audit(state, ch, "RESET", "人工重置（L2+ 操作）")
    save_state(state)
    return s["state"]


def main():
    ap = argparse.ArgumentParser(description="龍魂 AI 助手三通道统一熔断闸门")
    ap.add_argument("action", choices=["status", "check", "fail", "success", "reset", "json"])
    ap.add_argument("channel", nargs="?", default=None)
    ap.add_argument("reason", nargs="*", default=[])
    args = ap.parse_args()

    if args.action == "status":
        state = load_state()
        print("── 龍魂 AI 助手三通道统一熔断闸门 ──")
        for ch, cfg in CHANNELS.items():
            s = state[ch]
            icon = {"CLOSED": "🟢", "OPEN": "🔴", "HALF_OPEN": "🟡"}[s["state"]]
            print(f"  {icon} {ch} {cfg['name']:16} {s['state']:10} 失败{s['fail_count']}/{cfg['fail_threshold']} {s['last_event']}")
        return 0

    if not args.channel or args.channel not in CHANNELS:
        print(f"🔴 需指定通道: {', '.join(CHANNELS)}", file=sys.stderr)
        return 1

    state = load_state()
    ch = args.channel
    reason = " ".join(args.reason)

    if args.action == "check":
        ok = cmd_check(state, ch)
        save_state(state)
        print(f"{'🟢' if ok else '🔴'} {ch} {state[ch]['state']} → {'放行' if ok else '熔断拦截(meltdown)'}")
        return 0 if ok else 1
    if args.action == "fail":
        s = cmd_fail(state, ch, reason)
        print(f"🔴 {ch} 状态: {s}")
        return 0
    if args.action == "success":
        s = cmd_success(state, ch)
        print(f"🟢 {ch} 状态: {s}")
        return 0
    if args.action == "reset":
        s = cmd_reset(state, ch)
        print(f"🟢 {ch} 已重置: {s}")
        return 0
    if args.action == "json":
        print(json.dumps(state[ch], ensure_ascii=False))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
