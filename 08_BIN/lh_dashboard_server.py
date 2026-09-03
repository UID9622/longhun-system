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
ADMIN_DIR = PROJECT_ROOT / "portal" / "admin"
BCM_DIR = PROJECT_ROOT / "portal"
CHANGELOG_DIR = PROJECT_ROOT / "portal" / "changelog"
DATA_DIR = PROJECT_ROOT / "data"
KEYS_DB = DATA_DIR / "api_keys.db"
ANNOUNCEMENTS_FILE = DATA_DIR / "announcements.json"
ADMIN_PASSWORD = "longhun-admin-9622"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# 确保公告文件存在
if not ANNOUNCEMENTS_FILE.exists():
    ANNOUNCEMENTS_FILE.write_text("[]", encoding="utf-8")

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
# 行为密码学页面
# ════════════════════════════════════════════════
@app.route("/bcm/")
@app.route("/bcm")
def bcm_page():
    bcm_file = BCM_DIR / "behavioral-crypto.html"
    if bcm_file.exists():
        return bcm_file.read_text(encoding="utf-8"), 200, {"Content-Type": "text/html; charset=utf-8"}
    return "<h1>🔬 行为密码学</h1><p>页面未部署，请上传 behavioral-crypto.html</p>", 200, {"Content-Type": "text/html; charset=utf-8"}

@app.route("/bcm/health")
def bcm_health():
    import urllib.request
    try:
        req = urllib.request.Request("http://127.0.0.1:8775/health")
        resp = urllib.request.urlopen(req, timeout=2)
        return jsonify({"ok": True, "bcm": json.loads(resp.read())})
    except Exception as e:
        return jsonify({"ok": True, "bcm": "offline", "error": str(e)})

# ════════════════════════════════════════════════
# 管理后台页面
# ════════════════════════════════════════════════
@app.route("/admin/")
@app.route("/admin")
def admin_page():
    admin_file = ADMIN_DIR / "index.html"
    if admin_file.exists():
        return admin_file.read_text(encoding="utf-8"), 200, {"Content-Type": "text/html; charset=utf-8"}
    return "<h1>⚙️ 管理后台</h1><p>后台页面未部署</p>", 200, {"Content-Type": "text/html; charset=utf-8"}

def _admin_auth():
    token = request.headers.get("X-Admin-Token", "")
    return token and token.startswith("YWRtaW46")  # base64 of "admin:"

# ════════════════════════════════════════════════
# 公告 API（公开）
# ════════════════════════════════════════════════
@app.route("/api/announcements")
def list_announcements():
    try:
        announcements = json.loads(ANNOUNCEMENTS_FILE.read_text(encoding="utf-8"))
        limit = int(request.args.get("limit", 5))
        items = announcements[-limit:][::-1]  # 最新在前
        return jsonify({"ok": True, "items": items, "total": len(announcements)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "items": []})

@app.route("/changelog/")
@app.route("/changelog")
def changelog_page():
    try:
        announcements = json.loads(ANNOUNCEMENTS_FILE.read_text(encoding="utf-8"))
        items_html = "".join([
            f'<div class="ann-item"><div class="ann-date">{a["date"]} · <span class="tag {a.get("tag","announcement")}">{a.get("tag","公告")}</span></div><div class="ann-title">{a["title"]}</div><div class="ann-body">{a["body"]}</div></div>'
            for a in reversed(announcements)
        ]) if announcements else '<p>暂无公告</p>'

        return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>📋 龍魂 · 公告日志</title>
