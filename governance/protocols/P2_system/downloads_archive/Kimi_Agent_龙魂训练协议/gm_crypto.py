#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国密算法核心模块 (SM3/SM4)
实现标准：GB/T 32905-2016 (SM3), GB/T 32907-2016 (SM4)
纯 Python 3 实现，零第三方依赖，仅使用标准库 struct

DNA: #龍芯⚡️2026-06-30-國密核心-v1.0
"""

import struct
from typing import List, Tuple, Optional


# =============================================================================
# SM3 哈希算法 (GB/T 32905-2016)
# =============================================================================

class SM3算法:
    """SM3 密码杂凑算法实现，输出 256 位（32 字节）哈希值"""

    # SM3 初始哈希值（IV）
    初始值 = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
    ]

    @staticmethod
    def 循环左移(值: int, 位数: int) -> int:
        """32 位循环左移运算"""
        位数 = 位数 % 32
        return ((值 << 位数) | (值 >> (32 - 位数))) & 0xFFFFFFFF

    @staticmethod
    def FF_j(索引: int, 变量一: int, 变量二: int, 变量三: int) -> int:
        """布尔函数 FF，根据轮数索引选择不同公式"""
        if 0 <= 索引 <= 15:
            return 变量一 ^ 变量二 ^ 变量三
        else:
            return (变量一 & 变量二) | (变量一 & 变量三) | (变量二 & 变量三)

    @staticmethod
    def GG_j(索引: int, 变量一: int, 变量二: int, 变量三: int) -> int:
        """布尔函数 GG，根据轮数索引选择不同公式"""
        if 0 <= 索引 <= 15:
            return 变量一 ^ 变量二 ^ 变量三
        else:
            # Python 的 ~ 产生无限精度负数，但 (& 变量三) 会自然限制为 32 位
            return (变量一 & 变量二) | ((~变量一) & 变量三)

    @staticmethod
    def P0(输入值: int) -> int:
        """置换函数 P0"""
        return 输入值 ^ SM3算法.循环左移(输入值, 9) ^ SM3算法.循环左移(输入值, 17)

    @staticmethod
    def P1(输入值: int) -> int:
        """置换函数 P1"""
        return 输入值 ^ SM3算法.循环左移(输入值, 15) ^ SM3算法.循环左移(输入值, 23)

    @staticmethod
    def T_j(索引: int) -> int:
        """常量生成函数 T"""
        if 0 <= 索引 <= 15:
            return 0x79CC4519
        else:
            return 0x7A879D8A

    @classmethod
    def 消息填充(cls, 消息: bytes) -> bytes:
        """对消息进行填充，使其长度满足 512 位的整数倍"""
        消息长度 = len(消息) * 8  # 消息长度（位）

        # 步骤 1：附加一个 '1' 位（0x80 字节）
        填充消息 = 消息 + b'\x80'

        # 步骤 2：附加 k 个 '0' 位，使得 (消息长度 + 1 + k) ≡ 448 (mod 512)
        # 即填充后的长度（位）满足：长度 ≡ 448 (mod 512)
        # 当前长度（位）= 消息长度 + 8（0x80 的 8 位）
        当前位长度 = 消息长度 + 8
        # 需要填充的 0 的位数
        零位数量 = (448 - (当前位长度 % 512)) % 512
        零字节数量 = 零位数量 // 8
        填充消息 += b'\x00' * 零字节数量

        # 步骤 3：附加 64 位消息长度（大端序）
        长度字节 = struct.pack('>Q', 消息长度)
        填充消息 += 长度字节

        return 填充消息

    @classmethod
    def 消息扩展(cls, 消息块: bytes) -> Tuple[List[int], List[int]]:
        """将 64 字节（512 位）消息块扩展为字数组 W 和 W1"""
        # 将消息块拆分为 16 个 32 位字（大端序）
        W = list(struct.unpack('>16I', 消息块))

        # 扩展生成 W[16..67]
        for j in range(16, 68):
            新字 = cls.P1(W[j - 16] ^ W[j - 9] ^ cls.循环左移(W[j - 3], 15))
            新字 ^= cls.循环左移(W[j - 13], 7) ^ W[j - 6]
            W.append(新字 & 0xFFFFFFFF)

        # 生成 W1[0..63]
        W1 = []
        for j in range(64):
            W1.append((W[j] ^ W[j + 4]) & 0xFFFFFFFF)

        return W, W1

    @classmethod
    def 压缩函数(cls, 哈希状态: List[int], 消息块: bytes) -> List[int]:
        """CF 压缩函数：处理 512 位消息块，更新哈希状态"""
        # 复制当前哈希状态到工作寄存器
        A, B, C, D, E, F, G, H = 哈希状态

        # 消息扩展
        W, W1 = cls.消息扩展(消息块)

        # 64 轮迭代
        for j in range(64):
            T = cls.T_j(j)
            SS1 = cls.循环左移(
                (cls.循环左移(A, 12) + E + cls.循环左移(T, j % 32)) & 0xFFFFFFFF, 7
            )
            SS2 = SS1 ^ cls.循环左移(A, 12)
            TT1 = (cls.FF_j(j, A, B, C) + D + SS2 + W1[j]) & 0xFFFFFFFF
            TT2 = (cls.GG_j(j, E, F, G) + H + SS1 + W[j]) & 0xFFFFFFFF
            D = C
            C = cls.循环左移(B, 9)
            B = A
            A = TT1
            H = G
            G = cls.循环左移(F, 19)
            F = E
            E = cls.P0(TT2)

        # 输出与输入的异或（ Davies-Meyer 结构）
        新状态 = [
            (A ^ 哈希状态[0]) & 0xFFFFFFFF,
            (B ^ 哈希状态[1]) & 0xFFFFFFFF,
            (C ^ 哈希状态[2]) & 0xFFFFFFFF,
            (D ^ 哈希状态[3]) & 0xFFFFFFFF,
            (E ^ 哈希状态[4]) & 0xFFFFFFFF,
            (F ^ 哈希状态[5]) & 0xFFFFFFFF,
            (G ^ 哈希状态[6]) & 0xFFFFFFFF,
            (H ^ 哈希状态[7]) & 0xFFFFFFFF,
        ]

        return 新状态

    @classmethod
    def 计算哈希(cls, 数据: bytes) -> bytes:
        """
        计算 SM3 哈希值

        参数：
            数据: 输入字节数据
        返回：
            32 字节（256 位）哈希值
        """
        # 消息填充
        填充数据 = cls.消息填充(数据)

        # 初始化哈希状态
        哈希状态 = list(cls.初始值)

        # 逐块处理（每块 64 字节 = 512 位）
        for i in range(0, len(填充数据), 64):
            消息块 = 填充数据[i:i + 64]
            哈希状态 = cls.压缩函数(哈希状态, 消息块)

        # 将 8 个 32 位字打包为 32 字节输出（大端序）
        return struct.pack('>8I', *哈希状态)


def sm3_哈希(数据: bytes) -> bytes:
    """
    SM3 哈希函数便捷接口

    参数：
        数据: 输入字节数据
    返回：
        32 字节（256 位）哈希值

    示例：
        >>> 结果 = sm3_哈希(b"abc")
        >>> len(结果)
        32
    """
    return SM3算法.计算哈希(数据)


# =============================================================================
# SM4 分组加密算法 (GB/T 32907-2016)
# =============================================================================

class SM4算法:
    """SM4 分组密码算法实现，分组大小 128 位，密钥长度 128 位"""

    # SM4 S 盒（256 字节）
    S盒 = bytes([
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
        0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
        0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
        0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
        0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
        0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
        0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
        0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
        0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
        0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48,
    ])

    # 密钥扩展算法 FK 常量
    FK常量 = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]

    # 密钥扩展算法 CK 常量（32 个）
    CK常量 = [
        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
        0xC0C7CED5, 0xDCE3EAf1, 0xF8FF060D, 0x141B2229,
        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279,
    ]

    @classmethod
    def S盒替换(cls, 输入字: int) -> int:
        """对 32 位字进行 S 盒替换"""
        结果 = 0
        for i in range(4):
            字节值 = (输入字 >> (24 - i * 8)) & 0xFF
            替换值 = cls.S盒[字节值]
            结果 = (结果 << 8) | 替换值
        return 结果

    @classmethod
    def 线性变换_L(cls, 输入值: int) -> int:
        """加密时的线性变换 L"""
        return (
            输入值
            ^ cls._循环左移32(输入值, 2)
            ^ cls._循环左移32(输入值, 10)
            ^ cls._循环左移32(输入值, 18)
            ^ cls._循环左移32(输入值, 24)
        ) & 0xFFFFFFFF

    @classmethod
    def 线性变换_L1(cls, 输入值: int) -> int:
        """密钥扩展时的线性变换 L'"""
        return (
            输入值
            ^ cls._循环左移32(输入值, 13)
            ^ cls._循环左移32(输入值, 23)
        ) & 0xFFFFFFFF

    @classmethod
    def _循环左移32(cls, 值: int, 位数: int) -> int:
        """32 位循环左移"""
        位数 = 位数 % 32
        return ((值 << 位数) | (值 >> (32 - 位数))) & 0xFFFFFFFF

    @classmethod
    def 轮函数F(cls, 输入元组: Tuple[int, int, int, int], 轮密钥: int) -> int:
        """轮函数 F：τ(X1 ⊕ X2 ⊕ X3 ⊕ rk) 后接线性变换 L，再与 X0 异或"""
        X0, X1, X2, X3 = 输入元组
        # 轮密钥应与 X1⊕X2⊕X3 一起进入 S 盒替换（非线性变换 τ）
        中间值 = X1 ^ X2 ^ X3 ^ 轮密钥
        替换结果 = cls.S盒替换(中间值)
        线性结果 = cls.线性变换_L(替换结果)
        return X0 ^ 线性结果

    @classmethod
    def 密钥扩展(cls, 密钥: bytes) -> List[int]:
        """密钥扩展算法：从 128 位密钥生成 32 个轮密钥"""
        # 将密钥拆分为 4 个 32 位字
        K = list(struct.unpack('>4I', 密钥))

        # 与 FK 常量异或
        for i in range(4):
            K[i] ^= cls.FK常量[i]

        # 生成 32 个轮密钥
        轮密钥列表 = []
        for i in range(32):
            K_i4 = K[i + 1] ^ K[i + 2] ^ K[i + 3]
            替换结果 = cls.S盒替换(K_i4 ^ cls.CK常量[i])
            K_new = (K[i] ^ cls.线性变换_L1(替换结果)) & 0xFFFFFFFF
            K.append(K_new)
            轮密钥列表.append(K_new)

        return 轮密钥列表

    @classmethod
    def 单分组加密(cls, 明文块: bytes, 轮密钥列表: List[int]) -> bytes:
        """加密单个 128 位分组"""
        # 将明文拆分为 4 个 32 位字（大端序）
        X = list(struct.unpack('>4I', 明文块))

        # 32 轮迭代
        for i in range(32):
            X_new = cls.轮函数F((X[0], X[1], X[2], X[3]), 轮密钥列表[i])
            X = [X[1], X[2], X[3], X_new]

        # 反序变换：输出 X[3], X[2], X[1], X[0]
        密文 = struct.pack('>4I', X[3], X[2], X[1], X[0])
        return 密文

    @classmethod
    def 单分组解密(cls, 密文块: bytes, 轮密钥列表: List[int]) -> bytes:
        """解密单个 128 位分组（使用逆序的轮密钥）"""
        逆序轮密钥 = list(reversed(轮密钥列表))
        return cls.单分组加密(密文块, 逆序轮密钥)


