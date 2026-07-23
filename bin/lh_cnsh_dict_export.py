#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH标准词典 · CSV生成器
DNA: #龍芯⚡️丙午·乙未·乙未·酉时·☷坤-CNSH-DICT-CSV-GEN-v1.0
从 cnsh_standard_dictionary.json 生成 CSV 对照表
"""
import json
import csv
import sys
from pathlib import Path

DICT_PATH = Path(__file__).parent.parent / "03_知識圖譜" / "cnsh_standard_dictionary.json"
OUT_CSV = Path(__file__).parent.parent / "03_知識圖譜" / "cnsh_standard_dictionary.csv"
OUT_TSV = Path(__file__).parent.parent / "03_知識圖譜" / "cnsh_standard_dictionary.tsv"

def generate():
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data['entries']
    meta = data['meta']
    
    # 分类映射
    cat_map = {c['code']: c['name'] for c in meta['taxonomy']}
    
    # CSV (逗号分隔，Excel友好)
    rows = []
    for e in entries:
        rows.append({
            'ID': e['id'],
            '分类': cat_map.get(e['category'], e['category']),
            '英文原词': e['en'],
            '中文直译': e['cn_direct'],
            'CNSH建议命名': e['cnsh'],
            '人话解释': e['explanation'],
            '文化出处': e.get('cultural_origin', ''),
            '龍魂场景': e.get('scene', ''),
            'CNSH用法示例': e.get('cnsh_usage', ''),
            '关联术语': ', '.join(e.get('related', []))
        })
    
    # 写 CSV
    with open(OUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ CSV: {OUT_CSV} ({len(rows)} 条)")
    
    # 写 TSV (制表符分隔，方便Notion导入)
    with open(OUT_TSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ TSV: {OUT_TSV} ({len(rows)} 条)")
    
    # 按分类统计
    from collections import Counter
    cat_counts = Counter(row['分类'] for row in rows)
    print(f"\n📊 分类统计:")
    for cat, count in cat_counts.most_common():
        print(f"   {cat}: {count} 条")
    
    return rows

if __name__ == '__main__':
    generate()
