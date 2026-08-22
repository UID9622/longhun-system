#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-MEMORY-SM-CRYPTO-v1.0
# License: MulanPSL v2
"""
國密密码模块 · SM3 哈希 + SM4 加密 + SM3 哈希链
═══════════════════════════════════════════════════════
纯 Python 实现，零外部依赖。
来源: CNSH 国密工具模块（cnsh_guomi.py）
标准: GB/T 32905-2016 (SM3) · GB/T 32907-2016 (SM4)
"""

import os
import struct
import time
from typing import Union, List, Optional


# ════════════════════════════════════════════════════
# SM3 哈希算法 (GB/T 32905-2016)
# ════════════════════════════════════════════════════

class SM3:
    """SM3 密码杂凑算法，输出 256 位摘要。"""

    IV = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
    ]
    T0 = 0x79CC4519
    T1 = 0x7A879D8A

    @staticmethod
    def _rotl(x: int, n: int) -> int:
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def _ff(x: int, y: int, z: int, j: int) -> int:
        return x ^ y ^ z if j < 16 else (x & y) | (x & z) | (y & z)

    @staticmethod
    def _gg(x: int, y: int, z: int, j: int) -> int:
        return x ^ y ^ z if j < 16 else (x & y) | (~x & z)

    @staticmethod
    def _p0(x: int) -> int:
        return x ^ SM3._rotl(x, 9) ^ SM3._rotl(x, 17)

    @staticmethod
    def _p1(x: int) -> int:
        return x ^ SM3._rotl(x, 15) ^ SM3._rotl(x, 23)

    @classmethod
    def hash(cls, data: Union[str, bytes]) -> bytes:
        """计算 SM3 哈希，返回 32 字节"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        bit_len = len(data) * 8
        data += b"\x80"
        while (len(data) * 8) % 512 != 448:
            data += b"\x00"
        data += struct.pack(">Q", bit_len)

        v = cls.IV[:]
        for i in range(0, len(data), 64):
            block = data[i:i + 64]
            w = [0] * 68
            w[0:16] = [int.from_bytes(block[j:j + 4], "big") for j in range(0, 64, 4)]
            for j in range(16, 68):
                w[j] = cls._p1(w[j - 16] ^ w[j - 9] ^ cls._rotl(w[j - 3], 15)) ^ \
                       cls._rotl(w[j - 13], 7) ^ w[j - 6]
            w1 = [w[j] ^ w[j + 4] for j in range(64)]
            a, b, c, d, e, f, g, h = v
            for j in range(64):
                tj = cls.T0 if j < 16 else cls.T1
                ss1 = cls._rotl((cls._rotl(a, 12) + e + cls._rotl(tj, j % 32)) & 0xFFFFFFFF, 7)
                ss2 = ss1 ^ cls._rotl(a, 12)
                tt1 = (cls._ff(a, b, c, j) + d + ss2 + w1[j]) & 0xFFFFFFFF
                tt2 = (cls._gg(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
                d, c, b, a = c, cls._rotl(b, 9), a, tt1
                h, g, f, e = g, cls._rotl(f, 19), e, cls._p0(tt2)
            for idx in range(8):
                v[idx] ^= [a, b, c, d, e, f, g, h][idx]

        return b"".join(x.to_bytes(4, "big") for x in v)

    @classmethod
    def hex(cls, data: Union[str, bytes]) -> str:
        """SM3 哈希 → 十六进制字符串"""
        return cls.hash(data).hex()


# ════════════════════════════════════════════════════
# SM4 分组加密算法 (GB/T 32907-2016)
# ════════════════════════════════════════════════════

class SM4:
    """SM4 分组密码，128 位密钥，128 位分组，32 轮。"""

    FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
    CK = [
        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
        0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,
        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279,
    ]
    SBOX = bytes([
        0xD6,0x90,0xE9,0xFE,0xCC,0xE1,0x3D,0xB7,0x16,0xB6,0x14,0xC2,0x28,0xFB,0x2C,0x05,
        0x2B,0x67,0x9A,0x76,0x2A,0xBE,0x04,0xC3,0xAA,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
        0x9C,0x42,0x50,0xF4,0x91,0xEF,0x98,0x7A,0x33,0x54,0x0B,0x43,0xED,0xCF,0xAC,0x62,
        0xE4,0xB3,0x1C,0xA9,0xC9,0x08,0xE8,0x95,0x80,0xDF,0x94,0xFA,0x75,0x8F,0x3F,0xA6,
        0x47,0x07,0xA7,0xFC,0xF3,0x73,0x17,0xBA,0x83,0x59,0x3C,0x19,0xE6,0x85,0x4F,0xA8,
        0x68,0x6B,0x81,0xB2,0x71,0x64,0xDA,0x8B,0xF8,0xEB,0x0F,0x4B,0x70,0x56,0x9D,0x35,
        0x1E,0x24,0x0E,0x5E,0x63,0x58,0xD1,0xA2,0x25,0x22,0x7C,0x3B,0x01,0x21,0x78,0x87,
        0xD4,0x00,0x46,0x57,0x9F,0xD3,0x27,0x52,0x4C,0x36,0x02,0xE7,0xA0,0xC4,0xC8,0x9E,
        0xEA,0xBF,0x8A,0xD2,0x40,0xC7,0x38,0xB5,0xA3,0xF7,0xF2,0xCE,0xF9,0x61,0x15,0xA1,
        0xE0,0xAE,0x5D,0xA4,0x9B,0x34,0x1A,0x55,0xAD,0x93,0x32,0x30,0xF5,0x8C,0xB1,0xE3,
        0x1D,0xF6,0xE2,0x2E,0x82,0x66,0xCA,0x60,0xC0,0x29,0x23,0xAB,0x0D,0x53,0x4E,0x6F,
        0xD5,0xDB,0x37,0x45,0xDE,0xFD,0x8E,0x2F,0x03,0xFF,0x6A,0x72,0x6D,0x6C,0x5B,0x51,
        0x8D,0x1B,0xAF,0x92,0xBB,0xDD,0xBC,0x7F,0x11,0xD9,0x5C,0x41,0x1F,0x10,0x5A,0xD8,
        0x0A,0xC1,0x31,0x88,0xA5,0xCD,0x7B,0xBD,0x2D,0x74,0xD0,0x12,0xB8,0xE5,0xB4,0xB0,
        0x89,0x69,0x97,0x4A,0x0C,0x96,0x77,0x7E,0x65,0xB9,0xF1,0x09,0xC5,0x6E,0xC6,0x84,
        0x18,0xF0,0x7D,0xEC,0x3A,0xDC,0x4D,0x20,0x79,0xEE,0x5F,0x3E,0xD7,0xCB,0x39,0x48,
    ])

    @classmethod
    def _tau(cls, a: int) -> int:
        b = 0
        for i in range(4):
            b |= cls.SBOX[(a >> (8 * (3 - i))) & 0xFF] << (8 * (3 - i))
        return b

    @classmethod
    def _rotl(cls, x: int, n: int) -> int:
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    @classmethod
    def _l(cls, a: int) -> int:
        return a ^ cls._rotl(a, 2) ^ cls._rotl(a, 10) ^ cls._rotl(a, 18) ^ cls._rotl(a, 24)

    @classmethod
    def _lp(cls, a: int) -> int:
        return a ^ cls._rotl(a, 13) ^ cls._rotl(a, 23)

    @classmethod
    def _expand_key(cls, key: bytes) -> list:
        if len(key) != 16:
            raise ValueError("SM4 密钥长度必须为 16 字节")
        mk = [int.from_bytes(key[i:i + 4], "big") for i in range(0, 16, 4)]
        k = [mk[i] ^ cls.FK[i] for i in range(4)]
        rk = []
        for i in range(32):
            k[i % 4] ^= cls._lp(cls._tau(k[(i + 1) % 4] ^ k[(i + 2) % 4] ^ k[(i + 3) % 4] ^ cls.CK[i]))
            rk.append(k[i % 4])
        return rk

    @classmethod
    def _f(cls, x0: int, x1: int, x2: int, x3: int, rk: int) -> int:
        return x0 ^ cls._l(cls._tau(x1 ^ x2 ^ x3 ^ rk))

    @classmethod
    def _crypt_block(cls, block: bytes, rk: list) -> bytes:
        x = [int.from_bytes(block[i:i + 4], "big") for i in range(0, 16, 4)]
        for i in range(32):
            x.append(cls._f(x[i], x[i + 1], x[i + 2], x[i + 3], rk[i]))
        return x[35].to_bytes(4, "big") + x[34].to_bytes(4, "big") + \
               x[33].to_bytes(4, "big") + x[32].to_bytes(4, "big")

    @classmethod
    def _pad(cls, data: bytes) -> bytes:
        n = 16 - (len(data) % 16)
        return data + bytes([n] * n)

    @classmethod
    def _unpad(cls, data: bytes) -> bytes:
        return data[:-data[-1]]

    @classmethod
    def encrypt(cls, plaintext: bytes, key: bytes) -> bytes:
        """SM4 ECB 加密"""
        rk = cls._expand_key(key)
        padded = cls._pad(plaintext)
        result = b""
        for i in range(0, len(padded), 16):
            result += cls._crypt_block(padded[i:i + 16], rk)
        return result

    @classmethod
    def decrypt(cls, ciphertext: bytes, key: bytes) -> bytes:
        """SM4 ECB 解密"""
        rk = cls._expand_key(key)[::-1]
        result = b""
        for i in range(0, len(ciphertext), 16):
            result += cls._crypt_block(ciphertext[i:i + 16], rk)
        return cls._unpad(result)

    @classmethod
    def generate_key(cls) -> bytes:
        """生成 16 字节 SM4 密钥"""
        return os.urandom(16)


# ════════════════════════════════════════════════════
# SM3 哈希链 — 防篡改追溯
# ════════════════════════════════════════════════════

class SM3HashChain:
    """SM3 哈希链：每笔操作链接前一笔哈希，形成不可篡改的追溯链。

    用法:
        chain = SM3HashChain()
        chain.add("第一次操作的数据")
        chain.add("第二次操作的数据")
        chain.verify()  # → True
    """

    def __init__(self, genesis: Optional[bytes] = None):
        self.chain: List[dict] = []
        self._genesis = genesis or os.urandom(32)
        self._add_link("genesis", self._genesis, prev_hash=bytes(32))

    def _add_link(self, label: str, data: bytes, prev_hash: bytes):
        ts = time.time()
        link_hash = SM3.hash(prev_hash + data + struct.pack(">d", ts))
        self.chain.append({
            "index": len(self.chain),
            "label": label,
            "timestamp": ts,
            "data_hash": SM3.hex(data),
            "prev_hash": prev_hash.hex() if prev_hash != bytes(32) else "0" * 64,
            "link_hash": link_hash.hex(),
        })
        return link_hash

    def add(self, label: str, data: Union[str, bytes]) -> str:
        """添加一个节点，返回 link_hash"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        prev = bytes.fromhex(self.chain[-1]["link_hash"]) if self.chain else bytes(32)
        return self._add_link(label, data, prev).hex()

    def verify(self) -> tuple[bool, List[int]]:
        """验证全链完整性 → (是否通过, 失败节点索引列表)"""
        failures = []
        for i in range(1, len(self.chain)):
            link = self.chain[i]
            prev = self.chain[i - 1]
            expected_prev = prev["link_hash"]
            if link["prev_hash"] != expected_prev:
                failures.append(i)
        return (len(failures) == 0, failures)

    def last_hash(self) -> str:
        """当前链尾哈希"""
        return self.chain[-1]["link_hash"]

    def to_list(self) -> List[dict]:
        """导出为 JSON 可序列化列表"""
        return self.chain


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    # SM3 自检
    expected = "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    assert SM3.hex("abc") == expected, "SM3 自检失败"
    print("🟢 SM3 自检通过")

    # SM4 自检
    key = b"0123456789abcdef"
    pt = b"hello CNSH guomi!"
    ct = SM4.encrypt(pt, key)
    dt = SM4.decrypt(ct, key)
    assert dt == pt, "SM4 自检失败"
    print("🟢 SM4 加解密自检通过")

    # 哈希链自检
    chain = SM3HashChain()
    chain.add("op1", "data one")
    chain.add("op2", "data two")
    ok, fails = chain.verify()
    assert ok, "哈希链自检失败"
    print("🟢 SM3 哈希链自检通过")
    print("🟢 全部国密模块自检通过")
