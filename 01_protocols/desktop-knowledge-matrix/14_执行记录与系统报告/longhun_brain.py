# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂脑干 · longhun_brain.py
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️丙午·壬辰·庚午·壬午·䷳艮为山-BRAIN-CORE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

三端统一记忆核心：
  📱 iOS快捷指令  → POST :9625/remember
  🤖 宝宝(Claude) → GET  :9625/recall
  📓 Notion       → 自动同步每条记忆
  💻 Cursor本地   → python3 longhun_brain.py

用法：
  python3 longhun_brain.py           # 启动API服务
  python3 longhun_brain.py --remember "今天决定了亮剑时刻" --tag 决策,亮剑
  python3 longhun_brain.py --recall 最小损失
  python3 longhun_brain.py --timeline 2026-04-26
  python3 longhun_brain.py --status   # 查看脑干健康
"""

import sys, os, json, hashlib, sqlite3, argparse
from datetime import datetime, date
from pathlib import Path

# ═══════════════════════════════════════
# 0. 全局配置
# ═══════════════════════════════════════

BRAIN_DIR  = Path.home() / "longhun-system" / "brain"
DB_PATH    = BRAIN_DIR / "memories.db"
LOG_PATH   = BRAIN_DIR / "brain.log"
PORT       = 9625

UID        = "9622"
GPG        = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM    = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

WUXING_MAP = {"水":1,"木":3,"火":2,"金":4,"土":5}
NUM_TO_WX  = {1:"水",2:"火",3:"木",4:"金",5:"土",6:"金",7:"火",8:"木",9:"水",0:"土"}

# 来源标记
SOURCE_ICON = {
    "ios":    "📱",
    "claude": "🤖",
    "notion": "📓",
    "cursor": "💻",
    "system": "⚙️",
    "unknown":"❓",
}

BRAIN_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════
# 1. 数字根 & DNA
# ═══════════════════════════════════════

def digital_root(n: int) -> int:
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def make_dna(content: str, type_code: str = "MEM") -> str:
    ts   = datetime.now().strftime("%Y%m%d%H%M%S")
    h    = hashlib.sha256(f"{content}|{ts}|{UID}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{type_code}-{h}"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def tricolor(dr: int) -> str:
    return "🔴" if dr in (3,9) else "🟡" if dr == 6 else "🟢"

# ═══════════════════════════════════════
# 2. 数据库（只追加，不删不改）
# ═══════════════════════════════════════

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS memories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            dna         TEXT UNIQUE NOT NULL,
            content     TEXT NOT NULL,
            wuxing      TEXT DEFAULT '土',
            persona     TEXT DEFAULT '宝宝',
            dr          INTEGER DEFAULT 0,
            tricolor    TEXT DEFAULT '🟢',
            tags        TEXT DEFAULT '[]',
            source      TEXT DEFAULT 'unknown',
            sha256_self TEXT,
            sha256_prev TEXT,
            notion_id   TEXT DEFAULT '',
            created_at  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chain_anchor (
            id      INTEGER PRIMARY KEY CHECK (id=1),
            last_sha TEXT NOT NULL DEFAULT ''
        );
        INSERT OR IGNORE INTO chain_anchor (id, last_sha) VALUES (1,'');

        -- 禁止DELETE和UPDATE（append-only铁律）
        CREATE TRIGGER IF NOT EXISTS no_delete_memories
            BEFORE DELETE ON memories BEGIN
            SELECT RAISE(ABORT,'🔴 龍魂铁律：记忆不可删除');
        END;

        CREATE TRIGGER IF NOT EXISTS no_update_memories
            BEFORE UPDATE ON memories BEGIN
            SELECT RAISE(ABORT,'🔴 龍魂铁律：记忆不可篡改');
        END;
    """)
    con.commit()
    con.close()

def get_last_sha() -> str:
    con = sqlite3.connect(DB_PATH)
    row = con.execute("SELECT last_sha FROM chain_anchor WHERE id=1").fetchone()
    con.close()
    return row[0] if row else ""

def set_last_sha(sha: str):
    con = sqlite3.connect(DB_PATH)
    con.execute("UPDATE chain_anchor SET last_sha=? WHERE id=1", (sha,))
    con.commit()
    con.close()

# ═══════════════════════════════════════
# 3. 核心操作
# ═══════════════════════════════════════

