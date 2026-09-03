#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-CRYPTO-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · crypto —— 哈希/HMAC/口令派生（全标准库 · 禁 MD5/SHA-1）
"""
import hashlib
import hmac
import base64
import secrets


def sha256(data: str, hexout: bool = True) -> str:
    """SHA-256 哈希（龍魂下界）"""
    h = hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data)
    return h.hexdigest() if hexout else h.digest()


def sha3(data: str) -> str:
    return hashlib.sha3_256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def hmac_sha256(key: str, message: str) -> str:
    """HMAC-SHA256 签名"""
    return hmac.new(key.encode("utf-8"), message.encode("utf-8"),
                    hashlib.sha256).hexdigest()


def verify_hmac(key: str, message: str, signature: str) -> bool:
    """恒定时间校验 HMAC 签名"""
    return hmac.compare_digest(hmac_sha256(key, message), signature)


def derive_key(password: str, salt: str = "CNSH-SALT", length: int = 32) -> bytes:
    """scrypt 口令派生（抗暴力）"""
    return hashlib.scrypt(password.encode("utf-8"), salt=salt.encode("utf-8"),
                          n=2 ** 14, r=8, p=1, dklen=length)


def encrypt(text: str, password: str) -> str:
    """简单对称加密（scrypt 派生 + XOR 流 + 随机盐）· 教学级，生产请接 SM4/AES 硬件
    输出: base64(salt|密文)"""
    salt = secrets.token_hex(16)
    key = derive_key(password, salt)
    data = text.encode("utf-8")
    stream = key * (len(data) // len(key) + 1)
    cipher = bytes(a ^ b for a, b in zip(data, stream))
    return base64.b64encode((salt + ":" + base64.b64encode(cipher).decode()).encode()).decode()


def decrypt(token: str, password: str) -> str:
    """decrypt(encrypt 输出) → 原文"""
    raw = base64.b64decode(token).decode()
    salt, b64 = raw.split(":", 1)
    cipher = base64.b64decode(b64)
    key = derive_key(password, salt)
    stream = key * (len(cipher) // len(key) + 1)
    plain = bytes(a ^ b for a, b in zip(cipher, stream))
    return plain.decode("utf-8")


def random_token(nbytes: int = 32) -> str:
    """密码学安全随机 token"""
    return base64.urlsafe_b64encode(secrets.token_bytes(nbytes)).decode().rstrip("=")
