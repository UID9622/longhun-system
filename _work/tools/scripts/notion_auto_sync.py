#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion→Git 自动同步脚本
DNA: #龍芯⚡️2026-05-24-NOTION-AUTO-SYNC-v1.0
UID: 9622
Purpose: 一键导出Notion所有公开页面 → Git → DNA签名

使用方法:
    python3 notion_auto_sync.py

结果:
    - ~/longhun-system/notion_sync/latest/
    - DNA签名链: notion_sync/dna_chain.jsonl
    - Git提交自动化
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

# 配置
NOTION_PAGES = {
    "DNA": "https://www.notion.so/uid9622/DNA-34d7125a9c9f81d2be91d1e3e3be34eb",
    "BAOBAO-COLLAB-v1": "https://www.notion.so/uid9622/UID9622-24618c23ac3247a19e652de6ab09f82c",
    "FLOW-DECISION-v3": "https://www.notion.so/uid9622/UID9622-3427125a9c9f80449e88f4f2170b7940",
    "AI-COLLABORATION": "https://www.notion.so/uid9622/AI-868fec34e5a24e7e829dc5851a75f6b7",
    "SYSTEMS-v1": "https://www.notion.so/uid9622/UID9622-v1-0-33d7125a9c9f81818d40de9b63c86203",
    "UNIFIED-FRAMEWORK": "https://www.notion.so/uid9622/b35faf462bc042aa9de5192520180728",
}

SYNC_DIR = Path.home() / "longhun-system" / "notion_sync"
LATEST_DIR = SYNC_DIR / "latest"
DNA_CHAIN_FILE = SYNC_DIR / "dna_chain.jsonl"

def ensure_dirs():
    """创建必要的目录"""
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ 目录就绪: {SYNC_DIR}")

def generate_dna_signature(content: str) -> str:
    """生成DNA签名"""
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d")
    dna = f"#龍芯⚡️{timestamp}-NOTION-{content_hash}"
    return dna

def save_notion_export(page_name: str, content: str):
    """保存Notion导出"""
    export_file = LATEST_DIR / f"{page_name}.md"
    export_file.write_text(content, encoding="utf-8")

    dna = generate_dna_signature(content)

    # 追加到DNA链
    dna_entry = {
        "timestamp": datetime.now().isoformat(),
        "page_name": page_name,
        "file": str(export_file),
        "dna": dna,
        "content_hash": hashlib.sha256(content.encode()).hexdigest(),
    }

    with open(DNA_CHAIN_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(dna_entry, ensure_ascii=False) + "\n")

    print(f"📄 导出: {page_name}")
    print(f"   DNA: {dna}")
    print(f"   路径: {export_file}")

def git_commit():
    """自动提交到Git"""
    os.chdir(Path.home() / "longhun-system")

    try:
        # 添加修改
        subprocess.run(["git", "add", "notion_sync/"], check=True, capture_output=True)

        # 生成提交信息
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"feat(notion): Notion自动同步 - {timestamp}\n\nDNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-NOTION-AUTO-SYNC"

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True,
            capture_output=True
        )

        print(f"✅ Git提交成功")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git操作失败: {e}")
        print("   (可能没有新改动)")

def main():
    """主流程"""
    print("=" * 60)
    print("🐉 龍魂 Notion→Git 自动同步")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}")
    print("=" * 60)

    ensure_dirs()

    print("\n📌 配置的Notion页面:")
    for name, url in NOTION_PAGES.items():
        print(f"   - {name}")
        print(f"     {url}")

    print("\n📝 手动步骤 (目前需要手动导出):")
    print("   1. 打开上面的每个Notion页面")
    print("   2. 右上角 '⋯' → 'Export' → 'Markdown & CSV'")
    print("   3. 下载后放入: ~/longhun-system/notion_sync/latest/")
    print("   4. 命名格式: DNA.md, BAOBAO-COLLAB-v1.md, 等")
    print("   5. 再次运行本脚本 (会自动检测并提交)")

    print("\n🔄 自动化部分:")
    print("   - 检测导出的markdown文件")
    print("   - 生成DNA签名")
    print("   - 记录到 dna_chain.jsonl")
    print("   - 自动Git提交")

    # 检查是否有新文件
    md_files = list(LATEST_DIR.glob("*.md"))
    if md_files:
        print(f"\n✅ 检测到 {len(md_files)} 个markdown文件")
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            page_name = md_file.stem
            save_notion_export(page_name, content)

        git_commit()
    else:
        print("\n⚠️  没有发现markdown文件")
        print("   请先导出Notion页面到: " + str(LATEST_DIR))

    print("\n" + "=" * 60)
    print("✅ 同步完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
