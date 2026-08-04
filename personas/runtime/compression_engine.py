#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

# DNA:#龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-FILE1-v1.0-1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂超强压缩引擎 · LongHun Compression Engine v1.0

支持多算法级联压缩 + 龍魂自定义字典压缩：
- zlib / gzip / bz2 / lzma / zstd（若已安装）
- 自定义字典替换（高频关键词 → 短标记）
- 重复行/重复模式去重
- 自动选择最优算法

用法:
    python3 compression_engine.py compress <file> --mode auto
    python3 compression_engine.py decompress <file>
    python3 compression_engine.py benchmark <file>
"""

import os
import sys
import json
import zlib
import gzip
import bz2
import lzma
import base64
import argparse
import hashlib
from pathlib import Path
from typing import Dict, Tuple, Optional, Any

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False


class 龍魂压缩引擎:
    DNA = "#龍芯⚡️2026-06-24-LONGHUN-COMPRESSION-ENGINE-v1.0"

    # 龍魂高频关键词字典（可扩展）
    LONGHUN_DICT = {
        "龍魂": "LH",
        "LongHun": "LH",
        "UID9622": "U9",
        "CNSH": "CN",
        "DNA": "D",
        "追溯": "Z",
        "压缩": "Y",
        "人格": "R",
        "模块": "M",
        "系统": "X",
        "状态": "S",
        "高峰期": "P",
        "三色": "3C",
        "红": "R",
        "黄": "Y",
        "绿": "G",
    }

    def __init__(self):
        self.methods = {
            "zlib": self._zlib,
            "gzip": self._gzip,
            "bz2": self._bz2,
            "lzma": self._lzma,
        }
        if HAS_ZSTD:
            self.methods["zstd"] = self._zstd

    def _zlib(self, data: bytes, decompress: bool = False) -> bytes:
        return zlib.decompress(data) if decompress else zlib.compress(data, level=9)

    def _gzip(self, data: bytes, decompress: bool = False) -> bytes:
        return gzip.decompress(data) if decompress else gzip.compress(data, compresslevel=9)

    def _bz2(self, data: bytes, decompress: bool = False) -> bytes:
        return bz2.decompress(data) if decompress else bz2.compress(data, compresslevel=9)

    def _lzma(self, data: bytes, decompress: bool = False) -> bytes:
        return lzma.decompress(data) if decompress else lzma.compress(data, preset=9)

    def _zstd(self, data: bytes, decompress: bool = False) -> bytes:
        if decompress:
            return zstd.ZstdDecompressor().decompress(data)
        return zstd.ZstdCompressor(level=22).compress(data)

    def 龍魂字典编码(self, text: str, reverse: bool = False) -> str:
        """用龍魂字典做短标记替换"""
        mapping = self.LONGHUN_DICT
        if reverse:
            # 按值长度降序，避免短值覆盖
            items = sorted(mapping.items(), key=lambda x: -len(x[1]))
            for full, short in items:
                text = text.replace(short, full)
        else:
            # 按关键词长度降序
            items = sorted(mapping.items(), key=lambda x: -len(x[0]))
            for full, short in items:
                text = text.replace(full, short)
        return text

    def 重复模式压缩(self, text: str) -> str:
        """简单重复行去重：连续相同行用 <N>x行内容 表示"""
        lines = text.splitlines()
        if not lines:
            return text
        out = []
        prev = lines[0]
        count = 1
        for line in lines[1:]:
            if line == prev:
                count += 1
            else:
                if count > 1:
                    out.append(f"<{count}x>{prev}")
                else:
                    out.append(prev)
                prev = line
                count = 1
        if count > 1:
            out.append(f"<{count}x>{prev}")
        else:
            out.append(prev)
        return "\n".join(out)

    def 重复模式解压(self, text: str) -> str:
        import re
        out = []
        for line in text.splitlines():
            m = re.match(r"^<(\d+)x>(.*)$", line)
            if m:
                out.extend([m.group(2)] * int(m.group(1)))
            else:
                out.append(line)
        return "\n".join(out)

    def 压缩(self, data: bytes, method: str = "auto", use_dict: bool = True, use_dedup: bool = True) -> Dict[str, Any]:
        """
        超强压缩：字典编码 → 重复去重 → 算法压缩 → base64 封装
        """
        original_size = len(data)
        meta = {
            "DNA": self.DNA,
            "original_size": original_size,
            "use_dict": use_dict,
            "use_dedup": use_dedup,
        }

        # 1. 字典编码（仅文本）
        text = data.decode("utf-8", errors="ignore")
        if use_dict:
            text = self.龍魂字典编码(text)

        # 2. 重复模式压缩
        if use_dedup:
            text = self.重复模式压缩(text)

        payload = text.encode("utf-8")
        meta["after_dict_dedup_size"] = len(payload)

        # 3. 选择算法
        if method == "auto":
            best_method, best_data = self._auto_compress(payload)
            meta["method"] = best_method
        else:
            if method not in self.methods:
                raise ValueError(f"不支持的压缩算法: {method}")
            best_data = self.methods[method](payload)
            meta["method"] = method

        meta["compressed_size"] = len(best_data)
        meta["ratio"] = round(len(best_data) / original_size, 4) if original_size else 0.0
        meta["saved"] = round(1 - meta["ratio"], 4)

        # 4. 封装
        package = {
            "meta": meta,
            "payload": base64.b64encode(best_data).decode("ascii"),
        }
        package_bytes = json.dumps(package, ensure_ascii=False).encode("utf-8")
        return {
            "package": package,
            "package_bytes": package_bytes,
            "meta": meta,
        }

    def _auto_compress(self, data: bytes) -> Tuple[str, bytes]:
        best_size = len(data)
        best_method = "raw"
        best_data = data
        for name, fn in self.methods.items():
            try:
                compressed = fn(data)
                if len(compressed) < best_size:
                    best_size = len(compressed)
                    best_method = name
                    best_data = compressed
            except Exception:
                continue
        return best_method, best_data

    def 解压(self, package: Dict[str, Any]) -> bytes:
        meta = package["meta"]
        payload = base64.b64decode(package["payload"])
        method = meta.get("method", "raw")

        if method == "raw":
            data = payload
        elif method in self.methods:
            data = self.methods[method](payload, decompress=True)
        else:
            raise ValueError(f"不支持的解压算法: {method}")

        text = data.decode("utf-8", errors="ignore")

        if meta.get("use_dedup"):
            text = self.重复模式解压(text)
        if meta.get("use_dict"):
            text = self.龍魂字典编码(text, reverse=True)

        return text.encode("utf-8")

    def 基准测试(self, data: bytes) -> Dict[str, Any]:
        results = {}
        for method in ["raw"] + list(self.methods.keys()) + ["auto"]:
            try:
                if method == "raw":
                    size = len(data)
                    ratio = 1.0
                else:
                    res = self.压缩(data, method=method)
                    size = res["meta"]["compressed_size"]
                    ratio = res["meta"]["ratio"]
                results[method] = {"size": size, "ratio": ratio}
            except Exception as e:
                results[method] = {"error": str(e)}
        return results


def main():
    parser = argparse.ArgumentParser(description="龍魂超强压缩引擎")
    parser.add_argument("action", choices=["compress", "decompress", "benchmark"])
    parser.add_argument("file", type=str)
    parser.add_argument("--method", "-m", default="auto", help="压缩算法: auto/zlib/gzip/bz2/lzma/zstd")
    parser.add_argument("--no-dict", action="store_true", help="不使用龍魂字典")
    parser.add_argument("--no-dedup", action="store_true", help="不去重")
    parser.add_argument("--output", "-o", type=str, default=None)
    args = parser.parse_args()

    engine = 龍魂压缩引擎()
    path = Path(args.file)
    data = path.read_bytes()

    if args.action == "compress":
        result = engine.压缩(data, method=args.method, use_dict=not args.no_dict, use_dedup=not args.no_dedup)
        meta = result["meta"]
        out_path = Path(args.output) if args.output else Path(str(path) + ".lhpack")
        out_path.write_bytes(result["package_bytes"])
        print(f"🗜️ 压缩完成: {meta['method']}")
        print(f"   原始: {meta['original_size']} bytes")
        print(f"   压缩后: {meta['compressed_size']} bytes")
        print(f"   压缩率: {meta['ratio']:.2%} (节省 {meta['saved']:.2%})")
        print(f"   输出: {out_path}")

    elif args.action == "decompress":
        package = json.loads(data.decode("utf-8"))
        restored = engine.解压(package)
        out_path = Path(args.output) if args.output else Path(str(path).replace(".lhpack", ".restored"))
        out_path.write_bytes(restored)
        print(f"📦 解压完成: {out_path}")

    elif args.action == "benchmark":
        results = engine.基准测试(data)
        print("\n📊 压缩基准测试")
        print("-" * 40)
        for method, info in results.items():
            if "error" in info:
                print(f"  {method:8s}: 错误 - {info['error']}")
            else:
                print(f"  {method:8s}: {info['size']:10d} bytes  ({info['ratio']:.2%})")


if __name__ == "__main__":
    main()
