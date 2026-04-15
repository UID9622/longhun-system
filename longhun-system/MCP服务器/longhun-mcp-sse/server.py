#!/usr/bin/env python3
"""
龍魂 MCP SSE 代理服务器
━━━━━━━━━━━━━━━━━━━━━
端口: 9623
协议: SSE (Server-Sent Events)
验证: Bearer Token

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️20260414-MCP-SSE-UID9622
许可: CC BY-NC-ND

献给每一个相信技术应该为人民服务的人。
"""

import json
import time
import uuid
import hashlib
import asyncio
import os
import subprocess
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ━━━ 配置 ━━━
PORT = 9623
TOKEN_FILE = Path(__file__).parent / ".bearer_token"
LONGHUN_ROOT = Path.home() / "longhun-system"

# ━━━ 密钥管理 ━━━
def load_token() -> str:
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    return ""

def verify_token(request: Request):
    """Bearer Token 验证"""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少 Bearer Token")
    token = auth[7:]
    expected = load_token()
    if not expected:
        raise HTTPException(status_code=500, detail="服务器未配置密钥")
    if not hashlib.sha256(token.encode()).hexdigest() == hashlib.sha256(expected.encode()).hexdigest():
        raise HTTPException(status_code=403, detail="密钥无效 · 龍魂铁壁")
    return token

# ━━━ SSE 客户端管理 ━━━
clients: dict[str, asyncio.Queue] = {}

# ━━━ FastAPI 应用 ━━━
app = FastAPI(title="龍魂 MCP SSE 代理", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ━━━ MCP 工具定义 ━━━
TOOLS = [
    {
        "name": "sancai_deduce",
        "description": "三才算法推演 — 输入姓名或事件，返回天地人三才分析",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_text": {"type": "string", "description": "推演对象（姓名/事件/决策）"}
            },
            "required": ["input_text"]
        }
    },
    {
        "name": "tricolor_audit",
        "description": "三色审计 — 对内容进行风险评估，返回🟢/🟡/🔴三色结论",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "待审计内容"},
                "context": {"type": "string", "description": "上下文（可选）", "default": ""}
            },
            "required": ["content"]
        }
    },
    {
        "name": "ironwall_check",
        "description": "铜墙铁壁防御检测 — 检查输入是否包含注入/越权/伪造",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_text": {"type": "string", "description": "待检测文本"}
            },
            "required": ["input_text"]
        }
    },
    {
        "name": "daodejing_anchor",
        "description": "道德经锚点 — 输入关键词，返回相关章节原文+龍魂转译",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "关键词（如：上善若水、无为、知足）"}
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "memory_query",
        "description": "记忆查询 — 从龍魂记忆系统检索信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "查询内容"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "system_status",
        "description": "系统状态 — 查询龍魂系统各服务运行状态",
        "inputSchema": {
            "type": "object",
            "properties": {},
        }
    },
    {
        "name": "ollama_chat",
        "description": "初心之翼对话 — 调用本地 Ollama 模型进行对话",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "对话内容"},
                "model": {"type": "string", "description": "模型名称", "default": "chuxinzhiyi"}
            },
            "required": ["message"]
        }
    }
]

