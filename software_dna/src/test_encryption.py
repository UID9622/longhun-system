# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 DNA 协议 · 加密测试套件 v1.0
AES-256-GCM + KMS + 签章验证

DNA:#龍芯⚡️2026-06-07-DNA-ENCRYPTION-TEST-v1.0
责任: UID9622 · 不免责
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
# [测试数据]
# ============================================================================

PLAINTEXT_SAMPLES = [
    "龍魂系统·DNA 协议·敏感信息",
    "机密数据：用户密码和 API 密钥",
    "",  # 空字符串
    "a" * 1000,  # 大数据
    "特殊字符：!@#$%^&*()_+-={}[]|:;<>?,./",
]

ASSOCIATED_DATA = {
    "device_id": "device-9622",
    "timestamp": datetime.now().isoformat(),
    "user": "admin",
}


# ============================================================================
# [加密引擎测试]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安装")
class TestDNAEncryptionEngine:
    """加密引擎测试"""

    @pytest.fixture
    def engine(self):
        """创建加密引擎"""
        master_key = os.urandom(32)
        return DNAEncryptionEngine(master_key)

    def test_engine_initialization(self, engine):
        """测试引擎初始化"""
        assert engine.master_key is not None
        assert len(engine.master_key) == 32

    def test_key_generation(self, engine):
        """测试密钥生成"""
        key = engine.generate_key("test-key-001")

        assert key.key_id == "test-key-001"
        assert key.algorithm == EncryptionAlgorithm.AES_256_GCM
        assert len(key.key_material) == 32
        assert key.created_at is not None
        assert key.expires_at is not None

    def test_key_validity(self, engine):
        """测试密钥有效性"""
        key = engine.generate_key("validity-test", expires_in_days=1)

        # 新密钥应该有效
        assert key.is_valid() is True
        assert key.is_expired() is False

    def test_key_expiration(self, engine):
        """测试密钥过期"""
        key = engine.generate_key("expiry-test", expires_in_days=-1)  # 已过期

        assert key.is_valid() is False
        assert key.is_expired() is True

    def test_encrypt_decrypt_roundtrip(self, engine):
        """测试加密/解密往返"""
        plaintext = "龍魂系统·DNA 协议"
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
        """测试带附加数据的加密"""
        plaintext = "敏感信息"
        key_id = "aad-test"

        # 加密
        cipher_blob = engine.encrypt(plaintext, key_id, ASSOCIATED_DATA)

        # 验证 AAD 被保存
        assert cipher_blob.associated_data == ASSOCIATED_DATA

        # 解密应该成功
        decrypted = engine.decrypt(cipher_blob, key_id)
        assert decrypted == plaintext

    def test_encrypt_multiple_samples(self, engine):
        """测试多个样本加密"""
        for plaintext in PLAINTEXT_SAMPLES:
            key_id = f"sample-{hash(plaintext)}"

            # 加密
            cipher_blob = engine.encrypt(plaintext, key_id)

            # 解密
            decrypted = engine.decrypt(cipher_blob, key_id)

            # 验证
            assert decrypted == plaintext

    def test_different_keys_produce_different_ciphertexts(self, engine):
        """测试不同密钥产生不同的密文"""
        plaintext = "龍魂"

        cipher1 = engine.encrypt(plaintext, "key-1")
        cipher2 = engine.encrypt(plaintext, "key-2")

        # 相同明文，不同密钥，密文应该不同
        assert cipher1.ciphertext != cipher2.ciphertext

    def test_same_key_different_nonce(self, engine):
        """测试相同密钥不同 Nonce 产生不同密文"""
        plaintext = "龍魂"
        key_id = "nonce-test"

        cipher1 = engine.encrypt(plaintext, key_id)
        cipher2 = engine.encrypt(plaintext, key_id)

        # 同一密钥，相同明文，但 Nonce 不同，密文应该不同
        assert cipher1.nonce != cipher2.nonce
        assert cipher1.ciphertext != cipher2.ciphertext

    def test_sign_and_verify(self, engine):
        """测试签署和验证"""
        plaintext = "重要数据"

        # 签署
        signature = engine.sign(plaintext)

        # 验证
        is_valid = engine.verify(plaintext, signature)

        assert is_valid is True

    def test_signature_tampering_detection(self, engine):
        """测试签章窜改检测"""
        plaintext = "重要数据"

        signature = engine.sign(plaintext)

        # 篡改明文
        tampered_plaintext = "篡改的数据"

        is_valid = engine.verify(tampered_plaintext, signature)

        # 应该检测到篡改
        assert is_valid is False

    def test_signature_validation_with_wrong_signature(self, engine):
        """测试错误签章验证"""
        plaintext = "原始数据"
        wrong_signature = base64.b64encode(b"wrong_signature").decode()

        is_valid = engine.verify(plaintext, wrong_signature)

        assert is_valid is False

    def test_encrypt_empty_string(self, engine):
        """测试加密空字符串"""
        plaintext = ""
        key_id = "empty-test"

        cipher_blob = engine.encrypt(plaintext, key_id)
        decrypted = engine.decrypt(cipher_blob, key_id)

        assert decrypted == plaintext

    def test_encrypt_large_data(self, engine):
        """测试加密大数据"""
        plaintext = "x" * 10000  # 10KB
        key_id = "large-test"

        cipher_blob = engine.encrypt(plaintext, key_id)
        decrypted = engine.decrypt(cipher_blob, key_id)

        assert decrypted == plaintext
        assert len(cipher_blob.ciphertext) > 0

    def test_decrypt_with_wrong_key(self, engine):
        """测试使用错误密钥解密"""
        plaintext = "机密信息"

        cipher_blob = engine.encrypt(plaintext, "key-1")

        # 尝试用不存在的密钥解密
        with pytest.raises(ValueError):
            engine.decrypt(cipher_blob, "key-wrong")

    def test_cipher_blob_json_serialization(self, engine):
        """测试 CipherBlob JSON 序列化"""
        plaintext = "龍魂"

        cipher_blob = engine.encrypt(plaintext, "json-test", ASSOCIATED_DATA)

        # 转换为 JSON
        json_str = cipher_blob.to_json()
        data = json.loads(json_str)

        # 验证结构
        assert data['algorithm'] == "aes-256-gcm"
        assert data['ciphertext'] is not None
        assert data['nonce'] is not None
        assert data['tag'] is not None
        assert data['associated_data'] == ASSOCIATED_DATA

    def test_key_caching(self, engine):
        """测试密钥缓存"""
        key_id = "cache-test"

        # 生成密钥
        key1 = engine.generate_key(key_id)

        # 重新加密应该使用缓存
        key2 = engine.key_cache.get(key_id)

        assert key2 is not None
        assert key1.key_id == key2.key_id