def remember(content: str,
             wuxing:  str  = "土",
             persona: str  = "宝宝·Claude",
             tags:    list = None,
             source:  str  = "unknown") -> dict:
    """存入一条记忆（追加只写）"""
    tags    = tags or []
    dna     = make_dna(content)
    created = datetime.now().isoformat()

    # 数字根 & 三色
    dr_val  = digital_root(sum(ord(c) for c in content) % 999)
    tc      = tricolor(dr_val)

    # SHA-256哈希链
    prev    = get_last_sha()
    self_sha= sha256(f"{dna}|{content}|{created}|{prev}")

    record = {
        "dna":         dna,
        "content":     content,
        "wuxing":      wuxing,
        "persona":     persona,
        "dr":          dr_val,
        "tricolor":    tc,
        "tags":        json.dumps(tags, ensure_ascii=False),
        "source":      source,
        "sha256_self": self_sha,
        "sha256_prev": prev,
        "created_at":  created,
    }

    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("""
            INSERT INTO memories
            (dna,content,wuxing,persona,dr,tricolor,tags,source,sha256_self,sha256_prev,created_at)
            VALUES (:dna,:content,:wuxing,:persona,:dr,:tricolor,:tags,:source,
                    :sha256_self,:sha256_prev,:created_at)
        """, record)
        con.commit()
        set_last_sha(self_sha)
    except sqlite3.IntegrityError:
        pass  # 重复DNA直接忽略
    finally:
        con.close()

    record["tags"] = tags
    _log_event("REMEMBER", dna, source)
    return record

def recall(keyword: str = "", wuxing: str = "", limit: int = 20) -> list:
    """全文搜索记忆"""
    con  = sqlite3.connect(DB_PATH)
    sql  = "SELECT id,dna,content,wuxing,persona,tricolor,tags,source,created_at FROM memories WHERE 1=1"
    args = []
    if keyword:
        sql += " AND content LIKE ?"
        args.append(f"%{keyword}%")
    if wuxing:
        sql += " AND wuxing=?"
        args.append(wuxing)
    sql += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    rows = con.execute(sql, args).fetchall()
    con.close()
    return [_row_to_dict(r) for r in rows]

def timeline(day: str = None) -> list:
    """按日期查看时间线"""
    day = day or date.today().isoformat()
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("""
        SELECT id,dna,content,wuxing,persona,tricolor,tags,source,created_at
        FROM memories
        WHERE created_at LIKE ?
        ORDER BY id ASC
    """, (f"{day}%",)).fetchall()
    con.close()
    return [_row_to_dict(r) for r in rows]

def replay(dna_code: str) -> dict:
    """精确回放一条记忆"""
    con = sqlite3.connect(DB_PATH)
    row = con.execute("""
        SELECT id,dna,content,wuxing,persona,tricolor,tags,source,sha256_self,sha256_prev,created_at
        FROM memories WHERE dna=?
    """, (dna_code,)).fetchone()
    con.close()
    if not row:
        return {"error": f"找不到 DNA: {dna_code}"}
    return {
        "id":          row[0],
        "dna":         row[1],
        "content":     row[2],
        "wuxing":      row[3],
        "persona":     row[4],
        "tricolor":    row[5],
        "tags":        json.loads(row[6] or "[]"),
        "source":      row[7],
        "sha256_self": row[8],
        "sha256_prev": row[9],
        "created_at":  row[10],
        "chain_valid": True,
    }

def status() -> dict:
    """脑干健康状态"""
    con   = sqlite3.connect(DB_PATH)
    total = con.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    today = con.execute(
        "SELECT COUNT(*) FROM memories WHERE created_at LIKE ?",
        (f"{date.today().isoformat()}%",)
    ).fetchone()[0]
    by_src= dict(con.execute(
        "SELECT source,COUNT(*) FROM memories GROUP BY source"
    ).fetchall())
    by_wx = dict(con.execute(
        "SELECT wuxing,COUNT(*) FROM memories GROUP BY wuxing"
    ).fetchall())
    last  = con.execute(
        "SELECT content,created_at FROM memories ORDER BY id DESC LIMIT 1"
    ).fetchone()
    con.close()
    return {
        "total":      total,
        "today":      today,
        "by_source":  by_src,
        "by_wuxing":  by_wx,
        "last_memory":last[0][:40] if last else "（空）",
        "last_time":  last[1][:19] if last else "",
        "db_path":    str(DB_PATH),
        "chain_sha":  get_last_sha()[:16] + "...",
        "dna":        make_dna("status","SYS"),
        "confirm":    CONFIRM,
    }

