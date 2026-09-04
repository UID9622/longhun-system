#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 记忆自加载器
# ═══════════════════════════════════════════
# DNA: #龍芯⚡2026-07-06-LH-MEMORY-LOAD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
# 用途: 每次 AI 会话启动时，自动加载 brain/memories.db 全部记忆
# 运行: python3 bin/lh_memory_load.py
"""

import sqlite3
import json
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "brain" / "memories.db"


def load_all_memories():
    """加载全部记忆并按时间排序输出"""
    if not DB_PATH.exists():
        print("🔴 记忆库不存在:", DB_PATH)
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, dna, content, wuxing, persona, dr, tricolor, tags, source, created_at "
        "FROM memories ORDER BY id ASC"
    ).fetchall()
    conn.close()
    return rows


def format_memories(rows):
    """格式化输出记忆列表"""
    print(f"\n{'='*60}")
    print(f"🐉 龍魂记忆库 · 共 {len(rows)} 条 · 会话启动加载")
    print(f"{'='*60}")

    for r in rows:
        tags = json.loads(r["tags"]) if r["tags"] else []
        print(f"\n  [{r['tricolor']}] [{r['wuxing']}·dr{r['dr']}] {r['persona']}")
        print(f"  {r['content']}")
        print(f"  DNA: {r['dna']}")
        print(f"  Tags: {', '.join(tags)} | {r['created_at']}")

    print(f"\n{'='*60}")
    print(f"🐉 焊死记忆已加载，本会话执行受以上约束。")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    rows = load_all_memories()
    if rows:
        format_memories(rows)
    else:
        print("🟡 记忆库为空，等待初始化...")
    sys.exit(0)
