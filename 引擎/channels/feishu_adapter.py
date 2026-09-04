#!/usr/bin/env python3
"""
🐉 龍魂引擎 · 飞书通道适配器
=============================
飞书消息 → 统一 Message → 引擎内核 → 统一 Response → 飞书卡片

复用原有飞书桥接的 API 调用逻辑，但内核已统一。

启动:
  python3 引擎/channels/feishu_adapter.py
  端口: 9637 (默认)

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-FEISHU-ADAPTER-v1.0
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Request, HTTPException  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse

from 引擎.message import Message, Response, Channel, MessageType, AuditLevel
from 引擎.engine_core import LonghunEngine

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·乙未·甲子·申时·需-FEISHU-ADAPTER-v1.0"

# ─── 飞书配置 ───
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN", "")
FEISHU_BOT_PORT = int(os.getenv("FEISHU_BOT_PORT", "9637"))

# ─── 全局引擎实例 ───
engine = LonghunEngine(safe_mode=True)

# ─── FastAPI ───
app = FastAPI(
    title="龍魂引擎 · 飞书通道",
    description="所有飞书消息统一过龍魂引擎内核",
    version="2.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ─── 飞书 API 工具 ───
def get_tenant_access_token() -> str:
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return ""
    import urllib.request
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()).get("tenant_access_token", "")
    except Exception:
        return ""


def reply_feishu(open_id: str, msg_id: str, content: Dict[str, Any]):
    """回复飞书消息"""
    token = get_tenant_access_token()
    if not token:
        print("[飞书] 无 token，跳过回复")
        return

    import urllib.request
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{msg_id}/reply"
    body = {
        "content": json.dumps(content, ensure_ascii=False),
        "msg_type": "interactive" if "header" in content else "text",
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST")
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[飞书] 回复失败: {e}")


# ─── 消息转换 ───
def feishu_to_message(event: Dict[str, Any]) -> Message:
    """飞书事件 → 统一 Message"""
    message_raw = event.get("message", {})
    content_str = message_raw.get("content", "{}")
    try:
        content_obj = json.loads(content_str) if isinstance(content_str, str) else content_str
    except json.JSONDecodeError:
        content_obj = {}

    text = content_obj.get("text", "").strip()
    sender = event.get("sender", {})
    msg_id = message_raw.get("message_id", "")

    return Message(
        channel=Channel.FEISHU,
        content=text,
        user_id=sender.get("open_id", ""),
        user_name=sender.get("sender_id", {}).get("user_id", ""),
        session_id=message_raw.get("chat_id", ""),
        channel_meta={
            "tenant_key": event.get("tenant_key", ""),
            "msg_id": msg_id,
            "msg_type": message_raw.get("message_type", ""),
            "chat_type": message_raw.get("chat_type", ""),
            "root_id": message_raw.get("root_id", ""),
        },
        raw_payload=event,
    )


def response_to_feishu_card(response: Response, query_text: str = "") -> Dict[str, Any]:
    """统一 Response → 飞书卡片"""
    # 如果已经有卡片数据，直接返回
    if response.card_data:
        return response.card_data

    status_color = {
        AuditLevel.GREEN: "green",
        AuditLevel.YELLOW: "yellow",
        AuditLevel.RED: "red",
    }.get(response.audit_level, "grey")

    status_icon = {
        AuditLevel.GREEN: "✅",
        AuditLevel.YELLOW: "⚠️",
        AuditLevel.RED: "🔴",
    }.get(response.audit_level, "ℹ️")

    title = response.title or "龍魂引擎"
    content_preview = response.content[:2000] if response.content else "无内容"

    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"{status_icon} {title}"},
            "template": status_color,
        },
        "elements": [
            {"tag": "markdown", "content": content_preview},
        ],
    }

    # 添加快捷回复按钮
    if response.quick_replies:
        actions = []
        for reply in response.quick_replies[:5]:
            actions.append({
                "tag": "button",
                "text": {"tag": "plain_text", "content": reply[:20]},
                "type": "default",
                "value": {"text": reply},
            })
        if actions:
            card["elements"].append({
                "tag": "action",
                "actions": actions,
            })

    # 底部DNA
    footer = f"🧬 {response.dna_trace}" if response.dna_trace else DNA
    if response.persona_used:
        footer += f" · {response.persona_used}"
    card["elements"].append({
        "tag": "hr",
    })
    card["elements"].append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": footer}],
    })

    return card


# ─── API 端点 ───
@app.get("/health")
def health():
    return {
        "status": "ok",
        "channel": "feishu",
        "dna": DNA,
        "engine": engine.get_health(),
    }


@app.get("/api/query")
def api_query(q: str = ""):
    """HTTP直接查询"""
    if not q:
        return {"error": "请提供 q 参数"}
    msg = Message(channel=Channel.API, content=q)
    response = engine.process(msg)
    card = response_to_feishu_card(response, q)
    return {"response": response.to_dict(), "card": card}


@app.post("/feishu/event")
async def feishu_event(request: Request):
    """飞书事件订阅端点"""
    body = await request.json()

    # URL 验证
    if body.get("type") == "url_verification":
        token = body.get("token", "")
        if FEISHU_VERIFY_TOKEN and token != FEISHU_VERIFY_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
        return JSONResponse({"challenge": body.get("challenge", "")})

    # 消息事件
    if body.get("type") == "event_callback":
        event = body.get("event", {})
        event_type = event.get("type", "")

        if event_type == "im.message.receive_v1":
            # 转换 → 引擎处理
            msg = feishu_to_message(event)
            response = engine.process(msg)

            # 回发飞书卡片
            sender = event.get("sender", {})
            open_id = sender.get("open_id", "")
            msg_id_raw = event.get("message", {}).get("message_id", "")

            if open_id and msg_id_raw:
                card = response_to_feishu_card(response, msg.content)
                reply_feishu(open_id, msg_id_raw, card)

            return JSONResponse({
                "code": 0, "msg": "ok",
                "intent": response.capability_used,
                "audit": response.audit_level.value,
            })

    return JSONResponse({"code": 0, "msg": "ok"})


@app.post("/webhook")
async def webhook(request: Request):
    """简化 Webhook"""
    body = await request.json()
    text = body.get("text", "")
    webhook_url = body.get("webhook_url", "")

    msg = Message(channel=Channel.FEISHU, content=text)
    response = engine.process(msg)
    card = response_to_feishu_card(response, text)

    if webhook_url:
        import urllib.request
        req_body = {"msg_type": "interactive", "card": card}
        req = urllib.request.Request(webhook_url, data=json.dumps(req_body).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Webhook 推送失败: {e}")

    return {"response": response.to_dict(), "card": card}


@app.get("/api/capabilities")
def api_capabilities():
    """能力清单"""
    caps = []
    for cap in engine.registry.list_all():
        caps.append({
            "name": cap.name,
            "display": cap.display_name,
            "description": cap.description,
            "examples": cap.examples[:3],
            "dangerous": cap.is_dangerous,
        })
    return {"dna": DNA, "capabilities": caps, "total": len(caps)}


# ─── 启动 ───
if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════╗
║   🐉 龍魂引擎 · 飞书通道 v2.0                      ║
╠══════════════════════════════════════════════════════╣
║  DNA:    {DNA}
║  端口:   {FEISHU_BOT_PORT}
║  引擎:   统一内核 · {len(engine.registry.list_all())} 项能力
╚══════════════════════════════════════════════════════╝
📡 端点:
   GET  /health                  — 健康检查
   GET  /api/query?q=...         — HTTP 查询
   GET  /api/capabilities        — 能力清单
   POST /feishu/event            — 飞书事件订阅
   POST /webhook                 — 简化 Webhook

💡 飞书配置:
   事件订阅: http://your-server:{FEISHU_BOT_PORT}/feishu/event
""")
    uvicorn.run(app, host="127.0.0.1", port=FEISHU_BOT_PORT, log_level="info")