class SM4工作模式:
    """SM4 工作模式：ECB 和 CBC"""

    @classmethod
    def PKCS7填充(cls, 数据: bytes, 块大小: int = 16) -> bytes:
        """PKCS#7 填充"""
        填充长度 = 块大小 - (len(数据) % 块大小)
        return 数据 + bytes([填充长度] * 填充长度)

    @classmethod
    def PKCS7去填充(cls, 数据: bytes) -> bytes:
        """PKCS#7 去填充"""
        填充长度 = 数据[-1]
        if 填充长度 > len(数据) or 填充长度 == 0:
            raise ValueError("无效的填充")
        return 数据[:-填充长度]

    @classmethod
    def ECB_加密(cls, 明文: bytes, 轮密钥列表: List[int]) -> bytes:
        """ECB 模式加密"""
        填充明文 = cls.PKCS7填充(明文)
        密文 = b''
        for i in range(0, len(填充明文), 16):
            块 = 填充明文[i:i + 16]
            密文 += SM4算法.单分组加密(块, 轮密钥列表)
        return 密文

    @classmethod
    def ECB_解密(cls, 密文: bytes, 轮密钥列表: List[int]) -> bytes:
        """ECB 模式解密"""
        if len(密文) % 16 != 0:
            raise ValueError("密文长度必须是 16 的整数倍")
        明文 = b''
        for i in range(0, len(密文), 16):
            块 = 密文[i:i + 16]
            明文 += SM4算法.单分组解密(块, 轮密钥列表)
        return cls.PKCS7去填充(明文)

    @classmethod
    def CBC_加密(cls, 明文: bytes, 轮密钥列表: List[int], 初始向量: bytes) -> bytes:
        """CBC 模式加密"""
        填充明文 = cls.PKCS7填充(明文)
        密文 = b''
        前一块密文 = 初始向量
        for i in range(0, len(填充明文), 16):
            块 = 填充明文[i:i + 16]
            # 与前一块密文（或 IV）异或
            异或块 = cls._块异或(块, 前一块密文)
            加密块 = SM4算法.单分组加密(异或块, 轮密钥列表)
            密文 += 加密块
            前一块密文 = 加密块
        return 密文

    @classmethod
    def CBC_解密(cls, 密文: bytes, 轮密钥列表: List[int], 初始向量: bytes) -> bytes:
        """CBC 模式解密"""
        if len(密文) % 16 != 0:
            raise ValueError("密文长度必须是 16 的整数倍")
        明文 = b''
        前一块密文 = 初始向量
        for i in range(0, len(密文), 16):
            块 = 密文[i:i + 16]
            解密块 = SM4算法.单分组解密(块, 轮密钥列表)
            # 与前一块密文（或 IV）异或
            异或块 = cls._块异或(解密块, 前一块密文)
            明文 += 异或块
            前一块密文 = 块
        return cls.PKCS7去填充(明文)

    @staticmethod
    def _块异或(块一: bytes, 块二: bytes) -> bytes:
        """两个字节块按位异或"""
        return bytes(a ^ b for a, b in zip(块一, 块二))


