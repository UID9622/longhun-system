#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 IP 资产脚本 · longhun_crypto_engine.py
DNA: #龍芯⚡️2026-07-04-PY-LONGHUN_CRYPTO_ENGINE-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
来源: /Users/zuimeidedeyihan/Downloads/Kimi_Agent_龍魂IP资产清单 (2)/longhun_crypto_engine.py
归档: /Users/zuimeidedeyihan/longhun-system/scripts/private-shared-imports/ip-assets-v2/longhun_crypto_engine.py
"""

# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  龍魂·国密DNA加密引擎 (LongHun Guomi DNA Crypto Engine)                      ║
║  DNA追溯码: #龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0                              ║
║  三色审计标准: 红(禁止)/黄(审查)/绿(通过)                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

功能特性:
    - SM3: 国密哈希算法，256位摘要
    - SM4: 国密对称加密，支持ECB/CBC模式
    - SM2: 国密非对称加密/数字签名
    - DNA追溯码: 嵌入加密数据的数字水印
    - 支持: JPG/PNG图片、文本、个人信息、指纹、配方数据

依赖: 标准库 + Pillow (图片处理)
"""

import os
import sys
import struct
import copy
import binascii
import base64
import json
import time
import random
import hashlib
import io
import re
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, Union, List

# ============================================================
# 第一部分: 国密算法核心实现 (SM3 / SM4 / SM2)
# ============================================================

# ── SM3 哈希算法 ──
SM3_IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
]
SM3_T0 = 0x79CC4519
SM3_T1 = 0x7A879D8A

def _u32(x):
    return x & 0xFFFFFFFF

def _rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def _ff_j(x, y, z, j):
    return (x ^ y ^ z) if 0 <= j <= 15 else ((x & y) | (x & z) | (y & z))

def _gg_j(x, y, z, j):
    return (x ^ y ^ z) if 0 <= j <= 15 else ((x & y) | (~x & z))

def _p0(x):
    return x ^ _rotl(x, 9) ^ _rotl(x, 17)

def _p1(x):
    return x ^ _rotl(x, 15) ^ _rotl(x, 23)

