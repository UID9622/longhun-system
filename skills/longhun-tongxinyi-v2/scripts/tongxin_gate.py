#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 v2.0 · 龍魂前置翻译门控 | Tongxinyi Gate v2.0
UID: 9622
DNA: #龍芯⚡️2026-07-01-LONGHUN-TONGXINYI-v2.0-GATE
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

功能：基于规则的用户输入理解、情绪净化、意图识别、三色审计与技能路由。
不调用外部 LLM，纯本地规则运行。
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 允许从相邻的 longhun-tags 技能导入
_TAGS_PATH = Path(__file__).resolve().parent.parent.parent / "longhun-tags" / "scripts"
if str(_TAGS_PATH) not in sys.path:
    sys.path.insert(0, str(_TAGS_PATH))

try:
    from longhun_tags import LongHunTagSystem
except Exception:
    LongHunTagSystem = None  # type: ignore


# ═══════════════════════════════════════════════════════════════
# DNA 与常量
# ═══════════════════════════════════════════════════════════════

DNA = "#龍芯⚡️2026-07-01-LONGHUN-TONGXINYI-v2.0-GATE"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

TRIGGER_SKILLS: List[Tuple[List[str], str]] = [
    (["标签", "五行", "八卦", "甲骨文", "星宿", "龍魂标签", "CNSH变量", "表情包"], "longhun-tags"),
    (["通心译", "先翻译再执行", "意图识别", "情绪净化", "Tongxin", "v2.0", "七维评估"], "longhun-tongxinyi-v2"),
    (["CNSH", "规范", "语法", "关键字"], "longhun-cnsh"),
    (["治理", "审计", "DNA追溯", "三色"], "longhun-governance"),
    (["铁律", "主权底线", "熔断"], "longhun-iron-laws"),
    (["运行", "字元", "AI画匠", "渲染"], "longhun-cnsh"),
    (["备份", "恢复", "清理"], "dragonsoul"),
    (["git", "提交", "commit", "pull request"], "longhun-git"),
]

EMOTION_KEYWORDS: Dict[str, Dict[str, Any]] = {
    "愤怒": {"label": "愤怒", "intensity": 0.8, "color": "🔴"},
    "火大": {"label": "愤怒", "intensity": 0.8, "color": "🔴"},
    "气死": {"label": "愤怒", "intensity": 0.9, "color": "🔴"},
    "滚": {"label": "愤怒", "intensity": 0.9, "color": "🔴"},
    "垃圾": {"label": "厌恶", "intensity": 0.7, "color": "🟡"},
    "失望": {"label": "失望", "intensity": 0.6, "color": "🟡"},
    "郁闷": {"label": "悲伤", "intensity": 0.5, "color": "🟡"},
    "开心": {"label": "喜悦", "intensity": 0.6, "color": "🟢"},
    "谢谢": {"label": "感激", "intensity": 0.4, "color": "🟢"},
    "赞": {"label": "喜悦", "intensity": 0.5, "color": "🟢"},
    "急": {"label": "焦虑", "intensity": 0.6, "color": "🟡"},
    "赶紧": {"label": "焦虑", "intensity": 0.5, "color": "🟡"},
}

ACTION_PATTERNS: Dict[str, List[str]] = {
    "query": ["查", "看", "找", "搜", "列出", "显示", "获取", "read", "list", "show"],
    "create": ["创建", "新建", "生成", "写", "添加", "create", "new", "add", "write"],
    "update": ["更新", "修改", "改", "升级", "edit", "update", "modify"],
    "delete": ["删除", "移除", "清", "清空", "delete", "remove", "clear"],
    "execute": ["执行", "运行", "启动", "调用", "run", "execute", "start"],
    "backup": ["备份", "恢复", "backup", "restore"],
}

RISK_KEYWORDS: List[str] = ["删除", "清空", "格式化", "drop", "rm -rf", "覆盖", "销毁", "kill"]


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

_now = lambda: datetime.now(timezone.utc).isoformat()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _dna_stamp(prefix: str = "TONGXINYI") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    short = _sha256(f"{prefix}:{ts}")
    return f"#龍芯⚡️{ts[:8]}-{ts[9:]}-{prefix}-{short}"


