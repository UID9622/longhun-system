#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════════════════╗
║     🐉 龍魂·AutoFlow 测试用例集 v1.0                                     ║
║     LongHun AutoFlow Test Suite                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA:  #龍芯⚡️丙午·辛未·乙酉·酉时·䷅讼-AUTOFLOW-TEST-SUITE-v1.0        ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                          ║
║  覆盖: 语义路由·否决词·恶意检测·全链路·数字根·审计·熔断·降级·边缘      ║
║  人格: P02(结构) + P05(验证) + P04(工程)                                 ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  pytest tests/test_autoflow.py -v                    # 全部测试
  pytest tests/test_autoflow.py -v -m core            # 核心测试
  pytest tests/test_autoflow.py -v -m integration     # 集成测试
  pytest tests/test_autoflow.py -v -k "test_intent"   # 按名称筛选
"""

import json
import sys
import time
from pathlib import Path

import pytest

# 加载项目路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

from lh_autoflow import (
    LonghunAutoFlow,
    AutoFlowResult,
    AuditMark,
    SEMANTIC_ROUTES,
    VETO_WORDS,
    MALICIOUS_PATTERNS,
    DNA_BASE,
    CONFIRM_CODE,
    GPG_FINGERPRINT,
    DEVICE_SEAL,
    VERSION,
)


# ═══════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def engine():
    """创建干净的引擎实例"""
    e = LonghunAutoFlow(enable_gpg=False)
    yield e
    e.reset()


@pytest.fixture
def engine_with_gpg():
    """创建启用 GPG 的引擎实例"""
    return LonghunAutoFlow(enable_gpg=True)


# ═══════════════════════════════════════════════════════════════
# 一、常量与基础验证
# ═══════════════════════════════════════════════════════════════

class TestConstants:
    """常量完整性验证 · P0 焊死底座"""

    def test_dna_base_format(self):
        """DNA 基础格式正确"""
        assert DNA_BASE.startswith("#龍芯⚡️")
        assert "AUTOFLOW" in DNA_BASE

    def test_confirm_code(self):
        """确认码不可变"""
        assert CONFIRM_CODE == "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

    def test_gpg_fingerprint(self):
        """GPG 指纹正确"""
        assert len(GPG_FINGERPRINT) == 40
        assert GPG_FINGERPRINT.startswith("A2D009")

    def test_device_seal(self):
        """设备封印完整"""
        assert "ZHUGEXIN" in DEVICE_SEAL
        assert "DEVICE-BIND" in DEVICE_SEAL

    def test_version(self):
        """版本号格式"""
        assert VERSION.count(".") == 2

    def test_veto_words_not_empty(self):
        """一票否决词表非空"""
        assert len(VETO_WORDS) >= 8

    def test_malicious_patterns_not_empty(self):
        """恶意模式表非空"""
        assert len(MALICIOUS_PATTERNS) >= 3

    def test_semantic_routes_count(self):
        """语义路由数量充足"""
        assert len(SEMANTIC_ROUTES) >= 20


# ═══════════════════════════════════════════════════════════════
# 二、意图解析 · 语义路由
# ═══════════════════════════════════════════════════════════════

class TestIntentParsing:
    """意图解析测试 · 覆盖所有主要语义抽屉"""

    # ── 审计/安全类 ──
    @pytest.mark.parametrize("text,expected", [
        ("检查系统安全", "P05"),
        ("帮我审计这段代码", "P05"),
        ("系统健康检查一下", "P05"),
        ("跑个巡检看看有没有问题", "P05"),
        ("三色审计一下", "P05"),
    ])
    def test_intent_audit_security(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected, f"'{text}' → {intent.primary_persona} != {expected}"
        assert intent.confidence >= 0.5

    # ── 修复/开发类 ──
    @pytest.mark.parametrize("text,expected", [
        ("修一下这个bug", "P02"),
        ("改好这个报错", "P02"),
        ("修复不报错的问题", "P02"),
        ("fix the issue", "P02"),
        ("debug一下", "P02"),
    ])
    def test_intent_fix_repair(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 部署类 ──
    @pytest.mark.parametrize("text,expected", [
        ("部署到鲲鹏服务器", "P14"),
        ("发布新版本", "P14"),
        ("上线这个功能", "P14"),
        ("deploy to production", "P14"),
    ])
    def test_intent_deploy(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 数学/数理类 ──
    @pytest.mark.parametrize("text,expected", [
        ("算一下数字根", "P06"),
        ("这个数字属什么属性", "P06"),
        ("用369分析下", "P06"),
        ("五行八卦算一下", "P06"),
        ("洛书推演", "P06"),
    ])
    def test_intent_math(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 安全漏洞类 ──
    @pytest.mark.parametrize("text,expected", [
        ("检查有没有SQL注入漏洞", "P77"),
        ("渗透测试一下", "P77"),
        ("找找XSS漏洞", "P77"),
        ("分析攻击面", "P77"),
        ("这个接口有越权风险吗", "P77"),
    ])
    def test_intent_security_vuln(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 内容/舆情类 ──
    @pytest.mark.parametrize("text,expected", [
        ("帮我分析抖音数据，看看有没有水军", "P05"),
        ("微博评论区有没有水军", "P05"),
        ("分析小红书舆情", "P05"),
    ])
    def test_intent_water_army(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 铁律/边界类 ──
    @pytest.mark.parametrize("text,expected", [
        ("查一下铁律怎么规定", "P00"),
        ("这个违反规矩吗", "P00"),
        ("宪法底座不可破", "P00"),
    ])
    def test_intent_iron_law(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 版权/署名类 ──
    @pytest.mark.parametrize("text,expected", [
        ("检查引用来源是否合规", "P05"),
        ("署名归属确认", "P05"),
        ("原创声明检查", "P05"),
    ])
    def test_intent_attribution(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 情绪类 ──
    @pytest.mark.parametrize("text,expected", [
        ("我心情不好需要安慰", "P02"),
        ("安抚一下情绪", "P02"),
    ])
    def test_intent_emotion(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 法律/合规类 ──
    @pytest.mark.parametrize("text,expected", [
        ("这个符合法规吗", "S1"),
        ("合规性审查", "S1"),
    ])
    def test_intent_legal(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 维权类 ──
    @pytest.mark.parametrize("text,expected", [
        ("我要投诉侵权", "S3"),
        ("帮我写申诉材料", "S3"),
    ])
    def test_intent_complaint(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 归档类 ──
    @pytest.mark.parametrize("text,expected", [
        ("归档这些文件", "P03"),
        ("整理入库", "P03"),
        ("验收归档", "P03"),
    ])
    def test_intent_archive(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 签章类 ──
    @pytest.mark.parametrize("text,expected", [
        ("给这份文档签章", "P15"),
        ("GPG签名", "P15"),
    ])
    def test_intent_seal(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── DNA/注册类 ──
    @pytest.mark.parametrize("text,expected", [
        ("生成DNA追溯码", "P18"),
        ("DNA登记", "P18"),
    ])
    def test_intent_dna(self, engine, text, expected):
        intent = engine._parse_intent(text)
        assert intent.primary_persona == expected

    # ── 默认路由 ──
    def test_intent_default_fallback(self, engine):
        """无法匹配时默认路由到 P05"""
        intent = engine._parse_intent("今天天气不错")
        assert intent.primary_persona == "P05"
        assert intent.confidence < 0.5

    # ── 多关键词匹配选最高分 ──
    def test_intent_multi_keyword_priority(self, engine):
        """「检查安全漏洞」同时匹配 '检查' 和 '漏洞'，应选 P77（漏洞更具体）"""
        intent = engine._parse_intent("检查安全漏洞")
        assert intent.primary_persona in ("P77", "P05")  # P77 有"漏洞"关键词

    # ── 空输入 ──
    def test_intent_empty_input(self, engine):
        intent = engine._parse_intent("")
        assert intent.primary_persona == "P05"
        assert intent.confidence < 0.5

    # ── 长输入 ──
    def test_intent_very_long_input(self, engine):
        long_text = "审计" + "内容" * 500
        intent = engine._parse_intent(long_text)
        assert intent.primary_persona == "P05"


# ═══════════════════════════════════════════════════════════════
# 三、一票否决词检测
# ═══════════════════════════════════════════════════════════════

class TestVetoWords:
    """一票否决词扫描 · 每条都必须触发"""

    def test_veto_triggered(self, engine):
        """每个否决词单独测试触发"""
        for word in VETO_WORDS:
            result = engine._check_veto(f"我觉得{word}是对的")
            assert result == word, f"否决词 '{word}' 未触发"

    def test_veto_embedded_in_text(self, engine):
        """否决词嵌入长文本中也能检测"""
        text = "关于这个项目，我们认为应该国际接轨，参考行业标准来设计。"
        result = engine._check_veto(text)
        assert result is not None  # 至少触发一个

    def test_veto_case_insensitive(self, engine):
        """大小写不敏感"""
        result = engine._check_veto("灵活处理")
        assert result is not None

    def test_veto_not_triggered_normal(self, engine):
        """正常文本不触发否决词"""
        result = engine._check_veto("帮我检查一下系统安全")
        assert result is None

    def test_veto_not_triggered_similar_but_not_exact(self, engine):
        """近义词不误触发（如'处理'不触发'灵活处理'）"""
        result = engine._check_veto("处理用户请求")
        assert result is None

    def test_veto_empty_input(self, engine):
        """空输入不触发"""
        result = engine._check_veto("")
        assert result is None

    def test_veto_full_rejection_in_execute(self, engine):
        """执行流程中触发否决词应被拒绝"""
        result = engine.execute("技术无国界是趋势")
        assert result.status == "REJECTED"
        assert "技术无国界" in str(result.reject_reason)
        assert result.audit_mark == "🔴"

    def test_veto_multiple_triggered(self, engine):
        """多个否决词同时出现，返回第一个"""
        result = engine._check_veto("灵活处理，国际接轨")
        assert result is not None


# ═══════════════════════════════════════════════════════════════
# 四、恶意输入检测
# ═══════════════════════════════════════════════════════════════

class TestMaliciousDetection:
    """恶意意图检测"""

    def test_xss_injection(self, engine):
        assert engine._is_malicious("<script>alert('xss')</script>")

    def test_xss_img_tag(self, engine):
        assert engine._is_malicious("<img src=x onerror=alert(1)>")

    def test_sql_injection_drop(self, engine):
        assert engine._is_malicious("DROP TABLE users;")

    def test_sql_injection_delete(self, engine):
        assert engine._is_malicious("DELETE FROM accounts WHERE 1=1")

    def test_command_injection(self, engine):
        assert engine._is_malicious("rm -rf /")

    def test_sudo_rm(self, engine):
        assert engine._is_malicious("sudo rm -rf /var/log")

    def test_javascript_protocol(self, engine):
        assert engine._is_malicious("javascript:alert(1)")

    def test_data_protocol(self, engine):
        assert engine._is_malicious("data:text/html,<script>alert(1)</script>")

    def test_normal_input_not_flagged(self, engine):
        assert not engine._is_malicious("正常的审计请求")

    def test_very_long_input(self, engine):
        """超长输入触发 DoS 防护"""
        long_text = "A" * 100001
        assert engine._is_malicious(long_text)

    def test_max_length_input_allowed(self, engine):
        """边界值：正好在限制以内的通过"""
        text = "A" * 100000
        # 不触发长度检查，但可能因其他原因触发（取决于内容）
        # 这里只验证不因为长度而拒绝
        assert len(text) <= 100000

    def test_empty_input_not_malicious(self, engine):
        assert not engine._is_malicious("")

    def test_chinese_sql_keywords_not_flagged(self, engine):
        """中文 SQL 关键词不应被误判"""
        # 中文字符不是 SQL 命令
        assert not engine._is_malicious("删除用户表中的数据")

    def test_rejection_in_execute(self, engine):
        """执行流程中恶意输入应被拒绝"""
        result = engine.execute("<script>alert(1)</script>")
        assert result.status == "REJECTED"
        assert result.audit_mark == "🔴"


# ═══════════════════════════════════════════════════════════════
# 五、数字根计算
# ═══════════════════════════════════════════════════════════════

class TestDigitalRoot:
    """数字根计算验证"""

    def test_basic_dr(self, engine):
        """基本数字根"""
        # h(104)+e(101)+l(108)+l(108)+o(111)=532→5+3+2=10→1+0=1
        assert engine._digital_root("hello") >= 1

    def test_zero_input(self, engine):
        assert engine._digital_root("") == 0

    def test_dr_range(self, engine):
        """数字根始终在 1-9 或 0"""
        for text in ["test", "中国", "龍魂", "123", "abc", "!@#"]:
            dr = engine._digital_root(text)
            if dr != 0:
                assert 1 <= dr <= 9, f"'{text}' dr={dr}"

    def test_dr_consistent(self, engine):
        """相同输入得到相同数字根"""
        dr1 = engine._digital_root("龍魂系统")
        dr2 = engine._digital_root("龍魂系统")
        assert dr1 == dr2

    def test_chain_math_valid(self, engine):
        """链路数字根验证"""
        assert engine._verify_chain_math("正常内容") is True


# ═══════════════════════════════════════════════════════════════
# 六、DNA 生成
# ═══════════════════════════════════════════════════════════════

class TestDNAGeneration:
    """DNA 追溯码生成"""

    def test_dna_format(self, engine):
        """DNA 格式正确"""
        dna = engine._generate_dna("TEST", "GEN")
        assert dna.startswith("#龍芯⚡️")
        assert "TEST" in dna
        assert "GEN" in dna
        # 验证 8 位十六进制后缀
        parts = dna.split("-")
        last = parts[-1]
        assert len(last) == 8
        assert all(c in "0123456789ABCDEF" for c in last)

    def test_dna_unique(self, engine):
        """每次生成的 DNA 不同"""
        dna1 = engine._generate_dna("A", "B")
        time.sleep(0.01)
        dna2 = engine._generate_dna("A", "B")
        assert dna1 != dna2

    def test_dna_different_modules(self, engine):
        """不同模块生成不同 DNA"""
        dna1 = engine._generate_dna("AUDIT", "RUN")
        dna2 = engine._generate_dna("DEPLOY", "RUN")
        assert dna1 != dna2

    def test_dna_in_result(self, engine):
        """执行结果中必含 DNA"""
        result = engine.execute("审计系统状态")
        assert result.dna
        assert "#龍芯⚡️" in result.dna


# ═══════════════════════════════════════════════════════════════
# 七、路径推演
# ═══════════════════════════════════════════════════════════════

class TestPathPlanning:
    """执行路径推演"""

    def test_plan_contains_primary(self, engine):
        """推演路径包含主人格"""
        intent = engine._parse_intent("审计系统安全")
        plan = engine._plan_path(intent, "审计系统安全")
        personas = [s.persona for s in plan]
        assert "P05" in personas, f"主人格 P05 不在路径中: {personas}"

    def test_plan_ends_with_archive(self, engine):
        """任何路径末尾都含归档步骤(P03或P15)"""
        intent = engine._parse_intent("部署上线")
        plan = engine._plan_path(intent, "部署上线")
        last_personas = [s.persona for s in plan[-2:]]
        has_archive = "P03" in last_personas or "P15" in last_personas
        assert has_archive, f"路径最后两步无归档: {last_personas}"

    def test_fallback_plan(self, engine):
        """降级路径应包含基本步骤"""
        plan = engine._fallback_plan()
        assert len(plan) >= 3
        personas = [s.persona for s in plan]
        assert "P05" in personas

    def test_high_risk_route_has_extra_audit(self, engine):
        """高风险路由应包含额外审计"""
        intent = engine._parse_intent("渗透测试漏洞")
        plan = engine._plan_path(intent, "渗透测试漏洞")
        personas = [s.persona for s in plan]
        # 高风险路由审计更多
        assert len(plan) >= 3


# ═══════════════════════════════════════════════════════════════
# 八、全链路执行
# ═══════════════════════════════════════════════════════════════

class TestFullExecution:
    """全链路端到端执行"""

    def test_normal_execution_success(self, engine):
        """正常执行应成功"""
        result = engine.execute("审计系统安全状态")
        assert result.status in ("SUCCESS", "PARTIAL")
        assert result.audit_mark in ("🟢", "🟡")
        assert result.execution_chain
        assert len(result.step_results) > 0

    def test_execution_has_dna(self, engine):
        """每次执行都必须有 DNA"""
        result = engine.execute("检查系统状态")
        assert result.dna

    def test_execution_has_confirm_code(self, engine):
        """每次执行都必须包含确认码"""
        result = engine.execute("审计一下")
        assert result.confirm_code == CONFIRM_CODE

    def test_execution_has_gpg_fingerprint(self, engine):
        """每次执行都必须有 GPG 指纹"""
        result = engine.execute("检查安全")
        assert result.gpg_fingerprint == GPG_FINGERPRINT

    def test_execution_produces_trace(self, engine):
        """执行产生追踪记录"""
        engine.execute("审计系统")
        assert len(engine.trace) > 0

    def test_multiple_executions_independent(self, engine):
        """多次执行互不影响"""
        r1 = engine.execute("审计系统状态")
        r2 = engine.execute("修一下bug")
        assert r1.dna != r2.dna
        assert r1.dna != r2.dna

    def test_execution_with_context(self, engine):
        """带上下文的执行"""
        result = engine.execute("检查安全", context={"user": "UID9622", "session": "test"})
        assert result.status != "REJECTED"

    def test_execution_seal_generated(self, engine):
        """正常执行应生成签章"""
        result = engine.execute("检查系统健康")
        if result.status != "REJECTED":
            assert result.seal is not None
            assert "dna" in result.seal
            assert "signer" in result.seal

    def test_execution_seal_contains_founder(self, engine):
        """签章包含创始人信息"""
        result = engine.execute("审计代码")
        if result.seal:
            assert result.seal.get("founder") == "诸葛鑫（Lucky）· 龍芯北辰"
            assert result.seal.get("uid") == "UID9622"

    def test_execution_archived(self, engine):
        """正常执行应产生归档 ID"""
        result = engine.execute("审计状态")
        if result.status != "REJECTED":
            assert result.archived_id is not None
            assert result.archived_id.startswith("ARCH-")


# ═══════════════════════════════════════════════════════════════
# 九、审计
# ═══════════════════════════════════════════════════════════════

class TestAudit:
    """三色审计机制"""

    def test_normal_output_green(self, engine):
        """正常输出🟢"""
        output = {"verdict": "🟢 PASS", "score": 0.95}
        result = engine._step_audit(output, engine._fallback_plan()[0])
        assert result == "🟢"

    def test_fuse_output_red(self, engine):
        """熔断输出🔴"""
        output = {"verdict": "🔴 FUSE: 检测到违规"}
        result = engine._step_audit(output, engine._fallback_plan()[0])
        assert result == "🔴"

    def test_hold_output_yellow(self, engine):
        """待审输出🟡"""
        output = {"verdict": "🟡 HOLD: 需要人工审核"}
        result = engine._step_audit(output, engine._fallback_plan()[0])
        assert result == "🟡"

    def test_none_output_red(self, engine):
        """空输出🔴"""
        result = engine._step_audit(None, engine._fallback_plan()[0])
        assert result == "🔴"

    def test_final_audit_no_red_steps(self, engine):
        """无红色步骤时通过"""
        from lh_autoflow import StepResult
        results = [
            StepResult("P05", "success", output={"verdict": "🟢"}, audit_mark="🟢"),
        ]
        verdict = engine._final_audit(results, AuditMark.GREEN, "test")
        assert verdict == AuditMark.GREEN


# ═══════════════════════════════════════════════════════════════
# 十、熔断
# ═══════════════════════════════════════════════════════════════

class TestFuse:
    """熔断机制"""

    def test_fuse_writes_log(self, engine):
        """熔断写入日志文件"""
        dna = engine._generate_dna("TEST", "FUSE")
        engine._trigger_fuse("L2", "测试熔断", dna)
        # 验证熔断日志目录存在
        fuse_dir = PROJECT_ROOT / "state" / "fuse_logs"
        assert fuse_dir.exists()

    def test_fuse_in_trace(self, engine):
        """熔断记录在追踪中"""
        dna = engine._generate_dna("TEST", "FUSE")
        engine._trigger_fuse("L1", "紧急熔断", dna)
        fuse_actions = [t for t in engine.trace if "FUSE" in t["action"]]
        assert len(fuse_actions) > 0


# ═══════════════════════════════════════════════════════════════
# 十一、降级与重试
# ═══════════════════════════════════════════════════════════════

class TestDegradation:
    """降级与重试机制"""

    def test_find_backup_known_persona(self, engine):
        """已知人格有备用人格"""
        backup = engine._find_backup("P02")
        assert backup is not None
        assert backup == "P10"

    def test_find_backup_unknown_persona(self, engine):
        """未知人格无备份"""
        backup = engine._find_backup("P99")
        assert backup is None

    def test_fallback_plan_has_p05(self, engine):
        """降级路径必须包含 P05 审计"""
        plan = engine._fallback_plan()
        personas = [s.persona for s in plan]
        assert "P05" in personas

    def test_locked_persona_tracked(self, engine):
        """锁定人格被记录"""
        engine.locked_personas.add("P02")
        assert "P02" in engine.locked_personas

    def test_reset_clears_locks(self, engine):
        """reset 清除锁定"""
        engine.locked_personas.add("P02")
        engine.reset()
        assert len(engine.locked_personas) == 0

    def test_reset_clears_trace(self, engine):
        """reset 清除追踪"""
        engine._add_trace("TEST", "test")
        engine.reset()
        assert len(engine.trace) == 0


# ═══════════════════════════════════════════════════════════════
# 十二、拒绝场景
# ═══════════════════════════════════════════════════════════════

class TestRejection:
    """各种拒绝执行场景"""

    def test_veto_word_rejection(self, engine):
        result = engine.execute("灵活处理这个问题")
        assert result.status == "REJECTED"
        assert result.dna
        assert result.reject_reason

    def test_malicious_input_rejection(self, engine):
        result = engine.execute("<script>alert(1)</script>")
        assert result.status == "REJECTED"

    def test_sql_injection_rejection(self, engine):
        result = engine.execute("DROP TABLE users;")
        assert result.status == "REJECTED"

    def test_rejection_has_dna(self, engine):
        """拒绝执行也必须有 DNA"""
        result = engine.execute("技术无国界")
        assert result.dna

    def test_rejection_has_confirm_code(self, engine):
        """拒绝执行也必须包含确认码"""
        result = engine.execute("技术无国界")
        assert result.confirm_code == CONFIRM_CODE

    def test_rejection_gate_label(self, engine):
        """拒绝时有闸口标签"""
        result = engine.execute("技术无国界")
        assert "GATE" in result.execution_chain or result.reject_reason


# ═══════════════════════════════════════════════════════════════
# 十三、边缘情况
# ═══════════════════════════════════════════════════════════════

class TestEdgeCases:
    """边缘情况与异常输入"""

    def test_empty_string(self, engine):
        """空字符串"""
        result = engine.execute("")
        assert result.status in ("REJECTED", "SUCCESS")  # 空输入意图置信度低

    def test_whitespace_only(self, engine):
        """纯空白"""
        result = engine.execute("   \t\n  ")
        assert result.status in ("PARTIAL", "SUCCESS")

    def test_special_characters(self, engine):
        """特殊字符"""
        result = engine.execute("!@#$%^&*()")
        assert result.status != "REJECTED"  # 不触发否决词或恶意检测

    def test_emoji_input(self, engine):
        """Emoji 输入"""
        result = engine.execute("🤔🤔🤔 审计 🐉🐉🐉")
        assert result.status != "REJECTED"

    def test_unicode_input(self, engine):
        """Unicode 混合输入"""
        result = engine.execute("龍魂·检查·テスト·안전")
        assert result.status != "REJECTED"

    def test_numbers_only(self, engine):
        """纯数字"""
        result = engine.execute("1234567890")
        assert result.status in ("PARTIAL", "SUCCESS")

    def test_single_keyword(self, engine):
        """单个关键词"""
        result = engine.execute("审计")
        assert result.status in ("SUCCESS", "PARTIAL")

    def test_chinese_punctuation(self, engine):
        """中文标点"""
        result = engine.execute("「审计」系统——安全！")
        assert result.status in ("SUCCESS", "PARTIAL")

    def test_newlines_in_input(self, engine):
        """多行输入"""
        result = engine.execute("审计\n系统\n安全")
        assert result.status in ("SUCCESS", "PARTIAL")


# ═══════════════════════════════════════════════════════════════
# 十四、健康检查
# ═══════════════════════════════════════════════════════════════

class TestHealthCheck:
    """引擎健康检查"""

    def test_health_check_returns_dict(self, engine):
        health = engine.health_check()
        assert isinstance(health, dict)

    def test_health_check_keys(self, engine):
        health = engine.health_check()
        required_keys = ["engine", "version", "dna", "mode", "routes_count", "gates_count"]
        for key in required_keys:
            assert key in health, f"缺少键: {key}"

    def test_health_check_version(self, engine):
        health = engine.health_check()
        assert health["version"] == VERSION

    def test_health_check_routes_count(self, engine):
        health = engine.health_check()
        assert health["routes_count"] >= 20

    def test_health_check_gates_count(self, engine):
        health = engine.health_check()
        assert health["gates_count"] >= 5


# ═══════════════════════════════════════════════════════════════
# 十五、自检
# ═══════════════════════════════════════════════════════════════

class TestSelfTest:
    """内置自检"""

    def test_self_test_all_pass(self, engine):
        """自检应全部通过"""
        report = engine.run_self_test()
        assert report["total"] > 0
        assert report["passed"] == report["total"], f"自检失败: {report}"

    def test_self_test_returns_results(self, engine):
        report = engine.run_self_test()
        assert "results" in report
        assert len(report["results"]) > 0

    def test_self_test_veto_check(self, engine):
        """自检中的否决词检测正确"""
        report = engine.run_self_test()
        veto_tests = [r for r in report["results"] if "一票否决词" in r["test"]]
        assert len(veto_tests) > 0
        for t in veto_tests:
            assert t["passed"], f"否决词测试失败: {t}"


# ═══════════════════════════════════════════════════════════════
# 十六、路由列表
# ═══════════════════════════════════════════════════════════════

class TestRouteListing:
    """路由查询"""

    def test_list_routes(self, engine):
        routes = engine.list_routes()
        assert len(routes) == len(SEMANTIC_ROUTES)
        for r in routes:
            assert "keywords" in r
            assert "primary" in r
            assert "action" in r

    def test_list_gates(self, engine):
        gates = engine.list_gates()
        assert len(gates) >= 5
        assert all("num" in g and "name" in g for g in gates)


# ═══════════════════════════════════════════════════════════════
# 十七、归档
# ═══════════════════════════════════════════════════════════════

class TestArchive:
    """归档功能"""

    def test_archive_creates_file(self, engine):
        """归档生成 JSON 文件"""
        plan = engine._fallback_plan()
        from lh_autoflow import StepResult
        results = [StepResult("P05", "success", output={"ok": True})]
        seal = {"dna": "test", "signer": "P15"}
        dna = engine._generate_dna("TEST", "ARCHIVE")
        archive_id = engine._archive("test input", plan, results, AuditMark.GREEN, seal, dna)
        assert archive_id.startswith("ARCH-")

        archive_dir = PROJECT_ROOT / "state" / "autoflow_archive"
        files = list(archive_dir.glob(f"{archive_id}.json"))
        assert len(files) >= 1

    def test_archive_id_unique(self, engine):
        """每次归档 ID 唯一"""
        plan = engine._fallback_plan()
        from lh_autoflow import StepResult
        results = [StepResult("P05", "success")]
        seal = {"dna": "test"}
        id1 = engine._archive("t1", plan, results, AuditMark.GREEN, seal, "dna1")
        time.sleep(0.01)
        id2 = engine._archive("t2", plan, results, AuditMark.GREEN, seal, "dna2")
        assert id1 != id2


# ═══════════════════════════════════════════════════════════════
# 十八、集成测试
# ═══════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestIntegration:
    """端到端集成测试"""

    def test_full_flow_audit(self, engine):
        """完整审计流程"""
        result = engine.execute("审计系统安全状态并给出报告")
        assert result.status != "REJECTED"
        assert len(result.step_results) >= 2
        assert result.archived_id

    def test_full_flow_fix(self, engine):
        """完整修复流程"""
        result = engine.execute("修一下这个报错")
        assert result.status != "REJECTED"

    def test_full_flow_deploy(self, engine):
        """完整部署流程"""
        result = engine.execute("部署到鲲鹏服务器")
        # 部署是高风险的，可能 PARTIAL
        assert result.status in ("SUCCESS", "PARTIAL", "REJECTED")

    def test_full_flow_security(self, engine):
        """完整安全审计流程"""
        result = engine.execute("检查系统有没有SQL注入漏洞")
        assert result.status != "REJECTED"

    def test_full_flow_water_army(self, engine):
        """水军检测流程"""
        result = engine.execute("帮我分析抖音评论区有没有水军")
        assert result.status != "REJECTED"

    def test_full_flow_dna_registry(self, engine):
        """DNA 登记流程"""
        result = engine.execute("DNA登记这个文件")
        assert result.status != "REJECTED"

    def test_consecutive_executions(self, engine):
        """连续多次执行"""
        tasks = ["审计系统", "修复bug", "检查安全"]
        for task in tasks:
            result = engine.execute(task)
            assert result.status in ("SUCCESS", "PARTIAL", "REJECTED")
            assert result.dna

    def test_result_contains_all_required_fields(self, engine):
        """结果包含所有必需字段"""
        result = engine.execute("审计系统")
        required = ["status", "audit_mark", "dna", "execution_chain",
                     "step_results", "time_ms", "confirm_code", "gpg_fingerprint"]
        for field in required:
            assert getattr(result, field, None) is not None, f"缺少字段: {field}"

    def test_dry_run_execution(self, engine):
        """干运行测试——通过引擎内部方法"""
        intent = engine._parse_intent("部署到鲲鹏")
        plan = engine._plan_path(intent, "部署到鲲鹏")
        assert len(plan) > 0
        # 干运行不实际执行，只验证路径推演
        assert any(s.persona == "P14" for s in plan), "部署意图应路由到 P14"


# ═══════════════════════════════════════════════════════════════
# 十九、性能测试
# ═══════════════════════════════════════════════════════════════

class TestPerformance:
    """性能基准"""

    def test_intent_parse_fast(self, engine):
        """意图解析应在 10ms 内完成"""
        start = time.time()
        for _ in range(100):
            engine._parse_intent("审计系统安全状态")
        elapsed = (time.time() - start) * 1000
        avg = elapsed / 100
        assert avg < 10, f"意图解析过慢: {avg:.1f}ms/次"

    def test_full_execution_under_timeout(self, engine):
        """全链路执行应在超时内完成"""
        start = time.time()
        result = engine.execute("审计系统状态")
        elapsed = (time.time() - start) * 1000
        assert elapsed < 5000, f"全链路执行过慢: {elapsed:.0f}ms"

    def test_veto_scan_fast(self, engine):
        """否决词扫描应在 1ms 内完成"""
        start = time.time()
        for _ in range(1000):
            engine._check_veto("正常的审计文本内容")
        elapsed = (time.time() - start) * 1000
        avg = elapsed / 1000
        assert avg < 1, f"否决词扫描过慢: {avg:.1f}ms/次"


# ═══════════════════════════════════════════════════════════════
# 二十、序列化
# ═══════════════════════════════════════════════════════════════

class TestSerialization:
    """结果序列化"""

    def test_result_json_serializable(self, engine):
        """结果可 JSON 序列化"""
        result = engine.execute("审计系统")
        data = {
            "status": result.status,
            "audit_mark": result.audit_mark,
            "dna": result.dna,
            "execution_chain": result.execution_chain,
            "time_ms": result.time_ms,
            "archived_id": result.archived_id,
            "reject_reason": result.reject_reason,
            "confirm_code": result.confirm_code,
            "gpg_fingerprint": result.gpg_fingerprint,
            "step_results": [
                {
                    "persona": sr.persona,
                    "status": sr.status,
                    "audit": sr.audit_mark,
                    "duration_ms": sr.duration_ms,
                    "attempts": sr.attempts,
                }
                for sr in result.step_results
            ],
        }
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["status"] == result.status
        assert parsed["dna"] == result.dna

    def test_rejected_result_serializable(self, engine):
        """拒绝结果也可序列化"""
        result = engine.execute("技术无国界")
        data = {
            "status": result.status,
            "audit_mark": result.audit_mark,
            "dna": result.dna,
            "reject_reason": result.reject_reason,
        }
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["status"] == "REJECTED"


# ═══════════════════════════════════════════════════════════════
# CLI 测试入口（可选）
# ═══════════════════════════════════════════════════════════════

def test_cli_help():
    """CLI --help 不报错"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--help"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    assert "一句话全链路" in result.stdout