def sm4_加密(明文: bytes, 密鑰: bytes, 模式: str = "ECB", 初始向量: Optional[bytes] = None) -> bytes:
    """
    SM4 加密便捷接口

    参数：
        明文: 输入明文数据
        密鑰: 16 字节（128 位）密钥
        模式: "ECB" 或 "CBC"
        初始向量: CBC 模式需要 16 字节 IV（ECB 模式下可忽略）

    返回：
        密文字节数据

    示例：
        >>> 密鑰 = b'0123456789abcdef'
        >>> 明文 = b'Hello, SM4!'
        >>> 密文 = sm4_加密(明文, 密鑰, "CBC", b'1234567890abcdef')
    """
    if len(密鑰) != 16:
        raise ValueError("密钥必须是 16 字节（128 位）")

    轮密钥列表 = SM4算法.密钥扩展(密鑰)

    模式 = 模式.upper()
    if 模式 == "ECB":
        return SM4工作模式.ECB_加密(明文, 轮密钥列表)
    elif 模式 == "CBC":
        if 初始向量 is None or len(初始向量) != 16:
            raise ValueError("CBC 模式需要提供 16 字节的初始向量")
        return SM4工作模式.CBC_加密(明文, 轮密钥列表, 初始向量)
    else:
        raise ValueError(f"不支持的工作模式: {模式}")


