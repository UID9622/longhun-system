#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·申时·䷔噬嗑-MEMORY-ARCH-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·记忆分层架构 v1.0（MemGPT 思路落地）
三级记忆：工作记忆(working) / 长期记忆(longterm) / 档案(archive)
- working   : 当日会话日志，append-only  （.codebuddy/memory/YYYY-MM-DD.md）
- longterm  : 常驻结构化记忆，in-place 更新（.codebuddy/memory/MEMORY.md）
- archive   : 跨主题沉淀档案，落知识库   （knowledge/auto-learned/memory-archive/）

用法:
  lh_memory_arch.py status                      # 三层概览
  lh_memory_arch.py write -l working -t "..." [--topic 主题]
  lh_memory_arch.py write -l longterm -t "..." [--topic 主题]
  lh_memory_arch.py write -l archive  -t "..." [--topic 主题]
  lh_memory_arch.py read -l working [--days 3]  # 最近 N 天工作记忆
  lh_memory_arch.py read -l longterm [--head N]
  lh_memory_arch.py read -l archive [--list]
  lh_memory_arch.py distill [--days 14]         # 近期日志蒸馏→长期记忆巩固
"""
import argparse
import datetime
import os
import re
import sys

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "longhun-system")
MEM_DIR = os.path.join(BASE, ".codebuddy", "memory")
LONGTERM = os.path.join(MEM_DIR, "MEMORY.md")
ARCHIVE_DIR = os.path.join(BASE, "knowledge", "auto-learned", "memory-archive")

LAYERS = {"working", "longterm", "archive"}


def _now():
    return datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _today():
    return datetime.date.today().isoformat()


def _gen_dna(topic):
    """生成记忆条目 DNA（干支日期+主题+哈希8）"""
    h = __import__("hashlib").sha256(f"{_now()}{topic}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{_today()}-MEM-{topic or 'note'}-{h}"


def _daily_path(day=None):
    return os.path.join(MEM_DIR, f"{day or _today()}.md")


def _append(path, text, topic):
    """append-only 写入（文件尾非换行先补，防半截行吞内容）"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "rb") as f:
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b"\n":
                with open(path, "ab") as f2:
                    f2.write(b"\n")
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def _write_working(text, topic):
    ts = _now().split()[1]
    dna = _gen_dna(topic)
    entry = f"\n## [{ts}] {topic or '记录'} · {dna}\n- {text.strip()}\n"
    path = _daily_path()
    _append(path, entry, topic)
    return path


def _write_longterm(text, topic):
    """长期记忆：MEMORY.md 内追加条目（in-place）"""
    dna = _gen_dna(topic or "longterm")
    entry = f"\n## {_today()} · {topic or '长期记忆'} · {dna}\n{text.strip()}\n"
    if not os.path.exists(LONGTERM):
        _append(LONGTERM, entry, topic)
    else:
        with open(LONGTERM, "a", encoding="utf-8") as f:
            f.write(entry)
    return LONGTERM


def _write_archive(text, topic):
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", topic or "archive")[:24] or "archive"
    path = os.path.join(ARCHIVE_DIR, f"{_today()}-{slug}.md")
    dna = _gen_dna(topic or "archive")
    body = (
        f"# {topic or '記憶檔案'} · {_today()}\n\n"
        f"> DNA: `{dna}`\n> 层级: archive(档案) · 来源: 工作记忆沉淀\n\n"
        f"{text.strip()}\n"
    )
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def cmd_status():
    print("🐉 龍魂·记忆分层状态")
    # working
    days = sorted(f for f in os.listdir(MEM_DIR) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f))
    print(f"  working  工作记忆: {len(days)} 天日志（最新 {days[-1] if days else '无'}）")
    # longterm
    if os.path.exists(LONGTERM):
        size = os.path.getsize(LONGTERM)
        print(f"  longterm 长期记忆: MEMORY.md {size}B")
    else:
        print("  longterm 长期记忆: 未初始化")
    # archive
    n = len([f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".md")]) if os.path.isdir(ARCHIVE_DIR) else 0
    print(f"  archive  档案库: {n} 条沉淀")
    return 0


