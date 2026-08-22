#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
⚖️ 龍魂·公正总裁 / 首席审计员 API v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-JUDGE-API-v1.0

部署在鲲鹏，提供独立、公正、可审计的裁决与审计能力。
默认调用本地 Ollama 的 longhun-judge 模型。

端点:
  POST /judge   - 公正裁决
  POST /audit   - 三色审计
  GET  /health  - 健康检查
"""

import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# ---------- 常量 ----------
OWNER = "龍芯北辰 UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_LABEL = "JUDGE"
TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"
DAY_ANCHOR = date(1949, 10, 1)
HEXAGRAM = "火雷噬嗑"

OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.environ.get("JUDGE_MODEL", "longhun-judge:latest")

app = FastAPI(title="龍魂·公正总裁 API", version="1.0") if HAS_FASTAPI else None

# ---------- 干支 DNA ----------
def ganzhi_year(y):
    return TIAN_GAN[(y - 4) % 10] + DI_ZHI[(y - 4) % 12]


def ganzhi_month(y, m):
    stem = ((y - 4) % 10 % 5) * 2 + m
    return TIAN_GAN[stem % 10] + DI_ZHI[m % 12]


def ganzhi_day(d):
    delta = (d - DAY_ANCHOR).days
    return TIAN_GAN[delta % 10] + DI_ZHI[delta % 12]


def four_pillars(d=None):
    d = d or date.today()
    return ganzhi_year(d.year), ganzhi_month(d.year, d.month), ganzhi_day(d)


_seq = 0

def stamp_dna():
    global _seq
    _seq += 1
    yg, mg, dg = four_pillars()
    return f"#龍芯⚡️{yg}·{mg}·{dg}·{HEXAGRAM}-{DNA_LABEL}-{_seq:06d}"


# ---------- Ollama 调用 ----------
def ollama_generate(prompt: str, system: str = "", temperature: float = 0.3) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature, "top_p": 0.7, "top_k": 40},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("response", "").strip()


# ---------- 输出清洗 ----------
def clean_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", text)


# ---------- 裁决模板 ----------
JUDGE_PROMPT = """你作为龍魂·公正总裁，请对以下争议或请求做出独立、公正的裁决。
要求：
1. 事实认定
2. 适用规则（龍魂铁律/KFPP/SafeAI/君子协议）
3. 推理分析
4. 裁决结论（PASS / L1 / L2 / L3 / L4）
5. 整改建议
6. 申诉入口

争议内容：
{content}
"""

AUDIT_PROMPT = """你作为龍魂·首席审计员，请对以下对象进行三色审计（🟢绿/🟡黄/🔴红）。
要求：
1. 审计对象概述
2. 各维度评分（绿/黄/红）
3. 发现的问题与证据
4. 整改建议
5. 申诉入口

审计对象：
{content}
"""


# ---------- 格式化响应 ----------
def build_response(endpoint: str, content: str, raw_output: str) -> Dict[str, Any]:
    dna = stamp_dna()
    cst = timezone(timedelta(hours=8))
    return {
        "endpoint": endpoint,
        "model": MODEL_NAME,
        "content": content,
        "output": clean_ansi(raw_output),
        "dna": dna,
        "confirm_code": CONFIRM_CODE,
        "owner": OWNER,
        "timestamp": datetime.now(cst).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


# ---------- API 路由 ----------
if app:
    @app.post("/judge")
    async def judge(request: Request):
        data = await request.json()
        content = data.get("content", "")
        if not content:
            return JSONResponse({"error": "缺少 content 参数"}, status_code=400)
        output = ollama_generate(JUDGE_PROMPT.format(content=content))
        return JSONResponse(build_response("/judge", content, output))

    @app.post("/audit")
    async def audit(request: Request):
        data = await request.json()
        content = data.get("content", "")
        if not content:
            return JSONResponse({"error": "缺少 content 参数"}, status_code=400)
        output = ollama_generate(AUDIT_PROMPT.format(content=content))
        return JSONResponse(build_response("/audit", content, output))

    @app.get("/health")
    async def health():
        return JSONResponse({
            "status": "ok",
            "model": MODEL_NAME,
            "ollama": OLLAMA_URL,
            "dna": stamp_dna(),
        })


# ---------- CLI ----------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·公正总裁 API")
    parser.add_argument("--serve", action="store_true", help="启动 API 服务")
    parser.add_argument("--port", type=int, default=9666, help="服务端口")
    parser.add_argument("--judge", type=str, help="单次裁决")
    parser.add_argument("--audit", type=str, help="单次审计")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="监听地址")
    args = parser.parse_args()

    if args.serve:
        if not HAS_FASTAPI:
            print("❌ 需要安装 fastapi 和 uvicorn: pip install fastapi uvicorn")
            sys.exit(1)
        print(f"🚀 启动龍魂·公正总裁 API :{args.port}")
        print(f"   模型: {MODEL_NAME}")
        print(f"   Ollama: {OLLAMA_URL}")
        uvicorn.run(app, host=args.host, port=args.port)
        return

    if args.judge:
        output = ollama_generate(JUDGE_PROMPT.format(content=args.judge))
        print(json.dumps(build_response("/judge", args.judge, output), ensure_ascii=False, indent=2))
        return

    if args.audit:
        output = ollama_generate(AUDIT_PROMPT.format(content=args.audit))
        print(json.dumps(build_response("/audit", args.audit, output), ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
