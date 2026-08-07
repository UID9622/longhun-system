#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-06-MEMORY-VAULT-v2.0-CNSH-PIPELINE
# License: MulanPSL v2
"""
MemoryVault · 记忆保险库 v2.0
═══════════════════════════════
核心 API：压缩·CNSH文本化·SM4加密·SM3哈希链·DNA追溯

v2.0 新 pipeline (CNSH 作为通用流通格式):
  seal:  JSON对话 → 智能压缩 → 🔥CNSH文本 → SM4加密 → SM3哈希链 → DNA标记 → 密文块
  unseal: 密文块 → DNA验证 → SM3链校验 → SM4解密 → 🔥CNSH原文 + 🔥JSON双输出

CNSH 是数据流通的通用格式——longhun-memory / longhun-save / 鸿蒙插件 说同一种话。
DNA 是追溯凭证。三色审计是状态语言。

兼容性: 旧版 (v1 JSON-only) .lhm 文件仍可解析 (自动降级)。
"""

import json
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any, Union, Tuple

from .sm_crypto import SM3, SM4, SM3HashChain
from .dna import DNA, dna_now
from .compressor import MemoryCompressor, compression_stats
from .audit import AuditMark, ThreeColorAudit, AuditColor
from .cnsh_text import json_to_cnsh, cnsh_to_json, is_cnsh_text, detect_format


# ════════════════════════════════════════════════════
# 数据结构
# ════════════════════════════════════════════════════

@dataclass
class UnsealResult:
    """解密结果 · 🔥 CNSH + JSON 双输出"""
    ok: bool = False
    data: Optional[List[Dict[str, str]]] = None   # JSON 对话数据
    cnsh_text: str = ""                            # 🔥 CNSH 文本（通用数据流通格式）
    dna: str = ""
    tampered: bool = False
    chain_ok: bool = True
    audit: Optional[AuditMark] = None
    error: str = ""
    stats: Optional[dict] = None
    metadata: Optional[dict] = None                # CNSH 元数据

    def __repr__(self):
        if not self.ok:
            return f"UnsealResult(🔴 失败: {self.error})"
        if self.tampered:
            return f"UnsealResult(🔴 数据被篡改!)"
        msg_count = len(self.data) if self.data else 0
        cnsh_flag = " [CNSH]" if self.cnsh_text else ""
        return f"UnsealResult(🟢 OK, {msg_count}条消息{cnsh_flag}, {self.audit.emoji if self.audit else '?'})"

    def to_cnsh_file(self, path: str) -> None:
        """将 CNSH 文本写入文件"""
        if not self.cnsh_text:
            raise ValueError("无 CNSH 文本数据")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.cnsh_text)

    def to_json_file(self, path: str) -> None:
        """将 JSON 数据写入文件"""
        if not self.data:
            raise ValueError("无 JSON 数据")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════════════
# MemoryVault v2.0 — CNSH 管道
# ════════════════════════════════════════════════════

