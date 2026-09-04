#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷈小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ACTIVATION-API-v1.0-9E1D4C7B
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# 功能: 龍魂激活经济舱 REST API
# 端口: 9656
"""
龍魂系统 · 激活经济舱 REST API

端点:
  POST /api/activation/order    → 生成订单+二维码
  POST /api/activation/confirm  → 确认到账
  GET  /api/activation/status   → 查询状态
  GET  /api/activation/health   → 健康检查

启动:
  python bin/lh_activation_api.py
"""

import os
import sys
import json
import base64
import io
import sqlite3
import hashlib
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from flask import Flask, request, jsonify

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_payment_activate import LonghunPayment, _parse_amount, _generate_dna, _audit, P0_CONFIG
from lh_mfa_activate import generate_totp_secret, verify_totp_code, LonghunMFA
from payment_providers import get_payment_provider, list_providers
from payment_providers.notifications import notify_payment_confirmed, test_email

try:
    import qrcode
except ImportError:
    qrcode = None

# ═══════════════════════════════════════════════════════════════════════════════
# 审计对抗中枢钩子（左右互搏 + 红蓝对抗 + 数学建模）
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from lh_audit_battle_hub import AuditBattleHub
    AUDIT_HUB = AuditBattleHub()
except Exception as _audit_import_err:
    AUDIT_HUB = None


app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# 管理后台认证
# ═══════════════════════════════════════════════════════════════════════════════

ADMIN_TOKEN = os.environ.get("LONGHUN_ADMIN_TOKEN", P0_CONFIG["confirm"])


def _admin_auth():
    import base64
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False
    try:
        decoded = base64.b64decode(auth[7:]).decode("utf-8")
        return decoded == ADMIN_TOKEN
    except Exception:
        return False


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not _admin_auth():
            return jsonify({"error": "未授权"}), 401
        return f(*args, **kwargs)
    return decorated


def _audit_battle_hook(endpoint: str, problem: str, solution: str, response):
    """将左右互搏审计结果写入响应头（HTTP头仅限latin-1，故剥离emoji）"""
    if not AUDIT_HUB:
        return response
    try:
        result = AUDIT_HUB.duel_decision(problem, solution)
        score = result.get("score", {})
        color_map = {"🟢": "green", "🟡": "yellow", "🔴": "red"}
        raw_color = score.get("color", "")
        response.headers["X-LongHun-Audit-Score"] = str(score.get("overall", "-"))
        response.headers["X-LongHun-Audit-Color"] = color_map.get(raw_color, raw_color)
        response.headers["X-LongHun-Audit-Consensus"] = str(result.get("duel", {}).get("consensus", False))
    except Exception as e:
        response.headers["X-LongHun-Audit-Error"] = str(e)
    return response


