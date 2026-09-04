#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·辰时·䷓观-TEST-SANCAI-DNA-COMPRESS-v2.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 三才DNA无损压缩与内容指纹溯源框架 · 单元测试 v2.0
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08_BIN"))

from lh_sancai_dna_compress import (
    SancaiDNAEngine,
    SancaiExtractor,
    DNAChain,
    DNANode,
    HEADER_SIZE,
    MAGIC,
    main,
)


class TestSancaiExtractor(unittest.TestCase):
    def test_extract_tian(self):
        data = "龍魂系统三才DNA无损压缩算法测试".encode("utf-8")
        feat = SancaiExtractor().extract_tian(data)
        self.assertIn("semantic_hash", feat)
        self.assertIn("entropy", feat)
        self.assertGreater(feat["word_count"], 0)

    def test_extract_di(self):
        data = "第一句。\n第二句。\n\n第三段第一句。".encode("utf-8")
        feat = SancaiExtractor().extract_di(data)
        self.assertEqual(feat["paragraph_count"], 2)
        self.assertEqual(feat["sentence_count"], 3)

    def test_extract_ren(self):
        data = "UID9622 行为主权测试数据".encode("utf-8")
        feat = SancaiExtractor().extract_ren(data)
        self.assertEqual(feat["author"], "UID9622")
        self.assertIn("content_hash", feat)


class TestDNAChain(unittest.TestCase):
    def test_chain_integrity(self):
        chain = DNAChain()
        for i in range(3):
            node = DNANode(
                version="2.0",
                author="UID9622",
                chunk_index=i,
                original_offset=i * 100,
                chunk_size=100,
                chunk_hash="a" * 32,
                tian_hash="b" * 16,
                di_hash="c" * 16,
                ren_hash="d" * 16,
            )
            chain.add(node)
        ok, msg = chain.verify()
        self.assertTrue(ok, msg)
        self.assertEqual(len(chain.nodes), 3)
        self.assertEqual(chain.nodes[0].parent_hash, "0" * 32)

    def test_chain_tamper_detected(self):
        chain = DNAChain()
        node = DNANode(
            version="2.0", author="UID9622", chunk_index=0,
            original_offset=0, chunk_size=10, chunk_hash="a" * 32,
            tian_hash="b" * 16, di_hash="c" * 16, ren_hash="d" * 16,
        )
        chain.add(node)
        chain.nodes[0].chunk_hash = "x" * 32
        ok, msg = chain.verify()
        self.assertFalse(ok)


class TestSancaiDNAEngineCompress(unittest.TestCase):
    def test_roundtrip_text(self):
        original = ("龍魂系统主权声明\n" * 100).encode("utf-8")
        engine = SancaiDNAEngine(level=6)
        compressed = engine.compress(original)
        decompressed = engine.decompress(compressed)
        self.assertEqual(original, decompressed)

    def test_roundtrip_binary(self):
        original = bytes(range(256)) * 50
        engine = SancaiDNAEngine()
        compressed = engine.compress(original)
        decompressed = engine.decompress(compressed)
        self.assertEqual(original, decompressed)

    def test_compression_ratio(self):
        original = b" repeating pattern " * 2000
        engine = SancaiDNAEngine(level=9)
        compressed = engine.compress(original)
        ratio = len(original) / len(compressed)
        self.assertGreater(ratio, 1.0, "压缩率应大于 1")

    def test_multichunk(self):
        original = b"A" * (512 * 1024 + 1234)
        engine = SancaiDNAEngine(chunk_size=256 * 1024)
        compressed = engine.compress(original)
        info = engine.package_info(compressed)
        self.assertGreater(info["chunk_count"], 1)
        decompressed = engine.decompress(compressed)
        self.assertEqual(original, decompressed)

    def test_parallel_compress(self):
        original = ("并行压缩测试数据 " * 5000).encode("utf-8")
        engine_parallel = SancaiDNAEngine(chunk_size=64 * 1024, jobs=4)
        compressed = engine_parallel.compress(original)
        decompressed = engine_parallel.decompress(compressed)
        self.assertEqual(original, decompressed)
        ok, msg, _ = engine_parallel.verify_package(compressed)
        self.assertTrue(ok, msg)

    def test_verify_package_valid(self):
        original = ("验证测试数据" * 100).encode("utf-8")
        engine = SancaiDNAEngine()
        compressed = engine.compress(original)
        ok, msg, _ = engine.verify_package(compressed)
        self.assertTrue(ok, msg)

    def test_verify_package_corrupted(self):
        original = ("损坏检测测试" * 100).encode("utf-8")
        engine = SancaiDNAEngine()
        compressed = bytearray(engine.compress(original))
        compressed[-1] ^= 0xFF
        ok, msg, _ = engine.verify_package(bytes(compressed))
        self.assertFalse(ok)

    def test_package_info_contains_sovereignty(self):
        original = ("主权锚定测试").encode("utf-8")
        engine = SancaiDNAEngine()
        compressed = engine.compress(original)
        info = engine.package_info(compressed)
        self.assertIn("DNA", info["dna"])
        self.assertEqual(info["tricolor"], "🟢")
        self.assertIn("9622", info["dna"])


