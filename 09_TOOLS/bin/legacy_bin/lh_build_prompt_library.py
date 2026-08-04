#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·Notion 提示词库构建器 v2.0 (精筛 + 三分库)
==============================================
DNA: #龍芯⚡️丙午·辛未·乙酉·NOTION-PROMPT-LIBRARY-BUILDER-v2.0
用途: 从本地 Notion 镜像重新抽取「真·可复用提示词模板」，按 AI 助手分库
      (宝宝 / 通心译 / Claude / 通用)，产出结构化 JSON + 可读 MD。

与 v1.0 区别:
  · 剔除纯 DNA 码 / 纯标题行 / 空噪片段
  · 每条标记 kind: prompt(可复用) / reference(参考架构)
  · 每条标记 assistant: 宝宝 / 通心译 / Claude / 通用
  · 产出三分库: library_baobao.json / library_tongxinyi.json / library_claude.json / library_common.json

用法:
  python3 bin/lh_build_prompt_library.py
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = ROOT / "docs" / "notion_mirror" / "pages"
OUT_DIR = ROOT / "L7_数据层" / "notion_prompt_library"

DNA = "#龍芯⚡️丙午·辛未·乙酉·NOTION-PROMPT-LIBRARY-v2.0"

# ── 助手分类关键词 (优先级从上到下) ──
ASSISTANT_RULES = [
    ("通心译", re.compile(r"通心|ETE|语义转换|CNSH翻译|翻译引擎|翻译规则|大白话.*系统指令|生活语言.*指令", re.I)),
    ("Claude", re.compile(r"Claude|系统提示词|本地Claude", re.I)),
    ("宝宝", re.compile(r"宝宝|P02|意图识别|大脑集成|执行层|Notion操作|表达代理|龍芯修复师", re.I)),
]

# ── 可复用提示词判定 (命中任一即视为 prompt) ──
PROMPT_RULES = [
    re.compile(r"你是|你是一个|system prompt|作为.{0,6}人格|调用场景|身份[:：]"),
    re.compile(r"直接执行|执行动作|模板命令|快捷指令|指令触發|指令触发|翻译规则"),
    re.compile(r"可直接给本地Claude执行|本地Claude直接调用|把老大的|自动识别|通心翻译器"),
    re.compile(r"触发词|触发关键词|触发条件|快速识别表|路由决策|调度"),
    re.compile(r"原则|铁律|核心能力|标准模板|标准人格模板|灵魂契约"),
]

# ── 噪音过滤 (命中即丢弃) ──
NOISE_RULES = [
    re.compile(r"^#龍芯⚡️[\w·-]*$"),                          # 纯 DNA 码行
    re.compile(r"^https?://\S+$"),                             # 纯 URL
    re.compile(r"^[\s·•\-—|│]+$"),                            # 纯分隔符
]


def is_noise(text: str) -> bool:
    t = text.strip()
    if len(t) < 6:
        return True
    for r in NOISE_RULES:
        if r.fullmatch(t):
            return True
    # DNA 码夹杂在长文本里 (以 #龍芯 开头且几乎全是码)
    if t.startswith("#龍芯⚡️") and len(re.sub(r"#龍芯⚡️|[\w·-]", "", t)) < 4:
        return True
    return False


def classify_assistant(text: str) -> str:
    for name, r in ASSISTANT_RULES:
        if r.search(text):
            return name
    return "通用"


def classify_kind(text: str) -> str:
    for r in PROMPT_RULES:
        if r.search(text):
            return "prompt"
    return "reference"


def split_chunks(text: str):
    """按空行/换行切分，去重，保留顺序。"""
    seen = set()
    out = []
    for raw in re.split(r"\n+", text):
        chunk = raw.strip()
        if not chunk:
            continue
        # 去掉重复 DNA 摘要尾巴 (同一页被镜像多次拼接)
        if chunk in seen:
            continue
        seen.add(chunk)
        out.append(chunk)
    return out


