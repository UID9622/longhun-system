# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-b6bcca8a
"""test_dna.py — DNA 生成与确认码闸门测试（锚点5、锚点6）。"""

from __future__ import annotations

import re
from datetime import date

import pytest

from longhun_trust.dna import (
    CONFIRM_CODE,
    DNA_PLACEHOLDER_TAG,
    GPG_FINGERPRINT,
    generate_dna,
    verify_confirm_code,
)
from longhun_trust.exceptions import ConfirmCodeError

# 天干+地支组合（手写干支的典型形态）
_GANZHI_PAIR = re.compile(r"[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]")
# 八卦名（手写卦名）
_GUA_NAME = re.compile(r"[乾坤震巽坎离艮兑]")


@pytest.fixture(autouse=True)
def no_generator_env(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """确保无生成器环境：清除环境变量并隔离工作目录（避免命中 ./bin）。"""
    monkeypatch.delenv("LONGHUN_DNA_GENERATOR", raising=False)
    monkeypatch.chdir(tmp_path)


class TestGenerateDnaFallback:
    """锚点5：无生成器环境 → 兜底占位，且不含手写干支。"""

    def test_fallback_contains_placeholder_tag(self):
        dna = generate_dna("audit")
        assert DNA_PLACEHOLDER_TAG in dna

    def test_fallback_format(self):
        dna = generate_dna("audit")
        today = date.today().isoformat()
        assert dna == f"#龍芯⚡️{today}-AUDIT-v1.0-{DNA_PLACEHOLDER_TAG}"
        assert dna.startswith("#龍芯")

    def test_fallback_no_handwritten_ganzhi_or_gua(self):
        """正则断言兜底串不含任何手写干支/卦名。"""
        for tag in ("audit", "factcheck", "self heal", "X"):
            dna = generate_dna(tag)
            assert not _GANZHI_PAIR.search(dna), f"疑似手写干支: {dna}"
            assert not _GUA_NAME.search(dna), f"疑似手写卦名: {dna}"

    def test_action_tag_normalized_upper_and_dash(self):
        dna = generate_dna("self heal")
        assert "-SELF HEAL-" not in dna
        assert "-SELF-HEAL-" in dna

    def test_version_param(self):
        dna = generate_dna("audit", version="v2.3")
        assert "-v2.3-" in dna


class TestGenerateDnaWithGenerator:
    """生成器可用时优先使用外部生成器（真跑子进程验证）。"""

    def _write_generator(self, tmp_path, body: str):
        gen = tmp_path / "lh_dna_generator.py"
        gen.write_text(body, encoding="utf-8")
        return gen

    def test_env_generator_used(self, monkeypatch, tmp_path):
        gen = self._write_generator(
            tmp_path,
            "import sys\n"
            "print('#龍芯⚡️FROM-GENERATOR-' + sys.argv[2])\n",
        )
        monkeypatch.setenv("LONGHUN_DNA_GENERATOR", str(gen))
        dna = generate_dna("audit")
        # 生成器脚本打印 '#龍芯⚡️FROM-GENERATOR-' + sys.argv[2]（即 --action 值）
        assert dna == "#龍芯⚡️FROM-GENERATOR-AUDIT"
        assert DNA_PLACEHOLDER_TAG not in dna

    def test_generator_bad_output_falls_back(self, monkeypatch, tmp_path):
        """生成器输出不以 '#龍芯' 开头 → 兜底。"""
        gen = self._write_generator(tmp_path, "print('bogus-output')\n")
        monkeypatch.setenv("LONGHUN_DNA_GENERATOR", str(gen))
        dna = generate_dna("audit")
        assert DNA_PLACEHOLDER_TAG in dna

    def test_generator_crash_falls_back(self, monkeypatch, tmp_path):
        """生成器非零退出 → 兜底。"""
        gen = self._write_generator(
            tmp_path, "import sys; sys.exit(1)\n"
        )
        monkeypatch.setenv("LONGHUN_DNA_GENERATOR", str(gen))
        dna = generate_dna("audit")
        assert DNA_PLACEHOLDER_TAG in dna

    def test_generator_timeout_falls_back(self, monkeypatch, tmp_path):
        """生成器超时(>5s) → 兜底。"""
        gen = self._write_generator(
            tmp_path, "import time; time.sleep(30)\n"
        )
        monkeypatch.setenv("LONGHUN_DNA_GENERATOR", str(gen))
        monkeypatch.setattr("longhun_trust.dna._GENERATOR_TIMEOUT_SECONDS", 1)
        dna = generate_dna("audit")
        assert DNA_PLACEHOLDER_TAG in dna


class TestVerifyConfirmCode:
    """锚点6：错误确认码 → ConfirmCodeError。"""

    def test_wrong_code_raises(self):
        with pytest.raises(ConfirmCodeError):
            verify_confirm_code("wrong")

    def test_empty_code_raises(self):
        with pytest.raises(ConfirmCodeError):
            verify_confirm_code("")

    def test_correct_code_passes(self):
        verify_confirm_code(CONFIRM_CODE)  # 不抛异常即通过

    def test_constants(self):
        assert CONFIRM_CODE == "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        assert GPG_FINGERPRINT == "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        assert DNA_PLACEHOLDER_TAG == "【干支待本地生成器校准】"
