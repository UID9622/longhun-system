#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·DNA登记册 v1.0 — §200有痕开源DNA登记协议·CLI工具                     ║
║     DNA Registry · Append-Only · Immutable · Local Sovereignty           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·癸未·辰时-DNA-REGISTRY-CLI-v1.0                    ║
║  协议: §200 有痕开源DNA登记协议 v1.0                                         ║
║  铁律: 只追加·不删除·不修改·本地存储·主权不出                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    python3 bin/lh_dna_registry.py --recent 10
    python3 bin/lh_dna_registry.py --query "#龍芯⚡️2026-07-08"
    python3 bin/lh_dna_registry.py --stats
    python3 bin/lh_dna_registry.py --register <dna_链> --type CREATE --target <文件>
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


# ═══════════════════════════════════════════════════════════
# 路径配置
# ═══════════════════════════════════════════════════════════

项目根 = Path(__file__).parent.parent
登记册路径 = 项目根 / "L7_数据层" / "dna_registry.jsonl"
索引路径 = 项目根 / "L7_数据层" / "dna_registry_index.json"


# ═══════════════════════════════════════════════════════════
# 核心类
# ═══════════════════════════════════════════════════════════

class DNA登记册:
    """
    §200 有痕开源DNA登记册·只追加·不删除·不修改
    """

    def __init__(self, 路径: Optional[Path] = None):
        self.路径 = 路径 or 登记册路径
        self.索引路径 = 索引路径
        self._确保文件存在()

    def _确保文件存在(self):
        """确保登记册和索引文件存在"""
        self.路径.parent.mkdir(parents=True, exist_ok=True)
        if not self.路径.exists():
            self.路径.touch()
        if not self.索引路径.exists():
            self._重建索引()

    def 登记(self, dna: str, type: str = "ACTION", target: str = "", 
             source: str = "LOCAL", uid: str = "UID9622",
             parent_dna: str = "", description: str = "") -> Dict[str, Any]:
        """
        登记一条DNA记录（append-only）
        
        返回: 登记条目
        """
        条目 = {
            "dna": dna,
            "type": type.upper(),
            "target": target,
            "uid": uid,
            "timestamp": datetime.now().isoformat(),
            "parent_dna": parent_dna,
            "source": source,
            "description": description,
            "checksum": hashlib.sha256(dna.encode()).hexdigest()[:16],
            "immutable": True,
        }

        with open(self.路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(条目, ensure_ascii=False) + "\n")

        # 更新索引
        self._更新索引(条目)
        return 条目

    def _更新索引(self, 条目: Dict[str, Any]):
        """更新内存索引"""
        try:
            with open(self.索引路径, "r", encoding="utf-8") as f:
                索引 = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            索引 = {"entries": [], "by_type": {}, "by_file": {}, "count": 0}

        索引["entries"].append({
            "dna": 条目["dna"],
            "timestamp": 条目["timestamp"],
            "type": 条目["type"],
        })
        索引["by_type"][条目["type"]] = 索引["by_type"].get(条目["type"], 0) + 1
        if 条目["target"]:
            索引["by_file"][条目["target"]] = 索引["by_file"].get(条目["target"], 0) + 1
        索引["count"] = len(索引["entries"])

        with open(self.索引路径, "w", encoding="utf-8") as f:
            json.dump(索引, ensure_ascii=False, indent=2, fp=f)

    def _重建索引(self):
        """从登记册全文重建索引"""
        索引 = {"entries": [], "by_type": {}, "by_file": {}, "count": 0}

        if self.路径.exists():
            with open(self.路径, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        条目 = json.loads(line)
                        索引["entries"].append({
                            "dna": 条目["dna"],
                            "timestamp": 条目["timestamp"],
                            "type": 条目["type"],
                        })
                        索引["by_type"][条目["type"]] = 索引["by_type"].get(条目["type"], 0) + 1
                        if 条目.get("target"):
                            索引["by_file"][条目["target"]] = 索引["by_file"].get(条目["target"], 0) + 1
                    except json.JSONDecodeError:
                        continue

        索引["count"] = len(索引["entries"])
        with open(self.索引路径, "w", encoding="utf-8") as f:
            json.dump(索引, ensure_ascii=False, indent=2, fp=f)

    def 查询(self, dna_前缀: str) -> List[Dict[str, Any]]:
        """按DNA前缀查询（模糊匹配）"""
        结果 = []
        with open(self.路径, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    条目 = json.loads(line)
                    if dna_前缀 in 条目["dna"]:
                        结果.append(条目)
                except json.JSONDecodeError:
                    continue
        return 结果

    def 最近(self, n: int = 10) -> List[Dict[str, Any]]:
        """获取最近N条记录"""
        结果 = []
        with open(self.路径, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[-n:]:
            line = line.strip()
            if not line:
                continue
            try:
                结果.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return 结果

    def 按文件查询(self, 文件名: str) -> List[Dict[str, Any]]:
        """查询指定文件的所有DNA记录"""
        结果 = []
        with open(self.路径, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    条目 = json.loads(line)
                    if 文件名 in 条目.get("target", ""):
                        结果.append(条目)
                except json.JSONDecodeError:
                    continue
        return 结果

    def 统计(self) -> Dict[str, Any]:
        """登记册统计"""
        try:
            with open(self.索引路径, "r", encoding="utf-8") as f:
                索引 = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._重建索引()
            索引 = {"entries": [], "by_type": {}, "by_file": {}, "count": 0}

        # 计算时间跨度
        条目们 = 索引.get("entries", [])
        if 条目们:
            timestamps = [e["timestamp"] for e in 条目们 if "timestamp" in e]
            最早 = min(timestamps) if timestamps else "N/A"
            最新 = max(timestamps) if timestamps else "N/A"
        else:
            最早 = "N/A"
            最新 = "N/A"

        return {
            "总条目数": 索引["count"],
            "最早记录": 最早,
            "最新记录": 最新,
            "按类型分布": 索引.get("by_type", {}),
            "按文件分布(Top10)": dict(sorted(索引.get("by_file", {}).items(), key=lambda x: x[1], reverse=True)[:10]),
            "登记册路径": str(self.路径),
        }


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 DNA登记册 v1.0")
    parser.add_argument("--recent", type=int, help="查询最近N条记录")
    parser.add_argument("--query", type=str, help="按DNA前缀查询")
    parser.add_argument("--file", type=str, help="查询指定文件的所有DNA")
    parser.add_argument("--stats", action="store_true", help="统计")
    parser.add_argument("--register", type=str, help="登记DNA链")
    parser.add_argument("--type", type=str, default="ACTION", help="操作类型")
    parser.add_argument("--target", type=str, default="", help="目标文件")
    parser.add_argument("--source", type=str, default="LOCAL", help="来源")
    parser.add_argument("--desc", type=str, default="", help="描述")
    parser.add_argument("--rebuild-index", action="store_true", help="重建索引")
    args = parser.parse_args()

    册 = DNA登记册()

    if args.rebuild_index:
        册._重建索引()
        print("✅ 索引已重建")
        return

    if args.register:
        条目 = 册.登记(args.register, type=args.type, target=args.target, source=args.source, description=args.desc)
        print(f"✅ 已登记: {条目['dna']}")
        return

    if args.recent:
        结果 = 册.最近(args.recent)
        print(f"📋 最近 {len(结果)} 条记录:\n")
        for i, r in enumerate(reversed(结果), 1):
            print(f"  {i}. [{r['type']}] {r['dna'][:50]}...")
            print(f"     {r['target']} | {r['timestamp']}")
            print()
        return

    if args.query:
        结果 = 册.查询(args.query)
        print(f"🔍 查询 '{args.query}' → {len(结果)} 条:")
        for r in 结果:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        return

    if args.file:
        结果 = 册.按文件查询(args.file)
        print(f"📁 文件 '{args.file}' → {len(结果)} 条DNA记录")
        for r in 结果:
            print(f"  {r['dna']} | {r['type']} | {r['timestamp']}")
        return

    if args.stats:
        stats = 册.统计()
        print("📊 DNA登记册统计:\n")
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    # 默认: 显示统计
    stats = 册.统计()
    print("📊 DNA登记册统计:\n")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
