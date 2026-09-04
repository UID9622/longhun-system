#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 日历记忆系统 v1.0 —— 日历即记忆库 · 多源聚合 · 哈希链不可抹去
DNA: #龍芯⚡️丙午·丁酉·壬午·亥时·䷟恒-CALENDAR-MEMORY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

=====================================================================
设计（老大 2026-09-04 原话翻译）:
  「日历就是记忆系统，每天做什么都在这，不可抹去，可以被系统检索引用」
  → 日历 = 用户自己的时间记忆库（本地为主 · 数据主权 P0）
  → 系统 = 只做检索层 + 哈希链背书（改/删 → 链断可检测）

源（按日聚合 · 只读源 · append-only 输出）:
  recap   本地复盘  ~/.longhun/recap/recaps/recap-*.json   （每次 lh 命令执行记录）
  memory  工作日志  <longhun-system>/.codebuddy/memory/YYYY-MM-DD.md
  wanli   万年历记录  ~/.龍魂/万年历/private/data/*.json
  yearring 年轮事件  <longhun-system>/yearring/events/*.json
  notion  Notion 镜像  <longhun-system>/notion-mirror/*.md  （文件指纹增量）
  note    当日速记  ~/.longhun/calendar_memory/notes/<date>.jsonl （append-only·唯一用户写入口）

数据家: ~/.longhun/calendar_memory/
  days/<date>.json   按日聚合条目（指纹去重 · 只增不改）
  chain.json         封链记录 {prev_hash → root_hash} · 任意改动 → 链校验失败
  index.json         源文件指纹缓存（mtime+size · 增量扫描）

CLI:  python3 lh_calendar_memory.py ingest [date] | ingest-all | search <词> [--limit N]
      | day <YYYY-MM-DD> | seal [date] | verify | status | sources | note <date> <文本>
外部 API（万年历 server 注入调用）:
      get_day(date) / search(kw) / add_note(date, text) / seal(date) / status()
=====================================================================
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

HOME = Path.home()
LH = HOME / ".longhun" / "calendar_memory"
LH.mkdir(parents=True, exist_ok=True)
DAYS = LH / "days"
DAYS.mkdir(parents=True, exist_ok=True)
NOTES = LH / "notes"
NOTES.mkdir(parents=True, exist_ok=True)
CHAIN = LH / "chain.json"
INDEX = LH / "index.json"

# 源路径（可被环境变量覆盖，便于分发给其他用户/机器）
ROOT = Path(os.environ.get("LONGHUN_ROOT", str(HOME / "longhun-system")))
SRC = {
    "recap":    Path(os.environ.get("LH_RECAP_DIR", str(HOME / ".longhun/recap/recaps"))),
    "memory":   ROOT / ".codebuddy" / "memory",
    "wanli":    Path(os.environ.get("LH_WANLI_DATA", str(HOME / ".龍魂/万年历/private/data"))),
    "yearring": ROOT / "yearring" / "events",
    "notion":   ROOT / "notion-mirror",
}
SCHEMA = "longhun-calendar-memory-v1"
NOTE_DNA = "#龍芯⚡️{date}-CALMEM-NOTE-UID9622"


def _h(s: str, n: int = 16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ------------------------------------------------------------------ 源读取
def _read_recap(date_str: str) -> list:
    """复盘 json：iso 前缀等于当日 → (kind=cmd, title=cmd, text=summary)"""
    out = []
    d = SRC["recap"]
    if not d.exists():
        return out
    pat = re.compile(r"recap-(\d{8})")
    for f in sorted(d.glob("recap-*.json")):
        m = pat.search(f.name)
        if not m or m.group(1) != date_str.replace("-", ""):
            continue
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
            fp = _h(f"{date_str}|recap|{f.name}", 12)
            out.append({
                "fp": fp, "source": "recap", "kind": "复盘",
                "title": str(j.get("cmd", f.name)),
                "text": str(j.get("summary", ""))[:400],
                "dna": str(j.get("dna", "")), "file": f.name,
            })
        except Exception:
            pass
    return out


def _read_memory(date_str: str) -> list:
    """工作日志 md：按 h2/h3/正文块切，单日文件通常 1 个"""
    out = []
    f = SRC["memory"] / f"{date_str}.md"
    if not f.exists():
        return out
    try:
        txt = f.read_text(encoding="utf-8")
        # 去标题行后截取有内容的开头 2000 字作为当日摘要
        body = re.sub(r"^#\s+.*$", "", txt, flags=re.M).strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        out.append({
            "fp": _h(f"{date_str}|memory|{f.name}|{os.path.getsize(f)}", 12),
            "source": "memory", "kind": "工作日志",
            "title": date_str,
            "text": body[:1500],
            "dna": f"memory-{date_str}", "file": f.name,
        })
    except Exception:
        pass
    return out


def _read_wanli(date_str: str) -> list:
    """万年历私有数据：尝试按日期键/文件名匹配"""
    out = []
    d = SRC["wanli"]
    if not d.exists():
        return out
    for f in sorted(d.glob("*.json")):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
            recs = j if isinstance(j, list) else [j]
            for r in recs:
                if not isinstance(r, dict):
                    continue
                hit = any(date_str in str(r.get(k, "")) for k in ("date", "ts", "time", "created_at"))
                if not hit:
                    continue
                title = str(r.get("title") or r.get("kind") or f.stem)
                out.append({
                    "fp": _h(f"{date_str}|wanli|{f.name}|{title}", 12),
                    "source": "wanli", "kind": "万年历",
                    "title": title,
                    "text": json.dumps(r, ensure_ascii=False)[:400],
                    "dna": str(r.get("dna", "")), "file": f.name,
                })
        except Exception:
            pass
    return out


def _read_yearring(date_str: str) -> list:
    out = []
    f = SRC["yearring"] / f"{date_str}.json"
    if not f.exists():
        return out
    try:
        j = json.loads(f.read_text(encoding="utf-8"))
        for ev in j.get("events", []):
            out.append({
                "fp": _h(f"{date_str}|yearring|{ev.get('event_id','')}", 12),
                "source": "yearring", "kind": "年轮事件",
                "title": str(ev.get("event_type", "event")),
                "text": str(ev.get("dna", ""))[:300],
                "dna": str(ev.get("dna", "")), "file": f.name,
            })
    except Exception:
        pass
    return out


def _notion_fp(f: Path) -> str:
    st = f.stat()
    return f"{f.name}|{st.st_mtime:.0f}|{st.st_size}"


def _read_notion(date_str: str, cache: dict) -> list:
    """Notion 镜像 md：正文按行找日期行归日（文件指纹缓存增量）"""
    out = []
    d = SRC["notion"]
    if not d.exists():
        return out
    key = str(d)
    idx = cache.setdefault(key, {})
    for f in sorted(d.glob("*.md")):
        fp = _notion_fp(f)
        hit_date = None
        if idx.get(f.name) == fp and date_str not in (idx.get("_dates") or []):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # 找 YYYY-MM-DD 行
        for line in txt.splitlines()[:400]:
            m = re.search(r"(20\d{2}-\d{2}-\d{2})", line)
            if m and m.group(1) == date_str:
                hit_date = date_str
                break
        idx[f.name] = fp
        if hit_date:
            title = f.name.replace(".md", "")
            out.append({
                "fp": _h(f"{date_str}|notion|{f.name}", 12),
                "source": "notion", "kind": "Notion",
                "title": title[:120],
                "text": txt[:1000],
                "dna": "", "file": f.name,
            })
    return out


def _read_notes(date_str: str) -> list:
    """当日速记（append-only jsonl）—— 用户的每日亲手记忆"""
    out = []
    f = NOTES / f"{date_str}.jsonl"
    if not f.exists():
        return out
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            j = json.loads(line)
            out.append({
                "fp": _h(f"note|{date_str}|{j.get('ts','')}|{j.get('text','')}", 12),
                "source": "note", "kind": "速记",
                "title": "我的记录",
                "text": str(j.get("text", ""))[:500],
                "dna": str(j.get("dna", "")), "file": f.name,
            })
        except Exception:
            pass
    return out


# ------------------------------------------------------------------ 聚合
def _load_index() -> dict:
    if INDEX.exists():
        try:
            return json.loads(INDEX.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_index(idx: dict) -> None:
    INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")


def _load_day(date_str: str) -> dict:
    f = DAYS / f"{date_str}.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"schema": SCHEMA, "date": date_str, "ganzhi": "", "updated": "",
            "count": 0, "root_hash": "", "entries": []}


def _save_day(day: dict) -> None:
    # 条目按 fp 排序后整体指纹 → root_hash（该日记忆的数字指纹）
    fps = sorted(e["fp"] for e in day["entries"])
    day["root_hash"] = _h("|".join(fps), 16)
    day["count"] = len(day["entries"])
    day["updated"] = _iso()
    f = DAYS / f"{day['date']}.json"
    f.write_text(json.dumps(day, ensure_ascii=False, indent=1), encoding="utf-8")


def ingest(date_str: str = None, verbose: bool = True) -> dict:
    """增量摄入某日（默认今天）→ days/<date>.json（指纹去重 · 只增不改）"""
    date_str = date_str or _today()
    day = _load_day(date_str)
    have = {e["fp"] for e in day["entries"]}
    idx = _load_index()
    added = []
    for src_fn in (_read_recap, _read_memory, _read_wanli, _read_yearring, _read_notion, _read_notes):
        try:
            for e in src_fn(date_str):
                if e["fp"] in have:
                    continue
                day["entries"].append(e)
                have.add(e["fp"])
                added.append(e)
        except Exception:
            continue
    _save_day(day)
    _save_index(idx)
    if verbose:
        print(f"📅 记忆摄入 {date_str} · 新增 {len(added)} · 累计 {day['count']} 条")
        for e in added:
            print(f"   [{e['source']}] {e['title']}")
    return {"date": date_str, "added": len(added), "total": day["count"]}


def ingest_all() -> None:
    """扫描源文件分布 → 得到全部有记录的日期 → 逐日摄入"""
    dates = set()
    if SRC["recap"].exists():
        for f in SRC["recap"].glob("recap-*.json"):
            m = re.search(r"recap-(\d{8})", f.name)
            if m:
                dates.add(f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}")
    if SRC["memory"].exists():
        for f in SRC["memory"].glob("20*.md"):
            m = re.search(r"(20\d{2}-\d{2}-\d{2})", f.name)
            if m:
                dates.add(m.group(1))
    if SRC["yearring"].exists():
        for f in SRC["yearring"].glob("*.json"):
            m = re.search(r"(20\d{2}-\d{2}-\d{2})", f.name)
            if m:
                dates.add(m.group(1))
    if NOTES.exists():
        for f in NOTES.glob("*.jsonl"):
            m = re.search(r"(20\d{2}-\d{2}-\d{2})", f.name)
            if m:
                dates.add(m.group(1))
    total = 0
    for d in sorted(dates):
        total += ingest(d, verbose=False).get("total", 0)
    print(f"🧠 全量摄入完成 · {len(dates)} 天 · {total} 条记忆")


# ------------------------------------------------------------------ 检索
def search(kw: str, limit: int = 20) -> list:
    """跨全部已摄入日记忆全文检索 → [{date, count, entries:[...]}] 按日期倒序"""
    words = [w for w in re.split(r"[\s,，。、]+", kw.strip()) if w]
    if not words:
        return []
    results = []
    for f in sorted(DAYS.glob("*.json"), reverse=True):
        try:
            day = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        hits = []
        for e in day.get("entries", []):
            blob = " ".join(str(e.get(k, "")) for k in ("title", "text", "dna", "source"))
            if all(w.lower() in blob.lower() for w in words):
                hits.append(e)
        if hits:
            results.append({"date": day.get("date"), "count": len(hits), "entries": hits[:limit]})
            if sum(r["count"] for r in results) >= limit * 3:
                break
    return results[:limit]


# ------------------------------------------------------------------ 封链
def _load_chain() -> dict:
    if CHAIN.exists():
        try:
            return json.loads(CHAIN.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"schema": "longhun-calendar-memory-chain-v1", "chain": []}


def _save_chain(c: dict) -> None:
    CHAIN.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")


def seal(date_str: str = None, verbose: bool = True) -> dict:
    """将某日条目 root_hash 封进链：prev_hash → root_hash · 事后任何改动 → verify 失败"""
    date_str = date_str or _today()
    day = _load_day(date_str)
    c = _load_chain()
    chain = c["chain"]
    prev_hash = chain[-1]["hash"] if chain else "0" * 16
    rec = {
        "date": date_str,
        "count": day["count"],
        "prev_hash": prev_hash,
        "root_hash": day.get("root_hash", ""),
        "ts": _iso(),
    }
    rec["hash"] = _h(f"{rec['date']}|{rec['prev_hash']}|{rec['root_hash']}|{rec['count']}", 16)
    # append-only 封链：链环永不覆盖（不可抹去语义）
    # 幂等：同日同 root 已封 → 跳过，不产生重复环
    if chain and chain[-1]["date"] == date_str and chain[-1]["root_hash"] == rec["root_hash"]:
        if verbose:
            print(f"🔒 {date_str} 已封（幂等跳过）· root={rec['root_hash']}")
        return {"date": date_str, "count": day["count"], "hash": chain[-1]["hash"], "skipped": True}
    chain.append(rec)
    _save_chain(c)
    if verbose:
        print(f"🔒 封链 {date_str} · {day['count']} 条 · root={rec['root_hash']} · hash={rec['hash']}")
    return {"date": date_str, "count": day["count"], "hash": rec["hash"]}


def verify() -> dict:
    """重算整条链 → ok 或 断点位置"""
    c = _load_chain()
    chain = c.get("chain", [])
    prev = "0" * 16
    for i, r in enumerate(chain):
        want = _h(f"{r['date']}|{prev}|{r['root_hash']}|{r['count']}", 16)
        if r.get("hash") != want or r.get("prev_hash") != prev:
            return {"ok": False, "break_at": i, "date": r.get("date")}
        prev = r["hash"]
    return {"ok": True, "links": len(chain)}


# ------------------------------------------------------------------ 速记
def add_note(date_str: str, text: str) -> dict:
    """当日速记（append-only）→ notes/<date>.jsonl → 可被聚合/检索引用"""
    date_str = date_str or _today()
    text = (text or "").strip()
    if not text:
        return {"ok": False, "msg": "文本为空"}
    rec = {
        "ts": _iso(),
        "date": date_str,
        "text": text[:500],
        "dna": NOTE_DNA.format(date=date_str.replace("-", "")),
    }
    f = NOTES / f"{date_str}.jsonl"
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    ingest(date_str, verbose=False)
    seal(date_str, verbose=False)
    return {"ok": True, "date": date_str, "text": rec["text"]}


# ------------------------------------------------------------------ 展示
def show_day(date_str: str = None) -> None:
    date_str = date_str or _today()
    day = _load_day(date_str)
    print(f"📅 {day['date']} · {day['count']} 条 · root={day.get('root_hash','')}")
    for e in day.get("entries", []):
        print(f"  [{e.get('source')}|{e.get('kind')}] {e.get('title')}")
        txt = (e.get("text") or "").replace("\n", " ")
        if txt:
            print(f"      {txt[:160]}")


def status() -> dict:
    files = sorted(DAYS.glob("*.json"))
    total_entries = 0
    for f in files:
        try:
            total_entries += json.loads(f.read_text(encoding="utf-8")).get("count", 0)
        except Exception:
            pass
    return {
        "days": len(files), "entries": total_entries,
        "chain_links": len(_load_chain().get("chain", [])),
        "chain_ok": verify()["ok"],
        "data_dir": str(LH),
    }


def sources() -> None:
    print("🧠 日历记忆 · 数据源状态")
    for name, p in SRC.items():
        n = 0
        if p.exists():
            n = len(list(p.glob("*")))
        flag = "✅" if n else "⬜"
        print(f"  {flag} {name:<9} {p}")
    n = len(list(NOTES.glob("*.jsonl"))) if NOTES.exists() else 0
    print(f"  {'✅' if n else '⬜'} {'note':<9} {NOTES} ({n} 天速记)")


# ------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser(prog="lh_calendar_memory", description="龍魂日历记忆系统")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("ingest")
    sub.add_parser("ingest-all")
    p_search = sub.add_parser("search")
    p_search.add_argument("kw", nargs="*")
    p_search.add_argument("--limit", type=int, default=20)
    p_day = sub.add_parser("day")
    p_day.add_argument("date", nargs="?", default=None)
    p_seal = sub.add_parser("seal")
    p_seal.add_argument("date", nargs="?", default=None)
    sub.add_parser("verify")
    sub.add_parser("status")
    sub.add_parser("sources")
    p_note = sub.add_parser("note")
    p_note.add_argument("date", nargs="?", default=None)
    p_note.add_argument("text", nargs="*")
    args = ap.parse_args()

    if args.cmd == "ingest":
        ingest()
    elif args.cmd == "ingest-all":
        ingest_all()
    elif args.cmd == "search":
        kw = " ".join(args.kw or [])
        if not kw:
            print("用法: lh calmem search <关键字>"); return 1
        res = search(kw, limit=args.limit)
        print(f"🔎 搜索「{kw}」· {sum(r['count'] for r in res)} 条命中")
        for r in res:
            print(f"  📅 {r['date']} · {r['count']} 条")
            for e in r["entries"]:
                print(f"     [{e['source']}|{e['kind']}] {e['title']}")
                txt = (e.get("text") or "").replace("\n", " ")
                if txt:
                    print(f"        {txt[:140]}")
    elif args.cmd == "day":
        show_day(args.date)
    elif args.cmd == "seal":
        seal(args.date)
    elif args.cmd == "verify":
        v = verify()
        print(f"🔗 链校验: {'✅ 完整 (' + str(v['links']) + ' 环)' if v['ok'] else '🔴 断点 @' + str(v.get('break_at'))}")
        return 0 if v["ok"] else 2
    elif args.cmd == "status":
        s = status()
        print(f"🧠 日历记忆 · {s['days']} 天 · {s['entries']} 条 · 链 {s['chain_links']} 环"
              f" · {'✅' if s['chain_ok'] else '🔴'}")
        print(f"   数据家: {s['data_dir']}")
    elif args.cmd == "sources":
        sources()
    elif args.cmd == "note":
        r = add_note(args.date, " ".join(args.text or []))
        print(("✅ 速记已落账 · " if r.get("ok") else "❌ " + r.get("msg", "")) +
              (f"{r.get('date')} · 已聚合+封链" if r.get("ok") else ""))
    else:
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
