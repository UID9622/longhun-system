#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-BAGUA-SCHEDULER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂八卦决策调度器 · LongHun Bagua Decision Scheduler v1.0
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-BAGUA-SCHEDULER-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

STATE_DIR = Path.home() / ".龍魂" / "state"
STATE_PATH = STATE_DIR / "bagua_state.json"
LOG_PATH = STATE_DIR / "bagua_log.jsonl"
ALERT_OVERRIDE = STATE_DIR / "alert_override"

DEFAULT_STATE = {
    "态势值": 0,
    "当前卦象": "☵ 水洄",
    "熔断": False,
    "上次熔断": None,
    "校验失败次数": 0,
    "丁卯巡逻记录": [],
    "最后更新时间": datetime.now(timezone.utc).isoformat(),
}

# 态势值区间 → 卦象、动作、标签
GUA_TABLE: List[Tuple[int, int, str, str, str]] = [
    (0, 12, "☵ 水洄", "潜藏休养", "系统处于低功耗潜藏态，建议观察、备份、不主动进攻。"),
    (13, 25, "☶ 山止", "警觉校验", "边界出现风吹草动，启动校验与访问控制。"),
    (26, 37, "☳ 雷动", "快速响应", "态势活跃，适合执行短平快任务，注意三色审计。"),
    (38, 50, "☴ 风入", "持续监察", "风无孔不入，进入日志增强、根因追踪模式。"),
    (51, 62, "☲ 火明", "照亮核心", "关键信息浮现，适合公开部署、发布、对外交付。"),
    (63, 75, "☷ 坤载", "稳固承载", "大地厚重，适合归档、扩容、长期计划落地。"),
    (76, 87, "☱ 泽悦", "流通协作", "泽水相通，适合跨平台同步、社区协作、对外联络。"),
    (88, 94, "☰ 天行", "主动裁决", "天道刚健，进入高层决策与独断执行，需留痕。"),
    (95, 100, "☰ 天行·☴ 风入", "熔断裁决", "触发熔断，所有常规卦象冻结，仅天行裁决+风入监察。"),
]

FUSE_THRESHOLD = 95
FAIL_COUNT_LIMIT = 3


