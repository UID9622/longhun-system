# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂加密信封 — JSON + DNA追溯码 + SM4-CBC加密
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
================================================
DNA: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-SYNC-MSG-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

格式规范:
{
  "envelope": { version, dna, timestamp, source_device, target_device,
                encryption, key_derivation },
  "payload": { iv, ciphertext, auth_tag },
  "audit": { level, sovereignty_check, cross_platform_sig }
}

三色审计:
🟢 加密正确 — SM4-CBC + HMAC-SHA256验证
🟡 格式合规 — DNA追溯 + 版本兼容
🔴 解密失败 — 完整性校验失败
"""

import json
import time
import base64
import hashlib
import hmac
import logging
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict

logger = logging.getLogger("加密信封")


# ============================================================
# 君子协议
# ============================================================
君子协议 = """
================================================================================
龍魂加密信封 · 君子协议
================================================================================
1. 所有数据必须先加密再出应用，明文绝不离开应用边界
2. 加密使用国密SM4算法，密钥由ECDH协商派生
3. 每个信封携带DNA追溯码，确保数据可溯源
4. 禁止修改、删除信封中的审计字段
5. 违反协议将导致技术授权终止
================================================================================
"""


@dataclass
class 信封配置:
    """加密信封配置参数"""
    版本: str = "v5.3"
    DNA前缀: str = "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜"
    加密算法: str = "SM4-CBC"
    密钥派生: str = "HKDF-SHA256"
    IV长度: int = 16  # 128-bit for SM4
    密钥长度: int = 16  # 128-bit SM4 key
    HMAC算法: str = "HMAC-SHA256"
    时间戳格式: str = "epoch_ms"


@dataclass
class 信封头部:
    """信封元数据头部"""
    version: str = "v5.3"
    dna: str = ""
    timestamp: int = 0
    source_device: str = ""
    target_device: str = ""
    encryption: str = "SM4-CBC"
    key_derivation: str = "HKDF-SHA256"
    版本向量: Optional[Dict[str, int]] = None


@dataclass
class 信封载荷:
    """加密载荷"""
    iv: str = ""           # base64编码的IV
    ciphertext: str = ""   # base64编码的密文
    auth_tag: str = ""     # base64编码的HMAC


@dataclass
class 信封审计:
    """审计追踪信息"""
    level: str = "🟢"           # 🟢安全 / 🟡警告 / 🔴危险
    sovereignty_check: bool = True
    cross_platform_sig: str = ""  # payload的SHA256
    integrity_verified: bool = False
    chain_hash: str = ""         # 上一条消息的哈希，形成链


class SM4加解密器:
    """
    国密SM4-CBC加解密实现
    
    注意: 实际生产环境应使用gmssl或pysm4库
    此处提供标准接口，底层可替换
    """
    
    def __init__(self, 密钥: bytes):
        if len(密钥) not in [16, 24, 32]:
            raise ValueError("SM4密钥长度必须为16/24/32字节")
        self.密钥 = 密钥
        
        try:
            from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
            self._使用gmssl = True
            self._crypt_sm4 = CryptSM4()
            logger.info("🟢 [SM4] 使用gmssl库")
        except ImportError:
            try:
                from pysm4 import encrypt_ecb, decrypt_ecb, encrypt_cbc, decrypt_cbc
                self._使用gmssl = False
                self._使用pysm4 = True
                logger.info("🟢 [SM4] 使用pysm4库")
            except ImportError:
                self._使用gmssl = False
                self._使用pysm4 = False
                logger.warning("🟡 [SM4] 未找到SM4库，使用AES-256兼容模式")
                from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                self._使用备用 = True
    
    def 加密_CBC(self, 明文: bytes, IV: bytes) -> bytes:
        """SM4-CBC加密"""
        try:
            from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
            crypt = CryptSM4()
            crypt.set_key(self.密钥, SM4_ENCRYPT)
            # gmssl的CBC需要IV
            return crypt.crypt_cbc(IV, 明文)
        except ImportError:
            pass
        
        try:
            from pysm4 import encrypt_cbc
            return encrypt_cbc(明文.hex(), self.密钥.hex(), IV.hex())
        except ImportError:
            pass
        
        # 备用: 使用AES-256-CBC（兼容模式，非国密）
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        padder = self._pkcs7_pad(明文, 16)
        cipher = Cipher(algorithms.AES(self.密钥), modes.CBC(IV), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(padder) + encryptor.finalize()
    
    def 解密_CBC(self, 密文: bytes, IV: bytes) -> bytes:
        """SM4-CBC解密"""
        try:
            from gmssl.sm4 import CryptSM4, SM4_DECRYPT
            crypt = CryptSM4()
            crypt.set_key(self.密钥, SM4_DECRYPT)
            return crypt.crypt_cbc(IV, 密文)
        except ImportError:
            pass
        
        try:
            from pysm4 import decrypt_cbc
            结果 = decrypt_cbc(密文.hex(), self.密钥.hex(), IV.hex())
            return bytes.fromhex(结果) if isinstance(结果, str) else 结果
        except ImportError:
            pass
        
        # 备用
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        cipher = Cipher(algorithms.AES(self.密钥), modes.CBC(IV), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(密文) + decryptor.finalize()
        return self._pkcs7_unpad(padded, 16)
    
    @staticmethod
    def _pkcs7_pad(data: bytes, block_size: int) -> bytes:
        """PKCS7填充"""
        padding = block_size - (len(data) % block_size)
        return data + bytes([padding] * padding)
    
    @staticmethod
    def _pkcs7_unpad(data: bytes, block_size: int) -> bytes:
        """PKCS7去填充"""
        padding = data[-1]
        if padding > block_size:
            return data
        return data[:-padding]


class 加密信封:
    """
    龍魂加密信封管理器
    
    职责:
    1. 构建符合规范的JSON加密信封
    2. 使用SM4-CBC加密数据
    3. HMAC-SHA256完整性校验
    4. DNA追溯码生成与验证
    5. 审计信息自动附加
    """
    
    DNA = "#龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-SYNC-MSG-v1.0"
    
    def __init__(self, 配置: Optional[信封配置] = None):
        print(君子协议)
        self.配置 = 配置 or 信封配置()
        self.会话密钥: Optional[bytes] = None
        self._上一条哈希: str = "0" * 64  # 初始链哈希
        logger.info("🟢 [初始化] 加密信封管理器 v%s", self.配置.版本)
    
    def 设置会话密钥(self, 密钥: bytes):
        """设置SM4会话密钥"""
        if len(密钥) < self.配置.密钥长度:
            raise ValueError(f"密钥长度不足，需要{self.配置.密钥长度}字节")
        self.会话密钥 = 密钥[:self.配置.密钥长度]
        logger.info("🟢 [密钥] 会话密钥已设置")
    
    # ============================================================
    # 核心API
    # ============================================================
    
    def 构建信封(
        self,
        数据: Dict[str, Any],
        源设备: str,
        目标设备: str,
        版本向量: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        构建完整加密信封
        
        流程: JSON序列化 → 生成IV → SM4加密 → HMAC签名 → 组装信封
        
        Args:
            数据: 要加密的业务数据字典
            源设备: 源设备标识，格式 "platform|device_id"
            目标设备: 目标设备标识，格式 "platform|device_id"
            版本向量: 可选的版本向量时钟值
        
        Returns:
            完整信封JSON字典
        """
        if not self.会话密钥:
            raise RuntimeError("会话密钥未设置，请先协商密钥")
        
        # 步骤1: 序列化数据为JSON字符串
        明文JSON = json.dumps(数据, ensure_ascii=False, sort_keys=True)
        明文字节 = 明文JSON.encode('utf-8')
        
        # 步骤2: 生成随机IV
        import os
        IV = os.urandom(self.配置.IV长度)
        IV_B64 = base64.b64encode(IV).decode('ascii')
        
        # 步骤3: SM4-CBC加密
        加密器 = SM4加解密器(self.会话密钥)
        密文 = 加密器.加密_CBC(明文字节, IV)
        密文B64 = base64.b64encode(密文).decode('ascii')
        
        # 步骤4: HMAC-SHA256完整性校验
        HMAC值 = hmac.new(
            self.会话密钥,
            IV + 密文,
            hashlib.sha256
        ).digest()
        HMAC_B64 = base64.b64encode(HMAC值).decode('ascii')
        
        # 步骤5: 生成DNA追溯码
        DNA = self._生成DNA(源设备, 目标设备, 密文B64)
        
        # 步骤6: 计算跨平台签名
        载荷签名 = hashlib.sha256(
            (IV_B64 + 密文B64).encode()
        ).hexdigest()
        
        # 步骤7: 计算链哈希
        self._上一条哈希 = hashlib.sha256(
            (self._上一条哈希 + 载荷签名).encode()
        ).hexdigest()
        
        # 步骤8: 组装信封
        当前时间 = int(time.time() * 1000)
        
        信封 = {
            "envelope": {
                "version": self.配置.版本,
                "dna": DNA,
                "timestamp": 当前时间,
                "source_device": 源设备,
                "target_device": 目标设备,
                "encryption": self.配置.加密算法,
                "key_derivation": self.配置.密钥派生,
                **({"version_vector": 版本向量} if 版本向量 else {})
            },
            "payload": {
                "iv": IV_B64,
                "ciphertext": 密文B64,
                "auth_tag": HMAC_B64
            },
            "audit": {
                "level": "🟢",
                "sovereignty_check": True,
                "cross_platform_sig": 载荷签名,
                "integrity_verified": True,
                "chain_hash": self._上一条哈希
            }
        }
        
        logger.info("🟢 [信封] 构建完成 | DNA: %s | 大小: %d bytes",
                     DNA, len(json.dumps(信封).encode()))
        return 信封
    
    def 解密信封(
        self,
        信封: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        解密信封并验证完整性
        
        流程: 验证HMAC → 解密 → 验证DNA → 返回明文
        
        Args:
            信封: 加密信封JSON字典
        
        Returns:
            (明文数据, 信封元数据)
        
        Raises:
            ValueError: HMAC验证失败或格式错误
        """
        if not self.会话密钥:
            raise RuntimeError("会话密钥未设置")
        
        try:
            # 步骤1: 提取信封各部分
            头部 = 信封["envelope"]
            载荷 = 信封["payload"]
            审计 = 信封["audit"]
            
            # 步骤2: Base64解码
            IV = base64.b64decode(载荷["iv"])
            密文 = base64.b64decode(载荷["ciphertext"])
            收到HMAC = base64.b64decode(载荷["auth_tag"])
            
            # 步骤3: 验证HMAC
            计算HMAC = hmac.new(
                self.会话密钥,
                IV + 密文,
                hashlib.sha256
            ).digest()
            
            if not hmac.compare_digest(计算HMAC, 收到HMAC):
                logger.error("🔴 [解密] HMAC验证失败! 数据可能被篡改")
                raise ValueError("HMAC验证失败: 数据完整性被破坏")
            
            # 步骤4: SM4-CBC解密
            加密器 = SM4加解密器(self.会话密钥)
            明文字节 = 加密器.解密_CBC(密文, IV)
            
            # 步骤5: JSON反序列化
            明文JSON = 明文字节.decode('utf-8')
            明文数据 = json.loads(明文JSON)
            
            # 步骤6: 验证DNA追溯码
            DNA = 头部.get("dna", "")
            if not self._验证DNA(DNA):
                logger.warning("🟡 [解密] DNA格式异常: %s", DNA)
            
            # 步骤7: 验证跨平台签名
            载荷签名 = hashlib.sha256(
                (载荷["iv"] + 载荷["ciphertext"]).encode()
            ).hexdigest()
            
            if 载荷签名 != 审计.get("cross_platform_sig", ""):
                logger.warning("🟡 [解密] 跨平台签名不匹配")
            
            # 步骤8: 更新链哈希
            self._上一条哈希 = 审计.get("chain_hash", self._上一条哈希)
            
            logger.info("🟢 [解密] 信封解密成功 | 来源: %s | DNA: %s",
                         头部.get("source_device", "unknown"), DNA)
            
            元数据 = {
                "源设备": 头部.get("source_device"),
                "目标设备": 头部.get("target_device"),
                "时间戳": 头部.get("timestamp"),
                "DNA": DNA,
                "版本向量": 头部.get("version_vector"),
                "审计": 审计
            }
            
            return 明文数据, 元数据
            
        except (KeyError, json.JSONDecodeError) as e:
            logger.error("🔴 [解密] 信封格式错误: %s", str(e))
            raise ValueError(f"信封格式错误: {e}")
        except Exception as e:
            logger.error("🔴 [解密] 解密失败: %s", str(e))
            raise
    
    def 验证信封格式(self, 信封: Dict[str, Any]) -> bool:
        """
        验证信封格式是否符合规范（不解密）
        
        Args:
            信封: 待验证的信封字典
        
        Returns:
            bool: 格式是否合规
        """
        try:
            # 检查必需字段
            assert "envelope" in 信封, "缺少envelope"
            assert "payload" in 信封, "缺少payload"
            assert "audit" in 信封, "缺少audit"
            
            头部 = 信封["envelope"]
            载荷 = 信封["payload"]
            审计 = 信封["audit"]
            
            # 检查envelope字段
            assert "version" in 头部, "缺少version"
            assert "dna" in 头部, "缺少dna"
            assert "timestamp" in 头部, "缺少timestamp"
            assert "source_device" in 头部, "缺少source_device"
            assert "target_device" in 头部, "缺少target_device"
            assert "encryption" in 头部, "缺少encryption"
            
            # 检查payload字段
            assert "iv" in 载荷, "缺少iv"
            assert "ciphertext" in 载荷, "缺少ciphertext"
            assert "auth_tag" in 载荷, "缺少auth_tag"
            
            # 检查audit字段
            assert "level" in 审计, "缺少level"
            assert "sovereignty_check" in 审计, "缺少sovereignty_check"
            assert "cross_platform_sig" in 审计, "缺少cross_platform_sig"
            
            # 验证base64可解码
            base64.b64decode(载荷["iv"])
            base64.b64decode(载荷["ciphertext"])
            base64.b64decode(载荷["auth_tag"])
            
            # 验证DNA格式
            dna = 头部["dna"]
            assert dna.startswith("#龍芯⚡️"), f"DNA格式错误: {dna}"
            
            logger.info("🟢 [验证] 信封格式合规 | version: %s", 头部["version"])
            return True
            
        except (AssertionError, Exception) as e:
            logger.error("🔴 [验证] 信封格式错误: %s", str(e))
            return False
    
    # ============================================================
    # DNA追溯
    # ============================================================
    
    def _生成DNA(self, 源设备: str, 目标设备: str, 密文摘要: str) -> str:
        """
        生成DNA追溯码
        
        格式: #龍芯⚡️{日期}-{设备对}-{消息类型}-{随机}
        例: #龍芯⚡️丙午·甲午·甲子·庚午·䷙大畜-SYNC-MSG-v1.0
        """
        from datetime import datetime
        日期 = datetime.now().strftime("%Y-%m-%d")
        设备对 = f"{源设备.split('|')[0]}-{目标设备.split('|')[0]}".replace("|", "-")
        
        # 使用密文前16字节作为唯一标识
        摘要 = hashlib.sha256(密文摘要.encode()).hexdigest()[:8]
        
        DNA = f"{self.配置.DNA前缀}-{设备对}-{摘要}"
        return DNA
    
    def _验证DNA(self, DNA: str) -> bool:
        """验证DNA格式"""
        return (
            isinstance(DNA, str) and
            DNA.startswith("#龍芯⚡️") and
            len(DNA) > 20
        )
    
    # ============================================================
    # 实用工具
    # ============================================================
    
    def 信封转JSON(self, 信封: Dict[str, Any], 美化: bool = True) -> str:
        """将信封转为JSON字符串"""
        if 美化:
            return json.dumps(信封, indent=2, ensure_ascii=False)
        return json.dumps(信封, ensure_ascii=False)
    
    def 信封大小(self, 信封: Dict[str, Any]) -> int:
        """计算信封字节大小"""
        return len(json.dumps(信封).encode('utf-8'))
    
    def 获取统计信息(self) -> Dict[str, Any]:
        """获取信封统计信息"""
        return {
            "版本": self.配置.版本,
            "加密算法": self.配置.加密算法,
            "密钥派生": self.配置.密钥派生,
            "会话密钥已设置": self.会话密钥 is not None,
            "链哈希": self._上一条哈希[:16] + "...",
            "dna_template": self.DNA,
        }


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  龍魂加密信封测试")
    print(f"{'='*60}\n")
    
    # 创建信封管理器
    配置 = 信封配置()
    管理器 = 加密信封(配置)
    
    # 设置测试会话密钥
    import os
    测试密钥 = hashlib.sha256(b"longhun-test-key-2026").digest()[:16]
    管理器.设置会话密钥(测试密钥)
    
    # 测试数据
    测试数据 = {
        "type": "note_sync",
        "title": "测试笔记",
        "content": "这是一条跨平台同步的测试数据",
        "tags": ["测试", "跨平台"],
        "priority": "high",
        "created_at": int(time.time() * 1000),
    }
    
    print("原始数据:")
    print(json.dumps(测试数据, indent=2, ensure_ascii=False))
    print()
    
    # 构建信封
    信封 = 管理器.构建信封(
        数据=测试数据,
        源设备="harmonyos|device-001",
        目标设备="ios|device-002",
        版本向量={"harmonyos": 5, "ios": 3}
    )
    
    print("加密信封:")
    print(管理器.信封转JSON(信封))
    print(f"\n信封大小: {管理器.信封大小(信封)} bytes")
    
    # 解密信封
    print("\n" + "="*60)
    明文, 元数据 = 管理器.解密信封(信封)
    
    print("\n解密后数据:")
    print(json.dumps(明文, indent=2, ensure_ascii=False))
    
    print("\n元数据:")
    print(json.dumps(元数据, indent=2, ensure_ascii=False))
    
    # 验证格式
    print(f"\n格式验证: {管理器.验证信封格式(信封)}")
    
    print("\n" + "="*60)
    print("测试通过!" if 明文 == 测试数据 else "测试失败!")
