#!/usr/bin/env python3
"""
龍魂 Notion Webhook 接收器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
簽名人  : UID9622 · 諸葛鑫 · 中國退伍軍人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA     : #龍芯⚡️20260422-NOTION-HOOK01
端口    : :9623 (公網入口，ngrok 穿透)
理論指導: 曾仕強老師（永恒顯示）
原則    : 不黑箱·不收割·不說教·審計即主權

職責:
  ① 接收 Notion 的 Webhook 驗證握手（把 verification_token 落盤+打印）
  ② 接收 Notion 的事件推送（page/database/comment 的增刪改）
  ③ 轉發事件到本機 :9622 審計引擎寫 SQLite
  ④ 可選：HMAC-SHA256 驗簽（Notion 帶 X-Notion-Signature）

與 audit_engine.py 解耦 · 不改動原代碼
"""

import os
import sys
import json
import hmac
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, request, jsonify
import requests as http_req

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
WEBHOOK_PORT    = int(os.environ.get("WEBHOOK_PORT", "9623"))
AUDIT_ENGINE    = "http://127.0.0.1:9622"
DNA_TOKEN       = os.environ.get("DNA_TOKEN", "UID9622-CHANGE-THIS")
VERIFICATION_FILE = Path.home() / "cnsh" / "入口" / "DNA" / "notion_verification.txt"
WEBHOOK_LOG_DIR = Path.home() / "cnsh" / "logs"
# Notion 訂閱確認後會提供 verification token，寫這裡用於後續簽名校驗
NOTION_SIGNING_SECRET = os.environ.get("NOTION_SIGNING_SECRET", "")

VERIFICATION_FILE.parent.mkdir(parents=True, exist_ok=True)
WEBHOOK_LOG_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)