# ============================================================================
# [KMS 服务测试]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安装")
class TestKMSService:
    """KMS 密钥管理服务测试"""

    @pytest.fixture
    def kms(self, tmp_path):
        """创建 KMS 服务"""
        return KMSService(str(tmp_path))

    def test_key_storage(self, kms):
        """测试密钥存储"""
        key = kms.engine.generate_key("storage-test")

        # 存储密钥
        success = kms.store_key(key)

        assert success is True

    def test_key_loading(self, kms):
        """测试密钥加载"""
        # 生成并存储
        key = kms.engine.generate_key("load-test")
        kms.store_key(key)

        # 加载
        loaded_key = kms.load_key("load-test")

        assert loaded_key is not None
        assert loaded_key.key_id == key.key_id
        assert loaded_key.key_material == key.key_material

    def test_load_nonexistent_key(self, kms):
        """测试加载不存在的密钥"""
        loaded_key = kms.load_key("nonexistent")

        assert loaded_key is None

    def test_key_rotation(self, kms):
        """测试密钥轮转"""
        # 生成初始密钥
        original_key = kms.engine.generate_key("rotation-test")
        kms.store_key(original_key)

        # 轮转密钥
        new_key = kms.rotate_key("rotation-test")

        assert new_key is not None
        assert new_key.rotation_count == 1
        assert new_key.key_material != original_key.key_material

    def test_multiple_key_rotation(self, kms):
        """测试多次密钥轮转"""
        key = kms.engine.generate_key("multi-rotation")
        kms.store_key(key)

        # 轮转 3 次
        for i in range(3):
            new_key = kms.rotate_key("multi-rotation")
            assert new_key is not None
            assert new_key.rotation_count == i + 1

    def test_key_expiration_metadata(self, kms):
        """测试密钥过期元数据"""
        key = kms.engine.generate_key("expiry-test", expires_in_days=1)
        kms.store_key(key)

        # 加载并检查过期时间
        loaded_key = kms.load_key("expiry-test")

        assert loaded_key is not None
        assert loaded_key.expires_at is not None