def cmd_write(layer, text, topic):
    if layer == "working":
        path = _write_working(text, topic)
    elif layer == "longterm":
        path = _write_longterm(text, topic)
    else:
        path = _write_archive(text, topic)
    print(f"✅ 已写入 {layer}: {path}")
    return 0


def cmd_read(layer, days, head):
    if layer == "working":
        targets = sorted(
            f for f in os.listdir(MEM_DIR) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f)
        )[-days:]
        for f in targets:
            p = os.path.join(MEM_DIR, f)
            print(f"── {f}（{os.path.getsize(p)}B）──")
            with open(p, encoding="utf-8") as fh:
                print(fh.read()[-2000:])
    elif layer == "longterm":
        if not os.path.exists(LONGTERM):
            print("（长期记忆未初始化）")
            return 0
        with open(LONGTERM, encoding="utf-8") as f:
            content = f.read()
        print(content[:head] if head else content)
    else:
        if not os.path.isdir(ARCHIVE_DIR):
            print("（档案库为空）")
            return 0
        for f in sorted(os.listdir(ARCHIVE_DIR)):
            if f.endswith(".md"):
                p = os.path.join(ARCHIVE_DIR, f)
                print(f"  {f}  {os.path.getsize(p)}B")
    return 0


def cmd_auto():
    """自动巩固：阈值触发蒸馏（不常驻·调用即查·省算力）
    触发条件：今日日志 > 40KB 或 距上次巩固 ≥ 7 天"""
    state = os.path.join(MEM_DIR, ".auto_consolidate")
    last = open(state).read().strip() if os.path.exists(state) else ""
    today = _today()
    size = os.path.getsize(_daily_path()) if os.path.exists(_daily_path()) else 0
    days_since = 999
    if last:
        try:
            days_since = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(last)).days
        except ValueError:
            days_since = 999
    if size < 40_000 and days_since < 7:
        print("✅ 记忆健康，无需巩固")
        return 0
    cmd_distill(14)
    os.makedirs(MEM_DIR, exist_ok=True)
    with open(state, "w", encoding="utf-8") as f:
        f.write(today)
    print("✅ 记忆已自动巩固（distill→MEMORY.md）")
    return 0


def cmd_distill(days):
    """蒸馏：读近期 daily → 按主题聚合高频关键词 → 生成要点 → 追加 MEMORY.md"""
    days_l = sorted(
        f for f in os.listdir(MEM_DIR) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f)
    )[-days:]
    blob = ""
    for f in days_l:
        with open(os.path.join(MEM_DIR, f), encoding="utf-8") as fh:
            blob += fh.read() + "\n"
    # 主题聚合：统计 ## 标题频率
    heads = re.findall(r"^## (.+)$", blob, re.M)
    from collections import Counter
    top = Counter(h[:12] for h in heads if not h.startswith("["))
    summary = "\n".join(f"- {k}（{v} 次）" for k, v in top.most_common(12))
    body = (
        f"## 近期蒸馏 · {_today()}（{len(days_l)} 天日志聚合）\n"
        f"活跃主题 Top：\n{summary}\n"
    )
    with open(LONGTERM, "a", encoding="utf-8") as f:
        f.write("\n" + body)
    print(f"✅ 蒸馏完成：{len(days_l)} 天 → {len(top)} 个主题 → MEMORY.md")
    return 0


def main():
    ap = argparse.ArgumentParser(description="龍魂·记忆分层架构 v1.0")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("status")
    w = sub.add_parser("write")
    w.add_argument("-l", "--layer", choices=sorted(LAYERS), required=True)
    w.add_argument("-t", "--text", required=True)
    w.add_argument("--topic", default="")
    r = sub.add_parser("read")
    r.add_argument("-l", "--layer", choices=sorted(LAYERS), required=True)
    r.add_argument("--days", type=int, default=3)
    r.add_argument("--head", type=int, default=0)
    d = sub.add_parser("distill")
    d.add_argument("--days", type=int, default=14)
    sub.add_parser("auto")
    args = ap.parse_args()

    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "write":
        return cmd_write(args.layer, args.text, args.topic)
    if args.cmd == "read":
        return cmd_read(args.layer, args.days, args.head)
    if args.cmd == "distill":
        return cmd_distill(args.days)
    if args.cmd == "auto":
        return cmd_auto()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