def sm4_解密(密文: bytes, 密鑰: bytes, 模式: str = "ECB", 初始向量: Optional[bytes] = None) -> bytes:
    """
    SM4 解密便捷接口

    参数：
        密文: 输入密文数据（长度必须是 16 的整数倍）
        密鑰: 16 字节（128 位）密钥
        模式: "ECB" 或 "CBC"
        初始向量: CBC 模式需要 16 字节 IV（ECB 模式下可忽略）

    返回：
        明文字节数据

    示例：
        >>> 密鑰 = b'0123456789abcdef'
        >>> 密文 = sm4_加密(b'Hello, SM4!', 密鑰, "ECB")
        >>> 明文 = sm4_解密(密文, 密鑰, "ECB")
    """
    if len(密鑰) != 16:
        raise ValueError("密钥必须是 16 字节（128 位）")

    轮密钥列表 = SM4算法.密钥扩展(密鑰)

    模式 = 模式.upper()
    if 模式 == "ECB":
        return SM4工作模式.ECB_解密(密文, 轮密钥列表)
    elif 模式 == "CBC":
        if 初始向量 is None or len(初始向量) != 16:
            raise ValueError("CBC 模式需要提供 16 字节的初始向量")
        return SM4工作模式.CBC_解密(密文, 轮密钥列表, 初始向量)
    else:
        raise ValueError(f"不支持的工作模式: {模式}")


