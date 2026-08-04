#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 全设备孤儿文件批量导入
把血脉识别通过的文件导入 dragon_knowledge.db 和 manifest.json
DNA: #龍芯⚡️2026-06-26-DEVICE-ORPHAN-IMPORT-v1.0
"""

import hashlib
import json
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

HOME = Path.home()
DB_PATH = HOME / "_work" / "dragon_knowledge.db"
MANIFEST_PATH = HOME / "longhun-system" / "agents" / "manifest.json"
ANALYZED_JSON = Path("/tmp/longhun_device_harvester/analyzed.json")

CST = timezone(timedelta(hours=8))
DNA_SIGNATURE = "#龍芯⚡️2026-06-26-DEVICE-ORPHAN-IMPORT-v1.0"


def now_iso():
    return datetime.now(CST).isoformat()


def sha256_short(text: str, length=16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def init_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_orphan_files (
            entry_id TEXT PRIMARY KEY,
            file_path TEXT UNIQUE,
            file_name TEXT,
            file_hash TEXT UNIQUE,
            file_size INTEGER,
            module_id TEXT,
            title TEXT,
            description TEXT,
            version TEXT,
            dna_code TEXT,
            author TEXT,
            shield_level TEXT,
            bloodline INTEGER,
            content_snippet TEXT,
            imported_at TEXT
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dor_hash ON device_orphan_files(file_hash)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dor_path ON device_orphan_files(file_path)")
    conn.commit()


def load_existing_hashes(conn: sqlite3.Connection) -> set[str]:
    cursor = conn.cursor()
    existing = set()
    for table in ["ka_files", "device_orphan_files"]:
        try:
            cursor.execute(f"SELECT file_hash FROM {table}")
            existing.update(row[0] for row in cursor.fetchall())
        except sqlite3.OperationalError:
            pass
    return existing


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"version": "1.0.0", "agents": [], "dna": ""}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict[str, Any]):
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    print("🐉 龍魂 · 全设备孤儿文件批量导入\n")
    
    if not ANALYZED_JSON.exists():
        print(f"找不到分析结果: {ANALYZED_JSON}")
        return
    
    results = json.loads(ANALYZED_JSON.read_text(encoding="utf-8"))
    passed = [r for r in results if r["shield_passed"]]
    print(f"准备导入 {len(passed)} 个通过文件\n")
    
    conn = sqlite3.connect(DB_PATH)
    init_tables(conn)
    existing_hashes = load_existing_hashes(conn)
    manifest = load_manifest()
    existing_agent_ids = {a.get("id") for a in manifest.get("agents", [])}
    
    cursor = conn.cursor()
    imported = 0
    skipped = 0
    manifest_added = 0
    shield_counts = Counter()
    ext_counts = Counter()
    
    for i, r in enumerate(passed, 1):
        file_hash = r["file_hash"]
        if file_hash in existing_hashes:
            skipped += 1
            continue
        
        existing_hashes.add(file_hash)
        path = Path(r["path"])
        rel = r.get("rel_path", str(path))
        
        # 生成 entry_id
        entry_id = f"DOR-{sha256_short(rel)}-{file_hash[:8]}"
        
        cursor.execute("""
            INSERT INTO device_orphan_files 
            (entry_id, file_path, file_name, file_hash, file_size, module_id,
             title, description, version, dna_code, author, shield_level,
             bloodline, content_snippet, imported_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            entry_id,
            str(path),
            path.name,
            file_hash,
            r.get("size", 0),
            path.parent.name,
            r.get("title", path.name),
            r.get("description", "")[:300],
            r.get("version", ""),
            r.get("dna", ""),
            r.get("author", "UID9622"),
            r.get("shield_level", "YELLOW"),
            r.get("bloodline", 0),
            r.get("snippet", "")[:500],
            now_iso(),
        ))
        
        # 注册 manifest
        agent_id = f"device_orphan_{sha256_short(rel)}"
        if agent_id not in existing_agent_ids:
            agent = {
                "id": agent_id,
                "name": r.get("title", path.name),
                "file_name": rel,
                "layer": "L3",
                "type": "device_orphan_file",
                "version": r.get("version", ""),
                "description": r.get("description", "")[:150],
                "dna": r.get("dna") or DNA_SIGNATURE,
                "source": "device_harvester",
                "shield_level": r.get("shield_level", "YELLOW"),
                "bloodline": r.get("bloodline", 0),
                "registered_at": now_iso(),
            }
            manifest.setdefault("agents", []).append(agent)
            existing_agent_ids.add(agent_id)
            manifest_added += 1
        
        imported += 1
        shield_counts[r.get("shield_level", "YELLOW")] += 1
        ext_counts[path.suffix.lower()] += 1
        
        if i % 1000 == 0:
            conn.commit()
            print(f"  已导入 {imported} 个，跳过重复 {skipped}，注册 manifest {manifest_added}")
    
    conn.commit()
    
    # 升级 manifest 版本
    version = manifest.get("version", "1.0.0")
    try:
        major, minor = version.rsplit(".", 1)
        manifest["version"] = f"{major}.{int(minor) + 1}"
    except ValueError:
        manifest["version"] = "1.1.0"
    manifest["last_updated"] = now_iso()
    manifest["dna"] = f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-AGENT-MANIFEST-{manifest['version']}"
    save_manifest(manifest)
    
    conn.close()
    
    print(f"\n=== 导入完成 ===")
    print(f"通过文件: {len(passed)}")
    print(f"实际导入: {imported}")
    print(f"跳过重复: {skipped}")
    print(f"新增 manifest 条目: {manifest_added}")
    print(f"shield 分布: {dict(shield_counts)}")
    print(f"\n扩展名 TOP10:")
    for ext, cnt in ext_counts.most_common(10):
        print(f"  {ext}: {cnt}")
    print(f"\nmanifest 版本: {manifest['version']}")
    print(f"manifest agents 总数: {len(manifest['agents'])}")
    print(f"\nDNA: {DNA_SIGNATURE}")


if __name__ == "__main__":
    main()
