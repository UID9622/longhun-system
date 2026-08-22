#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权身份注册核心
LongHun UID9622 Sovereign Identity Registry Core

功能：
  - 生成唯一 UID9622-XXXXXX 编号
  - 生成 DNA 追溯码 #龍芯⚡️YYYYMMDD-REG-{hash8}
  - 计算 sovereign_hash = SHA256(uid + name + timestamp)
  - 生成一次性 confirm_code
  - 写入 ~/.龍魂/sovereign_registry/manifest.json（append-only）
  - 支持验证接口
  - 任何修改请求触发熔断并写入耻辱墙

DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-SOVEREIGN-REGISTRY-v1.0
"""

import os
import re
import json
import hashlib
import secrets
import datetime
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# 龍魂主权身份注册根目录
BASE_DIR = Path.home() / ".龍魂" / "sovereign_registry"
MANIFEST_PATH = BASE_DIR / "manifest.json"
SHAME_WALL_PATH = Path.home() / ".龍魂" / "shame_wall" / "sovereign.jsonl"
CARDS_DIR = BASE_DIR / "cards"

warnings.filterwarnings("ignore")


def ensure_dirs() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    SHAME_WALL_PATH.parent.mkdir(parents=True, exist_ok=True)


def sanitize_id_number(id_number: str) -> str:
    """清理证件号：仅保留字母、数字、部分符号。"""
    return re.sub(r"[^a-zA-Z0-9\-\/]", "", str(id_number))[:64]


def hash_id_number(id_number: str) -> str:
    """对证件号做本地 SHA-256 哈希。明文只在此函数内存中出现，不持久化。"""
    normalized = sanitize_id_number(id_number)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def sanitize_name(name: str) -> str:
    """清理姓名：允许中文、字母、空格、·。"""
    return re.sub(r"[^\u4e00-\u9fa5a-zA-Z\s\·\.]", "", str(name))[:32].strip()


def generate_uid() -> str:
    """生成唯一 UID9622 编号：UID9622-XXXXXX（6位大小写+数字）。"""
    suffix = secrets.token_urlsafe(6)[:6].upper()
    # 去掉可能存在的 - 和 _
    suffix = suffix.replace("-", "").replace("_", "")
    return f"UID9622-{suffix}"


def generate_dna(uid: str, timestamp: str) -> str:
    """生成 DNA 追溯码：#龍芯⚡️YYYYMMDD-REG-{hash8}"""
    date = datetime.datetime.fromisoformat(timestamp).strftime("%Y%m%d")
    hash8 = hashlib.sha256(f"{uid}:{timestamp}".encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️{date}-REG-{hash8}"


def generate_confirm_code() -> str:
    """生成一次性确认码：12位大小写+数字。"""
    return secrets.token_urlsafe(9)[:12].upper()


def compute_sovereign_hash(uid: str, name: str, timestamp: str) -> str:
    """计算主权哈希：SHA256(uid + name + timestamp)"""
    payload = f"{uid}:{name}:{timestamp}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_manifest() -> Dict[str, Any]:
    """加载主权身份 manifest.json。"""
    if not MANIFEST_PATH.exists():
        return {
            "version": "1.0",
            "schema": "sovereign-registry-v1",
            "immutable": True,
            "registry_dna": "#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-SOVEREIGN-REGISTRY-v1.0",
            "records": [],
        }
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: Dict[str, Any]) -> None:
    """保存 manifest.json。"""
    ensure_dirs()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def log_shame_wall(action: str, uid: Optional[str], reason: str, details: Optional[Dict] = None) -> None:
    """写入耻辱墙：任何试图修改/删除主权身份的行为。"""
    ensure_dirs()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "uid": uid,
        "reason": reason,
        "details": details or {},
    }
    with open(SHAME_WALL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def uid_exists(uid: str, manifest: Optional[Dict[str, Any]] = None) -> bool:
    """检查 UID 是否已存在。"""
    if manifest is None:
        manifest = load_manifest()
    return any(r.get("uid") == uid for r in manifest.get("records", []))


def id_number_exists(id_number_hash: str, manifest: Optional[Dict[str, Any]] = None) -> bool:
    """检查证件号是否已注册（基于哈希比对）。"""
    if manifest is None:
        manifest = load_manifest()
    return any(r.get("id_number_hash") == id_number_hash for r in manifest.get("records", []))


def register_sovereign_identity(
    name: str,
    id_type: str,
    id_number_hash: str,
    device_fingerprint: str = "",
    gpg_public_key: str = "",
) -> Dict[str, Any]:
    """
    注册 UID9622 主权身份。

    忠义铁律合规：本函数不再接收明文证件号，只接收证件号哈希。
    客户端应在本地完成证件号哈希后再调用，服务端全程不接触明文证件号。

    Args:
        name: 真实姓名
        id_type: 身份证/护照/退伍证
        id_number_hash: 证件号 SHA-256 哈希（本地生成）
        device_fingerprint: 设备指纹
        gpg_public_key: 可选 GPG 公钥

    Returns:
        注册结果字典
    """
    from audit import audit_registration

    name = sanitize_name(name)
    id_type = str(id_type).strip()[:32]
    id_number_hash = str(id_number_hash).strip()[:64]
    device_fingerprint = str(device_fingerprint).strip()[:256]
    gpg_public_key = str(gpg_public_key).strip()[:8192]

    if not name:
        return {"status": "error", "message": "姓名不能为空", "audit": "🔴"}
    if not id_number_hash:
        return {"status": "error", "message": "证件号哈希不能为空", "audit": "🔴"}
    if id_type not in ("身份证", "护照", "退伍证"):
        return {"status": "error", "message": "证件类型必须是：身份证、护照、退伍证", "audit": "🟡"}

    # 三色审计（基于哈希，不反推明文）
    audit = audit_registration(name, id_type, id_number_hash, device_fingerprint)
    if audit["level"] == "🔴":
        log_shame_wall("register_rejected", None, f"三色审计未通过: {audit.get('reason', '')}", audit)
        return {"status": "rejected", "message": audit.get("reason", "注册请求被三色审计拒绝"), "audit": audit}

    manifest = load_manifest()

    # 证件号重复检测（基于哈希）
    if id_number_exists(id_number_hash, manifest):
        log_shame_wall("register_rejected", None, "证件号已注册", {"id_number_hash": id_number_hash})
        return {"status": "duplicate", "message": "该证件号已注册主权身份", "audit": "🟡"}

    # 生成唯一 UID
    uid = generate_uid()
    while uid_exists(uid, manifest):
        uid = generate_uid()

    timestamp = datetime.datetime.now().isoformat()
    dna = generate_dna(uid, timestamp)
    sovereign_hash = compute_sovereign_hash(uid, name, timestamp)
    confirm_code = generate_confirm_code()

    record = {
        "uid": uid,
        "name": name,
        "id_type": id_type,
        "id_number_hash": id_number_hash,
        "device_fingerprint_hash": hashlib.sha256(device_fingerprint.encode("utf-8")).hexdigest() if device_fingerprint else "",
        "gpg_public_key": gpg_public_key,
        "sovereign_hash": sovereign_hash,
        "dna": dna,
        "confirm_code": confirm_code,
        "status": "active",
        "created_at": timestamp,
        "registered_at": timestamp,
    }

    manifest["records"].append(record)
    save_manifest(manifest)

    return {
        "status": "success",
        "message": "UID9622 主权身份注册成功",
        "uid": uid,
        "dna": dna,
        "sovereign_hash": sovereign_hash,
        "status_active": "active",
        "confirm_code": confirm_code,
        "created_at": timestamp,
        "audit": audit,
    }


def get_identity(uid: str) -> Optional[Dict[str, Any]]:
    """根据 UID 查询主权身份记录。"""
    manifest = load_manifest()
    for record in manifest.get("records", []):
        if record.get("uid") == uid:
            return record
    return None


def verify_identity(uid: str, signature: str) -> Dict[str, Any]:
    """
    验证主权身份。

    Args:
        uid: 主权身份ID
        signature: 用户签名（当前简化：与 confirm_code 或 sovereign_hash 比对）

    Returns:
        验证结果
    """
    record = get_identity(uid)
    if not record:
        return {"status": "not_found", "message": "主权身份不存在", "uid": uid}

    # 简化验证：签名可以是 confirm_code 或 sovereign_hash 的前16位
    valid = False
    if signature and (
        signature == record.get("confirm_code")
        or signature == record.get("sovereign_hash")
        or signature == record.get("sovereign_hash")[:16]
    ):
        valid = True

    if not valid:
        log_shame_wall("verify_failed", uid, "签名不匹配", {"signature_hash": hashlib.sha256(signature.encode()).hexdigest()})
        return {
            "status": "mismatch",
            "message": "签名不匹配",
            "uid": uid,
            "match": False,
        }

    return {
        "status": "verified",
        "message": "主权身份验证通过",
        "uid": uid,
        "match": True,
        "registered_at": record.get("registered_at"),
        "dna": record.get("dna"),
        "sovereign_hash": record.get("sovereign_hash"),
        "name": record.get("name"),
        "id_type": record.get("id_type"),
    }


def attempt_modification(uid: str, action: str, details: Optional[Dict] = None) -> Dict[str, Any]:
    """
    模拟修改/删除请求：触发🔴熔断，写入耻辱墙，返回拒绝。
    主权身份一旦注册不可更改。
    """
    log_shame_wall(action, uid, f"尝试{action}主权身份，触发熔断", details)
    return {
        "status": "fuse",
        "message": "主权身份不可修改、不可转让、不可删除",
        "uid": uid,
        "fuse_reason": "§9.52 量子态一次塌缩铁律 · 永久锚定",
        "audit": "🔴",
    }


def list_identities(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """列出所有主权身份摘要（脱敏）。"""
    manifest = load_manifest()
    records = manifest.get("records", [])
    if limit:
        records = records[-limit:]
    return [
        {
            "uid": r.get("uid"),
            "name": r.get("name"),
            "id_type": r.get("id_type"),
            "dna": r.get("dna"),
            "sovereign_hash": r.get("sovereign_hash"),
            "created_at": r.get("created_at"),
            "status": r.get("status"),
        }
        for r in records
    ]


if __name__ == "__main__":
    # 示例：客户端本地哈希后传入
    demo_hash = hash_id_number("110101199001011234")
    result = register_sovereign_identity("诸葛鑫", "身份证", demo_hash)
    print(json.dumps(result, ensure_ascii=False, indent=2))