# ============================================================================
# [端到端加密工作流测试]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安装")
class TestEndToEndEncryption:
    """端到端加密工作流测试"""

    def test_complete_encryption_workflow(self, tmp_path):
        """完整的加密工作流"""
        # 1. 初始化引擎和 KMS
        engine = DNAEncryptionEngine()
        kms = KMSService(str(tmp_path))

        # 2. 生成并存储密钥
        key = engine.generate_key("workflow-test")
        kms.store_key(key)

        # 3. 加密数据
        plaintext = "龍魂系统·敏感数据"
        cipher_blob = engine.encrypt(plaintext, "workflow-test", ASSOCIATED_DATA)

        # 4. 签署密文
        signature = engine.sign(cipher_blob.to_json())

        # 5. 验证签章
        is_valid = engine.verify(cipher_blob.to_json(), signature)
        assert is_valid is True

        # 6. 加载密钥并解密
        loaded_key = kms.load_key("workflow-test")
        assert loaded_key is not None

        decrypted = engine.decrypt(cipher_blob, "workflow-test")
        assert decrypted == plaintext

    def test_secure_data_transmission(self, tmp_path):
        """安全数据传输模拟"""
        # 发送方
        sender_engine = DNAEncryptionEngine()
        plaintext = "机密消息：龍魂"
        cipher_blob = sender_engine.encrypt(plaintext, "transmission-key")
        signature = sender_engine.sign(cipher_blob.to_json())

        # 中间层 (模拟传输)
        transmitted_data = {
            "cipher": cipher_blob.to_dict(),
            "signature": signature,
        }

        # 接收方
        receiver_engine = DNAEncryptionEngine(sender_engine.master_key)  # 共享主密钥
        transmitted_cipher = CipherBlob(**transmitted_data['cipher'])

        # 验证签章
        is_valid = receiver_engine.verify(
            transmitted_cipher.to_json(),
            transmitted_data['signature']
        )
        assert is_valid is True

        # 解密
        decrypted = receiver_engine.decrypt(transmitted_cipher, "transmission-key")
        assert decrypted == plaintext


# ============================================================================
# [性能测试]
# ============================================================================

@pytest.mark.skipif(not ENCRYPTION_AVAILABLE, reason="cryptography 未安装")
class TestEncryptionPerformance:
    """加密性能测试"""

    def test_encryption_speed_1mb(self):
        """测试 1MB 数据加密速度"""
        engine = DNAEncryptionEngine()
        plaintext = "x" * (1024 * 1024)  # 1MB

        import time
        start = time.time()
        cipher_blob = engine.encrypt(plaintext, "perf-test")
        elapsed = time.time() - start

        # 应该在 1 秒内完成
        assert elapsed < 1.0
        print(f"✅ 1MB 加密耗时: {elapsed:.3f}s")

    def test_decryption_speed_1mb(self):
        """测试 1MB 数据解密速度"""
        engine = DNAEncryptionEngine()
        plaintext = "x" * (1024 * 1024)  # 1MB
        cipher_blob = engine.encrypt(plaintext, "perf-test")

        import time
        start = time.time()
        decrypted = engine.decrypt(cipher_blob, "perf-test")
        elapsed = time.time() - start

        # 应该在 1 秒内完成
        assert elapsed < 1.0
        assert decrypted == plaintext
        print(f"✅ 1MB 解密耗时: {elapsed:.3f}s")

    def test_key_generation_speed(self):
        """测试密钥生成速度"""
        engine = DNAEncryptionEngine()

        import time
        start = time.time()

        for i in range(10):
            engine.generate_key(f"perf-key-{i}")

        elapsed = time.time() - start

        # 10 个密钥应该在 5 秒内生成
        assert elapsed < 5.0
        print(f"✅ 10 个密钥生成耗时: {elapsed:.3f}s")


# ============================================================================
# [运行测试]
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