def _detect_action(text: str) -> str:
    lower = text.lower()
    for action, kws in ACTION_PATTERNS.items():
        if any(k in text or k in lower for k in kws):
            return action
    return "unknown"


def _detect_subject(text: str) -> str:
    # 简单规则：找"我"、"你"、"系统"、"龍魂"等
    if re.search(r"我|咱们|UID9622", text):
        return "UID9622"
    if re.search(r"你|Kimi|龍魂", text):
        return "system"
    return "unknown"


def _detect_target(text: str) -> str:
    # 尝试提取宾语：动词后的名词
    for action, kws in ACTION_PATTERNS.items():
        for kw in kws:
            if kw in text:
                idx = text.find(kw) + len(kw)
                tail = text[idx:idx + 30].strip(" ，。！？\n")
                if tail:
                    return tail.split()[0] if tail.split() else tail
    return ""


def _detect_emotion(text: str) -> Tuple[str, float, str]:
    for kw, info in EMOTION_KEYWORDS.items():
        if kw in text:
            return info["label"], info["intensity"], info["color"]
    return "平静", 0.0, "🟢"


def _purify_text(text: str) -> str:
    # 去除情绪词后的中性化表达
    purified = text
    for kw in EMOTION_KEYWORDS:
        purified = purified.replace(kw, "")
    # 压缩多余空格和标点
    purified = re.sub(r"[\s！？。，]{2,}", " ", purified).strip()
    return purified or text


def _recommended_skill(text: str) -> str:
    scores: Dict[str, float] = {}
    for kws, skill in TRIGGER_SKILLS:
        for kw in kws:
            if kw in text:
                scores[skill] = scores.get(skill, 0.0) + 1.0
    if not scores:
        return "longhun-tongxinyi-v2"
    return max(scores.items(), key=lambda x: x[1])[0]


def _tri_color_audit(text: str, action: str, emotion_intensity: float) -> Dict[str, Any]:
    lower = text.lower()
    risk = any(r in text or r in lower for r in RISK_KEYWORDS)

    if risk and emotion_intensity > 0.7:
        return {"color": "🔴", "label": "熔断", "action": "需要 UID9622 二次确认", "risk_level": "high"}
    if risk or emotion_intensity > 0.6:
        return {"color": "🟡", "label": "待审", "action": "建议人工复核", "risk_level": "medium"}
    return {"color": "🟢", "label": "通行", "action": "继续执行", "risk_level": "low"}


def _sast_nodes(text: str) -> List[Dict[str, Any]]:
    # 简化版语义抽象语法树节点
    action = _detect_action(text)
    subject = _detect_subject(text)
    target = _detect_target(text)
    return [
        {"type": "subject", "value": subject},
        {"type": "action", "value": action},
        {"type": "target", "value": target},
        {"type": "modality", "value": "imperative" if action != "unknown" else "statement"},
    ]


def _select_longhun_tag(text: str, audit: Dict[str, Any]) -> Dict[str, Any]:
    if LongHunTagSystem is None:
        return {"code": "", "rendered": "", "note": "longhun-tags not available"}

    ts = LongHunTagSystem()

    # 根据语义选择标签
    if audit["risk_level"] == "high":
        tag = ts.get_tag("火·囚") or {}
    elif audit["risk_level"] == "medium":
        tag = ts.get_tag("水·囚") or {}
    elif any(k in text for k in ACTION_PATTERNS["create"]):
        tag = ts.get_tag("木·生") or {}
    elif any(k in text for k in ACTION_PATTERNS["query"]):
        tag = ts.get_tag("见") or {}
    elif any(k in text for k in ACTION_PATTERNS["execute"]):
        tag = ts.get_tag("行") or {}
    elif any(k in text for k in ACTION_PATTERNS["delete"]):
        tag = ts.get_tag("死") or {}
    else:
        tag = ts.get_tag("成") or {}

    code = tag.get("desc") or tag.get("label") or tag.get("char", "")
    return {
        "code": code,
        "rendered_html": ts.render_tag(code, style="html") if code else "",
        "rendered_text": ts.render_tag(code, style="text") if code else "",
    }


# ═══════════════════════════════════════════════════════════════
# TongxinyiGate 类
# ═══════════════════════════════════════════════════════════════

