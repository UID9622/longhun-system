# -*- coding: utf-8 -*-
"""
CNSH v2.1 国密 SM4 + GPG 加密签章模块
DNA: #龍芯⚡️2026-06-29-CNSH-CRYPTO-v2.1

依赖：
- SM4：本地 vendored 的 sm4 包（MIT License，作者 Eric Wong）
- GPG：本地 vendored 的 python-gnupg（BSD License）+ 系统 gpg 命令

设计原则：
- 密钥从用户口令经 SHA-256 派生为 16 字节 SM4 密钥。
- 密文使用 base64 编码为字符串，便于 CNSH 文本处理。
- GPG 使用独立 home 目录，默认懒加载生成 CNSH 签名密钥。
"""
import base64
import hashlib
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from ._vendor.sm4 import SM4Key
from ._vendor import gnupg


class CNSHCryptoError(Exception):
    pass


# ---------- SM4 ----------
def _derive_sm4_key(密钥: str) -> bytes:
    if isinstance(密钥, bytes):
        data = 密钥
    else:
        data = str(密钥).encode("utf-8")
    return hashlib.sha256(data).digest()[:16]


def sm4_encrypt(明文: str, 密钥: str) -> str:
    """SM4 加密，带 SHA-256 完整性校验，返回 base64 字符串。"""
    key = _derive_sm4_key(密钥)
    cipher = SM4Key(key)
    data = str(明文).encode("utf-8")
    digest = hashlib.sha256(data).digest()
    payload = digest + data
    encrypted = cipher.encrypt(payload, padding=True)
    return base64.b64encode(encrypted).decode("ascii")


def sm4_decrypt(密文: str, 密钥: str) -> str:
    """SM4 解密，校验 SHA-256 完整性，返回原文本。"""
    key = _derive_sm4_key(密钥)
    cipher = SM4Key(key)
    data = base64.b64decode(str(密文).encode("ascii"))
    decrypted = cipher.decrypt(data, padding=True)
    if len(decrypted) < 32:
        raise CNSHCryptoError("密文长度不足，完整性校验失败")
    stored_digest = decrypted[:32]
    plain_bytes = decrypted[32:]
    actual_digest = hashlib.sha256(plain_bytes).digest()
    if stored_digest != actual_digest:
        raise CNSHCryptoError("完整性校验失败，密钥错误或密文被篡改")
    return plain_bytes.decode("utf-8")


# ---------- GPG ----------
def _default_gpg_home() -> Path:
    home = Path.home() / ".longhun" / "cnsh_gpg"
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    return home


def _get_gpg(home: Optional[Path] = None) -> gnupg.GPG:
    gpg_home = home or _default_gpg_home()
    binary = os.environ.get("GPG_BINARY", "gpg")
    gpg = gnupg.GPG(gnupghome=str(gpg_home), gpgbinary=binary)
    gpg.encoding = "utf-8"
    return gpg


def _ensure_default_key(gpg: gnupg.GPG, passphrase: str = "CNSH-UID9622-LONGHUN") -> str:
    """确保存在默认 CNSH 签名密钥，返回 fingerprint。"""
    uid = "CNSH-Default-Key <cnsh@longhun.local>"
    keys = gpg.list_keys(keys=uid)
    if keys:
        return keys[0]["fingerprint"]

    input_data = gpg.gen_key_input(
        name_real="CNSH-Default-Key",
        name_email="cnsh@longhun.local",
        passphrase=passphrase,
        key_type="RSA",
        key_length=2048,
        expire_date="0",
    )
    key = gpg.gen_key(input_data)
    if not key:
        raise CNSHCryptoError("GPG 默认密钥生成失败")
    return key.fingerprint


def gpg_sign(数据: str, 密钥指纹: Optional[str] = None, passphrase: str = "CNSH-UID9622-LONGHUN") -> str:
    """GPG 分离签章，返回 ASCII armor 签名。"""
    gpg = _get_gpg()
    fingerprint = 密钥指纹 or _ensure_default_key(gpg, passphrase)

    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir) / "data"
        sig_path = Path(tmpdir) / "sig.asc"
        data_path.write_bytes(str(数据).encode("utf-8"))

        with open(data_path, "rb") as f:
            sig = gpg.sign_file(
                f,
                keyid=fingerprint,
                passphrase=passphrase,
                detach=True,
                output=str(sig_path),
            )
        if not sig or not sig_path.exists():
            raise CNSHCryptoError("GPG 签章失败")
        return sig_path.read_text(encoding="ascii")


def gpg_verify(数据: str, 签名: str, 密钥指纹: Optional[str] = None) -> bool:
    """GPG 验签。"""
    gpg = _get_gpg()
    # 若提供了外部公钥指纹，可在此扩展导入逻辑
    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir) / "data"
        sig_path = Path(tmpdir) / "sig.asc"
        data_path.write_bytes(str(数据).encode("utf-8"))
        sig_path.write_text(str(签名), encoding="ascii")

        with open(sig_path, "rb") as f:
            verified = gpg.verify_file(f, data_filename=str(data_path))
        return bool(verified.valid)


def gpg_import_key(公钥文本: str) -> str:
    """导入 GPG 公钥，返回 fingerprint。"""
    gpg = _get_gpg()
    result = gpg.import_keys(公钥文本)
    if not result or not result.fingerprints:
        raise CNSHCryptoError("GPG 公钥导入失败")
    return result.fingerprints[0]


def gpg_export_public_key(密钥指纹: Optional[str] = None) -> str:
    """导出默认公钥 ASCII armor。"""
    gpg = _get_gpg()
    fingerprint = 密钥指纹 or _ensure_default_key(gpg)
    return gpg.export_keys(fingerprint)
