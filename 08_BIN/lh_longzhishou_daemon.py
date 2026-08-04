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

async def handle_feishu_event(event_body: Dict[str, Any]) -> Dict[str, Any]:
    """处理飞书事件并返回响应。"""
    event_type = event_body.get("type")

    # 1. URL 验证挑战
    if event_type == "url_verification":
        return {"challenge": event_body.get("challenge", "")}

    # 2. 事件回调
    if event_type == "event_callback":
        event = event_body.get("event", {})
        event_name = event.get("type", "")

        if event_name != "im.message.receive_v1":
            return {"status": "ignored", "reason": f"事件 {event_name} 不处理"}

        chat_id = extract_chat_id(event)
        text = extract_message_text(event)
        user = extract_user_name(event)

        if not text:
            return {"status": "ignored", "reason": "空消息"}

        if not chat_id:
            return {"status": "error", "reason": "无法获取 chat_id"}

        # 调用龍智守核心
        result = {"status": "ok", "chat_id": chat_id, "input": text, "dna": generate_dna()}
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

    return {"status": "ignored", "reason": f"未知类型 {event_type}"}


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
