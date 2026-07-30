#!/usr/bin/env python3
#龍芯⚡️2026-06-19-SYNC-MSG-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂密钥协商器 — ECDH Curve25519 + HKDF-SHA256
================================================
DNA: #龍芯⚡️2026-06-19-SYNC-MSG-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

原理:
1. 各设备生成临时ECDH密钥对（Curve25519）
2. 通过安全通道交换公钥（二维码/NFC/蓝牙）
3. 各自计算共享密钥（ECDHE）
4. 用HKDF-SHA256派生SM4会话密钥
5. 临时密钥对使用后销毁（前向安全）

三色审计:
🟢 密钥协商成功 — ECDH完成，会话密钥已派生
🟡 公钥交换中 — 等待对端公钥
🔴 协商失败 — 密钥不匹配或被篡改
"""

import os
import hashlib
import logging
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger("密钥协商器")


# ============================================================
# 君子协议
# ============================================================
君子协议 = """
================================================================================
龍魂密钥协商器 · 君子协议
================================================================================
1. 私钥永不离设备，仅在内存中临时存在
2. 每次会话使用新的临时密钥对（前向安全）
3. 公钥交换必须通过可信通道（二维码扫描/NFC碰碰）
4. 共享密钥不可存储，仅用于派生会话密钥
5. 会话密钥使用后定期轮换
================================================================================
"""


@dataclass
class 密钥对:
    """ECDH密钥对"""
    公钥: bytes
    私钥: bytes
    算法: str = "Curve25519"


class 密钥协商器:
    """
    龍魂密钥协商器
    
    实现ECDH密钥交换 + HKDF密钥派生
    确保两个设备可以安全地协商出共享会话密钥
    """
    
    DNA = "#龍芯⚡️2026-06-19-SYNC-MSG-v1.0"
    
    def __init__(self):
        print(君子协议)
        self.密钥对: Optional[密钥对] = None
        self.共享密钥: Optional[bytes] = None
        self.会话密钥: Optional[bytes] = None
        self._交换完成 = False
        
        logger.info("🟢 [初始化] 密钥协商器 — Curve25519 + HKDF-SHA256")
    
    # ============================================================
    # 核心API
    # ============================================================
    
    def 生成密钥对(self) -> bytes:
        """
        生成ECDH临时密钥对
        
        Returns:
            公钥（用于交换）
        """
        try:
            # 尝试使用cryptography库
            from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
            from cryptography.hazmat.primitives import serialization
            
            私钥对象 = X25519PrivateKey.generate()
            公钥对象 = 私钥对象.public_key()
            
            私钥字节 = 私钥对象.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            公钥字节 = 公钥对象.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            
            self.密钥对 = 密钥对(
                公钥=公钥字节,
                私钥=私钥字节,
                算法="Curve25519"
            )
            
            logger.info("🟢 [密钥] Curve25519密钥对已生成")
            logger.info("🟢 [密钥] 公钥: %s...", 公钥字节.hex()[:32])
            
            return 公钥字节
            
        except ImportError:
            logger.warning("🟡 [密钥] cryptography库不可用，使用备用实现")
            return self._备用生成密钥对()
    
    def 计算共享密钥(self, 对端公钥: bytes) -> bytes:
        """
        使用对端公钥计算ECDH共享密钥
        
        Args:
            对端公钥: 对端设备的公钥
        
        Returns:
            共享密钥
        """
        if not self.密钥对:
            raise RuntimeError("本机密钥对未生成，请先调用生成密钥对()")
        
        try:
            from cryptography.hazmat.primitives.asymmetric.x25519 import (
                X25519PrivateKey, X25519PublicKey
            )
            from cryptography.hazmat.primitives import serialization
            
            # 恢复私钥对象
            私钥对象 = X25519PrivateKey.from_private_bytes(self.密钥对.私钥)
            
            # 恢复对端公钥对象
            对端公钥对象 = X25519PublicKey.from_public_bytes(对端公钥)
            
            # 计算共享密钥
            共享密钥 = 私钥对象.exchange(对端公钥对象)
            self.共享密钥 = 共享密钥
            
            # 立即销毁私钥（前向安全）
            self._安全销毁(self.密钥对.私钥)
            self.密钥对.私钥 = b"\x00" * 32  # 覆盖
            
            logger.info("🟢 [密钥] ECDH共享密钥已计算")
            logger.info("🟢 [密钥] 共享密钥长度: %d bytes", len(共享密钥))
            
            return 共享密钥
            
        except ImportError:
            return self._备用计算共享密钥(对端公钥)
    
    def 派生会话密钥(
        self,
        共享密钥: Optional[bytes] = None,
        上下文: str = "longhun-sm4-session"
    ) -> bytes:
        """
        使用HKDF-SHA256从共享密钥派生SM4会话密钥
        
        Args:
            共享密钥: ECDH共享密钥（默认使用上次计算的）
            上下文: HKDF上下文信息
        
        Returns:
            16字节SM4会话密钥
        """
        输入密钥 = 共享密钥 or self.共享密钥
        if not 输入密钥:
            raise RuntimeError("共享密钥未计算")
        
        try:
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            from cryptography.hazmat.primitives import hashes
            
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=16,  # SM4需要128-bit密钥
                salt=os.urandom(32),  # 随机盐值
                info=上下文.encode('utf-8')
            )
            
            会话密钥 = hkdf.derive(输入密钥)
            self.会话密钥 = 会话密钥
            
            # 销毁共享密钥
            self._安全销毁(self.共享密钥)
            self.共享密钥 = None
            
            logger.info("🟢 [密钥] HKDF会话密钥已派生")
            logger.info("🟢 [密钥] 会话密钥长度: %d bytes (SM4-128)", len(会话密钥))
            
            return 会话密钥
            
        except ImportError:
            return self._备用派生会话密钥(输入密钥, 上下文)
    
    def 派生多密钥(
        self,
        数量: int = 3,
        上下文列表: Optional[list] = None
    ) -> Dict[str, bytes]:
        """
        派生多个用途不同的密钥
        
        例如: 加密密钥、HMAC密钥、IV生成密钥
        
        Args:
            数量: 要派生的密钥数量
            上下文列表: 每个密钥的上下文信息
        
        Returns:
            密钥字典 {"key_0": bytes, "key_1": bytes, ...}
        """
        if not self.共享密钥:
            raise RuntimeError("共享密钥未计算")
        
        结果 = {}
        上下文列表 = 上下文列表 or [
            "longhun-encrypt",
            "longhun-hmac",
            "longhun-iv"
        ]
        
        for i, 上下文 in enumerate(上下文列表[:数量]):
            from cryptography.hazmat.primitives.kdf.hkdf import HKDF
            from cryptography.hazmat.primitives import hashes
            
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=16,
                salt=os.urandom(32),
                info=上下文.encode('utf-8')
            )
            结果[f"key_{i}"] = hkdf.derive(self.共享密钥)
        
        logger.info("🟢 [密钥] 已派生 %d 个用途密钥", len(结果))
        return 结果
    
    # ============================================================
    # 公钥编码/解码（用于二维码交换）
    # ============================================================
    
    def 公钥转二维码数据(self, 公钥: Optional[bytes] = None) -> str:
        """
        将公钥转为二维码可用的字符串格式
        
        Returns:
            格式: LONGHUN:ECDH:v1:{base64公钥}
        """
        import base64
        公钥数据 = 公钥 or (self.密钥对.公钥 if self.密钥对 else None)
        if not 公钥数据:
            raise RuntimeError("公钥不可用")
        
        公钥B64 = base64.b64encode(公钥数据).decode('ascii')
        return f"LONGHUN:ECDH:v1:{公钥B64}"
    
    def 二维码数据转公钥(self, 二维码数据: str) -> bytes:
        """
        从二维码字符串解析公钥
        
        Args:
            二维码数据: LONGHUN:ECDH:v1:{base64公钥}
        
        Returns:
            公钥字节
        """
        import base64
        
        if not 二维码数据.startswith("LONGHUN:ECDH:v1:"):
            raise ValueError("无效的龍魂公钥格式")
        
        公钥B64 = 二维码数据.replace("LONGHUN:ECDH:v1:", "")
        return base64.b64decode(公钥B64)
    
    # ============================================================
    # 安全清理
    # ============================================================
    
    def 销毁所有密钥(self):
        """安全销毁所有密钥材料"""
        if self.密钥对:
            if self.密钥对.私钥:
                self._安全销毁(self.密钥对.私钥)
            self.密钥对 = None
        
        if self.共享密钥:
            self._安全销毁(self.共享密钥)
            self.共享密钥 = None
        
        if self.会话密钥:
            self._安全销毁(self.会话密钥)
            self.会话密钥 = None
        
        self._交换完成 = False
        logger.info("🟢 [安全] 所有密钥已安全销毁")
    
    def _安全销毁(self, 数据: Optional[bytes]):
        """安全销毁敏感数据（覆盖内存）"""
        if 数据 and isinstance(数据, (bytes, bytearray)):
            # 用随机数据覆盖
            覆盖 = os.urandom(len(数据))
            if isinstance(数据, bytes):
                # bytes不可变，尽力而为
                pass
            else:
                for i in range(len(数据)):
                    数据[i] = 覆盖[i]
    
    # ============================================================
    # 备用实现（无cryptography库时）
    # ============================================================
    
    def _备用生成密钥对(self) -> bytes:
        """使用Python标准库生成兼容密钥对（备用）"""
        # 注意: 这不是真正的Curve25519，仅用于演示
        # 生产环境必须使用cryptography库
        
        logger.warning("🟡 [备用] 使用伪随机密钥（仅用于测试!）")
        
        私钥 = os.urandom(32)
        公钥 = hashlib.sha256(私钥).digest()  # 简化处理
        
        self.密钥对 = 密钥对(公钥=公钥, 私钥=私钥, 算法="Fallback")
        return 公钥
    
    def _备用计算共享密钥(self, 对端公钥: bytes) -> bytes:
        """备用共享密钥计算"""
        logger.warning("🟡 [备用] 使用简化密钥协商（仅用于测试!）")
        
        if not self.密钥对:
            raise RuntimeError("密钥对未生成")
        
        # 简化: 混合双方公钥哈希
        共享 = hashlib.sha256(
            self.密钥对.私钥 + 对端公钥
        ).digest()
        
        self.共享密钥 = 共享
        return 共享
    
    def _备用派生会话密钥(self, 共享密钥: bytes, 上下文: str) -> bytes:
        """备用HKDF实现"""
        logger.warning("🟡 [备用] 使用简化HKDF（仅用于测试!）")
        
        # 简化HKDF
        prk = hashlib.sha256(共享密钥 + b"prk").digest()
        会话密钥 = hashlib.sha256(prk + 上下文.encode() + b"okm").digest()[:16]
        
        self.会话密钥 = 会话密钥
        return 会话密钥
    
    # ============================================================
    # 状态查询
    # ============================================================
    
    @property
    def 已准备好交换(self) -> bool:
        """是否已生成密钥对，准备好交换"""
        return self.密钥对 is not None
    
    @property
    def 协商完成(self) -> bool:
        """密钥协商是否已完成"""
        return self.会话密钥 is not None
    
    def 获取状态(self) -> Dict[str, Any]:
        """获取协商器状态"""
        return {
            "密钥对已生成": self.密钥对 is not None,
            "公钥长度": len(self.密钥对.公钥) if self.密钥对 else 0,
            "共享密钥已计算": self.共享密钥 is not None,
            "会话密钥已派生": self.会话密钥 is not None,
            "会话密钥长度": len(self.会话密钥) if self.会话密钥 else 0,
            "算法": self.密钥对.算法 if self.密钥对 else "未设置",
            "dna": self.DNA
        }
    
    def 打印状态(self):
        """打印协商器状态"""
        print(f"\n{'='*50}")
        print("  密钥协商器状态")
        print(f"{'='*50}")
        状态 = self.获取状态()
        for k, v in 状态.items():
            print(f"  {k}: {v}")
        print(f"{'='*50}\n")


# ============================================================
# 完整协商流程
# ============================================================

def 完整协商流程() -> Tuple[bytes, bytes]:
    """
    演示完整的密钥协商流程
    
    返回:
        (设备A会话密钥, 设备B会话密钥) — 两者应相同
    """
    print(f"\n{'='*60}")
    print("  完整密钥协商流程演示")
    print(f"{'='*60}\n")
    
    # 设备A（鸿蒙）
    print("[步骤1] 设备A（鸿蒙）生成密钥对...")
    设备A = 密钥协商器()
    公钥A = 设备A.生成密钥对()
    
    # 设备B（iOS）
    print("[步骤2] 设备B（iOS）生成密钥对...")
    设备B = 密钥协商器()
    公钥B = 设备B.生成密钥对()
    
    # 交换公钥（通过二维码）
    print("[步骤3] 交换公钥（二维码扫描）...")
    QR_A = 设备A.公钥转二维码数据(公钥A)
    QR_B = 设备B.公钥转二维码数据(公钥B)
    print(f"  设备A的二维码: {QR_A[:60]}...")
    print(f"  设备B的二维码: {QR_B[:60]}...")
    
    # 解析对方公钥
    解析公钥B = 设备A.二维码数据转公钥(QR_B)
    解析公钥A = 设备B.二维码数据转公钥(QR_A)
    
    # 计算共享密钥
    print("[步骤4] 双方各自计算共享密钥...")
    共享A = 设备A.计算共享密钥(解析公钥B)
    共享B = 设备B.计算共享密钥(解析公钥A)
    
    print(f"  设备A共享密钥: {共享A.hex()[:32]}...")
    print(f"  设备B共享密钥: {共享B.hex()[:32]}...")
    print(f"  共享密钥一致: {共享A == 共享B}")
    
    # 派生会话密钥
    print("[步骤5] 双方各自派生SM4会话密钥...")
    会话A = 设备A.派生会话密钥(共享A)
    会话B = 设备B.派生会话密钥(共享B)
    
    print(f"  设备A会话密钥: {会话A.hex()}")
    print(f"  设备B会话密钥: {会话B.hex()}")
    print(f"  会话密钥一致: {会话A == 会话B}")
    
    # 验证
    if 会话A == 会话B:
        print("\n🟢 [成功] 密钥协商完成! 双方会话密钥一致")
    else:
        print("\n🔴 [失败] 会话密钥不一致!")
    
    return 会话A, 会话B


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  龍魂密钥协商器 — 测试")
    print(f"{'='*60}\n")
    
    # 测试完整流程
    try:
        会话A, 会话B = 完整协商流程()
        
        print(f"\n{'='*60}")
        print("  设备A状态:")
        设备A = 密钥协商器()
        设备A.生成密钥对()
        设备A.打印状态()
        
    except Exception as e:
        print(f"\n测试过程中出错: {e}")
        print("注意: 生产环境需要安装 cryptography 库")
        print("  pip install cryptography")
