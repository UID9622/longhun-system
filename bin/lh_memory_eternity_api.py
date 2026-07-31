# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-25-MEMORY-ETERNITY-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·记忆永存操作 API v1.0
把外脑压缩引擎 + 记忆永存引擎封装成 HTTP API，供仪表盘调用。
DNA: #龍芯⚡️2026-07-25-MEMORY-ETERNITY-API-v1.0
# STATUS: ⚠️ DEPRECATED · 功能由 bin/lh_memory_api.py + engines/lh_fixed_point_memory_archive.py 统一接管
# 保留原因: 历史 API 参考，新代码请使用 /v1/memory/archive/status 与 /v1/memory/archive/ingest
"""
import os
import sys
import json
import time
import hmac
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# FastAPI
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="龍魂·记忆永存操作 API", version="1.0")

# 安全：从环境变量或文件读取管理员令牌
ADMIN_TOKEN_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / ".eternity_api_token"
ADMIN_TOKEN = os.environ.get("LH_ETERNITY_API_TOKEN")
if not ADMIN_TOKEN and ADMIN_TOKEN_FILE.exists():
    ADMIN_TOKEN = ADMIN_TOKEN_FILE.read_text().strip()

if not ADMIN_TOKEN:
    seed = os.environ.get("USER", "uid9622") + "-eternity-" + str(PROJECT_ROOT)
    ADMIN_TOKEN = hashlib.sha256(seed.encode()).hexdigest()[:32]
    ADMIN_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    ADMIN_TOKEN_FILE.write_text(ADMIN_TOKEN)
    # 严格权限
    os.chmod(ADMIN_TOKEN_FILE, 0o600)


def verify_admin_token(token: Optional[str]) -> None:
    if not token:
        raise HTTPException(status_code=401, detail="缺少 X-Admin-Token")
    if not hmac.compare_digest(token, ADMIN_TOKEN):
        raise HTTPException(status_code=403, detail="X-Admin-Token 无效")


def run_script(script_path: Path, args: list, timeout: int = 300) -> Dict[str, Any]:
    """执行 Python 脚本，返回结构化结果。"""
    cmd = [sys.executable, str(script_path)] + args
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = round(time.time() - start, 2)
        output = proc.stdout.strip()
        stderr = proc.stderr.strip()

        # 优先尝试解析 JSON 输出
        result: Dict[str, Any] = {}
        try:
            # 有些脚本可能打印多行，找最后一行 JSON
            for line in reversed(output.splitlines()):
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    result = json.loads(line)
                    break
            if not result and output:
                result = json.loads(output)
        except json.JSONDecodeError:
            result = {"原始输出": output[:2000]}

        return {
            "状态": "🟢" if proc.returncode == 0 else "🔴",
            "返回码": proc.returncode,
            "耗时": f"{elapsed}s",
            "结果": result,
            "错误": stderr[:1000] if stderr else None,
        }
    except subprocess.TimeoutExpired:
        return {"状态": "🟡", "错误": f"执行超时（>{timeout}s）"}
    except Exception as e:
        return {"状态": "🔴", "错误": str(e)}


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "memory-eternity-api", "time": datetime.now().isoformat()}


@app.post("/compress-all")
async def compress_all(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_exobrain_compressor.py", ["compress-all"])


@app.post("/dedup")
async def dedup(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_exobrain_compressor.py", ["dedup"])


@app.post("/decay")
async def decay(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_exobrain_compressor.py", ["decay"])


@app.post("/graph")
async def graph(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_exobrain_compressor.py", ["graph"])


@app.post("/snapshot")
async def snapshot(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_memory_eternity.py", ["snapshot", "dashboard"])


@app.post("/sync")
async def sync_kunpeng(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_memory_eternity.py", ["sync"])


@app.post("/sync-all")
async def sync_all(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_memory_eternity.py", ["sync-all"])


@app.post("/verify")
async def verify(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_memory_eternity.py", ["verify"])


@app.get("/status")
async def status(request: Request, x_admin_token: Optional[str] = Header(None)):
    verify_admin_token(x_admin_token)
    return run_script(PROJECT_ROOT / "engines" / "lh_memory_eternity.py", ["status"])


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8781)
    args = parser.parse_args()

    print(f"🧬 记忆永存操作 API 启动: http://{args.host}:{args.port}")
    print(f"   Token 文件: {ADMIN_TOKEN_FILE}")
    uvicorn.run(app, host=args.host, port=args.port)
