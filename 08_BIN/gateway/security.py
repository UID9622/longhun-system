#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙魂API网关 · 安全引擎（五锁融合）
DNA: #龍芯⚡️2026-08-31-GATEWAY-SECURITY-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

第一锁 · HMAC-SHA256 签名（哈希作 HMAC key，服务端无需存明文，P0 兼容）
第三锁 · 时间戳 + Nonce 防重放（内存 LRU，Redis 可选）
第四锁 · IP 白名单（网关层可选；Nginx geo 见 nginx-ip-whitelist.conf）
"""

import hashlib
import hmac
import threading
import time
from collections import OrderedDict
from typing import Any

try:  # Redis 可选：配置了 redis_url 才用
    import redis  # type: ignore

    _HAS_REDIS = True
except Exception:  # noqa: BLE001
    redis = None  # type: ignore
    _HAS_REDIS = False

# ─── 第一锁 · HMAC 签名 ───
# key 用 sha256(secret) 即库中已存的 key_secret 哈希，服务端不需明文即可验签。
# message = "<method>\n<path>\n<body_sha256>\n<timestamp>\n<nonce>"


def build_message(method: str, path: str, body_sha256: str, timestamp: int, nonce: str) -> str:
    return f"{method.upper()}\n{path}\n{body_sha256}\n{timestamp}\n{nonce}"


def sign_request(
    secret: str, method: str, path: str, body_sha256: str, timestamp: int, nonce: str
) -> str:
    """客户端用明文 secret 生成签名。"""
    hmac_key = hashlib.sha256(secret.encode()).hexdigest().encode()
    msg = build_message(method, path, body_sha256, timestamp, nonce)
    return hmac.new(hmac_key, msg.encode(), hashlib.sha256).hexdigest()


def verify_hmac(
    key_secret_hash: str, signature: str, method: str, path: str, body_sha256: str, timestamp: int, nonce: str
) -> tuple[bool, str]:
    """服务端用库中哈希验签。key_secret_hash = 库中 key_secret 列。"""
    if not signature:
        return False, "Missing signature"
    expected = hmac.new(
        key_secret_hash.encode(), build_message(method, path, body_sha256, timestamp, nonce).encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return False, "Signature mismatch"
    return True, "OK"


def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


# ─── 第三锁 · Nonce 防重放 ───
class NonceGuard:
    """内存 LRU 版 Nonce 缓存（TTL 默认 300s）。多实例部署时请启用 Redis 版。"""

    def __init__(self, ttl: int = 300, max_entries: int = 100000, redis_url: str = ""):
        self.ttl = ttl
        self._cache: OrderedDict[str, float] = OrderedDict()
        self._lock = threading.Lock()
        self._max = max_entries
        self._redis = None
        if redis_url and _HAS_REDIS:
            self._redis = redis.from_url(redis_url)

    def check(self, key_id: str, nonce: str, timestamp: int) -> tuple[bool, str]:
        now = int(time.time())
        if abs(now - timestamp) > self.ttl:
            return False, "Timestamp expired"

        if self._redis is not None:
            k = f"nonce:{key_id}:{nonce}"
            if self._redis.exists(k):
                return False, "Nonce already used (replay attack)"
            self._redis.setex(k, self.ttl, "1")
            return True, "OK"

        with self._lock:
            k = f"{key_id}:{nonce}"
            now_f = time.time()
            # 惰性清理过期项
            while self._cache:
                _, exp = next(iter(self._cache.items()))
                if exp < now_f - self.ttl:
                    self._cache.popitem(last=False)
                else:
                    break
            if k in self._cache:
                return False, "Nonce already used (replay attack)"
            self._cache[k] = now_f
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)
            return True, "OK"

    def generate_nonce(self) -> str:
        import secrets

        return secrets.token_hex(16)


# ─── 第四锁 · IP 白名单（网关层可选） ───
class IPWhitelist:
    """启用条件：config.security.ip_whitelist.enabled=true 且 allowed_ips 非空。"""

    def __init__(self, enabled: bool = False, allowed_ips: list[str] | None = None):
        self.enabled = enabled
        self.allowed: set[str] = set(allowed_ips or [])

    def check(self, ip: str) -> bool:
        if not self.enabled:
            return True
        if not self.allowed:
            return True  # 配置了启用但没白名单 → 不拦截（防误锁自己）
        return ip in self.allowed


# 单例
_ip_whitelist: IPWhitelist | None = None
_nonce_guard: NonceGuard | None = None


def init_security(config: dict[str, Any] | None = None) -> None:
    """按配置初始化安全引擎单例。"""
    global _ip_whitelist, _nonce_guard
    cfg = (config or {}).get("security", {})
    wl = cfg.get("ip_whitelist", {})
    _ip_whitelist = IPWhitelist(bool(wl.get("enabled", False)), wl.get("allowed_ips", []))
    _nonce_guard = NonceGuard(
        ttl=int(cfg.get("nonce_ttl", 300)),
        redis_url=str(cfg.get("redis_url", "")),
    )


def get_ip_whitelist() -> IPWhitelist:
    if _ip_whitelist is None:
        init_security()
    return _ip_whitelist


def get_nonce_guard() -> NonceGuard:
    if _nonce_guard is None:
        init_security()
    return _nonce_guard
