#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-05-HEALTH-SNAPSHOT-ENGINE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·每日健康快照 + 一周健康报告引擎 v1.0 — `lh health snapshot` / `lh health report`
#  ─ snapshot: 记录当前健康全项(health --json) + 对外交付拓扑(节点/边/根哈希) + 最近3条变更事件
#              → ~/.longhun/health_snapshots/YYYY-MM-DD/HH.json（HH=07 早 / 21 晚）
#  ─ report:   汇总一周 7天×早晚 快照 → 周报 ~/.longhun/health_weekly/health_report_YYYY-MM-DD.md
#              + 自动 GPG 签名 + 耻辱墙事件 type=health_weekly
# 状态判定: 🟢 全绿 / 🟡 1-2项异常或待关注 / 🔴 3项以上异常或根哈希不一致
# 零三方依赖 · 静默运行（launchd 早晚自动跑 · 无输出）

import argparse
import contextlib
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # longhun-system/
BIN = ROOT / "08_BIN"
TOPO_JSON = ROOT / "docs" / "topology" / "对外交付_legion_topo.json"
STATE_DIR = Path.home() / ".longhun"
SNAP_DIR = STATE_DIR / "health_snapshots"              # 快照库 YYYY-MM-DD/HH.json
WEEKLY_DIR = STATE_DIR / "health_weekly"               # 周报库 health_report_*.md
SHAME_DIR = STATE_DIR / "shame_wall"
SHAME_JSON = SHAME_DIR / "shame_wall.json"             # 归一审判官耻辱墙
TOPO_AUDIT = SHAME_DIR / "topo_audit.jsonl"            # 拓扑事件流（周报拓扑变更汇总数据源）
GPG_SIGN = BIN / "lh_gpg_sign.py"

RED, YELLOW, GREEN = "🔴", "🟡", "🟢"


# ─────────────────────────── 基础工具 ───────────────────────────

def _now():
    return _dt.datetime.now().astimezone()


def _call_health_json() -> dict:
    """调 lh_health.py --json（复用全量自检逻辑 · 超时 120s）"""
    r = subprocess.run([sys.executable, str(BIN / "lh_health.py"), "--json"],
                       capture_output=True, text=True, timeout=120, cwd=str(ROOT))
    try:
        return json.loads(r.stdout or "{}")
    except Exception:  # noqa: BLE001
        return {"tool": "lh-health", "error": (r.stderr or r.stdout or "")[-400:],
                "checks": [], "summary": {"ok": 0, "fail": 0, "warn": 0, "total": 0}}


def _topo_local_status() -> dict:
    """对外交付拓扑本地状态: nodes/edges/root_hash/last_sync
    root_hash 与 lh_health 同口径: group|name|dna 行排序聚合 → SHA-256 前16位"""
    s = {"graph": "对外交付", "ok": False, "nodes": 0, "edges": 0,
         "root_hash": "", "last_sync": ""}
    if not TOPO_JSON.is_file():
        return s
    try:
        data = json.loads(TOPO_JSON.read_text(encoding="utf-8"))
        lines = []
        for g in data.get("groups", []):
            for a in g.get("assets", []):
                lines.append(f"{g.get('name')}|{a.get('name')}|{a.get('dna') or ''}")
        s["nodes"] = sum(len(g.get("assets", [])) for g in data.get("groups", []))
        s["edges"] = len(data.get("edges") or [])
        s["root_hash"] = hashlib.sha256(
            "\n".join(sorted(lines)).encode("utf-8")).hexdigest()[:16].upper()
        s["last_sync"] = str(data.get("last_sync", ""))
        s["ok"] = s["nodes"] > 0
    except Exception:  # noqa: BLE001
        pass
    return s


def _topo_events_tail(limit: int = 3) -> list:
    """耻辱墙 topo_audit.jsonl 反向最近 limit 条（含新旧两代事件兼容）"""
    rows = []
    if TOPO_AUDIT.is_file():
        with contextlib.suppress(Exception):
            for line in TOPO_AUDIT.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                rows.append({"ts": str(e.get("ts", "")), "type": str(e.get("type", "")),
                             "color": str(e.get("color", GREEN)), "severity": str(
                                 e.get("severity") or ("warning" if e.get("warn") else "info")),
                             "detail": str(e.get("detail", ""))[:160],
                             "ops": (e.get("ops") or [])})
    return rows[-max(1, limit):]


