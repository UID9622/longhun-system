#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·无为评论归档器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-无为归档-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能：将标记为"无为"的评论归档到 audit/comment_samples/vague_pressure/
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = BASE_DIR / "audit" / "comment_samples" / "vague_pressure"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# 无为模式特征词（用于自动检测）
VAGUE_PATTERNS = [
    "还行",
    "一般般",
    "就这样",
    "不太行",
    "差点意思",
    "写得还行",
    "不够深刻",
    "没什么特别的",
    "也就那样",
    "说不上来",
    "不好说",
    "一般吧",
    "还可以",
    "没啥用",
    "感觉不对",
]


def detect_vague(text):
    """检测是否包含无为/模糊压力模式"""
    hits = [p for p in VAGUE_PATTERNS if p in text]
    return len(hits) > 0, hits


def archive_comment(comment_text, source="未知", tags=None):
    """归档一条无为评论"""
    if tags is None:
        tags = []

    is_vague, detected = detect_vague(comment_text)
    if not is_vague:
        print(f"⚠️  未检测到无为模式特征词，但仍归档（显式指定）")
    else:
        print(f"🔍 检测到无为模式: {detected}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 生成简洁文件名
    safe_text = "".join(c for c in comment_text[:20] if c.isalnum() or c in (' ', '-', '_'))
    safe_text = safe_text.strip() or "未命名"
    filename = f"{timestamp}_{safe_text}.json"
    filepath = ARCHIVE_DIR / filename

    record = {
        "archive_time": datetime.now().isoformat(),
        "source": source,
        "text": comment_text,
        "tags": tags,
        "detected_patterns": detected,
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-无为归档-{source[:4] if len(source) >= 4 else source}"
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"✅ 归档完成: {filepath}")
    return str(filepath)


def batch_archive(comments_file):
    """批量导入评论（每行一条JSON）"""
    path = Path(comments_file)
    if not path.exists():
        print(f"❌ 文件不存在: {comments_file}")
        return 0

    count = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                text = data.get("text", data.get("content", ""))
                if not text:
                    continue
                is_vague, _ = detect_vague(text)
                if is_vague:
                    archive_comment(
                        text,
                        source=data.get("source", "批量导入"),
                        tags=data.get("tags", ["无为", "批量导入"])
                    )
                    count += 1
            except json.JSONDecodeError:
                print(f"⚠️  跳过非JSON行: {line[:50]}...")

    print(f"\n✅ 批量归档完成: {count} 条无为评论")
    return count


def main():
    parser = argparse.ArgumentParser(description="归档无为评论到 audit/comment_samples/vague_pressure/")
    parser.add_argument("--text", help="单条评论内容")
    parser.add_argument("--source", default="手动输入", help="来源（CSDN/微博/自动采集 等）")
    parser.add_argument("--tags", default="", help="标签，逗号分隔")
    parser.add_argument("--batch", help="批量导入JSONL文件路径")
    parser.add_argument("--stats", action="store_true", help="查看归档统计")
    args = parser.parse_args()

    if args.stats:
        files = list(ARCHIVE_DIR.glob("*.json"))
        print(f"📊 无为评论归档统计")
        print(f"   归档目录: {ARCHIVE_DIR}")
        print(f"   总条目数: {len(files)}")
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            print(f"   最近归档: {latest.name} ({datetime.fromtimestamp(latest.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})")
        return

    if args.batch:
        batch_archive(args.batch)
        return

    if not args.text:
        parser.error("需要 --text 或 --batch 参数")

    tags_list = [t.strip() for t in args.tags.split(',') if t.strip()]
    if "无为" not in tags_list:
        tags_list.append("无为")
    archive_comment(args.text, args.source, tags_list)


if __name__ == "__main__":
    main()
