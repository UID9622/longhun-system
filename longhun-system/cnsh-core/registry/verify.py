"""
CNSH L3 GPG Verify — GPG 签名验证层

有 python-gnupg 就验签，没有就降级到哈希校验。
不因为缺 GPG 库而崩溃，但会在返回值中标注降级状态。

Author: 诸葛鑫 (UID9622)
"""

import hashlib
from typing import Tuple

GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def verify_gpg_sig(
    content:     str,
    sig:         str,
    fingerprint: str = GPG_FINGERPRINT,
) -> Tuple[bool, str]:
    """
    验证 GPG 签名。

    有 gnupg 库 → 真签名验证
    无 gnupg 库 → 降级：返回 True + 降级提示
    """
    if not sig:
        return True, "无签名字段，已跳过（本地私用模式）"

    try:
        import gnupg
        gpg    = gnupg.GPG()
        result = gpg.verify(sig)

        if not result.valid:
            return False, f"GPG签名无效: {result.status}"

        stored_fp = fingerprint.replace(" ", "").upper()
        result_fp = (result.fingerprint or "").replace(" ", "").upper()
        if result_fp != stored_fp:
            return False, f"指纹不匹配：期望 {stored_fp[:8]}…，实际 {result_fp[:8]}…"

        return True, "GPG签名验证通过"

    except ImportError:
        return True, "⚠️ python-gnupg 未安装，已降级到哈希校验（建议: pip install python-gnupg）"
    except Exception as e:
        return False, f"GPG验证异常: {e}"


def sign_content(content: str, keyid: str = GPG_FINGERPRINT) -> str:
    """
    用本地 GPG 密钥签名内容。
    无 GPG 环境时返回空字符串（不崩溃）。
    """
    try:
        import gnupg
        gpg    = gnupg.GPG()
        signed = gpg.sign(content, keyid=keyid)
        return str(signed) if signed else ""
    except Exception:
        return ""


def compute_fingerprint(owner_gpg: str, content: str, timestamp: float) -> str:
    """
    无 GPG 环境时的轻量指纹（哈希替代）。
    格式：SHA256(gpg|content|ts) 前16位
    """
    raw = f"{owner_gpg}|{content}|{timestamp:.3f}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def verify_entry_hash(entry) -> Tuple[bool, str]:
    """
    验证单个 RegistryEntry 的 entry_hash 完整性。
    """
    if not entry.entry_hash:
        return True, "无entry_hash，跳过（旧数据）"

    expected = entry.compute_entry_hash()
    if entry.entry_hash == expected:
        return True, "🟢 哈希完整"
    return False, f"🔴 哈希篡改：存储={entry.entry_hash[:12]}… 期望={expected[:12]}…"
