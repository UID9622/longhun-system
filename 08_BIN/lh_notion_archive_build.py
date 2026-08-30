#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·癸巳·申时·䷣明夷-NOTION-ARCHIVE-BUILD-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: 工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）
# 状态: 🟢 v1.0 上线

"""Notion 备份转换引擎 v1.0 — 把 notion_archive 备份目录转为结构化索引 + 花名册库转表。

用法:
    python3 bin/lh_notion_archive_build.py            # 构建索引 JSON + 花名册结构 + 输出摘要
    python3 bin/lh_notion_archive_build.py --json     # 只输出索引 JSON 路径
    python3 bin/lh_notion_archive_build.py --domain CNSH与工程实现   # 只处理某域
    python3 bin/lh_notion_archive_build.py --roster   # 只转换花名册数据库结构

输出:
    - 12_DOCS/notion_archive_2026-08-07/notion_archive_INDEX.json   # 机器可读索引
    - 12_DOCS/notion_archive_2026-08-07/roster_schema.md             # 花名册字段结构表
    - 终端摘要（每域文档数/行数/DNA完整率）
"""

import json
import os
import re
import sys
from datetime import datetime

ARCHIVE_ROOT = os.path.join("12_DOCS", "notion_archive_2026-08-07")
OUTPUT_INDEX = os.path.join(ARCHIVE_ROOT, "notion_archive_INDEX.json")
ROSTER_SOURCE = os.path.join("archive", "backups_cp", "roster_notion_backup_20260830_120932.json")
OUTPUT_ROSTER = os.path.join(ARCHIVE_ROOT, "roster_schema.md")

# 兼容格式: `- **DNA**: #龍芯...` / `> DNA: ...` / `<!-- DNA: #龍芯... -->` / `【DNA：】`
DNA_RE = re.compile(r"\**DNA\**\s*[:：]\s*(#[^\s]+)", re.I)
# 标题须跳过元数据行（CONFIRM/SEAL/DNA/协议等），取第一个真实 H1
TITLE_RE = re.compile(r"^#\s+(.+)$")
TITLE_SKIP = ("CONFIRM", "SEAL", "DNA", "协议", "创建者", "归属名", "License",
              "状态", "来源", "GPG", "确认码", "<!--")


def extract_meta(fp: str) -> dict:
    """提取单个 .md 文件的元数据：标题/DNA/行数/首段/关键词"""
    with open(fp, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    text = "\n".join(lines)
    title = ""
    dna = ""
    for i, line in enumerate(lines[:40]):
        m = DNA_RE.search(line)
        if m and not dna:
            dna = m.group(1)
        if i < 15 and not title:
            m2 = TITLE_RE.match(line)
            if m2 and not any(k in m2.group(1) for k in TITLE_SKIP):
                title = m2.group(1).strip()
    if not title:
        # 回退：文件名（去 .md）
        title = os.path.basename(fp)[:-3]
    # 摘要：首个非空非头注释段落（≤120字）
    excerpt = ""
    for line in lines:
        s = line.strip()
        if not s or s.startswith(("#", ">", "<!--", "--")):
            continue
        excerpt = s[:120]
        break
    # 关键词：取标题拆分 + 常见标签
    kws = [w for w in re.split(r"[·\s\-—_/｜｜|]", title) if w and len(w) <= 20]
    return {
        "title": title,
        "dna": dna,
        "lines": len(lines),
        "excerpt": excerpt,
        "keywords": list(dict.fromkeys(kws))[:6],
    }


def build() -> dict:
    """扫描备份目录，构建完整索引"""
    domains = []
    total_docs = 0
    total_lines = 0
    dna_ok = 0
    for d in sorted(os.listdir(ARCHIVE_ROOT)):
        p = os.path.join(ARCHIVE_ROOT, d)
        if not os.path.isdir(p) or d.startswith("."):
            continue
        docs = []
        for f in sorted(os.listdir(p)):
            if not f.endswith(".md") or f.startswith("."):
                continue
            meta = extract_meta(os.path.join(p, f))
            meta["file"] = os.path.join(d, f)
            meta["domain"] = d
            docs.append(meta)
            total_docs += 1
            total_lines += meta["lines"]
            if meta["dna"]:
                dna_ok += 1
        domains.append({"domain": d, "docs": docs, "count": len(docs),
                        "lines": sum(x["lines"] for x in docs)})
    index = {
        "schema_version": "1.0.0",
        "source": ARCHIVE_ROOT,
        "built_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "stats": {
            "domains": len(domains),
            "docs": total_docs,
            "lines": total_lines,
            "dna_coverage": f"{dna_ok}/{total_docs}",
        },
        "domains": domains,
    }
    os.makedirs(ARCHIVE_ROOT, exist_ok=True)
    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    return index


def build_roster() -> str:
    """花名册数据库备份 → 字段结构表（Markdown）"""
    if not os.path.exists(ROSTER_SOURCE):
        return "⏭️ 花名册备份不存在，跳过"
    with open(ROSTER_SOURCE, encoding="utf-8") as f:
        d = json.load(f)
    props = d.get("properties", {})
    lines = [
        "# 🐉 龍芯家族花名册 · 数据库结构（Notion 备份转表）",
        "",
        f"> 源: `archive/backups_cp/` · 数据库标题: {d.get('title',[{}])[0].get('plain_text','?') if d.get('title') else '?'}",
        f"> 字段总数: {len(props)} · 对象: {d.get('object')} · 转表时间: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "| 字段 | 类型 | 字段 | 类型 |",
        "|:---|:---:|:---|:---:|",
    ]
    items = list(props.items())
    for i in range(0, len(items), 2):
        a = items[i]
        b = items[i + 1] if i + 1 < len(items) else ("", "")
        lines.append(f"| {a[0]} | {a[1].get('type','?')} | {b[0]} | {b[1].get('type','?') if b[1] else ''} |")
    md = "\n".join(lines) + "\n"
    os.makedirs(ARCHIVE_ROOT, exist_ok=True)
    with open(OUTPUT_ROSTER, "w", encoding="utf-8") as f:
        f.write(md)
    return f"🔵 花名册结构已转表: {OUTPUT_ROSTER} ({len(props)} 字段)"


def main():
    if "--roster" in sys.argv:
        print(build_roster())
        return
    index = build()
    s = index["stats"]
    print(f"🔵 Notion 备份索引已构建: {OUTPUT_INDEX}")
    print(f"   域 {s['domains']} · 文档 {s['docs']} · 行 {s['lines']} · DNA 覆盖 {s['dna_coverage']}")
    print(build_roster())
    if "--json" not in sys.argv:
        for dom in index["domains"]:
            print(f"   ├─ {dom['domain']}: {dom['count']}文档 {dom['lines']}行")
    if "--domain" in sys.argv:
        target = sys.argv[sys.argv.index("--domain") + 1]
        for dom in index["domains"]:
            if dom["domain"] == target:
                for x in dom["docs"]:
                    print(f"      {x['title']} | {x['lines']}行 | {x['dna'][:30] or '缺DNA'}")


if __name__ == "__main__":
    main()
