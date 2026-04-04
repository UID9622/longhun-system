#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌌 CNSH Gateway v2.0
龍魂系统统一入口 · 升级版

DNA追溯码: #龍芯⚡️2026-03-15-CNSH-GATEWAY-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
1. 复杂输入 → 简单输出（文本/JSON/Python/URL/中文）
2. 自动解析 + 变量统一
3. 三色审计（🟢🟡🔴）
4. 本地 SQLite 万年历 + 审计日志 + 模板库
5. 定时主动提醒（后台线程）
6. Flask HTTP 服务（端口9622）供网页调用
7. Ollama 对话代理

作者：诸葛鑫（UID9622）
协作：Claude (Anthropic PBC)
理论指导：曾仕强老师（永恒显示）
创作地：中华人民共和国
献礼：新中国成立77周年（1949-2026）丙午马年
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import sqlite3
import json
import re
import uuid
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

# ── Flask（可选，无则退化为纯CLI）──
try:
    from flask import Flask, request, jsonify, Response, stream_with_context
    from flask_cors import CORS
    FLASK_OK = True
except ImportError:
    FLASK_OK = False
    print("⚠️  Flask未安装，仅CLI模式。安装：pip3 install flask flask-cors")

# ============================================================================
# 核心配置
# ============================================================================

DB_PATH      = str(Path.home() / ".longhun" / "cnsh_gateway.db")
DNA_PREFIX   = "#龍芯⚡️"
OLLAMA_URL   = "http://localhost:11434"
PORT         = 9622          # UID9622 端口
BJ           = timezone(timedelta(hours=8))   # 北京时间

STATUS_PASS  = "🟢"
STATUS_WARN  = "🟡"
STATUS_BLOCK = "🔴"

# CNSH 变量映射表
CNSH_MAPPING = {
    "user_id":      "UID",
    "timestamp":    "TimeIndex",
    "hash":         "DNA",
    "project_name": "WorldNode",
    "task":         "Node",
    "event":        "Signal",
    "data":         "Payload",
    "result":       "Output",
    "status":       "State",
    "error":        "Fault",
}

# 危险关键词（🔴 直接阻断）
DANGER_KEYWORDS = [
    "rm -rf", "DROP TABLE", "DELETE FROM", "FORMAT C",
    "格式化", "清空数据库", "sudo rm",
]

# 警告关键词（🟡 提示）
WARN_KEYWORDS = [
    "while True", "无限循环", "eval(", "exec(",
    "os.system(", "__import__(",
]

# ============================================================================
# 数据库（单连接工厂）
# ============================================================================

