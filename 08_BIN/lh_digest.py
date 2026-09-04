#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-CONTENT-AUTO-DIGEST-LOOP-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
"""龍魂·内容自动消化闭环 v1.0 · Content Auto-Digest Loop

粘贴即消化——不再等老大开口。任何贴进来的内容自动走四步:
  ① 分类（代码/文档/对话/报告/链接/笔记/碎片/混杂）
  ② 意图（修复/补全/分析/归档/复盘/执行/对比/生成/重构）
  ③ 上下文（自动匹配 brain 索引/COMMAND_INDEX/协议面 → 只读·轻量·节能）
  ④ 缺口与建议（对比既有规范找缺口 → 可执行步骤）
结果归档 digest 日记（~/.longhun/digest/diary/YYYY-MM-DD.md）+ results.jsonl(append-only)。
执行复盘可视化请走 lh recap（digest 只做轻量沉淀，不自动生成重物·节能）。

命令（lh digest <sub>）:
  (无参数)                  # 消化 inbox/ 全部待处理内容
  add <文本或"多行">        # 文本直接落盘 inbox(时间戳) 并消化
  inbox <文件路径>          # 把外部文件收进 inbox（不消化·只收件）
  --file <文件路径>         # 消化指定文件（不移动原文）
  status                    # 收件箱/已消化统计
  list [--limit N]          # 最近消化结果
  view <id>                 # 查看某次消化详情
  diary [--date YYYY-MM-DD] # 查看消化日记（默认今天）
  flush [--dry-run]         # 清空已处理 inbox 原文(移到 done/ 不删除·P0只冻结)
  self-test                 # 自测
设计: 零三方 · 数据主权全本地 ~/.longhun/digest/ · 节能(不常驻·按触发) ·
      AI 每次收到用户粘贴 → 自动落盘 inbox + 跑本命令（行为焊死 AGENTS.md §内容自动消化）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path

HOME_LH = Path(os.environ.get("LH_DIGEST_HOME") or (Path.home() / ".longhun"))
DIGEST_DIR = HOME_LH / "digest"
INBOX_DIR = DIGEST_DIR / "inbox"
DONE_DIR = DIGEST_DIR / "done"
DIARY_DIR = DIGEST_DIR / "diary"
RESULTS = DIGEST_DIR / "results.jsonl"
ROOT = Path(__file__).resolve().parent.parent
TOP = "诸葛鑫 | UID9622 · 龍芯北辰"

# ─────────── 分类与意图启发式 ───────────
CODE_KW = re.compile(r"\b(def|class|function|import|from|const|let|var|return|struct|interface|fn|print|echo)\b|(功能|方法|打印|定义|变量|如果|否则|循环|返回|初始化)\s*(\(|\{|：|:)?")
INTENT_KEYWORDS = [
    ("修复", ["修复", "修一下", "报错", "bug", "错误", "不行", "坏了", "挂了", "fix"]),
    ("补全", ["补全", "补", "缺", "漏", "缺失", "没写", "还没做", "待办", "TODO"]),
    ("分析", ["分析", "看看", "什么", "为什么", "怎么回", "说明", "解释", "判断"]),
    ("归档", ["归档", "收录", "存", "记录", "登记", "加入", "收进", "沉淀"]),
    ("复盘", ["复盘", "总结", "汇报", "回顾", "小结", "检视"]),
    ("执行", ["执行", "跑", "做", "部署", "上线", "发布", "生成", "开始", "干吧"]),
    ("对比", ["对比", "比较", "区别", "差异", "哪个好", "versus", "vs"]),
    ("生成", ["生成", "写", "创作", "创建", "产出", "写一个", "做个"]),
    ("重构", ["重构", "优化", "精简", "改造", "重写", "瘦身", "重构"]),
]
DEFAULT_INTENT = "归档/分析"


def _now() -> datetime:
    return datetime.now()


def _stamp() -> str:
    """干支时间戳（简单）· 优先 lh_time_engine · 失败降级 ISO"""
    try:
        p = subprocess.run([sys.executable, str(ROOT / "bin" / "lh_time_engine.py"),
                            "--stamp"], capture_output=True, text=True, timeout=2)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip().splitlines()[0][:80]
    except Exception:
        pass
    return _now().strftime("%Y-%m-%dT%H:%M:%S+0800")


def _new_id(text: str) -> str:
    raw = text.strip()
    h = hashlib.sha1((raw[:2000]).encode("utf-8")).hexdigest()[:8]
    return f"dig-{_now().strftime('%Y%m%d%H%M%S')}-{h}"


def _ensure_dirs() -> None:
    for d in (DIGEST_DIR, INBOX_DIR, DONE_DIR, DIARY_DIR):
        d.mkdir(parents=True, exist_ok=True)


# ─────────── ① 分类 ───────────
def classify(text: str) -> tuple:
    lines = text.strip().splitlines()
    size = len(text)
    scores = {}
    # 代码：代码块 或 代码关键字(英/中 CNSH) 或 常见文件扩展名
    if re.search(r"```", text):
        scores["代码"] = scores.get("代码", 0) + 5
    kw_hits = CODE_KW.findall(text)
    if kw_hits:
        scores["代码"] = scores.get("代码", 0) + min(2 + len(kw_hits), 6)
    if re.search(r"\.(py|js|ts|sh|bash|json|yaml|yml|cnsh|sql)\b", text):
        scores["代码"] = scores.get("代码", 0) + 2
    # 链接
    url_n = len(re.findall(r"https?://", text))
    if url_n:
        scores["链接"] = scores.get("链接", 0) + min(1 + url_n, 4)
    # 文档/规范：Markdown 标题或长文
    if re.search(r"^#{1,4}\s", text, re.M):
        scores["文档/规范"] = scores.get("文档/规范", 0) + 4
    # 外部报告/复盘
    if re.search(r"(报告|汇报|周报|复盘|总结|白皮书|论文|简报)", text):
        scores["外部报告"] = scores.get("外部报告", 0) + 3
    # 对话记录：多行且≥1/3行带冒号口吻，且无明显代码特征
    if not scores.get("代码") and len(lines) >= 3:
        colon_lines = sum(1 for ln in lines if re.match(r"^\s*[^:：\n]{1,30}[：:]", ln))
        if colon_lines >= max(2, len(lines) // 3):
            scores["对话记录"] = scores.get("对话记录", 0) + 3
    # 兜底
    if not scores:
        if size > 1500 or len(lines) > 20:
            scores["文档/规范"] = 1
        else:
            scores["笔记/碎片想法"] = 3
    cat = max(scores.items(), key=lambda kv: (kv[1], kv[0]))[0]
    if cat == "笔记/碎片想法" and size > 2000:
        cat = "文档/规范"
    return cat, scores


# ─────────── ② 意图 ───────────
def detect_intent(text: str) -> str:
    best, best_n = DEFAULT_INTENT, 0
    for name, kws in INTENT_KEYWORDS:
        n = sum(1 for k in kws if k.lower() in text.lower())
        if n > best_n:
            best, best_n = name, n
    return best


# ─────────── ③ 上下文（轻量·只读·节能） ───────────
def _load_brain_index():
    idx = HOME_LH / "brain" / "brain_index.json"
    try:
        if idx.exists():
            return json.loads(idx.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


def match_context(text: str) -> list:
    """brain 索引关键词召回 top3（标题/note 含内容显著词即记命中）"""
    out = []
    idx = _load_brain_index()
    if not isinstance(idx, dict):
        return out
    items = idx.get("items") or idx.get("entries") or []
    words = set(re.findall(r"[\u4e00-\u9fa5]{2,6}", text))
    strong = {w for w in words if w in text} if False else words
    scored = []
    for it in items[:400]:
        blob = " ".join(str(it.get(k, "")) for k in ("title", "note", "topic", "tags"))
        n = sum(1 for w in strong if w and w in blob)
        if n >= 2:
            scored.append((n, it.get("title") or it.get("id") or "?"))
    scored.sort(reverse=True)
    for n, t in scored[:3]:
        out.append(f"🧠 {t} (命中{n}词)")
    return out


def _registered_cmds() -> set:
    """从 COMMAND_INDEX 提取已登记 lh 命令集合"""
    cmds = set()
    for p in (ROOT / ".codebuddy" / "COMMAND_INDEX.md",
              ROOT / ".codebuddy" / "memory" / "MEMORY.md"):
        try:
            if p.exists():
                t = p.read_text(encoding="utf-8", errors="ignore")
                cmds |= set(re.findall(r"\blh\s+([a-z][a-z0-9-]*)", t))
        except Exception:
            pass
    return cmds


def gap_check(text: str) -> list:
    """缺口检查：提及的 lh 命令是否已登记 / 收款地址是否硬编码 / 是否涉新焊点"""
    gaps = []
    reg = _registered_cmds()
    mentioned = set(re.findall(r"\blh\s+([a-z][a-z0-9-]{2,})", text))
    for m in sorted(mentioned):
        if m not in reg and not m.startswith(("gpg", "mcp", "wallet", "gov", "council")):
            gaps.append(f"提及命令 `lh {m}` 未见登记（COMMAND_INDEX/MEMORY）→ 新功能或新命令，需登记/确认")
    if re.search(r"9E81MBx|TCMC|solana|wallet", text, re.I) and not re.search(r"lh wallet|官方|crypto\.json", text):
        gaps.append("涉及收款地址 → 铁律: 地址永不硬编码(AGENTS.md §6.6)·统一 lh wallet/crypto.json")
    if "焊死" in text and not re.search(r"焊死|P0", text[:600]):
        gaps.append("出现『焊死』语义 → 需按 16.1 走规则修订流程+确认码+GPG")
    return gaps


# ─────────── ④ 执行建议 ───────────
def suggest(cat: str, intent: str, text: str, gaps: list) -> list:
    s = []
    if intent == "修复":
        s.append("按『最小闭环』先跑 `lh digest self-test` 类自检复现 → 定位报错源 → 修复 → `lh gpg` 补签")
    elif intent in ("补全",):
        s.append("对缺口逐项补全（见缺口清单）·补完 GPG 签名 + COMMAND_INDEX 登记（若涉新命令）")
    elif intent == "分析":
        s.append("输出三色结论(🟢/🟡/🔴) + 依据 · 需要推演走 P01 · 涉审计走 P05")
    elif intent == "执行":
        s.append("确认目标最小闭环 → 直接执行(权限内) → 完成即静默(节能协议)")
    elif intent == "复盘":
        s.append("可用 `lh recap generate --cmd \"digest …\"` 生成完整可视化复盘")
    elif intent == "对比":
        s.append("列差异表(维度/差异/影响) → 结论 + 推荐路径")
    elif intent == "生成":
        s.append("先看是否已有同功能引擎(不重复造轮子) → 缺才新建 → 走最小闭环")
    elif intent == "重构":
        s.append("保持对外行为不变 → 先备份/冻结旧版 → 重构 → 自测 → 签名")
    else:
        s.append("默认: 归档 + 提取关键锚点入索引（知识沉淀）")
    if cat == "代码":
        s.append("代码先过语法自检 + 三色审计（涉安全走 P77/P05）")
    if cat == "文档/规范":
        s.append("文档落 01_protocols/12_DOCS 对应目录 · 文件头四行(归属名) · GPG 签名")
    if cat == "链接":
        s.append("链接素材: 按需抓取网页内容后重新消化（纯链接只记录，不自动外网抓取·节能）")
    if gaps:
        s.append("⚠️ 缺口检查命中 → 先处理缺口清单再动作")
    return s


# ─────────── 消化主流程 ───────────
def digest_text(text: str, source: str = "") -> dict:
    _ensure_dirs()
    text = text.strip()
    if not text:
        return {"error": "空内容"}
    cat, scores = classify(text)
    intent = detect_intent(text)
    ctx = match_context(text)
    gaps = gap_check(text)
    sug = suggest(cat, intent, text, gaps)
    rec = {
        "id": _new_id(text),
        "ts": _now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "stamp": _stamp(),
        "source": source or "inbox",
        "category": cat,
        "cat_scores": {k: v for k, v in sorted(scores.items(), key=lambda x: -x[1])},
        "intent": intent,
        "context": ctx,
        "gaps": gaps,
        "suggestions": sug,
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.splitlines()),
        "preview": text[:120].replace("\n", " "),
    }
    with open(RESULTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _append_diary(rec)
    return rec


def _append_diary(rec: dict) -> None:
    d = DIARY_DIR / (_now().strftime("%Y-%m-%d") + ".md")
    body = (
        f"\n## 📥 {rec['id']} · {rec['ts'][:16]}\n"
        f"- 来源: {rec['source']} · 分类: **{rec['category']}** · 意图: **{rec['intent']}** · "
        f"{rec['bytes']}B/{rec['lines']}行\n"
        f"- 预览: {rec['preview']}\n"
    )
    if rec["context"]:
        body += f"- 上下文命中: {('; '.join(rec['context']))}\n"
    if rec["gaps"]:
        body += f"- ⚠️ 缺口 {len(rec['gaps'])}: {' | '.join(rec['gaps'])}\n"
    body += f"- 建议: {('；'.join(rec['suggestions']))}\n"
    body += f"\n> {TOP} · {rec['stamp']} · 三色待定\n"
    with open(d, "a", encoding="utf-8") as f:
        f.write(body)


def process_inbox() -> list:
    _ensure_dirs()
    out = []
    for p in sorted(INBOX_DIR.iterdir()):
        if not p.is_file() or p.suffix in (".asc", ".swp"):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            out.append({"file": str(p), "error": str(e)})
            continue
        if not txt.strip():
            continue
        rec = digest_text(txt, source=f"inbox:{p.name}")
        rec["file"] = str(p)
        out.append(rec)
        # 处理完移到 done/（P0只冻结·不删除）
        try:
            done_p = DONE_DIR / p.name
            shutil.move(str(p), str(done_p))
        except Exception:
            pass
    return out


def _read_results() -> list:
    recs = []
    if RESULTS.exists():
        for line in RESULTS.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip():
                try:
                    recs.append(json.loads(line))
                except Exception:
                    pass
    return recs


# ─────────── CLI ───────────
def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if argv and argv[0] in ("--help", "-h", "help"):
        print(__doc__)
        return 0
    if argv and argv[0] == "self-test":
        t = "def 测试():\n    打印('粘贴自测')\n功能 主(){ }\n\n请帮我修复这个代码的报错，并对比旧版差异。\n"
        r = digest_text(t, source="self-test")
        print(f"✅ self-test digest id={r['id']} cat={r['category']} intent={r['intent']}")
        return 0
    if argv and argv[0] == "add":
        text = " ".join(argv[1:]).strip()
        if not text:
            print("用法: lh digest add \"<文本>\"")
            return 2
        p = INBOX_DIR / (_now().strftime("%Y%m%d%H%M%S") + ".md")
        p.write_text(text, encoding="utf-8")
        rec = digest_text(text, source=f"add:{p.name}")
        try:
            shutil.move(str(p), str(DONE_DIR / p.name))  # 原文冻结到 done/
        except Exception:
            pass
        _print_rec(rec)
        return 0
    if argv and argv[0] == "inbox":
        fp = Path(argv[1]) if len(argv) > 1 else None
        if not fp or not fp.exists():
            print("用法: lh digest inbox <文件路径>")
            return 2
        p = INBOX_DIR / (_now().strftime("%Y%m%d%H%M%S") + fp.suffix)
        shutil.copy(str(fp), str(p))
        print(f"📥 已收件 → {p}")
        return 0
    if argv and argv[0] == "--file":
        fp = Path(argv[1]) if len(argv) > 1 else None
        if not fp or not fp.exists():
            print("用法: lh digest --file <文件路径>")
            return 2
        txt = fp.read_text(encoding="utf-8", errors="replace")
        rec = digest_text(txt, source=str(fp))
        _print_rec(rec)
        return 0
    if argv and argv[0] in ("status", "stats"):
        recs = _read_results()
        _ensure_dirs()
        pending = [p for p in INBOX_DIR.iterdir() if p.is_file()]
        cats = {}
        for r in recs:
            cats[r.get("category", "?")] = cats.get(r.get("category", "?"), 0) + 1
        print(f"📥 收件箱待处理: {len(pending)}")
        print(f"✅ 已消化: {len(recs)} · 分类分布: {cats or '无'}")
        print(f"🗂️  数据: {DIGEST_DIR} · 日记: {DIARY_DIR}")
        return 0
    if argv and argv[0] in ("list",):
        limit = 10
        recs = _read_results()
        try:
            if "--limit" in argv:
                limit = int(argv[argv.index("--limit") + 1])
        except Exception:
            pass
        for r in recs[-limit:]:
            print(f"  {r.get('id')} [{r.get('ts','')[:16]}] {r.get('category'):>6}/{r.get('intent')}  {r.get('preview','')[:60]}")
        return 0
    if argv and argv[0] == "view":
        rid = argv[1] if len(argv) > 1 else ""
        recs = _read_results()
        for r in recs:
            if r.get("id") == rid or rid in r.get("id", ""):
                print(json.dumps(r, ensure_ascii=False, indent=2))
                return 0
        print(f"未找到 {rid}")
        return 1
    if argv and argv[0] == "diary":
        date = None
        if "--date" in argv:
            date = argv[argv.index("--date") + 1]
        d = DIARY_DIR / ((date or _now().strftime("%Y-%m-%d")) + ".md")
        if d.exists():
            print(d.read_text(encoding="utf-8"))
        else:
            print(f"日记不存在: {d}")
        return 0
    if argv and argv[0] == "flush":
        _ensure_dirs()
        dry = "--dry-run" in argv
        moved = 0
        for p in sorted(INBOX_DIR.iterdir()):
            if p.is_file() and p.suffix != ".asc":
                if dry:
                    print(f"  [dry] {p.name}")
                else:
                    try:
                        shutil.move(str(p), str(DONE_DIR / p.name))
                    except Exception as e:
                        print(f"  ✗ {p.name}: {e}")
                moved += 1
        print(f"{'[dry-run] ' if dry else ''}移动 {moved} 个到 done/（不删除·只冻结）")
        return 0
    # 默认：消化 inbox
    out = process_inbox()
    if not out:
        print("📥 收件箱为空。粘贴内容后 AI 会自动 `lh digest add`/`--file` 消化。\n"
              "  也可以: lh digest add \"<内容>\" · lh digest inbox <文件> · lh digest status")
        return 0
    for rec in out:
        if rec.get("error"):
            print(f"  ✗ {rec.get('file')}: {rec['error']}")
        else:
            _print_rec(rec)
    return 0


def _print_rec(rec: dict) -> None:
    print(f"📥 {rec['id']}")
    print(f"   分类: {rec['category']} · 意图: {rec['intent']} · {rec['bytes']}B")
    if rec.get("context"):
        print(f"   上下文: {'; '.join(rec['context'][:3])}")
    if rec.get("gaps"):
        print(f"   ⚠️ 缺口 {len(rec['gaps'])}:")
        for g in rec["gaps"][:5]:
            print(f"      - {g}")
    print(f"   建议:")
    for sg in rec["suggestions"][:6]:
        print(f"      - {sg}")
    print(f"   ✅ 已归档 digest 日记 {rec['ts'][:16]} · {rec['stamp']}")
    print()


if __name__ == "__main__":
    sys.exit(main())
