#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补丁：补全道德经81章场景映射表
DNA: #龍芯⚡️2026-07-05-ROUND1-PATCH-DAODEJING-SCENE-MAP-v1.0

说明：
- 读取已有的 daodejing_scene_map.json（手工精调18章）
- 读取 docs/道德经81章_龍魂系统大白话解读_完整版_v5.0.md
- 提取每章的"现代战场一句话指南"作为金句
- 从"大白話"和"核心判斷"中提取关键词
- 保留已有章节的精调关键词，缺失章节用提取内容补全
"""

import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_MD = ROOT_DIR / "docs" / "道德经81章_龍魂系统大白话解读_完整版_v5.0.md"
EXISTING_JSON = ROOT_DIR / "data" / "round1" / "daodejing_scene_map.json"
OUTPUT_JSON = ROOT_DIR / "data" / "round1" / "daodejing_scene_map.json"


def extract_chapters(text: str):
    """从 v5.0 解读文件中提取每章信息"""
    # 按 "## 第X章 · 标题" 分割
    pattern = r'##\s+第(\d+)章\s*·\s*([^\n]+)\n'
    parts = re.split(pattern, text)
    chapters = {}

    # parts[0] 是前言，之后是 num, title, content 循环
    for i in range(1, len(parts), 3):
        if i + 2 >= len(parts):
            break
        num = parts[i].strip()
        title = parts[i + 1].strip()
        content = parts[i + 2]

        # 提取现代战场一句话指南
        guide_match = re.search(r'现代战场一句话指南\s*[\n>]*\s*["\']?([^"\'\n]+)', content)
        golden = guide_match.group(1).strip() if guide_match else f"第{num}章 · {title}"

        # 提取大白話（取前100字作为关键词源）
        dhb_match = re.search(r'\|\s*大白話\s*\|\s*([^|]+)', content)
        dhb_text = dhb_match.group(1).strip()[:120] if dhb_match else ""

        # 提取核心判断里的关键词（简单取前5条判断里的动词/名词）
        judge_items = re.findall(r'\d+\.\s*\*\*?([^\n]+)', content)
        judge_text = " ".join(judge_items[:5])

        # 组合关键词源
        keyword_source = dhb_text + " " + judge_text
        # 简单提取2-4字词作为关键词（去重、去标点）
        raw_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', keyword_source)
        # 过滤常见停用词
        stop_words = {"这是", "一个", "不是", "就是", "什么", "因为", "所以", "但是", "我们", "你们", "他们", "自己", "没有", "可以", "需要", "进行", "开始", "已经", "成为", "作为", "不能", "不要", "只能", "只要", "如果", "那么"}
        keywords = []
        for w in raw_words:
            if w not in stop_words and len(w) >= 2 and w not in keywords:
                keywords.append(w)
        keywords = keywords[:8]

        # 场景标签：从标题和核心判断推断
        tags = [title]
        if any(k in keyword_source for k in ["人民", "百姓", "老百姓"]):
            tags.append("人民")
        if any(k in keyword_source for k in ["数据", "主权", "隐私", "安全"]):
            tags.append("主权")
        if any(k in keyword_source for k in ["资本", "平台", "流量", "算法", "AI"]):
            tags.append("平台")
        if any(k in keyword_source for k in ["知足", "欲望", "攀比", "贪婪"]):
            tags.append("知足")
        if any(k in keyword_source for k in ["不争", "无为", "处下", "柔弱"]):
            tags.append("不争")

        chapters[num] = {
            "keywords": keywords,
            "scene": title,
            "golden_sentence": golden,
            "tags": tags[:4]
        }

    return chapters


def main():
    print("🐉 开始补全道德经81章场景映射表\n")

    # 1. 读取已有精调映射
    with open(EXISTING_JSON, "r", encoding="utf-8") as f:
        existing = json.load(f)
    print(f"已有精调章节：{len(existing)}")

    # 2. 读取 v5.0 解读
    text = SOURCE_MD.read_text(encoding="utf-8")
    extracted = extract_chapters(text)
    print(f"从 v5.0 提取章节：{len(extracted)}")

    # 3. 合并：已有章节保留，缺失章节用提取内容补全
    merged = {}
    for i in range(1, 82):
        key = str(i)
        if key in existing:
            merged[key] = existing[key]
        elif key in extracted:
            merged[key] = extracted[key]
        else:
            merged[key] = {
                "keywords": [],
                "scene": "待补充",
                "golden_sentence": "待补充",
                "tags": []
            }

    # 4. 备份原文件
    backup = EXISTING_JSON.with_suffix(".json.bak")
    EXISTING_JSON.rename(backup)
    print(f"原文件已备份：{backup.name}")

    # 5. 写入新文件
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成完整81章映射表：{OUTPUT_JSON}")
    print(f"   精调章节保留：{len(existing)}")
    print(f"   自动补全章节：{len(merged) - len(existing)}")
    print(f"\nDNA: #龍芯⚡️2026-07-05-ROUND1-PATCH-DAODEJING-SCENE-MAP-v1.0")


if __name__ == "__main__":
    main()
