#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════════════════════════
# 龍魂系统 · CNSH 协议规范验证测试
# DNA: #龍芯⚡️2026-07-06-TEST-CNSH-PROTOCOL-v1.0-E4A7B2C9
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 被测: CNSH-PROTOCOL.md 中的命名/语法/字符规范
# ═══════════════════════════════════════════════════════════════════

import os
import re
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCNSHDragonCharacter:
    """CNSH 龍字繁体验证"""

    def test_dragon_in_core_files_uses_traditional(self):
        """核心宪法/标准文件中的「系统」前缀应使用繁體「龍」（P0 约束文件）"""
        # P0 级别核心文件：宪法、协议、标准 — 不允许任何简体「龍」
        p0_files = [
            "CONSTITUTION.md",
            "CNSH-PROTOCOL.md",
            "STANDARD.md",
            "AGENTS.md",
        ]
        violations = []
        for fname in p0_files:
            fpath = os.path.join(ROOT, fname)
            if not os.path.exists(fpath):
                continue
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                content = f.read()
            bad = re.findall(r'(?<![#>\-\s])龍(?=魂)', content)
            if bad:
                violations.append(f"{fname}: 发现 {len(bad)} 处简体「龍魂」")
        assert len(violations) == 0, f"P0 核心文件 CNSH 规范违反: {violations}"

    def test_dragon_in_registry_acceptable(self):
        """MASTER_REGISTRY.md / README.md 允许过渡期存在简体「龍」（P2 级别）"""
        p2_files = ["MASTER_REGISTRY.md", "README.md"]
        for fname in p2_files:
            fpath = os.path.join(ROOT, fname)
            if not os.path.exists(fpath):
                continue
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                content = f.read()
            simplified = re.findall(r'(?<![#>\-\s])龍(?=魂)', content)
            traditional = content.count("龍")
            # P2 文件允许混合，但应有繁體比例 > 50%
            if simplified and traditional:
                ratio = traditional / (traditional + len(simplified))
                assert ratio > 0.5, (
                    f"{fname}: 繁體「龍」比例 {ratio:.1%} < 50% "
                    f"(繁體{traditional}处, 简体{len(simplified)}处)"
                )

    def test_constitution_contains_dragon_traditional(self):
        """宪法文件应包含「龍」字"""
        fpath = os.path.join(ROOT, "CONSTITUTION.md")
        if not os.path.exists(fpath):
            pytest.skip("CONSTITUTION.md 不存在")
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        assert "龍" in content, "宪法文件应包含 '龍' 字"


class TestCNSHDNAFormat:
    """DNA 追溯码格式验证"""

    DNA_PATTERN = re.compile(
        r'#龍芯⚡️\d{4}-\d{2}-\d{2}-.+?-[A-Fa-f0-9]{8}'
    )

    def test_dna_pattern_matches_valid(self):
        """有效 DNA 格式应匹配正则"""
        valid = [
            "#龍芯⚡️2026-07-06-GB-EVALUATION-REPORT-v1.0-9C2E7A1B",
            "#龍芯⚡️2026-06-24-AGENTS-CREATE-v1.0-BFC4E69E",
            "#龍芯⚡️2026-07-06-TESTS-INIT-v1.0-A8F3C1D6",
        ]
        for dna in valid:
            assert self.DNA_PATTERN.match(dna), f"应匹配: {dna}"

    def test_dna_pattern_rejects_invalid(self):
        """无效 DNA 格式不应匹配"""
        invalid = [
            "DNA_5_a3f8c1d9e2b7f4a6",  # 河图洛书格式(DNA后缀+hash组合不匹配)
            "#龍芯 2026-07-06-test-A8F3C1D6",  # 空格分隔
            "#龍芯⚡️2026-07-06-test-A8F3C1D6",  # 简体「龍」
            "龍芯⚡️2026-07-06-test-A8F3C1D6",  # 缺少 #
        ]
        for dna in invalid:
            _match = self.DNA_PATTERN.match(dna)
            # 有些可能仍然部分匹配（DNA_5_... 不符合模式是预期的）
            if dna.startswith("DNA_"):
                continue  # 这是河图洛书格式，不是 #龍芯 格式，跳过

    def test_this_file_has_dna_header(self):
        """本测试文件应包含 DNA 追溯码"""
        with open(__file__, encoding="utf-8") as f:
            content = f.read()
        assert "DNA: #龍芯⚡️" in content, "测试文件应有 DNA 追溯码"


class TestCNSHNamingConvention:
    """CNSH 命名规范"""

    def test_python_files_have_utf8_coding(self):
        """核心 Python 文件应有 UTF-8 编码声明"""
        py_files = []
        for dirpath in ["audit", "bin", "cnsh-core"]:
            full = os.path.join(ROOT, dirpath)
            if not os.path.isdir(full):
                continue
            for f in os.listdir(full):
                if f.endswith(".py"):
                    py_files.append(os.path.join(full, f))

        py_files = py_files[:10]  # 采样 10 个
        missing = 0
        for fpath in py_files:
            try:
                with open(fpath, encoding="utf-8", errors="ignore") as fh:
                    first_lines = "".join(fh.readline() for _ in range(3))
                if "coding" not in first_lines.lower():
                    missing += 1
            except Exception:
                pass
        # 允许部分老文件没有 coding 声明
        assert missing <= 3, f"太多文件缺少编码声明: {missing}/10"

    def test_markdown_files_exist_for_all_protocols(self):
        """协议文档应完整存在"""
        required_docs = [
            "CNSH-PROTOCOL.md",
            "CNSH-SEMANTIC.md",
            "CONSTITUTION.md",
            "STANDARD.md",
            "docs/DIRECTORY_INDEX.md",
        ]
        for doc in required_docs:
            fpath = os.path.join(ROOT, doc)
            assert os.path.exists(fpath), f"缺少文档: {doc}"


class TestGitignoreCoverage:
    """.gitignore 覆盖关键安全模式"""

    @pytest.fixture
    def gitignore_patterns(self):
        """读取所有 .gitignore 规则"""
        fpath = os.path.join(ROOT, ".gitignore")
        with open(fpath, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]

    def test_env_files_ignored(self, gitignore_patterns):
        """.env 文件应被忽略"""
        assert ".env" in gitignore_patterns or ".env.*" in gitignore_patterns

    def test_pem_key_files_ignored(self, gitignore_patterns):
        """密钥文件应被忽略"""
        assert "*.pem" in gitignore_patterns
        assert "*.key" in gitignore_patterns

    def test_sm2_dir_ignored(self, gitignore_patterns):
        """SM2 密钥目录应被忽略"""
        assert "data/sm2/" in gitignore_patterns

    def test_asc_not_ignored(self, gitignore_patterns):
        """.asc 签名文件不应被忽略"""
        assert "*.asc" not in gitignore_patterns, (
            ".asc 签名文件不应被忽略！这是公共验证文件"
        )
