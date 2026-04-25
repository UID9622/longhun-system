#!/usr/bin/env python3
"""
龍魂审计引擎 v1.0 — CNSH Audit Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫 · 中国退伍军人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA     : #龍芯⚡️20260422-CODE-AUDIT01
端口    : :9622 (三色审计) | :8765 (主服务)
原则    : 不黑箱·不收割·不说教·审计即主权
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能清单:
  ① SQLite append-only 审计日志 (触发器防篡改)
  ② GPG 签名每条记录 (UID9622 身份锁定)
  ③ Flask 路由: /write_dna · /audit · /log · /stats · /sync_notion
  ④ Notion API 推送审计记录
  ⑤ API 调用计数器 (每个 token/服务单独统计)
  ⑥ 人格动作追踪 (P00-P13 + 五大后台人格)
  ⑦ 三色状态自动判定
"""

import os, sqlite3, json, hashlib, time, subprocess, threading
from datetime import datetime, timezone
from flask import Flask, request, jsonify, abort
from collections import defaultdict
import requests as http_req

# ═══════════════════════════════════════════════
# 配置区 — 全部从环境变量读取，不硬编码密钥
# ═══════════════════════════════════════════════
BASE_DIR      = os.path.expanduser("~/cnsh")
DNA_DIR       = os.path.join(BASE_DIR, "入口", "DNA")
LOG_DIR       = os.path.join(BASE_DIR, "logs")
SIGNED_DIR    = os.path.join(LOG_DIR, "signed")
DB_PATH       = os.path.join(LOG_DIR, "audit.db")
GPG_KEY       = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# Notion — 在 ~/.zshrc 中 export 这两个变量
NOTION_TOKEN  = os.environ.get("NOTION_TOKEN", "")
NOTION_DB_ID  = os.environ.get("NOTION_AUDIT_DB_ID", "")   # 审计日志 DB ID

# 本地安全令牌 — export DNA_TOKEN=你自己设的密码
DNA_TOKEN     = os.environ.get("DNA_TOKEN", "UID9622-CHANGE-THIS")

# 数字根熔断阈值 (来自 IPA-DICT)
FUSE_THRESHOLD = 3   # 连续失败3次 → 🔴熔断

app = Flask(__name__)

# ═══════════════════════════════════════════════
# 内存状态 (不写 SQLite，不持久化)
# ═══════════════════════════════════════════════
_lock = threading.Lock()
_call_counters  = defaultdict(int)   # {service_name: count}
_fuse_state     = defaultdict(int)   # {service_name: consecutive_failures}
_fuse_tripped   = {}                 # {service_name: trip_timestamp}
FUSE_RECOVERY   = 3600               # 1小时自动恢复