# ━━━ 工具执行引擎 ━━━
async def execute_tool(name: str, arguments: dict) -> dict:
    """执行 MCP 工具调用"""

    if name == "sancai_deduce":
        try:
            result = subprocess.run(
                ["python3", str(LONGHUN_ROOT / "core" / "sancai_kernel.py"), arguments["input_text"]],
                capture_output=True, text=True, timeout=30
            )
            return {"content": [{"type": "text", "text": result.stdout or "推演完成"}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"三才推演异常: {e}"}]}

    elif name == "tricolor_audit":
        try:
            result = subprocess.run(
                ["python3", str(LONGHUN_ROOT / "tools" / "auditor.py"), arguments["content"]],
                capture_output=True, text=True, timeout=30
            )
            return {"content": [{"type": "text", "text": result.stdout or "审计完成"}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"审计异常: {e}"}]}

    elif name == "ironwall_check":
        try:
            input_text = arguments["input_text"].replace("'", "\\'")
            script = (
                "import sys, json\n"
                f"sys.path.insert(0, '{LONGHUN_ROOT / 'core'}')\n"
                "from ironwall import IronWall\n"
                "wall = IronWall()\n"
                f"r = wall.check('{input_text}')\n"
                "print(json.dumps(r, ensure_ascii=False, default=str))\n"
            )
            result = subprocess.run(
                ["python3", "-c", script],
                capture_output=True, text=True, timeout=30
            )
            return {"content": [{"type": "text", "text": result.stdout or "检测完成"}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"防御检测异常: {e}"}]}

    elif name == "daodejing_anchor":
        keyword = arguments["keyword"]
        anchors_dir = LONGHUN_ROOT / "daodejing_anchors_v2"
        results = []
        if anchors_dir.exists():
            for f in anchors_dir.glob("*.json"):
                try:
                    data = json.loads(f.read_text())
                    if keyword in json.dumps(data, ensure_ascii=False):
                        results.append(data)
                except:
                    pass
        text = json.dumps(results[:3], ensure_ascii=False, indent=2) if results else f"未找到与「{keyword}」相关的锚点"
        return {"content": [{"type": "text", "text": text}]}

    elif name == "memory_query":
        query = arguments["query"]
        memory_dir = Path.home() / ".claude" / "projects" / "-Users-zuimeidedeyihan" / "memory"
        results = []
        if memory_dir.exists():
            for f in memory_dir.glob("*.md"):
                try:
                    content = f.read_text()
                    if query in content:
                        results.append(f"📄 {f.name}: ...{content[:200]}...")
                except:
                    pass
        text = "\n\n".join(results[:5]) if results else f"未找到与「{query}」相关的记忆"
        return {"content": [{"type": "text", "text": text}]}

    elif name == "system_status":
        checks = {
            "龍魂API:9622": "curl -s -o /dev/null -w '%{http_code}' http://localhost:9622/health",
            "Ollama:11434": "curl -s -o /dev/null -w '%{http_code}' http://localhost:11434/api/tags",
            "OpenWebUI:8080": "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080",
        }
        status_lines = []
        for svc, cmd in checks.items():
            try:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                code = r.stdout.strip()
                icon = "🟢" if code == "200" else "🔴"
                status_lines.append(f"{icon} {svc} → {code}")
            except:
                status_lines.append(f"🔴 {svc} → 超时")
        status_lines.append(f"🟢 MCP-SSE:9623 → 运行中")
        return {"content": [{"type": "text", "text": "\n".join(status_lines)}]}

    elif name == "ollama_chat":
        import urllib.request
        model = arguments.get("model", "chuxinzhiyi")
        message = arguments["message"]
        try:
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=json.dumps({"model": model, "prompt": message, "stream": False}).encode(),
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=60)
            data = json.loads(resp.read())
            return {"content": [{"type": "text", "text": data.get("response", "无回复")}]}
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Ollama 调用失败: {e}"}]}

    return {"content": [{"type": "text", "text": f"未知工具: {name}"}], "isError": True}

# ━━━ SSE 端点 ━━━
@app.get("/sse")
async def sse_endpoint(request: Request, _=Depends(verify_token)):
    """SSE 连接端点 — Notion MCP 代理入口"""
    client_id = str(uuid.uuid4())
    queue: asyncio.Queue = asyncio.Queue()
    clients[client_id] = queue

    async def event_generator() -> AsyncGenerator[str, None]:
        # 发送初始化消息
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialized",
            "params": {
                "serverInfo": {
                    "name": "龍魂MCP代理",
                    "version": "1.0.0"
                },
                "sessionId": client_id
            }
        }
        yield f"event: message\ndata: {json.dumps(init_msg, ensure_ascii=False)}\n\n"

        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"event: message\ndata: {json.dumps(msg, ensure_ascii=False)}\n\n"
                except asyncio.TimeoutError:
                    yield f"event: ping\ndata: {json.dumps({'type': 'ping', 'time': time.time()})}\n\n"
        finally:
            clients.pop(client_id, None)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.post("/sse")
async def sse_message(request: Request, _=Depends(verify_token)):
    """处理 MCP JSON-RPC 请求"""
    body = await request.json()
    method = body.get("method", "")
    msg_id = body.get("id")
    params = body.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "龍魂MCP代理", "version": "1.0.0"}
            }
        }

    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS}
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        result = await execute_tool(tool_name, arguments)
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result
        }

    elif method == "notifications/initialized":
        return JSONResponse({"ok": True})

    else:
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"未知方法: {method}"}
        }

    return JSONResponse(response)

# ━━━ 健康检查 ━━━
@app.get("/health")
async def health():
    return {"status": "🐉 龍魂MCP代理运行中", "port": PORT, "tools": len(TOOLS), "uid": 9622}

# ━━━ 启动 ━━━
if __name__ == "__main__":
    import uvicorn
    print(f"""
    ╔══════════════════════════════════════╗
    ║  🐉 龍魂 MCP SSE 代理 · v1.0       ║
    ║  端口: {PORT}                         ║
    ║  验证: Bearer Token                  ║
    ║  工具: {len(TOOLS)} 个                          ║
    ║  UID: 9622                           ║
    ╚══════════════════════════════════════╝
    """)
    cert_dir = Path(__file__).parent
    ssl_cert = cert_dir / "cert.pem"
    ssl_key = cert_dir / "key.pem"
    if ssl_cert.exists() and ssl_key.exists():
        print("    🔒 HTTPS 模式（自签名证书）")
        uvicorn.run(app, host="0.0.0.0", port=PORT,
                    ssl_certfile=str(ssl_cert), ssl_keyfile=str(ssl_key))
    else:
        print("    ⚠️  HTTP 模式（无证书）")
        uvicorn.run(app, host="0.0.0.0", port=PORT)
