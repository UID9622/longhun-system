#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·癸亥·午时·☰乾-EVAL-PULLER-v1.0
"""
🐉 龍魂 · 测试套件自动拉取引擎 v1.0

自动从本地、Notion、GSM8K 等来源拉取测试题，去重后写入测试池。
"""

import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests


HOME = Path.home()
EVAL_DIR = HOME / ".longhun" / "eval"
SUITES_DIR = EVAL_DIR / "suites"
SOURCES_DIR = EVAL_DIR / "sources"
INDEX_FILE = EVAL_DIR / "index.json"

for d in [SUITES_DIR, SOURCES_DIR, EVAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def _dna(suffix: str = "PULL") -> str:
    h = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{suffix}-{h}-UID9622"


def _token() -> str:
    cfg = Path(__file__).resolve().parent.parent.parent / "config" / "notion_config.json"
    data = json.load(open(cfg, encoding="utf-8"))
    return data.get("notion_token") or data.get("token", "")


def _item_hash(item: Dict) -> str:
    text = item.get("question", item.get("content", "")).strip()
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _save_item(item: Dict) -> bool:
    """保存单个题目；返回是否为新题。"""
    item_id = _item_hash(item)
    path = SUITES_DIR / f"{item_id}.json"
    existed = path.exists()
    item["id"] = item_id
    item.setdefault("pulled_at", datetime.now().isoformat())
    item.setdefault("source", "unknown")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)
    return not existed


def _pull_local() -> List[Dict]:
    items = []
    # 用户本地测试池
    for f in SUITES_DIR.glob("*.json"):
        try:
            data = json.load(open(f, encoding="utf-8"))
            if isinstance(data, list):
                items.extend(data)
            elif isinstance(data, dict):
                items.append(data)
        except Exception:
            pass
    # 项目内置样例
    sample_dir = Path(__file__).resolve().parent / "sample_suites"
    for f in sample_dir.glob("*.json"):
        try:
            data = json.load(open(f, encoding="utf-8"))
            if isinstance(data, list):
                for it in data:
                    it.setdefault("source", f"sample:{f.stem}")
                items.extend(data)
            elif isinstance(data, dict):
                data.setdefault("source", f"sample:{f.stem}")
                items.append(data)
        except Exception:
            pass
    return items


def _pull_notion() -> List[Dict]:
    db_id = os.environ.get("EVAL_NOTION_DB_ID")
    if not db_id:
        return []
    headers = {
        "Authorization": f"Bearer {_token()}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    items = []
    next_cursor = None
    while True:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        r = requests.post(f"https://api.notion.com/v1/databases/{db_id}/query", headers=headers, json=payload)
        if r.status_code != 200:
            break
        data = r.json()
        for p in data.get("results", []):
            props = p.get("properties", {})
            question = ""
            for v in props.values():
                if v.get("type") == "title":
                    question = "".join(t.get("plain_text", "") for t in v.get("title", []))
                    break
            if question:
                items.append({"question": question, "source": "notion", "expected": "", "type": "open"})
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")
    return items


def _pull_gsm8k(max_items: int = 100) -> List[Dict]:
    url = "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl"
    cache = SOURCES_DIR / "gsm8k_test.jsonl"
    if not cache.exists():
        try:
            urllib.request.urlretrieve(url, str(cache))
        except Exception as e:
            print(f"    ⚠️ GSM8K 拉取失败: {e}")
            return []
    if not cache.exists():
        return []
    items = []
    with open(cache, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= max_items:
                break
            try:
                data = json.loads(line)
                items.append({
                    "question": data.get("question", ""),
                    "answer": data.get("answer", ""),
                    "expected": data.get("answer", ""),
                    "type": "math",
                    "source": "gsm8k",
                })
            except Exception:
                pass
    return items


def _pull_mmlu(max_items: int = 50) -> List[Dict]:
    samples = [
        {"question": "2 + 3 × 4 = ?", "choices": ["A. 20", "B. 14", "C. 24"], "answer": "B", "expected": "B. 14"},
        {"question": "CPU 中央处理器的英文全称是？", "choices": ["A. Central Process Unit", "B. Central Processing Unit", "C. Computer Personal Unit"], "answer": "B", "expected": "B. Central Processing Unit"},
        {"question": "下列哪个协议用于加密网页传输？", "choices": ["A. HTTP", "B. FTP", "C. HTTPS"], "answer": "C", "expected": "C. HTTPS"},
    ]
    items = []
    for s in samples[:max_items]:
        s["type"] = "mmlu"
        s["source"] = "mmlu-sample"
        items.append(s)
    return items


def pull_all() -> Dict:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🐉 开始拉取测试套件...")
    sources = {
        "local": _pull_local,
        "notion": _pull_notion,
        "gsm8k": lambda: _pull_gsm8k(),
        "mmlu": lambda: _pull_mmlu(),
    }

    total_new = 0
    total_dup = 0
    report = {"dna": _dna(), "timestamp": datetime.now().isoformat(), "sources": []}

    for name, fn in sources.items():
        try:
            raw_items = fn()
            new = 0
            for item in raw_items:
                if _save_item(item):
                    new += 1
                else:
                    total_dup += 1
            total_new += new
            report["sources"].append({"source": name, "raw": len(raw_items), "new": new, "status": "ok"})
            print(f"  ✅ {name}: 原始 {len(raw_items)} 条，新增 {new} 条")
        except Exception as e:
            report["sources"].append({"source": name, "error": str(e), "status": "failed"})
            print(f"  ❌ {name}: {e}")

    # 重建索引
    suites = []
    for f in SUITES_DIR.glob("*.json"):
        try:
            suites.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            pass
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "total": len(suites),
            "suites": suites,
        }, f, ensure_ascii=False, indent=2)

    report["total"] = len(suites)
    report["new"] = total_new
    report["duplicates"] = total_dup
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 测试池: {len(suites)} 条，本次新增 {total_new} 条，去重 {total_dup} 条")
    return report


if __name__ == "__main__":
    result = pull_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))
