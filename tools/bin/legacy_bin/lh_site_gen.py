#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          龍魂极简站生成器 v1.0 — Markdown → 静态站点                  ║
║  DNA: #龍芯⚡️丙午·丙申·癸丑·午时·需-SITE-GEN-v1.0-A1C3F782          ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【设计理念】
- 零依赖，纯Python标准库
- 单文件生成，不创建复杂目录
- 龙魂风格：黑白红三色、中文排版、干支时间戳
- 支持Markdown子集：标题/段落/列表/代码块/表格/链接/图片

用法:
  python3 bin/lh_site_gen.py <输入目录> [-o 输出目录] [-t 标题]

输入目录结构:
  input/
    index.md          → index.html（首页）
    chapter-01.md     → chapter-01.html
    assets/           → 复制到输出目录
"""

from __future__ import annotations
import re
import os
import sys
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field


# ══════════════════════════════════════════════════════════════════
# 【一、Markdown 解析器】
# ══════════════════════════════════════════════════════════════════

@dataclass
class MDBlock:
    """Markdown块"""
    type: str = "p"         # h1/h2/h3/h4/p/code/ul/ol/table/hr/img/quote
    content: str = ""
    children: list[str] = field(default_factory=list)
    meta: dict[str, str] = field(default_factory=dict)


def parse_markdown(text: str) -> list[MDBlock]:
    """解析Markdown为块列表"""
    blocks: list[MDBlock] = []
    lines = text.split("\n")
    i = 0
    buf: list[str] = []
    in_code = False
    in_table = False
    table_lines: list[str] = []

    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith("```"):
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            if in_code:
                in_code = False
                i += 1
                continue
            else:
                lang = line.strip()[3:].strip()
                code_lines: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                blocks.append(MDBlock(type="code", content="\n".join(code_lines), meta={"lang": lang}))
                i += 1
                continue

        if in_code:
            buf.append(line)
            i += 1
            continue

        # 表格
        if line.strip().startswith("|") and not in_table:
            # 检测表格头+分隔行
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i+1].strip()):
                in_table = True
                table_lines = [line]
                i += 1
                continue
        if in_table:
            if line.strip().startswith("|"):
                table_lines.append(line)
                i += 1
                continue
            else:
                # 表格结束
                blocks.append(_parse_table(table_lines))
                table_lines = []
                in_table = False
                continue

        # 标题
        hm = re.match(r'^(#{1,4})\s+(.+)', line)
        if hm:
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            level = len(hm.group(1))
            blocks.append(MDBlock(type=f"h{level}", content=hm.group(2).strip()))
            i += 1
            continue

        # 水平线
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            blocks.append(MDBlock(type="hr"))
            i += 1
            continue

        # 图片
        img = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img:
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            blocks.append(MDBlock(type="img", meta={"alt": img.group(1), "src": img.group(2)}))
            i += 1
            continue

        # 引用
        if line.strip().startswith("> "):
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            blocks.append(MDBlock(type="quote", content="\n".join(quote_lines)))
            continue

        # 无序列表
        if re.match(r'^\s*[-*+]\s+', line):
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            li_items: list[str] = []
            while i < len(lines) and re.match(r'^\s*[-*+]\s+', lines[i]):
                li_items.append(re.sub(r'^\s*[-*+]\s+', '', lines[i]))
                i += 1
            blocks.append(MDBlock(type="ul", children=li_items))
            continue

        # 有序列表
        if re.match(r'^\s*\d+\.\s+', line):
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            ol_items: list[str] = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                ol_items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i]))
                i += 1
            blocks.append(MDBlock(type="ol", children=ol_items))
            continue

        # 空行
        if not line.strip():
            if buf:
                blocks.append(MDBlock(type="p", content="\n".join(buf)))
                buf = []
            i += 1
            continue

        # 普通段落
        buf.append(line)
        i += 1

    if buf:
        blocks.append(MDBlock(type="p", content="\n".join(buf)))
    if in_table and table_lines:
        blocks.append(_parse_table(table_lines))

    return blocks


def _parse_table(lines: list[str]) -> MDBlock:
    """解析Markdown表格"""
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:  # 跳过表头和分隔行
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return MDBlock(type="table", meta={"headers": headers, "rows": rows})


# ══════════════════════════════════════════════════════════════════
# 【二、HTML 渲染器】
# ══════════════════════════════════════════════════════════════════

_INLINE_RULES: list[tuple[str, str]] = [
    (r'\*\*(.+?)\*\*', r'<strong>\1</strong>'),           # 粗体
    (r'__(.+?)__', r'<strong>\1</strong>'),
    (r'\*(.+?)\*', r'<em>\1</em>'),                       # 斜体
    (r'_(.+?)_', r'<em>\1</em>'),
    (r'`([^`]+)`', r'<code class="inline">\1</code>'),    # 行内代码
    (r'~~(.+?)~~', r'<del>\1</del>'),                     # 删除线
    (r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>'), # 链接
]


def render_inline(text: str) -> str:
    """渲染行内格式"""
    # HTML 转义
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for pattern, replacement in _INLINE_RULES:
        text = re.sub(pattern, replacement, text)
    return text


def render_block(block: MDBlock) -> str:
    """渲染单个块为HTML"""
    if block.type in ("h1", "h2", "h3", "h4"):
        level = int(block.type[1])
        return f"<h{level}>{render_inline(block.content)}</h{level}>"
    elif block.type == "p":
        return f"<p>{render_inline(block.content)}</p>"
    elif block.type == "hr":
        return "<hr>"
    elif block.type == "quote":
        inner = render_inline(block.content).replace("\n", "<br>")
        return f"<blockquote>{inner}</blockquote>"
    elif block.type == "code":
        lang = block.meta.get("lang", "")
        lang_attr = f' class="language-{lang}"' if lang else ""
        code = block.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre{lang_attr}><code>{code}</code></pre>"
    elif block.type == "ul":
        items = "\n".join(f"<li>{render_inline(item)}</li>" for item in block.children)
        return f"<ul>\n{items}\n</ul>"
    elif block.type == "ol":
        items = "\n".join(f"<li>{render_inline(item)}</li>" for item in block.children)
        return f"<ol>\n{items}\n</ol>"
    elif block.type == "img":
        alt = block.meta.get("alt", "")
        src = block.meta.get("src", "")
        return f'<figure><img src="{src}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>'
    elif block.type == "table":
        headers = block.meta.get("headers", [])
        rows = block.meta.get("rows", [])
        th = "".join(f"<th>{render_inline(h)}</th>" for h in headers)
        trs = []
        for row in rows:
            tds = "".join(f"<td>{render_inline(c if isinstance(c, str) else '')}</td>" for c in row)
            trs.append(f"<tr>{tds}</tr>")
        return f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    return ""


# ══════════════════════════════════════════════════════════════════
# 【三、龍魂风格模板】
# ══════════════════════════════════════════════════════════════════

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="generator" content="龍魂极简站生成器 v1.0">
<meta name="dna" content="{dna}">
<title>{title}</title>
<style>
/* ══ 龍魂极简风格 v1.0 ══ */
:root {{
  --bg: #fafaf8;
  --card: #ffffff;
  --text: #1a1a1a;
  --text-secondary: #666;
  --accent: #c62828;
  --accent-light: #ffebee;
  --border: #e0e0e0;
  --code-bg: #f5f5f5;
  --font-mono: 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace;
  --radius: 8px;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif;
  font-size: 16px;
  line-height: 1.8;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}}

.container {{
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}}

/* 头部 */
.site-header {{
  text-align: center;
  padding: 3rem 0 2rem;
  border-bottom: 2px solid var(--accent);
  margin-bottom: 2.5rem;
}}

.site-header h1 {{
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--accent);
}}

.site-header .subtitle {{
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
}}

/* 导航 */
nav {{
  margin-bottom: 2.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}}

nav a {{
  padding: 0.35rem 1rem;
  border-radius: var(--radius);
  text-decoration: none;
  color: var(--text);
  background: var(--card);
  border: 1px solid var(--border);
  font-size: 0.9rem;
  transition: all 0.2s;
}}

nav a:hover, nav a.active {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}

/* 内容 */
.content h2 {{
  font-size: 1.5rem;
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}

.content h3 {{
  font-size: 1.25rem;
  margin: 2rem 0 0.75rem;
}}

.content h4 {{
  font-size: 1.1rem;
  margin: 1.5rem 0 0.5rem;
}}

.content p {{
  margin: 0.75rem 0;
  text-align: justify;
}}

.content a {{
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px dotted var(--accent);
}}

.content a:hover {{
  border-bottom-style: solid;
}}

.content strong {{
  font-weight: 700;
  color: #111;
}}

.content em {{
  font-style: italic;
  color: #444;
}}

.content blockquote {{
  margin: 1.5rem 0;
  padding: 1rem 1.5rem;
  background: #fff9f0;
  border-left: 4px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
  color: #5a4a3a;
}}

.content pre {{
  margin: 1rem 0;
  padding: 1.2rem 1.5rem;
  background: #1e1e1e;
  color: #d4d4d4;
  border-radius: var(--radius);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
}}

.content code.inline {{
  padding: 0.15rem 0.4rem;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--accent);
}}

.content pre code {{
  background: none;
  border: none;
  padding: 0;
  color: inherit;
  font-size: inherit;
}}

.content ul, .content ol {{
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}}

.content li {{
  margin: 0.3rem 0;
}}

.content table {{
  width: 100%;
  margin: 1.5rem 0;
  border-collapse: collapse;
}}

.content th, .content td {{
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border);
  text-align: left;
}}

.content th {{
  background: #f5f5f5;
  font-weight: 700;
}}

.content tr:nth-child(even) {{
  background: #fafafa;
}}

.content hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}}

.content img {{
  max-width: 100%;
  height: auto;
  border-radius: var(--radius);
}}

.content figure {{
  margin: 1.5rem 0;
  text-align: center;
}}

.content figcaption {{
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
}}

/* 页脚 */
.site-footer {{
  margin-top: 4rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-secondary);
}}

/* 响应式 */
@media (max-width: 640px) {{
  .container {{ padding: 1rem; }}
  .site-header h1 {{ font-size: 1.5rem; }}
}}

/* 打印 */
@media print {{
  body {{ background: white; }}
  .container {{ max-width: 100%; }}
}}
</style>
</head>
<body>
<div class="container">
<header class="site-header">
<h1>{title}</h1>
{subtitle_html}
</header>
{nav_html}
<main class="content">
{content}
</main>
<footer class="site-footer">
<p>由 <strong>龍魂极简站生成器</strong> v1.0 生成 · {timestamp} · DNA: {dna}</p>
</footer>
</div>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════
# 【四、站点生成器】
# ══════════════════════════════════════════════════════════════════

@dataclass
class Page:
    """站点页面"""
    path: str           # 相对路径
    url: str            # URL路径
    title: str
    content: str        # Markdown原文
    html: str = ""


class SiteGenerator:
    """极简站生成器"""

    def __init__(self, input_dir: str, output_dir: str, site_title: str = "龍魂站点"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.site_title = site_title
        self.pages: list[Page] = []
        self._dna = ""

    def _make_dna(self) -> str:
        """生成站点的DNA"""
        raw = f"{self.site_title}-{datetime.now().isoformat()}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{h.upper()}"

    def discover(self) -> None:
        """发现输入目录中的所有Markdown文件"""
        self.pages = []
        for md_file in sorted(self.input_dir.glob("**/*.md")):
            rel = md_file.relative_to(self.input_dir)
            url = str(rel.with_suffix(".html"))
            if url.endswith("index.html"):
                url = "index.html"
                # 确保根 index.html
                if str(rel.parent) != ".":
                    url = str(rel.parent) + "/index.html"

            content = md_file.read_text(encoding="utf-8")
            # 取第一个 # 标题作为页面标题，否则用文件名
            title = md_file.stem
            for line in content.split("\n"):
                m = re.match(r'^#\s+(.+)', line.strip())
                if m:
                    title = m.group(1).strip()
                    break
            self.pages.append(Page(
                path=str(rel),
                url=url,
                title=title,
                content=content,
            ))

    def build_page(self, page: Page) -> str:
        """构建单页HTML"""
        blocks = parse_markdown(page.content)
        body = "\n".join(render_block(b) for b in blocks)

        # 导航
        nav_items = []
        for p in self.pages:
            active = ' class="active"' if p.url == page.url else ""
            nav_items.append(f'<a href="{p.url}"{active}>{p.title}</a>')
        nav_html = "<nav>" + "".join(nav_items) + "</nav>" if len(self.pages) > 1 else ""

        # 副标题
        subtitle_html = ""
        if page.url == "index.html" or page.url == "":
            subtitle_html = '<p class="subtitle">龍魂极简站 · 干支时间戳 · 文化主权</p>'

        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M")
        dna = self._make_dna()

        return PAGE_TEMPLATE.format(
            title=page.title,
            subtitle_html=subtitle_html,
            nav_html=nav_html,
            content=body,
            timestamp=ts,
            dna=dna,
        )

    def build(self) -> None:
        """构建全站"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.discover()

        if not self.pages:
            print("未找到Markdown文件，生成默认首页")
            self.pages = [Page(
                path="index.md", url="index.html",
                title=self.site_title,
                content=f"# {self.site_title}\n\n欢迎访问龍魂极简站点。\n\n请将 Markdown 文件放入 `{self.input_dir}` 目录。",
            )]

        for page in self.pages:
            page.html = self.build_page(page)
            out_path = self.output_dir / page.url
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(page.html, encoding="utf-8")
            print(f"  ✅ {page.path} → {page.url}")

        # 复制 assets 目录
        assets_src = self.input_dir / "assets"
        assets_dst = self.output_dir / "assets"
        if assets_src.exists() and assets_src.is_dir():
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
            count = sum(1 for _ in assets_dst.rglob("*") if _.is_file())
            print(f"  📁 assets/ → {count} 文件已复制")

        # 创建 CNAME（如果有）
        cname_file = self.input_dir / "CNAME"
        if cname_file.exists():
            shutil.copy(cname_file, self.output_dir / "CNAME")
            print(f"  🌐 CNAME: {cname_file.read_text().strip()}")

        print(f"\n🏁 生成完成: {self.output_dir.absolute()}")
        print(f"   页面数: {len(self.pages)}")


# ══════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂极简站生成器 — Markdown → 静态站点",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_site_gen.py docs/               # 生成站点
  python3 bin/lh_site_gen.py docs/ -o public/     # 指定输出目录
  python3 bin/lh_site_gen.py docs/ -t "我的文档"   # 自定义标题
        """,
    )
    parser.add_argument("input", help="输入目录（含Markdown文件）")
    parser.add_argument("-o", "--output", default="_site", help="输出目录（默认 _site）")
    parser.add_argument("-t", "--title", default="龍魂站点", help="站点标题")

    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(f"❌ 输入目录不存在: {args.input}")
        sys.exit(1)

    gen = SiteGenerator(args.input, args.output, args.title)
    gen.build()


if __name__ == "__main__":
    main()
