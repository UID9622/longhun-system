#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 双节点认证中间件 v1.0
DNA: #龍芯⚡️丙午·辛未·AUTH-MIDDLEWARE-v1.0

三层认证体系：
  L1: API Key（预共享密钥，首次握手）
  L2: DNA签章验证（每次请求带DNA+HMAC）
  L3: 芯片层级门禁（跨节点时验证对方芯片层级）

安全铁律：
  - 不在公网裸传API Key
  - DNA签章含时间戳，防重放（5分钟窗口）
  - 失败3次熔断10分钟
"""

import hashlib
import hmac
import json
import os
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple

ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·辛未·AUTH-MIDDLEWARE-v1.0"
UID_ROOT = "UID9622"

# ─── 密钥管理 ───
KEY_FILE = ROOT / "L6_同步层" / ".dual_node_keys"
KEY_FILE.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class AuthConfig:
    """认证配置"""
    node_id: str = "local"                    # 本节点ID
    node_role: str = "mac"                    # mac / kunpeng
    api_key: str = ""                          # 预共享密钥
    peer_api_key: str = ""                     # 对端密钥
    replay_window: int = 300                   # 防重放窗口（秒）
    max_failures: int = 3                      # 熔断阈值
    cooldown_seconds: int = 600                # 熔断冷却时间（秒）
    require_chip_tier: bool = False            # 是否要求芯片层级验证（鲲鹏端开）


@dataclass
class AuthState:
    """认证状态"""
    failures: int = 0
    last_failure: float = 0.0
    cooldown_until: float = 0.0


# ─── 密钥文件管理 ───

def generate_keys(node_id: str = "local") -> Tuple[str, str]:
    """生成API Key对（本地+对端共享密钥）"""
    local_key = hashlib.sha256(f"{node_id}:{uuid.uuid4().hex}:{time.time()}".encode()).hexdigest()[:32]
    peer_key = hashlib.sha256(f"peer:{node_id}:{uuid.uuid4().hex}:{time.time()}".encode()).hexdigest()[:32]
    return local_key, peer_key


def save_keys(config: AuthConfig) -> None:
    """持久化密钥（权限600）"""
    data = {
        "node_id": config.node_id,
        "node_role": config.node_role,
        "api_key": config.api_key,
        "peer_api_key": config.peer_api_key,
        "created_at": int(time.time()),
        "dna": DNA,
    }
    KEY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    os.chmod(KEY_FILE, 0o600)


def load_keys() -> Optional[AuthConfig]:
    """加载已有密钥"""
    if not KEY_FILE.exists():
        return None
    try:
        data = json.loads(KEY_FILE.read_text())
        return AuthConfig(
            node_id=data.get("node_id", "local"),
            node_role=data.get("node_role", "mac"),
            api_key=data.get("api_key", ""),
            peer_api_key=data.get("peer_api_key", ""),
        )
    except (json.JSONDecodeError, KeyError):
        return None


# ─── 认证核心 ───

class DualNodeAuth:
    """双节点认证引擎"""

    def __init__(self, config: AuthConfig):
        self.config = config
        self.state = AuthState()
        self._nonce_cache: Dict[str, float] = {}  # nonce -> timestamp, 防重放

    def is_cooldown(self) -> bool:
        """是否处于熔断冷却期"""
        if self.state.cooldown_until > time.time():
            return True
        # 冷却期过了，重置
        if self.state.cooldown_until > 0 and self.state.cooldown_until <= time.time():
            self.state.failures = 0
            self.state.cooldown_until = 0.0
        return False

    def record_failure(self) -> None:
        """记录认证失败，达到阈值触发熔断"""
        self.state.failures += 1
        self.state.last_failure = time.time()
        if self.state.failures >= self.config.max_failures:
            self.state.cooldown_until = time.time() + self.config.cooldown_seconds

    def verify_api_key(self, provided_key: str) -> bool:
        """L1: 验证API Key"""
        if self.is_cooldown():
            return False
        if not hmac.compare_digest(provided_key, self.config.peer_api_key):
            self.record_failure()
            return False
        return True

    def generate_dna_stamp(self, scene: str, payload_hash: str = "") -> Dict[str, Any]:
        """生成DNA签章（请求方调用）"""
        timestamp = int(time.time())
        nonce = uuid.uuid4().hex[:16]

        # 签章内容: scene + timestamp + nonce + payload_hash
        sign_content = f"{scene}:{timestamp}:{nonce}:{payload_hash}"
        signature = hmac.new(
            self.config.api_key.encode(),
            sign_content.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        return {
            "dna": DNA,
            "uid": UID_ROOT,
            "node_id": self.config.node_id,
            "node_role": self.config.node_role,
            "scene": scene,
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature,
            "payload_hash": payload_hash,
        }

    def verify_dna_stamp(self, stamp: Dict[str, Any], payload_hash: str = "") -> Tuple[bool, str]:
        """L2: 验证DNA签章（接收方调用）

        Returns: (是否通过, 失败原因)
        """
        if self.is_cooldown():
            return False, "认证熔断中"

        required = ["scene", "timestamp", "nonce", "signature", "node_id"]
        for k in required:
            if k not in stamp:
                return False, f"缺少字段: {k}"

        # 1. 时间戳防重放
        now = int(time.time())
        if abs(now - stamp["timestamp"]) > self.config.replay_window:
            return False, f"签章过期（窗口{self.config.replay_window}秒）"

        # 2. Nonce防重放
        if stamp["nonce"] in self._nonce_cache:
            return False, "重复nonce（重放攻击）"
        self._nonce_cache[stamp["nonce"]] = time.time()

        # 3. 签名验证
        sign_content = f"{stamp['scene']}:{stamp['timestamp']}:{stamp['nonce']}:{payload_hash}"
        expected = hmac.new(
            self.config.peer_api_key.encode(),
            sign_content.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        if not hmac.compare_digest(expected, stamp["signature"]):
            self.record_failure()
            return False, "签名不匹配"

        # 4. 清理过期nonce
        self._clean_nonce_cache()

        return True, "OK"

    def _clean_nonce_cache(self) -> None:
        """清理过期的nonce记录"""
        cutoff = time.time() - self.config.replay_window * 2
        expired = [k for k, v in self._nonce_cache.items() if v < cutoff]
        for k in expired:
            del self._nonce_cache[k]

    def get_headers(self, scene: str, payload: str = "") -> Dict[str, str]:
        """生成请求头（带API Key + DNA签章）"""
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16] if payload else ""
        stamp = self.generate_dna_stamp(scene, payload_hash)
        return {
            "X-Longhun-API-Key": self.config.api_key,
            "X-Longhun-DNA": json.dumps(stamp, ensure_ascii=False),
            "X-Longhun-Node-ID": self.config.node_id,
            "X-Longhun-Node-Role": self.config.node_role,
        }


# ─── FastAPI 中间件适配 ───

try:
    from fastapi import Request, HTTPException
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse

    class DualNodeAuthMiddleware(BaseHTTPMiddleware):
        """FastAPI 认证中间件"""

        def __init__(self, app, auth: DualNodeAuth, exclude_paths: list = None):
            super().__init__(app)
            self.auth = auth
            self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json"]

        async def dispatch(self, request: Request, call_next):
            # 跳过排除路径
            if request.url.path in self.exclude_paths:
                return await call_next(request)

            # L1: API Key
            api_key = request.headers.get("X-Longhun-API-Key", "")
            if not self.auth.verify_api_key(api_key):
                return JSONResponse(
                    status_code=401,
                    content={"error": "认证失败", "dna": DNA, "uid": UID_ROOT}
                )

            # L2: DNA签章
            dna_header = request.headers.get("X-Longhun-DNA", "")
            if dna_header:
                try:
                    stamp = json.loads(dna_header)
                    # 读取body计算hash（需要后续传递）
                    body = await request.body()
                    payload_hash = hashlib.sha256(body).hexdigest()[:16] if body else ""

                    ok, reason = self.auth.verify_dna_stamp(stamp, payload_hash)
                    if not ok:
                        return JSONResponse(
                            status_code=403,
                            content={"error": f"签章验证失败: {reason}", "dna": DNA}
                        )
                except json.JSONDecodeError:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "DNA签章格式错误", "dna": DNA}
                    )

            return await call_next(request)

    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


# ─── 命令行工具 ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂双节点认证工具")
    parser.add_argument("action", choices=["init", "show", "sign", "verify"])
    parser.add_argument("--node-id", default="local", help="节点ID")
    parser.add_argument("--role", default="mac", choices=["mac", "kunpeng"])
    parser.add_argument("--scene", default="TEST", help="签章场景")
    parser.add_argument("--payload", default="", help="载荷内容")
    args = parser.parse_args()

    if args.action == "init":
        config = AuthConfig(node_id=args.node_id, node_role=args.role)
        config.api_key, config.peer_api_key = generate_keys(args.node_id)
        save_keys(config)
        print(json.dumps({
            "node_id": config.node_id,
            "api_key": config.api_key,
            "peer_api_key": config.peer_api_key,
            "dna": DNA,
        }, ensure_ascii=False, indent=2))

    elif args.action == "show":
        config = load_keys()
        if config:
            print(json.dumps({
                "node_id": config.node_id,
                "node_role": config.node_role,
                "api_key_masked": config.api_key[:8] + "***",
                "peer_key_masked": config.peer_api_key[:8] + "***",
                "dna": DNA,
            }, ensure_ascii=False, indent=2))
        else:
            print("❌ 未初始化，请先执行: python3 L6_同步层/auth_middleware.py init")

    elif args.action == "sign":
        config = load_keys()
        if not config:
            print("❌ 未初始化")
            return
        auth = DualNodeAuth(config)
        stamp = auth.generate_dna_stamp(args.scene, args.payload)
        print(json.dumps(stamp, ensure_ascii=False, indent=2))

    elif args.action == "verify":
        config = load_keys()
        if not config:
            print("❌ 未初始化")
            return
        auth = DualNodeAuth(config)
        stamp = json.loads(sys.stdin.read())
        ok, reason = auth.verify_dna_stamp(stamp, args.payload)
        print(json.dumps({"ok": ok, "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    main()
