#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-SAVE-AUDIT-LOG-v1.0
# License: MulanPSL v2
"""
龍魂算力代理 · 审计日志引擎
══════════════════════════
每个请求注入 DNA 追溯 + 审计标记，审计日志用 SM4 加密存档为 .lhm。

与 longhun-memory 的集成:
  审计日志条目 → JSON序列化 → SM4加密 → .lhm 文件
  解封时可用 lh-memory unseal 解密查看
"""

import json
import os
import struct
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any


# ═══════════════════════════════════════════════
# SM4 轻量实现（与 longhun-memory 完全互操作·纯Python·无外部依赖）
# ═══════════════════════════════════════════════

class _SM4:
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

    @staticmethod
    def _rotl(x: int, n: int) -> int:
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    @classmethod
    def _tau(cls, a: int) -> int:
        b = 0
        for i in range(4):
            b |= cls.SBOX[(a >> (8 * (3 - i))) & 0xFF] << (8 * (3 - i))
        return b

    @classmethod
    def _l(cls, a: int) -> int:
        return a ^ cls._rotl(a, 2) ^ cls._rotl(a, 10) ^ cls._rotl(a, 18) ^ cls._rotl(a, 24)

    @classmethod
    def _lp(cls, a: int) -> int:
        return a ^ cls._rotl(a, 13) ^ cls._rotl(a, 23)

    @classmethod
    def _expand_key(cls, key: bytes) -> list:
        mk = [int.from_bytes(key[i:i+4], "big") for i in range(0, 16, 4)]
        k = [mk[i] ^ cls.FK[i] for i in range(4)]
        rk = []
        for i in range(32):
            k[i % 4] ^= cls._lp(cls._tau(
                k[(i+1)%4] ^ k[(i+2)%4] ^ k[(i+3)%4] ^ cls.CK[i]))
            rk.append(k[i % 4])
        return rk

    @classmethod
    def _crypt_block(cls, block: bytes, rk: list) -> bytes:
        x = [int.from_bytes(block[i:i+4], "big") for i in range(0, 16, 4)]
        for i in range(32):
            x.append(x[i] ^ cls._l(cls._tau(
                x[i+1] ^ x[i+2] ^ x[i+3] ^ rk[i])))
        return x[35].to_bytes(4, "big") + x[34].to_bytes(4, "big") + \
               x[33].to_bytes(4, "big") + x[32].to_bytes(4, "big")

    @classmethod
    def encrypt_ecb(cls, data: bytes, key: bytes) -> bytes:
        assert len(key) == 16, "密钥必须为16字节"
        rk = cls._expand_key(key)
        pad = 16 - len(data) % 16
        padded = data + bytes([pad] * pad)
        result = b""
        for i in range(0, len(padded), 16):
            result += cls._crypt_block(padded[i:i+16], rk)
        return result

    @classmethod
    def decrypt_ecb(cls, data: bytes, key: bytes) -> bytes:
        assert len(key) == 16, "密钥必须为16字节"
        rk = cls._expand_key(key)[::-1]
        result = b""
        for i in range(0, len(data), 16):
            result += cls._crypt_block(data[i:i+16], rk)
        pad = result[-1]
        if 0 < pad <= 16 and result[-pad:] == bytes([pad]*pad):
            return result[:-pad]
        raise ValueError("SM4 解密失败：padding 错误")


# ═══════════════════════════════════════════════
# DNA 生成
# ═══════════════════════════════════════════════

