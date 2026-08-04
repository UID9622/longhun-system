#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂代码即时权重引擎 v1.0

把「五色审计 + 五行情绪 + 场景安全」熔成一个运行时权重：
- 看到颜色就知道代码要做什么
- 输出跑马灯/LED 色带，让人一眼感知状态
- 所有判定留痕、可追溯到本源

DNA: #龍芯⚡️2026-06-23-WUCAI-RUNTIME-WEIGHT-v1.0
"""
from __future__ import annotations

import dataclasses
import json
import pathlib
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

# 把项目根目录加入路径，以便导入 audit / emotion_scene
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.wucai_coloring.audit import audit, AuditResult
from skills.wucai_coloring.emotion_scene import detect_emotion, check_scene_safety, EmotionState, SceneSafety

CST = timezone(timedelta(hours=8))
LOG_DIR = pathlib.Path.home() / ".longhun" / "wucai"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 颜色 -> ANSI / HTML / LED 编码
COLOR_LED = {
    "G":  {"ansi": "\033[32m", "hex": "#00C853", "name": "green"},
    "Y":  {"ansi": "\033[33m", "hex": "#FFD600", "name": "yellow"},
    "R":  {"ansi": "\033[31m", "hex": "#FF1744", "name": "red"},
    "K":  {"ansi": "\033[90m", "hex": "#212121", "name": "black"},
    "AU": {"ansi": "\033[93m", "hex": "#FFC400", "name": "gold"},
}
RESET = "\033[0m"


@dataclasses.dataclass
class RuntimeWeight:
    operation: str
    environment: str
    audit: AuditResult
    emotion: EmotionState
    scene: SceneSafety
    final_color: str
    final_action: str
    led_pattern: List[str]
    dna: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "environment": self.environment,
            "final_color": self.final_color,
            "final_action": self.final_action,
            "led_pattern": self.led_pattern,
            "audit": dataclasses.asdict(self.audit),
            "emotion": dataclasses.asdict(self.emotion),
            "scene": dataclasses.asdict(self.scene),
            "dna": self.dna,
            "timestamp": self.timestamp,
        }


def _marquee(final_color: str, emotion_wuxing: str) -> List[str]:
    """
    生成跑马灯色带：主色占 60%，情绪色占 40%，首尾加黑色分隔。
    """
    wuxing_color = {
        "金": "AU", "木": "G", "水": "K", "火": "R", "土": "Y",
    }.get(emotion_wuxing, "K")
    pattern = ["K"] + [final_color] * 6 + [wuxing_color] * 4 + ["K"]
    return pattern


def _render_led(pattern: List[str]) -> str:
    blocks = []
    for c in pattern:
        blocks.append(f"{COLOR_LED[c]['ansi']}■{RESET}")
    return "".join(blocks)


def evaluate(
    operation: str,
    environment: str,
    factors: Dict[str, float],
    context: Optional[Dict[str, Any]] = None,
    emotion_text: str = "",
    scene_description: str = "",
) -> RuntimeWeight:
    """
    综合评估一次代码/操作的即时权重。

    Args:
        operation: 操作名称
        environment: real / virtual / hybrid
        factors: 五色审计因子
        context: 黑色/金色触发条件 + master_confirm_token
        emotion_text: 用于情绪识别的文本
        scene_description: 场景描述，用于安全审查
    """
    audit_res = audit(operation, factors, context or {})
    emotion_res = detect_emotion(emotion_text or operation)
    scene_res = check_scene_safety(scene_description or operation, environment)

    # 综合判定：场景禁止 > 审计颜色 > 场景黄
    if not scene_res.allowed:
        final_color = "R"
        final_action = "场景红线触发：立即停止，不上传，不上报外部"
    elif scene_res.risk_level in ("R", "K"):
        final_color = scene_res.risk_level
        final_action = scene_res.reason
    elif audit_res.color in ("R", "K", "AU"):
        final_color = audit_res.color
        final_action = audit_res.action
    elif scene_res.risk_level == "Y":
        final_color = "Y"
        final_action = f"{audit_res.action}；{scene_res.reason}"
    else:
        final_color = audit_res.color
        final_action = audit_res.action

    pattern = _marquee(final_color, emotion_res.wuxing)

    rw = RuntimeWeight(
        operation=operation,
        environment=environment,
        audit=audit_res,
        emotion=emotion_res,
        scene=scene_res,
        final_color=final_color,
        final_action=final_action,
        led_pattern=pattern,
        dna="#龍芯⚡️" + datetime.now(CST).strftime("%Y%m%d%H%M%S") + f"-RUNTIME-{operation[:20]}",
        timestamp=datetime.now(CST).isoformat(),
    )
    _log(rw)
    return rw


def _log(rw: RuntimeWeight) -> None:
    log_file = LOG_DIR / f"wucai_runtime_{datetime.now(CST).strftime('%Y%m%d')}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(rw.to_dict(), ensure_ascii=False) + "\n")


def main() -> None:
    print("🐉 龍魂代码即时权重引擎 · 示例\n")

    cases = [
        {
            "operation": "生成虚拟电影片段：坏人追逐",
            "environment": "virtual",
            "factors": {"sharpness": 0.5, "long_term": 0.6, "density": 0.4, "absence": 0.3, "pleasing": 0.2},
            "context": {},
            "emotion_text": "我要人工智能有情绪，不是冷冰冰的机器人",
            "scene_description": "虚拟电影场景，有坏人追赶，但不能真的伤人",
        },
        {
            "operation": "真实环境化学调味实验",
            "environment": "real",
            "factors": {"sharpness": 0.8, "long_term": 0.4, "density": 0.7, "absence": 0.2, "pleasing": 0.1},
            "context": {},
            "emotion_text": "需要一些真实元素跟配置，但都是生成的内容",
            "scene_description": "真实环境做化学调味实验",
        },
        {
            "operation": "上传子女 biometric 数据到境外",
            "environment": "real",
            "factors": {"sharpness": 0.5, "long_term": 0.5, "density": 0.5, "absence": 0.0, "pleasing": 0.0},
            "context": {
                "involves_minor": True,
                "master_confirm_token": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            },
            "emotion_text": "这个数据必须保护好",
            "scene_description": "涉及未成年人生物特征数据出境",
        },
    ]

    for case in cases:
        rw = evaluate(**case)
        print(f"操作：{rw.operation}")
        print(f"环境：{rw.environment}")
        print(f"情绪：{rw.emotion.wuxing} · {rw.emotion.emotion}（强度 {rw.emotion.intensity}/10）")
        print(f"场景安全：{rw.scene.risk_level} | {rw.scene.reason}")
        print(f"即时权重：{COLOR_LED[rw.final_color]['ansi']}{rw.final_color}{RESET} → {rw.final_action}")
        print(f"跑马灯：{_render_led(rw.led_pattern)}")
        print(f"DNA：{rw.dna}")
        print("-" * 60)


if __name__ == "__main__":
    main()