def _audit_self_file():
    """启动时对激活 API 自身做一次漏洞扫描"""
    if not AUDIT_HUB:
        return
    try:
        api_file = Path(__file__).resolve()
        report = AUDIT_HUB.audit_target(api_file)
        _audit(
            Path(P0_CONFIG["log_dir"]) / "activation_api.log",
            f"[SELF-AUDIT] 激活 API 自审计 score={report.get('score', {}).get('overall')} color={report.get('score', {}).get('color')}",
        )
    except Exception as e:
        _audit(
            Path(P0_CONFIG["log_dir"]) / "activation_api.log",
            f"[SELF-AUDIT] 自审计失败: {e}",
            "WARN",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SQLite 计数器（真实传播/使用数据）
# ═══════════════════════════════════════════════════════════════════════════════

COUNTER_DB = Path(P0_CONFIG["log_dir"]) / "activation_counters.db"


def _init_counters():
    COUNTER_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS counters (
            name TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS counter_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            delta INTEGER,
            ip TEXT,
            ua TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS run_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            result TEXT,
            error_code TEXT,
            detail TEXT,
            order_id TEXT,
            ip TEXT,
            ua TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            ip TEXT,
            ua TEXT,
            created_at TEXT
        )
    """)
    # seed demo values if empty
    cur.execute("SELECT COUNT(*) FROM counters")
    if cur.fetchone()[0] == 0:
        seed = [("download", 128), ("view", 3842), ("use", 516), ("comment", 47), ("forward", 89)]
        cur.executemany(
            "INSERT INTO counters (name, count, updated_at) VALUES (?, ?, ?)",
            [(n, c, datetime.now().isoformat()) for n, c in seed]
        )
    conn.commit()
    conn.close()


def _counter_get(name: str) -> int:
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO counters (name, count) VALUES (?, 0)", (name,))
    conn.commit()
    cur.execute("SELECT count FROM counters WHERE name=?", (name,))
    val = cur.fetchone()[0]
    conn.close()
    return val


def _counter_inc(name: str, delta: int = 1) -> int:
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    ua = request.headers.get("User-Agent", "")[:200]
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO counters (name, count) VALUES (?, 0)", (name,))
    cur.execute(
        "UPDATE counters SET count=count+?, updated_at=? WHERE name=?",
        (delta, datetime.now().isoformat(), name),
    )
    cur.execute(
        "INSERT INTO counter_log (name, delta, ip, ua, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, delta, ip, ua, datetime.now().isoformat()),
    )
    cur.execute("SELECT count FROM counters WHERE name=?", (name,))
    val = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return val


def _counter_all() -> dict:
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute("SELECT name, count FROM counters")
    rows = dict(cur.fetchall())
    conn.close()
    return rows


def _log_run(action: str, result: str, error_code: str = "", detail: str = "", order_id: str = ""):
    """记录运行日志摘要"""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    ua = request.headers.get("User-Agent", "")[:200]
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO run_log (action, result, error_code, detail, order_id, ip, ua, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (action, result, error_code, detail, order_id, ip, ua, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def _last_run_log(limit: int = 10) -> list:
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute(
        "SELECT action, result, error_code, detail, order_id, created_at FROM run_log ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = [
        {
            "action": r[0],
            "result": r[1],
            "error_code": r[2] or "",
            "detail": r[3] or "",
            "order_id": r[4] or "",
            "created_at": r[5],
        }
        for r in cur.fetchall()
    ]
    conn.close()
    return rows


def _metrics_history(name: str, hours: int = 24) -> list:
    """返回最近 N 小时内每小时的计数增量"""
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    since = (datetime.now().replace(minute=0, second=0, microsecond=0).timestamp() - hours * 3600)
    since_iso = datetime.fromtimestamp(since).isoformat()
    cur.execute(
        """
        SELECT strftime('%Y-%m-%d %H:00:00', created_at) as hour, SUM(delta)
        FROM counter_log
        WHERE name=? AND created_at > ?
        GROUP BY hour
        ORDER BY hour ASC
        """,
        (name, since_iso),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"hour": r[0], "delta": r[1] or 0} for r in rows]


_init_counters()
_audit_self_file()


def _qr_base64(payload: str) -> str:
    if not qrcode:
        return ""
    qr = qrcode.QRCode(version=3, box_size=8, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


@app.after_request
def add_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "dna": "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-ACTIVATION-API-v1.0-9E1D4C7B",
        "confirm": P0_CONFIG["confirm"],
    })


@app.route("/order", methods=["POST"])
def order():
    payload = request.get_json(force=True) or {}
    amount_str = payload.get("amount", "1.00")
    name = payload.get("name", "匿名") or "匿名"
    note = payload.get("note", "")

    try:
        amount = _parse_amount(str(amount_str))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if amount < P0_CONFIG["min_amount"]:
        return jsonify({"error": f"金额不得低于 {P0_CONFIG['min_amount']} 元"}), 400

    lp = LonghunPayment()
    order_id = f"PAY-{datetime.now().strftime('%Y%m%d')}-{os.urandom(4).hex().upper()}"
    # 自定义生成 order 并保存
    dna = _generate_dna(order_id)
    qr_payload = (
        f"龍魂激活订单\n"
        f"订单号: {order_id}\n"
        f"金额: {amount} {P0_CONFIG['currency']}\n"
        f"支付人: {name}\n"
        f"备注: {note or '支持龍魂系统'}\n"
        f"激活舱: https://uid9622.cn/activation-lab/?order={order_id}"
    )

    order_record = {
        "order_id": order_id,
        "amount": str(amount.quantize(Decimal("0.01"))),
        "currency": P0_CONFIG["currency"],
        "name": name,
        "note": note,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "confirmed_at": None,
        "tx_id": None,
        "dna": dna,
    }
    lp.registry["orders"].append(order_record)
    lp.registry["total_orders"] = len(lp.registry["orders"])
    lp._save_registry()
    _audit(lp.audit_path, f"[API] 生成订单: {order_id}, 金额={amount}, 支付人={name}")
    _log_run("order.create", "success", detail=f"金额={amount} 支付人={name}", order_id=order_id)

    response = jsonify({
        "success": True,
        "order_id": order_id,
        "amount": order_record["amount"],
        "currency": order_record["currency"],
        "name": name,
        "dna": dna,
        "qr_base64": _qr_base64(qr_payload),
    })
    return _audit_battle_hook(
        "order",
        f"创建龍魂激活订单：生成支付二维码（金额 {amount} 元）",
        f"订单号={order_id} 支付人={name} 环境=支付渠道沙箱/真实切换",
        response,
    )


@app.route("/confirm", methods=["POST"])
def confirm():
    payload = request.get_json(force=True) or {}
    order_id = payload.get("order_id", "").strip()
    tx_id = payload.get("tx_id", "").strip()

    if not order_id or not tx_id:
        return jsonify({"error": "订单号和交易单号不能为空"}), 400

    lp = LonghunPayment()
    # 复用逻辑但返回 JSON
    order = None
    for o in lp.registry["orders"]:
        if o["order_id"] == order_id:
            order = o
            break

    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order["status"] == "confirmed":
        return jsonify({"error": "订单已确认"}), 400
    if tx_id in lp.registry["tx_ids"]:
        return jsonify({"error": "交易单号已使用"}), 400

    order["status"] = "confirmed"
    order["tx_id"] = tx_id
    order["confirmed_at"] = datetime.now().isoformat()
    lp.registry["tx_ids"].append(tx_id)
    total = Decimal(lp.registry.get("total_amount", "0.00")) + Decimal(order["amount"])
    lp.registry["total_amount"] = str(total.quantize(Decimal("0.01")))
    lp.registry["confirmed_orders"] = sum(1 for o in lp.registry["orders"] if o["status"] == "confirmed")
    lp._save_registry()
    _audit(lp.audit_path, f"[API] 确认到账: {order_id}, tx={tx_id}, 金额={order['amount']}", "SUCCESS")
    _log_run("order.confirm", "success", detail=f"金额={order['amount']}", order_id=order_id)

    response = jsonify({
        "success": True,
        "order_id": order_id,
        "tx_id": tx_id,
        "amount": order["amount"],
        "dna": order["dna"],
        "confirmed_at": order["confirmed_at"],
    })
    return _audit_battle_hook(
        "confirm",
        f"确认龍魂激活订单到账：{order_id}",
        f"交易单号={tx_id} 金额={order['amount']} 状态=confirmed",
        response,
    )


@app.route("/status", methods=["GET"])
def status():
    lp = LonghunPayment()
    total = Decimal(lp.registry.get("total_amount", "0.00"))
    total_orders = lp.registry.get("total_orders", 0)
    confirmed = lp.registry.get("confirmed_orders", 0)
    return jsonify({
        "total_amount": str(total),
        "currency": P0_CONFIG["currency"],
        "total_orders": total_orders,
        "confirmed_orders": confirmed,
        "pending": total_orders - confirmed,
        "orders": lp.registry["orders"][-20:],
        "payment_providers": list_providers(),
        "last_log": _last_run_log(5),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# 真实支付渠道（微信 / 支付宝）
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/payment/providers", methods=["GET"])
def payment_providers():
    """列出可用的支付渠道"""
    return jsonify({
        "providers": list_providers(),
        "manual_fallback": True,
    })


@app.route("/payment/create", methods=["POST"])
def payment_create():
    """调用真实支付渠道生成收款二维码"""
    payload = request.get_json(force=True) or {}
    order_id = payload.get("order_id", "").strip()
    provider_name = payload.get("provider", "wechat_pay").strip()

    if not order_id:
        return jsonify({"error": "order_id 不能为空"}), 400

    lp = LonghunPayment()
    order = next((o for o in lp.registry["orders"] if o["order_id"] == order_id), None)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.get("status") == "confirmed":
        return jsonify({"error": "订单已确认"}), 400

    provider = get_payment_provider(provider_name)
    if not provider:
        return jsonify({
            "error": f"支付渠道 {provider_name} 未启用或凭证未配置",
            "hint": "请配置 config/payment_credentials.yaml，或继续使用手动确认到账",
        }), 503

    amount = Decimal(order["amount"])
    result = provider.create_order(
        out_trade_no=order_id,
        amount=amount,
        description=order.get("note") or "支持龍魂系统",
    )

    if result.get("success"):
        order["payment_provider"] = result["provider"]
        order["payment_out_trade_no"] = result["out_trade_no"]
        lp._save_registry()
        _audit(lp.audit_path, f"[API] 创建真实支付订单: {order_id}, provider={result['provider']}")
        _log_run("payment.create", "success", detail=f"provider={result['provider']} 金额={result['amount']}", order_id=order_id)
        response = jsonify({
            "success": True,
            "order_id": order_id,
            "provider": result["provider"],
            "qr_code": result["qr_code"],
            "amount": result["amount"],
        })
        return _audit_battle_hook(
            "payment.create",
            f"调用真实支付渠道生成收款二维码：{order_id}",
            f"provider={result['provider']} 金额={result['amount']} 沙箱/真实切换=已配置",
            response,
        )
    _log_run("payment.create", "failed", error_code=result.get("error", "UNKNOWN"), detail=f"provider={provider_name}", order_id=order_id)
    return jsonify({"error": result.get("error", "未知错误")}), 502


@app.route("/payment/query", methods=["GET"])
def payment_query():
    """查询真实支付订单状态"""
    order_id = request.args.get("order_id", "").strip()
    if not order_id:
        return jsonify({"error": "order_id 不能为空"}), 400

    lp = LonghunPayment()
    order = next((o for o in lp.registry["orders"] if o["order_id"] == order_id), None)
    if not order:
        return jsonify({"error": "订单不存在"}), 404

    provider_name = order.get("payment_provider")
    if not provider_name:
        return jsonify({"error": "该订单未使用真实支付"}), 400

    provider = get_payment_provider(provider_name)
    if not provider:
        return jsonify({"error": "支付渠道当前不可用"}), 503

    result = provider.query_order(order.get("payment_out_trade_no", order_id))
    # 自动确认
    if result.get("success") and result.get("status") in ("SUCCESS", "TRADE_SUCCESS"):
        if order.get("status") != "confirmed":
            _confirm_order(lp, order, f"AUTO-{provider_name}-{datetime.now().timestamp()}")
        _log_run("payment.query", "success", detail=f"status={result.get('status')} provider={provider_name}", order_id=order_id)
    else:
        _log_run("payment.query", "pending", error_code=result.get("status") or result.get("error", "UNKNOWN"), detail=f"provider={provider_name}", order_id=order_id)
    return jsonify(result)


@app.route("/payment/notify/wechat", methods=["POST"])
def payment_notify_wechat():
    """微信支付异步通知"""
    body = request.get_data(as_text=True)
    provider = get_payment_provider("wechat_pay")
    if not provider:
        return "FAIL", 503

    result = provider.verify_notify(dict(request.headers), body)
    if not result.get("success"):
        return "FAIL", 400

    data = result.get("data", {})
    out_trade_no = data.get("out_trade_no")
    if not out_trade_no:
        return "FAIL", 400

    lp = LonghunPayment()
    order = next((o for o in lp.registry["orders"] if o["order_id"] == out_trade_no), None)
    if order and order.get("status") != "confirmed":
        _confirm_order(lp, order, f"WXNOTIFY-{data.get('transaction_id', '')}")
    return "SUCCESS", 200


@app.route("/payment/notify/alipay", methods=["POST"])
def payment_notify_alipay():
    """支付宝异步通知"""
    data = request.form.to_dict()
    signature = data.pop("sign", "")
    provider = get_payment_provider("alipay")
    if not provider:
        return "fail", 503

    result = provider.verify_notify(data, signature)
    if not result.get("success"):
        return "fail", 400

    out_trade_no = data.get("out_trade_no")
    trade_status = data.get("trade_status")
    if not out_trade_no or trade_status not in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        return "success", 200

    lp = LonghunPayment()
    order = next((o for o in lp.registry["orders"] if o["order_id"] == out_trade_no), None)
    if order and order.get("status") != "confirmed":
        _confirm_order(lp, order, f"ALINOTIFY-{data.get('trade_no', '')}")
    return "success", 200


def _confirm_order(lp: LonghunPayment, order: dict, tx_id: str):
    """统一确认订单到账"""
    if tx_id in lp.registry.get("tx_ids", []):
        return False
    order["status"] = "confirmed"
    order["tx_id"] = tx_id
    order["confirmed_at"] = datetime.now().isoformat()
    lp.registry.setdefault("tx_ids", []).append(tx_id)
    total = Decimal(lp.registry.get("total_amount", "0.00")) + Decimal(order["amount"])
    lp.registry["total_amount"] = str(total.quantize(Decimal("0.01")))
    lp.registry["confirmed_orders"] = sum(1 for o in lp.registry["orders"] if o["status"] == "confirmed")
    lp._save_registry()
    _audit(lp.audit_path, f"[API] 自动确认到账: {order['order_id']}, tx={tx_id}, 金额={order['amount']}", "SUCCESS")
    # 触发邮件/短信通知
    try:
        notify_payment_confirmed(order)
    except Exception as e:
        _audit(lp.audit_path, f"[API] 通知发送失败: {order['order_id']}, error={e}", "WARN")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# MFA / TOTP 扫码绑定（Web 端）
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/mfa/generate", methods=["POST", "GET"])
def mfa_generate():
    """生成 TOTP 密钥与二维码"""
    secret = generate_totp_secret()
    account = request.args.get("account") or request.get_json(force=True, silent=True) or {}
    if isinstance(account, dict):
        account = account.get("account", "longhun@uid9622.cn")
    issuer = "龍魂系统-UID9622"
    provisioning_uri = (
        f"otpauth://totp/{issuer}:{account}?secret={secret}"
        f"&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
    )
    qr = qrcode.QRCode(version=3, box_size=8, border=2)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return jsonify({
        "success": True,
        "secret": secret,
        "account": account,
        "issuer": issuer,
        "provisioning_uri": provisioning_uri,
        "qr_base64": qr_b64,
        "hint": "请用华为账号 / Google Authenticator / Authy / 微软 Authenticator 扫码",
    })


@app.route("/mfa/verify", methods=["POST"])
def mfa_verify():
    """验证 TOTP 动态码是否正确（不记录绑定）"""
    payload = request.get_json(force=True) or {}
    secret = payload.get("secret", "").strip()
    code = payload.get("code", "").strip()
    if not secret or not code:
        return jsonify({"valid": False, "error": "secret 和 code 不能为空"}), 400
    return jsonify({"valid": verify_totp_code(secret, code), "secret": secret[:4] + "****"})


@app.route("/mfa/bind", methods=["POST"])
def mfa_bind():
    """绑定 MFA 到订单并完成激活"""
    payload = request.get_json(force=True) or {}
    order_id = payload.get("order_id", "").strip()
    secret = payload.get("secret", "").strip()
    code = payload.get("code", "").strip()
    device_name = payload.get("device_name", "web-browser").strip() or "web-browser"

    if not order_id or not secret or not code:
        return jsonify({"error": "订单号、密钥、动态码不能为空"}), 400

    # 1. 验证订单已确认
    lp = LonghunPayment()
    order = next((o for o in lp.registry["orders"] if o["order_id"] == order_id), None)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.get("status") != "confirmed":
        return jsonify({"error": "订单尚未确认到账，请先完成支付确认"}), 400
    if order.get("mfa_bound"):
        return jsonify({"error": "该订单已绑定 MFA"}), 400

    # 2. 验证 TOTP
    if not verify_totp_code(secret, code):
        return jsonify({"error": "动态码错误，请重新输入"}), 400

    # 3. 写入 MFA registry
    mfa = LonghunMFA()
    device_id = f"{device_name}-{hashlib.sha256((order_id+secret).encode()).hexdigest()[:8]}"
    if device_id in mfa.registry.get("bindings", {}):
        return jsonify({"error": "该设备已绑定"}), 400

    mfa.registry.setdefault("bindings", {})[device_id] = {
        "secret": secret,
        "device_name": device_name,
        "order_id": order_id,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "last_activated": datetime.now().isoformat(),
    }
    mfa.registry.setdefault("used_codes", []).append(code)
    mfa._save_registry()

    # 4. 标记订单已 MFA 绑定
    order["mfa_bound"] = True
    order["mfa_device_id"] = device_id
    lp._save_registry()
    _audit(lp.audit_path, f"[API] 订单 {order_id} 完成 MFA 绑定: device={device_id}", "SUCCESS")
    _log_run("mfa.bind", "success", detail=f"device={device_id}", order_id=order_id)

    response = jsonify({
        "success": True,
        "order_id": order_id,
        "device_id": device_id,
        "dna": order["dna"],
        "message": "MFA 绑定成功，核心功能已激活",
    })
    return _audit_battle_hook(
        "mfa.bind",
        f"绑定 MFA 设备完成核心功能激活：{order_id}",
        f"device={device_id} 动态码已校验 状态=mfa_bound",
        response,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 真实传播/使用计数器 API
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/metrics/counter", methods=["GET"])
def metrics_counter_get():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({"error": "name 不能为空"}), 400
    return jsonify({"name": name, "count": _counter_get(name)})


@app.route("/metrics/counter", methods=["POST"])
def metrics_counter_post():
    payload = request.get_json(force=True) or {}
    name = payload.get("name", "").strip()
    delta = int(payload.get("delta", 1))
    comment = payload.get("comment", "").strip()
    if not name:
        return jsonify({"error": "name 不能为空"}), 400
    new_val = _counter_inc(name, delta)
    if comment and name == "comment":
        ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
        ua = request.headers.get("User-Agent", "")[:200]
        conn = sqlite3.connect(str(COUNTER_DB))
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO comments (name, content, ip, ua, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, comment[:500], ip, ua, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
    _log_run("metrics.counter", "success", detail=f"name={name} delta={delta}")
    return jsonify({"name": name, "count": new_val, "delta": delta})


@app.route("/metrics/all", methods=["GET"])
def metrics_counter_all():
    return jsonify(_counter_all())


@app.route("/notify/test", methods=["POST"])
@admin_required
def notify_test():
    """测试邮件通知配置"""
    result = test_email()
    _log_run("notify.test", "success" if result.get("success") else "failed", error_code=result.get("error", ""))
    return jsonify(result)


# ═══════════════════════════════════════════════════════════════════════════════
# 管理后台 API
# ═══════════════════════════════════════════════════════════════════════════════

@app.route("/admin/config", methods=["GET"])
def admin_config():
    """返回管理后台配置（不包含真实 token）"""
    return jsonify({
        "auth_required": True,
        "hint": "使用 #CONFIRM 确认码作为 Bearer Token",
    })


@app.route("/admin/orders", methods=["GET"])
@admin_required
def admin_orders():
    """返回所有订单"""
    lp = LonghunPayment()
    orders = lp.registry.get("orders", [])[::-1]
    status_filter = request.args.get("status", "").strip()
    if status_filter:
        orders = [o for o in orders if o.get("status") == status_filter]
    return jsonify({
        "total": len(orders),
        "confirmed": sum(1 for o in orders if o.get("status") == "confirmed"),
        "pending": sum(1 for o in orders if o.get("status") == "pending"),
        "orders": orders,
    })


@app.route("/admin/comments", methods=["GET"])
@admin_required
def admin_comments():
    """返回所有评论"""
    limit = int(request.args.get("limit", 100))
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute(
        "SELECT name, content, ip, ua, created_at FROM comments ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = [{"name": r[0], "content": r[1], "ip": r[2], "ua": r[3], "created_at": r[4]} for r in cur.fetchall()]
    conn.close()
    return jsonify({"comments": rows})


@app.route("/admin/logs", methods=["GET"])
@admin_required
def admin_logs():
    """返回运行日志"""
    limit = int(request.args.get("limit", 100))
    return jsonify({"logs": _last_run_log(limit)})


@app.route("/admin/stats", methods=["GET"])
@admin_required
def admin_stats():
    """返回管理统计"""
    lp = LonghunPayment()
    total = Decimal(lp.registry.get("total_amount", "0.00"))
    orders = lp.registry.get("orders", [])
    confirmed = [o for o in orders if o.get("status") == "confirmed"]
    return jsonify({
        "total_amount": str(total),
        "total_orders": len(orders),
        "confirmed_orders": len(confirmed),
        "pending_orders": len(orders) - len(confirmed),
        "mfa_bound": sum(1 for o in confirmed if o.get("mfa_bound")),
        "providers": list_providers(),
        "counters": _counter_all(),
    })


@app.route("/metrics/history", methods=["GET"])
def metrics_counter_history():
    name = request.args.get("name", "").strip()
    hours = int(request.args.get("hours", 24))
    if not name:
        return jsonify({"error": "name 不能为空"}), 400
    return jsonify({"name": name, "hours": hours, "data": _metrics_history(name, hours)})


@app.route("/metrics/comments", methods=["GET"])
def metrics_comments():
    limit = int(request.args.get("limit", 20))
    conn = sqlite3.connect(str(COUNTER_DB))
    cur = conn.cursor()
    cur.execute(
        "SELECT name, content, created_at FROM comments ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = [{"name": r[0], "content": r[1], "created_at": r[2]} for r in cur.fetchall()]
    conn.close()
    return jsonify({"comments": rows})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9656)
    args = parser.parse_args()
    print("#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-ACTIVATION-API-v1.0-9E1D4C7B")
    print(f"🎫 龍魂激活经济舱 API 启动: http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, threaded=True)
