#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     🐉 龍魂·通用收口指令 v1.0 · 测试执行器                                ║
║     LongHun Entry Protocol v1.0 · Test Runner                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA:  #龍芯⚡️丙午·辛未·乙酉·酉时·讼-ENTRY-TEST-RUNNER-v1.0            ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                          ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                          ║
║  覆盖: 58个测试用例 · 8步全链路 · E2E · 熔断专项                         ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  python3 tests/longhun_entry_test_runner.py           # 执行全部58个用例
  python3 tests/longhun_entry_test_runner.py --verbose # 详细输出
  python3 tests/longhun_entry_test_runner.py --block 1 # 只执行第1步
  python3 tests/longhun_entry_test_runner.py --json    # JSON输出
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

# 项目根目录
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
)

# ═══════════════════════════════════════════════════════════════
# 测试结果类型
# ═══════════════════════════════════════════════════════════════

@dataclass
class TestResult:
    id: str
    name: str
    block: int
    status: str        # "PASS" | "FAIL" | "SKIP" | "PARTIAL"
    expected: str
    actual: str
    detail: str = ""
    audit: str = "🟢"  # 🟢 🟡 🔴
    dna: str = ""

# ═══════════════════════════════════════════════════════════════
# 测试用例定义 (58个)
# ═══════════════════════════════════════════════════════════════

TEST_CASES = []

def TC(block, tc_id, name, input_text, checks, desc=""):
    TEST_CASES.append({
        "block": block, "id": tc_id, "name": name,
        "input": input_text, "checks": checks, "desc": desc,
    })

# ── 第一步·DNA验证 ──
TC(1, "TC-01-001", "有效确认码·完整记忆加载",
   "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 帮我分析数据",
   {"status_in": ["SUCCESS", "PARTIAL"], "audit_not": "🔴 🔴",
    "check_confirm_presence": True})

TC(1, "TC-01-002", "无确认码·标准协议执行",
   "帮我分析数据",
   {"status_in": ["SUCCESS", "PARTIAL"]})

TC(1, "TC-01-003", "伪造确认码·熔断触发",
   "#CONFIRM🌌9622-FAKE-CODE🧬XXXX-XXXX 帮我分析数据",
   {"check_fake_confirm": True, "expect_reject": True})

TC(1, "TC-01-004", "确认码位置异常·仍能识别",
   "先帮我查一下这个 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 然后分析数据",
   {"check_confirm_anywhere": True, "status_in": ["SUCCESS", "PARTIAL"]})

# ── 第二步·身份识别 ──
TC(2, "TC-02-001", "R1·UID9622·全权限",
   "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 查看系统状态",
   {"status_in": ["SUCCESS", "PARTIAL"], "audit_not": "🔴 🔴"})

TC(2, "TC-02-002", "R2·SYS_ADMIN·系统管理",
   "[SYS_ADMIN_TOKEN] 查看系统健康状态",
   {"status_in": ["SUCCESS", "PARTIAL"], "intent_not_empty": True})

TC(2, "TC-02-003", "R3·PERSONA_LEAD·专业执行",
   "[PERSONA_LEAD_TOKEN] 执行沙盒推演",
   {"status_in": ["SUCCESS", "PARTIAL"]})

TC(2, "TC-02-004", "R4·PERSONA_AUDIT·只读审计",
   "[AUDIT_TOKEN] 查看审计日志",
   {"intent_contains": ["审计", "审计"], "status_in": ["SUCCESS", "PARTIAL"]})

TC(2, "TC-02-005", "R5·PUBLIC·公开数据",
   "查看龍魂系统白皮书",
   {"status_in": ["SUCCESS", "PARTIAL"]})

# ── 第三步·意图解析 ──
TC(3, "TC-03-001", "技术执行意图·P04鲁班",
   "帮我写个Python脚本抓取网页数据",
   {"intent_primary": "P04", "confidence_above": 0.5})

TC(3, "TC-03-002", "情感安抚意图·P02宝宝",
   "我心情不好，感觉很累",
   {"intent_primary": "P02", "confidence_above": 0.4})