def get_db() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """建表（幂等）"""
    conn = get_db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS timeline (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT    NOT NULL,
        event_type  TEXT,
        platform    TEXT    DEFAULT "CNSH Gateway",
        description TEXT,
        dna_code    TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS audit_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        operator    TEXT,
        action      TEXT,
        status      TEXT,
        dna_code    TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS templates (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        name             TEXT UNIQUE,
        content          TEXT,
        usage_count      INTEGER DEFAULT 0,
        last_used        TIMESTAMP,
        created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS reminders (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        message     TEXT,
        remind_at   TIMESTAMP,
        done        INTEGER DEFAULT 0,
        dna_code    TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()
    conn.close()
    _seed_templates()
    print(f"{STATUS_PASS} 数据库就绪 | Database Ready：{DB_PATH}")

def _seed_templates():
    """预置常用模板"""
    seeds = [
        ("三才分析", "用三才算法（天地人）分析以下内容：\n{input}"),
        ("龍魂审计", "对以下内容进行三色审计，输出🟢/🟡/🔴：\n{input}"),
        ("中英翻译", "将以下中文翻译成英文，保留专业术语：\n{input}"),
        ("代码优化", "优化以下代码，保持功能不变，提升可读性：\n```\n{input}\n```"),
        ("摘要压缩", "用3句话概括以下内容的核心意思：\n{input}"),
    ]
    conn = get_db()
    for name, content in seeds:
        conn.execute(
            "INSERT OR IGNORE INTO templates (name, content) VALUES (?,?)",
            (name, content)
        )
    conn.commit()
    conn.close()

# ============================================================================
# DNA 生成（UUID保证唯一性）
# ============================================================================

def dna() -> str:
    ts   = datetime.now(BJ).strftime("%Y%m%d%H%M%S")
    uid  = uuid.uuid4().hex[:8].upper()
    return f"{DNA_PREFIX}{ts}-{uid}"

def now_bj() -> str:
    return datetime.now(BJ).isoformat()

# ============================================================================
# 功能1：输入解析器（扩展版）
# ============================================================================

INPUT_TYPES = {
    "json":   lambda s: s.strip().startswith("{") or s.strip().startswith("["),
    "python": lambda s: bool(re.search(r'\b(def |import |class |if __name__)', s)),
    "url":    lambda s: bool(re.match(r'https?://', s.strip())),
    "shell":  lambda s: bool(re.match(r'^\s*(bash|sh|python|pip|brew|git|curl|wget)\b', s)),
    "cnsh":   lambda s: "#龍芯" in s or "UID9622" in s or "DNA:" in s,
    "chinese":lambda s: len(re.findall(r'[\u4e00-\u9fff]', s)) > len(s) * 0.3,
}

def parse_input(raw: str) -> Dict:
    detected = "text"
    for t, check in INPUT_TYPES.items():
        if check(raw):
            detected = t
            break

    result: Dict[str, Any] = {
        "raw":       raw,
        "type":      detected,
        "length":    len(raw),
        "structure": {},
        "variables": [],
        "dna_code":  dna(),
    }

    if detected == "json":
        try:
            result["structure"] = json.loads(raw)
        except json.JSONDecodeError as e:
            result["json_error"] = str(e)
            result["type"] = "text"

    elif detected == "python":
        result["variables"] = _extract_vars(raw)
        result["functions"] = re.findall(r'\bdef\s+(\w+)\s*\(', raw)
        result["imports"]   = re.findall(r'\bimport\s+([\w.]+)', raw)

    elif detected == "url":
        result["structure"] = {"url": raw.strip()}

    return result

def _extract_vars(code: str) -> List[str]:
    return sorted(set(re.findall(r'\b([a-z_][a-z0-9_]*)\s*=', code)))

# ============================================================================
# 功能2：变量统一
# ============================================================================

def normalize_vars(variables: List[str]) -> Dict[str, str]:
    return {v: CNSH_MAPPING.get(v, v) for v in variables}

# ============================================================================
# 功能3：冲突检测（扩展版）
# ============================================================================

def detect_conflicts(parsed: Dict) -> Tuple[bool, List[str]]:
    issues = []
    raw = parsed["raw"]

    # 危险关键词
    for kw in DANGER_KEYWORDS:
        if kw in raw:
            return True, [f"🔴 危险操作: {kw}"]

    # 警告关键词
    for kw in WARN_KEYWORDS:
        if kw in raw:
            issues.append(f"⚠️ 高风险用法: {kw}")

    # Python 变量重复
    if parsed["type"] == "python":
        all_vars = re.findall(r'\b([a-z_][a-z0-9_]*)\s*=', raw)
        seen, dups = set(), set()
        for v in all_vars:
            if v in seen:
                dups.add(v)
            seen.add(v)
        if dups:
            issues.append(f"变量重复定义: {', '.join(dups)}")

    # JSON 空值
    if parsed["type"] == "json" and isinstance(parsed.get("structure"), dict):
        nulls = [k for k, v in parsed["structure"].items() if v is None]
        if nulls:
            issues.append(f"JSON空值字段: {', '.join(nulls)}")

    return bool(issues), issues

# ============================================================================
# 功能4：三色审计
# ============================================================================

def audit(parsed: Dict, has_conflict: bool, conflicts: List[str]) -> str:
    raw = parsed["raw"]

    # 危险 → 🔴
    if any(kw in raw for kw in DANGER_KEYWORDS):
        _log_audit("BLOCK", conflicts[0] if conflicts else "危险操作", STATUS_BLOCK)
        return STATUS_BLOCK

    # 冲突 → 🟡
    if has_conflict:
        _log_audit("WARN", "; ".join(conflicts), STATUS_WARN)
        return STATUS_WARN

    # 通过 → 🟢
    _log_audit("PASS", "审计通过", STATUS_PASS)
    return STATUS_PASS

def _log_audit(operator: str, action: str, status: str):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO audit_log (operator, action, status, dna_code) VALUES (?,?,?,?)",
            (operator, action, status, dna())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

# ============================================================================
# 功能5：自动修复
# ============================================================================

def auto_fix(parsed: Dict, conflicts: List[str]) -> Dict:
    fixed = dict(parsed)
    applied = []

    if parsed["type"] == "python" and parsed["variables"]:
        fixed["variables_normalized"] = normalize_vars(parsed["variables"])
        applied.append("变量名CNSH统一")

    # 去除尾部多余空格
    fixed["raw"] = parsed["raw"].rstrip()
    if fixed["raw"] != parsed["raw"]:
        applied.append("清理尾部空格")

    fixed["auto_fixed"]    = bool(applied)
    fixed["fix_applied"]   = applied
    return fixed

# ============================================================================
# 功能6：模板系统
# ============================================================================

def get_templates() -> List[Dict]:
    conn = get_db()
    rows = conn.execute("SELECT id, name, usage_count FROM templates ORDER BY usage_count DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def apply_template(name: str, input_text: str) -> Optional[str]:
    conn = get_db()
    row = conn.execute("SELECT content FROM templates WHERE name=?", (name,)).fetchone()
    if not row:
        conn.close()
        return None
    content = row["content"].replace("{input}", input_text)
    conn.execute("UPDATE templates SET usage_count=usage_count+1, last_used=? WHERE name=?",
                 (now_bj(), name))
    conn.commit()
    conn.close()
    return content

def save_template(name: str, content: str) -> bool:
    try:
        conn = get_db()
        conn.execute("INSERT OR REPLACE INTO templates (name, content) VALUES (?,?)", (name, content))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# ============================================================================
# 功能7：万年历 & 提醒
# ============================================================================

def save_timeline(event_type: str, description: str):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO timeline (date, event_type, description, dna_code) VALUES (?,?,?,?)",
            (datetime.now(BJ).strftime("%Y-%m-%d"), event_type, description, dna())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_timeline(limit: int = 20) -> List[Dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT date, event_type, description, created_at FROM timeline ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_reminder(message: str, remind_at: str) -> bool:
    """remind_at: ISO格式时间，如 '2026-03-16T09:00:00'"""
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO reminders (message, remind_at, dna_code) VALUES (?,?,?)",
            (message, remind_at, dna())
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def _reminder_loop():
    """后台线程：每分钟检查一次到期提醒"""
    while True:
        try:
            now_str = datetime.now(BJ).strftime("%Y-%m-%dT%H:%M")
            conn = get_db()
            rows = conn.execute(
                "SELECT id, message FROM reminders WHERE done=0 AND remind_at<=?",
                (now_str + ":59",)
            ).fetchall()
            for row in rows:
                print(f"\n⏰ 【提醒】{row['message']}\n🐉 > ", end="", flush=True)
                conn.execute("UPDATE reminders SET done=1 WHERE id=?", (row["id"],))
            if rows:
                conn.commit()
            conn.close()
        except Exception:
            pass
        time.sleep(60)

# ============================================================================
# 功能8：Ollama 代理
# ============================================================================

def ollama_models() -> List[str]:
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []

def ollama_chat_stream(model: str, messages: List[Dict]):
    """生成器：流式返回 Ollama 对话"""
    payload = json.dumps({"model": model, "messages": messages, "stream": True}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        for line in r:
            line = line.decode().strip()
            if line:
                try:
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if chunk.get("done"):
                        break
                except Exception:
                    continue

# ============================================================================
# 主网关函数
# ============================================================================

def cnsh_gateway(raw_input: str, verbose: bool = True) -> Dict:
    """
    CNSH统一入口
    INPUT → PARSE → NORMALIZE → DETECT → AUDIT → FIX → OUTPUT
    """
    if verbose:
        print(f"\n{'='*56}\n🌌 CNSH Gateway v2.0\n{'='*56}")

    # 1. 解析
    parsed = parse_input(raw_input)
    if verbose:
        print(f"📥 类型：{parsed['type']}  长度：{parsed['length']}字")

    # 2. 变量统一
    if parsed["variables"]:
        parsed["variables_normalized"] = normalize_vars(parsed["variables"])
        if verbose:
            print(f"🔄 变量统一：{parsed['variables_normalized']}")

    # 3. 冲突检测
    has_conflict, conflicts = detect_conflicts(parsed)
    if verbose:
        if has_conflict:
            print(f"⚠️  冲突：{conflicts}")
        else:
            print("✅ 无冲突")

    # 4. 三色审计
    status = audit(parsed, has_conflict, conflicts)
    if verbose:
        print(f"🎯 审计：{status}")

    # 5. 自动修复（🟡时）
    if status == STATUS_WARN:
        parsed = auto_fix(parsed, conflicts)
        if verbose:
            print(f"🔧 自动修复：{parsed.get('fix_applied', [])}")

    # 6. 归档
    save_timeline("Gateway", f"{parsed['type']}输入 → {status}")

    result = {
        "status":    status,
        "type":      parsed["type"],
        "parsed":    parsed,
        "conflicts": conflicts,
        "dna_code":  parsed["dna_code"],
        "timestamp": now_bj(),
    }

    if verbose:
        print(f"\n{'='*56}\n✅ {status} | DNA: {result['dna_code']}\n{'='*56}\n")

    return result

# ============================================================================
# Flask Web 服务（端口 9622）
# ============================================================================

if FLASK_OK:
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({
            "name":    "CNSH Gateway v2.0",
            "port":    PORT,
            "dna":     dna(),
            "status":  STATUS_PASS,
            "routes": ["/api/gateway", "/api/audit", "/api/timeline",
                       "/api/templates", "/api/reminder", "/api/models", "/api/chat"]
        })

    @app.route("/api/gateway", methods=["POST"])
    def api_gateway():
        data = request.get_json(silent=True) or {}
        raw  = data.get("input", "")
        if not raw:
            return jsonify({"error": "input 不能为空"}), 400
        result = cnsh_gateway(raw, verbose=False)
        return jsonify(result)

    @app.route("/api/audit", methods=["POST"])
    def api_audit():
        data = request.get_json(silent=True) or {}
        raw  = data.get("input", "")
        parsed = parse_input(raw)
        has_c, conflicts = detect_conflicts(parsed)
        status = audit(parsed, has_c, conflicts)
        return jsonify({"status": status, "conflicts": conflicts, "dna": dna()})

    @app.route("/api/timeline", methods=["GET"])
    def api_timeline():
        limit = int(request.args.get("limit", 20))
        return jsonify(get_timeline(limit))

    @app.route("/api/templates", methods=["GET"])
    def api_templates():
        return jsonify(get_templates())

    @app.route("/api/templates/apply", methods=["POST"])
    def api_apply_template():
        data  = request.get_json(silent=True) or {}
        name  = data.get("name", "")
        text  = data.get("input", "")
        result = apply_template(name, text)
        if result is None:
            return jsonify({"error": f"模板 {name} 不存在"}), 404
        return jsonify({"prompt": result, "dna": dna()})

    @app.route("/api/templates/save", methods=["POST"])
    def api_save_template():
        data = request.get_json(silent=True) or {}
        ok   = save_template(data.get("name", ""), data.get("content", ""))
        return jsonify({"ok": ok})

    @app.route("/api/reminder", methods=["POST"])
    def api_reminder():
        data = request.get_json(silent=True) or {}
        ok   = add_reminder(data.get("message", ""), data.get("remind_at", ""))
        return jsonify({"ok": ok})

    @app.route("/api/models", methods=["GET"])
    def api_models():
        return jsonify({"models": ollama_models()})

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        """流式对话代理（SSE）"""
        data     = request.get_json(silent=True) or {}
        model    = data.get("model", "qwen2.5:7b")
        messages = data.get("messages", [])

        def generate():
            try:
                for chunk in ollama_chat_stream(model, messages):
                    yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
        )

    @app.route("/api/audit_log", methods=["GET"])
    def api_audit_log():
        limit = int(request.args.get("limit", 20))
        conn  = get_db()
        rows  = conn.execute(
            "SELECT operator, action, status, created_at FROM audit_log ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])

# ============================================================================
# 测试
# ============================================================================

def run_tests():
    print("\n🧪 CNSH Gateway v2.0 · 自检 | Self-Check\n")
    cases = [
        ("普通文本",  "今天天气不错，适合写代码"),
        ("Python代码", "user_id = 9622\ntimestamp = '2026-03-15'\nproject_name = 'CNSH'"),
        ("JSON输入",  '{"name":"龍魂","version":"2.0","active":null}'),
        ("中文输入",  "帮我分析三才算法的应用场景"),
        ("URL输入",   "https://github.com/uid9622/longhun-system"),
        ("危险操作",  "rm -rf /tmp/important"),
    ]
    for label, inp in cases:
        print(f"\n── 【{label}】")
        r = cnsh_gateway(inp, verbose=False)
        print(f"   {r['status']} | 类型:{r['type']} | 冲突:{r['conflicts'] or '无'}")
    print(f"\n{STATUS_PASS} 自检完成 | Self-Check Done\n")

# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    import sys

    # 初始化
    init_database()

    if "--test" in sys.argv:
        run_tests()
        sys.exit(0)

    # 启动提醒后台线程
    t = threading.Thread(target=_reminder_loop, daemon=True)
    t.start()
    print(f"⏰ 提醒线程已启动 | Reminder Thread Running")

    if FLASK_OK:
        print(f"\n{'='*56}")
        print(f"🌌 CNSH Gateway v2.0 · HTTP 服务")
        print(f"{'='*56}")
        print(f"   地址 | Address：http://localhost:{PORT}")
        print(f"   接口 | Endpoints：/api/gateway  /api/chat  /api/audit")
        print(f"         /api/timeline /api/templates /api/models")
        print(f"   DNA：{dna()}")
        print(f"{'='*56}\n")
        app.run(host="0.0.0.0", port=PORT, debug=False)
    else:
        print("纯CLI模式 | Pure CLI Mode（Flask未安装 | Flask not installed）")
        run_tests()