def _judge_status(health: dict, topo: dict, has_unhandled: bool) -> tuple:
    """健康判定 → (mark, reason)
    🟢 全绿: 无异常项 · 根哈希一致 · 无未处理告警
    🟡 1-2项异常 / 拓扑有变更未同步
    🔴 3项以上异常 / 根哈希不一致(mark=🔴)"""
    checks = health.get("checks", [])
    issues = [c for c in checks if (c.get("mark") or "🟢") != GREEN]
    root = next((c for c in checks if "根哈希" in c.get("name", "")), None)
    root_bad = bool(root) and (root.get("mark") == RED or not root.get("ok"))
    n = len(issues)
    if n >= 3 or root_bad:
        names = "、".join(c.get("name", "") for c in issues[:5])
        return RED, f"{n} 项异常{(' · 根哈希不一致' if root_bad else '')} · {names}"
    if n >= 1 or has_unhandled:
        names = "、".join(c.get("name", "") for c in issues[:3]) or "拓扑事件待查看"
        return YELLOW, f"{n} 项待关注{(' · 拓扑变更未同步' if has_unhandled else '')} · {names}"
    return GREEN, "全部通过 · 根哈希在线一致 · 无未处理告警"


def _find_slot() -> str:
    """当前 slot: 07(<=11) / 21(>11)，保证早晚语义与目录规范"""
    h = _now().hour
    return "07" if h < 12 else "21"


# ─────────────────────────── snapshot ───────────────────────────

def cmd_snapshot(force: bool = False, quiet: bool = False) -> int:
    ts = _now()
    slot = _find_slot()
    health = _call_health_json()
    topo = _topo_local_status()
    events = _topo_events_tail(3)
    # 根哈希一致: 复用 health 第13项结论（含线上比对）
    root_ck = next((c for c in health.get("checks", [])
                    if "根哈希" in c.get("name", "")), None)
    if root_ck:
        topo["online_ok"] = bool(root_ck.get("ok")) and (root_ck.get("mark") != RED)
        m = re.search(r"[0-9A-F]{16}", str(root_ck.get("detail", "")))
        if m:
            topo["online_hash"] = m.group(0)
    has_unhandled = bool((health.get("topo_events") or {}).get("has_warn"))
    mark, reason = _judge_status(health, topo, has_unhandled)

    day_dir = SNAP_DIR / ts.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    out_p = day_dir / f"{slot}.json"
    if out_p.exists() and not force:
        if not quiet:
            print(f"  ⏭️  {out_p} 已存在（--force 覆盖）", flush=True)
        return 0
    snap = {
        "tool": "lh-health-snapshot", "version": "1.0",
        "ts": ts.isoformat(timespec="seconds"), "day": ts.strftime("%Y-%m-%d"),
        "slot": slot, "status": mark, "reason": reason,
        "health_summary": health.get("summary", {}),
        "health_checks": health.get("checks", []),
        "topo": topo, "topo_events": events,
        "error": health.get("error", ""),
    }
    tmp = out_p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, out_p)
    if not quiet:
        print(f"  ✅ 健康快照 {mark} · {ts.strftime('%Y-%m-%d %H:%M')} · {out_p}", flush=True)
    return 0


# ─────────────────────────── report ───────────────────────────

def _iso_week_range(ref: _dt.date) -> tuple:
    """ISO 周: 周一 ~ 周日（ref 所在自然周）"""
    monday = ref - _dt.timedelta(days=ref.weekday())
    sunday = monday + _dt.timedelta(days=6)
    return monday, sunday


def _load_week_snapshots(monday: _dt.date, sunday: _dt.date) -> list:
    """读一周快照 → [{day, slot, data}]（07/21 两槽）"""
    out = []
    for d in range((sunday - monday).days + 1):
        day = monday + _dt.timedelta(days=d)
        day_dir = SNAP_DIR / day.strftime("%Y-%m-%d")
        for slot in ("07", "21"):
            p = day_dir / f"{slot}.json"
            if p.is_file():
                try:
                    out.append({"day": day.strftime("%Y-%m-%d"), "slot": slot,
                                "data": json.loads(p.read_text(encoding="utf-8"))})
                except Exception:  # noqa: BLE001
                    out.append({"day": day.strftime("%Y-%m-%d"), "slot": slot, "data": {}})
    return out


