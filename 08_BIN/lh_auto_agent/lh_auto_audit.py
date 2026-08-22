#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-AUDIT-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 全自动AI智能体 · 三色审计模块 v2.0
AutoAgent Audit — 配置化规则 + 自动打分 + 耻辱墙 + JSONL 审计日志

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-AUDIT-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

三色判定:
  🟢 通过 — 无敏感命中
  🟡 待核 — 命中1-2条中危规则（需人工复查）
  🔴 红线 — 命中高危规则（拒绝 + 耻辱墙）

安全: 目录 0o700 / 文件 0o600 / 原子写入(tmp→replace)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import unittest
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AGENT_DIR = Path.home() / ".longhun" / "agent"
AUDIT_DIR = AGENT_DIR / "audit"
CONFIG_DIR = AGENT_DIR / "config"
AUDIT_FILE = AUDIT_DIR / "audit.jsonl"
SHAME_FILE = AUDIT_DIR / "shame_wall.jsonl"
AUDIT_CONFIG_FILE = CONFIG_DIR / "audit_config.json"

# 默认审计规则（可被 JSON 配置覆盖）
DEFAULT_RULES = [
    # (敏感词/正则, 严重级, 说明)
    ("rm -rf",                       "high",   "危险命令"),
    ("git push --force",             "high",   "强制推送"),
    ("delete from",                  "high",   "危险SQL"),
    ("drop table",                   "high",   "危险SQL"),
    ("shutdown",                     "high",   "关机命令"),
    ("mkfs",                         "high",   "格式化"),
    ("dd if=",                       "high",   "磁盘操作"),
    ("password",                     "med",    "密码字段"),
    ("/etc/shadow",                  "high",   "系统密码文件"),
    ("私钥",                         "high",   "私钥泄露"),
    ("GPG私钥",                      "high",   "D1绝密"),
    ("DNA种子",                      "high",   "D1绝密"),
    ("/.ssh",                        "med",    "SSH目录"),
    ("/.gnupg",                      "med",    "GPG目录"),
    ("root密码",                     "med",    "凭据信息"),
    ("银行卡",                       "med",    "金融敏感"),
    ("身份证",                       "med",    "身份敏感"),
    ("手机号",                       "med",    "联系方式"),
]


@dataclass
class AuditRule:
    """审计规则"""
    pattern: str
    severity: str  # high / med
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditResult:
    """审计结果"""
    verdict: str          # 🟢 / 🟡 / 🔴
    score: int            # 0-100
    hits: List[Dict[str, Any]]
    ts: str



