# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·民间防御样本收集器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-民间防御-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能：收集正向/负向样本，用于民间水军识别训练
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "civil_defense_samples"
POSITIVE_DIR = SAMPLE_DIR / "positive"  # 正向（星辰大海类）
NEGATIVE_DIR = SAMPLE_DIR / "negative"  # 负向（水军/打压类）
POSITIVE_DIR.mkdir(parents=True, exist_ok=True)
NEGATIVE_DIR.mkdir(parents=True, exist_ok=True)

# 星辰大海正向特征词（用于自动分类）
POSITIVE_KEYWORDS = [
    "星辰大海",
    "永不止步",
    "加油",
    "支持",
    "正能量",
    "点赞",
    "好样的",
    "厉害",
    "强",
    "牛",
    "respect",
    "致敬",
    "说得对",
    "没错",
    "真相",
    "理性",
    "客观",
    "中肯",
]

# 负向水军特征词
NEGATIVE_KEYWORDS = [
    "没用",
    "垃圾",
    "骗子",
    "呵呵",
    "就这",
    "都是假的",
    "洗地",
    "水军",
    "带节奏",
    "又不xxx",
    "一样烂",
    "两边都不是",
    "一丘之貉",
]


def auto_classify(text):
    """自动分类评论极性"""
    pos_score = sum(1 for kw in POSITIVE_KEYWORDS if kw in text)
    neg_score = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text)

    if pos_score > neg_score:
        return "positive", [kw for kw in POSITIVE_KEYWORDS if kw in text]
    elif neg_score > pos_score:
        return "negative", [kw for kw in NEGATIVE_KEYWORDS if kw in text]
    else:
        return "neutral", []


def add_sample(text, label="positive", source="未知", tags=None):
    """添加样本（正向/负向/中性）"""
    if tags is None:
        tags = []

    # 自动分类（如果未指定 label）
    if label == "auto":
        label, detected = auto_classify(text)
        tags.extend(detected)

    target_dir = POSITIVE_DIR if label == "positive" else NEGATIVE_DIR
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_text = "".join(c for c in text[:20] if c.isalnum() or c in (' ', '-', '_'))
    safe_text = safe_text.strip() or "未命名"
    filename = f"{label}_{timestamp}_{safe_text}.json"
    filepath = target_dir / filename

    record = {
        "collect_time": datetime.now().isoformat(),
        "label": label,  # "positive" / "negative" / "neutral"
        "text": text,
        "source": source,
        "tags": tags,
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-民间防御-{label[:4]}"
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"✅ 样本已添加 [{label}]: {filepath}")
    return str(filepath)


def batch_import(samples_file):
    """批量导入样本（每行JSON: {text, label?, source?, tags?}）"""
    path = Path(samples_file)
    if not path.exists():
        print(f"❌ 文件不存在: {samples_file}")
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
                add_sample(
                    text,
                    label=data.get("label", "auto"),
                    source=data.get("source", "批量导入"),
                    tags=data.get("tags", [])
                )
                count += 1
            except json.JSONDecodeError:
                # 纯文本行，自动分类
                text = line.strip()
                if text:
                    add_sample(text, label="auto", source="批量导入", tags=[])
                    count += 1

    print(f"\n✅ 批量导入完成: {count} 条样本")
    return count


def main():
    parser = argparse.ArgumentParser(description="收集民间防御样本（水军识别训练用）")
    parser.add_argument("--text", help="文本内容")
    parser.add_argument("--label", choices=["positive", "negative", "auto"],
                        default="auto", help="样本标签（默认自动分类）")
    parser.add_argument("--source", default="手动输入", help="来源")
    parser.add_argument("--tags", default="", help="标签，逗号分隔")
    parser.add_argument("--batch", help="批量导入JSONL文件路径")
    parser.add_argument("--stats", action="store_true", help="查看样本统计")
    args = parser.parse_args()

    if args.stats:
        pos = list(POSITIVE_DIR.glob("*.json"))
        neg = list(NEGATIVE_DIR.glob("*.json"))
        print(f"📊 民间防御样本统计")
        print(f"   样本目录: {SAMPLE_DIR}")
        print(f"   正向样本: {len(pos)} 条")
        print(f"   负向样本: {len(neg)} 条")
        print(f"   总计:     {len(pos) + len(neg)} 条")
        return

    if args.batch:
        batch_import(args.batch)
        return

    if not args.text:
        parser.error("需要 --text 或 --batch 参数")

    tags_list = [t.strip() for t in args.tags.split(',') if t.strip()]
    add_sample(args.text, args.label, args.source, tags_list)


if __name__ == "__main__":
    main()