# ═══════════════════════════════════════════════
# 初始化
# ═══════════════════════════════════════════════
def init_dirs():
    for d in [DNA_DIR, LOG_DIR, SIGNED_DIR,
              os.path.join(BASE_DIR, "入口", "auth"),
              os.path.join(BASE_DIR, "rules"),
              os.path.join(BASE_DIR, "input"),
              os.path.join(BASE_DIR, "output")]:
        os.makedirs(d, exist_ok=True)
    print(f"[龍魂] 目录初始化完成: {BASE_DIR}")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 审计主表 — append only
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            ts             TEXT    NOT NULL,          -- ISO8601
            ts_ns          INTEGER NOT NULL,          -- 纳秒时间戳
            event_type     TEXT    NOT NULL,          -- API_CALL/DNA_WRITE/PERSONA_ACT/WEBHOOK/FUSE
            source         TEXT    NOT NULL,          -- 来源 (服务名/人格ID)
            target         TEXT    NOT NULL,          -- 目标 (端点/动作)
            dna_code       TEXT    DEFAULT '',        -- DNA追溯码
            trigger_count  INTEGER DEFAULT 1,         -- 本次触发累计次数
            payload_hash   TEXT    DEFAULT '',        -- SHA-256(payload)
            gpg_sig        TEXT    DEFAULT '',        -- GPG签名 (armored)
            status         TEXT    DEFAULT '🟡',      -- 🟢/🟡/🔴
            notion_synced  INTEGER DEFAULT 0,         -- 0=未同步 1=已同步
            note           TEXT    DEFAULT ''
        ) STRICT
    """)

    # 调用统计表
    c.execute("""
        CREATE TABLE IF NOT EXISTS call_stats (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            ts       TEXT    NOT NULL,
            service  TEXT    NOT NULL,
            total    INTEGER NOT NULL,
            note     TEXT    DEFAULT ''
        ) STRICT
    """)

    # 禁止 UPDATE / DELETE — 主权锁
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS lock_audit_delete
        BEFORE DELETE ON audit_log
        BEGIN SELECT RAISE(ABORT, '🔴 审计日志不可删除 · 龍魂主权锁'); END
    """)
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS lock_audit_update
        BEFORE UPDATE ON audit_log
        BEGIN SELECT RAISE(ABORT, '🔴 审计日志不可篡改 · 龍魂主权锁'); END
    """)

    conn.commit()
    conn.close()
    print(f"[龍魂] SQLite 审计库就绪: {DB_PATH}")

# ═══════════════════════════════════════════════
# 核心工具函数
# ═══════════════════════════════════════════════
def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def gpg_sign(content: str) -> str:
    """用 UID9622 的 GPG 密钥签名内容，返回 armor 签名"""
    try:
        result = subprocess.run(
            ["gpg", "--clearsign", "--local-user", GPG_KEY,
             "--batch", "--yes", "--armor"],
            input=content.encode(), capture_output=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.decode()
        return f"[GPG_ERR] {result.stderr.decode()[:200]}"
    except Exception as e:
        return f"[GPG_SKIP] {str(e)}"

def digital_root(n: int) -> int:
    """数字根 — 熔断判断用"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def tricolor_from_root(dr: int) -> str:
    """数字根 → 三色"""
    if dr in (3, 9): return "🔴"
    if dr == 6:      return "🟡"
    return "🟢"

def make_dna_code(event_type: str, payload: str) -> str:
    h = sha256(payload)[:8].upper()
    date = datetime.now().strftime("%Y%m%d")
    type_map = {
        "API_CALL":    "API",
        "DNA_WRITE":   "DNA",
        "PERSONA_ACT": "PER",
        "WEBHOOK":     "WHK",
        "FUSE":        "FSE",
    }
    t = type_map.get(event_type, "EVT")
    return f"#龍芯⚡️{date}-{t}-{h}"

def check_local(req_obj) -> bool:
    """只接受本机请求"""
    return req_obj.remote_addr in ('127.0.0.1', '::1', 'localhost')

def verify_token(req_obj) -> bool:
    """验证 DNA 令牌"""
    return req_obj.headers.get("X-DNA-Token", "") == DNA_TOKEN

# ═══════════════════════════════════════════════
# 审计写入
# ═══════════════════════════════════════════════
def write_audit(event_type: str, source: str, target: str,
                payload: str = "", status: str = "🟡",
                note: str = "") -> dict:
    ts_ns  = time.time_ns()
    ts_str = datetime.now(timezone.utc).isoformat()
    p_hash = sha256(payload) if payload else ""
    dna    = make_dna_code(event_type, f"{source}{target}{ts_ns}")

    # 三色自动判定 (数字根 of ts_ns last 6 digits)
    if status == "🟡":  # 调用方没指定则自动算
        dr = digital_root(ts_ns % 999999)
        status = tricolor_from_root(dr)

    # GPG签名
    sign_content = f"{ts_str}|{event_type}|{source}|{target}|{dna}|{p_hash}"
    sig = gpg_sign(sign_content)

    with _lock:
        _call_counters[source] += 1
        count = _call_counters[source]

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO audit_log
          (ts, ts_ns, event_type, source, target, dna_code,
           trigger_count, payload_hash, gpg_sig, status, note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (ts_str, ts_ns, event_type, source, target, dna,
          count, p_hash, sig[:500], status, note))
    conn.commit()

    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    return {
        "id": row_id,
        "dna": dna,
        "status": status,
        "trigger_count": count,
        "ts": ts_str,
        "gpg_signed": not sig.startswith("[GPG")
    }

