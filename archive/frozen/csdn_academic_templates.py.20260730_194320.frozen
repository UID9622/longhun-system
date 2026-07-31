#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂CSDN学术论文模板库  |  CSDN Academic Paper Templates      ║
║  DNA: #龍芯⚡️2026-06-21-CSDN-ACADEMIC-TEMPLATES-v1.0          ║
║  用途: 将龍魂学术论文转换为 CSDN 标准发布稿件                   ║
╚══════════════════════════════════════════════════════════════╝

模板特点:
  - 标准学术结构: 摘要 · 关键词 · 目录 · 正文 · 公式对照表 · 参考文献
  - 自动生成 CSDN 友好的 Markdown
  - 内嵌创作者保护声明与 DNA 追溯
  - 支持中英双语摘要
  - 支持算法/公式对照表插入
"""

import importlib
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════
# 【基础工具函数】
# ═══════════════════════════════════════════════════════════════

def generate_dna(paper_id: str) -> str:
    """生成论文 CSDN 发布 DNA"""
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CSDN-ACADEMIC-{paper_id}"


def extract_headings(content: str) -> List[tuple]:
    """提取 Markdown 标题用于生成目录"""
    headings = []
    for line in content.split("\n"):
        match = re.match(r"^(#{2,4})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            anchor = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9_-]", "", title).lower()[:30]
            headings.append((level, title, anchor))
    return headings


def generate_toc(content: str) -> str:
    """生成目录"""
    headings = extract_headings(content)
    if not headings:
        return ""

    lines = ["## 目录", ""]
    for level, title, anchor in headings:
        indent = "  " * (level - 2)
        lines.append(f"{indent}- [{title}](#{anchor})")
    lines.append("")

    return "\n".join(lines)


def load_paper_content(source_path: str, max_chars: int = 50000) -> str:
    """加载论文源文件内容"""
    path = Path(source_path)
    if not path.is_absolute():
        # 相对于项目根目录
        project_root = Path(__file__).parent.parent.parent
        path = project_root / path

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(max_chars)
    except Exception as e:
        return f"<!-- 无法加载源文件: {e} -->\n\n"


def clean_paper_content(content: str) -> str:
    """
    清理论文内容，保留核心正文但移除不适合 CSDN 的元信息
    """
    # 移除 HTML comment 中的 DNA/GPG 等元信息行（保留君子协议声明）
    lines = content.split("\n")
    cleaned = []
    in_meta_block = False

    for line in lines:
        stripped = line.strip()

        # 跳过 Notion 标准头部块
        if "║" in stripped and ("DNA" in stripped or "GPG" in stripped or "创建者" in stripped):
            continue
        if "文档标题" in stripped and "版本" in stripped:
            continue

        # 保留君子协议声明
        if "君子协议" in stripped or "君子协议" in stripped:
            cleaned.append(line)
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


# ═══════════════════════════════════════════════════════════════
# 【CSDN 学术稿件模板】
# ═══════════════════════════════════════════════════════════════

def csdn_paper_article(
    paper_id: str,
    title: str,
    paper_type: str,
    language: str,
    source_path: str,
    keywords: List[str],
    abstract: Optional[str] = None,
    author: str = "UID9622 · 龍芯北辰",
    formula_table: str = "",
    include_toc: bool = True,
    csdn_cta: bool = True,
) -> str:
    """
    生成单篇 CSDN 学术论文稿件

    参数:
        paper_id: 论文ID
        title: 论文标题
        paper_type: 论文类型
        language: 源语言
        source_path: 源文件相对路径
        keywords: 关键词列表
        abstract: 摘要（如未提供则尝试从源文件提取）
        author: 作者
        formula_table: 算法公式对照表 Markdown
        include_toc: 是否生成目录
        csdn_cta: 是否添加 CSDN 文末引导
    """
    dna = generate_dna(paper_id)

    # 加载并清理源内容
    raw_content = load_paper_content(source_path)
    content = clean_paper_content(raw_content)

    # 如果未提供摘要，尝试提取
    if abstract is None:
        abstract = extract_abstract(content, language)

    # 生成双语摘要
    abstract_section = generate_abstract_section(abstract, language)

    # 生成目录
    toc = ""
    if include_toc:
        # 目录基于清理后的内容
        toc = generate_toc(content)

    # 关键词字符串
    keyword_str = " · ".join(keywords[:8]) if keywords else "龍魂 · CNSH · AI治理"

    lines = [
        f"<!--{dna}-->",
        "<!-- 君子协议: 本文件受龍魂DNA追溯保护 · CC BY-NC-SA 4.0 -->",
        "<!-- 类型: CSDN学术论文稿件 · 自动生成 · 禁止删除DNA后转载 -->",
        "",
        f"# {title}",
        "",
        f"> **论文类型**: {paper_type}  ",
        f"> **作者**: {author}  ",
        f"> **源语言**: {language}  ",
        f"> **DNA追溯**: `{dna}`  ",
        f"> **生成时间**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
    ]

    # 摘要
    lines.append(abstract_section)
    lines.append("")

    # 关键词
    lines.extend([
        "## 关键词",
        "",
        keyword_str,
        "",
    ])

    # 目录
    if toc:
        lines.append(toc)

    # 正文
    lines.extend([
        "## 正文",
        "",
        content,
        "",
    ])

    # 公式对照表
    if formula_table:
        lines.extend([
            "---",
            "",
            formula_table,
            "",
        ])

    # 创作者保护声明
    lines.extend([
        "---",
        "",
        "## 创作者保护声明",
        "",
        "本文遵循《龍魂创作者保护协议 v1.0》：",
        "- ✅ 学习、研究、引用请保留作者署名与原文链接；",
        "- ✅ 基于本文二次创新请标注继承关系与 DNA 追溯；",
        "- ❌ 禁止删除 DNA 追溯码后声称原创；",
        "- ❌ 禁止未经授权商业售卖核心内容。",
        "",
        f"**原作者**: {author}  ",
        f"**源文件**: `{source_path}`  ",
        f"**DNA追溯**: `{dna}`",
        "",
    ])

    # CSDN 文末引导
    if csdn_cta:
        lines.extend([
            "---",
            "",
            "> 💡 **如果本文对你有启发，欢迎点赞、收藏、关注！**  ",
            "> 🐉 **更多龍魂体系内容，请访问 [龍魂开源宪章](https://blog.csdn.net/UID9622)。**  ",
            "> 📌 **转载请务必保留 DNA 追溯与作者署名。**",
            "",
        ])

    return "\n".join(lines)


def generate_abstract_section(abstract: str, language: str) -> str:
    """生成摘要区块，支持中英双语"""
    lines = ["## 摘要", "", abstract, ""]

    if language == "英文":
        lines.extend([
            "## Abstract",
            "",
            abstract,
            "",
        ])

    return "\n".join(lines)


def extract_abstract(content: str, language: str) -> str:
    """尝试从论文内容提取摘要"""
    # 尝试匹配 ## 摘要 或 ## Abstract 后的内容
    patterns = [
        r"##\s*摘要\s*\n\s*(.+?)(?=\n##|\Z)",
        r"##\s*Abstract\s*\n\s*(.+?)(?=\n##|\Z)",
        r"\*\*摘要\*\*[：:]\s*(.+?)(?=\n\n|\Z)",
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            abstract = match.group(1).strip()
            # 限制长度
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            return abstract

    # 兜底：取前 300 字
    text = re.sub(r"[#*|`\-]", "", content).strip()
    return text[:300] + "..." if len(text) > 300 else text


# ═══════════════════════════════════════════════════════════════
# 【批量生成与发布辅助】
# ═══════════════════════════════════════════════════════════════

def default_formula_table_generator(keywords: List[str]) -> str:
    """
    默认公式对照表生成器（使用 importlib 动态加载，避免包名 hyphen 问题）
    """
    try:
        module = importlib.import_module("cnsh-core.mathematics.formula_comparison_table")
        matched = module.filter_formulas_by_keywords(keywords)
        if matched:
            return module.generate_markdown_table(matched, title="本文涉及算法公式对照表")
    except Exception as e:
        print(f"[公式对照表生成] 加载失败: {e}")
    return ""


def batch_generate_csdn_articles(
    registry: Dict,
    formula_table_generator=None,
    output_dir: Optional[str] = None,
) -> List[Dict]:
    """
    批量生成 CSDN 稿件

    参数:
        registry: 论文登记册字典
        formula_table_generator: 公式对照表生成函数（可选，默认使用 formula_comparison_table）
        output_dir: 输出目录（可选）
    """
    if formula_table_generator is None:
        formula_table_generator = default_formula_table_generator

    results = []

    for paper in registry.get("papers", []):
        paper_id = paper["id"]
        title = paper["title"]
        paper_type = paper["type"]
        language = paper["language"]
        source_path = paper["source_path"]
        keywords = paper.get("keywords", [])

        # 生成公式对照表
        formula_table = ""
        if formula_table_generator:
            matched = formula_table_generator(keywords)
            if matched:
                formula_table = matched

        # 生成 CSDN 稿件
        article = csdn_paper_article(
            paper_id=paper_id,
            title=title,
            paper_type=paper_type,
            language=language,
            source_path=source_path,
            keywords=keywords,
            formula_table=formula_table,
        )

        result = {
            "id": paper_id,
            "title": title,
            "content": article,
        }

        # 保存到文件
        if output_dir:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            safe_title = re.sub(r"[^\u4e00-\u9fff\w\-]", "_", title)[:50]
            file_path = out_path / f"{paper_id}_{safe_title}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(article)
            result["file_path"] = str(file_path)

        results.append(result)

    return results


# ═══════════════════════════════════════════════════════════════
# 【演示代码】
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂CSDN学术论文模板库 — 演示                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 示例：生成单篇论文 CSDN 稿件
    article = csdn_paper_article(
        paper_id="PAPER-20260621-001",
        title="示例：龍魂权重算法与三才决策模型",
        paper_type="学术论文",
        language="中文",
        source_path="docs/dragon-soul-open-hub/academic/☯️ 太极演变算法：以文化与伦理主权为核心的人本智能（论文草案） 3187125a9c9f809db023e7bb366916c9.md",
        keywords=["龍魂", "三才", "权重", "AI治理"],
        formula_table="## 算法公式对照表\n\n| 编号 | 公式 | 世界标准 | 龍魂扩展 |\n|-----|------|---------|---------|\n| F10 | 三才权重 | S = w_T·T + w_E·E + w_H·H | 人场 ≥ 34% |\n",
    )

    print("\n【生成的 CSDN 稿件前 1500 字符】")
    print(article[:1500])
    print("\n...")
