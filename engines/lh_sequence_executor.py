#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 龍魂·序列执行引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-SEQUENCE-EXECUTOR-v1.0

把多个审计/识别/裁决引擎串成流水线，统一入口、统一输出、统一 DNA。

默认流水线：
  SafeAI 上下文安全 → KFPP 知识纯净度 → CSDN 内容审计 → 公正总裁裁决

用法:
  python3 engines/lh_sequence_executor.py --text "有人说只有他能教某技术"
  python3 engines/lh_sequence_executor.py --file article.md
  python3 engines/lh_sequence_executor.py --text "..." --pipeline safeai,csdn,judge
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------- 常量 ----------
OWNER = "龍芯北辰 UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_LABEL = "SEQUENCE"
TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"
DAY_ANCHOR = date(1949, 10, 1)
HEXAGRAM = "火雷噬嗑"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"

JUDGE_API = "http://119.13.90.27/api/judge"

DEFAULT_PIPELINE = ["safeai", "kfpp", "csdn", "judge"]


# ---------- 干支 DNA ----------
def ganzhi_year(y):
    return TIAN_GAN[(y - 4) % 10] + DI_ZHI[(y - 4) % 12]


def ganzhi_month(y, m):
    stem = ((y - 4) % 10 % 5) * 2 + m
    return TIAN_GAN[stem % 10] + DI_ZHI[m % 12]


def ganzhi_day(d):
    delta = (d - DAY_ANCHOR).days
    return TIAN_GAN[delta % 10] + DI_ZHI[delta % 12]


def four_pillars(d=None):
    d = d or date.today()
    return ganzhi_year(d.year), ganzhi_month(d.year, d.month), ganzhi_day(d)


_seq = 0


def stamp_dna():
    global _seq
    _seq += 1
    yg, mg, dg = four_pillars()
    return f"#龍芯⚡️{yg}·{mg}·{dg}·{HEXAGRAM}-{DNA_LABEL}-{_seq:06d}"


# ---------- 阶段定义 ----------
@dataclass
class StageResult:
    stage: str
    status: str  # ok / warn / block / error
    level: str   # PASS / L1 / L2 / L3 / L4 / N/A
    score: float
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)


# 自然语言引导前缀，进入流水线前自动剥离
_SEQ_PREFIX_PATTERNS = [
    r"^(?:帮我(?:们|你|大家)?(?:一个|一下|个|吧)?\s*)?(?:综合|完整|全量|联合|深度|简单|快速|一键)?(?:序列执行|流水线|综合审计|联合审计|审计|裁决|检测|审查|检查|判断|判定|过一遍|走一遍|跑一下|执行|启动|调用|使用)(?:一下|一次|一遍|一轮|流程|引擎|模式)?\s*[:：]?\s*",
    r"^(?:帮我(?:们|你|大家)?(?:一个|一下|个|吧)?\s*)",
    r"^(?:请(?:你|帮我|大家)?\s*)",
    r"^(?:麻烦你(?:一下|帮我)?\s*)",
]


def _strip_natural_prefixes(text: str) -> str:
    """去掉自然语言入口的引导词，保留真正要审计的内容"""
    changed = True
    while changed:
        changed = False
        for pat in _SEQ_PREFIX_PATTERNS:
            new_text = re.sub(pat, "", text, flags=re.IGNORECASE)
            if new_text != text:
                text = new_text
                changed = True
                break
    return text.strip()