def _week_topo_changes(monday: _dt.date, sunday: _dt.date) -> dict:
    """周内拓扑变更汇总（从 topo_audit.jsonl ops 聚合 · 兼容旧事件 detail 正则）"""
    agg = {"events": 0, "add": 0, "update": 0, "remove": 0, "warn": 0, "red": 0}
    if not TOPO_AUDIT.is_file():
        return agg
    lo, hi = _dt.datetime.combine(monday, _dt.time.min), _dt.datetime.combine(
        sunday, _dt.time.max)
    with contextlib.suppress(Exception):
        for line in TOPO_AUDIT.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                ts = e.get("ts", "")
                if not ts:
                    continue
                for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
                    try:
                        dt_ = _dt.datetime.strptime(ts, fmt)
                        break
                    except ValueError:
                        dt_ = None
                if not dt_:
                    continue
                if not (lo <= dt_.replace(tzinfo=None) <= hi):
                    continue
            except Exception:  # noqa: BLE001
                continue
            agg["events"] += 1
            col = str(e.get("color", GREEN))
            if col == RED:
                agg["red"] += 1
            elif str(e.get("severity", "")) == "warning" or col == YELLOW:
                agg["warn"] += 1
            ops = e.get("ops") or []
            if ops:
                for o in ops:
                    op = str(o.get("op", ""))
                    if op == "add":
                        agg["add"] += 1
                    elif op == "update":
                        agg["update"] += 1
                    elif op == "remove":
                        agg["remove"] += 1
            else:  # 旧事件: detail 正则 "新增N·更新N·移除N"
                d = str(e.get("detail", ""))
                m_add = re.search(r"新增(\d+)", d)
                m_up = re.search(r"更新(\d+)", d)
                m_rm = re.search(r"移除(\d+)", d)
                agg["add"] += int(m_add.group(1)) if m_add else 0
                agg["update"] += int(m_up.group(1)) if m_up else 0
                agg["remove"] += int(m_rm.group(1)) if m_rm else 0
    return agg


def _fmt_row(snaps: list, day: str) -> str:
    """单日行: | 日期 | 07 | 21 | 日评 |"""
    cells = {"07": "—", "21": "—"}
    for s in snaps:
        if s["day"] == day:
            d = s["data"]
            mark = str(d.get("status", "")) or "?"
            cells[s["slot"]] = f"{mark} {str(d.get('reason', ''))[:18]}"
    return f"| {day} | {cells['07']} | {cells['21']} |"


