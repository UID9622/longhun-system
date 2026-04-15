#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☰☰ 龍🇨🇳魂 ☷ · 数据价值挖掘器
DNA: #龍芯⚡️2026-04-08-DATA-MINING-v1.0

挖掘1.4G数据归集中的有价值内容
"""

import json
import os
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "longhun-system"
DATA_DIR = BASE / "数据归集"
OUTPUT = BASE / "数据归集" / "价值提取报告.json"

def scan_data():
    """扫描数据归集目录"""
    stats = {
        "扫描时间": datetime.now().isoformat(),
        "目录": str(DATA_DIR),
        "发现": {}
    }
    
    # 扫描各类文件
    gz_files = list((DATA_DIR / "gz解压").glob("**/*.json")) if (DATA_DIR / "gz解压").exists() else []
    log_files = list((DATA_DIR / "logs").glob("**/*.log")) if (DATA_DIR / "logs").exists() else []
    
    stats["发现"] = {
        "gz_json文件": len(gz_files),
        "log日志文件": len(log_files),
        "总价值": "待评估"
    }
    
    # 提取有价值内容
    valuable = []
    
    # 检查归集清单
    manifest = DATA_DIR / "归集清单_20260306_083733.json"
    if manifest.exists():
        try:
            with open(manifest, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stats["发现"]["ChatGPT导出"] = len([x for x in data if 'ChatGPT' in str(x)])
                valuable.append({
                    "类型": "ChatGPT历史对话",
                    "来源": "归集清单",
                    "价值": "高 - 可提取知识"
                })
        except:
            pass
    
    stats["有价值内容"] = valuable
    
    # 保存报告
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    return stats

def main():
    print("☰☰ 龍🇨🇳魂 ☷ · 数据价值挖掘器")
    print("DNA: #龍芯⚡️2026-04-08-DATA-MINING-v1.0")
    print("")
    print(f"扫描目录: {DATA_DIR}")
    print("-" * 50)
    
    stats = scan_data()
    
    print(f"\n发现:")
    for k, v in stats["发现"].items():
        print(f"  - {k}: {v}")
    
    print(f"\n有价值内容: {len(stats['有价值内容'])} 项")
    for item in stats["有价值内容"]:
        print(f"  💎 {item['类型']} - {item['价值']}")
    
    print(f"\n报告已保存: {OUTPUT}")

if __name__ == "__main__":
    main()
