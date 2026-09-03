#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龙魂API网关 v1.2（五锁融合）
DNA: #龍芯⚡️2026-08-31-GATEWAY-v1.2-UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能:
  1. 第一锁 · 身份认证: API Key（明文兼容）+ HMAC-SHA256 签名（哈希作 key，P0 兼容）
  2. 第二锁 · 防盗刷: 四层令牌桶（全局/用户/接口/IP），Redis 可选
  3. 第三锁 · 防重放: 时间戳 + Nonce（300s 窗口）
  4. 第四锁 · IP 白名单: 网关层可选 + Nginx geo 模板
  5. 第五锁 · 密钥管理: 库中只存 SHA-256 + 90 天轮换（rotate_keys.py）
  6. 审计日志: 全链路元数据（不存请求内容，P0）
  7. 计费: 免费额度/按量阶梯/订阅套餐
"""

import hashlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, g, jsonify, request

sys.path.insert(0, str(Path(__file__).parent))

from auth import generate_api_key, get_api_key, get_plan, verify_api_key  # noqa: E402
from config import load_config  # noqa: E402
from db import init_db, prune_call_logs, write_audit  # noqa: E402
from limiter import get_limiter  # noqa: E402
from meter import (  # noqa: E402
    add_balance,
    deduct_balance,
    get_balance,
    get_daily_usage,
    increment_daily_usage,
    log_call,
)
from plans import PLANS, create_subscription, get_remaining_calls, get_subscription  # noqa: E402
from security import get_ip_whitelist, get_nonce_guard, sha256_hex, verify_hmac  # noqa: E402

init_db()
prune_call_logs(days=90)
config = load_config()

app = Flask(__name__)

# ─── 公开路径（无需鉴权） ───
PUBLIC_PATHS = {"/auth/register", "/docs", "/health", "/"}
SIGNATURE_REQUIRED = bool(config.get("security", {}).get("signature_required", False))


def _authed() -> bool:
    return hasattr(g, "key_id")


def _client_ip() -> str:
    return str(
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP", "")
        or request.remote_addr
        or ""
    )


def _deny(code: str, msg: str, status: int = 401) -> Any:
    return jsonify({"error": msg, "code": code}), status


@app.before_request
def authenticate() -> Any | None:
    """第一锁 + 第三锁：双模式鉴权（明文兼容 / HMAC 签名）+ 防重放。"""
    if request.path in PUBLIC_PATHS:
        return None

    key_id = request.headers.get("X-Api-Key") or request.headers.get("X-API-Key-ID", "")
    if not key_id:
        return _deny("AUTH_001", "Missing API Key")

    api_key = get_api_key(key_id)
    if not api_key:
        return _deny("AUTH_002", "Invalid API Key")

    signature = request.headers.get("X-Signature", "")
    timestamp_hdr = request.headers.get("X-Timestamp", "")
    nonce = request.headers.get("X-Nonce", "")

    # 出现任一 HMAC 头（signature/timestamp/nonce）或强制开启 → HMAC 模式
    use_hmac = bool(signature) or bool(timestamp_hdr) or bool(nonce) or SIGNATURE_REQUIRED
    if use_hmac:
        # ── HMAC 签名模式（公网推荐） ──
        if not (timestamp_hdr and nonce):
            return _deny("AUTH_003", "HMAC mode requires X-Timestamp and X-Nonce")
        try:
            ts = int(timestamp_hdr)
        except ValueError:
            return _deny("AUTH_004", "Invalid X-Timestamp")

        # 第三锁 · 防重放
        ok, msg = get_nonce_guard().check(key_id, nonce, ts)
        if not ok:
            return _deny("AUTH_005", msg, 401)

        # 第一锁 · 验签（哈希作 HMAC key）
        body_hash = sha256_hex(request.get_data())
        ok, msg = verify_hmac(
            api_key["key_secret"], signature, request.method, request.path, body_hash, ts, nonce
        )
        if not ok:
            return _deny("AUTH_006", msg)
        g.auth_mode = "hmac"
    else:
        # ── 明文模式（内网/开发兼容） ──
        secret = request.headers.get("X-API-Key-Secret", "")
        if not secret or not verify_api_key(key_id, secret):
            return _deny("AUTH_002", "Invalid API Key")
        g.auth_mode = "simple"

    g.key_id = key_id
    g.api_key = api_key
    g.plan = api_key["plan"]
    return None


@app.before_request
def ip_whitelist() -> Any | None:
    """第四锁 · IP 白名单（网关层可选）。"""
    if request.path in PUBLIC_PATHS:
        return None
    wl = get_ip_whitelist()
    if wl.enabled and not wl.check(_client_ip()):
        return _deny("IPWL_001", "IP not in whitelist", 403)
    return None


@app.before_request
def rate_limit() -> Any | None:
    """第二锁 · 四层令牌桶限流。"""
    if not _authed() or request.path in PUBLIC_PATHS:
        return None
    if request.path.startswith("/auth") or request.path == "/balance":
        return None  # 管理接口不计费不限流（自身防刷靠认证）

    ok, msg = get_limiter().allow(g.plan, request.path, _client_ip())
    if not ok:
        g.rate_limited = 1
        return _deny("RATE_001", msg, 429)
    return None


@app.before_request
def billing() -> Any | None:
    """计费闸：免费层查日额度 · 按量层查余额 · 订阅层查月度剩余。仅对 /v1/* 调用计费。"""
    if not _authed() or request.path in PUBLIC_PATHS:
        return None
    if request.path.startswith("/auth") or request.path == "/balance":
        return None  # 管理接口不计费

    plan = g.plan
    if plan == "free":
        daily_limit = PLANS.get(plan, {}).get("daily_calls", 100)
        if get_daily_usage(g.key_id) >= daily_limit:
            return jsonify(
                {
                    "error": "Daily quota exceeded",
                    "code": "QUOTA_001",
                    "limit": daily_limit,
                    "used": get_daily_usage(g.key_id),
                    "reset": "tomorrow",
                }
            ), 402
    elif plan == "pay_as_you_go":
        if get_balance(g.key_id) <= 0:
            return jsonify(
                {"error": "Insufficient balance", "code": "BAL_001", "balance": get_balance(g.key_id)}
            ), 402
    elif plan in ("basic", "pro", "enterprise"):
        remaining = get_remaining_calls(g.key_id)
        if remaining == 0:
            return jsonify(
                {"error": "Monthly call quota exceeded", "code": "QUOTA_002", "plan": plan}
            ), 402
    return None


@app.after_request
def audit(resp: Any) -> Any:
    """审计日志（只记元数据，不记请求内容，P0）。"""
    try:
        write_audit(
            key_id=getattr(g, "key_id", ""),
            endpoint=request.path,
            method=request.method,
            ip=_client_ip(),
            status_code=resp.status_code,
            response_time=time.time() - getattr(g, "_start", time.time()),
            auth_mode=getattr(g, "auth_mode", ""),
            signature_valid=1 if getattr(g, "auth_mode", "") in ("hmac", "simple") else 0,
            rate_limited=getattr(g, "rate_limited", 0),
        )
    except Exception:  # noqa: BLE001 审计失败不影响业务
        pass
    return resp


# ─── 路由：根/文档 ───
@app.route("/")
def index() -> Any:
    return jsonify(
        {
            "service": "longhun-gateway",
            "version": "1.2",
            "dna": "#龍芯⚡️2026-08-31-GATEWAY-v1.2-UID9622",
            "endpoints": ["/health", "/auth/register", "/auth/topup", "/auth/subscribe", "/balance", "/v1/chat"],
        }
    )


@app.route("/health")
def health() -> Any:
    return jsonify({"status": "healthy", "service": "longhun-gateway", "version": "1.2"})


# ─── 路由：注册 API Key ───
@app.route("/auth/register", methods=["POST"])
def register() -> Any:
    data = request.get_json(silent=True) or {}
    owner = str(data.get("owner", "unknown"))[:64]
    plan = data.get("plan", "free")

    # 只允许注册免费/按量；订阅套餐必须走 /auth/subscribe（需已有 Key + 鉴权）
    if plan not in ("free", "pay_as_you_go"):
        return jsonify({"error": "订阅套餐请走 /auth/subscribe", "code": "PLAN_001"}), 400

    result = generate_api_key(owner, plan)
    return jsonify(
        {
            "key_id": result["key_id"],
            "key_secret": result["key_secret"],
            "plan": plan,
            "note": "保存好 key_secret，丢失无法找回（库中只存哈希）",
        }
    )


# ─── 路由：查询余额/用量 ───
@app.route("/balance")
def balance() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401

    daily_used = get_daily_usage(g.key_id)
    daily_limit = PLANS.get(g.plan, {}).get("daily_calls")
    remaining = get_remaining_calls(g.key_id)

    return jsonify(
        {
            "key_id": g.key_id,
            "plan": g.plan,
            "daily": (
                {"used": daily_used, "limit": daily_limit, "remaining": daily_limit - daily_used}
                if daily_limit
                else {"used": daily_used, "limit": None}
            ),
            "balance": get_balance(g.key_id),
            "subscription_remaining": remaining if remaining >= 0 else "unlimited",
            "subscription": (
                {"plan": get_subscription(g.key_id)["plan"], "expires_at": get_subscription(g.key_id)["expires_at"]}
                if get_subscription(g.key_id)
                else None
            ),
        }
    )


# ─── 路由：充值 ───
@app.route("/auth/topup", methods=["POST"])
def topup() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401
    if g.plan in ("basic", "pro", "enterprise"):
        return jsonify({"error": "订阅用户无需充值", "code": "PLAN_002"}), 400

    data = request.get_json(silent=True) or {}
    amount = float(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    add_balance(g.key_id, amount)
    return jsonify({"key_id": g.key_id, "added": amount, "new_balance": get_balance(g.key_id)})


# ─── 路由：订阅套餐 ───
@app.route("/auth/subscribe", methods=["POST"])
def subscribe() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    plan = data.get("plan")
    auto_renew = 1 if data.get("auto_renew", 1) else 0

    if plan not in PLANS or plan in ("free", "pay_as_you_go"):
        return jsonify({"error": "无效订阅套餐", "code": "PLAN_003"}), 400

    result = create_subscription(g.key_id, plan, auto_renew)
    return jsonify(result)


# ─── 主调用接口（示例计费入口） ───
@app.route("/v1/chat", methods=["POST"])
def chat() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", ""))[:2000]
    model = str(data.get("model", "longhun-v1.0"))[:64]

    # 计量：递增当日计数
    daily_used = increment_daily_usage(g.key_id, 1)

    # 计费
    cost = 0.0
    if g.plan == "pay_as_you_go":
        if daily_used <= 10000:
            cost = 0.05
        elif daily_used <= 100000:
            cost = 0.04
        else:
            cost = 0.03
        if not deduct_balance(g.key_id, cost):
            return jsonify({"error": "Insufficient balance", "code": "BAL_002"}), 402
        log_call(g.key_id, "/v1/chat", cost)
    else:
        log_call(g.key_id, "/v1/chat", 0.0)

    stamp = hashlib.sha256(f"{g.key_id}:{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:8].upper()

    return jsonify(
        {
            "status": "ok",
            "response": f"[模拟响应:{model}] 你说了: {prompt[:80]}",
            "usage": {
                "key_id": g.key_id,
                "plan": g.plan,
                "daily_used": daily_used,
                "balance": get_balance(g.key_id),
            },
            "dna": f"#龍芯⚡️{stamp}",
        }
    )


# ─── 运行 ───
# ============================================================
# 🐉 媒体感官层 · 统一媒体网关 v1.0（2026-09-01 · 感官层四件套）
#   /v1/render → 女娲五彩石渲染引擎（wuxing/audit/flow/health → png/svg/html）
#   /v1/speak  → 龍魂声音引擎（TTS → wav/mp3）
#   /v1/video  → 龍魂视频引擎（文本/图片 → mp4/webm）
#   全部响应带 X-Longhun-Trace 追溯头
# ============================================================
import os as _os
import json as _json
import uuid as _uuid
import tempfile as _tf

from flask import send_file as _send_file

_BIN_DIR = str(Path(__file__).resolve().parent.parent)
if _BIN_DIR not in sys.path:
    sys.path.insert(0, _BIN_DIR)


@app.after_request
def _media_trace(resp: Any):
    """统一注入 X-Longhun-Trace 追溯头"""
    if "X-Longhun-Trace" not in resp.headers:
        resp.headers["X-Longhun-Trace"] = f"LH-{_uuid.uuid4().hex[:16]}"
    return resp


@app.route("/v1/render", methods=["POST"])
def v1_render() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    类型 = str(body.get("type", "wuxing"))
    数据 = body.get("data")
    格式 = str(body.get("format", "png"))
    if 格式 not in ("png", "svg", "html"):
        return jsonify({"error": "format must be png/svg/html", "trace": _uuid.uuid4().hex[:16]}), 400
    try:
        from wuwu_renderer import 渲染
        with _tf.TemporaryDirectory() as tmp:
            payload = _json.dumps(数据, ensure_ascii=False) if isinstance(数据, (dict, list)) else (数据 or None)
            out = 渲染(类型, payload, 格式, "media_render", 路径目录=Path(tmp))
            mime = {"png": "image/png", "svg": "image/svg+xml", "html": "text/html"}[格式]
            return _send_file(out, mimetype=mime, as_attachment=False, download_name=f"wuwu_{类型}.{格式}")
    except SystemExit as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"render failed: {e}"}), 500


@app.route("/v1/speak", methods=["POST"])
def v1_speak() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    text = str(body.get("text", "")).strip()
    if not text:
        return jsonify({"error": "text required", "trace": _uuid.uuid4().hex[:16]}), 400
    格式 = str(body.get("format", "wav"))
    声音 = body.get("voice")
    引擎 = str(body.get("engine", "say"))
    if 格式 not in ("wav", "mp3"):
        return jsonify({"error": "format must be wav/mp3", "trace": _uuid.uuid4().hex[:16]}), 400
    try:
        from lh_audio import cmd_speak
        with _tf.TemporaryDirectory() as tmp:
            out = cmd_speak(text, voice=声音, fmt=格式, out=_os.path.join(tmp, f"speak.{格式}"), engine=引擎)
            mime = "audio/wav" if 格式 == "wav" else "audio/mpeg"
            return _send_file(out, mimetype=mime, as_attachment=False, download_name=f"lh_speak.{格式}")
    except SystemExit as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"speak failed: {e}"}), 500


@app.route("/v1/video", methods=["POST"])
def v1_video() -> Any:
    if not _authed():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    输入 = body.get("input") or body.get("text")
    if not 输入:
        return jsonify({"error": "input/text required", "trace": _uuid.uuid4().hex[:16]}), 400
    模板 = body.get("template")
    格式 = str(body.get("format", "mp4"))
    if 格式 not in ("mp4", "webm"):
        return jsonify({"error": "format must be mp4/webm", "trace": _uuid.uuid4().hex[:16]}), 400
    try:
        from lh_video import cmd_video
        with _tf.TemporaryDirectory() as tmp:
            out = cmd_video(str(输入), template=模板, fmt=格式, out=_os.path.join(tmp, f"video.{格式}"))
            mime = "video/mp4" if 格式 == "mp4" else "video/webm"
            return _send_file(out, mimetype=mime, as_attachment=False, download_name=f"lh_video.{格式}")
    except SystemExit as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"video failed: {e}"}), 500


if __name__ == "__main__":
    host = str(config.get("gateway", {}).get("host", "127.0.0.1"))
    port = int(config.get("gateway", {}).get("port", 8092))
    debug = bool(config.get("gateway", {}).get("debug", False))

    print("🐉 龙魂API网关 v1.2（五锁融合）启动")
    print(f"  地址: http://{host}:{port}")
    print("  第一锁 身份认证: 明文兼容 + HMAC-SHA256 签名")
    print("  第二锁 防盗刷:   四层令牌桶（全局/用户/接口/IP）")
    print("  第三锁 防重放:   时间戳 + Nonce（300s）")
    print("  第四锁 IP白名单: " + ("已启用" if get_ip_whitelist().enabled else "未启用（config.yaml）"))
    print("  第五锁 密钥轮换: 90 天（rotate_keys.py --rotate）")
    print("  /auth/register   - 注册 API Key（free/pay_as_you_go）")
    print("  /auth/topup      - 充值（按量用户）")
    print("  /auth/subscribe  - 订阅套餐（basic/pro/enterprise）")
    print("  /balance         - 查询余额/用量")
    print("  /v1/chat         - 调用入口（计费点）")
    print("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅")

    app.run(host=host, port=port, debug=debug)
