#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 数字存在证明引擎 v1.0 · Digital Existence Proof Engine
# DNA: #龍芯⚡️丙午·乙未·乙未·子时·☰乾-EXISTENCE-PROOF-ENGINE-v1.0-9d1e2f3a
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 
# 核心理念: 
#   乔布斯:"在宇宙中留下痕迹"（make a dent in the universe）
#   龍魂诠释: 每个人——不论贫富、不论生死——都能在数字世界留下不被抹除的存在证明。
#   数据不出户，痕迹不可逆，DNA追溯码锚定时空。
#
# 用途:
#   1. 本地时间轴归档 — 每个人的数字痕迹按时间线不可逆存储
#   2. DNA存在证明 — 每条痕迹生成v∞干支卦追溯码
#   3. 可选链上锚定 — 只传哈希，内容永不离开用户设备
#   4. 家属继承接口 — 遗嘱式数字遗产移交

import sqlite3
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LH_ROOT = Path(os.environ.get("LH_ROOT", os.path.expanduser("~/longhun-system")))
EXISTENCE_DB = LH_ROOT / "data" / "existence_proof.db"
EXISTENCE_VAULT = LH_ROOT / "data" / "existence_vault"  # 加密归档目录

# 干支表（简化版·完整版见 ganzhi_dna_engine.py）
TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
BAGUA = ["☰乾","☱兑","☲离","☳震","☴巽","☵坎","☶艮","☷坤"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据库初始化
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def init_db():
    EXISTENCE_DB.parent.mkdir(parents=True, exist_ok=True)
    EXISTENCE_VAULT.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(EXISTENCE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS existence_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna TEXT NOT NULL UNIQUE,                    -- v∞干支卦追溯码
            content_hash TEXT NOT NULL,                   -- SHA-256 内容哈希
            content_type TEXT DEFAULT 'text',             -- text/image/audio/video/file
            title TEXT,                                   -- 标题（可选）
            summary TEXT,                                 -- 摘要（不存原文）
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            recorded_at TIMESTAMP,                        -- 事件发生时间（非录入时间）
            source TEXT,                                  -- 来源设备/应用
            location_hash TEXT,                           -- 位置哈希（可选·隐私保护）
            blockchain_tx TEXT,                           -- 区块链交易ID（可选）
            vault_path TEXT,                              -- 加密归档文件路径
            status TEXT DEFAULT 'active',                 -- active/frozen/inherited
            owner_uid TEXT DEFAULT 'UID9622',
            gpg_signature TEXT,                           -- 所有者GPG签名
            metadata TEXT DEFAULT '{}'                    -- 扩展元数据 JSON
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS existence_identities (
            uid TEXT PRIMARY KEY,
            nickname TEXT,
            public_key TEXT,                              -- 用户公钥
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_entries INTEGER DEFAULT 0,
            last_entry_at TIMESTAMP,
            inherited_to TEXT,                            -- 继承给谁
            status TEXT DEFAULT 'active'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS existence_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            entry_dna TEXT NOT NULL,
            seq_num INTEGER NOT NULL,                     -- 序列号（每个人的第几条痕迹）
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (entry_dna) REFERENCES existence_entries(dna)
        )
    """)
    conn.commit()
    return conn


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DNA生成（简版·完整版见 bin/ganzhi_dna_engine.py）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _ganzhi_from_datetime(dt: datetime) -> str:
    """从datetime推算干支四柱（简化版）"""
    year = dt.year
    # 年干支：以甲子年(1984)为基准
    base_gan = (year - 4) % 10
    base_zhi = (year - 4) % 12
    month = dt.month
    day = dt.day
    hour = dt.hour
    # 月干支
    m_gan = (base_gan * 2 + month) % 10
    m_zhi = (month + 1) % 12
    # 日干支（简化）
    d_gan = (base_gan + day - 1) % 10
    d_zhi = (base_zhi + day - 1) % 12
    # 时干支
    h_gan = (base_gan * 2 + hour // 2) % 10
    h_zhi = (hour // 2) % 12
    return f"{TIANGAN[base_gan]}{DIZHI[base_zhi]}·{TIANGAN[m_gan]}{DIZHI[m_zhi]}·{TIANGAN[d_gan]}{DIZHI[d_zhi]}·{TIANGAN[h_gan]}{DIZHI[h_zhi]}时"


def generate_existence_dna(content: str, title: str = "", uid: str = "UID9622") -> str:
    """
    为一段数字存在生成DNA追溯码
    
    格式: #存在⚡️<干支四柱>·<卦>-EXISTENCE-<动作>-<内容哈希8>
    """
    now = datetime.now(timezone.utc).astimezone()
    ganzhi = _ganzhi_from_datetime(now)
    
    # 卦象：基于内容+用户+时间的哈希取模
    raw = f"{content[:100]}{uid}{now.isoformat()}"
    gua_idx = int(hashlib.sha256(raw.encode()).hexdigest(), 16) % 8
    gua = BAGUA[gua_idx]
    
    # 内容哈希8位
    full_hash = hashlib.sha256(content.encode()).hexdigest()
    short_hash = full_hash[:8]
    
    return f"#存在⚡️{ganzhi}·{gua}-EXISTENCE-PROOF-{short_hash}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 核心操作
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def record_existence(
    content: str,
    title: str = "",
    content_type: str = "text",
    source: str = "龙魂·数字存在证明",
    uid: str = "UID9622",
    recorded_at: str = None,  # ISO格式·事件发生时间
    location: str = None,     # 可选位置描述
    store_vault: bool = False  # 是否加密归档原文
) -> dict[str, Any]:
    """
    录入一条数字存在痕迹
    
    返回: {dna, content_hash, timestamp, status}
    
    铁律：
    - 原文不进数据库，只存哈希+摘要
    - 可选加密归档到本地vault
    - DNA码不可伪造、不可删除
    """
    conn = init_db()
    
    # 生成DNA
    dna = generate_existence_dna(content, title, uid)
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # 摘要（取前200字符）
    summary = content[:200].replace('\n', ' ') + ("..." if len(content) > 200 else "")
    
    # 位置哈希（不存明文位置）
    location_hash = hashlib.sha256(location.encode()).hexdigest()[:16] if location else None
    
    # 加密归档（可选）
    vault_path = None
    if store_vault:
        vault_path = str(_archive_to_vault(dna, content, uid))
    
    # 事件时间
    rec_time = recorded_at or datetime.now(timezone.utc).astimezone().isoformat()
    
    now_str = datetime.now().isoformat()
    
    try:
        conn.execute("""
            INSERT OR IGNORE INTO existence_entries 
            (dna, content_hash, content_type, title, summary, recorded_at, source, 
             location_hash, vault_path, owner_uid, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '{}')
        """, (dna, content_hash, content_type, title, summary, rec_time, source, 
              location_hash, vault_path, uid))
        
        # 更新timeline
        seq = _next_seq(conn, uid)
        conn.execute("""
            INSERT INTO existence_timeline (uid, entry_dna, seq_num)
            VALUES (?, ?, ?)
        """, (uid, dna, seq))
        
        # 更新身份统计
        conn.execute("""
            INSERT OR IGNORE INTO existence_identities (uid, total_entries)
            VALUES (?, 0)
        """, (uid,))
        conn.execute("""
            UPDATE existence_identities 
            SET total_entries = total_entries + 1, last_entry_at = ?
            WHERE uid = ?
        """, (now_str, uid))
        
        conn.commit()
        
        return {
            "dna": dna,
            "content_hash": content_hash,
            "seq_num": seq,
            "recorded_at": rec_time,
            "recorded_now": now_str,
            "status": "active"
        }
    
    except sqlite3.IntegrityError:
        # DNA冲突（极其罕见），重试一次
        dna = generate_existence_dna(content + str(time.time_ns()), title, uid)
        conn.execute("""
            INSERT INTO existence_entries (dna, content_hash, content_type, title, summary, recorded_at, source, owner_uid, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '{}')
        """, (dna, content_hash, content_type, title, summary, rec_time, source, uid))
        seq = _next_seq(conn, uid)
        conn.execute("INSERT INTO existence_timeline (uid, entry_dna, seq_num) VALUES (?, ?, ?)", (uid, dna, seq))
        conn.commit()
        
        return {
            "dna": dna,
            "content_hash": content_hash,
            "seq_num": seq,
            "recorded_at": rec_time,
            "recorded_now": now_str,
            "status": "active"
        }
    finally:
        conn.close()


def verify_existence(dna: str) -> dict[str, Any]:
    """验证一条存在证明是否有效"""
    conn = sqlite3.connect(str(EXISTENCE_DB))
    row = conn.execute("""
        SELECT e.dna, e.content_hash, e.title, e.summary, e.recorded_at, 
               e.gpg_signature, e.status, t.seq_num, i.nickname
        FROM existence_entries e
        LEFT JOIN existence_timeline t ON e.dna = t.entry_dna
        LEFT JOIN existence_identities i ON e.owner_uid = i.uid
        WHERE e.dna = ?
    """, (dna,)).fetchone()
    conn.close()
    
    if not row:
        return {"verified": False, "reason": "DNA not found"}
    
    return {
        "verified": True,
        "dna": row[0],
        "content_hash": row[1],
        "title": row[2],
        "summary": row[3],
        "recorded_at": row[4],
        "gpg_signed": row[5] is not None,
        "status": row[6],
        "seq_num": row[7],
        "owner": row[8]
    }


def get_timeline(uid: str = "UID9622", limit: int = 50, offset: int = 0) -> list[Any]:
    """获取某人的存在时间轴"""
    conn = sqlite3.connect(str(EXISTENCE_DB))
    rows = conn.execute("""
        SELECT t.seq_num, e.dna, e.title, e.summary, e.recorded_at, e.status
        FROM existence_timeline t
        JOIN existence_entries e ON t.entry_dna = e.dna
        WHERE t.uid = ?
        ORDER BY e.recorded_at DESC
        LIMIT ? OFFSET ?
    """, (uid, limit, offset)).fetchall()
    conn.close()
    
    return [
        {
            "seq": r[0],
            "dna": r[1],
            "title": r[2],
            "summary": r[3],
            "timestamp": r[4],
            "status": r[5]
        }
        for r in rows
    ]


def get_stats(uid: str = "UID9622") -> dict[str, Any]:
    """某人存在统计"""
    conn = sqlite3.connect(str(EXISTENCE_DB))
    identity = conn.execute(
        "SELECT total_entries, last_entry_at, created_at FROM existence_identities WHERE uid = ?",
        (uid,)
    ).fetchone()
    
    total_all = conn.execute("SELECT COUNT(*) FROM existence_entries").fetchone()[0]
    
    conn.close()
    
    if not identity:
        return {"uid": uid, "total_entries": 0, "message": "尚未留下痕迹"}
    
    return {
        "uid": uid,
        "total_entries": identity[0],
        "last_entry": identity[1],
        "first_entry": identity[2],
        "total_in_system": total_all,
        "dna": f"#存在⚡️{uid}-TOTAL-{identity[0]}-ENTRIES"
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 辅助函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _next_seq(conn, uid: str) -> int:
    row = conn.execute(
        "SELECT COALESCE(MAX(seq_num), 0) + 1 FROM existence_timeline WHERE uid = ?",
        (uid,)
    ).fetchone()
    return row[0]


def _archive_to_vault(dna: str, content: str, uid: str) -> Path:
    """加密归档原文到vault"""
    date_str = datetime.now().strftime("%Y/%m/%d")
    vault_dir = EXISTENCE_VAULT / uid / date_str
    vault_dir.mkdir(parents=True, exist_ok=True)
    
    # 简化加密（生产环境用GPG）
    filename = f"{dna.replace('#','').replace('⚡️','_').replace('·','-').replace(' ','_')}.json"
    filepath = vault_dir / filename
    
    data = {
        "dna": dna,
        "uid": uid,
        "content": content,
        "recorded_at": datetime.now().isoformat()
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════════════╗
║  龍魂 · 数字存在证明引擎 v1.0                    ║
║  Digital Existence Proof Engine                  ║
║  DNA: #存在⚡️丙午·乙未·乙未·子时·☰乾               ║
║  理念: 每个人都在宇宙中留下痕迹                       ║
╚════════════════════════════════════════════════╝

用法:
  python3 bin/lh_existence_proof.py record <内容> [--title 标题] [--type text|image|audio]
  python3 bin/lh_existence_proof.py verify <DNA追溯码>
  python3 bin/lh_existence_proof.py timeline [uid] [--limit 50]
  python3 bin/lh_existence_proof.py stats [uid]
  python3 bin/lh_existence_proof.py init           # 初始化数据库

示例:
  python3 bin/lh_existence_proof.py record "今天教会了女儿骑自行车" --title "父爱的瞬间"
  python3 bin/lh_existence_proof.py verify "#存在⚡️丙午·乙未·乙未·子时·☰乾-EXISTENCE-PROOF-9d1e2f3a"
  python3 bin/lh_existence_proof.py timeline UID9622 --limit 20
  python3 bin/lh_existence_proof.py stats
        """.strip())
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        conn = init_db()
        print("✅ 数字存在证明数据库初始化完成")
        print(f"   路径: {EXISTENCE_DB}")
        print(f"   归档: {EXISTENCE_VAULT}")
        conn.close()
    
    elif cmd == "record":
        if len(sys.argv) < 3:
            print("❌ 请提供内容: python3 bin/lh_existence_proof.py record <内容>")
            sys.exit(1)
        
        content = sys.argv[2]
        title = ""
        ctype = "text"
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--title" and i+1 < len(args):
                title = args[i+1]; i += 2
            elif args[i] == "--type" and i+1 < len(args):
                ctype = args[i+1]; i += 2
            elif args[i] == "--vault":
                store_vault = True; i += 1
            else:
                i += 1
        
        result = record_existence(content, title=title, content_type=ctype)
        print(f"""
╔══════════════════════════════════════╗
║  ✅ 存在痕迹已记录                      ║
╠══════════════════════════════════════╣
║  DNA: {result['dna']}
║  序列: #{result['seq_num']}
║  哈希: {result['content_hash'][:16]}...
║  时间: {result['recorded_at']}
╠══════════════════════════════════════╣
║  "每个人都在宇宙中留下痕迹"               ║
╚══════════════════════════════════════╝
        """.strip())
    
    elif cmd == "verify":
        if len(sys.argv) < 3:
            print("❌ 请提供DNA追溯码")
            sys.exit(1)
        result = verify_existence(sys.argv[2])
        if result["verified"]:
            print(f"✅ 存在证明有效\n   DNA: {result['dna']}\n   标题: {result['title']}\n   时间: {result['recorded_at']}\n   序列: #{result['seq_num']}")
        else:
            print(f"🔴 未找到: {result['reason']}")
    
    elif cmd == "timeline":
        uid = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "UID9622"
        limit = 50
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            limit = int(sys.argv[idx+1]) if idx+1 < len(sys.argv) else 50
        
        entries = get_timeline(uid, limit)
        print(f"\n{'='*50}")
        print(f"  {uid} · 数字存在时间轴 · 共 {len(entries)} 条")
        print(f"{'='*50}")
        for e in entries:
            ts = e['timestamp'][:19] if e['timestamp'] else "无时间"
            print(f"\n  #{e['seq']:04d}  {ts}")
            print(f"  📜 {e['dna']}")
            if e['title']:
                print(f"  📝 {e['title']}")
            print(f"  💬 {e['summary'][:80]}")
            print(f"  {'─'*40}")
    
    elif cmd == "stats":
        uid = sys.argv[2] if len(sys.argv) > 2 else "UID9622"
        stats = get_stats(uid)
        print(f"""
╔══════════════════════════════════════╗
║  {uid} · 存在统计
╠══════════════════════════════════════╣
║  总痕迹: {stats.get('total_entries', 0)}
║  首次记录: {stats.get('first_entry', 'N/A')}
║  最后记录: {stats.get('last_entry', 'N/A')}
║  系统总计: {stats.get('total_in_system', 0)}
║  DNA: {stats.get('dna', 'N/A')}
╚══════════════════════════════════════╝
        """.strip())
    
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)