class MemoryVault:
    """記憶保險庫 · 压缩·CNSH·加密全链路

    用法:
        vault = MemoryVault(key="your-master-password-1234")

        # seal: JSON → CNSH → 压缩 → SM4
        blob = vault.seal(messages, strategy="smart")

        # unseal: 解密 → CNSH文本 + JSON双输出
        result = vault.unseal(blob)
        if result.ok:
            print(result.cnsh_text)      # 🔥 CNSH 人类可读
            for msg in result.data:       # 🔥 JSON 机器可读
                ...
    """

    MAGIC_V2 = b"\x89LH\x02M"   # 龍魂记忆 v2 魔数 (CNSH 格式)
    MAGIC_V1 = b"\x89LH\x00M"   # 龍魂记忆 v1 魔数 (JSON 格式，兼容)
    VERSION = 2

    def __init__(self, key: Union[str, bytes] = None, keep_recent: int = 5):
        self._sm4_key = self._derive_key(key if key else "longhun-default-key")
        self._chain = SM3HashChain()
        self._compressor = MemoryCompressor(keep_recent=keep_recent)
        self._history: List[str] = []

    @staticmethod
    def _derive_key(key: Union[str, bytes]) -> bytes:
        if isinstance(key, str):
            key = key.encode("utf-8")
        return SM3.hash(key + b":longhun-memory-sm4-key")[:16]

    # ═══════════════════════════════════════════════
    # seal: JSON → CNSH → SM4 → 打包
    # ═══════════════════════════════════════════════

    def seal(self, messages: List[Dict[str, str]],
             strategy: str = "smart",
             format: str = "cnsh",
             keywords: Optional[List[str]] = None) -> bytes:
        """封存对话记忆

        Args:
            messages: 对话列表
            strategy: 'smart' | 'recent' | 'summarize' | 'none'
            format: 'cnsh' (v2默认) | 'json' (v1兼容)
            keywords: 手动指定关键词

        Returns:
            加密字节流 (.lhm)
        """
        dna = DNA.create("MEMORY", "SEAL")
        self._history.append(dna.full)

        # Step 1: 智能压缩
        compressed = self._compressor.compress(messages, strategy)
        comp_stats = compression_stats(messages, compressed)

        # Step 2: 🔥 转换为 CNSH 文本 或保持 JSON
        if format == "cnsh":
            cnsh_text = json_to_cnsh(compressed, dna=dna.full,
                                     audit="🟢", keywords=keywords)
            payload = cnsh_text.encode("utf-8")
            is_cnsh_flag = 1  # 标记为 CNSH 格式
        else:
            payload = json.dumps(compressed, ensure_ascii=False).encode("utf-8")
            is_cnsh_flag = 0

        # Step 3: SM4 加密
        ciphertext = SM4.encrypt(payload, self._sm4_key)

        # Step 4: SM3 哈希链
        chain_data = json.dumps({
            "dna": dna.full, "msg_count": len(messages),
            "comp_msg_count": len(compressed),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "strategy": strategy, "format": format,
            "comp_stats": comp_stats,
        }, ensure_ascii=False)
        self._chain.add(f"seal-{dna.hash8}", chain_data)

        # Step 5: 三色审计
        audit = ThreeColorAudit.audit_seal(
            key_len=len(self._sm4_key), data_size=len(payload), dna=dna.full
        )

        # Step 6: 打包
        blob = self._pack(dna.full, ciphertext, audit, comp_stats, is_cnsh_flag)
        return blob

    # ═══════════════════════════════════════════════
    # unseal: 解密 → CNSH + JSON 双输出
    # ═══════════════════════════════════════════════

    def unseal(self, blob: bytes) -> UnsealResult:
        """解封 → 🔥 CNSH文本 + JSON 双输出"""
        # 自动检测格式
        is_v2 = blob[:5] == self.MAGIC_V2
        is_v1 = blob[:5] == self.MAGIC_V1
        if not is_v2 and not is_v1:
            return UnsealResult(ok=False, error="无效的龍魂记忆格式（魔数错误）")

        try:
            if is_v2:
                dna_str, ciphertext, stored_hash, stored_audit, is_cnsh_flag = self._unpack_v2(blob)
            else:
                dna_str, ciphertext, stored_hash, stored_audit = self._unpack_v1(blob)
                is_cnsh_flag = 0  # v1 永远 JSON
        except Exception as e:
            return UnsealResult(ok=False, error=f"解包失败: {e}")

        # DNA 验证
        parsed_dna = DNA.parse(dna_str)
        dna_valid = parsed_dna is not None

        # 完整性校验
        data_hash = SM3.hex(ciphertext)
        tampered = (data_hash != stored_hash)

        # SM4 解密
        try:
            plaintext = SM4.decrypt(ciphertext, self._sm4_key)
        except Exception as e:
            return UnsealResult(
                ok=False, dna=dna_str, tampered=True,
                error=f"解密失败（密钥错误或数据损坏）: {e}"
            )

        # 🔥 双输出: 根据格式标记分别解析
        messages: List[Dict] = []
        cnsh_text: str = ""
        metadata: Optional[dict] = None

        if is_cnsh_flag:
            # CNSH 格式 → 双输出
            try:
                cnsh_text = plaintext.decode("utf-8")
            except UnicodeDecodeError:
                return UnsealResult(ok=False, dna=dna_str, tampered=True,
                                    error="CNSH文本解码失败（数据损坏或密钥错误）")
            try:
                messages, metadata = cnsh_to_json(cnsh_text)
            except Exception:
                # CNSH 解析失败：CN text 有但 JSON 为空
                messages = []
        else:
            # JSON 格式 (v1 兼容) → 只 JSON, 可选转 CNSH
            try:
                json_text = plaintext.decode("utf-8")
                messages = json.loads(json_text)
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                return UnsealResult(ok=False, dna=dna_str, tampered=True,
                                    error=f"JSON解析失败（数据损坏或密钥错误）: {e}")
            # 向后兼容: 也生成 CNSH 文本
            try:
                cnsh_text = json_to_cnsh(messages, dna=dna_str)
            except Exception:
                pass

        # 哈希链
        chain_ok, _ = self._chain.verify()

        # 审计
        audit = ThreeColorAudit.audit_unseal(
            chain_ok=chain_ok, tampered=tampered,
            dna_valid=dna_valid, dna=dna_str,
        )

        ok = not tampered and dna_valid and chain_ok

        return UnsealResult(
            ok=ok,
            data=messages if messages else None,
            cnsh_text=cnsh_text,
            dna=dna_str,
            tampered=tampered,
            chain_ok=chain_ok,
            audit=audit,
            metadata=metadata,
        )

    # ═══════════════════════════════════════════════
    # 打包/解包 v2 (CNSH-aware)
    # ═══════════════════════════════════════════════

    def _pack(self, dna: str, ciphertext: bytes, audit: AuditMark,
              comp_stats: Optional[dict], is_cnsh: int = 1) -> bytes:
        """v2 打包格式:
        MAGIC(5) + version(1) + format_flag(1) + dna_len(1) + dna(N) +
        data_hash(32) + audit_json_len(2) + audit_json(N) +
        comp_json_len(2) + comp_json(N) + ciphertext(N)
        """
        dna_bytes = dna.encode("utf-8")
        data_hash = SM3.hash(ciphertext)
        audit_json = json.dumps(audit.to_dict(), ensure_ascii=False).encode("utf-8")
        comp_json = json.dumps(comp_stats or {}, ensure_ascii=False).encode("utf-8")

        blob = bytearray()
        blob.extend(self.MAGIC_V2)
        blob.append(self.VERSION)
        blob.append(is_cnsh & 0xFF)             # 🔥 CNSH 格式标记
        blob.append(min(len(dna_bytes), 255))
        blob.extend(dna_bytes[:255])
        blob.extend(data_hash)
        blob.extend(struct.pack(">H", len(audit_json)))
        blob.extend(audit_json)
        blob.extend(struct.pack(">H", len(comp_json)))
        blob.extend(comp_json)
        blob.extend(ciphertext)
        return bytes(blob)

    def _unpack_v2(self, blob: bytes) -> Tuple[str, bytes, str, dict, int]:
        """解包 v2"""
        pos = 5  # skip MAGIC
        version = blob[pos]; pos += 1
        if version != 2:
            raise ValueError(f"不支持的版本: {version}")
        is_cnsh = blob[pos]; pos += 1
        dna_len = blob[pos]; pos += 1
        dna = blob[pos:pos + dna_len].decode("utf-8"); pos += dna_len
        stored_hash = blob[pos:pos + 32].hex(); pos += 32
        audit_len = struct.unpack(">H", blob[pos:pos + 2])[0]; pos += 2
        audit_json = json.loads(blob[pos:pos + audit_len].decode("utf-8")); pos += audit_len
        try:
            comp_len = struct.unpack(">H", blob[pos:pos + 2])[0]; pos += 2
            _ = json.loads(blob[pos:pos + comp_len].decode("utf-8")); pos += comp_len
        except Exception:
            pass
        ciphertext = blob[pos:]
        return dna, ciphertext, stored_hash, audit_json, is_cnsh

    def _unpack_v1(self, blob: bytes) -> Tuple[str, bytes, str, dict]:
        """解包 v1 (向后兼容)"""
        pos = 5
        version = blob[pos]; pos += 1
        if version != 1:
            raise ValueError(f"不支持的版本: {version}")
        dna_len = blob[pos]; pos += 1
        dna = blob[pos:pos + dna_len].decode("utf-8"); pos += dna_len
        stored_hash = blob[pos:pos + 32].hex(); pos += 32
        audit_len = struct.unpack(">H", blob[pos:pos + 2])[0]; pos += 2
        audit_json = json.loads(blob[pos:pos + audit_len].decode("utf-8")); pos += audit_len
        try:
            comp_len = struct.unpack(">H", blob[pos:pos + 2])[0]; pos += 2
            _ = json.loads(blob[pos:pos + comp_len].decode("utf-8")); pos += comp_len
        except Exception:
            pass
        ciphertext = blob[pos:]
        return dna, ciphertext, stored_hash, audit_json

    # ═══════════════════════════════════════════════
    # 工具
    # ═══════════════════════════════════════════════

    @property
    def history(self) -> List[str]:
        return list(self._history)

    @property
    def chain_last_hash(self) -> str:
        return self._chain.last_hash()

    def chain_verify(self) -> bool:
        ok, _ = self._chain.verify()
        return ok

    def to_chain_json(self) -> str:
        return json.dumps(self._chain.to_list(), ensure_ascii=False, indent=2)

    def stat(self) -> dict:
        return {
            "total_seals": len(self._history),
            "chain_length": len(self._chain.chain),
            "chain_ok": self.chain_verify(),
            "last_hash": self.chain_last_hash,
            "last_dna": self._history[-1] if self._history else None,
            "version": 2,
            "format": "cnsh",
        }


