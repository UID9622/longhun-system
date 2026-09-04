#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cal_mac_bridge.py - 龍魂 CAL Mac 桥接 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CAL-MAC-BRIDGE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 职责: 监听 127.0.0.1:18765，承接鲲鹏经反向隧道(8766)转发的 Notion/CodeBuddy 请求
#       token 永不上云，全部留在 Mac。
# 启动: python3 ~/longhun-system/deploy/cal/cal_mac_bridge.py &
# 隧道: ssh -N -R 8766:127.0.0.1:18765 root@119.13.90.27

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    print("❌ 缺 fastapi/uvicorn: pip3 install fastapi uvicorn")
    sys.exit(1)

HOST = "127.0.0.1"
PORT = 18765
ENV_FILE = Path.home() / ".env"
INBOX_DIR = Path.home() / "longhun-system" / "06_CONTAINERS" / "cal-inbox"
CST = timezone(timedelta(hours=8))
VERSION = "1.0"
DNA = "#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CAL-MAC-BRIDGE-v1.0"

os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"


def now_str():
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def get_notion_token() -> str:
    try:
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("NOTION_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


def notion_search(query: str) -> dict:
    token = get_notion_token()
    if not token:
        return {"status": "error", "output": "🔴 Mac 上 ~/.env 缺 NOTION_TOKEN", "exit": -1}
    payload = json.dumps({"query": query, "page_size": 8}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.notion.com/v1/search",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            results = body.get("results", [])
            if not results:
                return {"status": "ok", "output": "📝 Notion 搜索完成：未找到匹配页面。", "exit": 0}
            lines = [f"📝 Notion 搜索「{query}」共 {len(results)} 条："]
            for r in results:
                obj = r.get("object", "")
                title = "无标题"
                if obj == "page":
                    props = r.get("properties", {})
                    title = props.get("title", {}).get("title", [{}])[0].get("plain_text", "无标题")
                elif obj == "database":
                    title = r.get("title", [{}])[0].get("plain_text", "无标题数据库")
                url = r.get("url", "")
                lines.append(f"- [{obj}] {title}\n  {url}")
            return {"status": "ok", "output": "\n".join(lines), "exit": 0}
    except urllib.error.HTTPError as e:
        return {"status": "error", "output": f"Notion HTTP {e.code}: {e.read().decode('utf-8','ignore')[:300]}", "exit": e.code}
    except Exception as e:
        return {"status": "error", "output": f"Notion 调用异常: {e}", "exit": -1}


def codebuddy_message(message: str) -> dict:
    try:
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(CST).strftime("%Y%m%d-%H%M%S")
        fname = INBOX_DIR / f"CAL-{ts}.md"
        content = f"# CAL 网页消息 · {ts}\n> 来自: https://uid9622.cn/cal/ · 已由 Mac 桥接收信\n\n{message}\n"
        fname.write_text(content, encoding="utf-8")
        return {"status": "ok", "output": f"✅ 消息已送达 CodeBuddy AI（Mac inbox: {fname.name}）\n我看到后会在 CodeBuddy 里处理。", "exit": 0}
    except Exception as e:
        return {"status": "error", "output": f"❌ 写 inbox 失败: {e}", "exit": -1}


app = FastAPI(title="龍魂 CAL Mac Bridge", version=VERSION)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "CAL Mac Bridge", "version": VERSION,
            "ts": now_str(), "dna": DNA, "notion": "ok" if get_notion_token() else "missing"}


@app.post("/api/notion/search")
async def notion_route(req: Request):
    try:
        body = await req.json()
    except Exception:
        return JSONResponse({"status": "error", "output": "JSON格式错误", "exit": -1})
    return notion_search(str(body.get("query", ""))[:200])


@app.post("/api/codebuddy/message")
async def codebuddy_route(req: Request):
    try:
        body = await req.json()
    except Exception:
        return JSONResponse({"status": "error", "output": "JSON格式错误", "exit": -1})
    return codebuddy_message(str(body.get("message", ""))[:2000])


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")