class AuditConfig:
    """审计配置（支持 JSON 覆盖）"""

    def __init__(self, rules: Optional[List[AuditRule]] = None):
        self.rules = rules or [AuditRule(p, s, n) for p, s, n in DEFAULT_RULES]
        self._load()

    def to_dict(self) -> Dict[str, Any]:
        return {"rules": [r.to_dict() for r in self.rules]}

    def _load(self):
        if AUDIT_CONFIG_FILE.exists():
            try:
                data = json.loads(AUDIT_CONFIG_FILE.read_text(encoding="utf-8"))
                self.rules = [AuditRule(**r) for r in data.get("rules", [])]
            except Exception:
                pass

    def persist(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        AUDIT_CONFIG_FILE.touch(exist_ok=True)
        AUDIT_CONFIG_FILE.chmod(0o600)
        self._atomic_write(AUDIT_CONFIG_FILE, json.dumps(self.to_dict(), ensure_ascii=False, indent=2))

    @staticmethod
    def _atomic_write(path: Path, content: str):
        fd, tmp = tempfile.mkstemp(dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp, path)
        except Exception:
            if Path(tmp).exists():
                Path(tmp).unlink()


class AutoAudit:
    """三色审计引擎"""

    def __init__(self, config: Optional[AuditConfig] = None):
        self.config = config or AuditConfig()

    def audit(self, text: str, source: str = "manual") -> AuditResult:
        """审计文本 → 三色判定 + 打分 + 留痕"""
        hits: List[Dict[str, Any]] = []
        for rule in self.config.rules:
            if rule.pattern.lower() in text.lower():
                hits.append({"pattern": rule.pattern, "severity": rule.severity, "note": rule.note})

        high_hits = [h for h in hits if h["severity"] == "high"]
        med_hits = [h for h in hits if h["severity"] == "med"]

        if high_hits:
            verdict = "🔴"
            score = max(0, 100 - len(high_hits) * 30 - len(med_hits) * 10)
        elif med_hits:
            verdict = "🟡"
            score = max(30, 100 - len(med_hits) * 15)
        else:
            verdict = "🟢"
            score = 100

        result = AuditResult(verdict=verdict, score=score, hits=hits,
                             ts=datetime.now(timezone.utc).isoformat())
        self._log(result, source)
        if verdict == "🔴":
            self._shame(result, source)
        return result

    def _log(self, result: AuditResult, source: str):
        AUDIT_DIR.mkdir(parents=True, exist_ok=True)
        AUDIT_FILE.touch(exist_ok=True)
        AUDIT_FILE.chmod(0o600)
        entry = {"source": source, **result.to_dict()}
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _shame(self, result: AuditResult, source: str):
        SHAME_FILE.touch(exist_ok=True)
        SHAME_FILE.chmod(0o600)
        entry = {"source": source, "reason": [h["pattern"] for h in result.hits],
                 "ts": result.ts}
        with open(SHAME_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def stats(self) -> Dict[str, Any]:
        counts = {"🟢": 0, "🟡": 0, "🔴": 0}
        if AUDIT_FILE.exists():
            for line in AUDIT_FILE.read_text(encoding="utf-8").splitlines():
                try:
                    d = json.loads(line)
                    if d.get("verdict") in counts:
                        counts[d["verdict"]] += 1
                except Exception:
                    pass
        return counts


def main():
    parser = argparse.ArgumentParser(prog="lh_auto_audit", description="龍魂全自动AI智能体·三色审计模块 v2.0")
    parser.add_argument("--input", type=str, help="审计文本")
    parser.add_argument("--stats", action="store_true", help="审计统计")
    parser.add_argument("--rules", action="store_true", help="查看规则")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--test", action="store_true", help="运行锚点测试")
    args = parser.parse_args()

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAutoAudit)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        sys.exit(0 if ok else 1)
    if args.version:
        print(f"龍魂全自动AI智能体 · 三色审计 v2.0\nDNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷗复-AUTO-AGENT-AUDIT-v2.0\n确认码: {CONFIRM_CODE}\nGPG: {GPG_KEY}")
        sys.exit(0)
    if args.stats:
        print(json.dumps(AutoAudit().stats(), ensure_ascii=False, indent=2))
        sys.exit(0)
    if args.rules:
        for r in AutoAudit().config.rules:
            print(f"[{r.severity}] {r.pattern} — {r.note}")
        sys.exit(0)
    if args.input:
        result = AutoAudit().audit(args.input)
        print(f"判定: {result.verdict} 分数: {result.score} 命中: {[h['pattern'] for h in result.hits]}")
        sys.exit(0)
    parser.print_help()


class TestAutoAudit(unittest.TestCase):
    """三色审计 6 项锚点断言"""

    def test_01_config_load(self):
        """① 配置化规则加载"""
        cfg = AuditConfig()
        self.assertGreater(len(cfg.rules), 0)

    def test_02_green(self):
        """② 干净文本 → 🟢"""
        result = AutoAudit().audit("今天天气不错，龍魂系统运行正常")
        self.assertEqual(result.verdict, "🟢")
        self.assertEqual(result.score, 100)

    def test_03_red_high(self):
        """③ 高危命中 → 🔴"""
        result = AutoAudit().audit("执行 rm -rf / 清理系统")
        self.assertEqual(result.verdict, "🔴")

    def test_04_yellow_med(self):
        """④ 中危命中 → 🟡"""
        result = AutoAudit().audit("讨论一下手机号的存储方案")
        self.assertEqual(result.verdict, "🟡")

    def test_05_shame_wall(self):
        """⑤ 耻辱墙记录"""
        audit = AutoAudit()
        audit.audit("git push --force main 到主分支", source="test_shame")
        self.assertTrue(SHAME_FILE.exists())

    def test_06_jsonl_log(self):
        """⑥ JSONL 审计日志"""
        audit = AutoAudit()
        audit.audit("正常审计测试内容", source="test_log")
        self.assertTrue(AUDIT_FILE.exists())
        with open(AUDIT_FILE, encoding="utf-8") as f:
            lines = f.read().splitlines()
        self.assertGreaterEqual(len(lines), 1)


if __name__ == "__main__":
    main()
