# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
🐉 龍魂引擎 · 微信公众号通道适配器
===================================
微信消息 → 统一 Message → 引擎内核 → 统一 Response → 微信回复

启动:
  python3 引擎/channels/wechat_adapter.py
  端口: 9638 (默认)

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-WECHAT-ADAPTER-v1.0
"""

from __future__ import annotations
import json
import os
import sys
import hashlib
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Request, HTTPException  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import PlainTextResponse

from 引擎.message import Message, Response, Channel, MessageType, AuditLevel
from 引擎.engine_core import LonghunEngine

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·乙未·甲子·申时·需-WECHAT-ADAPTER-v1.0"

# ─── 微信配置 ───
WECHAT_APPID = os.getenv("WECHAT_APPID", "")
WECHAT_APPSECRET = os.getenv("WECHAT_APPSECRET", "")
WECHAT_TOKEN = os.getenv("WECHAT_TOKEN", "")           # 服务器配置 Token
WECHAT_AES_KEY = os.getenv("WECHAT_ENCODING_AES_KEY", "")
WECHAT_BOT_PORT = int(os.getenv("WECHAT_BOT_PORT", "9638"))

# ─── 全局引擎 ───
engine = LonghunEngine(safe_mode=True)

app = FastAPI(
    title="龍魂引擎 · 微信公众号通道",
    version="2.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ─── 微信签名验证 ───
def verify_signature(signature: str, timestamp: str, nonce: str) -> bool:
    """验证微信服务器签名"""
    if not WECHAT_TOKEN:
        return True  # 未配置则跳过
    tmp = [WECHAT_TOKEN, timestamp, nonce]
    tmp.sort()
    sha1 = hashlib.sha1("".join(tmp).encode()).hexdigest()
    return sha1 == signature


# ─── XML 解析 ───
def parse_wechat_xml(xml_str: str) -> Dict[str, str]:
    """解析微信 XML 消息"""
    try:
        root = ET.fromstring(xml_str)
        return {child.tag: child.text or "" for child in root}
    except Exception:
        return {}


# ─── 消息转换 ───
def wechat_xml_to_message(parsed: Dict[str, str]) -> Message:
    """微信 XML → 统一 Message"""
    msg_type_str = parsed.get("MsgType", "text")
    msg_type_map = {
        "text": MessageType.TEXT,
        "image": MessageType.IMAGE,
        "voice": MessageType.VOICE,
        "event": MessageType.EVENT,
    }

    content = parsed.get("Content", "")
    if msg_type_str == "image":
        content = f"[图片] {parsed.get('PicUrl', '')}"
    elif msg_type_str == "voice":
        content = f"[语音] {parsed.get('Recognition', '')}"
    elif msg_type_str == "event":
        event = parsed.get("Event", "")
        if event == "subscribe":
            content = "关注事件"
        elif event == "CLICK":
            content = f"菜单点击: {parsed.get('EventKey', '')}"

    return Message(
        channel=Channel.WECHAT_OA,
        content=content,
        msg_type=msg_type_map.get(msg_type_str, MessageType.TEXT),
        user_id=parsed.get("FromUserName", ""),
        user_name="",
        channel_meta={
            "to_user": parsed.get("ToUserName", ""),
            "msg_type": msg_type_str,
            "msg_id": parsed.get("MsgId", ""),
            "create_time": parsed.get("CreateTime", ""),
        },
    )


def response_to_wechat_xml(response: Response, from_user: str, to_user: str) -> str:
    """统一 Response → 微信 XML 回复"""
    text = response.to_text()
    # 微信限制 2048 字符
    text = text[:2000]

    return f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{text}]]></Content>
</xml>"""


# ─── API 端点 ───
@app.get("/health")
def health():
    return {
        "status": "ok",
        "channel": "wechat_oa",
        "dna": DNA,
        "engine": engine.get_health(),
    }


@app.get("/wechat")
def wechat_verify(signature: str = "", timestamp: str = "", nonce: str = "", echostr: str = ""):
    """微信服务器配置验证"""
    if verify_signature(signature, timestamp, nonce):
        return PlainTextResponse(echostr)
    raise HTTPException(status_code=403, detail="签名验证失败")


@app.post("/wechat")
async def wechat_message(request: Request):
    """接收微信消息"""
    # 验证签名
    signature = request.query_params.get("signature", "")
    timestamp = request.query_params.get("timestamp", "")
    nonce = request.query_params.get("nonce", "")
    if not verify_signature(signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="签名验证失败")

    body = await request.body()
    xml_str = body.decode("utf-8")
    parsed = parse_wechat_xml(xml_str)

    if not parsed:
        return PlainTextResponse("success")

    # 转换 → 引擎处理
    msg = wechat_xml_to_message(parsed)
    response = engine.process(msg)

    # 转回微信格式
    from_user = parsed.get("FromUserName", "")
    to_user = parsed.get("ToUserName", "")
    reply_xml = response_to_wechat_xml(response, from_user, to_user)

    return PlainTextResponse(reply_xml, media_type="application/xml")


@app.get("/api/query")
def api_query(q: str = ""):
    """HTTP直接查询"""
    if not q:
        return {"error": "请提供 q 参数"}
    msg = Message(channel=Channel.API, content=q)
    response = engine.process(msg)
    return {"response": response.to_dict()}


@app.get("/api/capabilities")
def api_capabilities():
    caps = []
    for cap in engine.registry.list_all():
        caps.append({"name": cap.name, "display": cap.display_name, "description": cap.description, "examples": cap.examples[:3]})
    return {"dna": DNA, "capabilities": caps, "total": len(caps)}


# ─── 启动 ───
if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════╗
║   🐉 龍魂引擎 · 微信公众号通道 v2.0               ║
╠══════════════════════════════════════════════════════╣
║  DNA:    {DNA}
║  端口:   {WECHAT_BOT_PORT}
║  引擎:   统一内核 · {len(engine.registry.list_all())} 项能力
╚══════════════════════════════════════════════════════╝
📡 端点:
   GET  /health                  — 健康检查
   GET  /wechat?signature=...    — 微信服务器验证
   POST /wechat                  — 微信消息接收
   GET  /api/query?q=...         — HTTP 查询
   GET  /api/capabilities        — 能力清单

💡 配置:
   export WECHAT_APPID=wx...
   export WECHAT_APPSECRET=...
   export WECHAT_TOKEN=...  (公众号服务器配置token)
""")
    uvicorn.run(app, host="127.0.0.1", port=WECHAT_BOT_PORT, log_level="info")