class TestSancaiDNAEngineFingerprint(unittest.TestCase):
    def test_fingerprint_and_verify(self):
        data = ("文档完整性验证测试" * 50).encode("utf-8")
        engine = SancaiDNAEngine()
        fp = engine.fingerprint(data, author="UID9622")
        self.assertIn("fingerprint", fp)
        self.assertIn("chain", fp)
        ok, result = engine.verify_fingerprint(data, fp)
        self.assertTrue(ok)
        self.assertEqual(result["tricolor"], "🟢")

    def test_fingerprint_tamper_detected(self):
        data = ("原始内容" * 20).encode("utf-8")
        engine = SancaiDNAEngine()
        fp = engine.fingerprint(data)
        ok, result = engine.verify_fingerprint(data + b"x", fp)
        self.assertFalse(ok)
        self.assertEqual(result["tricolor"], "🔴")

    def test_audit_pass(self):
        data = ("龍魂系统三才DNA内容指纹溯源框架支持文档完整性验证、代码审计与数据流水线监控。\n" * 20).encode("utf-8")
        engine = SancaiDNAEngine()
        fp = engine.fingerprint(data)
        report = engine.audit(data, fp)
        self.assertEqual(report["tricolor"], "🟢")
        self.assertGreaterEqual(report["score"], 85)

    def test_chain_verify_from_fingerprint(self):
        data = ("签章链测试" * 20).encode("utf-8")
        engine = SancaiDNAEngine()
        fp = engine.fingerprint(data)
        chain = engine.chain_from_fingerprint(fp)
        ok, msg = chain.verify()
        self.assertTrue(ok, msg)


class TestCLI(unittest.TestCase):
    def test_compress_decompress_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "input.txt"
            out = Path(tmp) / "input.txt.lhdc"
            restored = Path(tmp) / "restored.txt"
            src.write_bytes(b"CLI roundtrip test " * 200)

            rc = main(["-c", str(src), "-o", str(out)])
            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())

            rc = main(["-d", str(out), "-o", str(restored)])
            self.assertEqual(rc, 0)
            self.assertEqual(src.read_bytes(), restored.read_bytes())

            rc = main(["-v", str(out)])
            self.assertEqual(rc, 0)

    def test_fingerprint_verify_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "doc.txt"
            src.write_bytes(("文档完整性测试" * 50).encode("utf-8"))

            rc = main(["--fingerprint", str(src), "--author", "UID9622"])
            self.assertEqual(rc, 0)
            fp_path = src.with_suffix(src.suffix + ".fingerprint.json")
            self.assertTrue(fp_path.exists())

            rc = main(["--verify-file", str(src), "--fingerprint-file", str(fp_path)])
            self.assertEqual(rc, 0)

    def test_audit_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "audit.txt"
            src.write_bytes(("三色审计测试\n" * 30).encode("utf-8"))
            rc = main(["--fingerprint", str(src)])
            self.assertEqual(rc, 0)
            rc = main(["--audit", str(src)])
            self.assertEqual(rc, 0)

    def test_chain_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "chain.txt"
            src.write_bytes(("签章链测试" * 20).encode("utf-8"))
            chain_out = Path(tmp) / "chain.json"

            rc = main(["--chain", str(src), "--chain-out", str(chain_out)])
            self.assertEqual(rc, 0)
            self.assertTrue(chain_out.exists())

            rc = main(["--verify-chain", str(chain_out)])
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
