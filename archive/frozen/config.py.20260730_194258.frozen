# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-SECOND-BRAIN-CONFIG-v1.0"""
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Obsidian vault 源路径
VAULT_PATH = Path.home() / "Obsidian" / "龍魂系統"

# 第二大脑数据目录
DATA_DIR = PROJECT_ROOT / "second-brain" / "data"
CHROMA_DIR = DATA_DIR / "chroma"
DB_PATH = DATA_DIR / "second_brain.db"

# 审计日志
AUDIT_LOG = PROJECT_ROOT / "audit" / "second_brain_sync.jsonl"

# Chroma 集合
COLLECTION_NAME = "second_brain_chunks"

# 嵌入模型
EMB_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# DNA 前缀
DNA_PREFIX = "#龍芯⚡️"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
