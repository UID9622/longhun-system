#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·每日审计引擎 v1.0 — 每日 03:00 自审 · 系统自己养自己
================================================================
DNA:    #龍芯⚡️20260902-DAILY-AUDIT-v1.0-9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
协议:    CC BY-NC-SA 4.0（核心思想层）

功能:
  --run    每日全流程: 互搏审计核心文件 + health + 铭碑校验 → 综合分
           → JSON 报告(~/.longhun/audit/daily/YYYY-MM-DD.json)
           → 分<80 自动耻辱墙告警 + Bark 通知
  --show   查看最近报告
  --dir    只输出报告目录

设计:
  - 纯标准库 · 零三方依赖 · 单文件可跑
  - 综合分 = 互搏overall×0.6 + health通过率×0.25 + 铭碑校验×0.15
  - 阈值: 🟢≥80 🟡≥60 🔴<60 (与 lh_audit_battle_hub 同口径)
  - 告警落点: ~/.longhun/audit/alerts.json (append-only 审计日志)
    + ~/.longhun/shame_wall/shame_wall.json (耻辱墙, 若存在)
    + Bark 推送 (key 存 ~/.longhun/bark_key, 无 key 静默跳过)
  - 报告保留 30 天, 自动清理过期
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # longhun-system/
BIN = ROOT / "08_BIN"
REPORT_DIR = Path.home() / ".longhun" / "audit" / "daily"
ALERT_FILE = Path.home() / ".longhun" / "audit" / "alerts.json"
SHAME_JSON = Path.home() / ".longhun" / "shame_wall" / "shame_wall.json"
BARK_KEY_FILE = Path.home() / ".longhun" / "bark_key"

# 每日互搏审计的核心文件（轻量·节能·覆盖"能治"三大件）
CORE_TARGETS = [
    "lh_asi_boot.py",   # ASI 启动
    "lh_memorial.py",   # 铭碑引擎
    "lh_health.py",     # 健康自检
    "lh_judge.py",      # 归一审判官
]


def run_capture(cmd: list, timeout: int = 180) -> str:
    """跑命令拿 stdout（失败静默返回空串）"""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:
        return ""


def audit_battle(target: str):
    """跑左右互搏审计，提取综合评分 overall + color"""
    out = run_capture([sys.executable, str(BIN / "lh_audit_battle_hub.py"),
                       "audit", "--target", str(BIN / target)], timeout=240)
    m = re.search(r"综合评分:\s*(\S+)\s+([\d.]+)\s*\(互搏[\d.]+ / 平衡[\d.]+ / 安全[\d.]+\)", out)
    if not m:
        return None
    return {"file": target, "color": m.group(1), "overall": float(m.group(2))}


def health_check():
    """跑 lh health --json，取 ok/fail 通过率"""
    out = run_capture([sys.executable, str(BIN / "lh_health.py"), "--json"], timeout=120)
    try:
        data = json.loads(out.split("\n", 1)[-1] if "\n{" in out else out)
    except Exception:
        return None
    s = data.get("summary", {})
    ok = s.get("ok", 0)
    total = s.get("total", 0)
    return {"ok": ok, "fail": s.get("fail", 0), "total": total,
            "pass_rate": round(ok / total * 100, 2) if total else 0.0}


def memorial_verify():
    """铭碑校验 → 100 或 0"""
    out = run_capture([sys.executable, str(BIN / "lh_memorial.py"), "--verify"], timeout=120)
    ok = "一致" in out and "🟢" in out
    return {"ok": ok, "detail": out.strip()[:80]}


def bark_push(title: str, body: str):
    """Bark 推送（无 key 或失败静默）"""
    if not BARK_KEY_FILE.exists():
        return
    key = BARK_KEY_FILE.read_text().strip()
    if not key:
        return
    url = f"https://api.day.app/{key}/{title}/{body}"
    try:
        import urllib.request
        urllib.request.urlopen(url, timeout=10)
    except Exception:
        pass


