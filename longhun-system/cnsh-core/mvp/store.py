"""
Merkle DNA 存储层
内容寻址 · SHA-256 Hash · JSON 持久化
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Optional

# 存储目录
STORE_DIR = os.path.join(os.path.dirname(__file__), "static", "pages")
os.makedirs(STORE_DIR, exist_ok=True)

# 内存缓存
_db: Dict[str, Dict] = {}


def _now() -> str:
    return datetime.now().isoformat()


def _file_path(hash_id: str) -> str:
    return os.path.join(STORE_DIR, f"{hash_id}.json")


def store(content: str, parent_id: Optional[str] = None, metadata: Optional[Dict] = None) -> str:
    """
    Merkle DNA 存储
    相同内容 = 相同 ID（内容寻址）
    """
    hash_id = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    record = {
        "id": hash_id,
        "content": content,
        "timestamp": _now(),
        "dna": "#CNSH-9622",
        "version": 1,
        "parent": parent_id,
        "children": [],
        "metadata": metadata or {},
    }

    # 如果已存在，直接返回（内容寻址特性）
    if hash_id in _db:
        return hash_id

    # 检查文件是否已存在
    fp = _file_path(hash_id)
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            _db[hash_id] = json.load(f)
        return hash_id

    # 更新父版本
    if parent_id and parent_id in _db:
        _db[parent_id]["children"].append(hash_id)
        with open(_file_path(parent_id), "w", encoding="utf-8") as f:
            json.dump(_db[parent_id], f, ensure_ascii=False, indent=2)

    _db[hash_id] = record

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    return hash_id


def load(hash_id: str) -> Optional[Dict]:
    """读取页面记录"""
    if hash_id in _db:
        return _db[hash_id]

    fp = _file_path(hash_id)
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        _db[hash_id] = data
        return data

    return None


def list_pages(limit: int = 50) -> list:
    """列出最近生成的页面"""
    files = sorted(
        [f for f in os.listdir(STORE_DIR) if f.endswith(".json")],
        key=lambda x: os.path.getmtime(os.path.join(STORE_DIR, x)),
        reverse=True,
    )
    results = []
    for f in files[:limit]:
        hid = f.replace(".json", "")
        data = load(hid)
        if data:
            results.append({
                "id": hid,
                "timestamp": data.get("timestamp"),
                "dna": data.get("dna"),
                "intent": data.get("metadata", {}).get("intent", ""),
            })
    return results
