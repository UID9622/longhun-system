#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 協議 · 加密模塊 v1.0
AES-256-GCM + KMS + 簽章驗證

DNA:#龍芯⚡️2026-06-07-DNA-ENCRYPTION-v1.0
責任: UID9622 · 不免責
"""

import os
import json
import base64
import logging
import hashlib
import hmac
from typing import Tuple, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    logging.warning("cryptography 未安裝")


# ============================================================================
# [日誌配置]
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# [數據結構]
# ============================================================================

class EncryptionAlgorithm(Enum):
    """加密算法"""
    AES_256_GCM = "aes-256-gcm"
    AES_256_CBC = "aes-256-cbc"
    CHACHA20 = "chacha20"


@dataclass
class EncryptionKey:
    """加密密鑰"""
    key_id: str
    algorithm: EncryptionAlgorithm
    key_material: bytes
    created_at: str
    expires_at: Optional[str] = None
    rotation_count: int = 0

    def is_expired(self) -> bool:
        """檢查是否過期"""
        if not self.expires_at:
            return False
        return datetime.fromisoformat(self.expires_at) < datetime.now()

    def is_valid(self) -> bool:
        """檢查是否有效"""
        return not self.is_expired()


@dataclass
class CipherBlob:
    """密文對象"""
    algorithm: str
    ciphertext: str  # base64 編碼
    nonce: str      # base64 編碼
    tag: str        # base64 編碼 (GCM tag)
    associated_data: Optional[Dict] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'algorithm': self.algorithm,
            'ciphertext': self.ciphertext,
            'nonce': self.nonce,
            'tag': self.tag,
            'associated_data': self.associated_data,
            'timestamp': self.timestamp,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


# ============================================================================
# [加密引擎]
# ============================================================================

class DNAEncryptionEngine:
    """DNA 加密引擎"""

    def __init__(self, master_key: Optional[bytes] = None):
        """
        初始化引擎

        Args:
            master_key: 主密鑰 (可選，否則使用環境變量)
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ImportError("cryptography 庫未安裝")

        self.master_key = master_key or self._load_master_key()
        self.key_cache: Dict[str, EncryptionKey] = {}

    def _load_master_key(self) -> bytes:
        """從環境變量加載主密鑰"""
        key_b64 = os.getenv('DNA_MASTER_KEY')

        if not key_b64:
            logger.warning("未設置 DNA_MASTER_KEY，使用生成的臨時密鑰")
            return os.urandom(32)

        return base64.b64decode(key_b64)

    def generate_key(
        self,
        key_id: str,
        algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM,
        expires_in_days: int = 90
    ) -> EncryptionKey:
        """
        生成加密密鑰

        Args:
            key_id: 密鑰 ID
            algorithm: 加密算法
            expires_in_days: 過期天數

        Returns:
            加密密鑰對象
        """
        # 使用 PBKDF2 派生密鑰
        salt = os.urandom(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        derived_key = kdf.derive(self.master_key)

        expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()

        key = EncryptionKey(
            key_id=key_id,
            algorithm=algorithm,
            key_material=derived_key,
            created_at=datetime.now().isoformat(),
            expires_at=expires_at,
        )

        self.key_cache[key_id] = key
        logger.info(f"✅ 生成密鑰: {key_id}")

        return key

    def encrypt(
        self,
        plaintext: str,
        key_id: str,
        associated_data: Optional[Dict] = None
    ) -> CipherBlob:
        """
        加密文本

        Args:
            plaintext: 明文
            key_id: 密鑰 ID
            associated_data: 附加數據 (用於完整性驗證)

        Returns:
            密文對象
        """
        # 獲取或生成密鑰
        if key_id not in self.key_cache:
            key = self.generate_key(key_id)
        else:
            key = self.key_cache[key_id]

        if not key.is_valid():
            raise ValueError(f"密鑰已過期: {key_id}")

        # 生成隨機 nonce
        nonce = os.urandom(12)  # 96 bits for GCM

        # 準備附加數據
        aad = None
        if associated_data:
            aad = json.dumps(associated_data, sort_keys=True, ensure_ascii=False).encode()

        # 加密
        cipher = AESGCM(key.key_material)
        ciphertext = cipher.encrypt(nonce, plaintext.encode(), aad)

        # 分離密文和 tag (GCM 在末尾附加 tag)
        actual_ciphertext = ciphertext[:-16]
        tag = ciphertext[-16:]

        # 返回密文對象
        return CipherBlob(
            algorithm=key.algorithm.value,
            ciphertext=base64.b64encode(actual_ciphertext).decode(),
            nonce=base64.b64encode(nonce).decode(),
            tag=base64.b64encode(tag).decode(),
            associated_data=associated_data,
        )

    def decrypt(
        self,
        cipher_blob: CipherBlob,
        key_id: str
    ) -> str:
        """
        解密文本

        Args:
            cipher_blob: 密文對象
            key_id: 密鑰 ID

        Returns:
            明文
        """
        # 獲取密鑰
        if key_id not in self.key_cache:
            raise ValueError(f"密鑰不存在: {key_id}")

        key = self.key_cache[key_id]

        # 解碼
        nonce = base64.b64decode(cipher_blob.nonce)
        ciphertext = base64.b64decode(cipher_blob.ciphertext)
        tag = base64.b64decode(cipher_blob.tag)

        # 重組密文 (ciphertext + tag)
        full_ciphertext = ciphertext + tag

        # 準備附加數據
        aad = None
        if cipher_blob.associated_data:
            aad = json.dumps(cipher_blob.associated_data, sort_keys=True, ensure_ascii=False).encode()

        # 解密
        try:
            cipher = AESGCM(key.key_material)
            plaintext = cipher.decrypt(nonce, full_ciphertext, aad)
            logger.info(f"✅ 解密成功: {key_id}")
            return plaintext.decode()

        except Exception as e:
            logger.error(f"❌ 解密失敗: {e}")
            raise ValueError(f"解密失敗，可能是密鑰或數據損壞")

    def sign(self, data: str) -> str:
        """
        簽署數據 (HMAC-SHA256)

        Args:
            data: 數據

        Returns:
            簽章 (hex)
        """
        signature = hmac.new(
            self.master_key,
            data.encode(),
            hashlib.sha256
        ).digest()

        return base64.b64encode(signature).decode()

    def verify(self, data: str, signature: str) -> bool:
        """
        驗證簽章

        Args:
            data: 數據
            signature: 簽章

        Returns:
            是否有效
        """
        expected_sig = self.sign(data)
        return hmac.compare_digest(expected_sig, signature)


# ============================================================================
# [KMS 密鑰管理服務]
# ============================================================================

class KMSService:
    """密鑰管理服務"""

    def __init__(self, kms_store: str = '/tmp/dna_kms'):
        self.kms_store = kms_store
        self.engine = DNAEncryptionEngine()
        os.makedirs(kms_store, exist_ok=True)

    def store_key(self, key: EncryptionKey) -> bool:
        """存儲密鑰"""
        try:
            key_file = os.path.join(self.kms_store, f"{key.key_id}.key")

            data = {
                'key_id': key.key_id,
                'algorithm': key.algorithm.value,
                'key_material': base64.b64encode(key.key_material).decode(),
                'created_at': key.created_at,
                'expires_at': key.expires_at,
                'rotation_count': key.rotation_count,
            }

            with open(key_file, 'w') as f:
                json.dump(data, f)

            logger.info(f"✅ 密鑰已存儲: {key.key_id}")
            return True

        except Exception as e:
            logger.error(f"❌ 存儲密鑰失敗: {e}")
            return False

    def load_key(self, key_id: str) -> Optional[EncryptionKey]:
        """加載密鑰"""
        try:
            key_file = os.path.join(self.kms_store, f"{key_id}.key")

            if not os.path.exists(key_file):
                logger.warning(f"密鑰文件不存在: {key_id}")
                return None

            with open(key_file, 'r') as f:
                data = json.load(f)

            key = EncryptionKey(
                key_id=data['key_id'],
                algorithm=EncryptionAlgorithm(data['algorithm']),
                key_material=base64.b64decode(data['key_material']),
                created_at=data['created_at'],
                expires_at=data.get('expires_at'),
                rotation_count=data.get('rotation_count', 0),
            )

            logger.info(f"✅ 密鑰已加載: {key_id}")
            return key

        except Exception as e:
            logger.error(f"❌ 加載密鑰失敗: {e}")
            return None

    def rotate_key(self, key_id: str) -> Optional[EncryptionKey]:
        """輪轉密鑰"""
        old_key = self.load_key(key_id)

        if not old_key:
            logger.error(f"密鑰不存在: {key_id}")
            return None

        # 生成新密鑰
        new_key = self.engine.generate_key(
            f"{key_id}_v{old_key.rotation_count + 1}",
            old_key.algorithm
        )

        # 更新計數器
        new_key.rotation_count = old_key.rotation_count + 1

        # 存儲新密鑰
        self.store_key(new_key)
        logger.info(f"✅ 密鑰已輪轉: {key_id}")

        return new_key


# ============================================================================
# [命令行示例]
# ============================================================================

def main():
    """示例用法"""
    # 初始化引擎
    engine = DNAEncryptionEngine()

    # [1] 生成密鑰
    key = engine.generate_key("dna-master-001")
    print(f"✅ 密鑰已生成: {key.key_id}")

    # [2] 加密
    plaintext = "龍魂系統·DNA 協議·敏感信息"
    associated_data = {
        "device_id": "device-9622",
        "timestamp": datetime.now().isoformat(),
    }

    cipher_blob = engine.encrypt(plaintext, "dna-master-001", associated_data)
    print(f"✅ 加密成功")
    print(f"   密文: {cipher_blob.ciphertext[:50]}...")

    # [3] 簽署
    signature = engine.sign(plaintext)
    print(f"✅ 簽署成功: {signature[:40]}...")

    # [4] 解密
    decrypted = engine.decrypt(cipher_blob, "dna-master-001")
    print(f"✅ 解密成功: {decrypted}")

    # [5] 驗證簽章
    is_valid = engine.verify(plaintext, signature)
    print(f"✅ 簽章驗證: {'有效' if is_valid else '無效'}")

    # [6] KMS 服務
    kms = KMSService()
    kms.store_key(key)
    loaded_key = kms.load_key("dna-master-001")
    print(f"✅ KMS 密鑰加載: {loaded_key.key_id if loaded_key else '失敗'}")

    # [7] 密鑰輪轉
    new_key = kms.rotate_key("dna-master-001")
    print(f"✅ 密鑰輪轉: {new_key.key_id if new_key else '失敗'}")


if __name__ == '__main__':
    main()