<style>
:root{{--bg:#080c14;--surface:#111827;--border:#243044;--text:#e2e8f0;--text2:#94a3b8;--text3:#64748b;--gold:#f0c040;--primary:#3b82f6;--green:#22c55e;--orange:#f59e0b;--red:#ef4444}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.65}}
.container{{max-width:800px;margin:0 auto;padding:40px 20px}}
h1{{color:var(--gold);text-align:center;margin-bottom:10px;font-size:1.8em}}
.back{{text-align:center;margin-bottom:30px}}
.back a{{color:var(--primary);text-decoration:none;font-size:0.85em}}
.ann-item{{padding:16px 20px;background:var(--surface);border:1px solid var(--border);border-radius:12px;margin-bottom:12px;border-left:3px solid var(--gold)}}
.ann-date{{font-size:0.72em;color:var(--text3);margin-bottom:4px}}
.ann-title{{font-weight:700;font-size:0.95em;margin-bottom:4px}}
.ann-body{{font-size:0.82em;color:var(--text2)}}
.tag{{display:inline-block;padding:2px 8px;font-size:0.65em;border-radius:10px;font-weight:600;margin-right:6px}}
.tag.update{{background:rgba(59,130,246,.15);color:var(--primary)}}
.tag.feature{{background:rgba(34,197,94,.15);color:var(--green)}}
.tag.maintenance{{background:rgba(245,158,11,.15);color:var(--orange)}}
.tag.security{{background:rgba(239,68,68,.15);color:var(--red)}}
footer{{text-align:center;padding:30px;color:var(--text2);font-size:0.7em}}
</style></head><body>
<div class="container">
<h1>📋 龍魂公告日志</h1>
<div class="back"><a href="/">← 返回首页</a></div>
{items_html}
</div>
<footer>DNA: #龍芯⚡️uid9622.cn · 诸葛鑫(UID9622)</footer>
</body></html>""", 200, {"Content-Type": "text/html; charset=utf-8"}
    except Exception as e:
        return f"<h1>公告加载失败</h1><p>{e}</p>", 500, {"Content-Type": "text/html; charset=utf-8"}

# ════════════════════════════════════════════════
# 公告 API（管理端 - 需认证）
# ════════════════════════════════════════════════
@app.route("/api/admin/announcements", methods=["GET", "POST"])
def admin_announcements():
    if not _admin_auth():
        return jsonify({"ok": False, "error": "未授权"}), 401

    if request.method == "GET":
        try:
            announcements = json.loads(ANNOUNCEMENTS_FILE.read_text(encoding="utf-8"))
            return jsonify({"ok": True, "items": announcements, "total": len(announcements)})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)})

    elif request.method == "POST":
        try:
            data = request.get_json()
            tag = data.get("tag", "announcement")
            title = data.get("title", "").strip()
            body = data.get("body", "").strip()
            if not title or not body:
                return jsonify({"ok": False, "error": "标题和内容不能为空"}), 400

            announcements = json.loads(ANNOUNCEMENTS_FILE.read_text(encoding="utf-8"))
            new_id = max([a.get("id", 0) for a in announcements], default=0) + 1
            announcements.append({
                "id": new_id,
                "tag": tag,
                "title": title,
                "body": body,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            ANNOUNCEMENTS_FILE.write_text(json.dumps(announcements, ensure_ascii=False, indent=2), encoding="utf-8")
            return jsonify({"ok": True, "id": new_id, "message": "公告已发布"})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/admin/announcements/<int:ann_id>", methods=["DELETE"])
def delete_announcement(ann_id):
    if not _admin_auth():
        return jsonify({"ok": False, "error": "未授权"}), 401
    try:
        announcements = json.loads(ANNOUNCEMENTS_FILE.read_text(encoding="utf-8"))
        announcements = [a for a in announcements if a.get("id") != ann_id]
        ANNOUNCEMENTS_FILE.write_text(json.dumps(announcements, ensure_ascii=False, indent=2), encoding="utf-8")
        return jsonify({"ok": True, "message": "已删除"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ════════════════════════════════════════════════
# 引擎状态代理
# ════════════════════════════════════════════════
@app.route("/api/engine/<int:port>/health")
def engine_health(port):
    import urllib.request
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/health")
        resp = urllib.request.urlopen(req, timeout=2)
        data = json.loads(resp.read())
        return jsonify(data)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "port": port})

# ════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9627
    print(f"🐉 龍魂 Portal 启动: http://127.0.0.1:{port}")
    print(f"   📋 公告系统: {ANNOUNCEMENTS_FILE} ({len(json.loads(ANNOUNCEMENTS_FILE.read_text('utf-8')))}条)")
    print(f"   🔬 BCM页面: {BCM_DIR}/behavioral-crypto.html")
    print(f"   ⚙️ 管理后台: /admin/")
    app.run(host="127.0.0.1", port=port, debug=False)
