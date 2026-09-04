#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ACADEMIC-REGISTRY-GENERATOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂学术资产登记册生成器  |  Academic Papers Registry Generator ║
║  DNA: #龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-ACADEMIC-REGISTRY-GENERATOR-v1.0       ║
║  用途: 扫描 docs/dragon-soul-open-hub/academic/ 生成论文登记册  ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


ACADEMIC_DIR = Path(__file__).parent.parent / "docs" / "dragon-soul-open-hub" / "academic"
REGISTRY_PATH = ACADEMIC_DIR / "academic_papers_registry.json"


def extract_title(file_path: Path) -> str:
    """从 Markdown 文件第一级标题提取标题"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(5000)  # 只读前 5000 字符
    except Exception:
        return file_path.stem

    # 匹配 # 标题
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # 匹配 HTML comment 中的文档标题
    match = re.search(r"文档标题[：:]\s*(.+)", content)
    if match:
        return match.group(1).strip()

    return file_path.stem


def detect_paper_type(title: str, content: str) -> str:
    """根据标题和关键词检测论文类型"""
    title_lower = title.lower()
    content_lower = content.lower()

    if "白皮书" in title or "whitepaper" in title_lower:
        return "白皮书"
    if "论文" in title or "paper" in title_lower or "hypothesis" in title_lower or "arxiv" in title_lower:
        return "学术论文"
    if "草案" in title or "draft" in title_lower:
        return "草案"
    if "哲学" in title or "思辨" in title or "思考" in title:
        return "思辨文章"

    # 内容关键词兜底
    if "abstract" in content_lower or "摘要" in content[:2000]:
        return "学术论文"

    return "技术文档"


def extract_keywords(title: str, content: str) -> List[str]:
    """提取关键词（基于标题和常见学术关键词匹配）"""
    keyword_pool = [
        "CNSH", "龍魂", "AI治理", "人工智能", "洛书", "易经", "道德经",
        "黎曼猜想", "Riemann", "太极", "三才", "五行", "数字身份",
        "创作者保护", "字体版权", "量子", "甲骨文", "IEEE", "arXiv",
        "算法", "数学", "人权", "伦理", "区块链", "数字人民币",
    ]

    text = (title + " " + content[:3000]).lower()
    found = []
    for kw in keyword_pool:
        if kw.lower() in text and kw not in found:
            found.append(kw)

    return found[:8]


def detect_language(content: str) -> str:
    """检测主要语言"""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content[:2000]))
    english_chars = len(re.findall(r"[a-zA-Z]", content[:2000]))
    return "中文" if chinese_chars >= english_chars else "英文"


def generate_paper_id(index: int) -> str:
    """生成论文ID"""
    return f"PAPER-{datetime.now().strftime('%Y%m%d')}-{index:03d}"


def generate_dna(paper_id: str) -> str:
    """生成 DNA 追溯码"""
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-ACADEMIC-REGISTRY-{paper_id}"


def scan_papers() -> Dict[str, Any]:
    """扫描学术目录并生成登记册"""
    papers = []
    skipped = []

    md_files = sorted([f for f in ACADEMIC_DIR.iterdir() if f.suffix.lower() == ".md"])

    for idx, file_path in enumerate(md_files, 1):
        # 跳过索引/总部类文件
        if "总部" in file_path.name or "hub" in file_path.name.lower() or "README" in file_path.name:
            skipped.append(file_path.name)
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            skipped.append(f"{file_path.name} (读取失败: {e})")
            continue

        title = extract_title(file_path)
        paper_type = detect_paper_type(title, content)
        keywords = extract_keywords(title, content)
        language = detect_language(content)
        paper_id = generate_paper_id(idx)

        papers.append({
            "id": paper_id,
            "title": title,
            "type": paper_type,
            "language": language,
            "source_path": str(file_path.relative_to(Path(__file__).parent.parent)),
            "filename": file_path.name,
            "keywords": keywords,
            "formulas": [],  # 后续由 formula matcher 填充
            "csdn": {
                "status": "未发布",
                "url": "",
                "published_at": "",
                "likes": 0,
                "collections": 0,
                "comments": 0,
            },
            "dna": generate_dna(paper_id),
            "created_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        })

    registry = {
        "_dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-ACADEMIC-PAPERS-REGISTRY-v1.0",
        "generated_at": datetime.now().isoformat(),
        "total": len(papers),
        "skipped": skipped,
        "papers": papers,
    }

    return registry


def save_registry(registry: Dict[str, Any]):
    """保存登记册到 JSON"""
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"✅ 登记册已保存: {REGISTRY_PATH}")
    print(f"   共登记论文: {registry['total']} 篇")
    print(f"   跳过文件: {len(registry['skipped'])} 个")


def main():
    print("🔍 扫描学术资产目录...")
    registry = scan_papers()
    save_registry(registry)

    print("\n📚 已登记论文列表:")
    for p in registry["papers"][:10]:
        print(f"  [{p['type']}] {p['title'][:50]}... ({p['language']})")
    if len(registry["papers"]) > 10:
        print(f"  ... 还有 {len(registry['papers']) - 10} 篇")


if __name__ == "__main__":
    main()