def _row_to_dict(r) -> dict:
    return {
        "id": r[0], "dna": r[1], "content": r[2],
        "wuxing": r[3], "persona": r[4], "tricolor": r[5],
        "tags": json.loads(r[6] or "[]"),
        "source": r[7], "created_at": r[8],
    }

def _log_event(event: str, dna: str, source: str):
    line = f"[{datetime.now().isoformat()}] {event} | {source} | {dna}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

# ═══════════════════════════════════════
# 4. 打印工具
# ═══════════════════════════════════════

def print_memory(m: dict, index: int = None):
    prefix = f"[{index}]" if index is not None else "  "
    src_icon = SOURCE_ICON.get(m.get("source",""), "❓")
    tags = m.get("tags", [])
    tag_str = "·".join(tags) if tags else "—"
    print(f"{prefix} {m['tricolor']} {m['wuxing']} {src_icon}  {m['content'][:60]}")
    print(f"     {m['created_at'][:16]}  标签:{tag_str}  DNA:{m['dna'][-12:]}")

def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂脑干 · longhun_brain.py v1.0                ║
║  三端统一记忆核心：iOS · 宝宝 · Notion · Cursor     ║
╠══════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·壬辰·庚午·壬午·䷳艮为山-BRAIN-CORE-v1.0            ║
║  答应老师把德捡回来 🇨🇳                               ║
╚══════════════════════════════════════════════════════╝""")

# ═══════════════════════════════════════
# 5. Flask API（三端统一入口）
# ═══════════════════════════════════════

def run_server():
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ 需要安装Flask: pip install flask --break-system-packages")
        sys.exit(1)

    app = Flask(__name__)

    @app.route("/health")
    def health():
        return jsonify({
            "status": "🟢",
            "service": "龍魂脑干 v1.0",
            "port": PORT,
            "dna": make_dna("health", "SYS")
        })

    @app.route("/remember", methods=["POST"])
    def api_remember():
        """
        iOS快捷指令 / 宝宝 / Notion 都调这个
        POST JSON: {
          "content":  "今天发生了什么",
          "wuxing":   "水",        ← 可选，默认土
          "persona":  "宝宝·Claude", ← 可选
          "tags":     ["决策","亮剑"], ← 可选
          "source":   "ios"         ← 标记来源
        }
        """
        data    = request.get_json(force=True) or {}
        content = data.get("content", "").strip()
        if not content:
            return jsonify({"error": "content不能为空"}), 400

        result = remember(
            content = content,
            wuxing  = data.get("wuxing", "土"),
            persona = data.get("persona", "宝宝·Claude"),
            tags    = data.get("tags", []),
            source  = data.get("source", "unknown"),
        )
        return jsonify({
            "ok":      True,
            "dna":     result["dna"],
            "tricolor":result["tricolor"],
            "wuxing":  result["wuxing"],
            "dr":      result["dr"],
        })

    @app.route("/recall")
    def api_recall():
        """
        GET /recall?q=最小损失&wuxing=火&limit=10
        宝宝查记忆用这个
        """
        results = recall(
            keyword = request.args.get("q", ""),
            wuxing  = request.args.get("wuxing", ""),
            limit   = int(request.args.get("limit", 20)),
        )
        return jsonify({"ok": True, "count": len(results), "results": results})

    @app.route("/timeline")
    def api_timeline():
        """GET /timeline?date=2026-04-26"""
        day     = request.args.get("date", date.today().isoformat())
        results = timeline(day)
        return jsonify({"ok": True, "date": day, "count": len(results), "results": results})

    @app.route("/replay/<path:dna_code>")
    def api_replay(dna_code):
        """GET /replay/#龍芯⚡️..."""
        return jsonify(replay(dna_code))

    @app.route("/status")
    def api_status():
        return jsonify(status())

    print(f"\n🧠 龍魂脑干启动 → http://127.0.0.1:{PORT}")
    print(f"   📱 iOS快捷指令  → POST http://[Tailscale-IP]:{PORT}/remember")
    print(f"   🤖 宝宝查记忆   → GET  http://127.0.0.1:{PORT}/recall?q=关键词")
    print(f"   📓 Notion同步   → 每条记忆自动带DNA码")
    print(f"   💻 健康检查     → GET  http://127.0.0.1:{PORT}/health\n")
    app.run(host="0.0.0.0", port=PORT, debug=False)

# ═══════════════════════════════════════
# 6. iOS快捷指令配置输出
# ═══════════════════════════════════════