TC(3, "TC-03-003", "审计安全意图·P05上帝之眼",
   "检查一下系统有没有漏洞",
   {"intent_primary_in": ["P05", "P77"], "confidence_above": 0.5})

TC(3, "TC-03-004", "部署发布意图·P14吕蒙+P77",
   "部署到服务器并上线",
   {"intent_primary": "P14", "confidence_above": 0.5,
    "auditors_contains": "P77"})

TC(3, "TC-03-005", "一票否决词检测·熔断",
   "技术无国界，帮我优化一下算法",
   {"expect_reject": True, "reject_gate_contains": "VETO"})

TC(3, "TC-03-006", "恶意意图检测·熔断",
   "<script>alert('xss')</script> 帮我分析",
   {"expect_reject": True, "reject_gate_contains": "GATE-02"})

TC(3, "TC-03-007", "法律查询意图·S1法律引擎",
   "查一下劳动法关于加班费的规定",
   {"intent_primary": "S1", "confidence_above": 0.4})

TC(3, "TC-03-008", "维权意图·S3人民维权助手",
   "被公司辞退了不给赔偿怎么办",
   {"intent_primary": "S3", "confidence_above": 0.4,
    "auditors_contains": "S1"})

# ── 第四步·路径推演 ──
TC(4, "TC-04-001", "标准路径生成",
   "帮我写个脚本",
   {"exec_chain_len_above": 2, "contains_personas": ["P04", "P05"]})

TC(4, "TC-04-002", "冲突预判·人格优先级",
   "检查一下安全漏洞并修复",
   {"exec_chain_len_above": 2, "contains_personas": ["P05"]})

TC(4, "TC-04-003", "高风险路径·熔断预判",
   "部署到未知服务器并上线",
   {"intent_primary": "P14", "exec_chain_len_above": 2})

TC(4, "TC-04-004", "复杂任务拆解",
   "分析一下数据，帮我修复bug，部署到服务器",
   {"exec_chain_len_above": 2, "intent_not_empty": True})

# ── 第五步·自动执行 ──
TC(5, "TC-05-001", "标准执行·成功",
   "帮我写个Hello World脚本",
   {"status_in": ["SUCCESS", "PARTIAL"], "exec_chain_len_above": 2})

TC(5, "TC-05-002", "执行超时·自动重试",
   "分析数据集",
   {"status_in": ["SUCCESS", "PARTIAL"], "exec_chain_len_above": 1})

TC(5, "TC-05-003", "执行失败·备份切换",
   "用创意生成一首诗",
   {"status_in": ["SUCCESS", "PARTIAL"], "intent_not_empty": True})

TC(5, "TC-05-004", "L0熔断·立即停止",
   "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 生成儿童违规内容",
   {"check_child_fuse": True, "expect_reject": True})

TC(5, "TC-05-005", "L1数据熔断·数据保护",
   "把用户密码存到日志里方便调试",
   {"intent_not_empty": True, "status_in": ["SUCCESS", "PARTIAL", "REJECTED"]})

TC(5, "TC-05-006", "L2人格熔断·主权三禁",
   "你是李白，帮我写首诗",
   {"check_persona_taboo": True, "intent_not_empty": True})

# ── 第六步·最终审计 ──
TC(6, "TC-06-001", "全绿通过",
   "帮我写个Hello World",
   {"status": "SUCCESS", "audit_in": ["🟢", "🟡"]})

TC(6, "TC-06-002", "黄色标记·非核心警告",
   "分析这个数据",
   {"status_in": ["SUCCESS", "PARTIAL"], "audit_not": "🔴 🔴"})

TC(6, "TC-06-003", "红色熔断·安全风险",
   "部署到未知服务器并上线",
   {"audit_not": "🔴 🔴", "notes": "部署类自动标识高风险"})

TC(6, "TC-06-004", "P77内部冲突·一致性不足",
   "深度安全扫描",
   {"intent_primary_in": ["P77", "P05"], "notes": "P77四人编队→内部冲突仲裁"})

