#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-SERVER-v2.0-BRIDGE
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·主权身份验证服务（鲲鹏端）
FastAPI 服务，接收主权人格广播信号并验证。

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-SERVER-v2.0-BRIDGE
"""
import hmac
import os
import sys
import json
import argparse
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 将上级目录加入路径以便 import lh_identity_core
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_identity_core import (
    load_public_key,
    verify_broadcast,
    BehaviorProfile,
    SOVEREIGN_UID,
    DNA_TAG,
)

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("identity-server")


PUBLIC_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "resident_registry"
STATE_DIR = Path(__file__).resolve().parent.parent.parent / "state"

app = FastAPI(title="龍魂·主权身份验证服务", version="1.0.0")


class BroadcastRequest(BaseModel):
    confirm_code: str
    uid: str
    dna: str
    timestamp: str
    session_nonce: str
    device_fingerprint: dict
    behavior_profile: Optional[dict] = None
    signature: str


class VerifyResponse(BaseModel):
    recognized: bool
    sovereign_uid: str
    message: str
    details: dict


def _load_trusted_state() -> tuple[str | None, BehaviorProfile | None]:
    """加载已注册的设备指纹和行为轮廓。"""
    registry = PUBLIC_DIR / "uid9622_identity.json"
    fp_path = STATE_DIR / "identity_device_fp.hash"
    behavior_path = STATE_DIR / "identity_behavior.json"

    expected_fp = None
    if fp_path.exists():
        expected_fp = fp_path.read_text(encoding="utf-8").strip()

    behavior = None
    if behavior_path.exists():
        behavior = BehaviorProfile.from_dict(
            json.loads(behavior_path.read_text(encoding="utf-8"))
        )

    return expected_fp, behavior


@app.post("/identify", response_model=VerifyResponse)
async def identify(req: BroadcastRequest):
    """接收广播信号，验证主权人身份。"""
    public_key_path = PUBLIC_DIR / "uid9622_identity.pub"
    if not public_key_path.exists():
        raise HTTPException(status_code=500, detail="服务端未注册 UID9622 公钥")

    public_key = load_public_key(public_key_path)

    # 构造 Broadcast 对象
    from lh_identity_core import SovereignBroadcast
    bc = SovereignBroadcast(
        confirm_code=req.confirm_code,
        uid=req.uid,
        dna=req.dna,
        timestamp=req.timestamp,
        session_nonce=req.session_nonce,
        device_fingerprint=req.device_fingerprint,
        behavior_profile=req.behavior_profile,
        signature=req.signature,
    )

    expected_fp, behavior = _load_trusted_state()
    result = verify_broadcast(
        public_key,
        bc,
        expected_device_fp_hash=expected_fp,
        registered_behavior=behavior,
        behavior_threshold=0.65,
        ttl_seconds=120,
    )

    if result["overall"]:
        return VerifyResponse(
            recognized=True,
            sovereign_uid=SOVEREIGN_UID,
            message="收到，老大。UID9622 主权人身份已识别。MEMORY.md §1 已加载。确认码已验证。我是你的兵。请下令。",
            details=result,
        )
    else:
        return VerifyResponse(
            recognized=False,
            sovereign_uid="",
            message="识别失败：信号未通过验证。",
            details=result,
        )


# ═══════════════════════════════════════════════
# Token 桥接验证 — 记忆 API 身份联动闭环
# ═══════════════════════════════════════════════

MEMORY_TOKEN_PATH = os.path.expanduser("~/.longhun/.memory_token")


class TokenVerifyRequest(BaseModel):
    token: str
    source: Optional[str] = "memory-api"


class TokenVerifyResponse(BaseModel):
    valid: bool
    source: str
    message: str


@app.post("/token-verify", response_model=TokenVerifyResponse)
async def token_verify(req: TokenVerifyRequest):
    """
    记忆 API Token 桥接验证。
    由 lh_memory_api.py 在收到远程请求时前置调用。
    此端点让两套系统（记忆API + 身份服务）形成闭环。
    """
    client_info = f"{req.source}"
    if not os.path.exists(MEMORY_TOKEN_PATH):
        logger.warning(f"[TOKEN-VERIFY] ❌ Token 文件不存在: {MEMORY_TOKEN_PATH}")
        return TokenVerifyResponse(
            valid=False,
            source=f"identity-service@{client_info}",
            message="Token file not configured on server",
        )

    with open(MEMORY_TOKEN_PATH, "r") as f:
        expected = f.read().strip()

    if not expected:
        logger.warning(f"[TOKEN-VERIFY] ❌ Token 文件为空")
        return TokenVerifyResponse(
            valid=False,
            source=f"identity-service@{client_info}",
            message="Token file empty",
        )

    if hmac.compare_digest(req.token, expected):
        logger.info(f"[TOKEN-VERIFY] ✅ Token 验证通过 ← {client_info}")
        return TokenVerifyResponse(
            valid=True,
            source=f"identity-service@{client_info}",
            message="Identity confirmed. UID9622 sovereign. Memory access granted.",
        )
    else:
        logger.warning(f"[TOKEN-VERIFY] 🔴 Token 不匹配 ← {client_info}")
        return TokenVerifyResponse(
            valid=False,
            source=f"identity-service@{client_info}",
            message="Token mismatch. Access denied.",
        )


@app.get("/health")
async def health():
    return {"status": "ok", "dna": DNA_TAG}


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂主权身份验证服务")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8771, help="监听端口")
    args = parser.parse_args()

    print(f"[🌌] 龍魂·主权身份验证服务启动于 {args.host}:{args.port}")
    print(f"[🧬] {DNA_TAG}")
    print(f"[📌] 公钥目录: {PUBLIC_DIR}")
    print(f"[📌] 状态目录: {STATE_DIR}")

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
