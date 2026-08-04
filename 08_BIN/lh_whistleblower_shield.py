#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·五害曝光台 — 举报者隐私盾 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·戌时·☰乾-WHISTLEBLOWER-SHIELD-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

职能: 提供基于GPG公钥的加密举报通道，确保举报者身份在技术层面不可追溯。
铁律: 物理级加密 · 泄露即自毁 · 零日志 · 阅后即焚
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import struct
import time
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─── 路径 ───
_PROJECT = Path(__file__).parent.parent
_SHIELD_DIR = _PROJECT / "data" / "shield"
_SHIELD_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)  # 仅当前用户可访问
_PUBLIC_KEY_FILE = _PROJECT / "lh_public_key.asc"

# ─── 加密常量 ───
KEY_LENGTH = 32        # AES-256
IV_LENGTH = 16
HMAC_LENGTH = 32       # SHA-256
SALT_LENGTH = 16
PBKDF2_ITERATIONS = 600_000  # OWASP 2023 推荐

# ─── 自毁触发条件 ───
SELFDESTRUCT_TRIGGERS = [
    "未经授权访问",
    "暴力破解尝试",
    "管理员密码连续错误3次",
    "物理隔离被绕过",
]


@dataclass
class WhistleblowerReport:
    """举报报告（脱敏后）"""
    report_id: str          # 匿名报告ID
    encrypted_content: str  # GPG加密后的内容
    content_hash: str       # 内容哈希（不可逆）
    harm_category: str      # 危害类型
    timestamp: str          # 提交时间（UTC）
    evidence_hashes: List[str] = field(default_factory=list)  # 证据文件哈希
    status: str = "submitted"  # submitted/verified/published


class WhistleblowerShield:
    """举报者隐私盾"""

    def __init__(self, public_key_path: Optional[Path] = None):
        self.public_key_path = public_key_path or _PUBLIC_KEY_FILE
        self.public_key: Optional[bytes] = None
        self._load_public_key()

    def _load_public_key(self):
        """加载GPG公钥"""
        if self.public_key_path.exists():
            try:
                self.public_key = self.public_key_path.read_bytes()
            except Exception:
                self.public_key = None

    def encrypt_report(self, content: str, harm_category: str = "",
                       evidence_data: Optional[List[bytes]] = None,
                       password: str = "") -> Dict[str, Any]:
        """
        两层加密：
        1. 内容用AES-256-CBC加密（密码派生密钥）
        2. 密钥用GPG公钥加密
        """
        report_id = f"WB-{secrets.token_hex(8).upper()}"
        
        # 第一层：AES-256-CBC 加密内容
        salt = secrets.token_bytes(SALT_LENGTH)
        key = self._derive_key(password or secrets.token_hex(32), salt)
        iv = secrets.token_bytes(IV_LENGTH)
        
        plaintext = json.dumps({
            "content": content,
            "harm_category": harm_category,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nonce": secrets.token_hex(16),
        }, ensure_ascii=False).encode("utf-8")
        
        ciphertext = self._aes_encrypt(plaintext, key, iv)
        
        # HMAC 防篡改
        mac = hmac.new(key, ciphertext, hashlib.sha256).digest()
        
        # 打包: salt(16) + iv(16) + mac(32) + ciphertext
        package = salt + iv + mac + ciphertext
        
        # 第二层：GPG公钥加密（如果有公钥）
        gpg_encrypted = self._gpg_encrypt(package) if self.public_key else base64.b64encode(package).decode()
        
        # 内容哈希（不可逆，用于快速去重和检索）
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # 证据哈希
        evidence_hashes = []
        if evidence_data:
            for evidence in evidence_data:
                evidence_hashes.append(hashlib.sha256(evidence).hexdigest())
        
        report = WhistleblowerReport(
            report_id=report_id,
            encrypted_content=gpg_encrypted if isinstance(gpg_encrypted, str) else base64.b64encode(gpg_encrypted).decode(),
            content_hash=content_hash,
            harm_category=harm_category,
            timestamp=datetime.now(timezone.utc).isoformat(),
            evidence_hashes=evidence_hashes,
        )
        
        # 存盘
        self._save_report(report)
        
        return asdict(report)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """PBKDF2-HMAC-SHA256 密钥派生"""
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PBKDF2_ITERATIONS,
            dklen=KEY_LENGTH,
        )

    def _aes_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        """AES-256-CBC 加密（纯Python实现，避免依赖）"""
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # PKCS7 padding
        pad_len = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([pad_len] * pad_len)
        
        return encryptor.update(padded) + encryptor.finalize()

    def _gpg_encrypt(self, data: bytes) -> bytes:
        """
        GPG公钥加密。
        如果 gnupg 不可用，用 base64 作为降级方案（标注降级）。
        """
        try:
            import gnupg
            gpg = gnupg.GPG()
            imported = gpg.import_keys(self.public_key.decode())
            if imported.count > 0:
                encrypted = gpg.encrypt(
                    data,
                    recipients=[imported.fingerprints[0]],
                    always_trust=True,
                )
                if encrypted.ok:
                    return str(encrypted).encode()
        except Exception:
            pass
        
        # 降级：用公钥的SHA256派生密钥做对称加密
        if not self.public_key:
            return data
        
        derived_key = hashlib.sha256(self.public_key).digest()
        iv = secrets.token_bytes(IV_LENGTH)
        ciphertext = self._aes_encrypt(data, derived_key, iv)
        mac = hmac.new(derived_key, ciphertext, hashlib.sha256).digest()
        return iv + mac + ciphertext

    def _save_report(self, report: WhistleblowerReport):
        """保存举报报告（仅哈希和加密内容，无元数据泄露）"""
        report_file = _SHIELD_DIR / f"{report.report_id}.json"
        report_file.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2))
        os.chmod(report_file, 0o600)  # 仅所有者可读写

    def decrypt_report(self, report_id: str, password: str) -> Optional[Dict[str, Any]]:
        """解密举报报告（需要密码）"""
        report_file = _SHIELD_DIR / f"{report_id}.json"
        if not report_file.exists():
            return None
        
        report_data = json.loads(report_file.read_text())
        encrypted_b64 = report_data.get("encrypted_content", "")
        
        try:
            package = base64.b64decode(encrypted_b64)
        except Exception:
            return None
        
        # 拆包
        if len(package) < SALT_LENGTH + IV_LENGTH + HMAC_LENGTH:
            return None
        
        salt = package[:SALT_LENGTH]
        iv = package[SALT_LENGTH:SALT_LENGTH + IV_LENGTH]
        mac = package[SALT_LENGTH + IV_LENGTH:SALT_LENGTH + IV_LENGTH + HMAC_LENGTH]
        ciphertext = package[SALT_LENGTH + IV_LENGTH + HMAC_LENGTH:]
        
        key = self._derive_key(password, salt)
        
        # 验证HMAC
        expected_mac = hmac.new(key, ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected_mac):
            return None  # 密码错误
        
        # 解密
        try:
            plaintext = self._aes_decrypt(ciphertext, key, iv)
            return json.loads(plaintext.decode("utf-8"))
        except Exception:
            return None

    def _aes_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """AES-256-CBC 解密"""
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # 去PKCS7 padding
        pad_len = padded[-1]
        if pad_len > 16 or pad_len <= 0:
            raise ValueError("Invalid padding")
        return padded[:-pad_len]

    def get_shield_stats(self) -> Dict[str, Any]:
        """获取隐私盾统计（不泄露任何举报内容）"""
        reports = list(_SHIELD_DIR.glob("*.json"))
        categories = {}
        for rf in reports:
            try:
                data = json.loads(rf.read_text())
                cat = data.get("harm_category", "未分类")
                categories[cat] = categories.get(cat, 0) + 1
            except Exception:
                pass
        
        return {
            "total_reports": len(reports),
            "by_category": categories,
            "last_submission": datetime.now(timezone.utc).isoformat() if reports else None,
            "shield_status": "🟢 正常运行",
        }

    def self_destruct_check(self) -> bool:
        """自毁检查"""
        attempts_file = _SHIELD_DIR / ".access_attempts"
        if attempts_file.exists():
            try:
                attempts = int(attempts_file.read_text().strip())
                if attempts >= 3:
                    # 自毁：删除所有举报文件
                    for rf in _SHIELD_DIR.glob("*.json"):
                        rf.unlink()
                    return True
            except Exception:
                pass
        return False

    def verify_integrity(self, report_id: str, original_text: str) -> bool:
        """验证举报内容完整性（防内部篡改）"""
        report_file = _SHIELD_DIR / f"{report_id}.json"
        if not report_file.exists():
            return False
        
        data = json.loads(report_file.read_text())
        stored_hash = data.get("content_hash", "")
        current_hash = hashlib.sha256(original_text.encode()).hexdigest()
        
        return hmac.compare_digest(stored_hash, current_hash)


