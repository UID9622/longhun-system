#!/usr/bin/env python3
# ════════════════════════════════════════════════
# 🏠 龍魂·时光机快照模块 v1.1
# 文件：~/longhun-system/time_machine.py
# DNA：#龍芯⚡️2026-04-06-时光机快照-v1.1
# 用途：每次对话自动留痕·本地加密·AI可读
# 加密：AES-256-CBC（cryptography低级API）
# 数字指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ════════════════════════════════════════════════
# v1.1 变更：Fernet(AES-128) → AES-256-CBC，与文档一致

import json
import os
import struct
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend

# ── 配置区（只改这里）──
CACHE_DIR = os.path.expanduser("~/longhun-system/cache")
KEY_FILE  = os.path.expanduser("~/longhun-system/.dna_key")

def init_key():
    """生成并保存本地 AES-256 密钥（只运行一次）"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.exists(KEY_FILE):
        key = os.urandom(32)          # 256 bit = 32 bytes
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        os.chmod(KEY_FILE, 0o600)     # 只有老大自己能读
        print("✅ AES-256 密钥已生成，只存你本地，不上云")
    else:
        print("🔑 密钥已存在，跳过生成")

def load_key() -> bytes:
    """读取本地 AES-256 密钥（32字节）"""
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    if len(key) != 32:
        raise ValueError("密钥长度异常，应为32字节(AES-256)")
    return key

def _encrypt(plaintext: bytes, key: bytes) -> bytes:
    """AES-256-CBC 加密，前16字节为随机IV"""
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor()
    return iv + enc.update(padded) + enc.finalize()

def _decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """AES-256-CBC 解密"""
    iv, data = ciphertext[:16], ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    dec = cipher.decryptor()
    padded = dec.update(data) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()

def save_snapshot(summary: str, trigger: str = "manual", persona: str = "宝宝P02"):
    """
    保存对话快照到本地（AES-256-CBC加密）

    参数：
        summary  - 这次对话在干什么（一句话）
        trigger  - 触发来源（manual/auto/cron）
        persona  - 当前激活的人格
    """
    key = load_key()

    snapshot = {
        "timestamp":      datetime.now().isoformat(),
        "session_id":     f"UID9622-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "trigger":        trigger,
        "persona_active": persona,
        "dna":            f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-对话快照-v1.1",
        "encrypt":        "AES-256-CBC",
        "content":        summary,
        "context_ref":    "longhun_auto_sync_v4.py",
        "gpg":            "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "confirm_code":   "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }

    encrypted = _encrypt(json.dumps(snapshot, ensure_ascii=False).encode(), key)

    filename = f"{CACHE_DIR}/snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dna"
    with open(filename, "wb") as f:
        f.write(encrypted)

    print(f"✅ 快照已存（AES-256）：{filename}")
    return filename

def read_snapshot(filepath: str) -> dict:
    """解密读取快照（本地宝宝专用）"""
    key = load_key()
    with open(filepath, "rb") as f:
        data = f.read()
    return json.loads(_decrypt(data, key).decode())

def list_snapshots() -> list:
    """列出所有快照（按时间倒序）"""
    if not os.path.exists(CACHE_DIR):
        return []
    files = sorted(
        [f for f in os.listdir(CACHE_DIR) if f.endswith(".dna")],
        reverse=True
    )
    return [os.path.join(CACHE_DIR, f) for f in files]

# ── 使用示例 ──
if __name__ == "__main__":
    init_key()
    save_snapshot(
        summary="老大聊了设备容器+时光机快照方案",
        trigger="auto",
        persona="宝宝P02"
    )
    print("\n📂 最近快照：")
    for snap in list_snapshots()[:3]:
        data = read_snapshot(snap)
        print(f"  {data['timestamp']} → {data['content']}")
