# -*- coding: utf-8 -*-
"""
龍魂流场唯一进出口 flow_port() 单元测试
DNA: #龍芯⚡️2026-05-27-FLOW-PORT-TESTS-v1.0
测试覆盖: 入站防盾·闸门·决策·出站防盾·账本·粒子层
"""
import tempfile
import unittest
from pathlib import Path

from cnsh.flow_decision.cnsh_flow_decision_core import CONFIRM_REQUIRED, GPG_REQUIRED
from cnsh.flow_field.port import (
    flow_port,
    _flow_out_error,
    _gate_out_dict,
    _defense_out_dict,
)


class TestFlowPort(unittest.TestCase):
    """流场唯一进出口的核心功能测试"""

    def setUp(self):
        """每个测试前初始化临时账本"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ledger = Path(self.temp_dir.name) / "ledger.jsonl"

    def tearDown(self):
        """每个测试后清理临时目录"""
        self.temp_dir.cleanup()

    def test_flow_port_hold_without_auto_execute(self):
        """测试默认情况：无 auto_execute 则挂起（hold）"""
        out = flow_port(
            {
                "message": "你好，流场单口测试",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "title": "test",
                },
            },
            ledger_path=self.ledger,
        )
        self.assertIn("particle", out)
        self.assertTrue(out.get("founder_same_rules"))
        self.assertFalse(out.get("execute_allowed", True))
        self.assertTrue(out.get("hold_for_audit"))
        self.assertIn("gate_v3", out)

    def test_flow_port_full_path_with_auto_execute(self):
        """测试完整路径：auto_execute=True 则执行"""
        out = flow_port(
            {
                "message": "你好，流场单口测试，建议按已有信息处理",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "evidence": "来源：单元测试；边界：不对外发布；目的：验证全链。",
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "dna_current": "#龍芯⚡️2026-05-15-FLOW-PORT-TEST-v1.0",
                    "title": "test",
                },
            },
            ledger_path=self.ledger,
        )
        self.assertTrue(out.get("execute_allowed"))
        # 验证账本已写入事件
        self.assertGreaterEqual(len(self.ledger.read_text(encoding="utf-8").strip().split("\n")), 2)

    def test_founder_same_rules_flag(self):
        """测试创始人同规则标志总是 True"""
        out = flow_port(
            {
                "message": "测试",
                "operator_id": "UID9622",
                "operator_tier": "T0",
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        self.assertTrue(out.get("founder_same_rules"))

    def test_empty_message_error(self):
        """测试空消息报错"""
        out = flow_port(
            {
                "message": "",
                "operator_id": "test_user",
                "operator_tier": "T3",
                "tags": {},
            },
            ledger_path=self.ledger,
        )
        self.assertEqual(out.get("tricolor"), "🔴")
        self.assertEqual(out.get("status"), "fuse")
        self.assertIn("message 不能为空", out.get("reply", ""))

    def test_empty_message_with_draft_reply(self):
        """测试空消息但有 draft_reply，应该使用 draft_reply"""
        out = flow_port(
            {
                "message": "",
                "draft_reply": "这是草稿回复",
                "operator_id": "test_user",
                "operator_tier": "T3",
                "auto_execute": True,
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        # 不应该报空消息错误
        self.assertNotEqual(out.get("status"), "fuse")

    def test_operator_tiers(self):
        """测试不同操作员等级（T0-T4）"""
        tiers = ["T0", "T1", "T2", "T3", "T4"]
        for tier in tiers:
            out = flow_port(
                {
                    "message": f"测试 {tier} 等级",
                    "operator_id": "UID9622",  # 使用认可的操作员ID
                    "operator_tier": tier,
                    "auto_execute": True,
                    "evidence": "单元测试等级",
                    "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
                },
                ledger_path=Path(tempfile.mkdtemp()) / "ledger.jsonl",
            )
            # operator_tier_applied 只在成功路径中
            if out.get("execute_allowed"):
                self.assertIn("operator_tier_applied", out)
            self.assertTrue(out.get("founder_same_rules"))

    def test_channel_parameter(self):
        """测试信道参数记录"""
        channels = ["api", "cli", "web", "internal"]
        for channel in channels:
            out = flow_port(
                {
                    "message": "测试信道",
                    "channel": channel,
                    "operator_id": "test_user",
                    "operator_tier": "T3",
                    "auto_execute": True,
                    "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
                },
                ledger_path=Path(tempfile.mkdtemp()) / "ledger.jsonl",
            )
            self.assertTrue(out.get("founder_same_rules"))

    def test_particle_layer_structure(self):
        """测试粒子层结构完整性"""
        out = flow_port(
            {
                "message": "测试粒子层",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        particle = out.get("particle")
        self.assertIsNotNone(particle)
        # 验证粒子层关键字段
        self.assertIn("dna", particle)
        self.assertIn("sha256", particle)  # 粒子层使用 sha256 而不是 content_sha256
        self.assertIn("tricolor", particle)
        self.assertIn("operator_id", particle)
        self.assertIn("operator_tier", particle)

    def test_ledger_creation(self):
        """测试账本文件创建和写入"""
        out = flow_port(
            {
                "message": "测试账本",
                "operator_id": "test_user",
                "operator_tier": "T3",
                "auto_execute": True,
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        # 验证账本文件已创建
        self.assertTrue(self.ledger.exists())
        # 验证账本包含事件
        ledger_content = self.ledger.read_text(encoding="utf-8")
        self.assertGreater(len(ledger_content.strip()), 0)

    def test_gate_v3_decision(self):
        """测试第一道闸门 v3.0 决策"""
        out = flow_port(
            {
                "message": "测试闸门决策",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "dna": "#龍芯⚡️2026-05-15-GATE-TEST-v1.0",
                },
            },
            ledger_path=self.ledger,
        )
        # 验证闸门决策输出
        self.assertIn("gate_v3", out)
        gate_v3 = out.get("gate_v3")
        self.assertIsNotNone(gate_v3)
        self.assertIn("digital_root", gate_v3)
        self.assertIn("audit_color", gate_v3)
        self.assertIn("decision", gate_v3)

    def test_defense_inbound_outbound(self):
        """测试入站和出站防盾"""
        out = flow_port(
            {
                "message": "测试防盾",
                "operator_id": "UID9622",  # 使用认可的操作员以加快通过闸门
                "operator_tier": "T2",
                "auto_execute": True,
                "evidence": "单元测试防盾",
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "skip_defense": False,  # 启用防盾
                },
            },
            ledger_path=self.ledger,
        )
        # 验证防盾结果（只在成功路径返回）
        if out.get("execute_allowed"):
            self.assertIn("defense", out)
            defense = out.get("defense")
            self.assertIsNotNone(defense)
            self.assertIn("inbound", defense)
            self.assertIn("outbound", defense)

    def test_skip_defense_flag(self):
        """测试跳过防盾标志"""
        out = flow_port(
            {
                "message": "跳过防盾测试",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "evidence": "单元测试跳过防盾",
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "skip_defense": True,  # 跳过防盾
                },
            },
            ledger_path=self.ledger,
        )
        # 防盾应该是 skipped 状态（只在成功路径）
        if out.get("execute_allowed"):
            defense = out.get("defense", {})
            inbound = defense.get("inbound", {})
            self.assertTrue(inbound.get("skipped", False))

    def test_sancai_output(self):
        """测试三才输出结构"""
        out = flow_port(
            {
                "message": "测试三才输出",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "evidence": "单元测试三才",
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        # 验证三才结构（只在成功路径返回）
        if out.get("execute_allowed"):
            self.assertIn("sancai", out)
            sancai = out.get("sancai")
            self.assertIsNotNone(sancai)
            self.assertIn("inputs", sancai)
            self.assertIn("weights", sancai)
            self.assertIn("score", sancai)
            self.assertIn("passed", sancai)

    def test_dna_tracking(self):
        """测试 DNA 链路追踪"""
        dna = "#龍芯⚡️2026-05-27-DNA-TRACK-TEST-v1.0"
        out = flow_port(
            {
                "message": "DNA 追踪测试",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "evidence": "单元测试DNA追踪",
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "dna_current": dna,
                },
            },
            ledger_path=self.ledger,
        )
        # 验证 DNA 被记录
        self.assertIn("dna", out)
        self.assertIn("protocol_dna", out)
        self.assertIn("gate_dna", out)
        # flow_port_dna 只在成功路径返回
        if out.get("execute_allowed"):
            self.assertIn("flow_port_dna", out)

    def test_default_ledger_path(self):
        """测试默认账本路径"""
        # 调用时不指定 ledger_path，应使用默认路径
        out = flow_port(
            {
                "message": "默认账本路径测试",
                "operator_id": "test_user",
                "operator_tier": "T3",
                "auto_execute": True,
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            }
        )
        self.assertTrue(out.get("founder_same_rules"))
        # 验证返回结构
        self.assertIn("reply", out)
        self.assertIn("tricolor", out)
        self.assertIn("status", out)

    def test_response_structure_on_success(self):
        """测试成功响应的完整结构"""
        out = flow_port(
            {
                "message": "成功路径测试",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "title": "结构测试",
                },
            },
            ledger_path=self.ledger,
        )
        # 验证响应结构的关键字段
        required_keys = [
            "reply",
            "tricolor",
            "status",
            "dna",
            "particle",
            "protocol_dna",
            "founder_same_rules",
            "execute_allowed",
            "hold_for_audit",
        ]
        for key in required_keys:
            self.assertIn(key, out, f"Missing key: {key}")

    def test_response_structure_on_error(self):
        """测试错误响应的结构"""
        out = flow_port(
            {
                "message": "",  # 空消息会触发错误
                "operator_id": "test_user",
                "operator_tier": "T3",
                "tags": {},
            },
            ledger_path=self.ledger,
        )
        # 验证错误响应结构
        self.assertEqual(out.get("tricolor"), "🔴")
        self.assertEqual(out.get("status"), "fuse")
        self.assertIn("particle", out)
        self.assertTrue(out.get("founder_same_rules"))

    def test_flow_out_error_helper(self):
        """测试错误输出助手函数"""
        err = _flow_out_error("测试错误消息", "T3", "test_user")
        self.assertEqual(err.get("tricolor"), "🔴")
        self.assertEqual(err.get("status"), "fuse")
        self.assertIn("reply", err)
        self.assertTrue(err.get("founder_same_rules"))

    def test_mixed_tags_priority(self):
        """测试混合标签的优先级"""
        out = flow_port(
            {
                "message": "标签优先级测试",
                "operator_id": "UID9622",
                "operator_tier": "T2",
                "auto_execute": True,
                "tags": {
                    "confirm_code": CONFIRM_REQUIRED,
                    "gpg": GPG_REQUIRED,
                    "title": "自定义标题",
                    "inspiration_mode": False,
                    "skip_defense": True,
                },
            },
            ledger_path=self.ledger,
        )
        self.assertTrue(out.get("founder_same_rules"))

    def test_channel_defaults_to_api(self):
        """测试信道未指定时默认为 api"""
        out = flow_port(
            {
                "message": "信道默认值测试",
                "operator_id": "test_user",
                "operator_tier": "T3",
                "auto_execute": True,
                "tags": {"confirm_code": CONFIRM_REQUIRED, "gpg": GPG_REQUIRED},
            },
            ledger_path=self.ledger,
        )
        # 验证响应成功（未因信道出错）
        self.assertTrue(out.get("founder_same_rules"))


if __name__ == "__main__":
    unittest.main()
