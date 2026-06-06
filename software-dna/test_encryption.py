#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 協議 · 加密測試套件 v1.0
AES-256-GCM + KMS + 簽章驗證

DNA: #龍芯⚡️2026-06-07-DNA-ENCRYPTION-TEST-v1.0
責任: UID9622 · 不免責
"""

import pytest
import os
import base64
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

try:
    from dna_encryption import (
        DNAEncryptionEngine,
        KMSService,
        EncryptionKey,
        EncryptionAlgorithm,
        CipherBlob,
    )
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False


# ============================================================================
# [測試數據]
# ============================================================================

PLAINTEXT_SAMPLES = [
    "龍魂系統·DNA 協議·敏感信息",
    "機密數據：用戶密碼和 API 密鑰",
    "",  # 空字符串
    "a" * 1000,  # 大數據
    "特殊字符：!@#$%^&*()_+-={}[]|:;<>?,./",
]

ASSOCIATED_DATA = {
    "device_id": "device-9622",
    "timestamp": datetime.now().isoformat(),
    "user": "admin",
}


# ============================================================================
# [加密引擎測試]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安裝")
class TestDNAEncryptionEngine:
    """加密引擎測試"""

    @pytest.fixture
    def engine(self):
        """創建加密引擎"""
        master_key = os.urandom(32)
        return DNAEncryptionEngine(master_key)

    def test_engine_initialization(self, engine):
        """測試引擎初始化"""
        assert engine.master_key is not None
        assert len(engine.master_key) == 32

    def test_key_generation(self, engine):
        """測試密鑰生成"""
        key = engine.generate_key("test-key-001")

        assert key.key_id == "test-key-001"
        assert key.algorithm == EncryptionAlgorithm.AES_256_GCM
        assert len(key.key_material) == 32
        assert key.created_at is not None
        assert key.expires_at is not None

    def test_key_validity(self, engine):
        """測試密鑰有效性"""
        key = engine.generate_key("validity-test", expires_in_days=1)

        # 新密鑰應該有效
        assert key.is_valid() is True
        assert key.is_expired() is False

    def test_key_expiration(self, engine):
        """測試密鑰過期"""
        key = engine.generate_key("expiry-test", expires_in_days=-1)  # 已過期

        assert key.is_valid() is False
        assert key.is_expired() is True

    def test_encrypt_decrypt_roundtrip(self, engine):
        """測試加密/解密往返"""
        plaintext = "龍魂系統·DNA 協議"
        key_id = "roundtrip-test"

        # 加密
        cipher_blob = engine.encrypt(plaintext, key_id)

        assert cipher_blob is not None
        assert cipher_blob.ciphertext != plaintext
        assert cipher_blob.nonce is not None
        assert cipher_blob.tag is not None

        # 解密
        decrypted = engine.decrypt(cipher_blob, key_id)

        assert decrypted == plaintext

    def test_encrypt_with_associated_data(self, engine):
        """測試帶附加數據的加密"""
        plaintext = "敏感信息"
        key_id = "aad-test"

        # 加密
        cipher_blob = engine.encrypt(plaintext, key_id, ASSOCIATED_DATA)

        # 驗證 AAD 被保存
        assert cipher_blob.associated_data == ASSOCIATED_DATA

        # 解密應該成功
        decrypted = engine.decrypt(cipher_blob, key_id)
        assert decrypted == plaintext

    def test_encrypt_multiple_samples(self, engine):
        """測試多個樣本加密"""
        for plaintext in PLAINTEXT_SAMPLES:
            key_id = f"sample-{hash(plaintext)}"

            # 加密
            cipher_blob = engine.encrypt(plaintext, key_id)

            # 解密
            decrypted = engine.decrypt(cipher_blob, key_id)

            # 驗證
            assert decrypted == plaintext

    def test_different_keys_produce_different_ciphertexts(self, engine):
        """測試不同密鑰產生不同的密文"""
        plaintext = "龍魂"

        cipher1 = engine.encrypt(plaintext, "key-1")
        cipher2 = engine.encrypt(plaintext, "key-2")

        # 相同明文，不同密鑰，密文應該不同
        assert cipher1.ciphertext != cipher2.ciphertext

    def test_same_key_different_nonce(self, engine):
        """測試相同密鑰不同 Nonce 產生不同密文"""
        plaintext = "龍魂"
        key_id = "nonce-test"

        cipher1 = engine.encrypt(plaintext, key_id)
        cipher2 = engine.encrypt(plaintext, key_id)

        # 同一密鑰，相同明文，但 Nonce 不同，密文應該不同
        assert cipher1.nonce != cipher2.nonce
        assert cipher1.ciphertext != cipher2.ciphertext

    def test_sign_and_verify(self, engine):
        """測試簽署和驗證"""
        plaintext = "重要數據"

        # 簽署
        signature = engine.sign(plaintext)

        # 驗證
        is_valid = engine.verify(plaintext, signature)

        assert is_valid is True

    def test_signature_tampering_detection(self, engine):
        """測試簽章竄改檢測"""
        plaintext = "重要數據"

        signature = engine.sign(plaintext)

        # 篡改明文
        tampered_plaintext = "篡改的數據"

        is_valid = engine.verify(tampered_plaintext, signature)

        # 應該檢測到篡改
        assert is_valid is False

    def test_signature_validation_with_wrong_signature(self, engine):
        """測試錯誤簽章驗證"""
        plaintext = "原始數據"
        wrong_signature = base64.b64encode(b"wrong_signature").decode()

        is_valid = engine.verify(plaintext, wrong_signature)

        assert is_valid is False

    def test_encrypt_empty_string(self, engine):
        """測試加密空字符串"""
        plaintext = ""
        key_id = "empty-test"

        cipher_blob = engine.encrypt(plaintext, key_id)
        decrypted = engine.decrypt(cipher_blob, key_id)

        assert decrypted == plaintext

    def test_encrypt_large_data(self, engine):
        """測試加密大數據"""
        plaintext = "x" * 10000  # 10KB
        key_id = "large-test"

        cipher_blob = engine.encrypt(plaintext, key_id)
        decrypted = engine.decrypt(cipher_blob, key_id)

        assert decrypted == plaintext
        assert len(cipher_blob.ciphertext) > 0

    def test_decrypt_with_wrong_key(self, engine):
        """測試使用錯誤密鑰解密"""
        plaintext = "機密信息"

        cipher_blob = engine.encrypt(plaintext, "key-1")

        # 嘗試用不存在的密鑰解密
        with pytest.raises(ValueError):
            engine.decrypt(cipher_blob, "key-wrong")

    def test_cipher_blob_json_serialization(self, engine):
        """測試 CipherBlob JSON 序列化"""
        plaintext = "龍魂"

        cipher_blob = engine.encrypt(plaintext, "json-test", ASSOCIATED_DATA)

        # 轉換為 JSON
        json_str = cipher_blob.to_json()
        data = json.loads(json_str)

        # 驗證結構
        assert data['algorithm'] == "aes-256-gcm"
        assert data['ciphertext'] is not None
        assert data['nonce'] is not None
        assert data['tag'] is not None
        assert data['associated_data'] == ASSOCIATED_DATA

    def test_key_caching(self, engine):
        """測試密鑰緩存"""
        key_id = "cache-test"

        # 生成密鑰
        key1 = engine.generate_key(key_id)

        # 重新加密應該使用緩存
        key2 = engine.key_cache.get(key_id)

        assert key2 is not None
        assert key1.key_id == key2.key_id


# ============================================================================
# [KMS 服務測試]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安裝")
class TestKMSService:
    """KMS 密鑰管理服務測試"""

    @pytest.fixture
    def kms(self, tmp_path):
        """創建 KMS 服務"""
        return KMSService(str(tmp_path))

    def test_key_storage(self, kms):
        """測試密鑰存儲"""
        key = kms.engine.generate_key("storage-test")

        # 存儲密鑰
        success = kms.store_key(key)

        assert success is True

    def test_key_loading(self, kms):
        """測試密鑰加載"""
        # 生成並存儲
        key = kms.engine.generate_key("load-test")
        kms.store_key(key)

        # 加載
        loaded_key = kms.load_key("load-test")

        assert loaded_key is not None
        assert loaded_key.key_id == key.key_id
        assert loaded_key.key_material == key.key_material

    def test_load_nonexistent_key(self, kms):
        """測試加載不存在的密鑰"""
        loaded_key = kms.load_key("nonexistent")

        assert loaded_key is None

    def test_key_rotation(self, kms):
        """測試密鑰輪轉"""
        # 生成初始密鑰
        original_key = kms.engine.generate_key("rotation-test")
        kms.store_key(original_key)

        # 輪轉密鑰
        new_key = kms.rotate_key("rotation-test")

        assert new_key is not None
        assert new_key.rotation_count == 1
        assert new_key.key_material != original_key.key_material

    def test_multiple_key_rotation(self, kms):
        """測試多次密鑰輪轉"""
        key = kms.engine.generate_key("multi-rotation")
        kms.store_key(key)

        # 輪轉 3 次
        for i in range(3):
            new_key = kms.rotate_key("multi-rotation")
            assert new_key is not None
            assert new_key.rotation_count == i + 1

    def test_key_expiration_metadata(self, kms):
        """測試密鑰過期元數據"""
        key = kms.engine.generate_key("expiry-test", expires_in_days=1)
        kms.store_key(key)

        # 加載並檢查過期時間
        loaded_key = kms.load_key("expiry-test")

        assert loaded_key is not None
        assert loaded_key.expires_at is not None


# ============================================================================
# [端到端加密工作流測試]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安裝")
class TestEndToEndEncryption:
    """端到端加密工作流測試"""

    def test_complete_encryption_workflow(self, tmp_path):
        """完整的加密工作流"""
        # 1. 初始化引擎和 KMS
        engine = DNAEncryptionEngine()
        kms = KMSService(str(tmp_path))

        # 2. 生成並存儲密鑰
        key = engine.generate_key("workflow-test")
        kms.store_key(key)

        # 3. 加密數據
        plaintext = "龍魂系統·敏感數據"
        cipher_blob = engine.encrypt(plaintext, "workflow-test", ASSOCIATED_DATA)

        # 4. 簽署密文
        signature = engine.sign(cipher_blob.to_json())

        # 5. 驗證簽章
        is_valid = engine.verify(cipher_blob.to_json(), signature)
        assert is_valid is True

        # 6. 加載密鑰並解密
        loaded_key = kms.load_key("workflow-test")
        assert loaded_key is not None

        decrypted = engine.decrypt(cipher_blob, "workflow-test")
        assert decrypted == plaintext

    def test_secure_data_transmission(self, tmp_path):
        """安全數據傳輸模擬"""
        # 發送方
        sender_engine = DNAEncryptionEngine()
        plaintext = "機密消息：龍魂"
        cipher_blob = sender_engine.encrypt(plaintext, "transmission-key")
        signature = sender_engine.sign(cipher_blob.to_json())

        # 中間層 (模擬傳輸)
        transmitted_data = {
            "cipher": cipher_blob.to_dict(),
            "signature": signature,
        }

        # 接收方
        receiver_engine = DNAEncryptionEngine(sender_engine.master_key)  # 共享主密鑰
        transmitted_cipher = CipherBlob(**transmitted_data['cipher'])

        # 驗證簽章
        is_valid = receiver_engine.verify(
            transmitted_cipher.to_json(),
            transmitted_data['signature']
        )
        assert is_valid is True

        # 解密
        decrypted = receiver_engine.decrypt(transmitted_cipher, "transmission-key")
        assert decrypted == plaintext


# ============================================================================
# [性能測試]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安裝")
class TestEncryptionPerformance:
    """加密性能測試"""

    def test_encryption_speed_1mb(self):
        """測試 1MB 數據加密速度"""
        engine = DNAEncryptionEngine()
        plaintext = "x" * (1024 * 1024)  # 1MB

        import time
        start = time.time()
        cipher_blob = engine.encrypt(plaintext, "perf-test")
        elapsed = time.time() - start

        # 應該在 1 秒內完成
        assert elapsed < 1.0
        print(f"✅ 1MB 加密耗時: {elapsed:.3f}s")

    def test_decryption_speed_1mb(self):
        """測試 1MB 數據解密速度"""
        engine = DNAEncryptionEngine()
        plaintext = "x" * (1024 * 1024)  # 1MB
        cipher_blob = engine.encrypt(plaintext, "perf-test")

        import time
        start = time.time()
        decrypted = engine.decrypt(cipher_blob, "perf-test")
        elapsed = time.time() - start

        # 應該在 1 秒內完成
        assert elapsed < 1.0
        assert decrypted == plaintext
        print(f"✅ 1MB 解密耗時: {elapsed:.3f}s")

    def test_key_generation_speed(self):
        """測試密鑰生成速度"""
        engine = DNAEncryptionEngine()

        import time
        start = time.time()

        for i in range(10):
            engine.generate_key(f"perf-key-{i}")

        elapsed = time.time() - start

        # 10 個密鑰應該在 5 秒內生成
        assert elapsed < 5.0
        print(f"✅ 10 個密鑰生成耗時: {elapsed:.3f}s")


# ============================================================================
# [運行測試]
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