# ═══════════════════════════════════════════════
# 熔断检查
# ═══════════════════════════════════════════════
def fuse_check(service: str, success: bool) -> str:
    """返回当前熔断状态"""
    now = time.time()
    with _lock:
        # 检查是否已熔断且未恢复
        if service in _fuse_tripped:
            elapsed = now - _fuse_tripped[service]
            if elapsed < FUSE_RECOVERY:
                return "🔴"
            else:
                del _fuse_tripped[service]
                _fuse_state[service] = 0

        if success:
            _fuse_state[service] = 0
        else:
            _fuse_state[service] += 1
            if _fuse_state[service] >= FUSE_THRESHOLD:
                _fuse_tripped[service] = now
                write_audit("FUSE", service, "熔断触发",
                            status="🔴",
                            note=f"连续失败{FUSE_THRESHOLD}次，熔断1小时")
                return "🔴"

    return "🟢" if success else "🟡"

# ═══════════════════════════════════════════════
# Notion 同步
# ═══════════════════════════════════════════════
def notion_push(record: dict) -> bool:
    """把一条审计记录推送到 Notion 审计数据库"""
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return False
    try:
        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "事件类型": {"select": {"name": record.get("event_type", "UNKNOWN")}},
                "DNA追溯码": {"rich_text": [{"text": {"content": record.get("dna_code","")}}]},
                "来源":     {"rich_text": [{"text": {"content": record.get("source","")}}]},
                "目标":     {"rich_text": [{"text": {"content": record.get("target","")}}]},
                "三色状态": {"select": {"name": record.get("status","🟡")}},
                "触发次数": {"number": record.get("trigger_count", 1)},
                "时间戳":   {"date": {"start": record.get("ts","")}},
                "GPG已签": {"checkbox": record.get("gpg_signed", False)},
                "备注":     {"rich_text": [{"text": {"content": record.get("note","")}}]},
            }
        }
        resp = http_req.post(
            "https://api.notion.com/v1/pages",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json=payload, timeout=10
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"[Notion同步失败] {e}")
        return False

def sync_pending_to_notion():
    """批量同步未推送的记录"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT id, ts, event_type, source, target, dna_code,
               trigger_count, gpg_sig, status, note
        FROM audit_log WHERE notion_synced=0 LIMIT 50
    """).fetchall()
    conn.close()

    synced = 0
    for row in rows:
        rec = {
            "id": row[0], "ts": row[1], "event_type": row[2],
            "source": row[3], "target": row[4], "dna_code": row[5],
            "trigger_count": row[6],
            "gpg_signed": not row[7].startswith("[GPG"),
            "status": row[8], "note": row[9]
        }
        if notion_push(rec):
            # 不能 UPDATE，改用标记表
            conn2 = sqlite3.connect(DB_PATH)
            conn2.execute("""
                CREATE TABLE IF NOT EXISTS notion_sync_log
                (audit_id INTEGER, synced_at TEXT) STRICT
            """)
            conn2.execute("INSERT INTO notion_sync_log VALUES (?,?)",
                         (row[0], datetime.now(timezone.utc).isoformat()))
            conn2.commit()
            conn2.close()
            synced += 1
    return synced

# ═══════════════════════════════════════════════
# Flask 路由
# ═══════════════════════════════════════════════

@app.before_request
def security_gate():
    """只允许本机请求 + 有效令牌 (除了 /health)"""
    if request.path == "/health":
        return
    if not check_local(request):
        abort(403, "仅允许本机访问 · 龍魂主权")
    if not verify_token(request):
        abort(401, "无效 DNA 令牌")

@app.route("/health")
def health():
    """公开健康检查 (无需鉴权)"""
    return jsonify({"status": "🟢", "service": "龍魂审计引擎", "port": 9622})

