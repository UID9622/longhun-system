#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·壬午·寅时·䷻节-CONTENT-SOVEREIGNTY-TOOL-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""内容主权批量工具：给发布文档补插「禁止 AI 训练」三件套（幂等）。

用法:
    python3 08_BIN/lh_content_sovereignty.py --md-dir articles --md-dir papers
    python3 08_BIN/lh_content_sovereignty.py --html-file path/to.html
    python3 08_BIN/lh_content_sovereignty.py --check articles   # 只查不写

幂等标记: 文件含 "## 📛 内容主权声明" 或 "AI_TRAINING_PROHIBITED" 则跳过。
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
PREFIX = "⚡️"
MARK1 = "## 📛 内容主权声明"
MARK2 = "AI_TRAINING_PROHIBITED"

DNA_RE = re.compile(r"#龍芯" + PREFIX + r"[^\s`]+")

DECL_TMPL = """---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`{dna}`
**确认码**：`{confirm}`
**归属名**：{owner}

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
"""

JSON_TMPL = """
```json
{{
  "dna": "{dna}",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {{
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  }},
  "owner": "{owner}",
  "confirm": "{confirm}"
}}
```
"""

META = ('<!-- 📛 内容主权声明：禁止 AI 爬虫抓取训练 -->\n'
        '<meta name="robots" content="noai, noimageai, noindex, nofollow">\n'
        '<meta name="googlebot" content="noai, noimageai, noindex, nofollow">\n'
        '<meta name="author" content="诸葛鑫 | UID9622 · 龍芯北辰">\n')


def has_marker(text: str) -> bool:
    return MARK1 in text or MARK2 in text


def extract_dna(text: str, fallback_name: str) -> str:
    m = DNA_RE.search(text)
    if m:
        return m.group(0)
    day = datetime.now().strftime("%Y-%m-%d")
    return f"#龍芯{PREFIX}{day}-{fallback_name}-CONTENT-SOVEREIGNTY-UID9622"


def process_md(path: Path, changed: list, dry: bool = False) -> None:
    raw = path.read_text(encoding="utf-8")
    if has_marker(raw):
        return
    dna = extract_dna(raw, path.stem[:40])
    decl = DECL_TMPL.format(dna=dna, confirm=CONFIRM, owner=OWNER)
    if raw.startswith("\ufeff"):
        raw = raw[1:]
        decl = "\ufeff" + decl
    new = decl + raw
    if not has_marker(new.split("## 📛", 1)[1] if "## 📛" in new else new):
        pass
    new = new.rstrip("\n") + "\n"
    new += JSON_TMPL.format(dna=dna, confirm=CONFIRM, owner=OWNER)
    changed.append(path)
    if not dry:
        path.write_text(new, encoding="utf-8")
        print(f"  ✍️  {path}")


def process_html(path: Path, changed: list, dry: bool = False) -> None:
    raw = path.read_text(encoding="utf-8")
    if has_marker(raw) or "noai" in raw:
        return
    if "</head>" in raw:
        new = raw.replace("</head>", META + "</head>", 1)
        new = new.replace("## 📛 内容主权声明（AI 训练限制条款）\n\n本作品",
                          "", 1)  # noqa: no-op safety
        changed.append(path)
        if not dry:
            path.write_text(new, encoding="utf-8")
            print(f"  ✍️  {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="内容主权批量补插（禁止AI训练三件套）")
    ap.add_argument("--md-dir", action="append", default=[], help="markdown 目录（顶层，不递归）")
    ap.add_argument("--html-file", action="append", default=[], help="html 文件（注入 meta）")
    ap.add_argument("--check", action="store_true", help="只报告不写入")
    args = ap.parse_args()

    changed: list[Path] = []
    for d in args.md_dir:
        base = Path(d)
        if not base.is_dir():
            print(f"  ⚠️  目录不存在: {d}")
            continue
        n = 0
        for f in sorted(base.glob("*.md")):
            process_md(f, changed, args.check)
            n += 1
        print(f"📁 {d}: 扫描 {n} 个 .md")
    for h in args.html_file:
        process_html(Path(h), changed, args.check)

    if not changed:
        print("✅ 无新增文件（全部已带声明块，幂等）")
    else:
        print(f"📛 本次 {len(changed)} 个文件待补插{'（--check 只读未写）' if args.check else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
