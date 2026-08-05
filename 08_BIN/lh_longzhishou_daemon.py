#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 龍智守飞书事件守护进程 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-LONGZHISHOU-DAEMON-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 接收飞书机器人消息事件回调（webhook）
  - 调用 scripts/龍智守.py 的守護() 进行反诈/国学/审计分析
  - 通过 feishu_bot 发送交互式卡片回复
  - 提供 /health 存活探针

环境变量（从 /opt/longhun-system/.env 加载）：
  FEISHU_APP_ID       飞书应用 ID
  FEISHU_APP_SECRET   飞书应用 Secret
  FEISHU_CHAT_ID      默认接收 chat_id（可选）
  FEISHU_ENCRYPT_KEY  事件加密密钥（可选）
  LONGZHISHOU_PORT    监听端口，默认 8780
  LONGZHISHOU_HOST    监听地址，默认 0.0.0.0
"""

import os
import sys
import json
import hmac
import hashlib
import base64
import time
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

# ============================================================
# 项目根路径
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

# ============================================================
# 加载 .env
# ============================================================
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

# ============================================================
# 配置
# ============================================================
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_ENCRYPT_KEY = os.environ.get("FEISHU_ENCRYPT_KEY", "")
DEFAULT_CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "")
HOST = os.environ.get("LONGZHISHOU_HOST", "0.0.0.0")
PORT = int(os.environ.get("LONGZHISHOU_PORT", "8783"))

# ============================================================
# FastAPI
# ============================================================
try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError as e:
    print(f"⚠️ 缺少依赖: {e}，请执行 pip install fastapi uvicorn")
    sys.exit(1)

# ============================================================
# 导入龍智守核心
# ============================================================
try:
    import 龍智守 as longzhishou
    LONGZHISHOU_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 无法导入龍智守模块: {e}")
    longzhishou = None
    LONGZHISHOU_AVAILABLE = False

try:
    import feishu_bot
    FEISHU_BOT_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 无法导入 feishu_bot: {e}")
    feishu_bot = None
    FEISHU_BOT_AVAILABLE = False

app = FastAPI(title="龍魂 · 龍智守飞书守护进程", version="1.0")

# ============================================================
# 工具函数
# ============================================================

def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def generate_dna(prefix: str = "LONGZHISHOU") -> str:
    ts = time.strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{prefix}:{ts}:{CONFIRM_CODE}".encode()).hexdigest()[:12].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def decrypt_feishu(encrypt: str, key: str) -> str:
    """飞书事件加密解密（AES-CBC-256）。"""
    if not key:
        raise RuntimeError("缺少 FEISHU_ENCRYPT_KEY")
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
    except ImportError:
        raise RuntimeError("解密需要 cryptography，请执行 pip install cryptography")

    encrypt_bytes = base64.b64decode(encrypt)
    key_bytes = hashlib.sha256(key.encode("utf-8")).digest()
    iv = key_bytes[:16]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypt_bytes) + decryptor.finalize()
    # 去除 PKCS7 填充
    pad_len = padded[-1]
    plain = padded[:-pad_len].decode("utf-8")
    # 飞书格式：前面 16 字节随机串 + 4 字节正文长度 + 正文 + 应用 ID
    json_len = int.from_bytes(plain[16:20], "big")
    return plain[20:20 + json_len]


def verify_feishu_signature(sign: str, timestamp: str, nonce: str, body: str, secret: str) -> bool:
    """可选：飞书签名验证（部分回调使用）。"""
    if not secret:
        return True
    raw = f"{timestamp}{nonce}{body}{secret}"
    expected = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return hmac.compare_digest(expected, sign)


def extract_chat_id(event_data: Dict[str, Any]) -> Optional[str]:
    """从飞书消息事件中提取 chat_id。"""
    msg = event_data.get("message", {})
    chat_id = msg.get("chat_id") or msg.get("receiver", {}).get("chat_id")
    if not chat_id:
        event = event_data.get("event", {})
        msg = event.get("message", {})
        chat_id = msg.get("chat_id") or msg.get("receiver", {}).get("chat_id")
    return chat_id or DEFAULT_CHAT_ID or None


def extract_message_text(event_data: Dict[str, Any]) -> str:
    """从飞书消息事件中提取文本内容。"""
    msg = event_data.get("message", {})
    content = msg.get("content", "{}")
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except Exception:
            content = {}
    return content.get("text", "").strip()


def extract_user_name(event_data: Dict[str, Any]) -> str:
    """提取发送者姓名（如有）。"""
    sender = event_data.get("sender", {})
    return sender.get("sender_name", "") or sender.get("user_id", "")


# ============================================================
# 事件处理
# ============================================================

# 卡片按钮点击幂等缓存：key -> 时间戳，防止飞书重试或用户连点导致副作用重复执行
_CARD_ACTION_COOLDOWN_SECONDS = 10
_recent_card_actions: Dict[str, float] = {}


def _card_action_key(chat_id: str, user_open_id: str, action_value: Dict[str, Any]) -> str:
    """生成按钮点击去重键。"""
    code = action_value.get("code", "") if isinstance(action_value, dict) else ""
    btn_action = action_value.get("action", "") if isinstance(action_value, dict) else ""
    raw = f"{chat_id}:{user_open_id}:{btn_action}:{code}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _cleanup_card_action_cache(now: float) -> None:
    """清理过期的按钮点击缓存。"""
    expired = now - _CARD_ACTION_COOLDOWN_SECONDS * 2
    for k in list(_recent_card_actions.keys()):
        if _recent_card_actions[k] < expired:
            del _recent_card_actions[k]


def _handle_card_action(action_data: Dict[str, Any], chat_id: str, user_open_id: str = "") -> Dict[str, Any]:
    """处理卡片按钮点击，返回飞书要求的 toast 响应格式。

    说明：
      - 按钮点击的反馈通过 toast 返回即可，不应再主动发一条文字消息，
        否则聊天流会出现重复的"已确认"，显得机械且扰民。
      - 增加幂等缓存，防止飞书网络重试或用户手快连点造成副作用重复触发。
    """
    raw_value = action_data.get("value", "{}")

    # 飞书回调的 value 通常是 dict；旧卡片曾误用 json.dumps 字符串，这里做兼容
    if isinstance(raw_value, dict):
        action_value = raw_value
    else:
        action_value_str = raw_value if isinstance(raw_value, str) else str(raw_value)
        try:
            action_value = json.loads(action_value_str)
            # 处理历史卡片双重 JSON 编码（字符串里还套了一层 JSON 字符串）
            if isinstance(action_value, str):
                action_value = json.loads(action_value)
        except Exception:
            action_value = {}

    btn_action = action_value.get("action", "未知") if isinstance(action_value, dict) else "未知"
    code = action_value.get("code", "") if isinstance(action_value, dict) else ""

    if btn_action == "confirm":
        toast_content = "✅ 已确认，龍魂守护完成"
    elif btn_action == "ignore":
        toast_content = "⏭️ 已忽略，不处理此条"
    else:
        toast_content = f"📨 收到操作：{btn_action}"

    # 可选：确认码校验（不匹配也放行，避免旧卡片失效）
    if code and code != CONFIRM_CODE:
        print(f"[DEBUG] 按钮确认码不匹配: {code[:20]}...", flush=True)

    # 幂等去重：同一用户在同一聊天对同一按钮的短时间重复点击只生效一次
    now = time.time()
    dedup_key = _card_action_key(chat_id, user_open_id, action_value)
    last_seen = _recent_card_actions.get(dedup_key, 0)
    _cleanup_card_action_cache(now)

    if now - last_seen < _CARD_ACTION_COOLDOWN_SECONDS:
        print(f"[DEBUG] 按钮点击去重: {btn_action} (chat={chat_id}, user={user_open_id})", flush=True)
        return {
            "toast": {
                "type": "success",
                "content": toast_content,
            }
        }

    _recent_card_actions[dedup_key] = now

    # 飞书卡片回调要求返回 toast 字段；按钮反馈不额外发文字消息，避免聊天流重复
    return {
        "toast": {
            "type": "success",
            "content": toast_content,
        }
    }


async def handle_feishu_event(event_body: Dict[str, Any]) -> Dict[str, Any]:
    """处理飞书事件并返回响应（支持 v1/v2 消息 + 卡片按钮回调）。"""
    event_type = event_body.get("type")

    # 1. URL 验证挑战（v1 格式）
    if event_type == "url_verification":
        return {"challenge": event_body.get("challenge", "")}

    # 2. 飞书 v2.0 事件格式
    if event_body.get("schema") == "2.0":
        header = event_body.get("header", {})
        event_name = header.get("event_type", "")
        event = event_body.get("event", {})

        # 2.1 卡片按钮回调 v2
        if event_name == "card.action.trigger":
            action_data = event.get("action", {})
            context = event.get("context", {})
            chat_id = context.get("open_chat_id", DEFAULT_CHAT_ID)
            operator = event.get("operator", {})
            user_open_id = operator.get("open_id", "")
            return _handle_card_action(action_data, chat_id, user_open_id)

        # 2.2 普通消息 v2
        if event_name == "im.message.receive_v1":
            chat_id = extract_chat_id(event)
            text = extract_message_text(event)
            user = extract_user_name(event)
            return await _process_message(chat_id, text, user)

        return {"status": "ignored", "reason": f"v2 事件 {event_name} 不处理"}

    # 3. 飞书 v1 事件格式
    if event_type == "event_callback":
        event = event_body.get("event", {})
        event_name = event.get("type", "")

        # 3.1 普通消息 v1
        if event_name == "im.message.receive_v1":
            chat_id = extract_chat_id(event)
            text = extract_message_text(event)
            user = extract_user_name(event)
            return await _process_message(chat_id, text, user)

        return {"status": "ignored", "reason": f"v1 事件 {event_name} 不处理"}

    # 4. 卡片按钮回调 v1（顶层 action，无 schema）
    action_data = event_body.get("action")
    if action_data:
        chat_id = event_body.get("open_chat_id", DEFAULT_CHAT_ID)
        user_open_id = event_body.get("open_id", "")
        return _handle_card_action(action_data, chat_id, user_open_id)

    return {"status": "ignored", "reason": f"未知类型 {event_type}"}


async def _process_message(chat_id: Optional[str], text: str, user: str) -> Dict[str, Any]:
    """处理普通消息，调用龍智守核心并发送卡片。"""
    if not text:
        return {"status": "ignored", "reason": "空消息"}

    if not chat_id:
        return {"status": "error", "reason": "无法获取 chat_id"}

    result = {"status": "ok", "chat_id": chat_id, "input": text, "user": user, "dna": generate_dna()}
    if LONGZHISHOU_AVAILABLE:
        try:
            intent, analysis, card, explain_file = longzhishou.守護(text, role="普通人", model="local")
            result["intent"] = intent
            result["explain_file"] = str(explain_file) if explain_file else None

            if FEISHU_BOT_AVAILABLE:
                try:
                    send_result = feishu_bot.send_card(chat_id, card)
                    result["send_status"] = send_result.get("code", "unknown")
                    result["send_msg"] = send_result.get("msg", "")
                except Exception as e:
                    result["send_status"] = "error"
                    result["send_msg"] = str(e)[:200]
            else:
                result["send_status"] = "skipped"
                result["send_msg"] = "feishu_bot 未加载"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)[:200]
            result["traceback"] = traceback.format_exc()
    else:
        result["status"] = "error"
        result["error"] = "龍智守模块未加载"

    return result


# ============================================================
# API 路由
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "longzhishou-daemon",
        "version": "1.0",
        "dna": generate_dna("HEALTH"),
        "confirm_code": CONFIRM_CODE,
        "modules": {
            "longzhishou": LONGZHISHOU_AVAILABLE,
            "feishu_bot": FEISHU_BOT_AVAILABLE,
        },
        "config": {
            "has_app_id": bool(FEISHU_APP_ID),
            "has_app_secret": bool(FEISHU_APP_SECRET),
            "has_encrypt_key": bool(FEISHU_ENCRYPT_KEY),
            "default_chat_id": bool(DEFAULT_CHAT_ID),
        },
    }


@app.post("/webhook")
async def webhook(request: Request):
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8", errors="ignore")

    # 入口日志：便于排查飞书回调是否到达、格式如何
    print(f"[DEBUG] 收到飞书请求: {body_text[:800]}", flush=True)

    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 如有加密则解密
    if payload.get("encrypt") and FEISHU_ENCRYPT_KEY:
        try:
            plain = decrypt_feishu(payload["encrypt"], FEISHU_ENCRYPT_KEY)
            payload = json.loads(plain)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Decrypt failed: {e}")

    result = await handle_feishu_event(payload)
    return JSONResponse(content=result)


# ============================================================
# 启动入口
# ============================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂 · 龍智守飞书守护进程 v1.0                  ║
║  地址: http://{HOST}:{PORT:<5}                      ║
║  模块: 龍智守={'✅' if LONGZHISHOU_AVAILABLE else '❌'}  feishu_bot={'✅' if FEISHU_BOT_AVAILABLE else '❌'}          ║
╚══════════════════════════════════════════════════════╝
""")
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        print("🟡 警告: 未配置 FEISHU_APP_ID / FEISHU_APP_SECRET，Webhook 可接收但无法回复消息")
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