def _build_report(monday: _dt.date, sunday: _dt.date, snaps: list,
                  changes: dict) -> str:
    status_cnt = {GREEN: 0, YELLOW: 0, RED: 0}
    abnormal = []
    for s in snaps:
        mark = str(s["data"].get("status", "")) or ""
        if mark in status_cnt:
            status_cnt[mark] += 1
        if mark != GREEN:
            issues = [f"{c.get('name','')}:{c.get('detail','')[:60]}"
                      for c in s["data"].get("health_checks", [])
                      if (c.get("mark") or GREEN) != GREEN]
            abnormal.append({"day": s["day"], "slot": s["slot"], "status": mark,
                             "reason": s["data"].get("reason", ""), "issues": issues[:6]})
    expect = 14
    lines = []
    lines.append(f"# 🏥 龍魂一周健康报告 · {monday:%Y-%m-%d} ~ {sunday:%Y-%m-%d}\n")
    lines.append("> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 ｜ GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    lines.append(f"> DNA: #龍芯⚡️2026-09-05-HEALTH-WEEKLY-REPORT-v1.0-UID9622")
    lines.append(f"> 生成: {_now().strftime('%Y-%m-%d %H:%M:%S')} · 自动早晚快照(07/21)+每周日自动汇总\n")

    lines.append("## 一、本周快照汇总")
    lines.append(f"- 应记录快照: {expect} 条（7 天 × 早/晚）· 实际: {len(snaps)} 条"
                 + (" 🟡 缺失快照" if len(snaps) < expect else ""))
    lines.append("")
    lines.append("| 日期 | 早07 | 晚21 |")
    lines.append("|:---|:---|:---|")
    for d in range((sunday - monday).days + 1):
        day = (monday + _dt.timedelta(days=d)).strftime("%Y-%m-%d")
        lines.append(_fmt_row(snaps, day))
    lines.append("")

    lines.append("## 二、状态分布")
    lines.append(f"- {GREEN} 全绿: {status_cnt[GREEN]} 条")
    lines.append(f"- {YELLOW} 待关注: {status_cnt[YELLOW]} 条")
    lines.append(f"- {RED} 需介入: {status_cnt[RED]} 条\n")

    lines.append("## 三、拓扑变更汇总（本周耻辱墙事件）")
    lines.append(f"- 变更事件: {changes['events']} 条 · "
                 f"新增 {changes['add']} · 更新 {changes['update']} · 移除 {changes['remove']}"
                 f"{(' · 🟡告警 ' + str(changes['warn']) + ' · 🔴' + str(changes['red'])) if changes['warn'] or changes['red'] else ''}\n")

    lines.append("## 四、异常快照详情")
    if not abnormal:
        lines.append("- 无异常快照 🟢")
    else:
        for a in abnormal:
            lines.append(f"- **{a['day']} {a['slot']}** · {a['status']} {a['reason']}")
            for it in a["issues"][:4]:
                lines.append(f"  - {it}")
    lines.append("")

    red_n = status_cnt[RED]
    yellow_n = status_cnt[YELLOW]
    if red_n:
        concl = f"{RED} **本周有 {red_n} 条需介入快照，建议关注以下异常并处理。**"
    elif yellow_n:
        concl = f"{YELLOW} 本周整体正常，但有 {yellow_n} 条待关注快照，建议查看异常详情。"
    else:
        concl = f"{GREEN} 本周正常：{len(snaps)}/{expect} 条快照全绿，系统平稳。"
    lines.append(f"## 五、结论建议\n{concl}\n")
    lines.append("---")
    lines.append("*龍魂·每日健康快照自动化 · 早 07:00 / 晚 21:00 自动记录 · 每周日 23:00 自动生成 · 耻辱墙事件 type=health_weekly*")
    return "\n".join(lines)


def _shame_weekly_append(ts, report_rel: str, mark: str, detail: str):
    """耻辱墙记录 type=health_weekly（同步 shame_wall.json · 轻量结构随墙 v1.1）"""
    with contextlib.suppress(Exception):
        SHAME_DIR.mkdir(parents=True, exist_ok=True)
        sj = json.loads(SHAME_JSON.read_text(encoding="utf-8")) if SHAME_JSON.is_file() \
            else {"version": "1.1", "记录": []}
        recs = sj.setdefault("记录", [])
        recs.append({"date": ts.date().isoformat(),
                     "time": ts.isoformat(timespec="seconds"),
                     "type": "health_weekly", "color": mark,
                     "bad": 1 if mark == RED else 0,
                     "warn": 1 if mark == YELLOW else 0,
                     "severity": "warning" if mark != GREEN else "info",
                     "reason": f"周健康报告 · {detail} · {report_rel}"})
        sj["总记录数"] = len(recs)
        sj["生成时间"] = ts.isoformat(timespec="seconds")
        SHAME_JSON.write_text(json.dumps(sj, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")


def cmd_report(week_ref: str = "", quiet: bool = False) -> int:
    ts = _now()
    try:
        ref = _dt.date.fromisoformat(week_ref) if week_ref else ts.date()
    except ValueError:
        print(f"  ❌ 日期格式错误: {week_ref}（需 YYYY-MM-DD）", flush=True)
        return 2
    monday, sunday = _iso_week_range(ref)
    snaps = _load_week_snapshots(monday, sunday)
    changes = _week_topo_changes(monday, sunday)
    md = _build_report(monday, sunday, snaps, changes)

    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    out_p = WEEKLY_DIR / f"health_report_{sunday.strftime('%Y-%m-%d')}.md"
    out_p.write_text(md + "\n", encoding="utf-8")

    # 自动 GPG 分离签名（与源文件同目录）
    sign_ok = False
    with contextlib.suppress(Exception):
        if GPG_SIGN.is_file():
            r = subprocess.run([sys.executable, str(GPG_SIGN), "sign", str(out_p)],
                               capture_output=True, text=True, timeout=120, cwd=str(ROOT))
            sign_ok = r.returncode == 0

    # 耻辱墙事件 health_weekly
    mark = RED if any(s["data"].get("status") == RED for s in snaps) else \
        (YELLOW if any(s["data"].get("status") == YELLOW for s in snaps) else GREEN)
    detail = f"{len(snaps)} 条快照 · 生成 {out_p.name}"
    _shame_weekly_append(ts, out_p.name, mark, detail)

    if not quiet:
        print(f"  ✅ 周健康报告 {mark} · {out_p} · GPG "
              f"{'✅' if sign_ok else '❌（lh_gpg_sign 签名失败）'}"
              f" · 耻辱墙 health_weekly 已记", flush=True)
    return 0 if sign_ok else (0 if not GPG_SIGN.is_file() else 1)


# ─────────────────────────── main ───────────────────────────

def main():
    ap = argparse.ArgumentParser(
        prog="lh health snapshot/report",
        description="龍魂每日健康快照 + 一周健康报告 (lh health snapshot | lh health report)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_snap = sub.add_parser("snapshot", help="生成当前健康快照 (早07/晚21)")
    p_snap.add_argument("--force", action="store_true", help="覆盖当日同槽已有快照")
    p_snap.add_argument("--quiet", action="store_true", help="静默（launchd 用）")
    p_rep = sub.add_parser("report", help="生成一周健康报告（默认本周）")
    p_rep.add_argument("--week", dest="week", metavar="YYYY-MM-DD", default="",
                       help="指定周内任一天（默认今天所在自然周）")
    p_rep.add_argument("--quiet", action="store_true", help="静默")
    args = ap.parse_args()

    if args.cmd == "snapshot":
        return cmd_snapshot(force=args.force, quiet=args.quiet)
    return cmd_report(week_ref=args.week, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
