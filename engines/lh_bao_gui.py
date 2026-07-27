#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·宝柜 (BaoGui) · 本地加密保险柜引擎 v1.0
对应协议: 01_protocols/LH-CODE-NAMING-STANDARD-v1.0.md
内部命名: vault → bao_gui
DNA: #龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-BAO-GUI-v1.0
"""

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 优先使用 cryptography，否则使用 hashlib 降级
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

HOME = Path.home()
BAOGUI_DIR = HOME / ".longhun" / "baogui"
DATA_DIR = BAOGUI_DIR / "data"
AUDIT_LOG = BAOGUI_DIR / "audit.jsonl"
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥時·☰乾-BAO-GUI-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

CST = timezone(timedelta(hours=8))


def _now() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")


def _device_salt() -> bytes:
    """设备盐：从硬件信息派生，不暴露原始值"""
    raw = f"{HOME}|{os.uname().nodename}|{os.getlogin()}|UID9622".encode("utf-8")
    return hashlib.sha256(raw).digest()


def _derive_key(password: str, salt: bytes) -> bytes:
    """PBKDF2-HMAC-SHA256 派生 32 字节密钥"""
    if HAS_CRYPTO:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000,
        )
        return kdf.derive(password.encode("utf-8"))
    else:
        # 降级：仅供无依赖环境测试，不建议生产
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=32)


def _make_dna_trace(action: str, item: str) -> str:
    stamp = _now()
    base = f"{DNA}|{action}|{item}|{stamp}|{CONFIRM}"
    return f"{DNA}-{_short_hash(base)}"


def _short_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:12].upper()


def _ensure_dirs():
    BAOGUI_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _audit(action: str, item: str, status: str, detail: str = ""):
    _ensure_dirs()
    entry = {
        "time": _now(),
        "dna": _make_dna_trace(action, item),
        "action": action,
        "item": item,
        "status": status,
        "detail": detail,
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class BaoGui:
    """本地加密保险柜：数据根留本机，AES-256-GCM 加密"""

    def __init__(self, password: Optional[str] = None):
        self.salt = _device_salt()
        if password is None:
            password = os.environ.get("BAOGUI_PASSWORD", "")
        if not password:
            raise RuntimeError("宝柜需要密码：环境变量 BAOGUI_PASSWORD 或构造函数传入")
        self.key = _derive_key(password, self.salt)
        self._token = secrets.token_hex(8)
        _ensure_dirs()
        _audit("init", "baogui", "ok", f"token={self._token[:8]}")

    def _encrypt(self, plaintext: bytes) -> bytes:
        if HAS_CRYPTO:
            iv = secrets.token_bytes(12)
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv))
            encryptor = cipher.encryptor()
            ct = encryptor.update(plaintext) + encryptor.finalize()
            tag = encryptor.tag
            return base64.b64encode(iv + tag + ct)
        else:
            # 降级：简单 XOR+MAC（仅用于无依赖测试）
            iv = secrets.token_bytes(32)
            ct = bytes(b ^ self.key[i % 32] ^ iv[i % 32] for i, b in enumerate(plaintext))
            mac = hmac.new(self.key, iv + ct, hashlib.sha256).digest()
            return base64.b64encode(iv + mac + ct)

    def _decrypt(self, payload: bytes) -> bytes:
        raw = base64.b64decode(payload)
        if HAS_CRYPTO:
            iv, tag, ct = raw[:12], raw[12:28], raw[28:]
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            return decryptor.update(ct) + decryptor.finalize()
        else:
            iv, mac, ct = raw[:32], raw[32:64], raw[64:]
            expected = hmac.new(self.key, iv + ct, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected):
                raise ValueError("MAC 校验失败")
            return bytes(b ^ self.key[i % 32] ^ iv[i % 32] for i, b in enumerate(ct))

    def _file_path(self, name: str) -> Path:
        safe = _short_hash(name)
        return DATA_DIR / f"{safe}.bg"

    def put(self, name: str, content: str, category: str = "general") -> str:
        """写入保险柜，返回 DNA 追溯码"""
        if not name:
            raise ValueError("name 不能为空")
        record = {
            "name": name,
            "category": category,
            "content": content,
            "created": _now(),
            "version": 1,
        }
        payload = json.dumps(record, ensure_ascii=False).encode("utf-8")
        path = self._file_path(name)
        path.write_bytes(self._encrypt(payload))
        dna = _make_dna_trace("put", name)
        _audit("put", name, "ok", dna)
        return dna

    def get(self, name: str) -> Dict:
        """读取保险柜内容"""
        path = self._file_path(name)
        if not path.exists():
            _audit("get", name, "not_found")
            raise FileNotFoundError(f"宝柜中不存在: {name}")
        payload = path.read_bytes()
        record = json.loads(self._decrypt(payload))
        dna = _make_dna_trace("get", name)
        _audit("get", name, "ok", dna)
        return record

    def delete(self, name: str, confirm_code: str = "") -> str:
        """删除需要 DNA 确认码"""
        if confirm_code != CONFIRM:
            _audit("delete", name, "denied", "确认码错误")
            raise PermissionError("删除宝柜内容需要提供正确 DNA 确认码")
        path = self._file_path(name)
        if path.exists():
            path.unlink()
        dna = _make_dna_trace("delete", name)
        _audit("delete", name, "ok", dna)
        return dna

    def list(self) -> List[Dict]:
        """列出所有条目（不含内容）"""
        items = []
        for f in sorted(DATA_DIR.glob("*.bg")):
            try:
                record = json.loads(self._decrypt(f.read_bytes()))
                items.append({
                    "name": record["name"],
                    "category": record.get("category", "general"),
                    "created": record.get("created", ""),
                    "version": record.get("version", 1),
                })
            except Exception:
                continue
        return items


def _self_test() -> bool:
    print("=" * 50)
    print("龍魂·宝柜引擎自检")
    print("=" * 50)
    bg = BaoGui(password="test-password-9622")
    # 写入
    dna = bg.put("test_secret", "这是只有老大能看的内容", category="sensitive")
    print(f"  ✅ 写入: {dna}")
    # 读取
    rec = bg.get("test_secret")
    assert rec["content"] == "这是只有老大能看的内容"
    print(f"  ✅ 读取内容一致")
    # 列出
    items = bg.list()
    assert any(i["name"] == "test_secret" for i in items)
    print(f"  ✅ 列出条目: {len(items)}")
    # 删除需要确认码
    try:
        bg.delete("test_secret", "wrong")
        assert False, "应该拒绝"
    except PermissionError:
        print("  ✅ 错误确认码被拒绝")
    bg.delete("test_secret", CONFIRM)
    print("  ✅ 正确确认码删除成功")
    print("🟢 宝柜自检全部通过")
    return True


def main():
    parser = argparse.ArgumentParser(description="龍魂·宝柜 (BaoGui) 加密保险柜")
    parser.add_argument("--password", help="保险柜密码（推荐环境变量 BAOGUI_PASSWORD）")
    parser.add_argument("--self-test", action="store_true", help="运行自检")
    parser.add_argument("--put", metavar="NAME", help="写入条目")
    parser.add_argument("--get", metavar="NAME", help="读取条目")
    parser.add_argument("--list", action="store_true", help="列出条目")
    parser.add_argument("--delete", metavar="NAME", help="删除条目（需 --confirm）")
    parser.add_argument("--confirm", default="", help=f"删除确认码，例如 {CONFIRM}")
    parser.add_argument("--content", default="", help="写入内容")
    parser.add_argument("--category", default="general", help="分类")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return

    pwd = args.password or os.environ.get("BAOGUI_PASSWORD") or getpass.getpass("宝柜密码: ")
    bg = BaoGui(password=pwd)

    if args.put:
        dna = bg.put(args.put, args.content, args.category)
        print(f"已写入: {args.put}")
        print(f"DNA: {dna}")
    elif args.get:
        rec = bg.get(args.get)
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    elif args.list:
        for item in bg.list():
            print(f"[{item['category']}] {item['name']} · {item['created']}")
    elif args.delete:
        dna = bg.delete(args.delete, args.confirm)
        print(f"已删除: {args.delete} · {dna}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
