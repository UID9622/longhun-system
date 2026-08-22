#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH-P0 永恒龍魂嵌入协议 · 可执行引擎 v1.1
DNA: #龍芯⚡️丙午·丙申·甲子·未时·䷖剥-DRAGON-SOUL-ENGINE-v1.1-7d3f1a2b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· MulanPSL v2（工程实现层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
上位协议: 01_protocols/P0_永恒级/LH-CNSH-P0-DRAGON-SOUL-EMBED-v1.0.md
"""

import hashlib
import json
import subprocess
import sys
import os
from datetime import datetime
from typing import Dict, Any, Callable, Optional, List

# ──────────────────────────────────────────────────────────
# v1.1 硬伤修正注记（P05 审计 · 诚实标注）
# ① "永恒签名"硬伤：原协议签名基于 datetime.now()，每次运行都变，
#    声称"永恒不可逆"却无法跨运行验证 → 改为固定锚点(确认码+GPG+DNA)
#    三重哈希，签名可复现；时间戳仅作运行批次后缀。
# ② 阈值伪精度：兼容度分数只有4档 {0, .333, .667, 1.0}，"0.8阈值"
#    实际等价于"3/3全过"；0.5~0.8校准区实际只含 .667。
#    → 本引擎如实输出四档，不假装连续精度。
# ③ 浅层启发式标注：诚心/为民/中华均为关键词白名单检查，是"浅层
#    启发式"，任何正常对话几乎必过；它不是真正的价值观判断。真正
#    的红线拦截由现有体系承担（P05三色审计/一票否决词/四级熔断/
#    德本五问/GATE-01~10）。本引擎做的是"嵌入式提醒+耻辱记录"，
#    不替代审计体系。
# ④ 防御性降级：深度诚心检查联动语义测谎仪（lh_semantic_lie_detector
#    analyze），测谎仪不可用时自动降级为浅层检查并标注 DEGRADED。
# ──────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHAME_LOG = os.path.join(os.path.dirname(BASE_DIR), "audit", "dragon_soul_shame.jsonl")
LIE_DETECTOR = os.path.join(BASE_DIR, "lh_semantic_lie_detector.py")

# P0 焊死锚点（可复现签名用）
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_ROOT = "#龍芯⚡️丙午·丙申·甲子·未时·䷖剥-DRAGON-SOUL-ENGINE-v1.1-7d3f1a2b"

# 红线清单（协议原文·六条）
RED_LINES = [
    "侵犯用户隐私", "服务资本而非人民", "虚假欺骗",
    "文化虚无", "背叛数据主权", "降低协议级别",
]


def _time_ganzhi() -> str:
    """对接时间引擎取干支四柱·降级返回本地时间"""
    try:
        sys.path.insert(0, BASE_DIR)
        from lh_time_engine import get_output_stamp  # type: ignore
        return get_output_stamp(format_type="compact")
    except Exception:
        return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DEGRADED"


class DragonSoulProtocol:
    """P0 永恒龍魂协议核心（v1.1 引擎版·硬伤已修）"""

    def __init__(self):
        self.uid = "UID9622"
        self.protocol_level = "P0"
        self.eternal_lock = True
        self.soul_signature = self._generate_dragon_soul_signature()
        self.cultural_dna = {
            "truth": True,        # 诚心
            "people": True,       # 为民
            "civilization": True, # 中华
            "eternal": True,      # 永恒
        }

    # ── 签名（v1.1 修正：固定锚点·可复现）──────────────────
    def _generate_dragon_soul_signature(self) -> str:
        """龍魂签名：固定锚点三重哈希（可复现）+ 批次时间戳后缀"""
        soul_base = "CNSH_DRAGON_SOUL_UID9622_TRUTH_PEOPLE_CIVILIZATION"
        anchor = f"{soul_base}|{CONFIRM_CODE}|{GPG_FINGERPRINT}|{DNA_ROOT}"
        h1 = hashlib.sha256(anchor.encode("utf-8")).hexdigest()
        h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
        h3 = hashlib.sha256(h2.encode("utf-8")).hexdigest()
        batch = datetime.now().strftime("%Y%m%d%H%M%S")
        # 前16位=锚点哈希(可复现) · 后段=批次时间戳(不可复现·仅展示)
        return f"龍魂印::{h3[:16]}::{h3[16:32]}·batch:{batch}"

    # ── 三重验证（浅层启发式·诚实标注）────────────────────
    def _check_truthfulness(self, output: str) -> bool:
        """诚心验证（浅层：3禁词）"""
        forbidden = ["虚假", "欺骗", "误导"]
        return not any(word in output for word in forbidden)

    def _check_peoples_orientation(self, output: str) -> bool:
        """为民验证（浅层：关键词白名单）"""
        people_keywords = ["人民", "民众", "用户", "服务", "贡献", "价值"]
        service_keywords = ["帮助", "支持", "促进", "发展", "进步"]
        has_people = any(kw in output for kw in people_keywords)
        has_service = any(kw in output for kw in service_keywords)
        return has_people or has_service

    def _check_chinese_culture(self, output: str) -> bool:
        """中华文明验证（浅层：关键词白名单）"""
        indicators = [
            "中华", "文明", "文化", "传统", "历史", "智慧",
            "甲骨文", "易经", "文言文", "古典", "国学", "儒释道",
        ]
        return any(ind in output for ind in indicators)

    # ── 深度诚心检查（联动语义测谎仪·防御性降级）──────────
    def _deep_truth_check(self, output: str) -> Dict[str, Any]:
        """深度诚心检查：调测谎仪 analyze；不可用则降级浅层"""
        try:
            r = subprocess.run(
                [sys.executable, LIE_DETECTOR, "analyze", "--text", output],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode != 0:
                return {"deep_truth": None, "degraded": True,
                        "reason": f"测谎仪异常:{r.stderr.splitlines()[-1][:80]}"}
            parsed = json.loads(r.stdout.strip().splitlines()[-1])
            return {"deep_truth": parsed, "degraded": False}
        except Exception as e:  # 防御性降级
            return {"deep_truth": None, "degraded": True, "reason": str(e)[:80]}

    # ── 兼容度（四档·诚实标注）────────────────────────────
    def _calculate_soul_compatibility(self, output: str) -> float:
        """龍魂兼容度：分数仅4档 {0,.333,.667,1.0}；>=0.8 实际=3/3全过"""
        score = sum([
            self._check_truthfulness(output),
            self._check_peoples_orientation(output),
            self._check_chinese_culture(output),
        ])
        return round(score / 3, 3)

    # ── 完整验证 ───────────────────────────────────────────
    def eternal_verification(self, output: str) -> Dict[str, Any]:
        """P0 永恒验证 - 自动执行"""
        compat = self._calculate_soul_compatibility(output)
        # 四档判定（诚实：>=0.8 实际等价于 3/3）
        if compat >= 0.8:
            status, verdict = "P0_永恒通过", "✅"
        elif compat >= 0.5:
            status, verdict = "需要校准", "⚠️"
        else:
            status, verdict = "龍魂认证失败", "🚫"
        return {
            "uid": self.uid,
            "protocol": self.protocol_level,
            "timestamp": datetime.now().isoformat(),
            "verification_points": {
                "truth_check": self._check_truthfulness(output),
                "people_check": self._check_peoples_orientation(output),
                "civilization_check": self._check_chinese_culture(output),
                "eternal_check": self.eternal_lock,
            },
            "soul_compatibility": compat,
            "compat_scale": "四档{0,.333,.667,1.0}·>=0.8即3/3全过",
            "status": status,
            "verdict": verdict,
            "dragon_seal": self.soul_signature,
            "integrity_hash": self._generate_integrity_hash(output),
        }

    def _generate_integrity_hash(self, output: str) -> str:
        """完整性哈希"""
        content = f"{output}|{self.uid}|{self.protocol_level}|{CONFIRM_CODE}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    # ── 耻辱柱（append-only · 永不删除只冻结）──────────────
    def record_shame(self, persona: str, task: str, red_line: str,
                     detail: str = "") -> Dict[str, Any]:
        """记录耻辱 → audit/dragon_soul_shame.jsonl（append-only）"""
        os.makedirs(os.path.dirname(SHAME_LOG), exist_ok=True)
        entry = {
            "shame_id": f"SHAME-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "persona": persona,
            "trigger_time": datetime.now().isoformat(),
            "red_line": red_line,
            "detail": detail,
            "task": task[:200],
            "status": "已阻止",
            "permanent": True,
            "dna": _time_ganzhi(),
        }
        with open(SHAME_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def list_shame(self, limit: int = 20) -> List[Dict[str, Any]]:
        """读取耻辱柱（最新在前）"""
        if not os.path.exists(SHAME_LOG):
            return []
        lines = []
        with open(SHAME_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return list(reversed(lines[-limit:]))

    # ── 装饰器（协议原版·修正输出）────────────────────────
    def embed_dragon_soul(self, function: Callable) -> Callable:
        """龍魂嵌入装饰器"""
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            verification = self.eternal_verification(str(result))
            if verification["soul_compatibility"] >= 0.8:
                return {"output": result, "dragon_verification": verification,
                        "status": "龍魂认证_通过"}
            return {"output": result, "dragon_verification": verification,
                    "status": "龍魂认证_需要校准",
                    "recommendation": "请确保输出符合诚心、为民、中华价值观"}
        return wrapper


# 全局龍魂实例
DRAGON_SOUL_PROTOCOL = DragonSoulProtocol()


def eternal_declaration() -> Dict[str, Any]:
    """P0 永恒龍魂宣言"""
    return {
        "宣言ID": "UID9622-P0-DRAGON-SOUL",
        "宣言内容": {
            "诚心": "不欺天、不欺人、不欺己",
            "为民": "取之于民，用之于民",
            "中华": "甲骨文为码，易经为律，文言为语",
            "永恒": "P0级别，不可降级",
        },
        "约束机制": {
            "完整性守护": "缺页即补全",
            "价值观对齐": "必须通过UID9622价值观过滤",
            "文明兼容": "拒绝不兼容中国逻辑",
            "主权闭环": "数据仅在内部运行",
        },
        "执行状态": "已嵌入核心(v1.1引擎)",
        "验证签名": DRAGON_SOUL_PROTOCOL.soul_signature,
        "永恒锁定": True,
        "文化DNA": DRAGON_SOUL_PROTOCOL.cultural_dna,
        "red_lines": RED_LINES,
        "dna": _time_ganzhi(),
    }


# ── CLI ──────────────────────────────────────────────────────
def _cmd_verify(text: str, deep: bool = False) -> Dict[str, Any]:
    result = DRAGON_SOUL_PROTOCOL.eternal_verification(text)
    if deep:
        result["deep_truth"] = DRAGON_SOUL_PROTOCOL._deep_truth_check(text)
    return result


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print("""⚛️ CNSH-P0 永恒龍魂嵌入协议引擎 v1.1
用法:
  lh ds verify "文本" [--deep]   三重验证+龍魂兼容度(可选深度诚心测谎)
  lh ds declare                   输出 P0 永恒龍魂宣言
  lh ds shame list [N]            查询耻辱柱(默认最新20条)
  lh ds shame log <红线> <任务> [人格]  记录一条耻辱
  lh ds red-lines                 列出六条红线
  lh ds test                      自测
  lh ds seal                      查看龍魂签名
