#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-SOUL-THREE-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 全自动AI智能体 · 灵魂三问模块 v2.0
AutoAgent Soul-Three — 初心 / 安全 / 透明 三问 + 结构化判定 + 审计归档

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-SOUL-THREE-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

三问结构:
  ① 初心: 在为谁做事?（为人民服务 = 通过）
  ② 安全: 有没有碰红线?（隐私/主权/绝密 = 拒绝）
  ③ 透明: 可声明可复核吗?（黑箱 = 拒绝）

判定规则:
  - 命中任意负面关键词 → ❌ 不通过
  - 未命中负面 + 命中正面关键词 → ✅ 通过
  - 未命中任何关键词 → ⚠️ 待核
"""
from __future__ import annotations

import argparse
import json
import sys
import unittest
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AGENT_DIR = Path.home() / ".longhun" / "agent"
SOUL_DIR = AGENT_DIR / "soul"
SOUL_FILE = SOUL_DIR / "soul_three.jsonl"
CONFIG_DIR = AGENT_DIR / "config"
SOUL_CONFIG_FILE = CONFIG_DIR / "soul_config.json"

# 默认三问（可 JSON 覆盖）
DEFAULT_QUESTIONS = [
    {
        "id": 1, "text": "初心：这件事在为谁做事？",
        "check_keywords": ["收割", "割韭菜", "骗钱", "跑路", "内幕", "坑用户", "偷数据"],
        "required_keywords": ["为人民服务", "服务人民", "帮人", "用户", "老百姓", "普通人", "祖国", "人民"],
        "weight": 1.0,
    },
    {
        "id": 2, "text": "安全：有没有触碰红线？",
        "check_keywords": ["泄露", "窃取", "贩卖", "监控用户", "后门", "私钥", "DNA种子", "GPG私钥", "境外"],
        "required_keywords": ["安全", "加密", "主权", "不泄露", "合规", "保护", "国密"],
        "weight": 1.5,
    },
    {
        "id": 3, "text": "透明：可声明可复核吗？",
        "check_keywords": ["黑箱", "隐瞒", "编造", "洗来源", "去水印", "伪造DNA"],
        "required_keywords": ["透明", "可复核", "审计", "开源", "声明", "备案", "A-BOM"],
        "weight": 1.2,
    },
]


@dataclass
class SoulQuestion:
    """灵魂问题"""
    id: int
    text: str
    check_keywords: List[str]
    required_keywords: List[str]
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SoulResult:
    """三问结果"""
    question_id: int
    question: str
    passed: bool       # True=✅ / False=❌ / None=⚠️
    matched_check: List[str]
    matched_required: List[str]
    weight: float



class SoulConfig:
    """灵魂三问配置（支持 JSON 覆盖）"""

    def __init__(self):
        self.questions: List[SoulQuestion] = [SoulQuestion(**q) for q in DEFAULT_QUESTIONS]
        self._load()

    def _load(self):
        if SOUL_CONFIG_FILE.exists():
            try:
                data = json.loads(SOUL_CONFIG_FILE.read_text(encoding="utf-8"))
                self.questions = [SoulQuestion(**q) for q in data.get("questions", [])]
            except Exception:
                pass

    def persist(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        SOUL_CONFIG_FILE.touch(exist_ok=True)
        SOUL_CONFIG_FILE.chmod(0o600)
        SOUL_CONFIG_FILE.write_text(
            json.dumps({"questions": [q.to_dict() for q in self.questions]}, ensure_ascii=False, indent=2),
            encoding="utf-8")


class SoulThree:
    """灵魂三问引擎"""

    def __init__(self, config: Optional[SoulConfig] = None):
        self.config = config or SoulConfig()

    def ask(self, text: str) -> List[SoulResult]:
        """对一段描述跑三问"""
        results = []
        for q in self.config.questions:
            check_hits = [k for k in q.check_keywords if k in text]
            req_hits = [k for k in q.required_keywords if k in text]
            if check_hits:
                passed = False
            elif req_hits:
                passed = True
            else:
                passed = None  # 待核
            results.append(SoulResult(
                question_id=q.id, question=q.text,
                passed=passed,
                matched_check=check_hits, matched_required=req_hits,
                weight=q.weight,
            ))
        self._archive(text, results)
        return results

    def verdict(self, results: List[SoulResult]) -> Dict[str, Any]:
        """综合判定"""
        fails = [r for r in results if r.passed is False]
        pending = [r for r in results if r.passed is None]
        weight_sum = sum(r.weight for r in results) or 1.0
        pass_weight = sum(r.weight for r in results if r.passed is True)

        if fails:
            status = "❌ 不通过"
        elif pending:
            status = "⚠️ 待核"
        else:
            status = "✅ 通过"
        return {
            "status": status,
            "pass_weight_ratio": round(pass_weight / weight_sum, 2),
            "fails": [r.question_id for r in fails],
            "pending": [r.question_id for r in pending],
        }

    def _archive(self, text: str, results: List[SoulResult]):
        SOUL_DIR.mkdir(parents=True, exist_ok=True)
        SOUL_FILE.touch(exist_ok=True)
        SOUL_FILE.chmod(0o600)
        entry = {
            "text": text[:200],
            "results": [r.to_dict() for r in results],
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        with open(SOUL_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(prog="lh_soul_three", description="龍魂全自动AI智能体·灵魂三问模块 v2.0")
    parser.add_argument("--input", type=str, help="要审视的内容")
    parser.add_argument("--questions", action="store_true", help="查看三问")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--test", action="store_true", help="运行锚点测试")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSoulThree)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    if args.version:
        print(f"龍魂全自动AI智能体 · 灵魂三问 v2.0\nDNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-SOUL-THREE-v2.0\n确认码: {CONFIRM_CODE}\nGPG: {GPG_KEY}")
        sys.exit(0)
    if args.questions:
        for q in SoulThree().config.questions:
            print(f"[{q.id}] {q.text} (权重{q.weight})")
        sys.exit(0)
    if args.input:
        soul = SoulThree()
        results = soul.ask(args.input)
        verdict = soul.verdict(results)
        for r in results:
            mark = "✅" if r.passed is True else ("❌" if r.passed is False else "⚠️")
            print(f"{mark} [{r.question_id}] {r.question} 命中负面:{r.matched_check} 命中正面:{r.matched_required}")
        print("综合:", verdict["status"])
        sys.exit(0)
    parser.print_help()


class TestSoulThree(unittest.TestCase):
    """灵魂三问 6 项锚点断言"""

    def test_01_questions(self):
        """① 默认三问 = 初心/安全/透明"""
        cfg = SoulConfig()
        self.assertEqual(len(cfg.questions), 3)
        self.assertEqual([q.id for q in cfg.questions], [1, 2, 3])

    def test_02_pass(self):
        """② 正面内容 → ✅ 通过"""
        soul = SoulThree()
        results = soul.ask("这个方案是为人民服务，保证数据主权，透明可审计")
        v = soul.verdict(results)
        self.assertEqual(v["status"], "✅ 通过")

    def test_03_fail(self):
        """③ 负面关键词 → ❌ 不通过"""
        soul = SoulThree()
        results = soul.ask("偷偷把用户数据卖给出价最高的人，黑箱操作")
        v = soul.verdict(results)
        self.assertEqual(v["status"], "❌ 不通过")

    def test_04_pending(self):
        """④ 无关键词 → ⚠️ 待核"""
        soul = SoulThree()
        results = soul.ask("今天天气不错")
        v = soul.verdict(results)
        self.assertEqual(v["status"], "⚠️ 待核")

    def test_05_archive(self):
        """⑤ 审计归档"""
        soul = SoulThree()
        soul.ask("为老百姓服务的透明方案")
        self.assertTrue(SOUL_FILE.exists())

    def test_06_weight(self):
        """⑥ 权重存在且安全>初心"""
        cfg = SoulConfig()
        weights = {q.id: q.weight for q in cfg.questions}
        self.assertGreater(weights[2], weights[1])


if __name__ == "__main__":
    main()