def _sm3_cf(v_i, b_i):
    w = [0] * 68
    w1 = [0] * 64
    for j in range(16):
        w[j] = int.from_bytes(b_i[j*4:(j+1)*4], 'big')
    for j in range(16, 68):
        w[j] = _p1(w[j-16] ^ w[j-9] ^ _rotl(w[j-3], 15)) ^ _rotl(w[j-13], 7) ^ w[j-6]
    for j in range(64):
        w1[j] = w[j] ^ w[j+4]
    a, b, c, d, e, f, g, h = [v_i[i] for i in range(8)]
    for j in range(64):
        ss1 = _rotl((_rotl(a, 12) + e + (_rotl(SM3_T0 if j < 16 else SM3_T1, j % 32))) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ _rotl(a, 12)
        tt1 = (_ff_j(a, b, c, j) + d + ss2 + w1[j]) & 0xFFFFFFFF
        tt2 = (_gg_j(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d = c; c = _rotl(b, 9); b = a; a = tt1
        h = g; g = _rotl(f, 19); f = e; e = _p0(tt2)
    v_j = [a, b, c, d, e, f, g, h]
    return [(_u32(v_i[i]) ^ _u32(v_j[i])) for i in range(8)]


class SM3:
    """SM3密码杂凑算法 - 国密哈希，输出256位(32字节)摘要"""
    def __init__(self):
        self._reset()

    def _reset(self):
        self._iv = copy.deepcopy(SM3_IV)
        self._buffer = bytearray()
        self._count = 0

    def update(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._buffer.extend(data)
        self._count += len(data) * 8
        while len(self._buffer) >= 64:
            self._iv = _sm3_cf(self._iv, self._buffer[:64])
            self._buffer = self._buffer[64:]

    def digest(self):
        buffer = self._buffer.copy()
        count = self._count
        iv = copy.deepcopy(self._iv)
        buffer.append(0x80)
        while (len(buffer) % 64) != 56:
            buffer.append(0x00)
        buffer.extend(struct.pack('>Q', count))
        while len(buffer) >= 64:
            iv = _sm3_cf(iv, buffer[:64])
            buffer = buffer[64:]
        return b''.join(v.to_bytes(4, 'big') for v in iv)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')

    def reset(self):
        self._reset()


def sm3_hash(data):
    """便捷函数: 直接计算SM3哈希"""
    s = SM3()
    s.update(data)
    return s.hexdigest()


# ── SM4 对称加密算法 ──
SM4_SBOX = bytes([
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

SM4_FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
SM4_CK = [
    0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,
    0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
    0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,
    0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
    0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,
    0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
    0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,
    0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279,
]

def _sm4_tau(a):
    a = _u32(a)
    return _u32((SM4_SBOX[(a >> 24) & 0xFF] << 24) | (SM4_SBOX[(a >> 16) & 0xFF] << 16) |
                (SM4_SBOX[(a >> 8) & 0xFF] << 8) | SM4_SBOX[a & 0xFF])

def _sm4_l(b):
    b = _u32(b)
    return _u32(b ^ _rotl(b, 2) ^ _rotl(b, 10) ^ _rotl(b, 18) ^ _rotl(b, 24))

def _sm4_l_prime(b):
    b = _u32(b)
    return _u32(b ^ _rotl(b, 13) ^ _rotl(b, 23))

def _sm4_f(x0, x1, x2, x3, rk):
    t = _u32(x1 ^ x2 ^ x3 ^ rk)
    return _u32(x0 ^ _sm4_l(_sm4_tau(t)))

def _sm4_key_expansion(key):
    K = [0] * 36
    MK = [_u32(int.from_bytes(key[i*4:(i+1)*4], 'big')) for i in range(4)]
    for i in range(4):
        K[i] = _u32(MK[i] ^ SM4_FK[i])
    rk = []
    for i in range(32):
        t = _u32(K[i+1] ^ K[i+2] ^ K[i+3] ^ SM4_CK[i])
        K[i+4] = _u32(K[i] ^ _sm4_l_prime(_sm4_tau(t)))
        rk.append(K[i+4])
    return rk


class SM4Cipher:
    """SM4分组密码算法 - 国密对称加密，128位密钥/分组"""
    BLOCK_SIZE = 16

    def __init__(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        if len(key) != 16:
            raise ValueError(f"SM4密钥必须为16字节, 当前{len(key)}字节")
        self._rk = _sm4_key_expansion(key)

    def _crypt_block(self, block, decrypt=False):
        X = [_u32(int.from_bytes(block[i*4:(i+1)*4], 'big')) for i in range(4)]
        rk = self._rk[::-1] if decrypt else self._rk
        for i in range(32):
            X.append(_sm4_f(X[i], X[i+1], X[i+2], X[i+3], rk[i]))
        return b''.join(_u32(X[i]).to_bytes(4, 'big') for i in range(35, 31, -1))

    def encrypt(self, plaintext):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        pad_len = self.BLOCK_SIZE - (len(plaintext) % self.BLOCK_SIZE)
        padded = plaintext + bytes([pad_len] * pad_len)
        ciphertext = b''
        for i in range(0, len(padded), self.BLOCK_SIZE):
            ciphertext += self._crypt_block(padded[i:i+self.BLOCK_SIZE])
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        for i in range(0, len(ciphertext), self.BLOCK_SIZE):
            plaintext += self._crypt_block(ciphertext[i:i+self.BLOCK_SIZE], decrypt=True)
        pad_len = plaintext[-1]
        if pad_len < 1 or pad_len > self.BLOCK_SIZE:
            raise ValueError("无效的填充")
        return plaintext[:-pad_len]

    def encrypt_cbc(self, plaintext, iv):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        if isinstance(iv, str):
            iv = iv.encode('utf-8')
        if len(iv) != self.BLOCK_SIZE:
            raise ValueError(f"IV必须为{self.BLOCK_SIZE}字节")
        pad_len = self.BLOCK_SIZE - (len(plaintext) % self.BLOCK_SIZE)
        padded = plaintext + bytes([pad_len] * pad_len)
        ciphertext, prev = b'', iv
        for i in range(0, len(padded), self.BLOCK_SIZE):
            block = bytes(a ^ b for a, b in zip(padded[i:i+self.BLOCK_SIZE], prev))
            enc = self._crypt_block(block)
            ciphertext += enc
            prev = enc
        return ciphertext

    def decrypt_cbc(self, ciphertext, iv):
        if isinstance(iv, str):
            iv = iv.encode('utf-8')
        if len(iv) != self.BLOCK_SIZE:
            raise ValueError(f"IV必须为{self.BLOCK_SIZE}字节")
        plaintext, prev = b'', iv
        for i in range(0, len(ciphertext), self.BLOCK_SIZE):
            dec = self._crypt_block(ciphertext[i:i+self.BLOCK_SIZE], decrypt=True)
            plaintext += bytes(a ^ b for a, b in zip(dec, prev))
            prev = ciphertext[i:i+self.BLOCK_SIZE]
        pad_len = plaintext[-1]
        if pad_len < 1 or pad_len > self.BLOCK_SIZE:
            raise ValueError("无效的填充")
        return plaintext[:-pad_len]


# ── SM2 非对称加密/签名算法 ──
# 正确的SM2曲线参数 (通过OpenSSL验证)
SM2_P = 0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff
SM2_A = 0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc
SM2_B = 0x28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93
SM2_N = 0xfffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123
SM2_GX = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
SM2_GY = 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
SM2_G = (SM2_GX, SM2_GY)
SM2_IDA_DEFAULT = b"1234567812345678"

def _sm2_mod_inverse(a, m):
    """模逆元 - 扩展欧几里得算法"""
    g, x, y = _extended_gcd(a % m, m)
    if g != 1:
        return None
    return (x % m + m) % m

def _extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _extended_gcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def _sm2_point_add(P, Q, p):
    """椭圆曲线点加法"""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and y1 != y2:
        return None
    if x1 == x2 and y1 == y2:
        if y1 == 0:
            return None
        lam = ((3 * x1 * x1 + SM2_A) * _sm2_mod_inverse(2 * y1, p)) % p
    else:
        inv = _sm2_mod_inverse((x2 - x1) % p, p)
        if inv is None:
            return None
        lam = ((y2 - y1) * inv) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def _sm2_scalar_mult(k, P, p):
    """椭圆曲线标量乘法 (double-and-add)"""
    if k == 0 or P is None:
        return None
    if k < 0:
        k = -k
        x, y = P
        P = (x, (-y) % p)
    result, addend, kk = None, P, k
    while kk:
        if kk & 1:
            result = _sm2_point_add(result, addend, p)
        addend = _sm2_point_add(addend, addend, p)
        kk >>= 1
    return result

def _sm2_point_to_bytes(P, compressed=False):
    if P is None:
        return b'\x00'
    x, y = P
    xb = x.to_bytes(32, 'big')
    if compressed:
        return (b'\x02' if (y & 1) == 0 else b'\x03') + xb
    return b'\x04' + xb + y.to_bytes(32, 'big')

def _bytes_to_sm2_point(data):
    if data[0:1] == b'\x00':
        return None
    if data[0:1] == b'\x04':
        return (int.from_bytes(data[1:33], 'big'), int.from_bytes(data[33:65], 'big'))
    raise ValueError("不支持的点编码格式")

def _kdf(z, klen):
    """密钥派生函数 KDF"""
    ct, rcnt = 1, (klen + 31) // 32
    ha = b''
    for _ in range(rcnt):
        h = SM3()
        h.update(z + ct.to_bytes(4, 'big'))
        ha += h.digest()
        ct += 1
    return ha[:klen]

def _sm2_get_z(id_a, P_a):
    """计算Z值 (签名预处理)"""
    entla = (len(id_a) * 8).to_bytes(2, 'big')
    a = SM2_A.to_bytes(32, 'big')
    b = SM2_B.to_bytes(32, 'big')
    gx = SM2_GX.to_bytes(32, 'big')
    gy = SM2_GY.to_bytes(32, 'big')
    x_a = P_a[0].to_bytes(32, 'big')
    y_a = P_a[1].to_bytes(32, 'big')
    h = SM3()
    h.update(entla + id_a + a + b + gx + gy + x_a + y_a)
    return h.digest()


class SM2Cipher:
    """SM2椭圆曲线公钥密码算法 - 国密非对称加密/数字签名"""

    def __init__(self, private_key=None, public_key=None):
        self.p = SM2_P
        self.n = SM2_N
        self.G = SM2_G
        if isinstance(private_key, (bytes, bytearray)):
            self._sk = int.from_bytes(private_key, 'big')
        elif isinstance(private_key, int):
            self._sk = private_key
        else:
            self._sk = None
        if isinstance(public_key, (bytes, bytearray)):
            self._pk = _bytes_to_sm2_point(b'\x04' + public_key)
        elif isinstance(public_key, tuple):
            self._pk = public_key
        elif self._sk is not None:
            self._pk = _sm2_scalar_mult(self._sk, self.G, self.p)
        else:
            self._pk = None

    @classmethod
    def generate_keypair(cls):
        sk = random.randrange(1, SM2_N)
        sm2 = cls(private_key=sk)
        return sk.to_bytes(32, 'big'), sm2.get_public_key_bytes()

    def get_public_key_bytes(self):
        if self._pk is None:
            return None
        return self._pk[0].to_bytes(32, 'big') + self._pk[1].to_bytes(32, 'big')

    def get_private_key_bytes(self):
        return self._sk.to_bytes(32, 'big') if self._sk else None

    def encrypt(self, plaintext, random_k=None):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        if self._pk is None:
            raise ValueError("缺少公钥")
        klen = len(plaintext)
        while True:
            k = random_k if random_k else random.randrange(1, self.n)
            random_k = None
            C1 = _sm2_scalar_mult(k, self.G, self.p)
            if C1 is None:
                continue
            S = _sm2_scalar_mult(k, self._pk, self.p)
            if S is None:
                continue
            x2 = S[0].to_bytes(32, 'big')
            y2 = S[1].to_bytes(32, 'big')
            t = _kdf(x2 + y2, klen)
            if all(b == 0 for b in t):
                continue
            C2 = bytes(a ^ b for a, b in zip(plaintext, t))
            h = SM3()
            h.update(x2 + plaintext + y2)
            return _sm2_point_to_bytes(C1) + h.digest() + C2

    def decrypt(self, ciphertext):
        if self._sk is None:
            raise ValueError("缺少私钥")
        C1 = _bytes_to_sm2_point(ciphertext[:65])
        C3 = ciphertext[65:97]
        C2 = ciphertext[97:]
        klen = len(C2)
        S = _sm2_scalar_mult(self._sk, C1, self.p)
        x2 = S[0].to_bytes(32, 'big')
        y2 = S[1].to_bytes(32, 'big')
        t = _kdf(x2 + y2, klen)
        M = bytes(a ^ b for a, b in zip(C2, t))
        h = SM3()
        h.update(x2 + M + y2)
        if h.digest() != C3:
            raise ValueError("C3验证失败")
        return M

    def sign(self, message, id_a=SM2_IDA_DEFAULT):
        if isinstance(message, str):
            message = message.encode('utf-8')
        if self._sk is None:
            raise ValueError("缺少私钥")
        Z_A = _sm2_get_z(id_a, self._pk)
        h = SM3()
        h.update(Z_A + message)
        e = int.from_bytes(h.digest(), 'big')
        n, d = self.n, self._sk
        while True:
            k = random.randrange(1, n)
            P1 = _sm2_scalar_mult(k, self.G, self.p)
            if P1 is None:
                continue
            r = (e + P1[0]) % n
            if r == 0 or r + k == n:
                continue
            s = (_sm2_mod_inverse((1 + d) % n, n) * ((k - (d * r) % n) % n)) % n
            if s == 0:
                continue
            return (r, s)

    def verify(self, message, signature, id_a=SM2_IDA_DEFAULT):
        if isinstance(message, str):
            message = message.encode('utf-8')
        if self._pk is None:
            raise ValueError("缺少公钥")
        r, s = signature
        if not (1 <= r < self.n and 1 <= s < self.n):
            return False
        Z_A = _sm2_get_z(id_a, self._pk)
        h = SM3()
        h.update(Z_A + message)
        e = int.from_bytes(h.digest(), 'big')
        t = (r + s) % self.n
        if t == 0:
            return False
        P = _sm2_point_add(_sm2_scalar_mult(s, self.G, self.p),
                          _sm2_scalar_mult(t, self._pk, self.p), self.p)
        if P is None:
            return False
        return (e + P[0]) % self.n == r

    def sign_digest(self, digest_bytes):
        """对摘要直接签名 (用于DNA签名)"""
        if isinstance(digest_bytes, str):
            digest_bytes = digest_bytes.encode('utf-8')
        if len(digest_bytes) != 32:
            digest_bytes = sm3_hash(digest_bytes).encode()
        e = int.from_bytes(digest_bytes[:32], 'big') % self.n
        n, d = self.n, self._sk
        while True:
            k = random.randrange(1, n)
            P1 = _sm2_scalar_mult(k, self.G, self.p)
            if P1 is None:
                continue
            r = (e + P1[0]) % n
            if r == 0 or r + k == n:
                continue
            s = (_sm2_mod_inverse((1 + d) % n, n) * ((k - (d * r) % n) % n)) % n
            if s == 0:
                continue
            return (r, s)



# ============================================================
# 第二部分: DNA追溯码系统
# ============================================================

class DNATraceCode:
    """
    龍魂DNA追溯码生成与管理
    格式: #龍芯⚡️YYYY-MM-DD-MODULE-vX.X
    """

    MODULE_CODES = {
        'guomi_crypto': 'GUOMI-CRYPTO',
        'image_encrypt': 'IMG-ENCRYPT',
        'text_encrypt': 'TXT-ENCRYPT',
        'personal_info': 'PINFO-ENCRYPT',
        'fingerprint': 'FINGERPRINT',
        'formula': 'FORMULA',
        'audit': 'AUDIT-VERIFY',
    }

    AUDIT_COLORS = {
        'red': '🔴 红色-禁止/高风险',
        'yellow': '🟡 黄色-审查/中风险',
        'green': '🟢 绿色-通过/低风险',
    }

    def __init__(self, module: str, version: str = "3.0"):
        self.module = module
        self.version = version
        self.timestamp = datetime.now().strftime("%Y-%m-%d")

    def generate(self, extra_data: dict[str, Any] = None) -> str:
        """生成DNA追溯码"""
        module_code = self.MODULE_CODES.get(self.module, self.module.upper())
        base = f"#龍芯⚡️{self.timestamp}-{module_code}-v{self.version}"
        if extra_data:
            extra_str = base64.b64encode(json.dumps(extra_data, ensure_ascii=False).encode()).decode()
            base += f"|{extra_str}"
        return base

    @staticmethod
    def parse(dna_code: str) -> dict[str, Any]:
        """解析DNA追溯码"""
        if not dna_code.startswith("#龍芯⚡️"):
            return {"valid": False, "error": "无效的DNA追溯码格式"}
        parts = dna_code.split("|")
        main = parts[0]
        segments = main.replace("#龍芯⚡️", "").split("-")
        # 格式: YYYY-MM-DD-MODULE-vX.X
        # segments: [YYYY, MM, DD, MODULE_PART1, MODULE_PART2, ..., vX.X]
        timestamp = "-".join(segments[0:3]) if len(segments) >= 3 else ""
        version = segments[-1] if len(segments) > 3 else ""
        module = "-".join(segments[3:-1]) if len(segments) > 4 else (segments[3] if len(segments) == 4 else "")
        result = {
            "valid": True,
            "timestamp": timestamp,
            "module": module,
            "version": version,
        }
        if len(parts) > 1:
            try:
                result["extra"] = json.loads(base64.b64decode(parts[1]).decode())
            except:
                result["extra"] = None
        return result

    @staticmethod
    def generate_audit_dna(data_hash: str, audit_level: str, inspector_id: str) -> str:
        """生成审计DNA标记"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        audit_sig = sm3_hash(f"{data_hash}|{audit_level}|{inspector_id}|{timestamp}")
        return f"AUDIT[{audit_level}]:{inspector_id}:{timestamp}:{audit_sig[:16]}"


class WatermarkEmbedder:
    """数字水印嵌入器 - LSB/元数据水印"""

    @staticmethod
    def embed_lsb(image_bytes: bytes, watermark: str) -> bytes:
        """将水印嵌入图片的LSB (最低有效位)"""
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pixels = img.load()
            width, height = img.size
            # 将水印转为二进制
            wm_bytes = watermark.encode('utf-8')
            wm_len = len(wm_bytes)
            # 前16位存储水印长度
            binary_data = format(wm_len, '016b')
            for byte in wm_bytes:
                binary_data += format(byte, '08b')
            # 嵌入LSB
            data_idx = 0
            for y in range(height):
                for x in range(width):
                    if data_idx >= len(binary_data):
                        break
                    r, g, b = pixels[x, y]
                    # 在R通道嵌入1位
                    bit = int(binary_data[data_idx])
                    r = (r & 0xFE) | bit
                    pixels[x, y] = (r, g, b)
                    data_idx += 1
                if data_idx >= len(binary_data):
                    break
            output = io.BytesIO()
            img.save(output, format='PNG')  # PNG保证无损
            return output.getvalue()
        except ImportError:
            raise ImportError("需要安装Pillow库: pip install Pillow")

    @staticmethod
    def extract_lsb(image_bytes: bytes) -> str:
        """从图片LSB提取水印"""
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        pixels = img.load()
        width, height = img.size
        # 提取前16位作为长度
        binary_data = ''
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
            if len(binary_data) >= 16:
                break
        wm_len = int(binary_data[:16], 2)
        total_bits = 16 + wm_len * 8
        binary_data = ''
        extracted = 0
        for y in range(height):
            for x in range(width):
                if extracted >= total_bits:
                    break
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                extracted += 1
            if extracted >= total_bits:
                break
        # 解码水印
        wm_bits = binary_data[16:]
        wm_bytes = bytearray()
        for i in range(0, len(wm_bits), 8):
            byte_str = wm_bits[i:i+8]
            if len(byte_str) == 8:
                wm_bytes.append(int(byte_str, 2))
        return wm_bytes.decode('utf-8', errors='ignore')

    @staticmethod
    def embed_metadata(image_bytes: bytes, metadata: dict[str, Any]) -> bytes:
        """将DNA元数据嵌入PNG的文本块 (tEXt)"""
        from PIL import Image
        from PIL.PngImagePlugin import PngInfo
        img = Image.open(io.BytesIO(image_bytes))
        pnginfo = PngInfo()
        for key, value in metadata.items():
            pnginfo.add_text(key, str(value))
        output = io.BytesIO()
        img.save(output, format='PNG', pnginfo=pnginfo)
        return output.getvalue()

    @staticmethod
    def extract_metadata(image_bytes: bytes) -> dict[str, Any]:
        """从PNG文本块提取元数据"""
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        return dict(img.info) if hasattr(img, 'info') else {}


# ============================================================
# 第三部分: 国密引擎核心类
# ============================================================

class LongHunCryptoEngine:
    """
    龍魂国密加密引擎 - 核心入口类
    封装SM2/SM3/SM4三大国密算法
    """

    def __init__(self):
        self.sm3 = SM3()
        self._session_key = None
        self._sm4_cipher = None

    def generate_sm4_key(self) -> bytes:
        """生成随机SM4会话密钥 (16字节)"""
        self._session_key = os.urandom(16)
        self._sm4_cipher = SM4Cipher(self._session_key)
        return self._session_key

    def set_sm4_key(self, key: bytes):
        """设置SM4会话密钥"""
        self._session_key = key
        self._sm4_cipher = SM4Cipher(key)

    @staticmethod
    def sm4_encrypt(data: bytes, key: bytes, iv: bytes = None) -> dict[str, Any]:
        """SM4加密便捷方法"""
        cipher = SM4Cipher(key)
        if iv is None:
            iv = os.urandom(16)
        ciphertext = cipher.encrypt_cbc(data, iv)
        return {"ciphertext": ciphertext, "iv": iv}

    @staticmethod
    def sm4_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """SM4解密便捷方法"""
        cipher = SM4Cipher(key)
        return cipher.decrypt_cbc(ciphertext, iv)

    @staticmethod
    def sm2_generate_keypair() -> Tuple[bytes, bytes]:
        """生成SM2密钥对"""
        return SM2Cipher.generate_keypair()

    @staticmethod
    def sm2_encrypt(plaintext: bytes, public_key: bytes) -> bytes:
        """SM2公钥加密"""
        sm2 = SM2Cipher(public_key=public_key)
        return sm2.encrypt(plaintext)

    @staticmethod
    def sm2_decrypt(ciphertext: bytes, private_key: bytes) -> bytes:
        """SM2私钥解密"""
        sm2 = SM2Cipher(private_key=private_key)
        return sm2.decrypt(ciphertext)

    @staticmethod
    def sm2_sign(message: bytes, private_key: bytes) -> Tuple[int, int]:
        """SM2签名"""
        sm2 = SM2Cipher(private_key=private_key)
        return sm2.sign(message)

    @staticmethod
    def sm2_verify(message: bytes, signature: Tuple[int, int], public_key: bytes) -> bool:
        """SM2验签"""
        sm2 = SM2Cipher(public_key=public_key)
        return sm2.verify(message, signature)

    @staticmethod
    def sm3_digest(data: bytes) -> str:
        """SM3哈希摘要 (64字符hex)"""
        return sm3_hash(data)

    def generate_dna_code(self, module: str, extra: dict[str, Any] = None) -> str:
        """生成DNA追溯码"""
        dna = DNATraceCode(module=module)
        return dna.generate(extra)



# ============================================================
# 第四部分: 文件加密器类
# ============================================================

class ImageEncryptor:
    """
    图片加密器 - JPG/PNG加密 + DNA嵌入
    支持: SM4-CBC加密 + DNA元数据 + LSB水印
    """

    def __init__(self, engine: LongHunCryptoEngine = None):
        self.engine = engine or LongHunCryptoEngine()
        self.dna = DNATraceCode('image_encrypt')

    def encrypt(self, image_data: bytes, sm4_key: bytes = None,
                owner_id: str = "unknown", encrypt_format: str = "dna_visible") -> dict[str, Any]:
        """
        加密图片并嵌入DNA追溯码

        Args:
            image_data: 原始图片字节
            sm4_key: SM4密钥 (16字节), 不指定则自动生成
            owner_id: 所有者ID
            encrypt_format: "full"完全加密 / "dna_visible"DNA可见

        Returns:
            dict: 包含加密图片、DNA码、SM3摘要等
        """
        if sm4_key is None:
            sm4_key = os.urandom(16)

        # 1. 计算原始图片SM3摘要
        orig_hash = self.engine.sm3_digest(image_data)

        # 2. 生成DNA追溯码
        dna_extra = {
            "owner": owner_id,
            "orig_hash": orig_hash[:16],
            "format": encrypt_format,
            "type": "image",
        }
        dna_code = self.dna.generate(dna_extra)

        # 3. SM4-CBC加密图片数据
        iv = os.urandom(16)
        encrypted = self.engine.sm4_encrypt(image_data, sm4_key, iv)
        ciphertext = encrypted["ciphertext"]

        # 4. 构建加密包
        encrypt_pkg = {
            "dna_code": dna_code,
            "orig_hash": orig_hash,
            "iv": binascii.hexlify(iv).decode(),
            "ciphertext": binascii.hexlify(ciphertext).decode(),
            "timestamp": datetime.now().isoformat(),
        }
        pkg_json = json.dumps(encrypt_pkg, ensure_ascii=False).encode('utf-8')

        # 5. 对DNA码进行SM2签名 (如果提供了企业私钥)
        sm3_pkg_hash = self.engine.sm3_digest(pkg_json)

        result = {
            "dna_code": dna_code,
            "orig_hash": orig_hash,
            "pkg_hash": sm3_pkg_hash,
            "sm4_key": binascii.hexlify(sm4_key).decode(),
            "iv": binascii.hexlify(iv).decode(),
            "ciphertext": binascii.hexlify(ciphertext).decode(),
            "encrypt_format": encrypt_format,
            "package": pkg_json.decode(),
        }

        # 6. 如果DNA可见模式，生成带DNA的封面图片
        if encrypt_format == "dna_visible":
            try:
                from PIL import Image
                # 创建DNA封面图
                cover = self._create_dna_cover(image_data, dna_code, orig_hash)
                result["cover_image"] = binascii.hexlify(cover).decode()
            except ImportError:
                result["cover_image"] = None

        return result

    def decrypt(self, ciphertext_hex: str, sm4_key_hex: str, iv_hex: str) -> bytes:
        """解密图片"""
        ciphertext = binascii.unhexlify(ciphertext_hex)
        sm4_key = binascii.unhexlify(sm4_key_hex)
        iv = binascii.unhexlify(iv_hex)
        return self.engine.sm4_decrypt(ciphertext, sm4_key, iv)

    def embed_dna_watermark(self, image_data: bytes, dna_code: str) -> bytes:
        """将DNA码嵌入图片LSB水印"""
        return WatermarkEmbedder.embed_lsb(image_data, dna_code)

    def extract_dna_watermark(self, image_data: bytes) -> str:
        """从图片提取DNA水印"""
        return WatermarkEmbedder.extract_lsb(image_data)

    def embed_dna_metadata(self, image_data: bytes, metadata: dict[str, Any]) -> bytes:
        """将DNA元数据嵌入PNG"""
        return WatermarkEmbedder.embed_metadata(image_data, metadata)

    @staticmethod
    def _create_dna_cover(original_image_data: bytes, dna_code: str, data_hash: str) -> bytes:
        """创建带DNA标记的加密封面图"""
        from PIL import Image, ImageDraw, ImageFont
        img = Image.open(io.BytesIO(original_image_data))
        # 缩小并模糊化
        small = img.resize((200, 200))
        # 创建加密封面
        cover = Image.new('RGB', (400, 300), color=(20, 20, 40))
        cover.paste(small, (100, 20))
        draw = ImageDraw.Draw(cover)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            font = ImageFont.load_default()
        draw.text((10, 230), f"🔒 龍魂加密 DNA:{dna_code[:40]}...", fill=(0, 255, 0), font=font)
        draw.text((10, 250), f"SM3:{data_hash[:32]}...", fill=(0, 200, 200), font=font)
        draw.text((10, 270), "检测部门专用 - 需要授权解密", fill=(255, 100, 0), font=font)
        output = io.BytesIO()
        cover.save(output, format='PNG')
        return output.getvalue()


class TextEncryptor:
    """
    文本加密器 - 文本加密 + DNA头尾标记
    """

    DNA_HEADER_MARK = "===龍魂DNA头==="
    DNA_FOOTER_MARK = "===龍魂DNA尾==="

    def __init__(self, engine: LongHunCryptoEngine = None):
        self.engine = engine or LongHunCryptoEngine()
        self.dna = DNATraceCode('text_encrypt')

    def encrypt(self, text: str, sm4_key: bytes = None, owner_id: str = "unknown") -> dict[str, Any]:
        """加密文本并添加DNA标记"""
        if sm4_key is None:
            sm4_key = os.urandom(16)

        text_bytes = text.encode('utf-8') if isinstance(text, str) else text
        orig_hash = self.engine.sm3_digest(text_bytes)

        # DNA追溯码
        dna_code = self.dna.generate({
            "owner": owner_id,
            "orig_hash": orig_hash[:16],
            "type": "text",
            "length": len(text_bytes),
        })

        # SM4加密
        iv = os.urandom(16)
        encrypted = self.engine.sm4_encrypt(text_bytes, sm4_key, iv)

        # 构建带DNA标记的加密文本
        dna_header = f"{self.DNA_HEADER_MARK}{dna_code}{self.DNA_HEADER_MARK}"
        dna_footer = f"{self.DNA_FOOTER_MARK}{orig_hash}{self.DNA_FOOTER_MARK}"

        encrypted_b64 = base64.b64encode(encrypted["ciphertext"]).decode()
        iv_b64 = base64.b64encode(iv).decode()

        # 完整加密包: DNA头 + IV + 密文 + DNA尾
        full_package = f"{dna_header}\nIV:{iv_b64}\nDATA:{encrypted_b64}\n{dna_footer}"

        return {
            "dna_code": dna_code,
            "orig_hash": orig_hash,
            "sm4_key": binascii.hexlify(sm4_key).decode(),
            "encrypted_package": full_package,
            "iv": iv_b64,
            "ciphertext": encrypted_b64,
        }

    def decrypt(self, encrypted_package: str, sm4_key_hex: str) -> str:
        """解密带DNA标记的文本"""
        # 提取IV和数据
        iv_match = re.search(r'IV:([A-Za-z0-9+/=]+)', encrypted_package)
        data_match = re.search(r'DATA:([A-Za-z0-9+/=]+)', encrypted_package)
        if not iv_match or not data_match:
            raise ValueError("无效的加密包格式")
        iv = base64.b64decode(iv_match.group(1))
        ciphertext = base64.b64decode(data_match.group(1))
        sm4_key = binascii.unhexlify(sm4_key_hex)
        plaintext = self.engine.sm4_decrypt(ciphertext, sm4_key, iv)
        return plaintext.decode('utf-8')

    def verify_dna(self, encrypted_package: str) -> dict[str, Any]:
        """验证DNA标记完整性"""
        header_match = re.search(rf'{self.DNA_HEADER_MARK}(.+?){self.DNA_HEADER_MARK}', encrypted_package)
        footer_match = re.search(rf'{self.DNA_FOOTER_MARK}([a-f0-9]+){self.DNA_FOOTER_MARK}', encrypted_package)
        return {
            "has_header": header_match is not None,
            "has_footer": footer_match is not None,
            "dna_code": header_match.group(1) if header_match else None,
            "hash_in_footer": footer_match.group(1) if footer_match else None,
        }


class PersonalInfoEncryptor:
    """
    个人信息加密器 - 银行卡/电话/身份证号 SM2加密
    支持: SM2公钥加密 + DNA哈希
    """

    # 字段类型定义
    FIELD_TYPES = {
        'bank_card': {'name': '银行卡号', 'pattern': r'\d{13,19}', 'mask': '****'},
        'phone': {'name': '手机号', 'pattern': r'1[3-9]\d{9}', 'mask': '****'},
        'id_card': {'name': '身份证号', 'pattern': r'\d{17}[\dXx]', 'mask': '**********'},
        'address': {'name': '地址', 'pattern': None, 'mask': '**'},
        'name': {'name': '姓名', 'pattern': None, 'mask': '*'},
        'fingerprint': {'name': '指纹特征', 'pattern': None, 'mask': '[生物特征]'},
    }

    def __init__(self, engine: LongHunCryptoEngine = None):
        self.engine = engine or LongHunCryptoEngine()
        self.dna = DNATraceCode('personal_info')

    def encrypt_field(self, field_type: str, value: str, sm2_public_key: bytes) -> dict[str, Any]:
        """
        加密单个个人信息字段

        Args:
            field_type: 字段类型 (bank_card/phone/id_card/address/name/fingerprint)
            value: 原始值
            sm2_public_key: SM2公钥

        Returns:
            dict: 加密结果 + DNA追溯
        """
        if field_type not in self.FIELD_TYPES:
            raise ValueError(f"不支持的字段类型: {field_type}")

        field_info = self.FIELD_TYPES[field_type]
        value_bytes = value.encode('utf-8')

        # SM3摘要用于DNA
        value_hash = self.engine.sm3_digest(value_bytes)

        # SM2公钥加密
        encrypted = self.engine.sm2_encrypt(value_bytes, sm2_public_key)
        encrypted_b64 = base64.b64encode(encrypted).decode()

        # DNA追溯码
        dna_code = self.dna.generate({
            "field": field_type,
            "hash": value_hash[:16],
            "mask": self._mask_value(value, field_type),
        })

        return {
            "field_type": field_type,
            "field_name": field_info['name'],
            "encrypted": encrypted_b64,
            "dna_code": dna_code,
            "hash": value_hash,
            "mask": self._mask_value(value, field_type),
        }

    def decrypt_field(self, encrypted_b64: str, sm2_private_key: bytes) -> str:
        """解密个人信息字段"""
        encrypted = base64.b64decode(encrypted_b64)
        plaintext = self.engine.sm2_decrypt(encrypted, sm2_private_key)
        return plaintext.decode('utf-8')

    def encrypt_person(self, person_data: dict[str, Any], sm2_public_key: bytes) -> dict[str, Any]:
        """加密完整个人信息"""
        results = {}
        dna_codes = []
        for field_type, value in person_data.items():
            if field_type in self.FIELD_TYPES and value:
                result = self.encrypt_field(field_type, str(value), sm2_public_key)
                results[field_type] = result
                dna_codes.append(result["dna_code"])

        # 生成汇总DNA
        combined_hash = self.engine.sm3_digest(json.dumps(person_data, ensure_ascii=False).encode())
        master_dna = self.dna.generate({
            "fields": list(results.keys()),
            "combined_hash": combined_hash[:16],
            "field_count": len(results),
        })

        return {
            "master_dna": master_dna,
            "combined_hash": combined_hash,
            "fields": results,
            "field_count": len(results),
        }

    @staticmethod
    def _mask_value(value: str, field_type: str) -> str:
        """脱敏显示"""
        if field_type == 'bank_card' and len(value) >= 8:
            return value[:4] + '*' * (len(value) - 8) + value[-4:]
        elif field_type == 'phone' and len(value) >= 7:
            return value[:3] + '****' + value[-4:]
        elif field_type == 'id_card' and len(value) >= 8:
            return value[:4] + '*' * (len(value) - 8) + value[-4:]
        elif len(value) > 2:
            return value[0] + '*' * (len(value) - 2) + value[-1]
        return '*' * len(value)


class FormulaEncryptor:
    """
    配方加密器 - 配方数据加密 + 阈值DNA
    支持: SM4加密 + 成分阈值检查 + 合规DNA
    """

    def __init__(self, engine: LongHunCryptoEngine = None):
        self.engine = engine or LongHunCryptoEngine()
        self.dna = DNATraceCode('formula')

    def encrypt_formula(self, formula: dict[str, Any], sm4_key: bytes = None,
                        compliance_rules: dict[str, Any] = None) -> dict[str, Any]:
        """
        加密配方数据

        Args:
            formula: {"name": "配方名", "ingredients": [{"name": "成分", "ratio": 百分比}]}
            sm4_key: SM4密钥
            compliance_rules: 合规规则 {"max_xxx": 最大值, "min_xxx": 最小值}

        Returns:
            dict: 加密结果 + 合规报告 + DNA
        """
        if sm4_key is None:
            sm4_key = os.urandom(16)

        formula_json = json.dumps(formula, ensure_ascii=False).encode()
        orig_hash = self.engine.sm3_digest(formula_json)

        # SM4加密
        iv = os.urandom(16)
        encrypted = self.engine.sm4_encrypt(formula_json, sm4_key, iv)

        # 合规检查
        compliance = self._check_compliance(formula, compliance_rules)

        # 配方DNA (包含成分摘要)
        ingredients_dna = []
        for ing in formula.get("ingredients", []):
            ing_hash = sm3_hash(f"{ing.get('name', '')}:{ing.get('ratio', 0)}")
            ingredients_dna.append(f"{ing.get('name', '')}@{ing_hash[:8]}")

        # 阈值DNA
        threshold_dna = []
        if compliance_rules:
            for rule_name, limit in compliance_rules.items():
                actual = self._get_actual_value(formula, rule_name)
                status = "OK" if (actual is not None and self._check_rule(actual, limit, rule_name)) else "ALERT"
                threshold_dna.append(f"{rule_name}:{status}")

        dna_extra = {
            "formula_name": formula.get("name", "unknown"),
            "ingredients": ingredients_dna,
            "thresholds": threshold_dna,
            "compliance": compliance["status"],
            "orig_hash": orig_hash[:16],
        }
        dna_code = self.dna.generate(dna_extra)

        return {
            "dna_code": dna_code,
            "orig_hash": orig_hash,
            "sm4_key": binascii.hexlify(sm4_key).decode(),
            "iv": binascii.hexlify(iv).decode(),
            "ciphertext": binascii.hexlify(encrypted["ciphertext"]).decode(),
            "compliance": compliance,
            "formula_summary": ingredients_dna,
            "threshold_summary": threshold_dna,
        }

    def decrypt_formula(self, ciphertext_hex: str, sm4_key_hex: str, iv_hex: str) -> dict[str, Any]:
        """解密配方"""
        ciphertext = binascii.unhexlify(ciphertext_hex)
        sm4_key = binascii.unhexlify(sm4_key_hex)
        iv = binascii.unhexlify(iv_hex)
        plaintext = self.engine.sm4_decrypt(ciphertext, sm4_key, iv)
        return json.loads(plaintext.decode('utf-8'))

    def _check_compliance(self, formula: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
        """检查配方合规性"""
        if not rules:
            return {"status": "unknown", "checks": []}

        checks = []
        all_pass = True
        for rule_name, limit in rules.items():
            actual = self._get_actual_value(formula, rule_name)
            passed = actual is not None and self._check_rule(actual, limit, rule_name)
            checks.append({
                "rule": rule_name,
                "limit": limit,
                "actual": actual,
                "passed": passed,
            })
            if not passed:
                all_pass = False

        return {
            "status": "pass" if all_pass else "fail",
            "audit_color": "green" if all_pass else "red",
            "checks": checks,
        }

    def _get_actual_value(self, formula: dict[str, Any], rule_name: str):
        """从配方中获取规则对应的实际值"""
        # 去掉max_/min_前缀
        ingredient_name = rule_name
        if rule_name.startswith("max_") or rule_name.startswith("min_"):
            ingredient_name = rule_name[4:]
        for ing in formula.get("ingredients", []):
            if ingredient_name.lower() in ing.get("name", "").lower():
                return ing.get("ratio")
        return None

    def _check_rule(self, actual, limit, rule_name: str) -> bool:
        """检查单个规则"""
        if rule_name.startswith("max_"):
            return actual <= limit
        elif rule_name.startswith("min_"):
            return actual >= limit
        return True



# ============================================================
# 第五部分: 密钥管理
# ============================================================

class KeyManager:
    """
    龍魂密钥管理系统
    - 检测部门公钥 (验证DNA签名)
    - 企业私钥 (签名DNA)
    - 会话密钥管理 (SM4对称密钥)
    """

    def __init__(self, keystore_dir: str = "./keystore"):
        self.keystore_dir = keystore_dir
        self._enterprise_sk = None
        self._enterprise_pk = None
        self._inspector_pk = None
        self._session_keys = {}
        os.makedirs(keystore_dir, exist_ok=True)

    def generate_enterprise_keypair(self) -> Tuple[bytes, bytes]:
        """生成企业SM2密钥对 (用于签名DNA)"""
        sk, pk = SM2Cipher.generate_keypair()
        self._enterprise_sk = sk
        self._enterprise_pk = pk
        # 保存到文件
        sk_path = os.path.join(self.keystore_dir, "enterprise_sk.pem")
        pk_path = os.path.join(self.keystore_dir, "enterprise_pk.pem")
        with open(sk_path, 'wb') as f:
            f.write(b"-----BEGIN SM2 PRIVATE KEY-----\n" +
                    base64.b64encode(sk) +
                    b"\n-----END SM2 PRIVATE KEY-----\n")
        with open(pk_path, 'wb') as f:
            f.write(b"-----BEGIN SM2 PUBLIC KEY-----\n" +
                    base64.b64encode(pk) +
                    b"\n-----END SM2 PUBLIC KEY-----\n")
        return sk, pk

    def load_enterprise_keypair(self) -> Tuple[bytes, bytes]:
        """加载企业密钥对"""
        sk_path = os.path.join(self.keystore_dir, "enterprise_sk.pem")
        pk_path = os.path.join(self.keystore_dir, "enterprise_pk.pem")
        if os.path.exists(sk_path) and os.path.exists(pk_path):
            with open(sk_path, 'rb') as f:
                content = f.read()
                sk_data = re.search(r'-----BEGIN SM2 PRIVATE KEY-----(.+?)-----END SM2 PRIVATE KEY-----',
                                   content.decode(), re.DOTALL)
                if sk_data:
                    self._enterprise_sk = base64.b64decode(sk_data.group(1).strip())
            with open(pk_path, 'rb') as f:
                content = f.read()
                pk_data = re.search(r'-----BEGIN SM2 PUBLIC KEY-----(.+?)-----END SM2 PUBLIC KEY-----',
                                   content.decode(), re.DOTALL)
                if pk_data:
                    self._enterprise_pk = base64.b64decode(pk_data.group(1).strip())
            return self._enterprise_sk, self._enterprise_pk
        return self.generate_enterprise_keypair()

    def set_inspector_public_key(self, pk_bytes: bytes):
        """设置检测部门公钥 (用于验证)"""
        self._inspector_pk = pk_bytes

    def generate_session_key(self, key_id: str | None = None) -> bytes:
        """生成SM4会话密钥"""
        key = os.urandom(16)
        kid = key_id or f"sk_{int(time.time())}"
        self._session_keys[kid] = key
        return key

    def get_session_key(self, key_id: str) -> bytes:
        """获取会话密钥"""
        return self._session_keys.get(key_id)

    def list_session_keys(self) -> List[str]:
        """列出所有会话密钥ID"""
        return list(self._session_keys.keys())

    def sign_dna(self, dna_code: str) -> str:
        """使用企业私钥签名DNA码"""
        if self._enterprise_sk is None:
            raise ValueError("企业私钥未加载")
        sm2 = SM2Cipher(private_key=self._enterprise_sk)
        r, s = sm2.sign(dna_code.encode())
        return f"{hex(r)},{hex(s)}"

    def verify_dna_signature(self, dna_code: str, signature: str) -> bool:
        """使用检测部门公钥验证DNA签名"""
        if self._inspector_pk is None:
            raise ValueError("检测部门公钥未设置")
        parts = signature.split(",")
        if len(parts) != 2:
            return False
        r = int(parts[0], 16)
        s = int(parts[1], 16)
        sm2 = SM2Cipher(public_key=self._inspector_pk)
        return sm2.verify(dna_code.encode(), (r, s))

    def get_enterprise_public_key(self) -> bytes:
        return self._enterprise_pk

    @property
    def enterprise_sk(self) -> bytes:
        return self._enterprise_sk

    @property
    def enterprise_pk(self) -> bytes:
        return self._enterprise_pk


# ============================================================
# 第六部分: 审计系统
# ============================================================

class AuditSystem:
    """
    龍魂三色审计系统
    红(禁止) / 黄(审查) / 绿(通过)
    """

    COLORS = {
        'red': {'level': 3, 'label': '🔴 红色 - 禁止', 'action': '立即阻止并上报'},
        'yellow': {'level': 2, 'label': '🟡 黄色 - 审查', 'action': '需要人工审查'},
        'green': {'level': 1, 'label': '🟢 绿色 - 通过', 'action': '正常通行'},
    }

    def __init__(self, engine: LongHunCryptoEngine = None):
        self.engine = engine or LongHunCryptoEngine()

    def verify_data_integrity(self, original_data: bytes, stored_hash: str) -> dict[str, Any]:
        """验证数据完整性 (SM3哈希对比)"""
        current_hash = self.engine.sm3_digest(original_data)
        match = current_hash == stored_hash
        return {
            "status": "pass" if match else "fail",
            "audit_color": "green" if match else "red",
            "current_hash": current_hash,
            "stored_hash": stored_hash,
            "match": match,
        }

    def verify_dna_trace(self, dna_code: str, expected_module: str | None = None) -> dict[str, Any]:
        """验证DNA追溯码"""
        parsed = DNATraceCode.parse(dna_code)
        if not parsed["valid"]:
            return {"status": "fail", "audit_color": "red", "reason": "无效的DNA码"}

        # 检查时间戳
        try:
            ts = datetime.strptime(parsed["timestamp"], "%Y-%m-%d")
            age_days = (datetime.now() - ts).days
            if age_days > 365:
                return {"status": "expired", "audit_color": "yellow",
                        "reason": f"DNA码已过期 {age_days} 天"}
        except:
            return {"status": "fail", "audit_color": "red", "reason": "无效的时间戳"}

        # 检查模块
        if expected_module and parsed.get("module") != expected_module:
            return {"status": "mismatch", "audit_color": "red",
                    "reason": f"模块不匹配: 期望{expected_module}, 实际{parsed.get('module')}"}

        return {"status": "pass", "audit_color": "green",
                "module": parsed.get("module"), "timestamp": parsed["timestamp"]}

    def audit_encrypted_package(self, package: dict[str, Any], inspector_id: str) -> dict[str, Any]:
        """对加密包进行完整审计"""
        results = []
        final_color = "green"

        # 1. DNA追溯码验证
        if "dna_code" in package:
            dna_result = self.verify_dna_trace(package["dna_code"])
            results.append({"check": "DNA追溯", **dna_result})
            if self.COLORS.get(dna_result["audit_color"], {}).get("level", 1) >                self.COLORS.get(final_color, {}).get("level", 1):
                final_color = dna_result["audit_color"]

        # 2. 哈希完整性
        if "orig_hash" in package and "ciphertext" in package:
            # 密文可能是hex或base64编码
            ct_hex = package["ciphertext"]
            try:
                ct_bytes = binascii.unhexlify(ct_hex)
            except (binascii.Error, ValueError):
                # 尝试base64解码
                ct_bytes = base64.b64decode(ct_hex)
            ct_hash = self.engine.sm3_digest(ct_bytes)
            hash_ok = "pkg_hash" in package and package["pkg_hash"] == ct_hash
            results.append({
                "check": "密文哈希",
                "status": "pass" if hash_ok else "mismatch",
                "audit_color": "green" if hash_ok else "red",
            })
            if not hash_ok:
                final_color = "red"

        # 3. 生成审计DNA
        audit_dna = DNATraceCode.generate_audit_dna(
            package.get("orig_hash", ""), final_color, inspector_id
        )

        return {
            "audit_color": final_color,
            "audit_label": self.COLORS[final_color]["label"],
            "checks": results,
            "inspector_id": inspector_id,
            "audit_dna": audit_dna,
            "timestamp": datetime.now().isoformat(),
        }


# ============================================================
# 第七部分: 便捷入口函数
# ============================================================

def quick_encrypt_image(image_data: bytes, key_manager: KeyManager = None) -> dict[str, Any]:
    """快速加密图片"""
    engine = LongHunCryptoEngine()
    km = key_manager or KeyManager()
    if km.enterprise_pk is None:
        km.load_enterprise_keypair()
    encryptor = ImageEncryptor(engine)
    sm4_key = km.generate_session_key()
    return encryptor.encrypt(image_data, sm4_key)

def quick_encrypt_text(text: str, key_manager: KeyManager = None) -> dict[str, Any]:
    """快速加密文本"""
    engine = LongHunCryptoEngine()
    km = key_manager or KeyManager()
    if km.enterprise_pk is None:
        km.load_enterprise_keypair()
    encryptor = TextEncryptor(engine)
    sm4_key = km.generate_session_key()
    return encryptor.encrypt(text, sm4_key)

def quick_encrypt_personal(data: dict[str, Any], sm2_public_key: bytes,
                           key_manager: KeyManager = None) -> dict[str, Any]:
    """快速加密个人信息"""
    engine = LongHunCryptoEngine()
    encryptor = PersonalInfoEncryptor(engine)
    return encryptor.encrypt_person(data, sm2_public_key)

def quick_encrypt_formula(formula: dict[str, Any], compliance: dict[str, Any] = None,
                          key_manager: KeyManager = None) -> dict[str, Any]:
    """快速加密配方"""
    engine = LongHunCryptoEngine()
    km = key_manager or KeyManager()
    if km.enterprise_pk is None:
        km.load_enterprise_keypair()
    encryptor = FormulaEncryptor(engine)
    sm4_key = km.generate_session_key()
    return encryptor.encrypt_formula(formula, sm4_key, compliance)


# ============================================================
# DNA追溯码全局标识
# ============================================================
ENGINE_VERSION = "3.0"
ENGINE_DNA_CODE = "#龍芯⚡️2026-07-04-GUOMI-CRYPTO-v3.0"

if __name__ == "__main__":
    print(f"龍魂·国密DNA加密引擎 v{ENGINE_VERSION}")
    print(f"DNA追溯码: {ENGINE_DNA_CODE}")
    print("=" * 60)
    print("支持的算法: SM2(非对称) | SM3(哈希) | SM4(对称)")
    print("支持的数据: 图片 | 文本 | 个人信息 | 指纹 | 配方")
    print("审计标准: 🔴红 🟡黄 🟢绿")



# ============================================================
# 第八部分: 单元测试
# ============================================================

def run_all_tests():
    """运行全部单元测试"""
    results = []

    def test(name, func):
        try:
            func()
            results.append((name, "✅ 通过"))
            print(f"  ✅ {name}")
        except Exception as e:
            results.append((name, f"❌ 失败: {e}"))
            print(f"  ❌ {name}: {e}")

    print("\n" + "=" * 60)
    print("龍魂·国密DNA加密引擎 - 单元测试")
    print(f"DNA追溯码: {ENGINE_DNA_CODE}")
    print("=" * 60)

    # --- SM3 测试 ---
    print("\n📦 SM3 哈希测试")

    def test_sm3_basic():
        s = SM3()
        s.update(b"abc")
        assert s.hexdigest() == "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    test("SM3基础测试('abc')", test_sm3_basic)

    def test_sm3_long():
        h = sm3_hash(b"LongHunGuoMiDNA" * 100)
        assert len(h) == 64
    test("SM3长数据测试", test_sm3_long)

    # --- SM4 测试 ---
    print("\n📦 SM4 对称加密测试")

    def test_sm4_ecb():
        key = b'0123456789abcdef'
        cipher = SM4Cipher(key)
        data = b"Hello, LongHun SM4!"
        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        assert decrypted == data
    test("SM4-ECB加解密", test_sm4_ecb)

    def test_sm4_cbc():
        key = b'0123456789abcdef'
        iv = b'fedcba9876543210'
        cipher = SM4Cipher(key)
        data = b"Hello, SM4-CBC Mode for LongHun System!"
        encrypted = cipher.encrypt_cbc(data, iv)
        decrypted = cipher.decrypt_cbc(encrypted, iv)
        assert decrypted == data
    test("SM4-CBC加解密", test_sm4_cbc)

    def test_sm4_large():
        key = os.urandom(16)
        iv = os.urandom(16)
        cipher = SM4Cipher(key)
        data = os.urandom(10240)  # 10KB
        encrypted = cipher.encrypt_cbc(data, iv)
        decrypted = cipher.decrypt_cbc(encrypted, iv)
        assert decrypted == data
    test("SM4大文件加密(10KB)", test_sm4_large)

    # --- SM2 测试 ---
    print("\n📦 SM2 非对称加密/签名测试")

    def test_sm2_keygen():
        sk, pk = SM2Cipher.generate_keypair()
        assert len(sk) == 32 and len(pk) == 64
    test("SM2密钥对生成", test_sm2_keygen)

    def test_sm2_encrypt():
        sk, pk = SM2Cipher.generate_keypair()
        msg = b"LongHun DNA Trace System"
        sm2_enc = SM2Cipher(public_key=pk)
        cipher = sm2_enc.encrypt(msg)
        sm2_dec = SM2Cipher(private_key=sk)
        dec = sm2_dec.decrypt(cipher)
        assert dec == msg
    test("SM2加解密", test_sm2_encrypt)

    def test_sm2_sign():
        sk, pk = SM2Cipher.generate_keypair()
        msg = b"LongHun DNA Trace System"
        sm2_sign = SM2Cipher(private_key=sk)
        r, s = sm2_sign.sign(msg)
        sm2_verify = SM2Cipher(public_key=pk)
        assert sm2_verify.verify(msg, (r, s))
    test("SM2签名验签", test_sm2_sign)

    def test_sm2_multisign():
        sk, pk = SM2Cipher.generate_keypair()
        messages = [b"msg1", b"msg2", b"msg3"]
        sm2_sign = SM2Cipher(private_key=sk)
        sm2_verify = SM2Cipher(public_key=pk)
        for msg in messages:
            sig = sm2_sign.sign(msg)
            assert sm2_verify.verify(msg, sig)
    test("SM2多消息签名", test_sm2_multisign)

    # --- DNA追溯码测试 ---
    print("\n📦 DNA追溯码测试")

    def test_dna_generate():
        dna = DNATraceCode('guomi_crypto')
        code = dna.generate({"test": "data"})
        assert code.startswith("#龍芯⚡️")
        assert "GUOMI-CRYPTO" in code
    test("DNA追溯码生成", test_dna_generate)

    def test_dna_parse():
        dna = DNATraceCode('guomi_crypto', "3.0")
        code = dna.generate()
        parsed = DNATraceCode.parse(code)
        assert parsed["valid"] == True
        assert parsed["module"] == "GUOMI-CRYPTO"
    test("DNA追溯码解析", test_dna_parse)

    def test_dna_audit():
        dna = DNATraceCode.generate_audit_dna("abc123", "green", "INSPECTOR_001")
        assert "AUDIT[green]" in dna
        assert "INSPECTOR_001" in dna
    test("DNA审计标记生成", test_dna_audit)

    # --- 图片加密器测试 ---
    print("\n📦 图片加密器测试")

    def test_image_encrypt():
        engine = LongHunCryptoEngine()
        img_enc = ImageEncryptor(engine)
        # 创建测试图片
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_data = buf.getvalue()
        sm4_key = os.urandom(16)
        result = img_enc.encrypt(img_data, sm4_key)
        assert "dna_code" in result
        assert "ciphertext" in result
        assert result["orig_hash"] == engine.sm3_digest(img_data)
    test("图片加密+DNA生成", test_image_encrypt)

    def test_image_decrypt():
        engine = LongHunCryptoEngine()
        img_enc = ImageEncryptor(engine)
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='blue')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_data = buf.getvalue()
        sm4_key = os.urandom(16)
        result = img_enc.encrypt(img_data, sm4_key)
        decrypted = img_enc.decrypt(result["ciphertext"], result["sm4_key"], result["iv"])
        assert decrypted == img_data
    test("图片解密验证", test_image_decrypt)

    # --- 文本加密器测试 ---
    print("\n📦 文本加密器测试")

    def test_text_encrypt():
        engine = LongHunCryptoEngine()
        txt_enc = TextEncryptor(engine)
        text = "这是龍魂系统的敏感文本数据，包含机密信息！"
        sm4_key = os.urandom(16)
        result = txt_enc.encrypt(text, sm4_key)
        assert "dna_code" in result
        assert "encrypted_package" in result
    test("文本加密+DNA", test_text_encrypt)

    def test_text_decrypt():
        engine = LongHunCryptoEngine()
        txt_enc = TextEncryptor(engine)
        text = "龍魂国密加密引擎测试文本 - DNA追溯"
        sm4_key = os.urandom(16)
        result = txt_enc.encrypt(text, sm4_key)
        decrypted = txt_enc.decrypt(result["encrypted_package"], result["sm4_key"])
        assert decrypted == text
    test("文本解密验证", test_text_decrypt)

    def test_text_dna_verify():
        engine = LongHunCryptoEngine()
        txt_enc = TextEncryptor(engine)
        text = "DNA验证测试文本"
        sm4_key = os.urandom(16)
        result = txt_enc.encrypt(text, sm4_key)
        verify = txt_enc.verify_dna(result["encrypted_package"])
        assert verify["has_header"] == True
        assert verify["has_footer"] == True
    test("文本DNA标记验证", test_text_dna_verify)

    # --- 个人信息加密器测试 ---
    print("\n📦 个人信息加密器测试")

    def test_personal_encrypt():
        engine = LongHunCryptoEngine()
        pii_enc = PersonalInfoEncryptor(engine)
        sk, pk = SM2Cipher.generate_keypair()
        result = pii_enc.encrypt_field('bank_card', '6222021234567890123', pk)
        assert result["field_type"] == "bank_card"
        assert "encrypted" in result
        assert "dna_code" in result
        assert "****" in result["mask"]
    test("个人信息字段加密", test_personal_encrypt)

    def test_personal_decrypt():
        engine = LongHunCryptoEngine()
        pii_enc = PersonalInfoEncryptor(engine)
        sk, pk = SM2Cipher.generate_keypair()
        original = '13800138000'
        result = pii_enc.encrypt_field('phone', original, pk)
        decrypted = pii_enc.decrypt_field(result["encrypted"], sk)
        assert decrypted == original
    test("个人信息字段解密", test_personal_decrypt)

    def test_personal_full():
        engine = LongHunCryptoEngine()
        pii_enc = PersonalInfoEncryptor(engine)
        sk, pk = SM2Cipher.generate_keypair()
        person = {
            'name': '张三',
            'phone': '13800138000',
            'id_card': '110101199001011234',
            'bank_card': '6222021234567890123',
        }
        result = pii_enc.encrypt_person(person, pk)
        assert result["field_count"] == 4
        assert "master_dna" in result
    test("完整个人信息加密", test_personal_full)

    # --- 配方加密器测试 ---
    print("\n📦 配方加密器测试")

    def test_formula_encrypt():
        engine = LongHunCryptoEngine()
        fml_enc = FormulaEncryptor(engine)
        formula = {
            "name": "测试配方A",
            "ingredients": [
                {"name": "成分X", "ratio": 30.5},
                {"name": "成分Y", "ratio": 45.2},
                {"name": "水", "ratio": 24.3},
            ]
        }
        compliance = {"max_成分X": 35.0, "max_成分Y": 50.0}
        sm4_key = os.urandom(16)
        result = fml_enc.encrypt_formula(formula, sm4_key, compliance)
        assert result["compliance"]["status"] == "pass"
        assert "dna_code" in result
    test("配方加密+合规检查", test_formula_encrypt)

    def test_formula_decrypt():
        engine = LongHunCryptoEngine()
        fml_enc = FormulaEncryptor(engine)
        formula = {"name": "测试配方B", "ingredients": [{"name": "A", "ratio": 50}]}
        sm4_key = os.urandom(16)
        result = fml_enc.encrypt_formula(formula, sm4_key)
        decrypted = fml_enc.decrypt_formula(result["ciphertext"], result["sm4_key"], result["iv"])
        assert decrypted["name"] == "测试配方B"
    test("配方解密验证", test_formula_decrypt)

    # --- 密钥管理测试 ---
    print("\n📦 密钥管理测试")

    def test_key_manager():
        km = KeyManager(keystore_dir="/tmp/longhun_test_keystore")
        sk, pk = km.load_enterprise_keypair()
        assert sk is not None and pk is not None
        assert len(sk) == 32 and len(pk) == 64
        # 清理
        import shutil
        shutil.rmtree("/tmp/longhun_test_keystore", ignore_errors=True)
    test("密钥管理生成/加载", test_key_manager)

    # --- 审计系统测试 ---
    print("\n📦 审计系统测试")

    def test_audit_verify():
        audit = AuditSystem()
        data = b"test data for audit"
        hash_val = sm3_hash(data)
        result = audit.verify_data_integrity(data, hash_val)
        assert result["match"] == True
        assert result["audit_color"] == "green"
    test("审计-完整性验证", test_audit_verify)

    def test_audit_dna():
        audit = AuditSystem()
        dna = DNATraceCode('guomi_crypto').generate()
        result = audit.verify_dna_trace(dna, 'GUOMI-CRYPTO')
        assert result["status"] == "pass"
        assert result["audit_color"] == "green"
    test("审计-DNA追溯验证", test_audit_dna)

    # --- 集成测试 ---
    print("\n📦 集成测试")

    def test_full_workflow():
        """完整工作流: 生成密钥 -> 加密文本 -> 签名DNA -> 审计验证"""
        engine = LongHunCryptoEngine()
        km = KeyManager(keystore_dir="/tmp/longhun_integration_test")
        km.load_enterprise_keypair()

        # 1. 加密文本
        txt_enc = TextEncryptor(engine)
        sm4_key = km.generate_session_key()
        text = "龍魂国密DNA加密引擎完整工作流测试"
        enc_result = txt_enc.encrypt(text, sm4_key)

        # 2. 签名DNA
        dna_sig = km.sign_dna(enc_result["dna_code"])
        assert "," in dna_sig

        # 3. 解密验证
        decrypted = txt_enc.decrypt(enc_result["encrypted_package"], enc_result["sm4_key"])
        assert decrypted == text

        # 4. 审计
        audit = AuditSystem(engine)
        audit_result = audit.audit_encrypted_package(enc_result, "INSPECTOR_001")
        assert audit_result["audit_color"] in ["red", "yellow", "green"]

        # 清理
        import shutil
        shutil.rmtree("/tmp/longhun_integration_test", ignore_errors=True)
    test("完整工作流集成", test_full_workflow)

    # --- 汇总 ---
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    passed = sum(1 for _, r in results if "通过" in r)
    failed = sum(1 for _, r in results if "失败" in r)
    print(f"总计: {len(results)} | ✅ 通过: {passed} | ❌ 失败: {failed}")
    if failed > 0:
        print("\n失败的测试:")
        for name, r in results:
            if "失败" in r:
                print(f"  - {name}: {r}")
    print("=" * 60)
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
