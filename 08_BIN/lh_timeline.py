#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·甲申·辛巳·亥时·䷋否-TIMELINE-LOGGER-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""⏱️ 操作时间轴引擎 v1.0 — 龍魂全部操作可回溯（2026-09-04·方案A3落地）

理念: 所有 lh 命令执行自动追加一行 JSONL（含干支戳），按日分文件。
时间轴=审计链的轻量视图·与 session（当前状态）/ checkpoint（任务断点）互补。

数据: ~/.longhun/timeline/YYYY-MM-DD.jsonl（JSONL·append-only·极低存储开销）
行格式: {"ts": ISO, "ganzhi": "丙午·…·子时", "type": "command", "cmd": "...", "total": N}
用法:
  lh timeline show [--today|--date YYYY-MM-DD|--tail N]
  lh timeline search <关键词>     → 全文搜索历史操作
  lh timeline export [--json]    → 导出当日全部（--json 走标准输出）
  lh timeline stats              → 统计（总行数/按日分布/命令频次Top）
  lh timeline _record <cmd>      → 自动记录钩子（由 lh.py 调用·静默）

干支说明: 此处为简版（年干支60甲子·月干支按公历月·时支2h制），
完整四柱（含日柱/卦象/节气月建）走权威时间引擎 `lh te --stamp` 审计链。
"""
import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.home() / ".longhun"
TIMELINE_DIR = ROOT / "timeline"

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"


def _local_now() -> datetime:
    """干支以北京时为准（本地时区）·时间戳列仍含 UTC 偏移"""
    return datetime.now().astimezone()


def ganzhi_simple(dt: datetime) -> str:
    """简版干支戳: 年(60甲子) + 月(简) + 时(2h制·23时归子时正确)"""
    y = (dt.year - 4) % 60
    hour = (dt.hour + 1) // 2 % 12
    return (f"{TIANGAN[y % 10]}{DIZHI[y % 12]}年·"
            f"{TIANGAN[dt.month % 10]}{DIZHI[dt.month % 12]}月·"
            f"{DIZHI[hour]}时")


def _file_for(date_str: str) -> Path:
    TIMELINE_DIR.mkdir(parents=True, exist_ok=True)
    return TIMELINE_DIR / f"{date_str}.jsonl"


def _read_lines(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            d = json.loads(ln)
            if isinstance(d, dict):
                out.append(d)
        except Exception:
            continue
    return out


def record(cmd_name: str = "", typ: str = "command", extra: dict | None = None) -> dict:
    """追加一行（append-only·线程安全度够用: 每命令一次·低频）"""
    now = _local_now()
    rec = {"ts": now.isoformat(), "ganzhi": ganzhi_simple(now),
           "type": typ, "cmd": cmd_name or "-"}
    if extra:
        rec.update(extra)
    with open(_file_for(now.strftime("%Y-%m-%d")), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def cmd_show(args) -> int:
    if args.date:
        date_str = args.date
    else:
        date_str = _local_now().strftime("%Y-%m-%d")
    rows = _read_lines(_file_for(date_str))
    if args.tail:
        rows = rows[-args.tail:]
    if not rows:
        print(f"  ⏱️  {date_str} 无记录（每执行一条 lh 命令自动追加）")
        return 0
    print(f"  ⏱️  时间轴 · {date_str} · {len(rows)} 条\n")
    for r in rows:
        ts = (r.get("ts") or "")[11:19]
        cmd = r.get("cmd") or "-"
        mark = "🐉" if r.get("type") != "command" else "⚡"
        print(f"  {mark} {ts}  [{r.get('ganzhi')}]  {cmd}")
    return 0


def cmd_search(kw: str) -> int:
    hits = []
    for f in sorted(TIMELINE_DIR.glob("*.jsonl")):
        for r in _read_lines(f):
            blob = json.dumps(r, ensure_ascii=False)
            if kw in blob:
                hits.append((f.stem, r))
    if not hits:
        print(f"  ⏱️  未找到含「{kw}」的历史操作")
        return 0
    print(f"  ⏱️  命中 {len(hits)} 条:\n")
    for day, r in hits[:30]:
        ts = (r.get("ts") or "")[11:19]
        print(f"  {day} {ts}  [{r.get('ganzhi')}]  {r.get('cmd') or '-'}")
    if len(hits) > 30:
        print(f"  … 其余 {len(hits) - 30} 条被截断（导出可看全量）")
    return 0


def cmd_export(json_out: bool) -> int:
    rows = []
    for f in sorted(TIMELINE_DIR.glob("*.jsonl")):
        rows.extend(_read_lines(f))
    rows.sort(key=lambda r: r.get("ts", ""))
    if json_out:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        for r in rows:
            ts = (r.get("ts") or "")[11:19]
            print(f"{r.get('ts','')[:10]} {ts}  [{r.get('ganzhi')}]  {r.get('cmd') or '-'}")
    print(f"\n  ⏱️  共 {len(rows)} 条 · 时间轴导出完成")
    return 0


def cmd_stats() -> int:
    per_day = Counter()
    per_cmd = Counter()
    total = 0
    for f in sorted(TIMELINE_DIR.glob("*.jsonl")):
        rows = _read_lines(f)
        total += len(rows)
        per_day[f.stem] = len(rows)
        for r in rows:
            c = r.get("cmd") or "-"
            per_cmd[c] += 1
    print(f"  ⏱️  时间轴统计 · 共 {total} 条 · 文件 {len(per_day)} 个")
    if per_day:
        print("\n  按日分布:")
        for day, n in sorted(per_day.items()):
            print(f"    {day}  {n} 条")
    if per_cmd:
        print("\n  命令频次 Top10:")
        for c, n in per_cmd.most_common(10):
            print(f"    {n:>3}  lh {c}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh timeline", description="操作时间轴")
    sub = ap.add_subparsers(dest="cmd")
    sh = sub.add_parser("show", help="查看某日时间轴")
    sh.add_argument("--today", action="store_true")
    sh.add_argument("--date", default="")
    sh.add_argument("--tail", type=int, default=0)
    sr = sub.add_parser("search", help="全文搜索历史操作")
    sr.add_argument("kw")
    ex = sub.add_parser("export", help="导出全部")
    ex.add_argument("--json", action="store_true", dest="json_out")
    sub.add_parser("stats", help="统计")
    rc = sub.add_parser("_record", help="自动记录钩子（lh.py 内部）")
    rc.add_argument("cmd_name", nargs="?", default="")
    args = ap.parse_args()
    if args.cmd in (None, "show"):
        return cmd_show(args)
    if args.cmd == "search":
        return cmd_search(args.kw)
    if args.cmd == "export":
        return cmd_export(args.json_out)
    if args.cmd == "stats":
        return cmd_stats()
    if args.cmd == "_record":
        record(args.cmd_name or "")
        return 0
    print(f"  ❌ 未知子命令: {args.cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
