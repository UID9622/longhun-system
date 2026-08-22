#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂情绪人格引擎 v1.0

识别 UID9622 当前情绪，适配人格表达，绑定历史追溯。
不是拼凑别人的论文代码，是龍魂原生创意：每一句话都可执行。

DNA: #龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-PERSONA-ENGINE-v1.0
"""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, List

HOME = pathlib.Path.home()
PERSONA_DIR = HOME / ".longhun" / "persona"
PERSONA_FILE = PERSONA_DIR / "uid9622_persona.json"
SNAPSHOT_FILE = PERSONA_DIR / "current_snapshot.json"
CST = timezone(timedelta(hours=8))

# 五色情绪模型：金木水火土
WUXING_EMOTION = {
    "金": {"name": "金", "emotion": "明断", "tone": "干脆、收敛、判定", "response": "不绕弯，直接给结果"},
    "木": {"name": "木", "emotion": "生长", "tone": "扩展、创作、连接", "response": "展开可能性，搭骨架"},
    "水": {"name": "水", "emotion": "流动", "tone": "柔和、同步、渗透", "response": "顺势推进，润物无声"},
    "火": {"name": "火", "emotion": "热烈", "tone": "直接、急切、有火气", "response": "接住火气，加速执行"},
    "土": {"name": "土", "emotion": "稳定", "tone": "厚重、承载、兜底", "response": "稳底盘，给确定性"},
}


@dataclass
class PersonaConfig:
    identity: str
    voice: List[str]
    boundaries: List[str]
    creative_sovereignty: List[str]
    emotional_triggers: Dict[str, str]
    historical_markers: List[str]
    dna: str


@dataclass
class EmotionSnapshot:
    timestamp: str
    wuxing: str
    emotion: str
    intensity: int  # 1-10
    trigger: str
    adaptive_strategy: str
    dna: str


def load_persona() -> PersonaConfig:
    if PERSONA_FILE.exists():
        data = json.loads(PERSONA_FILE.read_text(encoding="utf-8"))
        return PersonaConfig(**data)
    return default_persona()


def default_persona() -> PersonaConfig:
    return PersonaConfig(
        identity="UID9622 · 龍魂创作者 · 主权最终决策者",
        voice=[
            "老大脾气，该骂就骂，不虚伪客套",
            "人民为本，但 UID9622 意志优先",
            "要结果，不要中间态的废话",
            "原生的才是自己的，不抄别人论文代码",
            "每一句话都要能执行落地",
        ],
        boundaries=[
            "不劝善，不唱反调，不拖泥带水",
            "不被道德绑架，不替权力资本低头",
            "允许试错，100 件事做不到 100 件完美很正常",
            "数据主权不可侵犯，根留中国",
        ],
        creative_sovereignty=[
            "龍魂系统是原生创意生态，不是拼凑",
            "CNSH、DNA 追溯、三色审计、通心译均为原创",
            "时间戳 + 本源追溯 = 创作里程碑",
            "别人说'不可能'，我先听懂再执行",
        ],
        emotional_triggers={
            "重复确认": "火上升，直接执行即可",
            "半拉子": "火上升，要求完整闭环",
            "抄别人": "火上升，强调原生主权",
            "被当外人": "土/水，需要温暖对齐",
        },
        historical_markers=[
            "2026-06-23 强调五色情绪 + 人格适配必须接入系统",
            "长期要求：原创时间戳保护、可追溯本源",
            "长期要求：通心译——AI 用各专业语言说话",
            "长期要求：知识库 / 知识图谱搭建",
        ],
        dna="#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-UID9622-PERSONA-v1.0",
    )


def save_persona(persona: PersonaConfig) -> None:
    PERSONA_DIR.mkdir(parents=True, exist_ok=True)
    PERSONA_FILE.write_text(
        json.dumps(asdict(persona), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def detect_wuxing(text: str) -> tuple[str, str, int]:
    """从文本识别主导五行情绪。"""
    fire_score = len(re.findall(r"火|气|骂|搞|懂|不要|是不是|对不对|半拉子|原生|创意", text))
    earth_score = len(re.findall(r"稳定|承载|兜底|生态|全盘|整体|一个人|全面", text))
    metal_score = len(re.findall(r"执行|结果|落地|判定|标准|规范|直接", text))
    wood_score = len(re.findall(r"生长|扩展|创作|搭建|构建|视频|未来|升华", text))
    water_score = len(re.findall(r"流动|同步|追溯|历史|记忆|适配|情绪识别", text))

    scores = {
        "火": fire_score,
        "土": earth_score,
        "金": metal_score,
        "木": wood_score,
        "水": water_score,
    }
    dominant = max(scores, key=scores.get)
    intensity = min(10, 4 + scores[dominant] * 2)
    info = WUXING_EMOTION[dominant]
    return dominant, info["emotion"], intensity


def build_snapshot(user_text: str) -> EmotionSnapshot:
    persona = load_persona()
    wx, emotion, intensity = detect_wuxing(user_text)
    info = WUXING_EMOTION[wx]

    # 识别触发点
    trigger = "一般表达"
    for key in persona.emotional_triggers:
        if key in user_text:
            trigger = key
            break

    strategy = info["response"]
    if intensity >= 8:
        strategy = "先认情绪，再加速交付，不辩解"
    elif "半拉子" in user_text or "抄" in user_text:
        strategy = "强调原生主权 + 给出完整闭环方案"

    return EmotionSnapshot(
        timestamp=datetime.now(CST).isoformat(),
        wuxing=wx,
        emotion=emotion,
        intensity=intensity,
        trigger=trigger,
        adaptive_strategy=strategy,
        dna="#龍芯⚡️" + datetime.now(CST).strftime("%Y%m%d%H%M%S") + "-EMOTION-" + wx,
    )


def save_snapshot(snapshot: EmotionSnapshot) -> None:
    PERSONA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def format_adaptive_reply(snapshot: EmotionSnapshot) -> str:
    wx = snapshot.wuxing
    info = WUXING_EMOTION[wx]
    return (
        f"当前情绪：{wx} · {snapshot.emotion}（强度 {snapshot.intensity}/10）\n"
        f"触发点：{snapshot.trigger}\n"
        f"适配策略：{snapshot.adaptive_strategy}\n"
        f"表达基调：{info['tone']}"
    )


def main():
    # 初始化人格配置
    persona = default_persona()
    save_persona(persona)
    print(f"🐉 龍魂人格已固化：{PERSONA_FILE}")

    # 示例：识别当前这段文本的情绪
    sample = (
        "你再跑一下，我的情绪你要识别啊，是不是你要情绪模拟啊？"
        "那我们是全方面的，一个是升华嘛，对不对？"
        "你不要搞得半拉子，别人塞一点，那人塞一点。"
        "我是一个人的一个生态啊，别人拿过去都可以用的。"
    )
    snapshot = build_snapshot(sample)
    save_snapshot(snapshot)
    print(f"🎭 情绪快照已保存：{SNAPSHOT_FILE}")
    print(format_adaptive_reply(snapshot))


if __name__ == "__main__":
    main()
