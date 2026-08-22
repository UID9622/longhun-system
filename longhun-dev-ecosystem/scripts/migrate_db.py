# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 数据库迁移（幂等·兼容已有库）
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-MIGRATE-V2-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
用法: 在项目根目录执行  python3 scripts/migrate_db.py
说明: v2.0 新增月度主权确认金字段/表（LH-DEVELOPER-FEE-CONVENTION-v1.0.md）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text  # noqa: E402
from backend.models import engine, init_db  # noqa: E402

# 需新增的列: {表: {列: 建列SQL片段}}
_ADD_COLUMNS = {
    "developers": {
        "monthly_fee_status": "VARCHAR(20) DEFAULT 'active'",
        "last_paid_month": "VARCHAR(7)",
        "fee_arrears": "INTEGER DEFAULT 0",
        "total_contributed": "FLOAT DEFAULT 0",
        "fee_start_month": "VARCHAR(7)",
        "is_enterprise": "BOOLEAN DEFAULT 0",
    },
}


def _migrate_columns():
    """为已存在的表补齐新增列（幂等）"""
    added = []
    with engine.connect() as conn:
        for table, cols in _ADD_COLUMNS.items():
            exists = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"),
                {"n": table},
            ).fetchone()
            if not exists:
                continue
            for col, ddl in cols.items():
                has = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
                if col in [r[1] for r in has]:
                    continue
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {ddl}"))
                added.append(f"{table}.{col}")
    print(f"✅ 补齐列: {added if added else '无需补齐'}")


if __name__ == "__main__":
    init_db()  # 创建新表（payment_orders / monthly_fee_records）及缺失库
    _migrate_columns()  # 兼容已有库补齐列
    print("✅ 数据库迁移完成 (data/developers.db · v2.0 月度主权确认金)")
