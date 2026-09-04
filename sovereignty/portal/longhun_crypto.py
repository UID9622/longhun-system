#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# #龍芯⚡️丙午·甲午·戊寅·戊午·䷕贲-ENGINE-LONGHUN_CRYPTO-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂统一加密工具包

DeepSeek 执行器与龍魂本地网关之间的共享加密层：
- Fernet 对称加密（请求/响应体）
- HMAC-SHA256 完整性校验
- 时间戳 + nonce 防重放

DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-CRYPTO-v1.0
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
from collections import deque
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet


class LonghunCryptoError(Exception):
    pass


def _normalize_secret(raw_secret: str) -> bytes:
    """把任意字符串归一化为 Fernet 可用的 32 字节 URL-safe base64 密钥。"""
    if not raw_secret:
        raise LonghunCryptoError("加密密钥不能为空")
    # 若用户已提供 32 字节 base64（约 44 字符含等号），直接复用
    try:
        decoded = base64.urlsafe_b64decode(raw_secret.encode())
        if len(decoded) == 32:
            return raw_secret.encode()
    except Exception:
        pass
    # 否则用 SHA-256 派生 32 字节，再编码为 base64
    key = hashlib.sha256(raw_secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(key)


def _fernet(raw_secret: str) -> Fernet:
    return Fernet(_normalize_secret(raw_secret))


def encrypt_payload(payload: Dict[str, Any], raw_secret: str) -> str:
    """把 dict 加密为 base64 字符串。"""
    f = _fernet(raw_secret)
    token = f.encrypt(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    return base64.urlsafe_b64encode(token).decode("ascii")


def decrypt_payload(cipher_b64: str, raw_secret: str) -> Dict[str, Any]:
    """把 base64 密文解密为 dict。"""
    try:
        f = _fernet(raw_secret)
        token = base64.urlsafe_b64decode(cipher_b64.encode("ascii"))
        plain = f.decrypt(token)
        return json.loads(plain.decode("utf-8"))
    except Exception as e:
        raise LonghunCryptoError(f"解密失败: {e}") from e


def hmac_sign(message: str, raw_secret: str) -> str:
    """对字符串做 HMAC-SHA256，返回 hex。"""
    key = _normalize_secret(raw_secret)
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()


def hmac_verify(message: str, signature: str, raw_secret: str) -> bool:
    expected = hmac_sign(message, raw_secret)
    return hmac.compare_digest(expected, signature)


def make_envelope(payload: Dict[str, Any], raw_secret: str, ttl: Optional[int] = None) -> Dict[str, Any]:
    """生成带 HMAC、时间戳、nonce 的安全信封。"""
    cipher = encrypt_payload(payload, raw_secret)
    ts = int(time.time())
    nonce = secrets.token_urlsafe(16)
    sig_message = f"{cipher}|{ts}|{nonce}"
    return {
        "cipher": cipher,
        "hmac": hmac_sign(sig_message, raw_secret),
        "ts": ts,
        "nonce": nonce,
    }


class NonceCache:
    """固定大小的 nonce 去重缓存。"""

    def __init__(self, max_size: int = 10000, ttl: int = 600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: deque = deque()

    def is_used(self, nonce: str) -> bool:
        now = time.time()
        # 清理过期
        while self._cache and self._cache[0][1] < now - self.ttl:
            self._cache.popleft()
        for n, _ in self._cache:
            if n == nonce:
                return True
        return False

    def mark_used(self, nonce: str):
        if self.is_used(nonce):
            raise LonghunCryptoError("nonce 已使用，疑似重放攻击")
        self._cache.append((nonce, time.time()))
        while len(self._cache) > self.max_size:
            self._cache.popleft()


def open_envelope(
    envelope: Dict[str, Any],
    raw_secret: str,
    nonce_cache: Optional[NonceCache] = None,
    ttl: int = 300,
) -> Dict[str, Any]:
    """校验并打开安全信封，返回原始 payload。"""
    cipher = envelope.get("cipher", "")
    ts = envelope.get("ts")
    nonce = envelope.get("nonce", "")
    signature = envelope.get("hmac", "")

    if not (cipher and ts and nonce and signature):
        raise LonghunCryptoError("信封字段不完整")

    now = int(time.time())
    if abs(now - int(ts)) > ttl:
        raise LonghunCryptoError("时间戳过期或未来时间")

    if nonce_cache is not None:
        nonce_cache.mark_used(nonce)

    sig_message = f"{cipher}|{ts}|{nonce}"
    if not hmac_verify(sig_message, signature, raw_secret):
        raise LonghunCryptoError("HMAC 校验失败")

    return decrypt_payload(cipher, raw_secret)
