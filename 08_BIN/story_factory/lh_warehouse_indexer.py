#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·午时·☰乾-WAREHOUSE-INDEXER-v1.0
"""
🐉 龍魂 · 素材仓库索引器
扫描 /Users/zuimeidedeyihan/Pictures/龍魂素材仓库，
按编码规则自动分类、生成 DNA、写入 JSON 索引。
"""

import json
import hashlib
import time
import re
from pathlib import Path
from datetime import datetime
from PIL import Image

ENGINE_ROOT = Path(__file__).resolve().parent


def load_warehouse_config() -> dict:
    cfg_file = ENGINE_ROOT / "configs" / "warehouse.json"
    with open(cfg_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_dna(code: str) -> str:
    h = hashlib.sha256(f"{code}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{code}-{h}-UID9622"


def parse_code(filename: str) -> dict:
    """从文件名解析编码。"""
    base = Path(filename).stem
    # 角色: HD-001_谢文东_成年锚点图
    char_match = re.match(r"^(HD-\d+)_(.+)$", base)
    if char_match:
        return {"type": "character", "code": char_match.group(1), "name": char_match.group(2).split("_")[0]}
    # 场景: ENV-01_东北校园
    env_match = re.match(r"^(ENV-\d+)_(.+)$", base)
    if env_match:
        return {"type": "scene", "code": env_match.group(1), "name": env_match.group(2)}
    # 道具/服装: A-01-01-001_黑色中山装, S-01-01-001_金刀_谢文东, B-S_打火机_大哥大_金链
    prop_match = re.match(r"^([A-Z](?:-\d+)?(?:-[A-Z])?(?:-\d+){0,3})_(.+)$", base)
    if prop_match:
        return {"type": "prop", "code": prop_match.group(1), "name": prop_match.group(2)}
    return {"type": "unknown", "code": base, "name": base}


def index_warehouse():
    cfg = load_warehouse_config()
    root = Path(cfg["warehouse_root"])
    if not root.exists():
        print(f"❌ 素材仓库不存在: {root}")
        return

    index = {
        "dna": generate_dna("WAREHOUSE"),
        "root": str(root),
        "scanned_at": datetime.now().isoformat(),
        "stats": {"total": 0, "characters": 0, "scenes": 0, "props": 0, "audio": 0, "unknown": 0},
        "assets": {},
    }

    for f in sorted(root.rglob("*")):
        if not f.is_file():
            continue
        suffix = f.suffix.lower()
        if suffix not in [".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".aiff", ".m4a"]:
            continue

        info = parse_code(f.name)
        code = info["code"]
        asset = {
            "filename": f.name,
            "path": str(f),
            "type": info["type"],
            "name": info["name"],
            "code": code,
            "dna": generate_dna(code),
            "size_bytes": f.stat().st_size,
            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
        }

        if suffix in [".png", ".jpg", ".jpeg", ".webp"]:
            try:
                with Image.open(f) as img:
                    asset["dimensions"] = f"{img.width}x{img.height}"
            except Exception:
                pass

        index["assets"][code] = asset
        index["stats"]["total"] += 1
        if info["type"] == "character":
            index["stats"]["characters"] += 1
        elif info["type"] == "scene":
            index["stats"]["scenes"] += 1
        elif info["type"] == "prop":
            index["stats"]["props"] += 1
        elif info["type"] == "audio":
            index["stats"]["audio"] += 1
        else:
            index["stats"]["unknown"] += 1

    index_file = ENGINE_ROOT / "configs" / "warehouse_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"✅ 素材仓库索引完成")
    print(f"🧬 仓库 DNA: {index['dna']}")
    print(f"📁 根目录: {root}")
    print(f"📊 统计: {json.dumps(index['stats'], ensure_ascii=False)}")
    print(f"📝 索引保存: {index_file}")
    return index


def main():
    index_warehouse()


if __name__ == "__main__":
    main()
