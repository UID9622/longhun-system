#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·主权身份密钥生成器
生成 Ed25519 身份密钥对，私钥物理隔离存储于 ~/.longhun/identity/
公钥可注册到鲲鹏服务端 resident_registry。

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-KEYGEN-v1.0
"""
import os
import sys
import json
import stat
import base64
from pathlib import Path
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


SOVEREIGN_UID = "9622"
PRIVATE_DIR = Path.home() / ".longhun" / "identity"
PUBLIC_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "resident_registry"


def ensure_dir(path: Path, mode: int = 0o700) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, mode)


def derive_key_from_passphrase(passphrase: str, salt: bytes) -> bytes:
    """用 PBKDF2 从口令派生 32 字节密钥，用于本地私钥加密存储。"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def generate_identity_keypair(passphrase: str | None = None) -> tuple[bytes, bytes, dict]:
    """
    生成 Ed25519 身份密钥对。
    返回: (private_pem, public_pem, metadata)
    """
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # 元数据
    meta = {
        "uid": SOVEREIGN_UID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "Ed25519",
        "purpose": "sovereign_identity_broadcast",
        "dna": "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-v1.0",
        "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }

    if passphrase:
        # 用口令加密私钥存储
        salt = os.urandom(16)
        # 注意: cryptography 库没有内置 Ed25519 加密，这里只存储原始私钥字节并用 AES 封装
        private_raw = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        aes_key = derive_key_from_passphrase(passphrase, salt)
        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, private_raw, json.dumps(meta, ensure_ascii=False).encode("utf-8"))
        encrypted_pem = {
            "version": "v1",
            "salt": base64.b64encode(salt).decode("ascii"),
            "nonce": base64.b64encode(nonce).decode("ascii"),
            "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
            "meta": meta,
        }
        private_bytes = json.dumps(encrypted_pem, ensure_ascii=False, indent=2).encode("utf-8")
    else:
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_bytes, public_bytes, meta


def load_private_key(passphrase: str | None = None) -> Ed25519PrivateKey:
    """从 ~/.longhun/identity/uid9622_private.enc 加载私钥。"""
    private_path = PRIVATE_DIR / "uid9622_private.enc"
    if not private_path.exists():
        raise FileNotFoundError(f"私钥不存在: {private_path}")

    data = json.loads(private_path.read_text(encoding="utf-8"))
    if "ciphertext" in data:
        if not passphrase:
            raise ValueError("私钥已加密，需要提供 passphrase")
        salt = base64.b64decode(data["salt"])
        nonce = base64.b64decode(data["nonce"])
        ciphertext = base64.b64decode(data["ciphertext"])
        aes_key = derive_key_from_passphrase(passphrase, salt)
        aesgcm = AESGCM(aes_key)
        private_raw = aesgcm.decrypt(nonce, ciphertext, json.dumps(data["meta"], ensure_ascii=False).encode("utf-8"))
        return Ed25519PrivateKey.from_private_bytes(private_raw)
    else:
        # 兼容未加密的 PEM
        return serialization.load_pem_private_key(
            private_path.read_bytes(), password=None
        )


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="龍魂主权身份密钥生成器")
    parser.add_argument("--passphrase", "-p", help="加密私钥的口令（推荐）")
    parser.add_argument("--force", "-f", action="store_true", help="强制重新生成（会覆盖旧私钥）")
    args = parser.parse_args()

    ensure_dir(PRIVATE_DIR)
    ensure_dir(PUBLIC_DIR)

    private_path = PRIVATE_DIR / "uid9622_private.enc"
    public_path = PUBLIC_DIR / "uid9622_identity.pub"
    meta_path = PUBLIC_DIR / "uid9622_identity.json"

    if private_path.exists() and not args.force:
        print(f"[⚠️] 私钥已存在: {private_path}")
        print("    如需重新生成，请加 --force（会覆盖旧私钥）。")
        return 1

    print("[🔥] 正在生成 UID9622 主权身份密钥对...")
    private_bytes, public_bytes, meta = generate_identity_keypair(args.passphrase)

    private_path.write_bytes(private_bytes)
    os.chmod(private_path, stat.S_IRUSR | stat.S_IWUSR)  # 0600

    public_path.write_bytes(public_bytes)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[✅] 私钥已物理隔离存储: {private_path} (权限 0600)")
    print(f"[✅] 公钥已注册: {public_path}")
    print(f"[✅] 元数据: {meta_path}")
    print(f"[🧬] DNA: {meta['dna']}")
    print(f"[🌌] 主权确认码: {meta['confirm_code']}")
    print("\n[📌] 下一步: 把公钥同步到鲲鹏服务器的 data/resident_registry/ 目录下。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
