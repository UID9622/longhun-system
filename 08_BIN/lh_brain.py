#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-09-03-BRAIN-MEMORY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# -*- coding: utf-8 -*-
"""
龍魂 · 超级大脑记忆引擎 v1.0 · Super Brain Memory

补齐「对话中自动加载与更新记忆」的机制（CodeBuddy 超级大脑记忆系统任务 2026-09-03）:
  - 长期记忆权威源: .codebuddy/memory/MEMORY.md（workspace）+ 每日日志 .codebuddy/memory/YYYY-MM-DD.md
  - 本引擎记忆库:   ~/.longhun/brain/notes.jsonl（append-only 记忆片段）+ brain_index.json（关键词→片段ID·O(1)）
  - 检索增强:       save 时自动切词入索引 · search 先查索引再读全文 · 零三方依赖（CJK 二元组+英文单词）

命令:
  lh brain load [--context] [--lines N]      # 加载最近记忆 / --context 输出压缩上下文(MEMORY前N行+今日日志+最近3条)
  lh brain save [--note "xxx"] [--kw a,b] [--source xxx] [--silent]   # 存入长期记忆·自动入索引
  lh brain search <关键词> [--limit N] [--json]   # O(1) 索引召回
  lh brain remember <文本> [--silent]         # 「记住这个」别名·kind=decision
  lh brain summary [--silent]                 # 聚合当日/最近记忆→生成摘要(note kind=summary + summaries/<date>.md)
  lh brain hook pre|post [--cmd xxx]          # lh.py 自动联动钩子(轮数自增/环境触发保存/超50轮建议)
  lh brain index rebuild                      # 全量重建索引（保险）
  lh brain stats                              # 记忆库状态

数据主权: 全部落本地 ~/.longhun/brain/，不传云、不入第三方。append-only（P0 不删除只冻结）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

HOME_DIR = Path.home() / ".longhun"
# 支持 LH_BRAIN_DIR 环境覆盖（测试隔离/多会话独立库），默认 ~/.longhun/brain
BRAIN_DIR = Path(os.environ.get("LH_BRAIN_DIR") or (HOME_DIR / "brain"))
NOTES_FILE = BRAIN_DIR / "notes.jsonl"
INDEX_FILE = BRAIN_DIR / "brain_index.json"
SESSION_FILE = BRAIN_DIR / "session.json"
SUMMARY_DIR = BRAIN_DIR / "summaries"
ROOT = Path(__file__).resolve().parent.parent

# 记忆权威源降级链（首个存在者胜）: 任务假设 ~/.longhun/MEMORY.md → workspace 长期记忆 → 运行摘要
MEMORY_SOURCES: List[Path] = [
    HOME_DIR / "MEMORY.md",
    ROOT / ".codebuddy" / "memory" / "MEMORY.md",
    HOME_DIR / "memory" / "latest_digest.md",
    HOME_DIR / "memory" / "codebuddy_merged.md",
]
DAILY_DIR = ROOT / ".codebuddy" / "memory"

MAX_CTX_LINES = 50
_MAX_TOKENS_PER_NOTE = 512


# ---------- 基础工具 ----------

def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _note_id(text: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:6]
    return f"B-{ts}-{h}"


def _is_cjk(ch: str) -> bool:
    try:
        return unicodedata.name(ch).startswith("CJK")
    except ValueError:
        return False


def _tokenize(text: str) -> Set[str]:
    """关键词切分：英文单词(≥2) + CJK 连续段(2字及以上整体 + 滑动二元组)。零三方。"""
    toks: Set[str] = set()
    text = text.lower()
    for w in re.findall(r"[a-z0-9_]{2,}", text):
        toks.add(w)
    # CJK 连续段
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(seg) >= 2:
            toks.add(seg)
        for i in range(len(seg) - 1):
            toks.add(seg[i:i + 2])
    if len(toks) > _MAX_TOKENS_PER_NOTE:
        toks = set(list(toks)[:_MAX_TOKENS_PER_NOTE])
    return toks


def _load_notes() -> List[Dict[str, Any]]:
    if not NOTES_FILE.exists():
        return []
    out: List[Dict[str, Any]] = []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _load_index() -> Dict[str, List[str]]:
    if not INDEX_FILE.exists():
        return {}
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_index(idx: Dict[str, List[str]]) -> None:
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    tmp.replace(INDEX_FILE)


def _append_note(note: Dict[str, Any]) -> None:
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(note, ensure_ascii=False) + "\n")


def _update_index_for(note: Dict[str, Any]) -> None:
    """把单个 note 的词汇并入索引（save 时增量）。"""
    idx = _load_index()
    nid = note.get("id", "")
    if not nid:
        return
    toks = _tokenize(note.get("text", ""))
    for kw in note.get("keywords", []) or []:
        if isinstance(kw, str) and kw:
            toks.add(kw.strip().lower())
    for t in toks:
        bucket = idx.setdefault(t, [])
        if nid not in bucket:
            bucket.append(nid)
    _save_index(idx)


def _rebuild_index() -> Dict[str, List[str]]:
    idx: Dict[str, List[str]] = {}
    for n in _load_notes():
        nid = n.get("id", "")
        if not nid:
            continue
        toks = _tokenize(n.get("text", ""))
        for kw in n.get("keywords", []) or []:
            if isinstance(kw, str) and kw:
                toks.add(kw.strip().lower())
        for t in toks:
            idx.setdefault(t, []).append(nid)
    for bucket in idx.values():
        # 去重且保序（按 note 原始顺序）
        seen: Set[str] = set()
        dedup = []
        for nid in bucket:
            if nid not in seen:
                seen.add(nid)
                dedup.append(nid)
        bucket[:] = dedup
    _save_index(idx)
    return idx


def _note_snippet(note: Dict[str, Any], width: int = 110) -> str:
    text = (note.get("text") or "").replace("\n", " ⏎ ")
    if len(text) > width:
        text = text[:width] + "…"
    return text


def _print_note_line(note: Dict[str, Any]) -> None:
    kind = note.get("kind", "note")
    ts = (note.get("ts") or "")[5:16]  # MM-DDTHH:MM
    print(f"  🧠 [{note.get('id','')}] {kind} · {ts}")
    print(f"      {_note_snippet(note)}")


# ---------- 记忆源读取 ----------

def _first_memory_source() -> Path | None:
    for p in MEMORY_SOURCES:
        if p.exists():
            return p
    return None


def _read_context(lines: int = MAX_CTX_LINES) -> List[str]:
    """权威长期记忆前 N 行（压缩上下文）。"""
    src = _first_memory_source()
    if src is None:
        return [f"(无权威记忆源: 预期 {MEMORY_SOURCES[0]})"]
    out = []
    try:
        with open(src, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= lines:
                    break
                out.append(line.rstrip("\n"))
    except OSError as e:
        return [f"(读取 {src} 失败: {e})"]
    out.insert(0, f"# 📇 记忆源: {src} (前 {min(lines, len(out)) or lines} 行)")
    return out


def _daily_headlines(limit: int = 8) -> List[str]:
    """今日日志的 ## 标题（对话日志脉络）。"""
    d = DAILY_DIR / f"{_today()}.md"
    if not d.exists():
        return []
    heads = []
    with open(d, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("## ") and len(heads) < limit:
                heads.append(line.strip().lstrip("# ").strip())
    return heads


# ---------- 子命令 ----------

def cmd_load(context: bool, lines: int) -> int:
    if context:
        print("".join(_read_context(lines)))
        heads = _daily_headlines()
        if heads:
            print(f"\n# 🗓️ 今日日志脉络 {_today()}")
            for h in heads:
                print(f"  · {h}")
        notes = _load_notes()
        recent = [n for n in notes if n.get("kind") != "summary"][-3:]
        if recent:
            print(f"\n# 🧠 最近记忆片段（{len(recent)}）")
            for n in recent:
                _print_note_line(n)
        return 0
    # 默认: 最近 3 条记忆摘要
    notes = _load_notes()
    if not notes:
        print("  🧠 记忆库为空。用 `lh brain save --note \"...\"` 写入第一条。")
        return 0
    recent = notes[-3:]
    print(f"\n  🧠 超级大脑 · 最近 3 条记忆摘要（共 {len(notes)} 条）\n")
    for n in recent:
        _print_note_line(n)
    src = _first_memory_source()
    if src:
        print(f"\n  📇 权威记忆源: {src} 在线")
    return 0


def _save(note_text: str, keywords: List[str], source: str, kind: str, silent: bool) -> int:
    note_text = (note_text or "").strip()
    if not note_text:
        # 支持 stdin 管道（非 tty）
        if not sys.stdin.isatty():
            note_text = sys.stdin.read().strip()
    if not note_text:
        print("  ❌ 内容为空。用法: lh brain save --note \"要记住的内容\"")
        return 2
    if len(note_text) > 2000:
        print("  ⚠️ 内容过长(>2000字符)，请精简后重存")
        return 2
    # kind 自动判定（可按语义覆盖）
    auto_kind = kind
    if not auto_kind:
        if re.match(r"^(焊点|决策|裁决|铁律|记住|约定|确定)", note_text):
            auto_kind = "decision"
        elif re.match(r"^(新节点|图谱|注册|新增)", note_text):
            auto_kind = "node"
        else:
            auto_kind = "note"
    note: Dict[str, Any] = {
        "id": _note_id(note_text),
        "ts": _now_iso(),
        "date": _today(),
        "kind": auto_kind,
        "source": source or "lh-brain",
        "keywords": [k.strip() for k in keywords if k and k.strip()],
        "text": note_text,
    }
    _append_note(note)
    _update_index_for(note)
    if silent:
        return 0
    print(f"  ✅ 记忆已存盘 [{note['id']}] kind={auto_kind} · {note['ts']}")
    print(f"      {_note_snippet(note)}")
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    return _save(args.note or "", args.kw or [], args.source or "", args.kind or "", args.silent)


def cmd_remember(text: str, silent: bool) -> int:
    text = (text or "").strip()
    # 剥离「记住这个/记下来/记住了」前缀
    text = re.sub(r"^(记住这个|记下来|记住了|记住)[:：]?\s*", "", text)
    return _save(text, [], "user-say-remember", "decision", silent)


def cmd_search(query: str, limit: int, as_json: bool) -> int:
    query = (query or "").strip()
    if not query:
        print("  ❌ 用法: lh brain search <关键词>")
        return 2
    idx = _load_index()
    tokens = _tokenize(query)
    # 若索引空 → 先重建（保险）
    if not idx:
        idx = _rebuild_index()
    hits: Counter = Counter()
    for t in tokens:
        for nid in idx.get(t, []):
            hits[nid] += 1
    if not hits:
        # 降级: 线性扫描（索引未覆盖时保证能召回）
        for n in _load_notes():
            toks = _tokenize(n.get("text", ""))
            if tokens & toks:
                hits[n.get("id", "")] += 1
    if not hits:
        print(f"  🔍 未找到与「{query}」相关的记忆（共 {_load_notes().__len__()} 条）")
        return 1
    notes_by_id = {n.get("id", ""): n for n in _load_notes()}
    top_ids = [nid for nid, _ in hits.most_common(limit)]
    results = [notes_by_id[nid] for nid in top_ids if nid in notes_by_id]
    if as_json:
        print(json.dumps({"query": query, "total": len(results),
                          "results": results}, ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🔍 「{query}」命中 {len(results)} 条\n")
    for n in results:
        _print_note_line(n)
    return 0


def cmd_summary(silent: bool) -> int:
    notes = _load_notes()
    if not notes:
        print("  🧠 记忆库为空，暂无可总结")
        return 0
    day = _today()
    day_notes = [n for n in notes if n.get("date") == day]
    pool = day_notes or notes[-10:]
    kinds = Counter(n.get("kind", "note") for n in pool)
    tok_cnt: Counter = Counter()
    for n in pool:
        for t in _tokenize(n.get("text", "")):
            tok_cnt[t] += 1
    # 主题词: 过滤纯英文助词与过长段
    stop = {"memory", "lh", "brain", "note", "the", "and", "system"}
    topics = [t for t, _ in tok_cnt.most_common(20)
              if t not in stop and len(t) <= 12][:8]
    lines = [
        f"# 🧠 龙魂超级大脑 · 记忆摘要 {day}",
        "",
        f"- 记忆库总量: {len(notes)} 条（当日 {len(day_notes)} 条）",
        f"- 当日构成: " + " · ".join(f"{k}×{v}" for k, v in kinds.items()) if kinds else "- 构成: -",
        f"- 主题词: {(' / '.join(topics)) if topics else '（样本过少）'}",
        "",
    ]
    for n in pool[-3:]:
        lines.append(f"- [{n.get('id','')}] ({n.get('kind','note')}) {_note_snippet(n, 90)}")
    digest = "\n".join(lines)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    (SUMMARY_DIR / f"{day}.md").write_text(digest + "\n", encoding="utf-8")
    note: Dict[str, Any] = {
        "id": _note_id("summary:" + day),
        "ts": _now_iso(),
        "date": day,
        "kind": "summary",
        "source": "lh-brain-summary",
        "keywords": [f"摘要{day}"],
        "text": digest.replace("\n", " ⏎ ")[:1500],
    }
    _append_note(note)
    _update_index_for(note)
    if silent:
        return 0
    print(digest)
    print(f"\n  ✅ 摘要已存: {SUMMARY_DIR / (day + '.md')} + 记忆片段 [summary-{day}]")
    return 0


def cmd_hook(pre: bool, post: bool, cmd_label: str) -> int:
    """lh.py 自动联动钩子（静默·<2ms）: pre=轮数自增+超50轮建议 · post=环境触发保存/摘要。"""
    if os.environ.get("LH_BRAIN_OFF") == "1":
        return 0
    try:
        sess: Dict[str, Any] = {}
        if SESSION_FILE.exists():
            try:
                sess = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            except Exception:
                sess = {}
        if sess.get("date") != _today():
            sess = {"date": _today(), "rounds": 0, "cmds": []}
        if pre:
            sess["rounds"] = int(sess.get("rounds", 0)) + 1
            cmds = sess.setdefault("cmds", [])
            cmds.append({"t": datetime.now().strftime("%H:%M:%S"), "cmd": cmd_label or ""})
            if len(cmds) > 200:
                del cmds[: len(cmds) - 200]
            SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
            SESSION_FILE.write_text(json.dumps(sess, ensure_ascii=False), encoding="utf-8")
            if int(sess["rounds"]) == 50 and not os.environ.get("LH_BRAIN_QUIET"):
                print("  🧠 本会话已达 50 轮·建议 `lh brain summary` 沉淀记忆")
            return 0
        if post:
            note = os.environ.get("LH_BRAIN_SAVE")
            if note and note.strip():
                subprocess_quiet(["save", "--note", note.strip(), "--source", "lh-hook-post", "--silent"])
            if os.environ.get("LH_BRAIN_SUMMARY") == "1":
                subprocess_quiet(["summary", "--silent"])
            return 0
    except Exception:
        pass
    return 0


def subprocess_quiet(brain_args: List[str]) -> None:
    """同进程引擎不可靠时退回子进程（静默）。"""
    import subprocess
    try:
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_brain.py")] + brain_args,
                       cwd=str(ROOT), check=False, capture_output=True)
    except Exception:
        pass


def cmd_index(action: str) -> int:
    if action == "rebuild":
        idx = _rebuild_index()
        print(f"  ✅ 索引重建完成: {len(idx)} 词条")
        return 0
    print(f"  📇 索引词条: {len(_load_index())}")
    return 0


def cmd_stats(as_json: bool) -> int:
    notes = _load_notes()
    idx = _load_index()
    sess: Dict[str, Any] = {}
    if SESSION_FILE.exists():
        try:
            sess = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except Exception:
            sess = {}
    kinds = Counter(n.get("kind", "note") for n in notes)
    payload = {
        "notes_total": len(notes),
        "notes_today": sum(1 for n in notes if n.get("date") == _today()),
        "kinds": dict(kinds),
        "index_terms": len(idx),
        "session": sess,
        "brain_dir": str(BRAIN_DIR),
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"\n  🧠 超级大脑记忆库")
    print(f"  · 片段总数: {len(notes)} · 今日新增: {payload['notes_today']}")
    print(f"  · 构成: " + (" · ".join(f"{k}×{v}" for k, v in kinds.items()) if kinds else "空"))
    print(f"  · 索引词条: {len(idx)} 个（O(1) 召回）")
    print(f"  · 本会话轮数: {sess.get('rounds', 0)}")
    print(f"  · 数据目录: {BRAIN_DIR}")
    return 0


# ---------- 主入口 ----------

def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="lh brain", description="龙魂超级大脑记忆引擎",
                                allow_abbrev=False)
    sub = p.add_subparsers(dest="cmd")

    pl = sub.add_parser("load", help="加载最近记忆 / 压缩上下文")
    pl.add_argument("--context", action="store_true", help="输出压缩上下文(MEMORY前50行+今日日志+最近3条)")
    pl.add_argument("--lines", type=int, default=MAX_CTX_LINES)
    pl.set_defaults(fn=lambda a: cmd_load(a.context, a.lines))

    ps = sub.add_parser("save", help="存入长期记忆")
    ps.add_argument("--note", default="", help="要记住的内容")
    ps.add_argument("--kw", default=[], nargs="*", help="附加关键词（空格分隔）")
    ps.add_argument("--source", default="", help="来源标记")
    ps.add_argument("--kind", default="", help="note/decision/node/summary（缺省自动判定）")
    ps.add_argument("--silent", action="store_true")
    ps.set_defaults(fn=cmd_save)

    pr = sub.add_parser("remember", help="「记住这个」别名（kind=decision）")
    pr.add_argument("text", nargs="*", help="要记住的内容")
    pr.add_argument("--silent", action="store_true")
    pr.set_defaults(fn=lambda a: cmd_remember(" ".join(a.text).strip(), a.silent))

    pq = sub.add_parser("search", help="关键词检索（先查索引 O(1)）")
    pq.add_argument("query", nargs="*", help="检索词（可多个，空格分隔）")
    pq.add_argument("--limit", type=int, default=5)
    pq.add_argument("--json", action="store_true")
    pq.set_defaults(fn=lambda a: cmd_search(" ".join(a.query).strip(), a.limit, a.json))

    pm = sub.add_parser("summary", help="聚合当日/最近记忆→摘要入库")
    pm.add_argument("--silent", action="store_true")
    pm.set_defaults(fn=lambda a: cmd_summary(a.silent))

    ph = sub.add_parser("hook", help="lh.py 自动联动钩子")
    ph.add_argument("mode", choices=["pre", "post"], help="pre=执行前(轮数自增) post=执行后(环境触发)")
    ph.add_argument("--cmd", default="")
    ph.set_defaults(fn=lambda a: cmd_hook(a.mode == "pre", a.mode == "post", a.cmd))

    pi = sub.add_parser("index", help="索引维护")
    pi.add_argument("action", choices=["rebuild", "status"])
    pi.set_defaults(fn=lambda a: cmd_index(a.action))

    pt = sub.add_parser("stats", help="记忆库状态")
    pt.add_argument("--json", action="store_true")
    pt.set_defaults(fn=lambda a: cmd_stats(a.json))

    args = p.parse_args(argv)
    if not hasattr(args, "fn"):
        p.print_help()
        return 0
    try:
        return args.fn(args)
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
