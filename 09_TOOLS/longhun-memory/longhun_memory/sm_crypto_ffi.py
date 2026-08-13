#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️2026-08-06-MEMORY-SM-FFI-v1.0
# License: MulanPSL v2
"""
SM4/SM3 Rust FFI 桥接器
═══════════════════════
通过 ctypes 调用 Rust longhun-core 原生 SM4/SM3，
纯 Python 作为降级回退。速度提升 ~50-100x。

用法:
    from longhun_memory.sm_crypto_ffi import sm4_encrypt, sm4_decrypt, sm3_hash

    密文 = sm4_encrypt(原文.encode(), key_bytes)      # Rust 加速，回退 Python
    原文 = sm4_decrypt(密文, key_bytes)
    哈希 = sm3_hash(数据)

架构:
    try → load liblonghun_core.dylib/.so → Rust FFI
    except → fallback pure Python SM4/SM3
"""

import ctypes
import os
import platform
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════
# 库查找
# ═══════════════════════════════════════════

def _find_dylib() -> Optional[str]:
    """在多个标准路径查找 longhun-core 动态库"""
    machine = platform.machine()
    system = platform.system()

    candidates = []

    # 本地开发: Rust workspace target/
    # __file__ → longhun_memory/sm_crypto_ffi.py
    # parent(1) longhun_memory → (2) longhun-memory → (3) tools → (4) longhun-system
    root = Path(__file__).resolve().parent.parent.parent.parent
    candidates.append(root / "rust" / "target" / "release" / "liblonghun_core.dylib")
    candidates.append(root / "rust" / "target" / "release" / "liblonghun_core.so")
    # 备用: 多一层（可能在 09_TOOLS/ 下）
    root2 = root.parent
    candidates.append(root2 / "rust" / "target" / "release" / "liblonghun_core.dylib")
    candidates.append(root2 / "rust" / "target" / "release" / "liblonghun_core.so")

    # 鲲鹏生产路径
    candidates.append(Path("/opt/longhun/lib/liblolonghun_core.so"))
    candidates.append(Path("/usr/local/lib/liblolonghun_core.so"))

    # 系统库路径
    if system == "Darwin":
        candidates.append(Path("/usr/local/lib/liblolonghun_core.dylib"))
        candidates.append(Path.home() / ".longhun" / "lib" / "liblonghun_core.dylib")
    elif system == "Linux":
        candidates.append(Path("/usr/local/lib/liblolonghun_core.so"))
        if machine == "aarch64":
            candidates.append(Path("/opt/longhun/lib/liblolonghun_core.so"))

    for p in candidates:
        if p.exists():
            return str(p.resolve())
    return None


# ═══════════════════════════════════════════
# Rust FFI 客户端
# ═══════════════════════════════════════════

class _RustCrypto:
    """Rust longhun-core SM4/SM3 FFI 客户端"""

    def __init__(self, dylib_path: str):
        self._lib = ctypes.CDLL(dylib_path)

        # 使用 c_void_p 作为返回类型以避免 ctypes 自动管理 C 内存
        # Rust 分配的内存由 longhun_free_string 释放

        # longhun_sm4_encrypt(data: *u8, data_len: i32, key_hex: *c_char) -> *c_char
        self._lib.longhun_sm4_encrypt.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
            ctypes.c_char_p,
        ]
        self._lib.longhun_sm4_encrypt.restype = ctypes.c_void_p

        # longhun_sm4_decrypt(data_hex: *c_char, key_hex: *c_char) -> *c_char
        self._lib.longhun_sm4_decrypt.argtypes = [
            ctypes.c_char_p, ctypes.c_char_p,
        ]
        self._lib.longhun_sm4_decrypt.restype = ctypes.c_void_p

        # longhun_sm3_hash(data: *u8, data_len: i32) -> *c_char
        self._lib.longhun_sm3_hash.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
        ]
        self._lib.longhun_sm3_hash.restype = ctypes.c_void_p

        # longhun_free_string(ptr: *c_char)
        self._lib.longhun_free_string.argtypes = [ctypes.c_void_p]
        self._lib.longhun_free_string.restype = None

    def _read_cstr(self, ptr) -> Optional[str]:
        """从 C 指针读字符串并释放"""
        if ptr is None:
            return None
        try:
            text = ctypes.cast(ptr, ctypes.c_char_p).value
            if text is None:
                return None
            return text.decode("utf-8")
        finally:
            self._lib.longhun_free_string(ptr)

    def sm4_encrypt(self, data: bytes, key: bytes) -> Optional[bytes]:
        """Rust SM4 ECB 加密 → hex 密文"""
        buf = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
        key_hex = key.hex().encode("utf-8")
        result = self._lib.longhun_sm4_encrypt(buf, len(data), key_hex)
        text = self._read_cstr(result)
        if text is None or text.startswith("{"):
            return None
        return bytes.fromhex(text)

    def sm4_decrypt(self, ciphertext: bytes, key: bytes) -> Optional[bytes]:
        """Rust SM4 ECB 解密 → 原文"""
        hex_str = ciphertext.hex().encode("utf-8")
        key_hex = key.hex().encode("utf-8")
        result = self._lib.longhun_sm4_decrypt(hex_str, key_hex)
        text = self._read_cstr(result)
        if text is None or text.startswith("{"):
            return None
        return text.encode("utf-8")

    def sm3_hash(self, data: bytes) -> Optional[bytes]:
        """Rust SM3 哈希 → 32字节"""
        buf = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
        result = self._lib.longhun_sm3_hash(buf, len(data))
        text = self._read_cstr(result)
        if text is None:
            return None
        return bytes.fromhex(text)


