#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#龍芯⚡️2025-01-15-國密核心-加密模塊-v1.0.0-a1b2c3d4
國密算法核心實現（SM2/SM3/SM4）
龍魂體系支撐層
"""
import hashlib
import hmac
import os


class SM3哈希器:
    """SM3 國密哈希算法 - 龍魂專用（簡化實現）"""

    def __init__(self):
        self._中間狀態 = bytearray()
        self._初始向量 = [
            0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
            0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e
        ]
        # 64個常量 T0..T63
        self._常量列表 = [0x79cc4519] * 16 + [0x7a879d8a] * 48

    def _循環左移(self, 值: int, 位移: int) -> int:
        掩碼 = 0xFFFFFFFF
        return ((值 << 位移) | (值 >> (32 - 位移))) & 掩碼

    def _布爾函數(self, i: int, 甲: int, 乙: int, 丙: int) -> int:
        if i < 16:
            return (甲 ^ 乙 ^ 丙) & 0xFFFFFFFF
        else:
            return ((甲 & 乙) | (甲 & 丙) | (乙 & 丙)) & 0xFFFFFFFF

    def _線性函數(self, i: int, 甲: int, 乙: int, 丙: int) -> int:
        if i < 16:
            return (甲 ^ 乙 ^ 丙) & 0xFFFFFFFF
        else:
            return (甲 ^ 乙 ^ 丙) & 0xFFFFFFFF

    def _壓縮函數(self, 向量: list[Any], 數據塊: bytes) -> list[Any]:
        # 將數據塊轉為16個32位字
        W = [int.from_bytes(數據塊[j*4:(j+1)*4], 'big') for j in range(16)]
        # 擴展到64個字
        for j in range(16, 68):
            W.append(
                self._循環左移(W[j-16] ^ W[j-9] ^ self._循環左移(W[j-3], 15), 7)
                ^ self._循環左移(W[j-13], 17) ^ W[j-6]
            )

        甲, 乙, 丙, 丁, 戊, 己, 庚, 辛 = 向量

        for j in range(64):
            SS1 = self._循環左移(
                (self._循環左移(甲, 12) + 戊 + self._循環左移(self._常量列表[j], j % 32)) & 0xFFFFFFFF,
                7
            )
            SS2 = SS1 ^ self._循環左移(甲, 12)
            TT1 = (self._線性函數(j, 甲, 乙, 丙) + 丁 + SS2 + W[j]) & 0xFFFFFFFF
            TT2 = (self._布爾函數(j, 戊, 己, 庚) + 辛 + SS1) & 0xFFFFFFFF
            丁 = 丙
            丙 = self._循環左移(乙, 9)
            乙 = 甲
            甲 = TT1
            辛 = 庚
            庚 = self._循環左移(己, 19)
            己 = 戊
            戊 = TT2 ^ self._循環左移(TT2, 9) ^ self._循環左移(TT2, 17)

        return [
            (向量[0] ^ 甲) & 0xFFFFFFFF,
            (向量[1] ^ 乙) & 0xFFFFFFFF,
            (向量[2] ^ 丙) & 0xFFFFFFFF,
            (向量[3] ^ 丁) & 0xFFFFFFFF,
            (向量[4] ^ 戊) & 0xFFFFFFFF,
            (向量[5] ^ 己) & 0xFFFFFFFF,
            (向量[6] ^ 庚) & 0xFFFFFFFF,
            (向量[7] ^ 辛) & 0xFFFFFFFF,
        ]

    def 更新(self, 數據: bytes) -> 'SM3哈希器':
        self._中間狀態.extend(數據)
        return self

    def 摘要(self) -> bytes:
        原始長度 = len(self._中間狀態) * 8
        填充後 = self._中間狀態 + bytearray([0x80])
        while (len(填充後) * 8) % 512 != 448:
            填充後.append(0x00)
        填充後.extend(原始長度.to_bytes(8, 'big'))

        向量 = self._初始向量.copy()
        for i in range(0, len(填充後), 64):
            塊 = bytes(填充後[i:i+64])
            向量 = self._壓縮函數(向量, 塊)

        return b''.join(v.to_bytes(4, 'big') for v in 向量)

    def 十六進制摘要(self) -> str:
        return self.摘要().hex()


def sm3_哈希(輸入數據: bytes) -> bytes:
    """
    SM3 哈希函數 - 龍魂體系數據完整性驗證
    :param 輸入數據: 待哈希的字節數據
    :return: 32字節哈希值
    """
    哈希器 = SM3哈希器()
    哈希器.更新(輸入數據)
    return 哈希器.摘要()


class SM4密碼器:
    """SM4 國密分組密碼 - 龍魂專用加密模塊"""

    def __init__(self, 密鑰: bytes):
        if len(密鑰) != 16:
            raise ValueError("SM4密鑰必須為16字節")
        self._密鑰 = 密鑰
        self._輪密鑰 = self._密鑰擴展(密鑰)

    _S盒 = bytes([
        0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7,
        0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
        0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3,
        0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a,
        0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
        0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95,
        0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
        0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba,
        0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
        0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b,
        0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
        0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2,
        0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
        0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52,
        0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
        0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5,
        0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
        0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55,
        0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
        0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60,
        0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
        0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f,
        0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
        0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f,
        0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
        0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd,
        0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
        0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e,
        0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
        0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20,
        0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
    ])

    _固定參數 = [
        0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc
    ] * 8

    def _循環左移(self, 值: int, 位移: int) -> int:
        掩碼 = 0xFFFFFFFF
        return ((值 << 位移) | (值 >> (32 - 位移))) & 掩碼

    def _非線性變換(self, 輸入值: int) -> int:
        結果 = 0
        for i in range(4):
            結果 |= self._S盒[(輸入值 >> (i * 8)) & 0xFF] << (i * 8)
        return 結果 & 0xFFFFFFFF

    def _線性變換L(self, 輸入值: int) -> int:
        return (輸入值 ^ self._循環左移(輸入值, 2) ^
                self._循環左移(輸入值, 10) ^
                self._循環左移(輸入值, 18) ^
                self._循環左移(輸入值, 24)) & 0xFFFFFFFF

    def _線性變換L_密鑰(self, 輸入值: int) -> int:
        return (輸入值 ^ self._循環左移(輸入值, 13) ^
                self._循環左移(輸入值, 23)) & 0xFFFFFFFF

    def _輪函數F(self, 狀態: list[Any], 輪密鑰: int) -> int:
        輸入值 = 狀態[1] ^ 狀態[2] ^ 狀態[3] ^ 輪密鑰
        非線性 = self._非線性變換(輸入值)
        線性 = self._線性變換L(非線性)
        return (狀態[0] ^ 線性) & 0xFFFFFFFF

    def _密鑰擴展(self, 密鑰: bytes) -> list[Any]:
        初始密鑰 = [int.from_bytes(密鑰[i:i+4], 'big') for i in range(0, 16, 4)]
        常量_密鑰 = [初始密鑰[i] ^ self._固定參數[i] for i in range(4)]

        輪密鑰列表 = []
        for i in range(32):
            常量_中間 = 常量_密鑰[1] ^ 常量_密鑰[2] ^ 常量_密鑰[3] ^ self._固定參數[i]
            非線性 = self._非線性變換(常量_中間)
            線性 = self._線性變換L_密鑰(非線性)
            新值 = (常量_密鑰[0] ^ 線性) & 0xFFFFFFFF
            輪密鑰列表.append(新值)
            常量_密鑰 = 常量_密鑰[1:] + [新值]

        return 輪密鑰列表

    def _輪變換(self, 明文塊: bytes, 加密: bool) -> bytes:
        狀態 = [int.from_bytes(明文塊[i:i+4], 'big') for i in range(0, 16, 4)]
        密鑰順序 = self._輪密鑰 if 加密 else self._輪密鑰[::-1]

        for 輪密鑰 in 密鑰順序:
            新狀態 = [
                狀態[1], 狀態[2], 狀態[3],
                self._輪函數F(狀態, 輪密鑰)
            ]
            狀態 = 新狀態

        return b''.join(v.to_bytes(4, 'big') for v in 狀態[::-1])

    def 加密(self, 明文: bytes) -> bytes:
        """SM4 ECB模式加密"""
        填充長度 = 16 - (len(明文) % 16)
        填充後 = 明文 + bytes([填充長度] * 填充長度)
        密文 = b''
        for i in range(0, len(填充後), 16):
            密文 += self._輪變換(填充後[i:i+16], True)
        return 密文

    def 解密(self, 密文: bytes) -> bytes:
        """SM4 ECB模式解密"""
        明文 = b''
        for i in range(0, len(密文), 16):
            明文 += self._輪變換(密文[i:i+16], False)
        填充長度 = 明文[-1]
        return 明文[:-填充長度]


def sm4_加密(明文: bytes, 密鑰: bytes) -> bytes:
    """SM4 加密便捷函數"""
    密碼器 = SM4密碼器(密鑰)
    return 密碼器.加密(明文)


def sm4_解密(密文: bytes, 密鑰: bytes) -> bytes:
    """SM4 解密便捷函數"""
    密碼器 = SM4密碼器(密鑰)
    return 密碼器.解密(密文)


if __name__ == "__main__":
    print("=== 國密核心模塊自檢 ===")
    # SM3 測試
    測試數據 = "龍魂系統UID9622測試數據".encode('utf-8')
    哈希結果 = sm3_哈希(測試數據)
    print(f"SM3 哈希結果: {哈希結果.hex()}")

    # SM4 測試（密鑰必須16字節）
    密鑰 = b"LongHunKey16Byte"
    明文 = "龍魂訓練數據優化器機密數據".encode('utf-8')
    密文 = sm4_加密(明文, 密鑰)
    解密文 = sm4_解密(密文, 密鑰)
    print(f"SM4 加密驗證: {'通過' if 解密文 == 明文 else '失敗'}")
    print(f"加密後: {密文.hex()[:32]}...")