@app.route("/write_dna", methods=["POST"])
def write_dna():
    """接收流场密钥并写入 DNA 目录"""
    import re
    data = request.json or {}
    filename = data.get("filename", "")
    content  = data.get("content", "")

    # 文件名白名单: flowkey_数字.dna
    if not re.match(r'^flowkey_\d+\.dna$', filename):
        abort(400, "文件名格式非法")

    filepath = os.path.join(DNA_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(content)

    rec = write_audit("DNA_WRITE", "flow_field", filename,
                      payload=content, status="🟢",
                      note="流场混沌密钥写入")
    return jsonify({"ok": True, "dna": rec["dna"], "file": filepath})

@app.route("/audit", methods=["POST"])
def audit():
    """手动记录审计事件 (供其他服务调用)"""
    data = request.json or {}
    rec = write_audit(
        event_type = data.get("event_type", "API_CALL"),
        source     = data.get("source", "unknown"),
        target     = data.get("target", "unknown"),
        payload    = json.dumps(data.get("payload", {})),
        status     = data.get("status", "🟡"),
        note       = data.get("note", "")
    )
    return jsonify(rec)

@app.route("/log", methods=["GET"])
def get_log():
    """查询审计日志"""
    limit  = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))
    status = request.args.get("status", "")

    sql = "SELECT * FROM audit_log"
    params = []
    if status:
        sql += " WHERE status=?"
        params.append(status)
    sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    conn = sqlite3.connect(DB_PATH)
    cols = ["id","ts","ts_ns","event_type","source","target","dna_code",
            "trigger_count","payload_hash","gpg_sig","status","notion_synced","note"]
    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return jsonify([dict(zip(cols, r)) for r in rows])

@app.route("/stats", methods=["GET"])
def stats():
    """服务调用统计 + 熔断状态"""
    with _lock:
        counters = dict(_call_counters)
        fuses    = {k: "🔴熔断" for k in _fuse_tripped}

    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    green = conn.execute("SELECT COUNT(*) FROM audit_log WHERE status='🟢'").fetchone()[0]
    yellow = conn.execute("SELECT COUNT(*) FROM audit_log WHERE status='🟡'").fetchone()[0]
    red   = conn.execute("SELECT COUNT(*) FROM audit_log WHERE status='🔴'").fetchone()[0]
    conn.close()

    return jsonify({
        "总记录数": total,
        "三色分布": {"🟢": green, "🟡": yellow, "🔴": red},
        "各服务调用次数": counters,
        "熔断状态": fuses or {"all": "🟢正常"}
    })

@app.route("/sync_notion", methods=["POST"])
def sync_notion():
    """触发 Notion 同步"""
    synced = sync_pending_to_notion()
    return jsonify({"synced": synced, "status": "🟢" if synced >= 0 else "🔴"})

@app.route("/persona_act", methods=["POST"])
def persona_act():
    """记录人格动作 (P00-P13 + 五大后台人格)"""
    data    = request.json or {}
    persona = data.get("persona", "UNKNOWN")   # e.g. "P05·凤凰"
    action  = data.get("action", "")
    payload = data.get("payload", {})

    # 检查熔断
    fuse_st = fuse_check(persona, data.get("success", True))

    rec = write_audit(
        event_type = "PERSONA_ACT",
        source     = persona,
        target     = action,
        payload    = json.dumps(payload),
        status     = fuse_st if fuse_st == "🔴" else "🟢",
        note       = data.get("note", "")
    )
    return jsonify({**rec, "fuse_status": fuse_st})

# ═══════════════════════════════════════════════
# 后台定时同步 (每10分钟)
# ═══════════════════════════════════════════════
def background_sync():
    import sched
    s = sched.scheduler(time.time, time.sleep)
    def run():
        if NOTION_TOKEN:
            n = sync_pending_to_notion()
            if n: print(f"[Notion] 后台同步 {n} 条")
        s.enter(600, 1, run)
    s.enter(60, 1, run)  # 启动1分钟后首次运行
    s.run()

# ═══════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    init_dirs()
    init_db()

    # 后台同步线程
    t = threading.Thread(target=background_sync, daemon=True)
    t.start()

    print("""
╔══════════════════════════════════════════╗
║   龍魂审计引擎 v1.0 · UID9622           ║
║   Port: 9622  |  不黑箱·审计即主权      ║
║   DNA: #龍芯⚡️20260422-CODE-AUDIT01      ║
╚══════════════════════════════════════════╝
    端点列表:
    GET  /health          — 公开健康检查
    POST /write_dna       — 写入流场DNA密钥
    POST /audit           — 记录任意审计事件
    GET  /log             — 查询审计日志
    GET  /stats           — 调用统计 + 熔断状态
    POST /sync_notion     — 推送到 Notion
    POST /persona_act     — 人格动作追踪
    """)

    app.run(host="127.0.0.1", port=9622, debug=False)