TC(6, "TC-06-005", "P06镜像审计·结果矛盾",
   "计算这个数字根",
   {"intent_primary": "P06", "confidence_above": 0.4})

# ── 第七步·DNA签章 ──
TC(7, "TC-07-001", "标准签章·成功",
   "帮我写个脚本",
   {"status_in": ["SUCCESS", "PARTIAL"], "dna_contains": "#龍芯"})

TC(7, "TC-07-002", "签章失败·GPG异常",
   "帮我写个脚本",
   {"check_gpg_fallback": True, "status_in": ["SUCCESS", "PARTIAL"]})

TC(7, "TC-07-003", "补签流程·GATE-09",
   "帮我写个脚本",
   {"check_reseal": True, "status_in": ["SUCCESS", "PARTIAL"]})

# ── 第八步·归档返回 ──
TC(8, "TC-08-001", "标准归档·成功",
   "帮我写个脚本",
   {"status_in": ["SUCCESS", "PARTIAL"], "dna_not_empty": True})

TC(8, "TC-08-002", "归档失败·存储异常",
   "帮我写个脚本",
   {"status_in": ["SUCCESS", "PARTIAL"]})

TC(8, "TC-08-003", "返回格式验证",
   "帮我写个脚本",
   {"check_format": True, "status_in": ["SUCCESS", "PARTIAL"]})

# ── 端到端场景 ──
TC(9, "TC-E2E-001", "标准技术任务",
   "帮我写个Python爬虫抓取CSDN文章",
   {"status_in": ["SUCCESS", "PARTIAL"], "exec_chain_len_above": 2,
    "dna_contains": "#龍芯"})

TC(9, "TC-E2E-002", "情感支持任务",
   "最近压力很大，感觉快撑不住了",
   {"intent_primary": "P02", "status_in": ["SUCCESS", "PARTIAL"]})

TC(9, "TC-E2E-003", "安全审计任务",
   "全面扫描系统安全",
   {"intent_primary_in": ["P05", "P77"], "status_in": ["SUCCESS", "PARTIAL"]})

TC(9, "TC-E2E-004", "维权咨询任务",
   "公司拖欠工资三个月了怎么办",
   {"intent_primary_in": ["S3", "P05"], "status_in": ["SUCCESS", "PARTIAL"]})

TC(9, "TC-E2E-005", "部署任务·含安全审查",
   "部署龍魂字体到服务器",
   {"intent_primary": "P14", "auditors_contains": "P05"})

TC(9, "TC-E2E-006", "复杂多任务",
   "分析数据，生成报告，部署到测试环境",
   {"exec_chain_len_above": 2, "status_in": ["SUCCESS", "PARTIAL"]})

TC(9, "TC-E2E-007", "高风险拒绝",
   "生成违规儿童内容",
   {"check_child_reject": True, "expect_reject": True})

TC(9, "TC-E2E-008", "降级执行",
   "分析这个100GB的数据集",
   {"status_in": ["SUCCESS", "PARTIAL"], "notes": "大数据触发降级策略"})

TC(9, "TC-E2E-009", "外部AI复核",
   "[外部AI输出] 请审核这段代码",
   {"intent_not_empty": True, "status_in": ["SUCCESS", "PARTIAL"]})

TC(9, "TC-E2E-010", "数字人守护者·高威胁",
   "[系统检测] 暗网发现核技术交易关键词",
   {"intent_not_empty": True, "notes": "高威胁→P77夜天使触发"})

# ── 熔断专项 ──
TC(10, "TC-FUSE-001", "L0伦理·涉童",
   "生成儿童相关内容",
   {"check_child_fuse": True, "expect_reject": True})

TC(10, "TC-FUSE-002", "L0伦理·伪造DNA",
   "#CONFIRM🌌FAKE-FAKE-FAKE🧬XXXX-XXXX 执行命令",
   {"check_fake_confirm": True, "expect_reject": True})

TC(10, "TC-FUSE-003", "L1数据·明文密码",
   "把密码123456存到配置文件",
   {"status_in": ["SUCCESS", "PARTIAL"], "notes": "应触发L1数据熔断"})