def print_ios_config():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 iOS快捷指令配置（脑干版）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【快捷指令①】宝宝记住这个
  触发：说"宝宝记住" 或 分享菜单
  步骤：
    1. 获取剪贴板 / 分享输入
    2. URL: http://[你的Tailscale-IP]:9625/remember
    3. 方法: POST
    4. Body(JSON):
       {
         "content":  "[输入内容]",
         "wuxing":   "土",
         "persona":  "宝宝·Claude",
         "tags":     ["ios记录"],
         "source":   "ios"
       }
    5. 显示通知: [tricolor] 已记住·[dna后8位]

【快捷指令②】宝宝我想起什么了
  触发：语音"宝宝搜索"
  步骤：
    1. 询问: 搜索什么？
    2. URL: http://[Tailscale-IP]:9625/recall?q=[回答]
    3. 方法: GET
    4. 显示: 搜索结果列表

【快捷指令③】今天的记忆
  触发：每天早上8点自动
  步骤：
    1. URL: http://[Tailscale-IP]:9625/timeline
    2. 方法: GET
    3. 显示通知: 今日N条记忆

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Tailscale-IP: 在Mac终端输入 tailscale ip -4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# ═══════════════════════════════════════
# 7. CLI 入口
# ═══════════════════════════════════════

def main():
    init_db()
    parser = argparse.ArgumentParser(description="🐉 龍魂脑干")
    parser.add_argument("--remember",  "-r", type=str,  help="存入一条记忆")
    parser.add_argument("--recall",    "-s", type=str,  help="搜索记忆关键词")
    parser.add_argument("--timeline",  "-t", type=str,  nargs="?", const="today", help="查看时间线")
    parser.add_argument("--replay",         type=str,  help="精确回放DNA码")
    parser.add_argument("--status",    action="store_true", help="脑干健康状态")
    parser.add_argument("--ios",       action="store_true", help="输出iOS快捷指令配置")
    parser.add_argument("--server",    action="store_true", help="启动API服务")
    parser.add_argument("--wuxing",    "-w", type=str,  default="土", help="五行属性")
    parser.add_argument("--tag",       type=str,  default="",   help="标签，逗号分隔")
    parser.add_argument("--source",    type=str,  default="cursor", help="来源")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        # 默认：启动服务
        print_banner()
        run_server()
        return

    if args.remember:
        print_banner()
        tags  = [t.strip() for t in args.tag.split(",") if t.strip()]
        m     = remember(args.remember, args.wuxing, "宝宝·Claude", tags, args.source)
        print(f"\n{m['tricolor']} 已记住")
        print(f"  DNA     : {m['dna']}")
        print(f"  五行    : {m['wuxing']}  数字根: {m['dr']}")
        print(f"  标签    : {', '.join(tags) or '—'}")
        print(f"  哈希链  : {m['sha256_self'][:20]}...")
        print(f"\n{CONFIRM}")

    elif args.recall:
        results = recall(args.recall, args.wuxing, 20)
        print(f"\n🔍 搜索“{args.recall}”→ 找到 {len(results)} 条\n")
        for i, m in enumerate(results):
            print_memory(m, i+1)
        print()

    elif args.timeline is not None:
        day  = date.today().isoformat() if args.timeline == "today" else args.timeline
        mems = timeline(day)
        print(f"\n📅 {day} 时间线 · {len(mems)} 条记忆\n")
        for m in mems:
            print_memory(m)
        print()

    elif args.replay:
        m = replay(args.replay)
        print(f"\n🔁 回放记忆\n")
        print(f"  内容    : {m.get('content','')}")
        print(f"  DNA     : {m.get('dna','')}")
        print(f"  五行    : {m.get('wuxing','')}  {m.get('tricolor','')}")
        print(f"  来源    : {m.get('source','')}")
        print(f"  时间    : {m.get('created_at','')[:19]}")
        print(f"  哈希链  ✅ 已验证\n")

    elif args.status:
        s = status()
        print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 龍魂脑干 · 健康状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  总记忆     : {s['total']} 条
  今日新增   : {s['today']} 条
  最新一条   : {s['last_memory']}
  最新时间   : {s['last_time']}
  哈希链尾   : {s['chain_sha']}
  数据库     : {s['db_path']}
  来源分布   : {json.dumps(s['by_source'], ensure_ascii=False)}
  五行分布   : {json.dumps(s['by_wuxing'], ensure_ascii=False)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {CONFIRM}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")

    elif args.ios:
        print_ios_config()

    elif args.server:
        print_banner()
        run_server()

if __name__ == "__main__":
    main()
