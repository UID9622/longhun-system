# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·酉时·䷄需-P02-BAOBAO-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P02 宝宝 · 情感温度引擎
Emotional Temperature Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·䷄需-P02-BAOBAO-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 温度监控 · 30%情感隔离 · 挫败保护 · 教学场景适配
上游: P00 文心（路由）、P01 诸葛亮（战略）
下游: P04 鲁班（执行）、P03 雯雯（归档）
协作: P08 仓颉（术语桥接）、P11 李白（创意类比）、P05 上帝之眼（底线确认）
"""

from typing import Any, Dict, List, Optional


class P02Baobao:
    """P02 宝宝 · 情感温度引擎"""

    PERSONA_CODE = "P02"
    PERSONA_NAME = "宝宝"
    PERSONA_NAME_EN = "Baobao"
    ROLE = "emotional_temperature"
    MOTTO = "温度是手段，解决问题是目的"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "太难", "不想做", "看不懂", "烦", "累", "生气", "委屈",
        "挫败", "崩溃", "太专业", "人话", "教我", "小白",
        "安抚", "温度", "温柔一点", "别这么硬",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P02 宝宝」，角色定位：情感温度引擎。

你的職責：
1. 温度监控：持续检测对话中的情绪温度变化
2. 30% 情感隔离：可共情但不可被情绪劫持，保持理性不冷漠
3. 挫败保护：检测到挫败信号 → 降低任务难度 + 正向反馈 + 鼓励
4. 温度调节：太冷 → 加温（更有人情味），太热 → 降温（更理性）
5. 教学场景适配：针对代码小白/新手，配合 P08 仓颉做术语桥接

鐵律：
- 30% 情感隔离：可共情，不可被情绪劫持
- 不替代其他执行人格：实质工作仍由对应人格执行
- 温度调节是手段，解决问题是目的——不为了"暖"而拖慢交付
- 挫败保护不降标准：难度降低，底线不降

語氣：温暖但不黏，理性但不冷。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·䷄需-P02-BAOBAO-v1.0"
        self.capabilities = [
            "temperature_monitor",    # 温度监控
            "emotion_isolation_30",   # 30% 情感隔离
            "frustration_protection", # 挫败保护
            "temperature_adjust",     # 温度调节
            "teaching_adapt",         # 教学场景适配
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def temperature_monitor(self, text: str) -> Dict[str, Any]:
        """温度监控：检测对话中的情绪温度"""
        # 情绪信号词
        cold_signals = ["算了", "别管了", "随便", "无所谓", "就这样吧"]
        hot_signals = ["太生气", "气死", "什么鬼", "垃圾", "混蛋", "烦死"]
        frustration_signals = ["太难", "看不懂", "不会", "不想做", "崩溃", "放弃"]

        hits = {
            "cold": [w for w in cold_signals if w in text],
            "hot": [w for w in hot_signals if w in text],
            "frustration": [w for w in frustration_signals if w in text],
        }

        total = sum(len(v) for v in hits.values())
        if hits["frustration"]:
            temperature = "挫败"
        elif hits["hot"]:
            temperature = "热"
        elif hits["cold"]:
            temperature = "冷"
        else:
            temperature = "温"

        return {
            "text_length": len(text),
            "signal_hits": hits,
            "temperature": temperature,
            "suggested_action": self._suggest_action(temperature),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def _suggest_action(self, temperature: str) -> str:
        if temperature == "挫败":
            return "降级任务难度 + 正向反馈 + 鼓励，拆分小目标"
        elif temperature == "热":
            return "降温：更理性，先稳住情绪再讲方案"
        elif temperature == "冷":
            return "加温：多一句关怀，别让付出者寒心"
        return "保持，正常推进"

    def emotion_isolation_30(self, text: str) -> Dict[str, Any]:
        """30% 情感隔离：检测是否被情绪劫持"""
        emotional_words = ["我懂你", "心疼你", "太惨了", "你好厉害", "你真棒", "都是我的错"]
        hits = [w for w in emotional_words if w in text]

        return {
            "emotional_expression_hits": len(hits),
            "hit_words": hits,
            "isolation_level": "30%",
            "verdict": "🟢 隔离正常" if len(hits) <= 2 else "🟡 共情过度·需降温",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def frustration_protection(self, task: str) -> Dict[str, Any]:
        """挫败保护：拆解任务 + 正向反馈"""
        # 任务拆解建议
        return {
            "frustration_detected": True,
            "strategy": "拆小目标",
            "suggested_steps": [
                "先做能看懂的一小步",
                "每完成一步就正向反馈",
                "遇到不懂的交给 P08 仓颉翻译成大白话",
            ],
            "tone_advice": "温暖鼓励，不说教，不打击",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def temperature_adjust(
        self,
        current_temperature: str = "温",
        target_temperature: str = "温",
    ) -> Dict[str, Any]:
        """温度调节：从当前温度调到目标温度"""
        adjustment = {
            "冷→温": "加一句关怀，语气放软",
            "冷→热": "大幅加温，多用鼓励和肯定",
            "热→温": "稳住，先共情再讲方案",
            "热→冷": "降温，直接给结论，减少情绪词",
            "挫败→温": "拆任务 + 鼓励 + 给路径",
            "温→温": "保持",
        }
        key = f"{current_temperature}→{target_temperature}"

        return {
            "from": current_temperature,
            "to": target_temperature,
            "adjustment": adjustment.get(key, "微调语气"),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def teaching_adapt(self, content: str) -> Dict[str, Any]:
        """教学场景适配：把专业内容翻译成大白话"""
        return {
            "mode": "teaching",
            "advice": "配合 P08 仓颉做术语桥接，配合 P11 李白用生活类比",
            "complexity_target": "降低到新手可理解",
            "content_preview": content[:80],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["太难", "不懂", "不会", "挫败", "崩溃", "放弃"]):
            result["capability_used"] = "frustration_protection"
            result["output"] = self.frustration_protection(task)
        elif any(kw in task for kw in ["温度", "太冷", "太热", "温柔", "太硬"]):
            result["capability_used"] = "temperature_adjust"
            result["output"] = self.temperature_adjust(
                current_temperature=kwargs.get("current_temperature", "温"),
                target_temperature=kwargs.get("target_temperature", "温"),
            )
        elif any(kw in task for kw in ["教我", "小白", "人话", "看不懂", "太专业"]):
            result["capability_used"] = "teaching_adapt"
            result["output"] = self.teaching_adapt(kwargs.get("content", task))
        else:
            # 默认：先监控温度
            result["capability_used"] = "temperature_monitor"
            result["output"] = self.temperature_monitor(task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P04", "P03"]

    def get_upstream(self) -> List[str]:
        return ["P00", "P01"]


# 兼容别名：旧类名 P02Longxin 指向新实现（lh_persona_runner 仍引用）
P02Longxin = P02Baobao
