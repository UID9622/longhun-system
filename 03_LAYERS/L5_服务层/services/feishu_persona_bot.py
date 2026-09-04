#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🤖 龍魂人格查询 · 飞书机器人 Webhook 服务

> DNA: #龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-FEISHU-PERSONA-BOT-v1.0
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 作用: 接收飞书消息 → 调用 lh_persona_report --feishu-card → 返回卡片
> 
> 飞书配置:
>   - 事件订阅: /feishu/persona/event
>   - 机器人指令: @机器人 人格、@机器人 人格 P01、@机器人 人格 top5、@机器人 人格 健康度
> 
> 启动:
>   python3 L5_服务层/services/feishu_persona_bot.py
>   # 或通过 bin/longhun-launcher.py 注册服务
> 
> 环境变量:
>   FEISHU_APP_ID       — 飞书应用 ID
>   FEISHU_APP_SECRET   — 飞书应用密钥
>   FEISHU_VERIFY_TOKEN — 飞书事件验证 Token
>   PERSONA_BOT_PORT    — 服务端口 (默认: 9636)
"""

import json
import os
import sys
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse

ROOT = Path(__file__).resolve().parent.parent.parent
REPORT_SCRIPT = ROOT / "bin" / "lh_persona_report.py"

DNA = "#龍芯⚡️丙午·乙未·壬午·丙午·䷳艮为山-FEISHU-PERSONA-BOT-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ─── 飞书配置 ───
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_VERIFY_TOKEN = os.getenv("FEISHU_VERIFY_TOKEN", "")
PERSONA_BOT_PORT = int(os.getenv("PERSONA_BOT_PORT", "9636"))

app = FastAPI(
    title="龍魂人格查询 · 飞书机器人",
    description="实时查询龍魂人格内阁评估数据",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_tenant_access_token() -> str:
    """获取飞书 tenant_access_token"""
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return ""
    import urllib.request
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    body = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data.get("tenant_access_token", "")
    except Exception:
        return ""


def send_feishu_message(receive_id: str, msg_type: str, content: Dict[str, Any], token: str = ""):
    """发送飞书消息"""
    token = token or get_tenant_access_token()
    if not token:
        print("[飞书] 未配置 APP_ID/SECRET，跳过发送")
        return
    
    import urllib.request
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": "open_id"}
    
    body = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": json.dumps(content, ensure_ascii=False),
    }
    
    req = urllib.request.Request(
        url + "?" + "&".join(f"{k}={v}" for k, v in params.items()),
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[飞书] 发送失败: {e}")
        return None


def reply_feishu_card(receive_id: str, msg_id: str, card: Dict[str, Any]):
    """以卡片方式回复飞书消息"""
    token = get_tenant_access_token()
    if not token:
        return
    
    import urllib.request
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{msg_id}/reply"
    
    body = {
        "content": json.dumps(card, ensure_ascii=False),
        "msg_type": "interactive",
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[飞书] 回复失败: {e}")


def get_persona_card(query: str = "") -> Dict[str, Any]:
    """调用报表脚本获取飞书卡片"""
    try:
        cmd = [sys.executable, str(REPORT_SCRIPT), "--feishu-card"]
        if query:
            cmd.append(query)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {"msg_type": "text", "content": {"text": f"报表生成失败: {result.stderr}"}}
    except Exception as e:
        return {"msg_type": "text", "content": {"text": f"查询异常: {str(e)}"}}


# ─── API 端点 ───

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "feishu-persona-bot",
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/persona/report")
def api_persona_report(query: str = ""):
    """
    获取人格评估卡片 (供飞书或其他系统调用)
    
    GET /api/persona/report?query=P01       → 单个人格
    GET /api/persona/report?query=top5      → Top5
    GET /api/persona/report?query=健康度    → 健康度
    GET /api/persona/report                 → 总览
    """
    return get_persona_card(query)


@app.post("/feishu/event")
async def feishu_event(request: Request):
    """
    飞书事件订阅端点
    
    飞书机器人配置:
      请求网址: http://your-server:9636/feishu/event
    """
    body = await request.json()
    
    # URL 验证 (飞书配置时会发 challenge)
    if body.get("type") == "url_verification":
        token = body.get("token", "")
        challenge = body.get("challenge", "")
        # 验证 token
        if FEISHU_VERIFY_TOKEN and token != FEISHU_VERIFY_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
        return JSONResponse({"challenge": challenge})
    
    # 消息事件
    if body.get("type") == "event_callback":
        event = body.get("event", {})
        event_type = event.get("type", "")
        
        if event_type == "im.message.receive_v1":
            message = event.get("message", {})
            msg_type = message.get("message_type", "")
            msg_id = message.get("message_id", "")
            content_str = message.get("content", "{}")
            
            try:
                content = json.loads(content_str) if isinstance(content_str, str) else content_str
            except json.JSONDecodeError:
                content = {}
            
            text = content.get("text", "").strip()
            
            # 解析用户意图
            # 匹配: 人格、人格 全部、人格 P01、人格 top5、人格 健康度、人格 诸葛亮
            query = ""
            import re
            m = re.match(r'^人格\s*(.*)', text)
            if m:
                query = m.group(1).strip()
            elif "人格" in text:
                # 模糊匹配
                parts = text.replace("人格", "").strip()
                query = parts
            
            if not query:
                return JSONResponse({"code": 0, "msg": "no persona query"})
            
            # 生成卡片
            card = get_persona_card(query)
            
            # 回复消息 (需要飞书应用已配置)
            sender = event.get("sender", {})
            open_id = sender.get("open_id", "")
            if open_id and msg_id:
                reply_feishu_card(open_id, msg_id, card.get("card", card))
            
            return JSONResponse({"code": 0, "msg": "ok", "query": query})
    
    return JSONResponse({"code": 0, "msg": "ok"})


@app.post("/webhook/persona")
async def webhook_persona(request: Request):
    """
    简化版 Webhook（无需飞书事件订阅，直接 POST 调用）
    
    POST body: {"text": "人格 P01", "open_id": "ou_xxx"}
    返回: 飞书卡片 JSON
    
    可用于:
      - 自定义机器人 Webhook
      - 定时任务推送到飞书群
    """
    body = await request.json()
    text = body.get("text", "")
    open_id = body.get("open_id", "")
    push_to_group = body.get("push_to_group", False)
    webhook_url = body.get("webhook_url", "")
    
    # 解析查询
    query = text.replace("人格", "").strip()
    
    # 生成卡片
    result = get_persona_card(query)
    
    # 如果指定了 webhook URL，推送到飞书群
    if push_to_group and webhook_url:
        import urllib.request
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(result).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req) as resp:
                push_resp = json.loads(resp.read())
            result["push_result"] = push_resp
        except Exception as e:
            result["push_error"] = str(e)
    
    return result


def main():
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════╗
║   🤖 龍魂人格查询 · 飞书机器人服务                ║
╠══════════════════════════════════════════════════════╣
║  DNA:   {DNA}  ║
║  确认:  {CONFIRM} ║
║  端口:  {PERSONA_BOT_PORT}                                    ║
╚══════════════════════════════════════════════════════╝
""")
    print(f"📡 端点:")
    print(f"   GET  /health                   — 健康检查")
    print(f"   GET  /api/persona/report?query= — 人格查询 API")
    print(f"   POST /feishu/event             — 飞书事件订阅")
    print(f"   POST /webhook/persona          — 简化 Webhook")
    print(f"\n💡 飞书配置:")
    print(f"   事件订阅地址: http://your-server:{PERSONA_BOT_PORT}/feishu/event")
    print(f"   环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_VERIFY_TOKEN")
    print(f"\n🚀 启动中...")
    
    uvicorn.run(app, host="127.0.0.1", port=PERSONA_BOT_PORT, log_level="info")


if __name__ == "__main__":
    main()
