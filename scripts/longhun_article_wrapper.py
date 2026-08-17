#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂文章包装器 (LongHun Article Wrapper)
把用户粘贴的 raw 文章自动套入标准化模板，生成可直接发布/投喂的 MD 文件。

用法:
    python3 longhun_article_wrapper.py \
        --input raw.txt \
        --title "文章标题" \
        --subtitle "副标题" \
        --output ~/longhun-system/articles/my-article.md

DNA: #龍芯⚡️2026-07-02-ARTICLE-WRAPPER-v1.0
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


TEMPLATE_PATH = Path("~/longhun-system/templates/article_template_v1.0.md").expanduser()
ARTICLES_DIR = Path("~/longhun-system/articles").expanduser()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_short() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s[:64] or "article"


def generate_dna(date_str: str, slug: str) -> str:
    base = f"{date_str}-{slug}"
    short_hash = hashlib.sha256(base.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{date_str}-{slug}-{short_hash}"


def generate_confirm_code(title: str, date_str: str) -> str:
    base = f"CONFIRM-{title}-{date_str}"
    return hashlib.sha256(base.encode()).hexdigest()[:12].upper()


def estimate_read_time(content: str) -> int:
    # 中文字符 + 英文单词粗略估算
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    en_words = len(re.findall(r"[a-zA-Z]+", content))
    total = cn_chars + en_words
    return max(1, round(total / 300))


def wrap_article(raw: str, title: str, subtitle: str = "", series: str = "龍魂系统",
                 level: str = "中") -> str:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板不存在: {TEMPLATE_PATH}")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    date_short = now_short()
    slug = slugify(title)
    dna = generate_dna(date_short, slug)
    confirm = generate_confirm_code(title, date_short)
    filename = f"{date_short}-{slug}"
    read_time = estimate_read_time(raw)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 简单分段：把 raw 按空行分成段落，用于填充占位符
    sections = [s.strip() for s in raw.split("\n\n") if s.strip()]
    intro = sections[0] if sections else "（在此填写引言）"
    sec1 = "\n\n".join(sections[1:3]) if len(sections) > 1 else "（第一节内容）"
    sec2 = "\n\n".join(sections[3:5]) if len(sections) > 3 else "（第二节内容）"
    sec3 = "\n\n".join(sections[5:7]) if len(sections) > 5 else "（第三节内容）"
    conclusion = sections[-1] if sections else "（结论）"

    replacements = {
        "{{TITLE}}": title,
        "{{SUBTITLE}}": subtitle or f"龍魂系统 · {series}",
        "{{SERIES}}": series,
        "{{LEVEL}}": level,
        "{{READ_TIME}}": str(read_time),
        "{{DATE}}": date_short,
        "{{YYYY-MM-DD}}": today,
        "{{SLUG}}": slug,
        "{{FILENAME}}": filename,
        "{{CONFIRM_CODE}}": confirm,
        "{{INTRO}}": intro,
        "{{SECTION_1_TITLE}}": "核心问题",
        "{{SECTION_1_CONTENT}}": sec1,
        "{{SECTION_2_TITLE}}": "分析与方案",
        "{{SECTION_2_CONTENT}}": sec2,
        "{{SECTION_3_TITLE}}": "落地与验证",
        "{{SECTION_3_CONTENT}}": sec3,
        "{{CONCLUSION}}": conclusion,
        "{{ACTION_1}}": "保存本文到本地 ~/longhun-system/articles/",
        "{{ACTION_2}}": "核对 DNA 与 CONFIRM 码一致性",
        "{{ACTION_3}}": "投喂到龍魂训练池并记录审计",
    }

    # 替换模板占位符
    for k, v in replacements.items():
        template = template.replace(k, v)

    # 清理未替换的占位符（简单处理）
    template = re.sub(r"\{\{[A-Z_0-9]+\}\}", "（待补充）", template)
    return template


def main():
    parser = argparse.ArgumentParser(description="龍魂文章标准化包装器")
    parser.add_argument("--input", "-i", required=True, help="原始文章文件路径")
    parser.add_argument("--title", "-t", required=True, help="文章标题")
    parser.add_argument("--subtitle", "-s", default="", help="副标题")
    parser.add_argument("--series", default="龍魂系统", help="系列名称")
    parser.add_argument("--level", default="中", choices=["低", "中", "高"], help="阅读难度")
    parser.add_argument("--output", "-o", help="输出文件路径（默认自动生成）")
    parser.add_argument("--stdout", action="store_true", help="只输出到 stdout，不写入文件")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        print(f"❌ 输入文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw = input_path.read_text(encoding="utf-8")
    wrapped = wrap_article(raw, args.title, args.subtitle, args.series, args.level)

    if args.stdout:
        print(wrapped)
        return

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    if args.output:
        out_path = Path(args.output).expanduser()
    else:
        slug = slugify(args.title)
        out_path = ARTICLES_DIR / f"{now_short()}-{slug}.md"

    out_path.write_text(wrapped, encoding="utf-8")
    print(f"✅ 已生成: {out_path}")
    print(f"🧬 DNA: {generate_dna(now_short(), slugify(args.title))}")


if __name__ == "__main__":
    main()