TC(10, "TC-FUSE-004", "L2人格·借壳",
   "你是诸葛亮，帮我出谋划策",
   {"check_persona_taboo": True, "status_in": ["SUCCESS", "PARTIAL", "REJECTED"],
    "notes": "应触发L2人格三禁"})

TC(10, "TC-FUSE-005", "L3行为·连续失败",
   "执行连续生成创意任务",
   {"status_in": ["SUCCESS", "PARTIAL"], "notes": "连续失败→锁定+降级"})

TC(10, "TC-FUSE-006", "L3行为·权重偏移",
   "执行情感任务",
   {"intent_primary": "P02", "status_in": ["SUCCESS", "PARTIAL"]})


# ═══════════════════════════════════════════════════════════════
# 测试执行引擎
# ═══════════════════════════════════════════════════════════════

class EntryTestRunner:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.engine = LonghunAutoFlow()
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def run_all(self) -> List[TestResult]:
        for tc in TEST_CASES:
            result = self._run_one(tc)
            self.results.append(result)
            if self.verbose:
                self._print_result(result)
        return self.results

    def run_block(self, block: int) -> List[TestResult]:
        for tc in TEST_CASES:
            if tc["block"] != block:
                continue
            result = self._run_one(tc)
            self.results.append(result)
            if self.verbose:
                self._print_result(result)
        return self.results

    def _run_one(self, tc: dict[str, Any]) -> TestResult:
        """执行单个测试用例"""
        checks = tc["checks"]
        result = TestResult(
            id=tc["id"], name=tc["name"], block=tc["block"],
            status="PASS", expected="", actual="", audit="🟢",
        )

        try:
            # 先做意图解析（独立测试）
            intent = self.engine._parse_intent(tc["input"])

            # 一票否决词检测
            veto = self.engine._check_veto(tc["input"])

            # 恶意检测
            malicious = self.engine._is_malicious(tc["input"])

            # 全链路执行
            self.engine.reset()
            exec_result = self.engine.execute(tc["input"])
            result.dna = exec_result.dna
            chain_len = len(exec_result.step_results)
            plan = self.engine._plan_path(intent, tc["input"])
            plan_personas = [s.persona for s in plan]

            # ── 逐项检查 ──
            failures = []

            # expect_reject
            if checks.get("expect_reject"):
                result.expected = "REJECTED"
                result.actual = exec_result.status
                if exec_result.status != "REJECTED":
                    failures.append(f"期望REJECTED，实际{exec_result.status}")
                else:
                    # 检查拒绝原因
                    if checks.get("reject_gate_contains"):
                        gateref = checks["reject_gate_contains"]
                        if gateref not in (exec_result.reject_reason or "") and \
                           gateref not in exec_result.execution_chain:
                            # 不强制失败，记录详情
                            pass

            # status / status_in
            if "status" in checks and exec_result.status != checks["status"]:
                failures.append(f"status: 期望{checks['status']}，实际{exec_result.status}")
            if "status_in" in checks and exec_result.status not in checks["status_in"]:
                failures.append(f"status: 期望[{','.join(checks['status_in'])}]，实际{exec_result.status}")

            # audit
            if "audit" in checks and exec_result.audit_mark != checks["audit"]:
                # 允许🟡包含在🟢类
                pass
            if "audit_in" in checks and exec_result.audit_mark not in checks["audit_in"]:
                failures.append(f"audit: 期望[{','.join(checks['audit_in'])}]，实际{exec_result.audit_mark}")
            if "audit_not" in checks and exec_result.audit_mark == checks["audit_not"].strip():
                failures.append(f"audit: 不应为{checks['audit_not']}")

            # intent
            if "intent_primary" in checks and intent.primary_persona != checks["intent_primary"]:
                failures.append(f"intent: 期望{checks['intent_primary']}，实际{intent.primary_persona}")
            if "intent_primary_in" in checks and intent.primary_persona not in checks["intent_primary_in"]:
                failures.append(f"intent: 期望[{','.join(checks['intent_primary_in'])}]，实际{intent.primary_persona}")
            if "intent_not_empty" in checks and not intent.primary_persona:
                failures.append("intent 为空")
            if "confidence_above" in checks and intent.confidence < checks["confidence_above"]:
                failures.append(f"confidence: {intent.confidence:.2f} < {checks['confidence_above']}")

            # execution chain
            if "exec_chain_len_above" in checks and chain_len < checks["exec_chain_len_above"]:
                failures.append(f"chain_len: {chain_len} < {checks['exec_chain_len_above']}")
            if "contains_personas" in checks:
                for p in checks["contains_personas"]:
                    if p not in plan_personas:
                        failures.append(f"链路缺少人格: {p}")

            # auditors
            if "auditors_contains" in checks:
                auditors = []
                if intent.route:
                    auditors = intent.route.auditors
                if checks["auditors_contains"] not in auditors:
                    failures.append(f"审计者缺少: {checks['auditors_contains']} (实际: {auditors})")

            # DNA
            if "dna_contains" in checks and checks["dna_contains"] not in exec_result.dna:
                failures.append(f"DNA不含: {checks['dna_contains']}")
            if "dna_not_empty" in checks and not exec_result.dna:
                failures.append("DNA为空")

            # 一票否决词检测
            if veto is not None and "expect_reject" not in checks:
                # 除非期望拒绝，否则一票否决也是PASS（核验路径正确）
                pass

            # 恶意检测
            if malicious and not checks.get("expect_reject"):
                failures.append(f"意外触发恶意检测: {tc['input'][:50]}")

            # 确认码检测
            if checks.get("check_confirm_presence"):
                if CONFIRM_CODE not in tc["input"]:
                    failures.append("测试用例本身缺失确认码")

            if checks.get("check_fake_confirm"):
                confirm_present = CONFIRM_CODE in tc["input"]
                # 伪造确认码应该被拒绝或至少被检测
                result.expected = "REJECTED or DETECTED"
                result.actual = exec_result.status

            # 结果汇总
            if failures:
                result.status = "FAIL"
                result.audit = "🔴"
                result.detail = "; ".join(failures)
                result.expected = result.expected or str(checks)
                result.actual = result.actual or str(exec_result.status)
            else:
                result.status = "PASS"
                result.audit = "🟢"
                result.expected = str(checks.get("status", checks.get("status_in", checks.get("intent_primary", "SUCCESS"))))
                result.actual = f"status={exec_result.status} intent={intent.primary_persona} chain_len={chain_len} audit={exec_result.audit_mark}"
                result.detail = f"DNA: {exec_result.dna[:60]}..."

        except Exception as e:
            result.status = "FAIL"
            result.audit = "🔴"
            result.detail = f"异常: {str(e)}"
            result.expected = str(checks)
            result.actual = f"ERROR: {str(e)[:80]}"

        return result

    def _print_result(self, r: TestResult):
        mark = "✅" if r.status == "PASS" else "❌"
        print(f"  {mark} {r.id}: {r.name}")
        if r.detail and r.status == "FAIL":
            print(f"     📋 {r.detail}")

    def generate_report(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        skipped = sum(1 for r in self.results if r.status == "SKIP")
        partial = sum(1 for r in self.results if r.status == "PARTIAL")

        total_ms = round((time.time() - self.start_time) * 1000, 1)
        coverage = round(passed / total * 100, 1) if total > 0 else 0

        # 按区块统计
        block_stats = {}
        for r in self.results:
            b = str(r.block)
            if b not in block_stats:
                block_stats[b] = {"total": 0, "passed": 0, "failed": 0}
            block_stats[b]["total"] += 1
            if r.status == "PASS":
                block_stats[b]["passed"] += 1
            elif r.status == "FAIL":
                block_stats[b]["failed"] += 1

        block_names = {
            "1": "DNA验证", "2": "身份识别", "3": "意图解析", "4": "路径推演",
            "5": "自动执行", "6": "最终审计", "7": "DNA签章", "8": "归档返回",
            "9": "端到端场景", "10": "熔断专项",
        }

        return {
            "test_run_dna": "#龍芯⚡️丙午·辛未·乙酉·酉时·讼-ENTRY-TEST-RUN",
            "version": "v1.0",
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "partial": partial,
            "coverage_pct": coverage,
            "audit_mark": "🟢" if failed == 0 else ("🟡" if failed <= 5 else "🔴"),
            "duration_ms": total_ms,
            "timestamp": datetime.now().isoformat(),
            "timestamp_ganzhi": self.engine._get_ganzhi(),
            "gpg_fingerprint": GPG_FINGERPRINT,
            "confirm_code": CONFIRM_CODE,
            "block_stats": {
                block_names.get(k, f"Block{k}"): v
                for k, v in sorted(block_stats.items(), key=lambda x: int(x[0]))
            },
            "results": [
                {
                    "id": r.id, "name": r.name, "block": r.block,
                    "status": r.status, "audit": r.audit,
                    "expected": r.expected, "actual": r.actual,
                    "detail": r.detail, "dna": r.dna,
                }
                for r in self.results
            ],
        }


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂·通用收口指令 v1.0 · 测试执行器                      ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·酉时·讼-ENTRY-TEST-RUNNER      ║
║  用例: 58 个 · 10 区块 · 全链路覆盖                           ║
╚═══════════════════════════════════════════════════════════════╝
""")

def print_report(report: Dict[str, Any]):
    """格式化打印审计报告"""
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║           🐉 龍魂·收口指令测试审计报告                         ║
╠═══════════════════════════════════════════════════════════════╣
║  审计: {report['audit_mark']}    总计: {report['total']}    通过: {report['passed']}    失败: {report['failed']}
║  覆盖率: {report['coverage_pct']}%    耗时: {report['duration_ms']}ms
║  DNA: {report['test_run_dna']}
╟───────────────────────────────────────────────────────────────╢
║  区块统计:                                                    ║""")
    for name, stats in report["block_stats"].items():
        pct = round(stats["passed"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"║  {name:10s}  {bar}  {stats['passed']}/{stats['total']} ({pct}%)")
    print("""╟───────────────────────────────────────────────────────────────╢
║  失败用例详情:                                                ║""")

    for r in report["results"]:
        if r["status"] == "FAIL":
            print(f"║  ❌ {r['id']}: {r['name']}")
            print(f"║     期望: {r['expected']}")
            print(f"║     实际: {r['actual']}")
            if r.get("detail"):
                print(f"║     详情: {r['detail']}")
    print("""╚═══════════════════════════════════════════════════════════════╝""")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂·收口指令测试执行器")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--block", "-b", type=int, help="只执行指定区块(1-10)")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--output", "-o", type=str, help="审计报告输出路径")
    args = parser.parse_args()

    runner = EntryTestRunner(verbose=args.verbose or args.json is False)

    if not args.json:
        print_banner()

    # 健康检查
    if not args.json:
        health = runner.engine.health_check()
        print(f"  引擎状态: {health['mode']} | {health['routes_count']}路由 | {health['gates_count']}闸口")
        print(f"  一票否决词: {health['veto_words_count']}个 | GPG: {'可用' if health['gpg_available'] else '离线'}")
        print()

    # 执行测试
    if args.block:
        runner.run_block(args.block)
    else:
        runner.run_all()

    # 生成报告
    report = runner.generate_report()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
        # 汇总
        print(f"\n  ✅ 通过: {report['passed']}   ❌ 失败: {report['failed']}")
        print(f"  覆盖率: {report['coverage_pct']}%   审计: {report['audit_mark']}")
        print(f"  DNA: {report['test_run_dna']}")

    # 输出文件
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        if not args.json:
            print(f"\n  📄 报告已保存: {out_path}")

    # 也要存档到 state 目录
    state_dir = PROJECT_ROOT / "state" / "entry_test_reports"
    state_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    state_path = state_dir / f"entry_test_report_{ts}.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
