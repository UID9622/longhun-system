#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-31-HASH-API-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M73 哈希产权引擎 · 独立 API 服务（FastAPI · 127.0.0.1:9628）。

页面模板直连（决策流场总控页 v2.7 · M73）：
  pip install fastapi uvicorn pydantic
  python3 08_BIN/hash_api.py
  curl http://127.0.0.1:9628/hash/health
  curl -X POST http://127.0.0.1:9628/hash/register \
       -H 'Content-Type: application/json' \
       -d '{"name":"论文v1","type":"doc","owner":"UID9622","content":"..."}'

端口说明：页面模板写 9622（已被 longhun-api-gateway 占用）；9626 实测
被 lh_self_describing.py 占用（2026-08-31）。9628 为端口矩阵空位，固定
为 hash-api 常驻端口（老大确认常住·统一标准），被占用时自动顺延。

设计（M73 语义）：
  - content 只算 SHA-256，不存原文 → 数据主权·只存不可逆哈希（L1 数据铁律）
  - 复用 render/core/hash_registry.py 的 Merkle 链注册表（与渲染截图同链同源）
  - 注册表 append-only · chain_hash 链式防篡改 · 三色审计标记随响应返回
"""

import datetime
import hashlib
import sys
from pathlib import Path
from typing import Optional

# 把 longhun-system 根目录加进路径（复用 render/ 的 HashRegistry）
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from render.core.hash_registry import HashRegistry

VERSION = "1.0.0"
UID = "UID9622"
DNA = "#龍芯⚡️2026-08-31-HASH-API-v1.0-UID9622"
# 与渲染引擎共享同一条 Merkle 链（默认数据落 data/renders/，可用 env 覆盖）
DEFAULT_REGISTRY = str(ROOT / "data" / "renders" / "hash_registry.jsonl")

app = FastAPI(
    title="龍魂·哈希产权引擎 API",
    description="M73 哈希产权引擎 · SHA-256 + DNA 绑定 + Merkle 链注册",
    version=VERSION,
)
_registry: Optional[HashRegistry] = None


def get_registry() -> HashRegistry:
    global _registry
    if _registry is None:
        _registry = HashRegistry(DEFAULT_REGISTRY)
    return _registry


def make_dna(action: str, sha256: str) -> str:
    """业务注册 DNA：日期 + 模块 + 动作 + 哈希8位（v∞ 干支卦 DNA 的轻量版）。"""
    today = datetime.date.today().isoformat()
    return f"#龍芯⚡️{today}-HASH-{action}-{sha256[:8].upper()}"


class RegisterRequest(BaseModel):
    name: str = Field(..., description="资产名（如 论文v1 / 截图002）")
    type: str = Field(default="doc", description="资产类型：doc/img/video/code/other")
    owner: str = Field(default=UID, description="归属者（默认 UID9622）")
    content: str = Field(..., description="内容（服务端只算 SHA-256，不存原文）")
    url: str = Field(default="", description="来源 URL（可选）")
    platform: str = Field(default="api", description="平台标签（可选）")


class VerifyRequest(BaseModel):
    sha256: str = Field(..., description="待验证的 SHA-256（hex，64 位）")


@app.get("/hash/health")
def health():
    reg = get_registry()
    return {
        "status": "ok",
        "service": "hash-api",
        "version": VERSION,
        "uid": UID,
        "dna": DNA,
        "registry": reg.stats(),
        "audit": "🟢",
    }


@app.post("/hash/register")
def register(req: RegisterRequest):
    reg = get_registry()
    sha = hashlib.sha256(req.content.encode("utf-8")).hexdigest()
    dna = make_dna("REGISTER", sha)
    rec = reg.register(sha, dna, req.url, req.platform,
                       {"name": req.name, "type": req.type, "owner": req.owner})
    return {
        "status": "registered",
        "sha256": sha,
        "dna": dna,
        "record": {k: rec[k] for k in ("seq", "ts", "prev", "chain_hash")},
        "audit": "🟢",
    }


@app.get("/hash/verify")
def verify(sha256: str):
    reg = get_registry()
    rec = reg.verify(sha256)
    if not rec:
        raise HTTPException(status_code=404, detail="未登记的哈希")
    return {"status": "verified", "record": rec, "audit": "🟢"}


@app.get("/hash/dna")
def by_dna(dna: str):
    recs = get_registry().verify_dna(dna)
    return {"status": "ok", "count": len(recs), "records": recs, "audit": "🟢"}


@app.get("/hash/stats")
def stats():
    return {"status": "ok", **get_registry().stats(), "audit": "🟢"}


def find_free_port(start: int, tries: int = 30) -> int:
    """从 start 起自动探测空闲端口（本机常驻服务多，避免端口冲突）。"""
    import socket
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"无空闲端口（{start}~{start + tries}）")


if __name__ == "__main__":
    import argparse
    import uvicorn
    ap = argparse.ArgumentParser(prog="hash_api.py", description="M73 哈希产权引擎 API")
    ap.add_argument("--port", type=int, default=9628,
                    help="监听端口（默认 9628·端口矩阵已登记；被占用则自动顺延）")
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    try:
        find_free_port(args.port, tries=1)
        port = args.port
    except RuntimeError:
        port = find_free_port(args.port + 1)
        print(f"⚠️ 端口 {args.port} 被占用，顺延到 {port}")
    print(f"🐉 龍魂哈希产权引擎 v{VERSION} · http://{args.host}:{port}/hash/health")
    uvicorn.run(app, host=args.host, port=port, log_level="warning")
