#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 孤儿文件自动分类整理
按项目、主题、时间维度对 device_orphan_files 进行分类
DNA: #龍芯⚡️2026-06-26-ORPHAN-CLASSIFY-v1.0
"""

import json
import os
import re
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / "_work" / "dragon_knowledge.db"

# 主题关键词映射
TOPIC_KEYWORDS = {
    "龍魂体系": ["龍魂", "longhun", "dragon soul", "德者永生殿", "君子协议"],
    "CNSH": ["CNSH", "cnsh", "中文编程", "通心译", "中文原生"],
    "数学公式": ["数学", "公式", "数字根", "河图洛书", "太极", "五行", "八卦", "洛书"],
    "数字人": ["数字人", "曾老师", "十维呼吸", "航标灯", "人格", "锚点"],
    "AI治理": ["审计", "DNA追溯", "主权", "合规", "铁律", "熔断"],
    "金融交易": ["交易", "e-CNY", "五行决策", "数字人民币", "风险"],
    "鸿蒙/iOS": ["鸿蒙", "HarmonyOS", "iOS", "CoreData", "小艺", "SwiftUI"],
    "知识库": ["知识库", "Notion", "笔记", "文档", "markdown"],
    "工具脚本": ["script", "脚本", "工具", "launcher", "executor"],
    "配置部署": ["deploy", "docker", "kubernetes", "config", "yaml", "json"],
}


def classify_by_path(path: str) -> str:
    """根据路径判断项目"""
    p = Path(path)
    parts = p.parts
    
    # 提取项目名：/Users/zuimeidedeyihan/<project>/...
    project = "根目录"
    if len(parts) >= 4:
        project = parts[3]
    elif len(parts) >= 3:
        project = parts[2]
    
    # 特殊项目映射
    project_aliases = {
        "longhun-system": "龍魂系统",
        "longhun-system-backup-2026-06-01-bfg": "龍魂备份",
        "Downloads": "下载文件",
        "Documents": "文档",
        "Obsidian": "Obsidian笔记",
        ".kimi-code": "Kimi技能",
        ".longhun": "龍魂配置",
        "cnsh": "CNSH",
        "persona": "人格系统",
        "agents": "Agent系统",
        "tools": "工具脚本",
        "experiments": "实验项目",
        "integrations": "集成项目",
    }
    project = project_aliases.get(project, project)
    
    return project


def classify_by_topic(text: str, filename: str) -> list[Any]:
    """根据内容判断主题标签"""
    text_lower = (text + " " + filename).lower()
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                topics.append(topic)
                break
    if not topics:
        topics.append("其他")
    return topics


def get_file_time(path: str) -> dict[str, Any]:
    """获取文件时间信息"""
    try:
        stat = os.stat(path)
        mtime = datetime.fromtimestamp(stat.st_mtime)
        return {
            "modified_year": mtime.year,
            "modified_month": mtime.strftime("%Y-%m"),
            "modified_at": mtime.isoformat(),
        }
    except Exception:
        return {
            "modified_year": 0,
            "modified_month": "未知",
            "modified_at": "",
        }


def main():
    print("🐉 龍魂 · 孤儿文件自动分类整理\n")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 添加分类字段
    try:
        cur.execute("ALTER TABLE device_orphan_files ADD COLUMN project TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE device_orphan_files ADD COLUMN topics TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE device_orphan_files ADD COLUMN modified_year INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("ALTER TABLE device_orphan_files ADD COLUMN modified_month TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    
    cur.execute("SELECT entry_id, file_path, content_snippet, file_name FROM device_orphan_files WHERE project IS NULL")
    rows = cur.fetchall()
    print(f"待分类文件: {len(rows)}")
    
    project_counter = Counter()
    topic_counter = Counter()
    year_counter = Counter()
    
    for i, (entry_id, file_path, snippet, file_name) in enumerate(rows, 1):
        project = classify_by_path(file_path)
        topics = classify_by_topic(snippet or "", file_name)
        time_info = get_file_time(file_path)
        
        cur.execute("""
            UPDATE device_orphan_files 
            SET project=?, topics=?, modified_year=?, modified_month=?
            WHERE entry_id=?
        """, (
            project,
            ",".join(topics),
            time_info["modified_year"],
            time_info["modified_month"],
            entry_id,
        ))
        
        project_counter[project] += 1
        for t in topics:
            topic_counter[t] += 1
        year_counter[time_info["modified_year"]] += 1
        
        if i % 1000 == 0:
            conn.commit()
            print(f"  已分类 {i} 个文件...")
    
    conn.commit()
    conn.close()
    
    print(f"\n=== 分类完成 ===")
    print(f"项目分布 TOP10:")
    for p, cnt in project_counter.most_common(10):
        print(f"  {p}: {cnt}")
    print(f"\n主题分布 TOP10:")
    for t, cnt in topic_counter.most_common(10):
        print(f"  {t}: {cnt}")
    print(f"\n年份分布:")
    for y, cnt in sorted(year_counter.items(), reverse=True)[:10]:
        print(f"  {y}: {cnt}")


if __name__ == "__main__":
    main()