# ════════════════════════════════════════════════════
# 自检
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "你好，帮我记住：项目代号'龙魂'"},
        {"role": "assistant", "content": "已记住：项目代号'龙魂'"},
        {"role": "user", "content": "目标是保护数据主权"},
        {"role": "assistant", "content": "了解：目标是保护数据主权"},
        {"role": "user", "content": "技术栈是 Python + SM4 加密"},
        {"role": "assistant", "content": "记录完毕"},
    ]

    vault = MemoryVault(key="test-password-123456")

    # ──── CNSH 格式 seal/unseal ────
    blob = vault.seal(messages, strategy="smart", format="cnsh")
    print(f"🔒 CNSH Seal: {len(blob)} 字节")

    result = vault.unseal(blob)
    print(f"🔓 Unseal: {result}")
    assert result.ok, "CNSH unseal 失败"
    assert result.cnsh_text, "CNSH 文本为空!"
    assert result.data and len(result.data) >= 1, "JSON数据为空!"
    print(f"  DNA: {result.dna}")
    print(f"  审计: {result.audit}")
    print(f"  消息数: {len(result.data)}")
    print(f"  CNSH 文本前80字: {result.cnsh_text[:80]}...")
    print("🟢 CNSH 双输出通过")

    # ──── 篡改检测 ────
    tampered_blob = bytearray(blob)
    tampered_blob[-10] ^= 0xFF
    result2 = vault.unseal(bytes(tampered_blob))
    print(f"篡改检测: {result2}")
    assert not result2.ok or result2.tampered or "损坏" in result2.error, \
        "篡改应被检测"
    print("🟢 篡改检测通过")

    # ──── 错误密码拒绝 ────
    vault2 = MemoryVault(key="wrong-password")
    result3 = vault2.unseal(blob)
    print(f"错密码: {result3}")
    assert not result3.ok, "错误密码应拒绝"
    print("🟢 错误密码拒绝通过")

    # ──── JSON 格式向后兼容 ────
    blob_json = vault.seal(messages, strategy="smart", format="json")
    result4 = vault.unseal(blob_json)
    assert result4.ok and result4.data, "JSON 兼容模式失败"
    print(f"🟢 JSON 兼容模式: {len(result4.data)} 条消息")

    print(f"\n统计: {json.dumps(vault.stat(), ensure_ascii=False, indent=2)}")
    print("🟢🟢🟢 MemoryVault v2.0 CNSH管道全链路自检通过!")