# =============================================================================
# 验证测试
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("国密算法 (SM3/SM4) 验证测试")
    print("=" * 60)

    # ---- SM3 测试 ----
    print("\n[SM3 哈希算法测试]")

    # 测试向量 1：空消息
    空哈希 = sm3_哈希(b"")
    print(f"SM3(\"\") = {空哈希.hex()}")
    assert 空哈希.hex().lower() == (
        "1ab21d8355cfa17f8e61194831e81a8f22bec8c728fefb747ed035eb5082aa2b"
    ), "SM3 空消息测试失败"
    print("  ✓ 空消息测试通过")

    # 测试向量 2："abc"
    abc哈希 = sm3_哈希(b"abc")
    print(f'SM3("abc") = {abc哈希.hex()}')
    assert abc哈希.hex().lower() == (
        "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    ), "SM3 'abc' 测试失败"
    print("  ✓ 'abc' 测试通过")

    # 测试向量 3：长消息 "abcd" * 16
    长消息 = b"abcd" * 16
    长哈希 = sm3_哈希(长消息)
    print(f'SM3("abcd" * 16) = {长哈希.hex()}')
    assert 长哈希.hex().lower() == (
        "debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732"
    ), "SM3 长消息测试失败"
    print("  ✓ 长消息测试通过")

    # ---- SM4 测试 ----
    print("\n[SM4 分组加密测试]")

    # 标准测试向量
    测试密钥 = bytes([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
                      0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
    测试明文 = bytes([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
                      0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
    标准密文 = bytes([0x68, 0x1E, 0xDF, 0x34, 0xD2, 0x06, 0x96, 0x5E,
                      0x86, 0xB3, 0xE9, 0x4F, 0x53, 0x6E, 0x42, 0x46])

    # ECB 模式单分组测试
    轮密钥 = SM4算法.密钥扩展(测试密钥)
    加密结果 = SM4算法.单分组加密(测试明文, 轮密钥)
    print(f"SM4 ECB 单分组加密: {加密结果.hex()}")
    assert 加密结果 == 标准密文, "SM4 ECB 单分组加密测试失败"
    print("  ✓ ECB 单分组加密测试通过")

    解密结果 = SM4算法.单分组解密(标准密文, 轮密钥)
    assert 解密结果 == 测试明文, "SM4 ECB 单分组解密测试失败"
    print("  ✓ ECB 单分组解密测试通过")

    # ECB 模式多分组测试
    多分组明文 = b"Hello, this is a test message for SM4 encryption!"
    ecb密文 = sm4_加密(多分组明文, 测试密钥, "ECB")
    ecb解密 = sm4_解密(ecb密文, 测试密钥, "ECB")
    assert ecb解密 == 多分组明文, "SM4 ECB 多分组测试失败"
    print("  ✓ ECB 模式多分组加解密测试通过")

    # CBC 模式测试
    测试IV = b"1234567890abcdef"
    cbc密文 = sm4_加密(多分组明文, 测试密钥, "CBC", 测试IV)
    cbc解密 = sm4_解密(cbc密文, 测试密钥, "CBC", 测试IV)
    assert cbc解密 == 多分组明文, "SM4 CBC 模式测试失败"
    print("  ✓ CBC 模式加解密测试通过")

    # 中文字符测试
    中文数据 = "国密算法 SM3/SM4 测试".encode('utf-8')
    中文ecb密文 = sm4_加密(中文数据, 测试密钥, "ECB")
    中文ecb解密 = sm4_解密(中文ecb密文, 测试密钥, "ECB")
    assert 中文ecb解密 == 中文数据, "SM4 中文数据 ECB 测试失败"
    print("  ✓ 中文数据 ECB 加解密测试通过")

    中文cbc密文 = sm4_加密(中文数据, 测试密钥, "CBC", 测试IV)
    中文cbc解密 = sm4_解密(中文cbc密文, 测试密钥, "CBC", 测试IV)
    assert 中文cbc解密 == 中文数据, "SM4 中文数据 CBC 测试失败"
    print("  ✓ 中文数据 CBC 加解密测试通过")

    # ---- 性能测试 ----
    print("\n[性能测试]")
    import time

    # SM3 性能
    大数据 = b"A" * (1024 * 1024)  # 1 MB
    开始时间 = time.time()
    sm3_哈希(大数据)
    sm3耗时 = time.time() - 开始时间
    print(f"SM3 哈希 1MB 数据耗时: {sm3耗时:.4f} 秒")

    # SM4 性能
    大明文 = b"B" * (1024 * 1024)  # 1 MB
    开始时间 = time.time()
    大密文 = sm4_加密(大明文, 测试密钥, "ECB")
    sm4加密耗时 = time.time() - 开始时间
    开始时间 = time.time()
    sm4_解密(大密文, 测试密钥, "ECB")
    sm4解密耗时 = time.time() - 开始时间
    print(f"SM4 ECB 加密 1MB 数据耗时: {sm4加密耗时:.4f} 秒")
    print(f"SM4 ECB 解密 1MB 数据耗时: {sm4解密耗时:.4f} 秒")

    print("\n" + "=" * 60)
    print("所有测试通过！✓")
    print("=" * 60)
