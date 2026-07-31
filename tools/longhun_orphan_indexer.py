# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 孤儿文件全文索引构建
使用 SQLite FTS5 建立全文搜索
DNA: #龍芯⚡️2026-06-26-ORPHAN-FULLTEXT-v1.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path.home() / "_work" / "dragon_knowledge.db"


def main():
    print("🐉 龍魂 · 孤儿文件全文索引构建\n")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 检查 FTS5 支持
    try:
        cur.execute("SELECT sqlite_compileoption_used('ENABLE_FTS5')")
        has_fts5 = cur.fetchone()[0]
        if not has_fts5:
            print("⚠️ SQLite 未启用 FTS5，尝试创建 FTS4...")
    except Exception as e:
        print(f"检查 FTS5 支持时出错: {e}")
    
    # 删除旧索引
    cur.execute("DROP TABLE IF EXISTS device_orphan_fts")
    conn.commit()
    
    # 创建 FTS5 虚拟表
    try:
        cur.execute("""
            CREATE VIRTUAL TABLE device_orphan_fts USING fts5(
                entry_id,
                file_path,
                file_name,
                title,
                description,
                content_snippet,
                project,
                topics,
                tokenize = 'porter unicode61'
            )
        """)
        print("✅ FTS5 全文索引表已创建")
    except sqlite3.OperationalError as e:
        print(f"FTS5 创建失败: {e}，尝试 FTS4...")
        cur.execute("""
            CREATE VIRTUAL TABLE device_orphan_fts USING fts4(
                entry_id,
                file_path,
                file_name,
                title,
                description,
                content_snippet,
                project,
                topics,
                tokenize = porter
            )
        """)
        print("✅ FTS4 全文索引表已创建")
    
    # 导入数据
    cur.execute("""
        SELECT entry_id, file_path, file_name, title, description, content_snippet, project, topics
        FROM device_orphan_files
    """)
    rows = cur.fetchall()
    print(f"准备索引 {len(rows)} 个文件...")
    
    cur.executemany("""
        INSERT INTO device_orphan_fts (entry_id, file_path, file_name, title, description, content_snippet, project, topics)
        VALUES (?,?,?,?,?,?,?,?)
    """, rows)
    conn.commit()
    
    # 验证
    cur.execute("SELECT COUNT(*) FROM device_orphan_fts")
    indexed_count = cur.fetchone()[0]
    
    # 测试搜索
    print("\n测试搜索 '龍魂':")
    cur.execute("""
        SELECT file_name, project, topics FROM device_orphan_fts
        WHERE device_orphan_fts MATCH '龍魂'
        LIMIT 5
    """)
    for row in cur.fetchall():
        print(f"  {row[0]} [{row[1]}] ({row[2]})")
    
    print(f"\n测试搜索 'CNSH':")
    cur.execute("""
        SELECT file_name, project, topics FROM device_orphan_fts
        WHERE device_orphan_fts MATCH 'CNSH'
        LIMIT 5
    """)
    for row in cur.fetchall():
        print(f"  {row[0]} [{row[1]}] ({row[2]})")
    
    conn.close()
    
    print(f"\n=== 全文索引完成 ===")
    print(f"索引文件数: {indexed_count}")
    print(f"数据库: {DB_PATH}")


if __name__ == "__main__":
    main()