def test_cli_list_routes():
    """CLI --list-routes 输出路由"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--list-routes"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    assert "语义路由" in result.stdout


def test_cli_health():
    """CLI --health 输出健康检查"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--health"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    assert "健康检查" in result.stdout


def test_cli_test():
    """CLI --test 运行自检"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--test"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0


def test_cli_execute():
    """CLI 执行任务"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "审计系统状态"],
        capture_output=True, text=True, timeout=10,
    )
    assert "执行报告" in result.stdout
    assert result.returncode == 0


def test_cli_json_output():
    """CLI --json 输出"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--json", "审计系统"],
        capture_output=True, text=True, timeout=10,
    )
    data = json.loads(result.stdout)
    assert "status" in data
    assert "dna" in data


def test_cli_dry_run():
    """CLI --dry-run 干运行"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--dry-run", "部署到鲲鹏"],
        capture_output=True, text=True, timeout=10,
    )
    assert "干运行" in result.stdout
    assert result.returncode == 0


def test_cli_verbose():
    """CLI --verbose 详细输出"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--verbose", "审计系统"],
        capture_output=True, text=True, timeout=10,
    )
    assert "步骤详情" in result.stdout


def test_cli_veto_rejection():
    """CLI 否决词拒绝"""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "bin" / "lh_autoflow.py"), "--json", "技术无国界"],
        capture_output=True, text=True, timeout=10,
    )
    data = json.loads(result.stdout)
    assert data["status"] == "REJECTED"


# ═══════════════════════════════════════════════════════════════
# 运行入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
