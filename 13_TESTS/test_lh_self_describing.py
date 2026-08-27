#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·丙戌·壬辰·䷍大有-ADS-TESTS-v4.0-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·ADS v4.0 单元测试（6组锚点断言）
运行: python3 tests/test_lh_self_describing.py  (或 pytest tests/test_lh_self_describing.py)
"""
import os
import sys
import tempfile
import shutil
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bin"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lh_self_describing import (  # noqa: E402
    SelfDescribingSystem, PerceptionLayer, SecurityLayer, PersistenceLayer,
    VersionManager, EventBus, make_dna, CONFIRM_CODE,
)


class TestADSAnchor(unittest.TestCase):
    """6组锚点断言（文档第七章验收标准）"""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="ads_ut_")
        os.environ["LONGHUN_ADS_DATA_DIR"] = cls.tmp

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_01_perception_layer_sense(self):
        """感知层: 含 system/process/memory/cpu/disk"""
        p = PerceptionLayer()
        data = p.sense()
        for key in ("system", "process", "memory", "cpu", "disk"):
            self.assertIn(key, data, f"感知层缺 {key}")

    def test_02_dna_format(self):
        """DNA: rizhu 标准，含龍芯+UID9622"""
        dna = make_dna("TEST")
        self.assertIn("龍芯", dna)
        self.assertIn("UID9622", dna)
        self.assertIn("TEST", dna)

    def test_03_security_confirm_code(self):
        """安全层: 确认码闸门 + API鉴权"""
        s = SecurityLayer()
        self.assertTrue(s.verify_confirm_code(CONFIRM_CODE))
        self.assertFalse(s.verify_confirm_code("wrong"))
        s2 = SecurityLayer(api_key="test-key")
        self.assertTrue(s2.verify_api_key("test-key"))
        self.assertFalse(s2.verify_api_key("bad-key"))
        # 未配置密钥 → 默认放行（依赖确认码闸门）
        self.assertTrue(SecurityLayer().verify_api_key(""))

    def test_04_persistence_roundtrip(self):
        """持久化: SQLite+JSON双轨往返"""
        p = PersistenceLayer(self.tmp)
        p.save_record({"dna": "#TEST", "timestamp": "2026-01-01T00:00:00", "layers": {"L1": {}}, "status": "🟢"})
        hist = p.load_history(limit=1)
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["dna"], "#TEST")
        self.assertEqual(hist[0]["status"], "🟢")
        self.assertEqual(p.count(), 1)
        self.assertTrue(p.json_path.exists(), "JSON双轨文件应存在")

    def test_05_event_bus_and_version(self):
        """事件总线 + 版本快照/回滚"""
        bus = EventBus()
        got = []
        bus.subscribe("t.ev", lambda e: got.append(e.name))
        bus.emit("t.ev", {})
        self.assertEqual(got, ["t.ev"], "事件订阅未触发")
        vm = VersionManager(self.tmp)
        vid = vm.snapshot({"k": 42}, tag="ut")
        self.assertEqual(vm.rollback(vid), {"k": 42}, "快照回滚失败")

    def test_06_full_describe_flow(self):
        """全链路: describe 四层输出 + 闸门拒绝 + 六角色"""
        sys_ = SelfDescribingSystem()
        # 无确认码 → 403 拒绝
        denied = sys_.describe("x")
        self.assertEqual(denied.get("code"), 403, "无确认码应拒绝")
        # 正确确认码 → 四层齐全
        ok = sys_.describe("测试自描述", CONFIRM_CODE)
        self.assertEqual(ok.get("status"), "🟢")
        self.assertIn("L1感知", ok["layers"])
        self.assertIn("L2认知", ok["layers"])
        self.assertIn("L3元认知", ok["layers"])
        self.assertIn("L4自指", ok["layers"])
        # 六角色全部可用
        for fn in (sys_.introspect, sys_.historian, sys_.diagnose, sys_.boundary, sys_.evolve):
            r = fn(CONFIRM_CODE)
            self.assertNotEqual(r.get("code"), 403, f"{fn.__name__} 被闸门拒绝")
        # 持久化落库
        self.assertGreaterEqual(sys_.persistence.count(), 1, "描述记录未落库")


if __name__ == "__main__":
    unittest.main(verbosity=2)
