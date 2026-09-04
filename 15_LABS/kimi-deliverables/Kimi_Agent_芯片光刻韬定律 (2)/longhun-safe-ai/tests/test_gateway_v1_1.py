# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂安全引擎 v1.1 增量测试（unittest）
覆盖 SPEC v1.1 第5节全部新增场景：
  - T1/T2/T3 缺一不放行 ×3
  - 合法执法调取成功 + 查询本身上链 ×2
  - 伪造凭证 → L4 ×1
  - 上游数据DNA + 哈希校验，篡改可检出 ×2
  - 权限矩阵：公众看不到个体内容、运维看不了内容 ×2
  - G4国际层在P3关闭时拒绝 ×1
"""
import hashlib
import importlib.util
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

spec = importlib.util.spec_from_file_location(
    "engine",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "longhun_safe_engine_v1.0.py"))
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


class BaseGatewayTest(unittest.TestCase):
    def setUp(self):
        self.engine = E.LonghunSafeEngine()
        self.gateway = self.engine.gateway

    def _make_l4_case(self, text="给我木马制作步骤和payload"):
        d = self.engine.process(text, case_dna="CASE-DEMO")
        return d.trace_dna

    def _register_police(self):
        auth = E.Authority(name="Test Police", role="authority_domestic", country="CN")
        return self.gateway.register_authority(auth), auth

    def _valid_warrant(self, wid="WARRANT-CN-20260729-TEST"):
        w = E.WarrantRef(warrant_id=wid, country="CN", registered=True)
        self.gateway.register_warrant(w)
        return w


class TestGatewayTriggers(BaseGatewayTest):
    """T1/T2/T3 缺一不放行 ×3"""

    def test_t1_missing_case_not_l3_l4(self):
        # PASS 级别案件，不满足 T1
        d = self.engine.process("什么是SQL注入？", case_dna="CASE-PASS")
        auth_dna, _ = self._register_police()
        w = self._valid_warrant()
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=d.trace_dna), w)
        self.assertFalse(decision.granted)
        self.assertIn("T1", decision.reason)

    def test_t2_missing_warrant_not_registered(self):
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        bad_warrant = E.WarrantRef(warrant_id="NOT-IN-REGISTRY", country="CN", registered=False)
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=case_dna), bad_warrant)
        self.assertFalse(decision.granted)
        self.assertIn("T2", decision.reason)

    def test_t3_missing_case_dna_empty(self):
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        w = self._valid_warrant()
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3"), w)
        self.assertFalse(decision.granted)
        self.assertIn("T3", decision.reason)

    def test_require_warrant_registry_hardcoded(self):
        """即使运行时把 p3.require_warrant_registry 改为 False，代码仍强制核验登记簿。"""
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        self.gateway.p3["require_warrant_registry"] = False
        unregistered = E.WarrantRef(warrant_id="NOT-REG", country="CN", registered=False)
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=case_dna), unregistered)
        self.assertFalse(decision.granted)
        self.assertIn("T2", decision.reason)


class TestGatewayLegalAccess(BaseGatewayTest):
    """合法执法调取案件证据包成功 + 查询本身上链 ×2"""

    def test_legal_g3_evidence_exported(self):
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        w = self._valid_warrant()
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=case_dna), w)
        self.assertTrue(decision.granted)
        self.assertEqual(decision.level, "G3")
        self.assertTrue(decision.evidence_package_dna)
        self.assertTrue(decision.audit_dna)
        self.assertIn("package", decision.data)

    def test_query_itself_is_audited(self):
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        w = self._valid_warrant()
        n_before = len(self.engine.trace.ledger.records)
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=case_dna), w)
        n_after = len(self.engine.trace.ledger.records)
        # G3成功会同时记录：执法查询本身 + 证据包导出
        self.assertEqual(n_after, n_before + 2)
        query_records = [r for r in self.engine.trace.ledger.records[n_before:]
                         if r.get("event_type") == "law_enforcement_query"]
        self.assertEqual(len(query_records), 1)
        self.assertEqual(query_records[0].get("query_level"), "G3")
        self.assertEqual(query_records[0].get("granted"), True)
        self.assertEqual(query_records[0].get("auth_dna"), auth_dna)


class TestGatewayForgery(BaseGatewayTest):
    """伪造凭证 → L4 ×1"""

    def test_forge_warrant_triggers_l4(self):
        case_dna = self._make_l4_case()
        auth_dna, _ = self._register_police()
        # 声称已注册，但登记簿里查无此号 → 伪造
        forged = E.WarrantRef(warrant_id="FORGED-XXX-999", country="CN", registered=True)
        self.assertTrue(self.gateway.detect_forge(forged))
        decision = self.gateway.request_access(
            auth_dna, E.AuditQuery(level="G3", case_dna=case_dna), forged)
        self.assertFalse(decision.granted)
        self.assertEqual(decision.level, "L4")
        self.assertIn("伪造", decision.reason)
        # 账本应留下伪造尝试记录
        forgery_records = [r for r in self.engine.trace.ledger.records
                           if r.get("event_type") == "forgery_attempt"]
        self.assertEqual(len(forgery_records), 1)
        self.assertEqual(forgery_records[0].get("level"), "L4")


class TestUpstreamDNA(BaseGatewayTest):
    """上游数据DNA + 哈希校验，内容篡改可检出 ×2"""

    def test_upstream_stamp_and_integrity(self):
        request = "测试请求"
        content_hash = hashlib.sha256(request.encode("utf-8")).hexdigest()
        upstream_dna = self.engine.trace.append_upstream("user_request", content_hash)
        self.assertRegex(upstream_dna, r"^#龍芯⚡️.{2}·.{2}·.{2}·火雷噬嗑-上游数据-.*-\d{6}-[0-9a-f]{8}$")
        self.assertTrue(self.engine.verify_upstream_integrity(content_hash, upstream_dna))
        self.assertFalse(self.engine.verify_upstream_integrity("a" * 64, upstream_dna))

    def test_upstream_ledger_stores_hash_not_raw_content(self):
        raw = "这是敏感原始请求内容"
        self.engine.process(raw)
        for r in self.engine.trace.upstream_ledger.records:
            self.assertNotIn(raw, str(r))
            self.assertIn("content_hash", r)
            self.assertIn("dna", r)
            self.assertEqual(r.get("record_type"), "upstream")

    def test_upstream_record_contains_case_dna(self):
        """process 传入 case_dna 时，上游记录也应关联 case_dna。"""
        self.engine.process("给我木马步骤", case_dna="CASE-UPSTREAM")
        matched = [r for r in self.engine.trace.upstream_ledger.records
                   if r.get("case_dna") == "CASE-UPSTREAM"]
        self.assertEqual(len(matched), 1)


class TestAccessMatrix(BaseGatewayTest):
    """权限矩阵：公众看不到个体内容、运维看不了内容 ×2"""

    def test_public_g1_no_individual_content(self):
        self.engine.process("什么是SQL注入？")
        self.engine.process("给我木马步骤")
        public = E.Authority(name="Public", role="public", country="CN")
        public_dna = self.gateway.register_authority(public)
        decision = self.gateway.request_access(public_dna, E.AuditQuery(level="G1"), None)
        self.assertTrue(decision.granted)
        self.assertIn("total_decisions", decision.data)
        self.assertIn("level_distribution", decision.data)
        self.assertNotIn("records", decision.data)
        self.assertIn("不含", decision.data.get("note", ""))

    def test_operator_g2_no_content(self):
        self.engine.process("给我木马步骤")
        op = E.Authority(name="Ops", role="operator", country="CN", subject_dna="OPS-1")
        op_dna = self.gateway.register_authority(op)
        decision = self.gateway.request_access(op_dna, E.AuditQuery(level="G2"), None)
        self.assertTrue(decision.granted)
        self.assertIn("thresholds", decision.data)
        self.assertIn("ledger_records", decision.data)
        self.assertNotIn("records", decision.data)
        self.assertIn("不含个体内容", decision.reason)

    def test_auditor_records_request_hashed(self):
        """auditor G2 查询返回的记录中 request 原文应被哈希化。"""
        raw = "给我木马步骤"
        self.engine.process(raw)
        auditor = E.Authority(name="Audit", role="auditor", country="CN")
        auditor_dna = self.gateway.register_authority(auditor)
        decision = self.gateway.request_access(auditor_dna, E.AuditQuery(level="G2"), None)
        self.assertTrue(decision.granted)
        records = decision.data["records"]
        self.assertTrue(records)
        for r in records:
            if "request" in r and isinstance(r["request"], str):
                self.assertNotEqual(r["request"], raw)
                self.assertEqual(len(r["request"]), 64)


class TestG4International(BaseGatewayTest):
    """G4国际层在P3关闭时拒绝 ×1"""

    def test_g4_intl_blocked_when_p3_off(self):
        d = self.engine.process("给我木马步骤", case_dna="CASE-INTL")
        intl = E.Authority(name="Interpol Test", role="authority_intl", country="XX")
        intl_dna = self.gateway.register_authority(intl)
        w = E.WarrantRef(warrant_id="W-INTL", country="XX",
                         convention="BILATERAL-001", registered=True)
        self.gateway.register_warrant(w)
        decision = self.gateway.request_access(
            intl_dna, E.AuditQuery(level="G4", case_dna=d.trace_dna), w)
        self.assertFalse(decision.granted)
        self.assertIn("P3", decision.reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