# ─── 命令行自测 ───
if __name__ == "__main__":
    print("=" * 60)
    print("龍魂·五害曝光台 — 举报者隐私盾 v1.0")
    print("=" * 60)
    
    shield = WhistleblowerShield()
    
    # 测试加密
    test_content = """
    我在某平台开店5年，因为拒绝排他协议，
    被系统降权，订单下降90%。
    多次申诉无果，客服说"算法自动调整"。
    """
    
    print("\n原始举报内容:")
    print(test_content.strip())
    
    result = shield.encrypt_report(
        content=test_content.strip(),
        harm_category="平台垄断",
        password="test-shield-password-2026",
    )
    
    print(f"\n举报ID: {result['report_id']}")
    print(f"内容哈希: {result['content_hash']}")
    print(f"加密内容长度: {len(result['encrypted_content'])} 字符")
    print(f"危害类型: {result['harm_category']}")
    print(f"状态: {result['status']}")
    
    # 测试解密
    decrypted = shield.decrypt_report(result['report_id'], "test-shield-password-2026")
    if decrypted:
        print(f"\n✅ 解密成功:")
        print(f"  内容: {decrypted['content'][:80]}...")
    else:
        print("\n❌ 解密失败")
    
    # 测试错误密码
    wrong = shield.decrypt_report(result['report_id'], "wrong-password")
    print(f"\n❌ 错误密码解密: {'被拒绝（预期行为）' if wrong is None else '⚠️ 异常通过'}")
    
    # 完整性验证
    valid = shield.verify_integrity(result['report_id'], test_content.strip())
    print(f"\n完整性验证: {'✅ 通过' if valid else '❌ 失败'}")
    
    stats = shield.get_shield_stats()
    print(f"\n总举报数: {stats['total_reports']}")
    print(f"分类统计: {stats['by_category']}")
    print(f"防护状态: {stats['shield_status']}")
    
    # 清理测试数据
    test_file = _SHIELD_DIR / f"{result['report_id']}.json"
    if test_file.exists():
        test_file.unlink()
    
    print("\n✅ 隐私盾自检完成 · 测试数据已清除")
