#!/usr/bin/env python3
"""
龍魂密钥仓库 · Keyring
keyring.py

作者: 诸葛鑫（UID9622）
DNA: DNA::SPEC-9622-20260419-KEYRING-V1
铁律 D4: HMAC密钥永不离开9622服务器·外部只能验证·不能生成
铁律 D10: 私钥永不出设备·但仓库可跨设备同步
铁律 D9: 云端永不存明文·此仓库也不进 git

核心：
  - master.key 64字节随机·压缩存仓库·老大看不懂
  - 设备子密钥 = HMAC(master, device_id)·每台设备不同
  - 激活凭证 → PBKDF2哈希存储·多对一
  - L3 签发: HMAC_SHA256(master, L2_dna) → 前8位
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import socket
import time
import zlib
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path.home() / "longhun-system" / ".keyring"
VAULT_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

MASTER_KEY_FILE = VAULT_DIR / "master.key"
ACTIVATIONS_FILE = VAULT_DIR / "activations.json"
DEVICES_FILE = VAULT_DIR / "devices.json"
SESSION_FILE = VAULT_DIR / "session.json"

DNA_TAG = "DNA::SPEC-9622-20260419-KEYRING-V1"
SALT = b"UID9622_KEYRING_SALT_2026"
SESSION_TTL_SEC = 30 * 60  # 30 分钟

# ─────────────────────────────────────────────────────────
# 主密钥：首次自动生成·以后每次读取
# ─────────────────────────────────────────────────────────
def get_or_init_master() -> bytes:
    """主密钥·压缩+base64 armor 存仓库"""
    if MASTER_KEY_FILE.exists():
        data = MASTER_KEY_FILE.read_bytes()
        return zlib.decompress(base64.b64decode(data))

    # 首次：生成 64 字节随机密钥
    master = secrets.token_bytes(64)
    armored = base64.b64encode(zlib.compress(master, 9))
    MASTER_KEY_FILE.write_bytes(armored)
    MASTER_KEY_FILE.chmod(0o600)

    # 记一份初始化日志（不含密钥本身）
    init_log = {
        "initialized_at": datetime.now().isoformat(),
        "key_hash_sha256": hashlib.sha256(master).hexdigest()[:16],
        "dna": DNA_TAG,
        "note": "master key generated on first use · keep this dir backed up",
    }
    (VAULT_DIR / "init.log.json").write_text(
        json.dumps(init_log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return master

# ─────────────────────────────────────────────────────────
# 设备子密钥：HMAC(master, device_id)
# ─────────────────────────────────────────────────────────
def device_id() -> str:
    """本机设备唯一标识"""
    try:
        host = socket.gethostname()
    except Exception:
        host = "unknown"
    user = os.environ.get("USER", "unknown")
    return f"{user}@{host}"

def device_subkey(master: bytes = None) -> bytes:
    """为本机生成子密钥（确定性派生·不存盘）"""
    if master is None:
        master = get_or_init_master()
    return hmac.new(master, device_id().encode("utf-8"), hashlib.sha256).digest()

# ─────────────────────────────────────────────────────────
# 激活凭证（多对一·PBKDF2哈希存）
# ─────────────────────────────────────────────────────────
def _hash_activation(token: str) -> str:
    """凭证 → PBKDF2-SHA256 哈希"""
    dk = hashlib.pbkdf2_hmac("sha256", token.encode("utf-8"), SALT, 240000, 32)
    return base64.urlsafe_b64encode(dk).decode()

def load_activations() -> list:
    if not ACTIVATIONS_FILE.exists():
        return []
    try:
        return json.loads(ACTIVATIONS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_activations(lst: list):
    ACTIVATIONS_FILE.write_text(
        json.dumps(lst, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ACTIVATIONS_FILE.chmod(0o600)

def add_activation(token: str, label: str = "") -> dict:
    """添加激活凭证（存的是 PBKDF2 哈希·原文不落盘）"""
    if len(token) < 6:
        raise ValueError("凭证至少 6 个字符")
    h = _hash_activation(token)
    lst = load_activations()
    for entry in lst:
        if entry["hash"] == h:
            return {"added": False, "reason": "该凭证已存在", "label": entry.get("label")}
    entry = {
        "hash": h,
        "label": label or f"激活凭证 #{len(lst) + 1}",
        "added_at": datetime.now().isoformat(),
    }
    lst.append(entry)
    save_activations(lst)
    return {"added": True, "label": entry["label"]}

def verify_activation(token: str) -> dict:
    """验证凭证·返回匹配的 label 或 None"""
    h = _hash_activation(token)
    for entry in load_activations():
        if hmac.compare_digest(entry["hash"], h):
            return {"valid": True, "label": entry.get("label"), "added_at": entry.get("added_at")}
    return {"valid": False}

# ─────────────────────────────────────────────────────────
# 设备注册表
# ─────────────────────────────────────────────────────────
def load_devices() -> list:
    if not DEVICES_FILE.exists():
        return []
    try:
        return json.loads(DEVICES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_devices(lst: list):
    DEVICES_FILE.write_text(
        json.dumps(lst, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    DEVICES_FILE.chmod(0o600)

def register_device(activation_label: str = "") -> dict:
    """注册本机到设备表"""
    did = device_id()
    master = get_or_init_master()
    subkey = device_subkey(master)
    subkey_fingerprint = hashlib.sha256(subkey).hexdigest()[:16]

    lst = load_devices()
    for entry in lst:
        if entry["device_id"] == did:
            entry["last_activated"] = datetime.now().isoformat()
            entry["activation_label"] = activation_label
            save_devices(lst)
            return {"new": False, "device_id": did, "fingerprint": subkey_fingerprint}

    entry = {
        "device_id": did,
        "fingerprint": subkey_fingerprint,
        "first_activated": datetime.now().isoformat(),
        "last_activated": datetime.now().isoformat(),
        "activation_label": activation_label,
    }
    lst.append(entry)
    save_devices(lst)
    return {"new": True, "device_id": did, "fingerprint": subkey_fingerprint}

# ─────────────────────────────────────────────────────────
# 会话状态（激活后 30 分钟有效）
# ─────────────────────────────────────────────────────────
def load_session() -> dict:
    if not SESSION_FILE.exists():
        return {"active": False}
    try:
        return json.loads(SESSION_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"active": False}

def save_session(s: dict):
    SESSION_FILE.write_text(
        json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    SESSION_FILE.chmod(0o600)

def is_session_active() -> bool:
    s = load_session()
    if not s.get("active"):
        return False
    if time.time() - s.get("last_activity", 0) > SESSION_TTL_SEC:
        s["active"] = False
        s["auto_expired_at"] = time.time()
        save_session(s)
        return False
    return True

def touch_session():
    s = load_session()
    s["last_activity"] = time.time()
    save_session(s)

def start_session(activation_label: str):
    s = {
        "active": True,
        "started_at": time.time(),
        "last_activity": time.time(),
        "activation_label": activation_label,
        "device_id": device_id(),
    }
    save_session(s)

def end_session():
    s = load_session()
    s["active"] = False
    s["ended_at"] = time.time()
    save_session(s)

# ─────────────────────────────────────────────────────────
# L2 / L3 DNA 生成（按 Notion 规范）
# ─────────────────────────────────────────────────────────
def generate_l2_dna(event_type: str, tag: str, uid: str = "9622", version: str = "V1", precise: bool = True) -> str:
    """DNA::TYPE-UID-DATE[-TIME]-TAG-VER"""
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    if precise:
        date += f"-{now.strftime('%H%M%S')}"
    return f"DNA::{event_type}-{uid}-{date}-{tag}-{version}"

def sign_l3(l2_dna: str) -> str:
    """L3 = L2::HMAC(master, L2)[:8]"""
    master = get_or_init_master()
    sig = hmac.new(master, l2_dna.encode("utf-8"), hashlib.sha256).hexdigest()[:8]
    return f"{l2_dna}::{sig}"

def verify_l3(l3_code: str) -> bool:
    if "::" not in l3_code:
        return False
    parts = l3_code.rsplit("::", 1)
    if len(parts) != 2:
        return False
    l2_part, sig_part = parts
    master = get_or_init_master()
    expected = hmac.new(master, l2_part.encode("utf-8"), hashlib.sha256).hexdigest()[:8]
    return hmac.compare_digest(sig_part, expected)

# ─────────────────────────────────────────────────────────
# 数字根闸门（复刻 Notion 规范）
# ─────────────────────────────────────────────────────────
def digital_root(s: str) -> int:
    digits = [int(c) for c in s if c.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    while total >= 10:
        total = sum(int(c) for c in str(total))
    return total

def fuse_gate(s: str) -> str:
    dr = digital_root(s)
    if dr in (3, 9):
        return "🔴 熔断"
    if dr == 6:
        return "🟡 待审"
    return "🟢 通行"