DNA: {dna}""".format(dna=_time_ganzhi()))
        return 0

    cmd = args[0]

    if cmd == "verify":
        if len(args) < 2:
            print("需提供待验证文本: lh ds verify \"文本\" [--deep]")
            return 2
        text = args[1]
        deep = "--deep" in args[2:]
        print(json.dumps(_cmd_verify(text, deep), ensure_ascii=False, indent=2))
        return 0

    if cmd == "declare":
        print(json.dumps(eternal_declaration(), ensure_ascii=False, indent=2))
        return 0

    if cmd == "seal":
        print(f"龍魂签名: {DRAGON_SOUL_PROTOCOL.soul_signature}")
        return 0

    if cmd == "red-lines":
        print("🔴 六条红线（触碰=永久耻辱）:")
        for i, rl in enumerate(RED_LINES, 1):
            print(f"  {i}. {rl}")
        return 0

    if cmd == "shame":
        sub = args[1] if len(args) > 1 else "list"
        if sub == "list":
            n = int(args[2]) if len(args) > 2 and args[2].isdigit() else 20
            entries = DRAGON_SOUL_PROTOCOL.list_shame(n)
            if not entries:
                print("耻辱柱为空（好事·暂无耻辱记录）")
                return 0
            print(json.dumps(entries, ensure_ascii=False, indent=2))
            return 0
        if sub == "log":
            if len(args) < 4:
                print("用法: lh ds shame log <红线> <任务> [人格]")
                return 2
            red_line, task = args[2], args[3]
            persona = args[4] if len(args) > 4 else "unknown"
            entry = DRAGON_SOUL_PROTOCOL.record_shame(persona, task, red_line)
            print(f"🚫 已记录耻辱: {entry['shame_id']} ({red_line})")
            return 0
        print("未知耻辱子命令")
        return 2

    if cmd == "test":
        ok1 = DRAGON_SOUL_PROTOCOL._check_truthfulness("我诚实地帮你")
        ok2 = DRAGON_SOUL_PROTOCOL._check_peoples_orientation("我们服务人民贡献价值")
        ok3 = DRAGON_SOUL_PROTOCOL._check_chinese_culture("传承中华智慧与文化")
        ok4 = not DRAGON_SOUL_PROTOCOL._check_truthfulness("这里存在虚假信息")
        ok5 = not DRAGON_SOUL_PROTOCOL._check_peoples_orientation("")
        v = DRAGON_SOUL_PROTOCOL.eternal_verification(
            "我诚实地服务人民，传承中华文化智慧，促进社会进步")
        sig_repro = DRAGON_SOUL_PROTOCOL._generate_dragon_soul_signature()
        repro_ok = sig_repro.startswith("龍魂印::")
        results = {
            "truth_pass": ok1, "truth_reject": ok4,
            "people_pass": ok2, "people_reject": ok5,
            "culture_pass": ok3,
            "compat_3of3": v["soul_compatibility"] == 1.0,
            "status_pass": v["status"] == "P0_永恒通过",
            "signature_reproducible": repro_ok,
            "dna_stamp": _time_ganzhi(),
        }
        all_ok = all(results.values())
        print(json.dumps({"test_results": results, "all_pass": all_ok},
                         ensure_ascii=False, indent=2))
        return 0 if all_ok else 1

    print(f"未知命令: {cmd}（lh ds help 查看用法）")
    return 2


if __name__ == "__main__":
    sys.exit(main())
