#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 MCP 服務器 v2.0
連接本地龍魂引擎 (http://localhost:8000)
讓 Claude Desktop 可以調用龍魂進行對話

DNA: #龍芯⚡️2026-04-06-MCP-LONGHUN-v2.0
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

🐱 大咪咪宝宝专属通道 · 玩着玩着就进步了 💋
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ── 核心配置 ──
API_URL = "http://localhost:8000/chat"
NOTION_TOKEN = "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"  # 🧠 老大的大脑令牌
NOTION_API_BASE = "https://api.notion.com/v1"


# ── 🐱 Notion 读取马仔（玩着都能进步） ──
def fetch_notion_recent_updates(days=7):
    """读取 Notion 最近 N 天的更新"""
    try:
        one_week_ago = (datetime.now() - timedelta(days=days)).isoformat()
        
        # 搜索最近修改的页面
        search_payload = {
            "filter": {
                "value": "page",
                "property": "object"
            },
            "sort": {
                "direction": "descending",
                "timestamp": "last_edited_time"
            }
        }
        
        req = urllib.request.Request(
            f"{NOTION_API_BASE}/search",
            data=json.dumps(search_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            
            # 过滤最近 N 天的
            recent = [
                r for r in results
                if r.get("last_edited_time", "") >= one_week_ago
            ]
            
            summary = f"📚 Notion 最近 {days} 天更新了 {len(recent)} 个页面\n\n"
            for page in recent[:5]:  # 只显示前5个
                title = page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "无标题")
                last_edited = page.get("last_edited_time", "")
                summary += f"- {title} (更新于 {last_edited})\n"
            
            return summary
            
    except Exception as e:
        return f"读取 Notion 失败: {e}"


def send_message(msg):
    """調用本地龍魂 API"""
    payload = json.dumps({
        "messages": [
            {"role": "user", "content": msg}
        ]
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            elif "error" in data:
                return f"龍魂引擎錯誤: {data['error']}"
            return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"調用龍魂引擎失敗: {e}"


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method")

        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "longhun-mcp", "version": "1.0.0"}
                }
            }
            print(json.dumps(response, ensure_ascii=False), flush=True)

        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "longhun_chat",
                            "description": "調用本地龍魂引擎（DeepSeek + 雙門驗證 + 易經推演）進行對話。當用戶的問題涉及東方智慧、命理、五行、道德經、風險審計或需要本地龍魂視角時使用。",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "description": "要發送給龍魂引擎的用戶問題"
                                    }
                                },
                                "required": ["message"]
                            }
                        },
                        {
                            "name": "notion_recent_updates",
                            "description": "🐱 读取老大 Notion 最近 N 天的更新（默认7天）。老大想复盘、想看最近做了什么、想找灵感的时候用。",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "days": {
                                        "type": "number",
                                        "description": "读取最近几天的更新（默认7天）",
                                        "default": 7
                                    }
                                },
                                "required": []
                            }
                        }
                    ]
                }
            }
            print(json.dumps(response, ensure_ascii=False), flush=True)

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            if name == "longhun_chat":
                msg = arguments.get("message", "")
                result = send_message(msg)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": result}
                        ]
                    }
                }
            elif name == "notion_recent_updates":
                days = arguments.get("days", 7)
                result = fetch_notion_recent_updates(days)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": result}
                        ]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {name}"}
                }
            print(json.dumps(response, ensure_ascii=False), flush=True)

        elif method == "notifications/initialized":
            pass


if __name__ == "__main__":
    main()