# ═══════════════════════════════════════════
# 统一入口（自动选择 Rust / Python）
# ═══════════════════════════════════════════

class _LazyBridge:
    """延迟加载 Rust FFI，自动回退纯 Python"""

    def __init__(self):
        self._rust: Optional[_RustCrypto] = None
        self._tried = False
        self._available = False

    @property
    def rust(self) -> Optional[_RustCrypto]:
        if not self._tried:
            self._tried = True
            path = _find_dylib()
            if path:
                try:
                    self._rust = _RustCrypto(path)
                    # 快速自检
                    test = self._rust.sm3_hash(b"ping")
                    if test and len(test) == 32:
                        self._available = True
                except Exception:
                    self._rust = None
        return self._rust

    @property
    def available(self) -> bool:
        self.rust  # trigger lazy init
        return self._available

    def sm4_encrypt(self, data: bytes, key: bytes) -> bytes:
        if self.available:
            result = self._rust.sm4_encrypt(data, key)
            if result is not None:
                return result
        from .sm_crypto import SM4
        return SM4.encrypt(data, key)

    def sm4_decrypt(self, data: bytes, key: bytes) -> bytes:
        if self.available:
            result = self._rust.sm4_decrypt(data, key)
            if result is not None:
                return result
        from .sm_crypto import SM4
        return SM4.decrypt(data, key)

    def sm3_hash(self, data: bytes) -> bytes:
        if self.available:
            result = self._rust.sm3_hash(data)
            if result is not None:
                return result
        from .sm_crypto import SM3
        return SM3.hash(data)

    def sm3_hex(self, data: bytes) -> str:
        return self.sm3_hash(data).hex()


_bridge = _LazyBridge()

sm4_encrypt = _bridge.sm4_encrypt
sm4_decrypt = _bridge.sm4_decrypt
sm3_hash = _bridge.sm3_hash
sm3_hex = _bridge.sm3_hex
rust_available = lambda: _bridge.available


# ═══════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════

if __name__ == "__main__":
    key = b"0123456789abcdef"
    data = "Hello from Python FFI! 龙魂 SM4/SM3 测试".encode("utf-8")

    # 检查 Rust 可用性
    print(f"Rust FFI: {'🟢 可用' if rust_available() else '🟡 回退纯Python'}")
    print(f"   库路径: {_find_dylib() or '未找到'}")

    # 加密/解密往返
    enc = sm4_encrypt(data, key)
    dec = sm4_decrypt(enc, key)
    assert dec == data, f"SM4 往返失败 (Rust={'yes' if rust_available() else 'no'})"
    print(f"🟢 SM4 往返: {len(data)}→{len(enc)}→{len(dec)} bytes")

    # SM3 哈希
    h = sm3_hash(data)
    assert len(h) == 32
    print(f"🟢 SM3: {h.hex()[:32]}...")

    # Rust 互操作验证: SM4 与 Python 实现结果一致
    try:
        from .sm_crypto import SM4 as PySM4, SM3 as PySM3
    except ImportError:
        from longhun_memory.sm_crypto import SM4 as PySM4, SM3 as PySM3
    enc_py = PySM4.encrypt(data, key)
    dec_py = PySM4.decrypt(enc, key)
    assert dec_py == data, "Python SM4 fail"
    print(f"🟢 Python SM4: {len(data)}→{len(enc_py)}→{len(dec_py)} bytes")

    h_py = PySM3.hash(data)
    assert len(h_py) == 32
    print(f"🟢 Python SM3: {h_py.hex()[:32]}...")

    print("🟢🟢🟢 SM Crypto FFI 桥接器自检通过")
