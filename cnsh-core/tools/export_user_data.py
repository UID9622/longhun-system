#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户数据一键导出

DNA:#龍芯⚡️2026-06-21-USER-DATA-EXPORT-v1.0

原则：
  - 人民数据属于人民，一键导出，无感赋能。
  - 不卡壳、不收费、格式开放。

用法：
  python export_user_data.py <用户ID>
  python export_user_data.py UID9622
"""

import sys
import os
import json
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def longhun_home() -> Path:
    return Path(os.path.expanduser("~/longhun-system"))


def collect_data(user_id: str) -> dict:
    """收集与用户相关的数据"""
    home = longhun_home()
    data = {
        "user_id": user_id,
        "export_time": datetime.now().isoformat(),
        "system": "longhun-system",
        "dna_registry_entries": [],
        "founder_trips": {},
        "people_rights_oaths": {},
        "execution_logs": [],
    }

    # 1. DNA 注册表中该用户创建或相关的文件
    registry_path = home / ".longhun" / "dna-audit" / "dna_registry.json"
    if registry_path.exists():
        try:
            reg = json.loads(registry_path.read_text(encoding='utf-8'))
            for entry in reg.get("entries", []):
                # 简单规则：模块名或 DNA 中含 UID 或用户名的视为相关
                if user_id in entry.get("dna", "") or user_id in entry.get("file", ""):
                    data["dna_registry_entries"].append(entry)
        except Exception:
            pass

    # 2. 创始人行程
    trips_path = home / ".longhun" / "founder_trips.json"
    if trips_path.exists():
        try:
            data["founder_trips"] = json.loads(trips_path.read_text(encoding='utf-8'))
        except Exception:
            pass

    # 3. 人民权益宣誓档案
    oaths_path = home / ".longhun" / "people_rights_oaths.json"
    if oaths_path.exists():
        try:
            data["people_rights_oaths"] = json.loads(oaths_path.read_text(encoding='utf-8'))
        except Exception:
            pass

    # 4. 执行日志
    log_path = Path(os.path.expanduser("~/.longhun/router-logs/execution.jsonl"))
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    if record.get("executor_uid") == user_id:
                        data["execution_logs"].append(record)
        except Exception:
            pass

    return data


def export_json(data: dict, output_dir: Path) -> Path:
    path = output_dir / f"user_data_{data['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return path


def export_csv_summary(data: dict, output_dir: Path) -> Path:
    path = output_dir / f"user_data_summary_{data['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    rows = [
        ["类别", "数量", "说明"],
        ["DNA注册条目", len(data["dna_registry_entries"]), "与你有DNA关联的文件"],
        ["创始人行程", len(data["founder_trips"]), "你报备的行程"],
        ["人民权益宣誓", len(data["people_rights_oaths"]), "已审查的服务商"],
        ["执行日志", len(data["execution_logs"]), "你的操作记录"],
    ]
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return path


def main():
    if len(sys.argv) < 2:
        print("🐉 用户数据一键导出")
        print("  用法: python export_user_data.py <用户ID>")
        print("  示例: python export_user_data.py UID9622")
        sys.exit(1)

    user_id = sys.argv[1]
    output_dir = longhun_home() / ".longhun" / "user-exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🐉 正在为 {user_id} 导出数据...")
    data = collect_data(user_id)

    json_path = export_json(data, output_dir)
    csv_path = export_csv_summary(data, output_dir)

    print(f"\n✅ 导出完成")
    print(f"  JSON 全量: {json_path}")
    print(f"  CSV 摘要: {csv_path}")
    print(f"\n数据主权在你手里，随时可取、可删、可带走。")


if __name__ == "__main__":
    main()