class TongxinyiGate:
    """
    通心译 v2.0 门控
    将原始输入翻译为 L0-L5 结构化意图 + 七维评估占位
    """

    def __init__(self, uid: str = "UID9622"):
        self.uid = uid
        self.dna = DNA

    def translate(self, raw_input: str, uid: Optional[str] = None) -> Dict[str, Any]:
        user = uid or self.uid
        emotion_label, emotion_intensity, emotion_color = _detect_emotion(raw_input)
        purified = _purify_text(raw_input)
        action = _detect_action(raw_input)
        subject = _detect_subject(raw_input)
        target = _detect_target(raw_input)
        audit = _tri_color_audit(raw_input, action, emotion_intensity)
        skill = _recommended_skill(raw_input)
        longhun_tag = _select_longhun_tag(raw_input, audit)

        # 置信度：简单启发式
        confidence = 0.6
        if action != "unknown":
            confidence += 0.15
        if target:
            confidence += 0.1
        if emotion_intensity < 0.3:
            confidence += 0.1
        confidence = min(0.98, round(confidence, 2))

        result: Dict[str, Any] = {
            "dna": _dna_stamp("TONGXINYI"),
            "parent_dna": DNA,
            "uid": user,
            "timestamp": _now(),
            "confidence": confidence,
            "recommended_skill": skill,
            "L0_原话保留": {
                "raw_input": raw_input,
                "input_hash": _sha256(raw_input),
                "preserved": True,
            },
            "L1_情绪净化": {
                "emotion_label": emotion_label,
                "emotion_intensity": emotion_intensity,
                "emotion_color": emotion_color,
                "purified_text": purified,
            },
            "L2_意图骨架": {
                "subject": subject,
                "action": action,
                "target": target,
                "priority": 5 if audit["risk_level"] == "low" else 8 if audit["risk_level"] == "medium" else 10,
            },
            "L3_SAST": {
                "root_type": action,
                "nodes": _sast_nodes(raw_input),
            },
            "L4_三色审计": audit,
            "L5_适配输出": {
                "recommended_skills": [skill],
                "five_part_receipt": {
                    "理解": f"识别意图为 {action}，目标为 {target or '未明确'}",
                    "补全": "" if target else "需要补充操作对象",
                    "预判": f"风险等级 {audit['risk_level']}",
                    "路径": f"推荐技能：{skill}",
                    "确认": "否" if audit["risk_level"] == "low" else "是",
                },
            },
            "龍魂标签": longhun_tag,
            "七维评估": {
                "D1_culture_lexicon": 0.80,
                "D2_semantic_syntax": 0.75,
                "D3_classical_chinese": 0.50,
                "D4_discourse_integrity": 0.85,
                "D5_civilization_safety": 0.95,
                "D6_creative_strategy": 0.60,
                "D7_semantic_precision": 0.80,
                "note": "规则基础分，完整评估请使用 tongxin_evaluator.py",
            },
        }
        return result

    def translate_batch(self, inputs: List[str], uid: Optional[str] = None) -> List[Dict[str, Any]]:
        return [self.translate(t, uid) for t in inputs]


# ═══════════════════════════════════════════════════════════════
# 演示入口
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("通心译 v2.0 · 龍魂前置翻译门控")
    print(f"DNA: {DNA}")
    print("=" * 60)

    gate = TongxinyiGate()

    samples = [
        "帮我查一下今天的系统状态",
        "把这个文件删了，气死我了",
        "运行 longhun-tags 演示",
        "通心译 v2.0 是什么",
    ]

    for text in samples:
        result = gate.translate(text)
        print(f"\n输入: {text}")
        print(f"  推荐技能: {result['recommended_skill']}")
        print(f"  置信度: {result['confidence']}")
        print(f"  情绪: {result['L1_情绪净化']['emotion_label']} ({result['L1_情绪净化']['emotion_intensity']})")
        print(f"  意图: {result['L2_意图骨架']['action']} -> {result['L2_意图骨架']['target']}")
        print(f"  三色审计: {result['L4_三色审计']['color']} {result['L4_三色审计']['label']}")
        print(f"  龍魂标签: {result['龍魂标签']['rendered_text']}")

    print("\n" + "=" * 60)
    print("完整 JSON 示例（最后一条）:")
    print("=" * 60)
    print(json.dumps(gate.translate(samples[-1]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
