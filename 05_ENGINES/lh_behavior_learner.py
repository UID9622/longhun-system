#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 行为学习引擎 (Behavior Learning Engine)
DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-BEHAVIOR-LEARNER-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 根据访问频率、停留时长、时间衰减动态调整文件/主题权重。
      热数据前置，冷数据自然降权，过期数据归档建议。
      鲲鹏 ARM64 原生：纯 Python + SQLite，无外部依赖。
"""

import json
import math
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / ".state" / "behavior_learner"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "behavior.sqlite"

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-BEHAVIOR-LEARNER-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

# 衰减参数：权重按半衰期 30 天指数衰减
HALFLIFE_DAYS = 30
DECAY_LAMBDA = math.log(2) / HALFLIFE_DAYS


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _days_since(ts: str) -> float:
    try:
        dt = datetime.fromisoformat(ts)
        return (datetime.now(CST) - dt).total_seconds() / 86400.0
    except Exception:
        return 9999.0


def _init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS behavior (
            item_id TEXT PRIMARY KEY,
            item_type TEXT NOT NULL,
            name TEXT NOT NULL,
            access_count INTEGER DEFAULT 0,
            total_duration INTEGER DEFAULT 0,
            last_accessed TEXT,
            raw_weight REAL DEFAULT 0.0,
            decayed_weight REAL DEFAULT 0.0,
            created_at TEXT
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_type ON behavior(item_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_weight ON behavior(decayed_weight)")
    conn.commit()
    return conn


class BehaviorLearner:
    """行为学习器：记录访问 → 更新权重 → 衰减排序"""

    def __init__(self):
        self.conn = _init_db()

    def record(
        self,
        item_id: str,
        item_type: str,
        name: str,
        duration: int = 0,
        weight_delta: float = 1.0,
    ) -> Dict[str, Any]:
        """记录一次访问行为"""
        now = now_iso()
        cursor = self.conn.execute(
            "SELECT access_count, total_duration, raw_weight, last_accessed FROM behavior WHERE item_id=?",
            (item_id,),
        )
        row = cursor.fetchone()
        if row:
            count, total_dur, raw_w, last_ts = row
            # 时间衰减：先把旧权重按时间衰减
            days = _days_since(last_ts) if last_ts else 0
            decayed_old = raw_w * math.exp(-DECAY_LAMBDA * days)
            new_raw = decayed_old + weight_delta
            new_count = count + 1
            new_dur = total_dur + max(duration, 0)
        else:
            new_raw = weight_delta
            new_count = 1
            new_dur = max(duration, 0)

        # 当前衰减权重
        decayed = new_raw  # 刚更新，衰减为 0

        self.conn.execute(
            """
            INSERT OR REPLACE INTO behavior
            (item_id, item_type, name, access_count, total_duration, last_accessed, raw_weight, decayed_weight, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM behavior WHERE item_id=?), ?))
            """,
            (
                item_id,
                item_type,
                name,
                new_count,
                new_dur,
                now,
                new_raw,
                decayed,
                item_id,
                now,
            ),
        )
        self.conn.commit()
        return {
            "item_id": item_id,
            "type": item_type,
            "name": name,
            "access_count": new_count,
            "total_duration": new_dur,
            "weight": round(new_raw, 4),
        }

    def refresh_weights(self) -> int:
        """全局刷新衰减权重，可定时任务调用"""
        cursor = self.conn.execute(
            "SELECT item_id, raw_weight, last_accessed FROM behavior"
        )
        updated = 0
        for item_id, raw_w, last_ts in cursor:
            days = _days_since(last_ts) if last_ts else 9999
            decayed = raw_w * math.exp(-DECAY_LAMBDA * days)
            self.conn.execute(
                "UPDATE behavior SET decayed_weight=? WHERE item_id=?",
                (decayed, item_id),
            )
            updated += 1
        self.conn.commit()
        return updated

    def top_items(
        self, item_type: Optional[str] = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """获取高权重项目"""
        self.refresh_weights()
        if item_type:
            cursor = self.conn.execute(
                "SELECT item_id, item_type, name, access_count, total_duration, last_accessed, decayed_weight FROM behavior WHERE item_type=? ORDER BY decayed_weight DESC LIMIT ?",
                (item_type, limit),
            )
        else:
            cursor = self.conn.execute(
                "SELECT item_id, item_type, name, access_count, total_duration, last_accessed, decayed_weight FROM behavior ORDER BY decayed_weight DESC LIMIT ?",
                (limit,),
            )
        results = []
        for row in cursor:
            results.append(
                {
                    "item_id": row[0],
                    "type": row[1],
                    "name": row[2],
                    "access_count": row[3],
                    "total_duration": row[4],
                    "last_accessed": row[5],
                    "weight": round(row[6], 4),
                }
            )
        return results

    def cold_items(self, days: int = 90, limit: int = 50) -> List[Dict[str, Any]]:
        """找出长期未访问的冷数据"""
        cursor = self.conn.execute(
            """
            SELECT item_id, item_type, name, access_count, last_accessed, decayed_weight FROM behavior
            WHERE (julianday('now') - julianday(last_accessed)) > ?
            ORDER BY decayed_weight ASC LIMIT ?
            """,
            (days, limit),
        )
        return [
            {
                "item_id": row[0],
                "type": row[1],
                "name": row[2],
                "access_count": row[3],
                "last_accessed": row[4],
                "weight": round(row[5], 4),
            }
            for row in cursor
        ]

    def recommend_from_context(
        self, recent_item_ids: List[str], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """基于最近访问做协同推荐：同类型高权重未访问"""
        if not recent_item_ids:
            return []
        types: set = set()
        for iid in recent_item_ids:
            cursor = self.conn.execute(
                "SELECT item_type FROM behavior WHERE item_id=?", (iid,)
            )
            row = cursor.fetchone()
            if row:
                types.add(row[0])

        results = []
        for t in types:
            for item in self.top_items(item_type=t, limit=limit):
                if item["item_id"] not in recent_item_ids:
                    results.append(item)
        results.sort(key=lambda x: -x["weight"])
        return results[:limit]


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂行为学习引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_record = sub.add_parser("record", help="记录访问")
    p_record.add_argument("item_id", help="项目ID")
    p_record.add_argument("--type", default="file", help="项目类型")
    p_record.add_argument("--name", default="", help="项目名称")
    p_record.add_argument("--duration", type=int, default=0, help="停留秒数")
    p_record.add_argument("--weight", type=float, default=1.0, help="权重增量")

    p_top = sub.add_parser("top", help="热数据")
    p_top.add_argument("--type", help="过滤类型")
    p_top.add_argument("--limit", type=int, default=20)

    p_cold = sub.add_parser("cold", help="冷数据归档建议")
    p_cold.add_argument("--days", type=int, default=90)
    p_cold.add_argument("--limit", type=int, default=50)

    p_refresh = sub.add_parser("refresh", help="刷新权重衰减")

    args = parser.parse_args()
    learner = BehaviorLearner()

    if args.cmd == "record":
        print(
            json.dumps(
                learner.record(
                    args.item_id,
                    args.type,
                    args.name or args.item_id,
                    args.duration,
                    args.weight,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.cmd == "top":
        print(json.dumps(learner.top_items(args.type, args.limit), ensure_ascii=False, indent=2))
    elif args.cmd == "cold":
        print(json.dumps(learner.cold_items(args.days, args.limit), ensure_ascii=False, indent=2))
    elif args.cmd == "refresh":
        n = learner.refresh_weights()
        print(f"✅ 已刷新 {n} 条权重")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
