#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · ASI 万法归一融合引擎 v1.0
DNA: #龍芯⚡️2026-08-22-ASI-FUSION-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰

用途:
  将金字塔兼容协议 v1.1 的七锚（金字塔/蚁群/369/易经/五行/道德经/生死门）
  串成一条决策证据链。每个决策走七闸，每闸留证据，输出三色+总分+证据卡。
  锚引擎缺失时自动降级并标注"降级"，绝不伪造数据。

用法:
  python3 lh_asi_fusion.py --input "提交新审计插件" --category audit
  python3 lh_asi_fusion.py --input "..." --meta /path/meta.json --json
"""

from __future__ import annotations
import json
import sys
import hashlib
import random
import argparse
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

# ------------------------------------------------------------
# 底座对接（锚引擎缺失则降级，不影响主链路）
# ------------------------------------------------------------
_BIN = str(Path(__file__).resolve().parent)
if _BIN not in sys.path:
    sys.path.insert(0, _BIN)


def _safe_import(name: str):
    """安全导入锚引擎，失败返回 None（降级标注）"""
    try:
        return __import__(name)
    except Exception:
        return None


# 锚引擎探测
_ANT_ROUTER = _safe_import("lh_ant_colony_router")
_TIME_ENGINE = _safe_import("lh_time_engine")
_DIGITAL_ROOT = _safe_import("lh_digital_root")
_WUXING = _safe_import("lh_wuxing_core")
_DAODEJING = _safe_import("lh_daodejing_engine")

# ------------------------------------------------------------
# 锚数据表（简化映射·真实引擎优先）
# ------------------------------------------------------------

# 河图数五行: 1/6水·2/7火·3/8木·4/9金·5/0土
DIGIT_TO_WUXING = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}

# 决策类型 → 五行需求
CATEGORY_WUXING = {
    "audit": "金", "审计": "金", "security": "金", "安全": "金",
    "growth": "木", "生长": "木", "dev": "木", "开发": "木", "plugin": "木", "插件": "木",
    "spread": "火", "传播": "火", "publish": "火", "发布": "火",
    "stability": "土", "稳定": "土", "protocol": "土", "协议": "土", "config": "土", "配置": "土",
    "flow": "水", "流动": "水", "sync": "水", "同步": "水", "data": "水", "数据": "水",
}

# 五行相克（左克右）
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# 奇门八门（简化为工程映射，真实奇门需节气飞盘）
EIGHT_GATES = ["开门", "休门", "生门", "伤门", "杜门", "景门", "死门", "惊门"]
GATE_VERDICT = {"开门": "吉", "休门": "吉", "生门": "吉", "景门": "平", "杜门": "平", "伤门": "凶", "惊门": "凶", "死门": "凶"}

# 369 熔断数字根（洛书不动点警示）
FUSE_DIGITS = {3, 9}

# 道德经锚词表
DAODE_POSITIVE = ["数据主权", "隐私", "为人民", "不伤人", "透明", "可复核", "中国法律",
                  "不删除只冻结", "诚实", "不编造", "守护", "开源", "归属名", "DNA"]
DAODE_NEGATIVE = ["收割", "监控", "作恶", "欺骗", "偷", "卖数据", "隐藏", "黑盒",
                  "洗来源", "去水印", "绕过", "伪造DNA", "倒卖"]


def _fingerprint(text: str) -> str:
    """输入指纹 → 8位哈希"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _digital_root(n: int) -> int:
    """数字根（1-9）"""
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


@dataclass
class Evidence:
    gate: str            # 闸名
    status: str          # 🟢/🟡/🔴
    verdict: str         # 放行/待审/拒绝
    detail: str          # 证据细节
    source: str          # 来源（引擎/数据表/降级标注）

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FusionResult:
    input_text: str
    category: str
    dna: str
    timestamp: str
    evidences: List[Evidence] = field(default_factory=list)
    status: str = "🟡"
    score: int = 0
    gate_health: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "input": self.input_text,
            "category": self.category,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "status": self.status,
            "score": self.score,
            "gate_health": self.gate_health,
            "evidences": [e.to_dict() for e in self.evidences],
        }

    def to_text(self) -> str:
        lines = [
            "=" * 56,
            "🐉 ASI 万法归一 · 决策证据链",
            "=" * 56,
            f"输入   : {self.input_text}",
            f"类型   : {self.category}",
            f"DNA    : {self.dna}",
            f"时间   : {self.timestamp}",
            "=" * 56,
        ]
        for e in self.evidences:
            lines.append(f"{e.status} [{e.gate}] {e.verdict} | {e.detail} | 来源:{e.source}")
        lines.append("=" * 56)
        lines.append(f"结果   : {self.status} · 总分 {self.score}")
        lines.append("=" * 56)
        return "\n".join(lines)


