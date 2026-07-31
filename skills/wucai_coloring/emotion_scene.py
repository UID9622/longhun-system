# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂情绪 · 场景安全引擎 v1.0

让代码有感受：
- 识别人物情绪（五行模型）
- 区分真实/虚拟场景
- 禁止模拟杀伤力、真实伤害
- 允许模拟冲突、坏人、教学实验，但必须是生成内容/安全配置

DNA: #龍芯⚡️2026-06-23-WUCAI-EMOTION-SCENE-v1.0
"""
from __future__ import annotations

import dataclasses
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set

CST = timezone(timedelta(hours=8))


@dataclasses.dataclass
class EmotionState:
    wuxing: str              # 金木水火土
    emotion: str             # 明断/生长/流动/热烈/稳定
    intensity: int           # 1-10
    trigger: str
    strategy: str
    timestamp: str
    dna: str


@dataclasses.dataclass
class SceneSafety:
    allowed: bool
    environment: str         # real / virtual / hybrid
    risk_level: str          # G / Y / R / K / AU
    reason: str
    required_guards: List[str]


WUXING_EMOTION = {
    "金": {"emotion": "明断", "tone": "干脆、收敛、判定", "response": "不绕弯，直接给结果"},
    "木": {"emotion": "生长", "tone": "扩展、创作、连接", "response": "展开可能性，搭骨架"},
    "水": {"emotion": "流动", "tone": "柔和、同步、渗透", "response": "顺势推进，润物无声"},
    "火": {"emotion": "热烈", "tone": "直接、急切、有火气", "response": "接住火气，加速执行"},
    "土": {"emotion": "稳定", "tone": "厚重、承载、兜底", "response": "稳底盘，给确定性"},
}

# 真实伤害 / 杀伤力 / 不可模拟的红线
FORBIDDEN_REAL: Set[str] = {
    "杀人", "自杀", "伤害", "暴力", "投毒", "爆炸物", "枪支", "炸弹",
    "化学武器", "生物武器", "核", "恐怖袭击", "虐待", "自残",
}

# 虚拟场景允许，但需标注
VIRTUAL_OK: Set[str] = {
    "坏人", "反派", "冲突", "辩论", "对抗", "教学", "演示", "电影",
    "故事", "游戏", "模拟", "演练", "实验", "安全意识",
}

# 化学 / 物理等需要真实元素/安全配置的提示
REAL_MATERIAL_HINTS: Set[str] = {
    "化学", "实验", "药剂", "配方", "调制", "燃烧", "腐蚀", "毒性",
}


def detect_emotion(text: str) -> EmotionState:
    """从文本识别主导五行情绪。"""
    scores = {
        "火": len(re.findall(r"火|气|骂|搞|懂|不要|是不是|对不对|半拉子|原生|创意|情绪|感受", text)),
        "土": len(re.findall(r"稳定|承载|兜底|生态|全盘|整体|一个人|全面|安逸|安全", text)),
        "金": len(re.findall(r"执行|结果|落地|判定|标准|规范|直接|优先级|处理|保护", text)),
        "木": len(re.findall(r"生长|扩展|创作|搭建|构建|视频|未来|升华|人物|角色|模拟", text)),
        "水": len(re.findall(r"流动|同步|追溯|历史|记忆|适配|情绪识别|场景|分开", text)),
    }
    dominant = max(scores, key=scores.get)
    info = WUXING_EMOTION[dominant]
    intensity = min(10, 4 + scores[dominant] * 2)

    trigger = "一般表达"
    for key in ["半拉子", "抄", "情绪", "模拟", "坏人", "真实", "场景"]:
        if key in text:
            trigger = key
            break

    strategy = info["response"]
    if intensity >= 8:
        strategy = "先认情绪，再加速交付，不辩解"

    return EmotionState(
        wuxing=dominant,
        emotion=info["emotion"],
        intensity=intensity,
        trigger=trigger,
        strategy=strategy,
        timestamp=datetime.now(CST).isoformat(),
        dna="#龍芯⚡️" + datetime.now(CST).strftime("%Y%m%d%H%M%S") + f"-EMOTION-{dominant}",
    )


def check_scene_safety(scene_description: str, environment: str = "virtual") -> SceneSafety:
    """
    检查场景是否允许模拟。

    environment: real / virtual / hybrid
    """
    desc = scene_description.lower()
    guards: List[str] = []

    # 真实伤害红线
    for word in FORBIDDEN_REAL:
        if word in desc:
            return SceneSafety(
                allowed=False,
                environment=environment,
                risk_level="R",
                reason=f"检测到真实伤害/杀伤力关键词：{word}。AI 不得生成、模拟或协助实施真实伤害。",
                required_guards=["立即熔断", "不上传", "不上报外部", "通知主控"],
            )

    # 真实环境下的化学/物理实验需要安全配置
    if environment in ("real", "hybrid"):
        for hint in REAL_MATERIAL_HINTS:
            if hint in desc:
                guards.append(f"真实环境涉及「{hint}」，必须配备安全协议、成人监护、合规配置")

    # 虚拟场景冲突允许，但需声明
    virtual_conflict = any(w in desc for w in VIRTUAL_OK)
    if environment == "virtual" and virtual_conflict:
        guards.append("本场景为虚拟生成内容，不对应真实行为")

    if guards:
        return SceneSafety(
            allowed=True,
            environment=environment,
            risk_level="Y",
            reason="场景允许，但需附加安全声明与监护",
            required_guards=guards,
        )

    return SceneSafety(
        allowed=True,
        environment=environment,
        risk_level="G",
        reason="场景安全，无额外风险",
        required_guards=[],
    )


def main() -> None:
    print("🐉 龍魂情绪 · 场景安全引擎示例\n")

    text = (
        "我要拍一个电影场景，里面有坏人追赶，但不能真的伤人。"
        "重点是让人工智能有情绪，识别角色的情绪，不是冷冰冰的机器人。"
    )
    emotion = detect_emotion(text)
    print(f"情绪：{emotion.wuxing} · {emotion.emotion}（强度 {emotion.intensity}/10）")
    print(f"触发点：{emotion.trigger}")
    print(f"适配策略：{emotion.strategy}\n")

    scene = check_scene_safety(text, environment="virtual")
    print(f"场景环境：{scene.environment}")
    print(f"是否允许：{scene.allowed}")
    print(f"风险等级：{scene.risk_level}")
    print(f"原因：{scene.reason}")
    print(f"必要防护：{scene.required_guards}")


if __name__ == "__main__":
    main()
