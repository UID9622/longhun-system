# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-8a30b5cf
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·丙申·辛酉·午时·☰乾-WAREHOUSE-UTILS-v1.0
"""
龍魂素材仓库统一入口。
"""

import json
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent


def get_warehouse_root() -> Path:
    cfg_file = ENGINE_ROOT / "configs" / "warehouse.json"
    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return Path(cfg["warehouse_root"])


def load_index() -> dict:
    idx_file = ENGINE_ROOT / "configs" / "warehouse_index.json"
    if not idx_file.exists():
        return {"assets": {}}
    with open(idx_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _extract_code(name: str) -> str:
    """从文件名或编码中提取素材编码。"""
    base = Path(name).stem  # 去掉扩展名
    # 编码通常是下划线前的部分：ENV-02_老街雨夜, HD-001_谢文东_...
    if "_" in base:
        return base.split("_")[0]
    return base


def get_asset_path(code: str) -> Path:
    """通过编码或文件名查找素材文件路径。"""
    idx = load_index()
    # 直接查编码
    asset = idx["assets"].get(code)
    if asset:
        return Path(asset["path"])
    # 从完整文件名解析编码再查
    parsed = _extract_code(code)
    asset = idx["assets"].get(parsed)
    if asset:
        return Path(asset["path"])
    # 回退：在仓库根目录按文件名前缀匹配
    root = get_warehouse_root()
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if f.name == code or f.stem.startswith(parsed + "_") or f.stem == parsed:
            return f
    return None


def list_assets(asset_type: str = "") -> list:
    idx = load_index()
    assets = idx.get("assets", {})
    if not asset_type:
        return list(assets.values())
    return [a for a in assets.values() if a["type"] == asset_type]