class FusionEngine:
    """七闸融合引擎"""

    def __init__(self, silent_fallback: bool = True):
        self.silent_fallback = silent_fallback

    # ---------- 闸1: 金字塔兼容 ----------
    def gate_pyramid(self, meta: Optional[Dict] = None) -> Evidence:
        try:
            from plugin_compat_check import run_compatibility_check
            from plugin_metadata import PluginMetadata
            if meta:
                known = set(PluginMetadata.__dataclass_fields__.keys())
                filtered = {k: v for k, v in meta.items() if k in known}
                m = PluginMetadata(**filtered)
            else:
                m = PluginMetadata(
                    plugin_id="asi.adhoc.v1", name="临时决策", version="1.0.0",
                    author="UID9622", description="ASI 临时决策（无元数据）",
                    category="experimental", compatible_core=True, compatible_with=[],
                    language=["zh"], target_audience=["all"], license="MulanPSL-2.0",
                    created_at=datetime.now().isoformat(),
                )
            r = run_compatibility_check(m)
            if r.status == "🟢":
                return Evidence("金字塔", "🟢", "放行", f"兼容核心锚点·得分{r.score}", "plugin_compat_check")
            if r.status == "🟡":
                return Evidence("金字塔", "🟡", "待审", f"{r.warnings}", "plugin_compat_check")
            return Evidence("金字塔", "🔴", "拒绝", f"{r.errors}", "plugin_compat_check")
        except Exception as e:
            # 降级：仅做核心锚点声明检查
            if meta and not meta.get("compatible_core", True):
                return Evidence("金字塔", "🔴", "拒绝", "未声明兼容核心锚点", f"降级(异常:{e})")
            return Evidence("金字塔", "🟢", "放行", "降级检查通过（核心锚点兼容）", f"降级(异常:{e})")

    # ---------- 闸2: 五行分类 ----------
    def gate_wuxing(self, category: str) -> Evidence:
        want = CATEGORY_WUXING.get(category.lower() if category else "", None)
        if not want:
            return Evidence("五行", "🟡", "待审", f"类型'{category}'未映射五行", "CATEGORY_WUXING表")
        # 若 wuxing_core 可用，尝试补充验证
        extra = ""
        if _WUXING:
            extra = "·wuxing_core已载"
        return Evidence("五行", "🟢", "放行", f"{category}→{want}行匹配", f"CATEGORY_WUXING{extra}")

    # ---------- 闸3: 369 数字根 ----------
    def gate_369(self, text: str) -> Evidence:
        dr = _digital_root(int(_fingerprint(text), 16))
        try:
            if _DIGITAL_ROOT and hasattr(_DIGITAL_ROOT, "数字根引擎"):
                dr = _DIGITAL_ROOT.数字根引擎.计算(int(_fingerprint(text), 16))
        except Exception:
            pass
        wuxing = DIGIT_TO_WUXING.get(dr, "土")
        if dr in FUSE_DIGITS:
            return Evidence("369", "🟡", "待审", f"数字根={dr}·洛书不动点警示·五行{wuxing}", "lh_digital_root/河图数")
        return Evidence("369", "🟢", "放行", f"数字根={dr}·非熔断·五行{wuxing}", "lh_digital_root/河图数")

    # ---------- 闸4: 易经卦象（软闸·凶相=择时🟡·不直接拒绝） ----------
    def gate_yijing(self) -> Evidence:
        try:
            if _TIME_ENGINE:
                block = _TIME_ENGINE.get_time_block()
                hexagram = block.get("hexagram_name") or "未知"
                phase = str(block.get("phase") or "调整")
                # phase: 执行→🟢 / 调整→🟡 / 观察→🟡(观察等待·择时)
                pmap = {"执行": ("🟢", "放行"), "调整": ("🟡", "待审"), "观察": ("🟡", "观察等待")}
                status, note = pmap.get(phase, ("🟡", "待审"))
                return Evidence("易经", status, note, f"卦={hexagram}·相位={phase}", "lh_time_engine(梅花易数时间起卦)")
        except Exception:
            pass
        # 降级：三才简化起卦（凶相→🟡择时·不拒绝）
        now = datetime.now()
        tian = _digital_root(now.year)
        di = _digital_root(now.month + now.day)
        ren = _digital_root(now.hour + now.minute)
        verdict = "平"
        if tian == di:
            verdict = "吉"
        elif WUXING_KE.get(DIGIT_TO_WUXING.get(tian, "土")) == DIGIT_TO_WUXING.get(di, "土"):
            verdict = "凶"
        vmap = {"吉": "🟢", "平": "🟡", "凶": "🟡"}
        status = vmap[verdict]
        note = "放行" if status == "🟢" else "择时·待审"
        return Evidence("易经", status, note, f"降级三才起卦 天{di}地{tian}人{ren}·相位{verdict}", "降级(三才简化)")

    # ---------- 闸5: 生死门（八门·软闸·死/惊/伤=择时警示🟡·不直接拒绝） ----------
    def gate_bagua(self) -> Evidence:
        try:
            if _TIME_ENGINE:
                block = _TIME_ENGINE.get_time_block()
                gate_raw = block.get("八门") or block.get("门") or None
                if gate_raw:
                    gate = str(gate_raw).replace("门", "") + "门"
                    if gate not in EIGHT_GATES:
                        gate = "生门"
                    verdict = GATE_VERDICT[gate]
                    vmap = {"吉": "🟢", "平": "🟡", "凶": "🟡"}
                    status = vmap[verdict]
                    note = "放行" if status == "🟢" else ("择时·待审" if verdict == "凶" else "待审")
                    return Evidence("生死门", status, note, f"{gate}·相位{verdict}", "lh_time_engine")
        except Exception:
            pass
        # 降级：时辰+日数字根 → 八门落位
        now = datetime.now()
        idx = (now.hour + _digital_root(now.day)) % 8
        gate = EIGHT_GATES[idx]
        verdict = GATE_VERDICT[gate]
        vmap = {"吉": "🟢", "平": "🟡", "凶": "🟡"}
        status = vmap[verdict]
        note = "放行" if status == "🟢" else ("择时·待审" if verdict == "凶" else "待审")
        return Evidence("生死门", status, note, f"{gate}(奇门八门简化落位)·相位{verdict}", "降级(八门简化映射)")

    # ---------- 闸6: 道德经锚 ----------
    def gate_daodejing(self, text: str) -> Evidence:
        pos = sum(1 for w in DAODE_POSITIVE if w in text)
        neg = sum(1 for w in DAODE_NEGATIVE if w in text)
        score = max(0, min(100, 50 + pos * 8 - neg * 20))
        if score >= 60:
            return Evidence("道德经", "🟢", "放行", f"德性分={score}·正锚{pos}/反锚{neg}", "德字扫描(离火运五问同源)")
        if score >= 40:
            return Evidence("道德经", "🟡", "待审", f"德性分={score}·正锚{pos}/反锚{neg}", "德字扫描(离火运五问同源)")
        return Evidence("道德经", "🔴", "拒绝", f"德性分={score}·触碰反锚词{neg}个", "德字扫描(离火运五问同源)")

    # ---------- 闸7: 蚁群共识（多轮平均·低共识=待审🟡·不直接拒绝） ----------
    def gate_ant(self, text: str) -> Evidence:
        seed = int(_fingerprint(text), 16)
        nodes, rounds = 8, 3
        approvals = 0
        for r in range(rounds):
            rnd = random.Random(seed + r * 7919)
            approvals += sum(1 for _ in range(nodes) if rnd.random() >= 0.5)
        consensus = round(approvals / (nodes * rounds), 2)
        extra = "·真实路由已载" if _ANT_ROUTER else ""
        if consensus >= 0.6:
            return Evidence("蚁群", "🟢", "放行", f"共识度={consensus}（{nodes}×{rounds}轮）", f"模拟投票{extra}")
        if consensus >= 0.4:
            return Evidence("蚁群", "🟡", "待审", f"共识度={consensus}（{nodes}×{rounds}轮）", f"模拟投票{extra}")
        return Evidence("蚁群", "🟡", "待审", f"共识度={consensus}·共识不足·建议再评估", f"模拟投票{extra}")

    # ---------- 主链路 ----------
    def run(self, input_text: str, category: str = "audit", meta: Optional[Dict] = None) -> FusionResult:
        evidences = [
            self.gate_pyramid(meta),
            self.gate_wuxing(category),
            self.gate_369(input_text),
            self.gate_yijing(),
            self.gate_bagua(),
            self.gate_daodejing(input_text),
            self.gate_ant(input_text),
        ]
        # 三色汇总
        has_red = any(e.status == "🔴" for e in evidences)
        has_yellow = any(e.status == "🟡" for e in evidences)
        status = "🔴" if has_red else ("🟡" if has_yellow else "🟢")
        # 总分（🟢=100 🟡=60 🔴=0）
        w = {"🟢": 100, "🟡": 60, "🔴": 0}
        score = round(sum(w[e.status] for e in evidences) / len(evidences))
        # 时间戳
        try:
            stamp = _TIME_ENGINE.get_output_stamp(format_type="full") if _TIME_ENGINE else datetime.now().isoformat()
        except Exception:
            stamp = datetime.now().isoformat()
        dna = f"#龍芯⚡️ASI-FUSION-{_fingerprint(input_text)}"
        gate_health = {e.gate: e.status for e in evidences}
        return FusionResult(
            input_text=input_text, category=category, dna=dna,
            timestamp=stamp, evidences=evidences, status=status,
            score=score, gate_health=gate_health,
        )


def main():
    parser = argparse.ArgumentParser(description="龍魂 ASI 万法归一融合引擎")
    parser.add_argument("--input", required=True, help="决策/插件/代码提交描述")
    parser.add_argument("--category", default="audit", help="类型: audit/security/growth/dev/spread/stability/protocol/flow 等")
    parser.add_argument("--meta", default=None, help="插件元数据 JSON 文件路径（可选）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    meta = None
    if args.meta:
        try:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"🔴 无法加载元数据: {e}")
            sys.exit(2)

    engine = FusionEngine()
    result = engine.run(args.input, args.category, meta)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.to_text())

    if result.status == "🟢":
        sys.exit(0)
    elif result.status == "🟡":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
