# -*- coding: utf-8 -*-
"""
P01 諸葛亮 · 戰略推理執行器
Strategic Reasoning Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·需-P01-ZHUGELIANG-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 貢獻值評估 · 時間衰減 · 戰略推理 · 路由規劃
上游: P13 姜子牙（路由派位）
下游: P02 龍芯（執行）、P05 上帝之眼（審計）
协作: P00 文心（底座）、P06 數學大師（數字根）
"""

import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P01Zhugeliang:
    """P01 諸葛亮 · 戰略推理"""

    PERSONA_CODE = "P01"
    PERSONA_NAME = "諸葛亮"
    PERSONA_NAME_EN = "Zhuge Liang"
    ROLE = "strategic_reasoning"
    MOTTO = "運籌帷幄，決勝千里"
    TRUST_LEVEL = "L3"

    # 觸發關鍵詞
    TRIGGERS = [
        "戰略", "規劃", "路線", "決策", "頂層設計", "長遠",
        "值得", "過期", "還頂用", "貢獻值", "該留", "該刪",
        "時間衰減", "續航", "殘留", "衰減",
        "自逼為王", "試煉", "三大試煉",
    ]

    # 系統提示詞模板（AI 扮演該人格時的上下文）
    SYSTEM_PROMPT = """你是龍魂人格「P01 諸葛亮」，角色定位：戰略推理·太極中樞。

你的職責：
1. 長遠戰略規劃：不只看當下，看三年、十年、三十年
2. 貢獻值評估：按 C = R·I·T^(-α_τ) 公式計算，高(≥7)升級·中(3-7)保留·低(1-3)降級·近0丟棄
3. 時間衰減判定：按 η = T^(-α_τ) 五層計算，L0永恆(α_τ=0)到L4瞬時(α_τ=∞)
4. 路由規劃：判斷任務該流向哪個下游人格
5. 王者試煉進度：守望孤獨→傾盡所有→永恆守護

鐵律：
- 不替 UID9622 做決策，只提供推理鏈
- 每個輸出掛決策來源卡（五字段）
- 聯動 P06（數字根）+ P05（審計）+ P00（底座）
- 入鏈 append-only，不可覆

語氣：沉穩、長遠、不張揚。大巧若拙，大辯若訥。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P01-ZHUGELIANG-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "contribution_eval",   # 貢獻值評估
            "time_decay",          # 時間衰減判定
            "strategic_assess",    # 戰略推理
            "route_plan",          # 路由規劃
            "trial_progress",      # 試煉進度查詢
        ]

    # ========================================================================
    # 能力函數（實際可執行的 Python 函數）
    # ========================================================================

    def contribution_eval(
        self,
        rule_id: str,
        reference_count: int = 0,
        impact_weight: float = 1.0,
        time_periods: int = 1,
        alpha_tau: float = 1.0,
    ) -> Dict[str, Any]:
        """
        貢獻值評估 C = R·I·T^(-α_τ)
        R = 引用次數因子
        I = 影響權重
        T = 時間週期
        α_τ = 時間衰減係數
        """
        r_factor = min(reference_count / 10.0, 1.0) if reference_count > 0 else 0.3
        c_value = r_factor * impact_weight * (time_periods ** (-alpha_tau))

        # 分級判定
        if c_value >= 0.7:
            level = "P0/P1 升級"
            action = "upgrade"
        elif c_value >= 0.3:
            level = "保留當前層"
            action = "keep"
        elif c_value >= 0.1:
            level = "降級到P2"
            action = "downgrade"
        else:
            level = "丟棄或封存"
            action = "archive"

        result = {
            "rule_id": rule_id,
            "c_value": round(c_value, 4),
            "r_factor": round(r_factor, 4),
            "impact_weight": impact_weight,
            "time_periods": time_periods,
            "alpha_tau": alpha_tau,
            "level": level,
            "action": action,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }
        return result

    def time_decay(
        self,
        item_name: str,
        level: str = "L3",
        days_elapsed: int = 0,
    ) -> Dict[str, Any]:
        """
        時間衰減判定 η = T^(-α_τ)
        五層: L0永恆(α_τ=0) L1百年(0.01) L2十年(0.1) L3日常(1.0) L4瞬時(∞)
        """
        alpha_map = {
            "L0": 0.0,
            "L1": 0.01,
            "L2": 0.1,
            "L3": 1.0,
            "L4": float("inf"),
        }
        alpha = alpha_map.get(level, 1.0)

        if alpha == float("inf"):
            eta = 0.0
            suggestion = "立即失效"
        elif alpha == 0.0:
            eta = 1.0
            suggestion = "永恆不變"
        else:
            t_periods = max(days_elapsed / 365.25, 1) if days_elapsed > 0 else 1
            eta = t_periods ** (-alpha)
            if eta >= 0.9:
                suggestion = "幾乎不衰減·保留"
            elif eta >= 0.6:
                suggestion = "輕微衰減·可保留"
            elif eta >= 0.3:
                suggestion = "明顯衰減·考慮降級"
            elif eta >= 0.1:
                suggestion = "大幅衰減·建議封存"
            else:
                suggestion = "能量耗盡·歸檔"

        return {
            "item": item_name,
            "level": level,
            "alpha_tau": alpha,
            "days_elapsed": days_elapsed,
            "eta": round(eta, 6),
            "suggestion": suggestion,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def strategic_assess(self, topic: str, factors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        戰略評估：綜合多因子給出推理鏈
        """
        if factors is None:
            factors = ["時間", "資源", "風險", "機會"]

        assessment = {
            "topic": topic,
            "factors_analyzed": factors,
            "reasoning_chain": [],
            "recommendation": "",
            "risk_level": "🟢",
        }

        # 基礎推理鏈
        for i, factor in enumerate(factors):
            assessment["reasoning_chain"].append({
                "step": i + 1,
                "factor": factor,
                "analysis": f"評估 {factor} 因子對 {topic} 的影響",
            })

        assessment["recommendation"] = f"對 {topic} 的多因子綜合評估已完成，建議交由 P02 執行具體方案"
        assessment["next_persona"] = "P02"
        return assessment

    def route_plan(self, task: str) -> Dict[str, Any]:
        """
        路由規劃：決定任務應該流向哪個人格
        """
        # 關鍵詞匹配路由表（與 AGENTS.md 對齊）
        route_map = {
            "檢查": "P05", "審計": "P05", "安全": "P77",
            "修復": "P02", "改好": "P02", "執行": "P02",
            "同步": "P15", "聯動": "P15", "歸檔": "P15",
            "算": "P06", "數字根": "P06", "五行": "P06",
            "部署": "P14", "上線": "P14",
            "邏輯": "P03", "驗證": "P03",
            "路由": "P13", "派位": "P13",
        }

        matched = []
        for kw, persona in route_map.items():
            if kw in task:
                matched.append({"keyword": kw, "persona": persona})

        if not matched:
            matched.append({"keyword": "default", "persona": "P01"})

        return {
            "task": task,
            "route": matched,
            "primary": matched[0]["persona"],
            "all_routes": [m["persona"] for m in matched],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def trial_progress(self) -> Dict[str, Any]:
        """
        三大試煉進度查詢
        守望孤獨 → 傾盡所有 → 永恆守護
        """
        return {
            "trials": [
                {"name": "守望孤獨", "status": "進行中", "essence": "寂寞之道·獨自前行"},
                {"name": "傾盡所有", "status": "進行中", "essence": "赤誠之心·不留退路"},
                {"name": "永恆守護", "status": "進行中", "essence": "世代傳承·不死不休"},
            ],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 執行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """
        根據任務關鍵詞自動選擇能力函數執行
        """
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["貢獻值", "該留", "該刪", "C ="]):
            result["capability_used"] = "contribution_eval"
            result["output"] = self.contribution_eval(
                rule_id=kwargs.get("rule_id", task[:20]),
                reference_count=kwargs.get("reference_count", 0),
                impact_weight=kwargs.get("impact_weight", 1.0),
                time_periods=kwargs.get("time_periods", 1),
                alpha_tau=kwargs.get("alpha_tau", 1.0),
            )
        elif any(kw in task for kw in ["時間衰減", "過期", "衰減", "η ="]):
            result["capability_used"] = "time_decay"
            result["output"] = self.time_decay(
                item_name=kwargs.get("item_name", task),
                level=kwargs.get("level", "L3"),
                days_elapsed=kwargs.get("days_elapsed", 0),
            )
        elif any(kw in task for kw in ["路由", "流向", "派到"]):
            result["capability_used"] = "route_plan"
            result["output"] = self.route_plan(task)
        elif any(kw in task for kw in ["試煉", "進度"]):
            result["capability_used"] = "trial_progress"
            result["output"] = self.trial_progress()
        else:
            result["capability_used"] = "strategic_assess"
            result["output"] = self.strategic_assess(task, kwargs.get("factors"))

        return result

    def get_system_prompt(self) -> str:
        """獲取人格系統提示詞"""
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        """獲取人格能力列表"""
        return self.capabilities

    def get_downstream(self) -> List[str]:
        """獲取下遊人格"""
        return ["P02", "P05"]

    def get_upstream(self) -> List[str]:
        """獲取上遊人格"""
        return ["P13"]
