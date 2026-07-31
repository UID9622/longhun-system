#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VAULT-API-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·本地保险柜 API v1.0                                    ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VAULT-API-v1.0        ║
# ║  仅本地 127.0.0.1 访问                                        ║
# ╚══════════════════════════════════════════════════════════════╝
"""
本地保险柜 HTTP API — 仅绑定 127.0.0.1，不对外暴露。

端点:
  GET  /health
  POST /vault/init
  POST /vault/add
  GET  /vault/list
  GET  /vault/get/{dna}
  POST /vault/delete
  POST /vault/sync
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from engines.lh_local_vault import LocalVault

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VAULT-API-v1.0"

app = FastAPI(title="龍魂本地保险柜 API", version="1.0.0")
vault = LocalVault()


class AddRequest(BaseModel):
    type: str = Field(..., min_length=1, max_length=64)
    data: str = Field(..., max_length=100000)
    password: Optional[str] = None


class DnaRequest(BaseModel):
    dna: str = Field(..., min_length=1)
    password: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "dna": DNA, "timestamp": datetime.now().isoformat()}


@app.post("/vault/init")
def init_vault():
    try:
        vault.init_vault()
        return {"status": "ok", "dna": DNA}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vault/add")
def add_entry(req: AddRequest):
    try:
        dna = vault.store(req.type, req.data, password=req.password)
        return {"status": "ok", "dna": dna}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vault/list")
def list_entries():
    try:
        entries = vault.list_entries()
        return {"status": "ok", "entries": entries, "count": len(entries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vault/get/{dna}")
def get_entry(dna: str, password: Optional[str] = None):
    try:
        data = vault.retrieve(dna, password=password)
        return {"status": "ok", "dna": dna, "data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="条目不存在")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vault/delete")
def delete_entry(req: DnaRequest):
    try:
        vault.delete(req.dna, password=req.password)
        return {"status": "ok", "dna": req.dna, "action": "frozen"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vault/sync")
def sync_memory():
    """调用记忆系统生成快照。"""
    try:
        snapshot_script = ROOT / "engines" / "lh_memory_eternity.py"
        result = subprocess.run(
            ["python3", str(snapshot_script), "snapshot"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂本地保险柜 API")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8780)
    args = ap.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
