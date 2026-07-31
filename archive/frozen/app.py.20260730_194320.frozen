#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂令系统 · LongHun Orders
公开裁决平台
DNA: #龍芯⚡️2026-06-28-LONGHUN-ORDERS-v1.0
"""
import os
import re
import hashlib
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, flash
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("LONGHUN_ORDERS_DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "orders.db"

APP_NAME = "龍魂令"
APP_VERSION = "1.0"
SYSTEM_UID = "UID9622"
SOVEREIGNTY = "本系统归属中华人民共和国 · 数据根留中国 · 令出即锚 · 锚定即追溯 · 追溯即公示"

LEVELS = [
    {"id": 1, "name": "问询令", "icon": "☵", "tone": "水洄", "desc": "事实不清，先问后裁，给予说明机会。", "evidence": "至少 1 层来源 + 时间戳"},
    {"id": 2, "name": "警示令", "icon": "☶", "tone": "山止", "desc": "行为越界，公开警示，限期整改。", "evidence": "至少 2 层独立来源 + 证据摘要"},
    {"id": 3, "name": "封禁令", "icon": "☲", "tone": "火明", "desc": "严重违规，冻结权限，阻断传播。", "evidence": "至少 3 层来源链 + 哈希固化"},
    {"id": 4, "name": "追缉令", "icon": "☰", "tone": "天行", "desc": "触犯底线，全网追溯，永久公示。", "evidence": "六层来源链 + GPG签名 + 链式哈希"},
]

STATUSES = ["draft", "anchored", "reviewing", "effective", "public", "closed", "revoked"]
STATUS_LABELS = {
    "draft": "起草中",
    "anchored": "已锚定",
    "reviewing": "审核中",
    "effective": "已生效",
    "public": "已公示",
    "closed": "已结案",
    "revoked": "已撤销",
}

app = Flask(__name__, static_url_path="/orders/static", static_folder="static")
app.secret_key = os.environ.get("LONGHUN_ORDERS_SECRET", secrets.token_hex(32))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def generate_dna(tag: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    h = hashlib.blake2b(f"{ts}-{tag}".encode(), digest_size=8).hexdigest()
    return f"#龍芯⚡️{ts}-{tag}-{h.upper()}"


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anchor_id TEXT UNIQUE NOT NULL,
            level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 4),
            title TEXT NOT NULL,
            description TEXT,
            issuer_uid TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'anchored',
            evidence_summary TEXT,
            evidence_hash TEXT,
            progress INTEGER DEFAULT 0,
            is_public INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            dna TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_anchor ON orders(anchor_id);
        CREATE INDEX IF NOT EXISTS idx_status ON orders(status);
        CREATE INDEX IF NOT EXISTS idx_public ON orders(is_public);
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


def require_secret(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        expected = os.environ.get("LONGHUN_ORDERS_INITIATE_KEY")
        if not expected:
            abort(403, "发起入口未配置密钥")
        token = request.headers.get("X-LongHun-Key", "") or request.form.get("initiate_key", "")
        if not secrets.compare_digest(token, expected):
            if request.method == "POST":
                flash("密钥错误，仅 UID9622 可发起龍魂令", "error")
                return redirect(url_for("initiate"))
            abort(403, "密钥错误")
        return f(*args, **kwargs)
    return decorated


@app.route("/orders/")
def index():
    return render_template(
        "index.html",
        levels=LEVELS,
        sovereignty=SOVEREIGNTY,
        dna=generate_dna("ORDERS-INDEX"),
        app_name=APP_NAME,
    )


@app.route("/orders/status/<anchor_id>")
def status(anchor_id):
    if not re.match(r"^[A-Z0-9_-]{4,64}$", anchor_id, re.I):
        abort(404)
    conn = get_db()
    row = conn.execute("SELECT * FROM orders WHERE anchor_id = ?", (anchor_id,)).fetchone()
    conn.close()
    if not row:
        return render_template(
            "status.html",
            found=False,
            anchor_id=anchor_id,
            sovereignty=SOVEREIGNTY,
            dna=generate_dna("ORDERS-STATUS-NOTFOUND"),
            app_name=APP_NAME,
        ), 404
    order = row_to_dict(row)
    level = LEVELS[order["level"] - 1]
    return render_template(
        "status.html",
        found=True,
        order=order,
        level=level,
        status_label=STATUS_LABELS.get(order["status"], order["status"]),
        sovereignty=SOVEREIGNTY,
        dna=order["dna"],
        app_name=APP_NAME,
    )


@app.route("/orders/initiate", methods=["GET", "POST"])
@require_secret
def initiate():
    if request.method == "POST":
        level = int(request.form.get("level", 1))
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        evidence_summary = request.form.get("evidence_summary", "").strip()
        issuer_uid = request.form.get("issuer_uid", SYSTEM_UID).strip() or SYSTEM_UID
        make_public = bool(request.form.get("make_public"))
        if not title or level < 1 or level > 4:
            flash("标题和令级必填", "error")
            return redirect(url_for("initiate"))
        anchor_id = f"ORD-{secrets.token_hex(8).upper()}"
        evidence_hash = hashlib.sha256(evidence_summary.encode()).hexdigest()[:16]
        dna = generate_dna(f"ORDERS-INITIATE-{anchor_id}")
        now = now_iso()
        conn = get_db()
        conn.execute(
            """INSERT INTO orders
            (anchor_id, level, title, description, issuer_uid, status,
             evidence_summary, evidence_hash, progress, is_public, created_at, updated_at, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (anchor_id, level, title, description, issuer_uid,
             "public" if make_public else "anchored", evidence_summary, evidence_hash,
             10 if make_public else 0, 1 if make_public else 0, now, now, dna),
        )
        conn.commit()
        conn.close()
        flash(f"龍魂令已锚定：{anchor_id}", "success")
        return redirect(url_for("status", anchor_id=anchor_id))
    return render_template(
        "initiate.html",
        levels=LEVELS,
        sovereignty=SOVEREIGNTY,
        dna=generate_dna("ORDERS-INITIATE"),
        app_name=APP_NAME,
    )