def _make_dna(action: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    sid = uuid.uuid4().hex[:8].upper()
    return f"#龍芯⚡️{ts}-PROXY-{action}-{sid}"


# ═══════════════════════════════════════════════
# 审计日志器
# ═══════════════════════════════════════════════

class AuditLogger:
    """代理审计日志器

    每个请求:
      请求头注入: X-LongHun-DNA
      响应头注入: X-LongHun-Audit: 🟢|🟡|🔴
      审计日志: ~/.longhun/proxy/audit/{日期}.lhm (SM4加密)

    用法:
        audit = AuditLogger(key="proxy-audit-key")
        dna = audit.begin_request(messages, model)
        # ... 处理请求 ...
        audit_header = audit.end_request(dna, resp, is_cached=False)
    """

    AUDIT_DIR = Path.home() / ".longhun" / "proxy" / "audit"
    AUDIT_KEY_SUFFIX = b":longhun-proxy-audit-sm4-key"

    def __init__(self, key: str = "longhun-proxy-default", enabled: bool = True):
        self._enabled = enabled
        self._key = self._derive_key(key.encode())
        self._pending: Dict[str, dict] = {}
        self.AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _derive_key(cls, raw: bytes) -> bytes:
        import hashlib
        h = hashlib.sha256()
        h.update(raw + cls.AUDIT_KEY_SUFFIX)
        return h.digest()[:16]

    def begin_request(self, messages: List[Dict], model: str,
                      temperature: float = 0.7) -> str:
        """请求开始 → 生成 DNA

        Returns: DNA 追溯码（注入 X-LongHun-DNA 头）
        """
        dna = _make_dna("REQUEST")
        self._pending[dna] = {
            "dna": dna,
            "ts_start": time.time(),
            "model": model,
            "msg_count": len(messages),
            "temperature": temperature,
            "preview": str(messages)[:200],
        }
        return dna

    def end_request(self, dna: str, response: dict,
                    is_cached: bool = False, is_local: bool = True,
                    latency_ms: float = 0, error: str = "") -> str:
        """请求结束 → 审计标记 + 写加密日志

        Returns: 审计字符串（注入 X-LongHun-Audit 响应头）
        """
        entry = self._pending.pop(dna, {"dna": dna, "ts_start": time.time()})
        elapsed = (time.time() - entry.get("ts_start", time.time())) * 1000

        if error:
            audit_emoji = "🔴"
            audit_label = f"RED: {error[:80]}"
        elif is_cached:
            audit_emoji = "🟢"
            audit_label = "GREEN: cache_hit"
        elif is_local:
            audit_emoji = "🟢"
            audit_label = "GREEN: local"
        else:
            audit_emoji = "🟡"
            audit_label = "YELLOW: cloud"

        log_entry = {
            "dna": dna,
            "ts": datetime.now(timezone.utc).isoformat(),
            "model": entry.get("model", "?"),
            "msgs": entry.get("msg_count", 0),
            "cached": is_cached,
            "local": is_local,
            "latency_ms": round(elapsed, 1),
            "audit": audit_emoji,
            "audit_label": audit_label,
            "error": error,
        }

        if self._enabled:
            self._write_log(log_entry)

        return f"{audit_emoji} {audit_label}"

    def _write_log(self, entry: dict) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = self.AUDIT_DIR / f"{today}.lhm"
        json_bytes = json.dumps(entry, ensure_ascii=False).encode("utf-8")
        cipher = _SM4.encrypt_ecb(json_bytes, self._key)
        with open(log_path, "ab") as f:
            f.write(struct.pack(">I", len(cipher)))
            f.write(cipher)

    def read_logs(self, date_str: str = None) -> List[dict]:
        ds = date_str or datetime.now().strftime("%Y-%m-%d")
        log_path = self.AUDIT_DIR / f"{ds}.lhm"
        if not log_path.exists():
            return []
        entries = []
        with open(log_path, "rb") as f:
            while True:
                lb = f.read(4)
                if not lb or len(lb) < 4:
                    break
                length = struct.unpack(">I", lb)[0]
                cb = f.read(length)
                if not cb:
                    break
                try:
                    plain = _SM4.decrypt_ecb(cb, self._key)
                    entries.append(json.loads(plain.decode("utf-8")))
                except Exception:
                    continue
        return entries

    def stat(self) -> dict:
        today = datetime.now().strftime("%Y-%m-%d")
        entries = self.read_logs(today)
        g = sum(1 for e in entries if "🟢" in e.get("audit", ""))
        y = sum(1 for e in entries if "🟡" in e.get("audit", ""))
        r = sum(1 for e in entries if "🔴" in e.get("audit", ""))
        cached = sum(1 for e in entries if e.get("cached"))
        local = sum(1 for e in entries if e.get("local"))
        return {
            "date": today,
            "total": len(entries),
            "audit": {"🟢": g, "🟡": y, "🔴": r},
            "cached": cached, "local": local,
            "cloud": len(entries) - local,
            "log_path": str(self.AUDIT_DIR),
        }


# ═══════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    key = b"test-key-1234567"
    data = "Hello, LongHun Audit! 龍魂审计日志SM4测试".encode()
    enc = _SM4.encrypt_ecb(data, key)
    dec = _SM4.decrypt_ecb(enc, key)
    assert dec == data, f"SM4 roundtrip fail"
    print(f"🟢 SM4: {len(data)}→{len(enc)}→{len(dec)} bytes")

    audit = AuditLogger(key="test-audit")
    dna = audit.begin_request([{"role":"user","content":"测试"}], model="qwen2.5")
    r = audit.end_request(dna, {}, is_cached=False, is_local=True, latency_ms=12.5)
    assert "🟢" in r, f"audit mark fail: {r}"
    print(f"🟢 审计标记: {r}  DNA: {dna}")

    logs = audit.read_logs()
    assert len(logs) >= 1, "log not written"
    print(f"🟢 日志: {len(logs)} 条")
    print(f"   统计: {audit.stat()}")
    print("🟢🟢🟢 审计日志引擎自检通过")
