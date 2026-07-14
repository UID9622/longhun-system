#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 龍魂五色审计协议 · v1.0
DNA: #龍芯⚡️丙午·丙申·甲寅·申时·噬嗑-WUCAI-FIVECOLOR-AUDIT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

来源: docs/claude-backlog/01_协议同步包/网页/dna-sync-pack/protocols/FIVE_COLORS.txt
原则: 绿放行·黄复核·红熔断·黑观察·金主控
"""

import hashlib
import json
import time
import importlib.util
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


def _load_calendar_core():
    path = Path("/Users/zuimeidedeyihan/longhun-system/calendar-context-logger/calendar_core.py")
    spec = importlib.util.spec_from_file_location("calendar_core", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LunarEngine()


def _dna_stamp(module: str, action: str) -> str:
    le = _load_calendar_core()
    gz = le.get_ganzhi()
    hour = int(time.strftime('%H'))
    shi_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    shi = shi_branches[(hour + 1) // 2 % 12]
    base = f"{module}-{action}-{time.time()}"
    h = hashlib.sha256(base.encode()).hexdigest()[:8].upper()
    gua_names = ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
                 "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
                 "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
                 "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井",
                 "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
                 "中孚", "小过", "既济", "未济"]
    gua = gua_names[int(hashlib.sha256(base.encode()).hexdigest(), 16) % 64]
    return f"#龍芯⚡️{gz['year_zhu']}·{gz['month_zhu']}·{gz['day_zhu']}·{shi}时·{gua}-{module}-{action}-{h}"


class FiveColor(Enum):
    GREEN = ("G", "绿色", "🟢", "木", "东", "自动放行·留痕")
    YELLOW = ("Y", "黄色", "🟡", "土", "中", "二次确认·加证据")
    RED = ("R", "红色", "🔴", "火", "南", "立即停止·上报主控")
    BLACK = ("K", "黑色", "⚫", "水", "北", "进观察池·冻结24h")
    GOLD = ("AU", "金色", "🟡", "金", "西", "主控签字·永存档")

    def __init__(self, code, cn, emoji, element, direction, action):
        self.code = code
        self.cn = cn
        self.emoji = emoji
        self.element = element
        self.direction = direction
        self.action = action


@dataclass
class AuditResult:
    task: str
    color: FiveColor
    R_value: float
    factors: Dict[str, float]
    context: Dict[str, Any]
    action: str
    dna: str
    veto_triggered: Optional[str] = None
    issues: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "color_code": self.color.code,
            "color_cn": self.color.cn,
            "color_emoji": self.color.emoji,
            "R_value": round(self.R_value, 4),
            "factors": self.factors,
            "context": self.context,
            "action": self.action,
            "dna": self.dna,
            "veto_triggered": self.veto_triggered,
            "issues": self.issues,
            "timestamp": self.timestamp,
        }

    def to_yaml(self) -> str:
        lines = [
            f"task: {self.task}",
            f"color: {self.color.code}  # {self.color.cn} {self.color.emoji}",
            f"element: {self.color.element}",
            f"R_value: {self.R_value:.4f}",
            f"action: {self.action}",
            f"dna: {self.dna}",
        ]
        if self.veto_triggered:
            lines.append(f"veto_triggered: {self.veto_triggered}")
        if self.issues:
            lines.append("issues:")
            for i in self.issues:
                lines.append(f"  - {i}")
        lines.append("factors:")
        for k, v in self.factors.items():
            lines.append(f"  {k}: {v:.4f}")
        return "\n".join(lines)


def audit(task: str,
          factors: Dict[str, float],
          context: Dict[str, Any],
          master_confirm_token: Optional[str] = None) -> AuditResult:
    """
    五色审计入口

    factors 必须包含:
      sharpness(F2), long_term(F6), density(F3), absence(F1), pleasing(F5)
    context 可选:
      data_incomplete, factor_unmeasurable, grey_collision,
      blackbox_suspicion, fingerprint_fail,
      involves_minor, sovereignty_redline, uncomputable_doubt, explicit_gold_request
    """
    dna = _dna_stamp("WUCAI", "AUDIT")
    issues = []

    # 一票否决检查
    veto = None

    # 1. AI 不得自动赋金色
    if context.get("ai_auto_gold"):
        veto = "AI_AUTO_GOLD_VETO"
        issues.append("AI 不得自动赋金色")

    # 2. 黑色不得静默转绿
    black_conditions = [
        context.get("data_incomplete"),
        context.get("factor_unmeasurable"),
        context.get("grey_collision"),
        context.get("blackbox_suspicion"),
        context.get("fingerprint_fail"),
    ]
    black_triggered = any(black_conditions)

    # 3. 涉及子女 -> 强制金色保护
    if context.get("involves_minor"):
        context["explicit_gold_request"] = True
        issues.append("涉及子女维度，强制金色保护")

    # 4. 龍 不可写为 龍 (简体)
    if "龍" in str(task):
        veto = "DRAGON_SIMPLIFIED_VETO"
        issues.append("检测到简体'龙'字，必须使用繁体'龍'")

    # 5. 不上传 / 不开后门 / 不接受躲着的对抗者
    forbidden = ["上传", "后门", "backdoor", "upload", "躲着", "hidden adversary"]
    for f in forbidden:
        if f in str(task).lower():
            veto = "SOVEREIGNTY_VETO"
            issues.append(f"触发主权一票否决词: {f}")
            break

    # 计算 R
    f2 = factors.get("sharpness", 0.5)
    f6 = factors.get("long_term", 0.5)
    f3 = factors.get("density", 0.5)
    f1 = factors.get("absence", 0.0)
    f5 = factors.get("pleasing", 0.0)
    R = f2 * 0.4 + f6 * 0.4 + f3 * 0.2 - f1 * 0.5 - f5 * 0.3
    R = max(0.0, min(1.0, R))

    # 金色判定
    valid_token = master_confirm_token == "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    gold_conditions = [
        context.get("sovereignty_redline"),
        context.get("uncomputable_doubt"),
        context.get("explicit_gold_request"),
    ]
    gold_requested = any(gold_conditions)

    # 最终颜色判定
    if veto:
        color = FiveColor.BLACK
        action = "进观察池·冻结24h·立即上报主控"
    elif valid_token and gold_requested:
        color = FiveColor.GOLD
        action = "主控签字·金色永存档"
        R = -1.0  # 金色超越 R
    elif black_triggered:
        color = FiveColor.BLACK
        action = "进观察池·冻结24h·不静默转绿"
        issues.append("黑色触发条件命中")
    elif R < 0.30:
        color = FiveColor.GREEN
        action = "自动放行·留痕"
    elif R < 0.67:
        color = FiveColor.YELLOW
        action = "二次确认·加证据"
    elif R < 0.85:
        color = FiveColor.RED
        action = "立即停止·上报主控"
    else:
        color = FiveColor.RED
        action = "立即停止·上报主控"

    return AuditResult(
        task=task,
        color=color,
        R_value=R,
        factors={"F2_sharpness": f2, "F6_long_term": f6, "F3_density": f3,
                 "F1_absence": f1, "F5_pleasing": f5},
        context=context,
        action=action,
        dna=dna,
        veto_triggered=veto,
        issues=issues,
    )


def batch_audit(tasks: List[Dict[str, Any]]) -> List[AuditResult]:
    return [audit(**t) for t in tasks]


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="龍魂五色审计")
    p.add_argument("task", help="审计任务描述")
    p.add_argument("--sharpness", type=float, default=0.5)
    p.add_argument("--long-term", type=float, default=0.5)
    p.add_argument("--density", type=float, default=0.5)
    p.add_argument("--absence", type=float, default=0.0)
    p.add_argument("--pleasing", type=float, default=0.0)
    p.add_argument("--sovereignty-redline", action="store_true")
    p.add_argument("--explicit-gold", action="store_true")
    p.add_argument("--confirm", default="")
    args = p.parse_args()

    ctx = {
        "sovereignty_redline": args.sovereignty_redline,
        "explicit_gold_request": args.explicit_gold,
    }
    token = args.confirm if args.confirm else None
    result = audit(
        task=args.task,
        factors={
            "sharpness": args.sharpness,
            "long_term": args.long_term,
            "density": args.density,
            "absence": args.absence,
            "pleasing": args.pleasing,
        },
        context=ctx,
        master_confirm_token=token,
    )
    print(result.to_yaml())