# ═══════════════════════════════════════════════
# 工具
# ═══════════════════════════════════════════════
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_raw(payload: dict, headers: dict):
    """把每條 webhook 原始內容落盤，永遠可追溯"""
    fname = WEBHOOK_LOG_DIR / f"notion_webhook_{datetime.now().strftime('%Y%m%d')}.jsonl"
    record = {
        "ts": now_iso(),
        "headers": {k: v for k, v in headers.items()
                    if k.lower().startswith(("x-notion", "content-type", "user-agent"))},
        "payload": payload,
    }
    with open(fname, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def forward_to_audit(event_type: str, source: str, target: str,
                     payload: dict, note: str = "") -> dict:
    """把事件轉發給 :9622 審計引擎"""
    try:
        resp = http_req.post(
            f"{AUDIT_ENGINE}/audit",
            headers={
                "X-DNA-Token": DNA_TOKEN,
                "Content-Type": "application/json",
            },
            json={
                "event_type": event_type,
                "source": source,
                "target": target,
                "payload": payload,
                "status": "🟢",
                "note": note,
            },
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json()
        return {"error": f"audit_engine_status_{resp.status_code}", "body": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}


def verify_notion_signature(raw_body: bytes, signature_header: str) -> bool:
    """Notion 用 HMAC-SHA256 簽名 · header: X-Notion-Signature: sha256=..."""
    if not NOTION_SIGNING_SECRET or not signature_header:
        return True  # 還沒配 secret 就先放行（訂閱完成後再強校驗）
    try:
        if signature_header.startswith("sha256="):
            signature_header = signature_header[7:]
        expected = hmac.new(
            NOTION_SIGNING_SECRET.encode(),
            raw_body,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)
    except Exception:
        return False


# ═══════════════════════════════════════════════
# 路由
# ═══════════════════════════════════════════════
@app.route("/health")
def health():
    return jsonify({
        "status": "🟢",
        "service": "龍魂 Notion Webhook 接收器",
        "port": WEBHOOK_PORT,
        "downstream": AUDIT_ENGINE,
        "signing_configured": bool(NOTION_SIGNING_SECRET),
    })


@app.route("/notion_webhook", methods=["POST", "GET"])
def notion_webhook():
    """
    Notion Webhook 入口。處理三種情況：
    1) 訂閱握手：Notion POST 一個 {"verification_token": "..."} → 我們落盤+打印
    2) 簽名驗證（可選）：header X-Notion-Signature
    3) 真實事件：轉發到 audit_engine
    """
    if request.method == "GET":
        return jsonify({"hint": "POST only. 這是 Notion Webhook 入口。",
                        "service": "龍魂"}), 200

    raw = request.get_data()
    sig = request.headers.get("X-Notion-Signature", "")

    # === 情況1: 訂閱握手 ===
    try:
        body = request.get_json(force=True, silent=True) or {}
    except Exception:
        body = {}

    log_raw(body, dict(request.headers))

    if "verification_token" in body:
        token = body["verification_token"]
        # 落盤永久保存
        VERIFICATION_FILE.write_text(
            f"# Notion Webhook Verification Token\n"
            f"# 收到時間: {now_iso()}\n"
            f"# 用途: 粘貼回 Notion 集成頁面確認訂閱\n\n"
            f"{token}\n"
        )
        print(f"\n🎫 ══════════ Notion 驗證令牌已到 ══════════")
        print(f"   TOKEN: {token}")
        print(f"   已存: {VERIFICATION_FILE}")
        print(f"   ▶ 把上面 TOKEN 粘貼回 Notion 集成的 Webhook 頁面確認訂閱")
        print(f"═════════════════════════════════════════════\n")

        # 也記一條審計
        forward_to_audit(
            event_type="WEBHOOK",
            source="notion",
            target="verification_handshake",
            payload={"verification_token": token[:8] + "..."},
            note="Notion webhook 訂閱握手",
        )
        # Notion 要求返回 200 即可
        return jsonify({"status": "verification_received",
                        "token_preview": token[:8] + "..."}), 200

    # === 情況2: 簽名驗證 ===
    if not verify_notion_signature(raw, sig):
        forward_to_audit(
            event_type="WEBHOOK",
            source="notion",
            target="signature_fail",
            payload={"sig_header": sig[:50]},
            note="🔴 HMAC 簽名校驗失敗",
        )
        return jsonify({"error": "invalid_signature"}), 401

    # === 情況3: 真實事件 ===
    event_type = body.get("type", "unknown")
    entity = body.get("entity", {}) or body.get("data", {})

    rec = forward_to_audit(
        event_type="WEBHOOK",
        source="notion",
        target=event_type,
        payload=body,
        note=f"Notion事件·{event_type}",
    )

    return jsonify({
        "ok": True,
        "forwarded_to": "audit_engine",
        "audit_id": rec.get("id"),
        "dna": rec.get("dna"),
    }), 200


@app.route("/verification_token")
def show_token():
    """方便查看最近收到的 verification token"""
    if VERIFICATION_FILE.exists():
        return VERIFICATION_FILE.read_text(), 200, {"Content-Type": "text/plain; charset=utf-8"}
    return "還沒收到 verification token。把 ngrok URL + /notion_webhook 填到 Notion 觸發一次即可。", 404


# ═══════════════════════════════════════════════
# 啟動
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════╗
║  龍魂 Notion Webhook 接收器 v1.0         ║
║  UID9622 · 諸葛鑫                        ║
║  DNA: #龍芯⚡️20260422-NOTION-HOOK01      ║
╚══════════════════════════════════════════╝
   端口:     :{WEBHOOK_PORT}  (ngrok 對外入口)
   下游:     {AUDIT_ENGINE}  (audit_engine.py)
   DNA令牌:  {DNA_TOKEN[:10]}...
   驗證簽名: {'✅ 已配置' if NOTION_SIGNING_SECRET else '⚠️  未配置（訂閱完再補）'}

   端點:
     POST /notion_webhook       — Notion webhook 入口
     GET  /verification_token   — 查看最近收到的 verification token
     GET  /health               — 健康檢查
""")
    app.run(host="0.0.0.0", port=WEBHOOK_PORT, debug=False)
