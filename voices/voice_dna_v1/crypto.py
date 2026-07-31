# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹本地加密模块
Dragon Soul Voice Local Encryption

功能：
  - 本地生成并管理 Fernet 主密钥与 HMAC 密钥
  - 按 user_id 派生用户级 Fernet 密钥
  - 声纹特征向量加密 + HMAC-SHA256 完整性校验
  - 不依赖外部服务，不联网传输

DNA: #龍芯⚡️20260628-VOICE-CRYPTO-v1.0
"""

import os
import hmac
import hashlib
import base64
import json
from pathlib import Path
from typing import Dict, Any

import numpy as np
from cryptography.fernet import Fernet, InvalidToken

from voice_anchor import BASE_DIR

KEYS_DIR = BASE_DIR / ".keys"
MASTER_KEY_FILE = KEYS_DIR / "master.key"
HMAC_KEY_FILE = KEYS_DIR / "hmac.key"


def ensure_keys() -> None:
    """确保本地密钥存在；不存在则自动生成。"""
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    if not MASTER_KEY_FILE.exists():
        MASTER_KEY_FILE.write_bytes(Fernet.generate_key())
        os.chmod(MASTER_KEY_FILE, 0o600)
    if not HMAC_KEY_FILE.exists():
        hmac_key = os.urandom(32)
        HMAC_KEY_FILE.write_bytes(hmac_key)
        os.chmod(HMAC_KEY_FILE, 0o600)


def get_master_fernet() -> Fernet:
    ensure_keys()
    return Fernet(MASTER_KEY_FILE.read_bytes())


def get_hmac_key() -> bytes:
    ensure_keys()
    return HMAC_KEY_FILE.read_bytes()


def _derive_key_material(user_id: str, salt: str) -> bytes:
    """使用 HMAC-SHA256 从主密钥派生用户级材料。"""
    hmac_key = get_hmac_key()
    return hmac.new(hmac_key, f"{salt}:{user_id}".encode("utf-8"), hashlib.sha256).digest()


def derive_user_fernet(user_id: str) -> Fernet:
    """派生用户级 Fernet 实例。"""
    material = _derive_key_material(user_id, "fernet")
    # Fernet 密钥需要 32 字节并做 url-safe base64 编码
    key = base64.urlsafe_b64encode(material)
    return Fernet(key)


def derive_export_key(user_id: str, password: str) -> Fernet:
    """从用户密码派生导出加密密钥（用于用户自主导出包）。"""
    base = _derive_key_material(user_id, "export")
    pw_hash = hashlib.sha256(password.encode("utf-8")).digest()
    mixed = bytes(a ^ b for a, b in zip(base, pw_hash))
    key = base64.urlsafe_b64encode(mixed)
    return Fernet(key)


def encrypt_features(features: np.ndarray, user_id: str) -> Dict[str, str]:
    """
    加密声纹特征向量，返回 ciphertext + hmac。

    Args:
        features: float32 特征向量
        user_id: 用户ID，用于派生用户级密钥

    Returns:
        {"ciphertext": "...", "hmac": "..."}
    """
    f = derive_user_fernet(user_id)
    payload = features.astype(np.float32).tobytes()
    ciphertext = f.encrypt(payload)
    h = hmac.new(get_hmac_key(), ciphertext, hashlib.sha256).hexdigest()
    return {
        "ciphertext": ciphertext.decode("ascii"),
        "hmac": h,
    }


def decrypt_features(crypto_obj: Dict[str, str], user_id: str) -> np.ndarray:
    """
    解密声纹特征向量并校验 HMAC。

    Args:
        crypto_obj: {"ciphertext": "...", "hmac": "..."}
        user_id: 用户ID

    Returns:
        float32 特征向量
    """
    f = derive_user_fernet(user_id)
    ciphertext = crypto_obj["ciphertext"].encode("ascii")

    expected_hmac = crypto_obj.get("hmac", "")
    actual_hmac = hmac.new(get_hmac_key(), ciphertext, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hmac, actual_hmac):
        raise ValueError("HMAC 校验失败：记录可能被篡改")

    payload = f.decrypt(ciphertext)
    return np.frombuffer(payload, dtype=np.float32)


def encrypt_export_payload(payload: bytes, user_id: str, password: str) -> str:
    """使用导出密钥加密用户导出包内容，返回 base64 字符串。"""
    f = derive_export_key(user_id, password)
    return f.encrypt(payload).decode("ascii")


def decrypt_export_payload(ciphertext_b64: str, user_id: str, password: str) -> bytes:
    """解密用户导出包内容。"""
    f = derive_export_key(user_id, password)
    return f.decrypt(ciphertext_b64.encode("ascii"))


def rotate_keys() -> Dict[str, str]:
    """
    轮换主密钥与 HMAC 密钥，并重新加密所有特征向量。
    注意：此操作会改变所有用户的派生密钥，需慎重。
    """
    from voice_anchor import load_manifest, save_manifest

    ensure_keys()
    old_master = MASTER_KEY_FILE.read_bytes()
    old_hmac = HMAC_KEY_FILE.read_bytes()

    manifest = load_manifest()
    reencrypted = 0
    for record in manifest.get("anchors", []):
        user_id = record.get("user_id", "system")
        crypto_obj = record.get("feature_vector_crypto")
        if crypto_obj:
            # 用旧密钥解密
            old_fernet = Fernet(old_master)
            old_hmac_key = old_hmac
            ct = crypto_obj["ciphertext"].encode("ascii")
            expected_hmac = crypto_obj["hmac"]
            actual_hmac = hmac.new(old_hmac_key, ct, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected_hmac, actual_hmac):
                continue
            payload = old_fernet.decrypt(ct)
            features = np.frombuffer(payload, dtype=np.float32)

            # 生成新密钥
            new_master = Fernet.generate_key()
            new_hmac = os.urandom(32)
            MASTER_KEY_FILE.write_bytes(new_master)
            HMAC_KEY_FILE.write_bytes(new_hmac)

            # 用新密钥加密
            record["feature_vector_crypto"] = encrypt_features(features, user_id)
            reencrypted += 1

    save_manifest(manifest)
    return {"status": "rotated", "reencrypted": reencrypted}
