#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
📋 龍魂·剪贴板容器 API
======================
DNA: #龍芯⚡️丙午·丙申·庚申·子时·☵坎-CLIPBOARD-VAULT-API-V1.0-P1

挂载到 sovereignty/portal API 服务，提供：
  - 列出容器中的剪贴项
  - 手动保存新剪贴项
  - 同步到本地 Neo4j 知识图谱

端点前缀: /api/clipboard-vault
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system")
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/bin")
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/05_ENGINES")

from ganzhi_dna_engine import DNA生成
from lh_clipboard_vault import list_vault, save, vault_to_kg_json

router = APIRouter(prefix="/api/clipboard-vault", tags=["clipboard-vault"])

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
VAULT_SCRIPT = PROJECT_ROOT / "08_BIN" / "lh_vault_to_kg.py"


def _dna(prefix: str) -> str:
    return DNA生成(模块=f"CLIPBOARD-VAULT-{prefix}", 动作="API", 版本="V1.0", 级别="P1")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SaveRequest(BaseModel):
    content: str = Field(..., min_length=1)
    source: str = "portal"
    topic: Optional[str] = None
    tags: Optional[List[str]] = None
    parent_dna: Optional[str] = None


class SyncResponse(BaseModel):
    ok: bool
    report: Dict[str, Any]


@router.get("/stats")
def stats():
    """容器统计。"""
    items = list_vault()
    topics: Dict[str, int] = {}
    tags: Dict[str, int] = {}
    for item in items:
        topics[item["topic"]] = topics.get(item["topic"], 0) + 1
        for t in item.get("tags", []):
            tags[t] = tags.get(t, 0) + 1
    return {
        "dna": _dna("STATS"),
        "timestamp": _now(),
        "total": len(items),
        "topics": topics,
        "tags": tags,
    }


@router.get("/items")
def items():
    """列出所有剪贴项。"""
    return {
        "dna": _dna("LIST"),
        "timestamp": _now(),
        "items": list_vault(),
    }


@router.post("/save")
def save_item(req: SaveRequest):
    """保存一条剪贴内容到容器。"""
    try:
        result = save(
            req.content,
            source=req.source,
            topic=req.topic,
            tags=req.tags,
            parent_dna=req.parent_dna,
        )
        return {
            "dna": _dna("SAVE"),
            "timestamp": _now(),
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {e}")


@router.post("/sync-to-kg")
def sync_to_kg():
    """把容器内容同步到 Neo4j 知识图谱。"""
    if not VAULT_SCRIPT.exists():
        raise HTTPException(status_code=500, detail="导入器脚本不存在")
    try:
        proc = subprocess.run(
            ["python3", str(VAULT_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
        )
        if proc.returncode != 0:
            raise HTTPException(status_code=502, detail=proc.stderr[-500:])
        # 提取 stdout 中的 JSON 对象（第一个以 { 开头的块到末尾）
        stdout = proc.stdout.strip()
        json_start = stdout.find("{")
        report: Dict[str, Any] = {}
        if json_start >= 0:
            try:
                report = json.loads(stdout[json_start:])
            except Exception:
                report = {"raw": stdout[-500:]}
        return {
            "dna": _dna("SYNC"),
            "timestamp": _now(),
            "report": report,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败: {e}")


@router.get("/kg-ready")
def kg_ready():
    """导出 KG 就绪 JSON（不写入 Neo4j）。"""
    return {
        "dna": _dna("KG-READY"),
        "timestamp": _now(),
        **vault_to_kg_json(),
    }