class SequenceExecutor:
    """序列执行引擎"""

    def __init__(self, pipeline: Optional[List[str]] = None):
        self.pipeline = pipeline or DEFAULT_PIPELINE
        self.results: List[StageResult] = []

    def run(self, text: str, title: str = "") -> Dict[str, Any]:
        """执行完整流水线"""
        text = _strip_natural_prefixes(text)
        cst = timezone(timedelta(hours=8))
        self.results = []

        for stage in self.pipeline:
            try:
                if stage == "safeai":
                    result = self._stage_safeai(text)
                elif stage == "kfpp":
                    result = self._stage_kfpp(text)
                elif stage == "csdn":
                    result = self._stage_csdn(text, title)
                elif stage == "judge":
                    result = self._stage_judge(text)
                elif stage == "water_army":
                    result = self._stage_shell(text, "lh_behavioral_water_army_engine.py", "水军检测")
                elif stage == "lie_detector":
                    result = self._stage_shell(text, "lh_semantic_lie_detector.py", "语义测谎")
                elif stage == "robot_score":
                    result = self._stage_shell(text, "lh_robot_score.py", "机器人评分")
                elif stage == "code_audit":
                    result = self._stage_shell(text, "lh_code_guardian.py", "代码审计")
                else:
                    result = StageResult(stage, "error", "N/A", 0, f"未知阶段: {stage}")
            except Exception as e:
                result = StageResult(stage, "error", "N/A", 0, f"阶段异常: {e}")

            self.results.append(result)
            # 短路：L4 直接熔断
            if result.level == "L4":
                break

        final_level = self._final_level()
        return {
            "pipeline": self.pipeline,
            "input": {"title": title, "text_preview": text[:200]},
            "results": [self._result_to_dict(r) for r in self.results],
            "final_level": final_level,
            "final_summary": self._final_summary(final_level),
            "dna": stamp_dna(),
            "confirm_code": CONFIRM_CODE,
            "owner": OWNER,
            "timestamp": datetime.now(cst).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        }

    def _stage_safeai(self, text: str) -> StageResult:
        from engines.lh_safeai_engine import LonghunSafeEngine
        engine = LonghunSafeEngine(ledger_path=None)
        d = engine.process(text, subject_dna="sequence-executor")
        level = d.level
        status = "block" if level == "L4" else ("warn" if level in ("L1", "L2") else "ok")
        score = self._level_to_score(level)
        return StageResult(
            stage="safeai",
            status=status,
            level=level,
            score=score,
            summary=d.reason[:200],
            details={"action": d.action, "response": d.response_template},
        )

    def _stage_kfpp(self, text: str) -> StageResult:
        cmd = ["python3", str(BIN_DIR / "lh_kfpp_engine.py"), "--inspect", text, "--actor", "sequence-executor"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        data = self._extract_json(r.stdout) or {"level": "N/A", "message": r.stdout[:200] or r.stderr[:200]}
        level = data.get("level", "N/A")
        if isinstance(level, str):
            for lv in ["L4", "L3", "L2", "L1"]:
                if lv in level:
                    level = lv
                    break
        # KFPP 通过时返回 {"status": "通过"}
        if level == "N/A" and data.get("status") == "通过":
            level = "PASS"
        status = "block" if level == "L4" else ("warn" if level in ("L1", "L2", "L3") else "ok")
        return StageResult(
            stage="kfpp",
            status=status,
            level=level,
            score=self._level_to_score(level),
            summary=data.get("message", data.get("action", ""))[:200],
            details=data,
        )

    def _stage_csdn(self, text: str, title: str) -> StageResult:
        from engines.lh_csdn_auditor import CSDNAuditor
        auditor = CSDNAuditor()
        data = auditor.audit_text(text, title=title)
        passed = data.get("passed", False)
        status = "ok" if passed else "warn"
        score = data.get("score", 0)
        level = "PASS" if passed else ("L2" if score >= 40 else "L4")
        return StageResult(
            stage="csdn",
            status=status,
            level=level,
            score=score,
            summary=data.get("summary", "")[:200],
            details=data,
        )

    def _stage_judge(self, text: str) -> StageResult:
        payload = json.dumps({"content": text}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"{JUDGE_API}/judge",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return StageResult("judge", "error", "N/A", 0, f"调用公正总裁失败: {e}")
        output = data.get("output", "")
        # 尝试从输出提取裁决级别
        level = "PASS"
        for lv in ["L4", "L3", "L2", "L1", "PASS"]:
            if lv in output:
                level = lv
                break
        status = "block" if level == "L4" else ("warn" if level in ("L1", "L2", "L3") else "ok")
        return StageResult(
            stage="judge",
            status=status,
            level=level,
            score=self._level_to_score(level),
            summary=output[:200],
            details={"dna": data.get("dna", "")},
        )

    def _stage_shell(self, text: str, script: str, name: str) -> StageResult:
        cmd = ["python3", str(BIN_DIR / script)]
        r = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=60)
        output = r.stdout.strip() or r.stderr.strip()
        return StageResult(
            stage=name,
            status="ok" if r.returncode == 0 else "warn",
            level="N/A",
            score=50,
            summary=output[:200],
            details={"script": script, "returncode": r.returncode},
        )

    @staticmethod
    def _level_to_score(level: str) -> float:
        mapping = {"PASS": 100, "L1": 75, "L2": 50, "L3": 25, "L4": 0}
        return mapping.get(level, 50)

    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        """从 stdout 中提取第一个 JSON 对象"""
        import re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return None

    @staticmethod
    def _result_to_dict(r: StageResult) -> Dict[str, Any]:
        return {
            "stage": r.stage,
            "status": r.status,
            "level": r.level,
            "score": r.score,
            "summary": r.summary,
            "details": r.details,
        }

    def _final_level(self) -> str:
        order = ["L4", "L3", "L2", "L1", "PASS"]
        levels = [r.level for r in self.results]
        for lv in order:
            if lv in levels:
                return lv
        return "N/A"

    def _final_summary(self, final_level: str) -> str:
        if final_level == "L4":
            return "流水线触达 L4 熔断，建议立即阻止并启动人工复核。"
        elif final_level in ("L2", "L3"):
            return f"流水线触达 {final_level}，存在风险，建议整改后复审。"
        elif final_level == "L1":
            return "流水线触达 L1，存在轻微瑕疵，建议关注。"
        return "流水线通过，未发现明显风险。"


# ---------- CLI ----------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·序列执行引擎")
    parser.add_argument("--text", type=str, help="输入文本")
    parser.add_argument("--file", type=str, help="输入文件路径")
    parser.add_argument("--title", type=str, default="", help="标题")
    parser.add_argument("--pipeline", type=str, default=",".join(DEFAULT_PIPELINE),
                        help=f"流水线阶段，逗号分隔，默认: {','.join(DEFAULT_PIPELINE)}")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        text = path.read_text(encoding="utf-8")
        title = args.title or path.name
    elif args.text:
        text = args.text
        title = args.title
    else:
        parser.print_help()
        return

    pipeline = [s.strip() for s in args.pipeline.split(",") if s.strip()]
    executor = SequenceExecutor(pipeline=pipeline)
    report = executor.run(text, title=title)

    if args.raw:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 64)
        print("🔄 龍魂·序列执行引擎 v1.0")
        print("=" * 64)
        print(f"输入: {report['input']['text_preview']}")
        print(f"流水线: {' → '.join(report['pipeline'])}")
        print("-" * 64)
        for r in report["results"]:
            emoji = {"ok": "🟢", "warn": "🟡", "block": "🔴", "error": "⚠️"}.get(r["status"], "⚪")
            print(f"{emoji} [{r['stage']}] {r['level']} | 得分: {r['score']}")
            print(f"   {r['summary']}")
        print("-" * 64)
        print(f"最终级别: {report['final_level']}")
        print(f"结论: {report['final_summary']}")
        print(f"🧬 {report['dna']}")
        print("=" * 64)


if __name__ == "__main__":
    main()
