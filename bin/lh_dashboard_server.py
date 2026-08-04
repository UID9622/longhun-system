#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DASHBOARD-SERVER-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂 · Dashboard 服务端
端口: 9627
功能: 官网首页 + API密钥管理 + 支付状态查询
"""

import os
import sys
import json
import sqlite3
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORTAL_DIR = PROJECT_ROOT / "portal" / "dashboard"
DATA_DIR = PROJECT_ROOT / "data"
KEYS_DB = DATA_DIR / "api_keys.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

# ════════════════════════════════════════════════
# 数据库
# ════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect(str(KEYS_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            provider TEXT PRIMARY KEY,
            api_key_encrypted TEXT NOT NULL,
            balance REAL DEFAULT 0,
            last_checked TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS payment_orders (
            order_no TEXT PRIMARY KEY,
            provider TEXT,
            amount REAL,
            method TEXT,
            status TEXT DEFAULT 'pending',
            qr_code TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            paid_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def _encrypt(text: str) -> str:
    """简单加密（生产环境应用国密SM4）"""
    key = hashlib.sha256(b"longhun-xpay-salt-9622").digest()
    from cryptography.fernet import Fernet
    f = Fernet(base64.urlsafe_b64encode(key[:32]))
    return f.encrypt(text.encode()).decode()

def _decrypt(encrypted: str) -> str:
    key = hashlib.sha256(b"longhun-xpay-salt-9622").digest()
    from cryptography.fernet import Fernet
    f = Fernet(base64.urlsafe_b64encode(key[:32]))
    return f.decrypt(encrypted.encode()).decode()

init_db()

# ════════════════════════════════════════════════
# 主页
# ════════════════════════════════════════════════
@app.route("/")
def index():
    index_file = PORTAL_DIR / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>🐉 龍魂 Dashboard</h1><p>index.html 未找到</p>", 200, {"Content-Type": "text/html; charset=utf-8"}

@app.route("/health")
def health():
    return jsonify({"ok": True, "service": "longhun-dashboard", "port": 9627, "time": datetime.now().isoformat()})

# ════════════════════════════════════════════════
# API密钥管理
# ════════════════════════════════════════════════
@app.route("/api/activation/keys/status")
def keys_status():
    conn = sqlite3.connect(str(KEYS_DB))
    result = {}
    for row in conn.execute("SELECT provider, balance, last_checked FROM api_keys"):
        result[row[0]] = {
            "configured": True,
            "balance": row[1],
            "balance_sufficient": row[1] > 0,
            "last_checked": row[2]
        }
    # 检查未配置的
    for p in ["deepseek", "kimi", "github"]:
        if p not in result:
            result[p] = {"configured": False, "balance": 0, "balance_sufficient": False}
    conn.close()
    return jsonify({"ok": True, **result})

@app.route("/api/activation/keys/save", methods=["POST"])
def keys_save():
    try:
        data = request.get_json()
        provider = data.get("provider", "")
        api_key = data.get("api_key", "")
        if not provider or not api_key:
            return jsonify({"ok": False, "error": "缺少provider或api_key"}), 400

        conn = sqlite3.connect(str(KEYS_DB))
        encrypted = _encrypt(api_key)
        conn.execute(
            "INSERT OR REPLACE INTO api_keys (provider, api_key_encrypted, updated_at) VALUES (?, ?, ?)",
            (provider, encrypted, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        # 更新环境变量
        env_map = {"deepseek": "DEEPSEEK_API_KEY", "kimi": "MOONSHOT_API_KEY", "github": "GITHUB_TOKEN"}
        if provider in env_map:
            os.environ[env_map[provider]] = api_key

        return jsonify({"ok": True, "provider": provider, "message": "API密钥已保存"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/activation/keys/get/<provider>")
def keys_get(provider):
    conn = sqlite3.connect(str(KEYS_DB))
    row = conn.execute("SELECT api_key_encrypted FROM api_keys WHERE provider=?", (provider,)).fetchone()
    conn.close()
    if row:
        try:
            decrypted = _decrypt(row[0])
            return jsonify({"ok": True, "provider": provider, "api_key": decrypted[:8] + "***"})
        except Exception:
            return jsonify({"ok": True, "provider": provider, "api_key": "***（解密失败）"})
    return jsonify({"ok": False, "error": "未配置"}), 404

# ════════════════════════════════════════════════
# 支付订单（支付宝沙箱）
# ════════════════════════════════════════════════
@app.route("/api/activation/order", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        provider = data.get("provider", "deepseek")
        amount = float(data.get("amount", 0))
        method = data.get("method", "alipay")
        description = data.get("description", f"API充值 ¥{amount}")

        if amount <= 0:
            return jsonify({"ok": False, "error": "金额必须大于0"}), 400

        order_no = f"LH{datetime.now().strftime('%Y%m%d%H%M%S')}{os.urandom(3).hex().upper()}"

        # 尝试调用支付宝沙箱
        qr_code = None
        qr_url = None
        alipay_error = None

        try:
            import importlib
            alipay_module = importlib.import_module("payment_providers.alipay_pay")
            # 读取配置
            cert_dir = Path.home() / ".longhun" / "certs"
            priv_key = cert_dir / "alipay_sandbox_app_private_key.pem"
            pub_key = cert_dir / "alipay_sandbox_app_public_key.pem"
            
            if priv_key.exists() and pub_key.exists():
                cfg = {
                    "app_id": os.environ.get("ALIPAY_APP_ID", ""),
                    "app_private_key_path": str(priv_key),
                    "alipay_public_key_path": str(pub_key),
                    "sandbox": True,
                    "notify_url": f"https://uid9622.cn/api/activation/payment/notify/alipay"
                }
                provider_obj = alipay_module.AlipayProvider(cfg)
                from decimal import Decimal
                result = provider_obj.create_order(order_no, Decimal(str(amount)), description)
                if result.get("success"):
                    qr_code = result.get("qr_code")
                else:
                    alipay_error = result.get("error", "支付宝返回异常")
            else:
                alipay_error = "支付宝沙箱证书未配置"
        except ImportError:
            alipay_error = "python-alipay-sdk 未安装"
        except Exception as e:
            alipay_error = str(e)

        # 存储订单
        conn = sqlite3.connect(str(KEYS_DB))
        conn.execute(
            "INSERT INTO payment_orders (order_no, provider, amount, method, status, qr_code) VALUES (?,?,?,?,?,?)",
            (order_no, provider, amount, method, "pending", qr_code or "")
        )
        conn.commit()
        conn.close()

        return jsonify({
            "ok": True,
            "order_no": order_no,
            "amount": amount,
            "provider": provider,
            "qr_code": qr_code,
            "qr_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={order_no}" if not qr_code else None,
            "alipay_error": alipay_error,
            "note": "支付宝沙箱模式下使用备用二维码" if not qr_code else None
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/activation/order/<order_no>/status")
def order_status(order_no):
    conn = sqlite3.connect(str(KEYS_DB))
    row = conn.execute(
        "SELECT order_no, provider, amount, status, created_at, paid_at FROM payment_orders WHERE order_no=?",
        (order_no,)
    ).fetchone()
    conn.close()
    if row:
        return jsonify({
            "ok": True,
            "order_no": row[0],
            "provider": row[1],
            "amount": row[2],
            "status": row[3],
            "created_at": row[4],
            "paid_at": row[5]
        })
    return jsonify({"ok": False, "error": "订单不存在"}), 404

@app.route("/api/activation/payment/notify/alipay", methods=["POST"])
def alipay_notify():
    """支付宝异步通知回调"""
    # 简单记录
    data = request.form.to_dict()
    order_no = data.get("out_trade_no", "")
    trade_status = data.get("trade_status", "")
    
    if trade_status == "TRADE_SUCCESS":
        conn = sqlite3.connect(str(KEYS_DB))
        conn.execute(
            "UPDATE payment_orders SET status='paid', paid_at=? WHERE order_no=?",
            (datetime.now().isoformat(), order_no)
        )
        conn.commit()
        conn.close()
        return "success"
    return "fail"

# ════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9627
    print(f"🐉 龍魂 Dashboard 启动: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