def append_alert(entry: dict):
    """append-only 告警审计日志"""
    ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = []
    if ALERT_FILE.exists():
        try:
            data = json.loads(ALERT_FILE.read_text())
        except Exception:
            data = []
    data.append(entry)
    ALERT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def append_shame_wall(entry: dict):
    """同步追加到耻辱墙 JSON（若存在且有 记录 list）"""
    if not SHAME_JSON.exists():
        return
    try:
        data = json.loads(SHAME_JSON.read_text())
    except Exception:
        return
    recs = data.get("记录") or data.get("records")
    if isinstance(recs, list):
        recs.append({
            "日期": entry["date"],
            "类型": "系统内审",
            "详情": entry["reason"],
            "综合分": entry["overall"],
        })
        SHAME_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def cleanup_old(days: int = 30):
    """清理超过 N 天的旧报告"""
    cutoff = datetime.now() - timedelta(days=days)
    for f in REPORT_DIR.glob("*.json"):
        try:
            dt = datetime.strptime(f.stem, "%Y-%m-%d")
            if dt < cutoff:
                f.unlink()
        except Exception:
            pass


def run_daily(quiet: bool = False):
    now = datetime.now(timezone.utc).astimezone()
    date_str = now.strftime("%Y-%m-%d")

    # 1. 互搏审计核心文件（取最低分代表当日基线）
    battles = []
    for t in CORE_TARGETS:
        r = audit_battle(t)
        if r:
            battles.append(r)
    battle_score = min((b["overall"] for b in battles), default=None)
    battle_color = next((b["color"] for b in battles if b["overall"] == battle_score), "🟡")

    # 2. 健康自检
    health = health_check()

    # 3. 铭碑校验
    memorial = memorial_verify()

    # 4. 综合分（缺项按 0 计，防止假高分）
    parts = []
    if battle_score is not None:
        parts.append(battle_score * 0.6)
    if health:
        parts.append(health["pass_rate"] * 0.25)
    if memorial:
        parts.append((100 if memorial["ok"] else 0) * 0.15)
    overall = round(sum(parts), 2) if parts else 0.0
    color = "🟢" if overall >= 80 else ("🟡" if overall >= 60 else "🔴")

    report = {
        "date": date_str,
        "generated_at": now.isoformat(),
        "dna": "#龍芯⚡️20260902-DAILY-AUDIT-v1.0-9622",
        "score": {"overall": overall, "color": color,
                  "battle": battle_score, "battle_color": battle_color,
                  "health": health["pass_rate"] if health else None,
                  "memorial_ok": memorial["ok"] if memorial else None},
        "details": {"battles": battles, "health": health, "memorial": memorial},
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / f"{date_str}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2))

    # 5. 低分告警（<80 → 耻辱墙 + Bark）
    if overall < 80:
        reason = (f"每日审计{color} 综合分{overall} "
                  f"(互搏{battle_score} health{report['score']['health']} 铭碑{report['score']['memorial_ok']})")
        alert = {"date": date_str, "time": now.isoformat(), "overall": overall,
                 "color": color, "reason": reason}
        append_alert(alert)
        append_shame_wall(alert)
        bark_push("🐉龍魂每日审计", f"{color} 综合分{overall} 需人工查看")

    cleanup_old()
    return report


def show_latest():
    files = sorted(REPORT_DIR.glob("*.json"), reverse=True)
    if not files:
        return "📭 暂无每日审计报告（先 --run）"
    r = json.loads(files[0].read_text())
    sc = r["score"]
    lines = [f"📊 每日审计 {r['date']} · {sc['color']} 综合分 {sc['overall']}",
             f"   互搏 {sc.get('battle')} · health {sc.get('health')} · 铭碑 {sc.get('memorial_ok')}"]
    for b in r["details"].get("battles", []):
        lines.append(f"   {b['file']:<22} {b['color']} {b['overall']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·每日审计引擎 v1.0")
    ap.add_argument("--run", action="store_true", help="每日全流程自审")
    ap.add_argument("--show", action="store_true", help="查看最近报告")
    ap.add_argument("--dir", action="store_true", help="报告目录")
    args = ap.parse_args()

    if args.show:
        print(show_latest())
        return 0
    if args.dir:
        print(str(REPORT_DIR))
        return 0

    report = run_daily()
    sc = report["score"]
    print(f"📊 每日审计 {report['date']} · {sc['color']} 综合分 {sc['overall']}"
          f" (互搏{sc['battle']} health{sc['health']} 铭碑{sc['memorial_ok']})")
    print(f"   报告: {REPORT_DIR / (report['date'] + '.json')}")
    if report["score"]["overall"] < 80:
        print(f"   ⚠️ 低于80阈值 · 耻辱墙+Bark 告警已触发")
    return 0


if __name__ == "__main__":
    sys.exit(main())