def generate_dna(tag: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    h = hashlib.blake2b(f"{ts}-{tag}".encode(), digest_size=8).hexdigest()
    return f"#龍芯⚡️{ts}-{tag}-{h.upper()}"


def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    STATE_PATH.write_text(json.dumps(DEFAULT_STATE, ensure_ascii=False, indent=2), encoding="utf-8")
    return DEFAULT_STATE.copy()


def save_state(state: Dict[str, Any]) -> None:
    state["最后更新时间"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def append_log(record: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_logs(n: int = 12) -> List[Dict[str, Any]]:
    if not LOG_PATH.exists():
        return []
    lines = LOG_PATH.read_text(encoding="utf-8").strip().splitlines()
    records = []
    for line in lines[-n:]:
        try:
            records.append(json.loads(line))
        except Exception:
            continue
    return records


def run_cmd(cmd: List[str], timeout: int = 8) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)


def _count_recent_errors(hours: int = 1) -> int:
    """统计近 N 小时日志中的 ERROR/CRITICAL/FATAL 行数（兜底数据源）。"""
    count = 0
    cutoff = time.time() - hours * 3600
    log_dirs = [
        Path.home() / ".longhun" / "logs",
        Path.home() / ".龍魂" / "automation_logs",
        Path.home() / ".龍魂" / "logs",
        Path.home() / "longhun-system" / "logs",
    ]
    for d in log_dirs:
        if not d.exists():
            continue
        for f in d.glob("*.log"):
            try:
                st = f.stat()
                if st.st_mtime < cutoff:
                    continue
                with f.open("r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        if re.search(r"\b(ERROR|CRITICAL|FATAL|Exception|Traceback)\b", line, re.I):
                            count += 1
            except Exception:
                continue
    return count


def get_lh_index_score() -> Tuple[int, str]:
    """优先调用 lh-index status，失败则统计日志异常。"""
    code, out, err = run_cmd(["lh-index", "status", "--json"])
    if code == 0 and out:
        try:
            data = json.loads(out)
            anomalies = data.get("anomalies", data.get("recent_errors", data.get("error_count", 0)))
            score = min(int(anomalies) * 10, 100)
            return score, f"lh-index status: anomalies={anomalies}"
        except Exception:
            pass
    count = _count_recent_errors(hours=1)
    score = min(count * 10, 100)
    return score, f"日志兜底: 近1小时异常行={count}"


def get_lh_calendar_score() -> Tuple[int, Dict[str, Any], str]:
    """调用 lh-cal --json 获取今日卦象/三色。"""
    code, out, err = run_cmd(["lh-cal", "--json"])
    if code == 0 and out:
        try:
            data = json.loads(out)
            tricolor = data.get("tricolor", {}) or {}
            label = tricolor.get("label", "")
            emoji = tricolor.get("emoji", "")
            gua = data.get("gua", "")
            # 将三色映射为态势辅助分
            label_lower = str(label).lower()
            if "红" in label_lower or "red" in label_lower:
                score = 70
            elif "黄" in label_lower or "yellow" in label_lower or "amber" in label_lower:
                score = 40
            else:
                score = 10
            return score, data, f"lh-cal: gua={gua} tricolor={emoji}{label}"
        except Exception as e:
            return 0, {}, f"lh-cal 解析失败: {e}"
    return 0, {}, f"lh-cal 调用失败: {err.strip()[:80]}"


def get_load_score() -> Tuple[int, str]:
    try:
        load5 = os.getloadavg()[1]
        cores = os.cpu_count() or 1
        score = int((load5 / cores) * 100)
        return min(max(score, 0), 100), f"系统负载: load5={load5:.2f} cores={cores}"
    except Exception as e:
        return 0, f"负载读取失败: {e}"


def get_override_score() -> Tuple[int, str]:
    if not ALERT_OVERRIDE.exists():
        return 0, "alert_override: 无"
    try:
        val = int(ALERT_OVERRIDE.read_text(encoding="utf-8").strip())
        val = min(max(val, 0), 100)
        return val, f"alert_override: {val}"
    except Exception as e:
        return 0, f"alert_override 读取失败: {e}"


def compute_situation() -> Tuple[int, Dict[str, Any]]:
    s1, note1 = get_lh_index_score()
    s2, cal_data, note2 = get_lh_calendar_score()
    s3, note3 = get_load_score()
    s4, note4 = get_override_score()

    score = int(s1 * 0.2 + s2 * 0.1 + s3 * 0.3 + s4 * 0.4)
    score = min(max(score, 0), 100)

    details = {
        "score": score,
        "components": {
            "lh_index": {"score": s1, "weight": 0.2, "note": note1},
            "calendar": {"score": s2, "weight": 0.1, "note": note2, "data": cal_data},
            "load": {"score": s3, "weight": 0.3, "note": note3},
            "override": {"score": s4, "weight": 0.4, "note": note4},
        },
    }
    return score, details


def resolve_gua(score: int) -> Tuple[str, str, str]:
    for lo, hi, name, action, desc in GUA_TABLE:
        if lo <= score <= hi:
            return name, action, desc
    return GUA_TABLE[-1][2], GUA_TABLE[-1][3], GUA_TABLE[-1][4]


def evaluate_and_update(state: Dict[str, Any], manual_score: Optional[int] = None) -> Dict[str, Any]:
    score, details = compute_situation()
    if manual_score is not None:
        score = manual_score
        details["manual"] = True

    name, action, desc = resolve_gua(score)

    fused = state.get("熔断", False)
    fail_count = state.get("校验失败次数", 0)

    if score >= FUSE_THRESHOLD:
        fail_count += 1
    else:
        fail_count = 0

    if fail_count >= FAIL_COUNT_LIMIT:
        fused = True
        name = "☰ 天行独断（☴ 风入监察）"
        action = "熔断裁决"
        desc = "熔断触发：所有常规卦象冻结，仅天行独断+风入监察，手工解除通道：lh-bagua reset。"
        state["上次熔断"] = datetime.now(timezone.utc).isoformat()

    state.update({
        "态势值": score,
        "当前卦象": name,
        "熔断": fused,
        "校验失败次数": fail_count,
        "最后更新时间": datetime.now(timezone.utc).isoformat(),
    })

    # 丁卯巡逻记录（保留最近 30 条）
    patrol = state.get("丁卯巡逻记录", [])
    patrol.append(datetime.now(timezone.utc).isoformat())
    state["丁卯巡逻记录"] = patrol[-30:]

    record = {
        "time": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "gua": name,
        "action": action,
        "desc": desc,
        "details": details,
        "fused": fused,
        "fail_count": fail_count,
        "dna": generate_dna("BAGUA-TRIGGER"),
    }
    append_log(record)
    save_state(state)
    return record


def cmd_status(args) -> int:
    state = load_state()
    print("🐉 龍魂八卦决策调度 · 状态")
    print(f"  态势值:   {state.get('态势值', 0)}")
    print(f"  当前卦象: {state.get('当前卦象', '☵ 水洄')}")
    print(f"  熔断:     {'🔴 已触发' if state.get('熔断') else '🟢 未触发'}")
    print(f"  校验失败: {state.get('校验失败次数', 0)}/{FAIL_COUNT_LIMIT}")
    print(f"  丁卯巡逻: 今日 {len(state.get('丁卯巡逻记录', []))} 次")
    if state.get("上次熔断"):
        print(f"  上次熔断: {state['上次熔断']}")
    print(f"  最后更新: {state.get('最后更新时间', '-')}")
    print(f"  DNA:      {generate_dna('BAGUA-STATUS')}")
    return 0


def cmd_set(args) -> int:
    score = args.value
    state = load_state()
    record = evaluate_and_update(state, manual_score=score)
    print(f"✅ 已手动设定态势值 → {score}")
    print(f"   当前卦象: {record['gua']} · {record['action']}")
    if record["fused"]:
        print("   ⚠️  熔断已触发，请运行 lh-bagua reset 解除")
    return 0


def cmd_trigger(args) -> int:
    state = load_state()
    if state.get("熔断"):
        print("🔒 系统处于熔断状态，仅天行独断有效。")
        print("   如需解除熔断：lh-bagua reset")
        return 1
    record = evaluate_and_update(state)
    print(f"🐉 龍魂八卦态势评估完成")
    print(f"   态势值:   {record['score']}")
    print(f"   当前卦象: {record['gua']}")
    print(f"   建议动作: {record['action']}")
    print(f"   说明:     {record['desc']}")
    print(f"   DNA:      {record['dna']}")
    return 0


def cmd_reset(args) -> int:
    state = load_state()
    was_fused = state.get("熔断", False)
    state["熔断"] = False
    state["校验失败次数"] = 0
    state["态势值"] = 0
    state["当前卦象"] = "☵ 水洄"
    state["最后更新时间"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    append_log({
        "time": datetime.now(timezone.utc).isoformat(),
        "score": 0,
        "gua": "☵ 水洄",
        "action": "熔断解除",
        "desc": "手工重置，解除熔断，恢复潜藏休养态。",
        "was_fused": was_fused,
        "dna": generate_dna("BAGUA-RESET"),
    })
    print("✅ 熔断已解除，系统恢复 ☵ 水洄 潜藏态。")
    return 0


def cmd_log(args) -> int:
    logs = read_logs(n=12)
    if not logs:
        print("暂无调度记录。")
        return 0
    print("🐉 最近调度记录（倒序）")
    for r in reversed(logs):
        t = r.get("time", "")[:19].replace("T", " ")
        print(f"  [{t}] 值={r.get('score'):>3} 卦={r.get('gua')} 动作={r.get('action')} {'🔴熔断' if r.get('fused') else ''}")
    return 0


def cmd_dashboard(args) -> int:
    state = load_state()
    score = state.get("态势值", 0)
    gua = state.get("当前卦象", "☵ 水洄")
    fused = state.get("熔断", False)
    fails = state.get("校验失败次数", 0)
    patrol_count = len(state.get("丁卯巡逻记录", []))

    # 计算下一丁卯时 05:00
    now = datetime.now(timezone.utc)
    next_dingmao = now.replace(hour=5, minute=0, second=0, microsecond=0)
    if next_dingmao <= now:
        next_dingmao = next_dingmao.replace(day=next_dingmao.day + 1)
    next_label = next_dingmao.astimezone().strftime("%m月%d日 %H:%M")

    box = f"""
╔══════════════════════════════════════════╗
║  🐉 龍魂八卦决策调度 · 实时状态          ║
╠══════════════════════════════════════════╣
║  态势值:   {score:>3}/100                              ║
║  当前卦:   {gua:<32}  ║
║  熔断:     {'🔴 已触发' if fused else '🟢 未触发':<30}  ║
║  校验失败: {fails}/{FAIL_COUNT_LIMIT}                                 ║
║  丁卯巡逻: 今日 {patrol_count:<2} 次                              ║
║  下一调度: 丁卯时 {next_label:<20}  ║
╚══════════════════════════════════════════╝
"""
    print(box.strip())
    print(f"DNA: {generate_dna('BAGUA-DASHBOARD')}")
    return 0


def cmd_check_hourly(args) -> int:
    """LaunchAgent 每小时调用：根据当前时辰决定动作。"""
    hour = datetime.now().hour
    if hour == 5:
        return cmd_trigger(args)
    elif hour == 11:
        return cmd_status(args)
    elif hour == 17:
        # 17:00 日志归档：trigger 一次再打印 log
        cmd_trigger(args)
        print("--- 日终归档 ---")
        return cmd_log(args)
    elif hour == 23:
        return cmd_reset(args)
    else:
        # 其余整点仅评估但不重置
        return cmd_trigger(args)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="龍魂八卦决策调度器 · lh-bagua",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="查看当前态势值、卦象、熔断状态")
    p_set = sub.add_parser("set", help="手动设定态势值（0-100）")
    p_set.add_argument("value", type=int, help="态势值")
    sub.add_parser("trigger", help="触发一次完整态势评估")
    sub.add_parser("reset", help="重置状态（解除熔断）")
    sub.add_parser("log", help="查看最近12次调度记录")
    sub.add_parser("dashboard", help="显示状态看板")
    sub.add_parser("hourly", help="内部：LaunchAgent 每小时调度入口")

    args = parser.parse_args(argv)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_PATH.exists():
        save_state(DEFAULT_STATE.copy())

    handlers = {
        "status": cmd_status,
        "set": cmd_set,
        "trigger": cmd_trigger,
        "reset": cmd_reset,
        "log": cmd_log,
        "dashboard": cmd_dashboard,
        "hourly": cmd_check_hourly,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
