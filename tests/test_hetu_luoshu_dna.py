# ═══════════════════════════════════════════════════════════════════
# 龍魂系统 · 河图洛书 DNA 生成器测试
# DNA: #龍芯⚡️2026-07-06-TEST-HETU-LUOSHU-DNA-v1.0-C5D7E9A3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 被测模块: bin/hetu_luoshu_dna.py
# ═══════════════════════════════════════════════════════════════════

import pytest
import hashlib


class TestHetuLuoshuDNA:
    """河图洛书 DNA 生成与验证"""

    def test_import_module(self):
        """模块应能正常导入"""
        from bin import hetu_luoshu_dna
        assert hetu_luoshu_dna is not None

    def test_dna_generation_basic(self, sample_timestamp):
        """基本 DNA 码生成"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成

        dna = 河图洛书_DNA生成("编辑器启动", "UID9622", sample_timestamp)
        assert dna.startswith("DNA_"), f"DNA 码应以 DNA_ 开头，实际: {dna}"
        parts = dna.split("_")
        assert len(parts) == 3, f"应有 3 部分，实际: {len(parts)} 部分"
        assert len(parts[2]) == 16, f"hash 部分应为 16 位 hex，实际长度: {len(parts[2])}"

    def test_dna_deterministic(self, sample_timestamp):
        """相同输入应始终生成相同 DNA"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成

        dna1 = 河图洛书_DNA生成("审计操作", "UID9622", sample_timestamp)
        dna2 = 河图洛书_DNA生成("审计操作", "UID9622", sample_timestamp)
        assert dna1 == dna2, "确定性输出: 相同输入应得相同 DNA"

    def test_dna_different_inputs_different_outputs(self, sample_timestamp):
        """不同输入应生成不同 DNA"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成

        dna1 = 河图洛书_DNA生成("操作A", "UID9622", sample_timestamp)
        dna2 = 河图洛书_DNA生成("操作B", "UID9622", sample_timestamp)
        assert dna1 != dna2, "不同操作应生成不同 DNA"

    def test_dna_verification_valid(self, sample_timestamp):
        """DNA 验证应有正确的往返"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成, 河图洛书_DNA验证

        dna = 河图洛书_DNA生成("编辑器启动", "UID9622", sample_timestamp)
        valid, msg = 河图洛书_DNA验证(dna, "编辑器启动", "UID9622", sample_timestamp)
        assert valid, f"有效 DNA 验证应通过: {msg}"

    def test_dna_verification_tampered(self, sample_timestamp):
        """篡改的 DNA 应被检测"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成, 河图洛书_DNA验证

        dna = 河图洛书_DNA生成("操作A", "UID9622", sample_timestamp)
        valid, msg = 河图洛书_DNA验证(dna, "操作B", "UID9622", sample_timestamp)
        assert not valid, f"篡改的 DNA 验证应失败: {msg}"

    def test_dna_verification_bad_format(self):
        """格式错误的 DNA 码应拒绝"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA验证

        valid, msg = 河图洛书_DNA验证("BAD_FORMAT", "test", "UID9622", "1700000000")
        assert not valid, msg

    def test_digital_root_zero(self):
        """数字根 0 应保持为 0"""
        from bin.hetu_luoshu_dna import _数字根
        assert _数字根(0) == 0

    def test_digital_root_nine(self):
        """9 的倍数应归为 9"""
        from bin.hetu_luoshu_dna import _数字根
        assert _数字根(9) == 9
        assert _数字根(18) == 9

    def test_digital_root_normal(self):
        """一般数字根计算"""
        from bin.hetu_luoshu_dna import _数字根
        assert _数字根(10) == 1
        assert _数字根(38) == 2  # 3+8=11, 1+1=2
        assert _数字根(7) == 7

    def test_zhongwu_immutable(self):
        """中五不动点恒为 5"""
        from bin.hetu_luoshu_dna import 中五不动点, 河图, 洛书
        assert 中五不动点 == 5
        assert 河图[4] == 5
        assert 洛书[4] == 5  # 洛书[1][1] 展平后第4位

    def test_bagua_mapping_complete(self):
        """八卦映射应包含全部 8 卦"""
        from bin.hetu_luoshu_dna import 八卦映射, 获取卦象
        assert len(八卦映射) == 8
        for name in ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]:
            gx = 获取卦象(name)
            assert gx is not None, f"缺少 {name} 卦"
            assert gx.名称 == name
            assert gx.五行 in ("金", "木", "水", "火", "土")
            assert 0 <= gx.权重 <= 100

    def test_hetu_luoshu_digital_root_of_text(self):
        """对文本计算数字根"""
        from bin.hetu_luoshu_dna import 河图洛书_数字根
        root = 河图洛书_数字根("龍魂系统")
        assert 1 <= root <= 9, f"数字根应在 1-9 范围内，实际: {root}"

    def test_dna_no_timestamp_defaults_to_now(self):
        """不提供时间戳时应使用当前时间"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成
        dna = 河图洛书_DNA生成("测试操作", "UID9622")
        assert dna.startswith("DNA_"), f"无时间戳也应成功生成: {dna}"

    def test_long_input_stability(self):
        """长文本输入应稳定"""
        from bin.hetu_luoshu_dna import 河图洛书_DNA生成
        long_text = "龍魂系统审计操作记录ABCDEFG" * 50
        dna = 河图洛书_DNA生成(long_text, "UID9622", "1700000000")
        assert dna.startswith("DNA_"), "长输入应正常生成 DNA"