def main():
    if not MIRROR_DIR.exists():
        print(f"❌ 镜像目录不存在: {MIRROR_DIR}")
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pages = []
    all_prompts = []
    for f in sorted(MIRROR_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        title = d.get("title", "").strip()
        text = d.get("text", "") or ""
        if not title or len(text) < 30:
            continue

        chunks = split_chunks(text)
        page_prompts = []
        for chunk in chunks:
            if is_noise(chunk):
                continue
            assistant = classify_assistant(chunk)
            kind = classify_kind(chunk)
            entry = {
                "page_id": d.get("page_id", f.stem),
                "title": title,
                "url": d.get("url", ""),
                "category": d.get("category", "其他·跨域"),
                "assistant": assistant,
                "kind": kind,
                "content": chunk,
            }
            page_prompts.append(entry)
            all_prompts.append(entry)

        pages.append({
            "page_id": d.get("page_id", f.stem),
            "title": title,
            "url": d.get("url", ""),
            "category": d.get("category", "其他·跨域"),
            "dna": d.get("dna", ""),
            "scraped_at": d.get("scraped_at", ""),
            "text_length": len(text),
            "prompt_count": len(page_prompts),
        })

    # ── 统计 ──
    by_assistant = {}
    by_kind = {}
    for p in all_prompts:
        by_assistant[p["assistant"]] = by_assistant.get(p["assistant"], 0) + 1
        by_kind[p["kind"]] = by_kind.get(p["kind"], 0) + 1

    library = {
        "meta": {
            "dna": DNA,
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "source": "本地Notion镜像 docs/notion_mirror/pages/*.json (离线)",
            "total_pages": len(pages),
            "total_prompts": len(all_prompts),
            "by_assistant": by_assistant,
            "by_kind": by_kind,
            "schema": "每条: {page_id,title,url,category,assistant,kind,content}",
        },
        "pages": pages,
        "prompts": all_prompts,
    }

    # 真·可复用提示词 = prompt 类；reference 类归档另存，不污染提示词库
    real_prompts = [p for p in all_prompts if p["kind"] == "prompt"]
    reference_prompts = [p for p in all_prompts if p["kind"] == "reference"]

    # meta 只反映真模板（修正一致性）
    by_assistant_real = {}
    for p in real_prompts:
        by_assistant_real[p["assistant"]] = by_assistant_real.get(p["assistant"], 0) + 1

    library["prompts"] = real_prompts
    library["meta"]["total_prompts"] = len(real_prompts)
    library["meta"]["by_assistant"] = by_assistant_real
    library["meta"]["by_kind"] = {"prompt": len(real_prompts), "reference": len(reference_prompts)}
    library["meta"]["reference_archived"] = len(reference_prompts)

    (OUT_DIR / "library_v2.json").write_text(
        json.dumps(library, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # reference 归档 (原始素材，非提示词模板)
    (OUT_DIR / "library_reference.json").write_text(
        json.dumps({
            "meta": {"dna": DNA, "count": len(reference_prompts),
                     "note": "原始页面正文片段·非可复用提示词模板·归档备查"},
            "prompts": reference_prompts,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ── 三分库 (+通用)，仅装 prompt 类真模板 ──
    assistants = ["宝宝", "通心译", "Claude", "通用"]
    split_files = {}
    for a in assistants:
        sub = [p for p in real_prompts if p["assistant"] == a]
        fname = f"library_{'common' if a == '通用' else a}.json"
        payload = {
            "meta": {
                "assistant": a,
                "dna": DNA,
                "built_at": library["meta"]["built_at"],
                "count": len(sub),
                "note": "真·可复用提示词模板 (kind=prompt)",
            },
            "prompts": sub,
        }
        (OUT_DIR / fname).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        split_files[a] = (fname, len(sub))

    # ── 可读 MD (按助手分组) ──
    md = build_markdown(library, assistants, split_files)
    (OUT_DIR / "可复用提示词汇编_v2.md").write_text(md, encoding="utf-8")

    # ── 控制台报告 ──
    by_assistant_real = {a: split_files[a][1] for a in assistants}
    print(f"✅ 提示词库 v2.0 构建完成 (精筛·只留真模板)")
    print(f"   页面: {len(pages)} | 真模板(prompt): {len(real_prompts)} | 归档(reference): {len(reference_prompts)}")
    print(f"   真模板按助手: {by_assistant_real}")
    for a in assistants:
        print(f"   · {a}: {split_files[a][1]} 条 → {split_files[a][0]}")
    print(f"   总索引: 可复用提示词汇编_v2.md / library_v2.json")


def build_markdown(library, assistants, split_files) -> str:
    L = []
    L.append("# 🐉 龍魂·可复用提示词汇编 v2.0 (精筛·三分库)\n")
    L.append(f"> 自动从 {library['meta']['total_pages']} 个 Notion 页面抽取 · 共 {library['meta']['total_prompts']} 条")
    L.append(f"> 按助手分库: 宝宝 / 通心译 / Claude / 通用\n")

    L.append("## 📊 统计\n")
    L.append("| 助手 | 条目 | 可复用(prompt) | 参考(reference) |")
    L.append("|------|:---:|:---:|:---:|")
    for a in assistants:
        sub = [p for p in library["prompts"] if p["assistant"] == a]
        np_ = sum(1 for x in sub if x["kind"] == "prompt")
        nr_ = sum(1 for x in sub if x["kind"] == "reference")
        L.append(f"| {a} | {len(sub)} | {np_} | {nr_} |")
    L.append("")

    for a in assistants:
        sub = [p for p in library["prompts"] if p["assistant"] == a]
        if not sub:
            continue
        emoji = {"宝宝": "🤖", "通心译": "🌐", "Claude": "🧠", "通用": "🐉"}[a]
        L.append(f"\n## {emoji} {a} 专属提示词库 ({len(sub)} 条)\n")
        # 按页面分组
        by_page = {}
        for p in sub:
            by_page.setdefault(p["title"], []).append(p)
        idx = 0
        for title, items in by_page.items():
            L.append(f"\n### 📄 {title}\n")
            for it in items:
                idx += 1
                tag = "▶ 提示词" if it["kind"] == "prompt" else "· 参考"
                L.append(f"{tag} #{idx} `[{it['kind']}]`\n")
                L.append(it["content"])
                L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
