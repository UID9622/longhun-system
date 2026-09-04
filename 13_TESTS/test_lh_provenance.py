#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-TEST_LH_PROVENANCE-42472382
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·逻辑溯源引擎 单元测试（锚点断言）
License: MulanPSL v2
创建者: 诸葛鑫（UID9622）
覆盖: DNA格式 · 确认码闸门(含emoji) · SHA-256校验 · 持久化SQLite+JSON双轨
      引擎注入 · 篡改检测 · 统计 · GPG签名验证
"""
import sys
import os
import json
import unittest
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))

from lh_provenance import (  # noqa: E402
    LogicalProvenanceEngine, SecurityLayer, PersistenceLayer, CONFIRM_CODE,
)


class TestLogicalProvenance(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_dna_format(self):
        """DNA必须符合lh_dna_generator系统标准：龍芯+干支四柱+卦+分隔符"""
        from lh_provenance import make_dna
        dna = make_dna("TEST")
        self.assertIn("龍芯", dna)
        self.assertIn("·", dna)
        self.assertIn("⚡️", dna)
        self.assertIn("ENGINE", dna)

    def test_confirm_code_emoji_safe(self):
        """确认码闸门必须严格匹配（含emoji🌌非ASCII·回归hmac bug）"""
        s = SecurityLayer()
        self.assertTrue(s.verify_confirm_code(CONFIRM_CODE))
        self.assertFalse(s.verify_confirm_code("wrong"))
        self.assertFalse(s.verify_confirm_code(""))
        self.assertFalse(s.verify_confirm_code(CONFIRM_CODE + "x"))

    def test_checksum_sha256(self):
        """SHA-256校验和可计算可验证"""
        s = SecurityLayer()
        content = "test content"
        checksum = s.compute_checksum(content)
        self.assertEqual(len(checksum), 64)
        self.assertTrue(s.verify_checksum(content, checksum))
        self.assertFalse(s.verify_checksum(content, "x" * 64))

    def test_persistence_sqlite_roundtrip(self):
        """SQLite持久化存→取"""
        p = PersistenceLayer(Path(self.tmp))
        record = {"module": "TEST", "dna": "#TEST", "timestamp": "2026-01-01",
                  "checksum": "abc", "content": "{}", "status": "🟢"}
        p.save(record)
        history = p.load_by_module("TEST")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["module"], "TEST")

    def test_persistence_json_dual_track(self):
        """JSON双轨文件必须落盘（供GPG分离签名）"""
        p = PersistenceLayer(Path(self.tmp))
        record = {"module": "TEST双轨", "dna": "#T", "timestamp": "2026-01-01",
                  "checksum": "abc", "content": "{}", "status": "🟢"}
        path = p.save(record)
        self.assertTrue(path.exists())
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["module"], "TEST双轨")

    def test_engine_inject_gate(self):
        """引擎注入必须验证确认码：错误拒·正确过"""
        e = LogicalProvenanceEngine(self.tmp)
        bad = e.inject("三色审计引擎", confirm_code="wrong")
        self.assertIn("error", bad)
        self.assertEqual(bad["status"], "🔴")
        ok = e.inject("三色审计引擎", confirm_code=CONFIRM_CODE)
        self.assertNotIn("error", ok)
        self.assertEqual(ok["status"], "🟢")
        self.assertTrue(ok["checksum"])

    def test_verify_tamper_detect(self):
        """校验和必须能检测篡改：错误期望值必拒"""
        e = LogicalProvenanceEngine(self.tmp)
        e.inject("DNA追溯链", confirm_code=CONFIRM_CODE)
        v1 = e.verify("DNA追溯链")
        self.assertTrue(v1["verified"])
        # 外部期望校验和不匹配 → 必须失败
        v2 = e.verify("DNA追溯链", expected_checksum="f" * 64)
        self.assertFalse(v2["verified"])
        self.assertEqual(v2["status"], "🔴")

    def test_stats(self):
        """统计信息完整"""
        e = LogicalProvenanceEngine(self.tmp)
        e.inject("主权网关", confirm_code=CONFIRM_CODE)
        s = e.get_stats()
        self.assertGreaterEqual(s["registered_modules"], 6)
        self.assertGreaterEqual(s["persistence"]["total_records"], 1)
        self.assertIn("engine_dna", s)
        self.assertIn("gpg_engine", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