@app.route("/orders/bulletin")
def bulletin():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM orders WHERE is_public = 1 OR status IN ('effective','public') ORDER BY created_at DESC LIMIT 100"
    ).fetchall()
    conn.close()
    orders = [row_to_dict(r) for r in rows]
    for o in orders:
        o["level_info"] = LEVELS[o["level"] - 1]
        o["status_label"] = STATUS_LABELS.get(o["status"], o["status"])
        o["evidence_summary_masked"] = _mask_evidence(o.get("evidence_summary", ""))
    return render_template(
        "bulletin.html",
        orders=orders,
        sovereignty=SOVEREIGNTY,
        dna=generate_dna("ORDERS-BULLETIN"),
        app_name=APP_NAME,
    )


def _mask_evidence(text: str) -> str:
    if not text:
        return "（无摘要）"
    if len(text) <= 24:
        return text
    return text[:12] + " *** " + text[-12:]


@app.route("/orders-api/health")
def health():
    return jsonify({"status": "ok", "dna": generate_dna("ORDERS-HEALTH")})


@app.route("/orders-api/list")
def api_list():
    conn = get_db()
    rows = conn.execute(
        "SELECT anchor_id, level, title, status, created_at, dna FROM orders WHERE is_public = 1 ORDER BY created_at DESC LIMIT 100"
    ).fetchall()
    conn.close()
    return jsonify({"orders": [row_to_dict(r) for r in rows], "dna": generate_dna("ORDERS-API-LIST")})


def seed_demo_order():
    conn = get_db()
    exists = conn.execute("SELECT 1 FROM orders LIMIT 1").fetchone()
    if not exists:
        now = now_iso()
        dna = generate_dna("ORDERS-DEMO")
        conn.execute(
            """INSERT INTO orders
            (anchor_id, level, title, description, issuer_uid, status,
             evidence_summary, evidence_hash, progress, is_public, created_at, updated_at, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("ORD-DEMO-9622", 2, "占位测试：网络水军警示令",
             "针对某平台批量造谣账号的警示令，证据链已固化。",
             SYSTEM_UID, "public",
             "截图矩阵 12 张 + GPG 签名链 3 条 + 时间戳 2026-06-28T00:00:00Z",
             hashlib.sha256(b"demo-evidence").hexdigest()[:16],
             35, 1, now, now, dna),
        )
        conn.commit()
    conn.close()


init_db()
seed_demo_order()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8446, debug=False)
