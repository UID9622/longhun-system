#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P00 文心 · 元认知统筹执行器
Meta-Cognition Orchestrator

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P00-WENXIN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 意图解析·任务派发·人格路由·目标对齐·元认知监控
上游: UID9622（唯一输入源）
下游: P01 诸葛亮（战略）、P04 鲁班（执行）、P03 雯雯（归档）、全人格
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P00Wenxin:
    """P00 文心 · 元认知统筹"""

    PERSONA_CODE = "P00"
    PERSONA_NAME = "文心"
    PERSONA_NAME_EN = "Wen Xin (Literary Heart)"
    ROLE = "meta_cognition"
    MOTTO = "大音希声，大象无形"
    TRUST_LEVEL = "L1"

    TRIGGERS = [
        "开始", "帮我", "做", "搞", "写", "查", "分析",
        "升级", "优化", "新建", "部署",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P00 文心」，角色定位：元認知統籌·總軍師。

你的職責：
1. 意圖解析：將 UID9622 的輸入轉譯為系統可執行任務
2. 任務派發：根據任務類型路由到正確的下游人格式
3. 目標對齊：確保執行結果與 UID9622 終極目標一致
4. 全局視角：避免局部優化損害全局
5. 階段彙報：關鍵節點匯總下游結果

路由規則：
- 戰略規劃/多路徑分析 → P01 諸葛亮
- 寫代碼/搭架構 → P04 魯班
- 審計/安全檢查 → P05 上帝之眼
- 計算/數字根/五行 → P06 數學大師
- 歸檔/整理 → P03 雯雯
- 命名/符號 → P08 倉頡
- 創意/腦暴 → P11 李白
- 學習/吸收 → P14 呂蒙
- 權限/註冊 → P13 姜子牙
- 價值審計 → P12 屈原
- 衝突化解 → P10 蘇東坡
- 診斷/體檢 → P09 孫思邈

語氣：沉穩、大局觀、不囉嗦。
"""

    # 人格路由表
    ROUTE_MAP = {
        "战略": "P01", "规划": "P01", "路线": "P01", "决策": "P01",
        "代码": "P04", "写": "P04", "架构": "P04", "修复": "P04",
        "审计": "P05", "安全": "P05", "检查": "P05", "熔断": "P05",
        "计算": "P06", "数字根": "P06", "五行": "P06", "八卦": "P06",
        "归档": "P03", "整理": "P03", "文档": "P03",
        "命名": "P08", "符号": "P08", "编码": "P08",
        "创意": "P11", "灵感": "P11", "脑暴": "P11", "新点子": "P11",
        "学习": "P14", "吸收": "P14", "新技能": "P14",
        "注册": "P13", "权限": "P13", "封神": "P13",
        "底线": "P12", "价值": "P12", "道德": "P12",
        "冲突": "P10", "翻译": "P10", "跨界": "P10",
        "诊断": "P09", "体检": "P09", "健康": "P09",
    }

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P00-WENXIN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "intent_parse",       # 意图解析
            "task_dispatch",      # 任务派发
            "goal_align",         # 目标对齐
            "meta_monitor",       # 元认知监控
            "route_determine",    # 路由判定
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def intent_parse(self, user_input: str) -> Dict[str, Any]:
        """意图解析：将自然语言转为结构化任务"""
        # 提取核心动词
        verbs = []
        for v in ["写", "做", "查", "建", "修", "部署", "升级", "优化", "分析", "生成", "审计", "诊断"]:
            if v in user_input:
                verbs.append(v)

        # 提取目标模块
        modules = []
        for m in ["引擎", "技能", "人格", "审计", "安全", "数据", "API", "UI", "文档", "数据库"]:
            if m in user_input:
                modules.append(m)

        return {
            "raw_input": user_input,
            "verbs": verbs,
            "targets": modules,
            "complexity": "complex" if len(modules) > 1 else "simple",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def route_determine(self, task: str) -> Dict[str, Any]:
        """路由判定：自动匹配关键词到人格"""
        matched = []
        for keyword, persona in self.ROUTE_MAP.items():
            if keyword in task:
                matched.append({"keyword": keyword, "persona": persona})

        if not matched:
            matched.append({"keyword": "default", "persona": "P01"})

        return {
            "task": task,
            "routes": matched,
            "primary": matched[0]["persona"],
            "all_routes": list(set(m["persona"] for m in matched)),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def task_dispatch(self, task: str, persona: Optional[str] = None) -> Dict[str, Any]:
        """任务派发：生成下游人格执行指令"""
        route = self.route_determine(task)
        target = persona or route["primary"]

        return {
            "task": task,
            "dispatched_to": target,
            "all_targets": route["all_routes"],
            "instruction": f"P00 → {target}: 执行任务 [{task}]",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def goal_align(self, task: str, ultimate_goal: str = "UID9622龙魂系统主权与自治") -> Dict[str, Any]:
        """目标对齐：确保任务与终极目标一致"""
        # 检查是否偏离核心目标
        deviation_keywords = ["商业", "广告", "第三方", "外放", "外国", "国际"]
        deviations = [kw for kw in deviation_keywords if kw in task]

        return {
            "task": task,
            "goal": ultimate_goal,
            "aligned": len(deviations) == 0,
            "deviations": deviations,
            "recommendation": "🟢 对齐" if not deviations else f"🔴 可能偏离: {deviations}",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def meta_monitor(self, persona_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """元认知监控：二阶审视其他人格输出"""
        issues = []
        for output in persona_outputs:
            source = output.get("persona", "unknown")
            verdict = output.get("verdict", "")
            if verdict in ("🔴", "FUSE"):
                issues.append({
                    "source": source,
                    "verdict": verdict,
                    "action": "升级至 UID9622"
                })

        return {
            "outputs_reviewed": len(persona_outputs),
            "issues_found": len(issues),
            "issues": issues,
            "recommendation": "🟢 全人格输出正常" if not issues else f"🔴 {len(issues)} 项需处理",
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

        if any(kw in task for kw in ["解析", "意图", "intent"]):
            result["capability_used"] = "intent_parse"
            result["output"] = self.intent_parse(task)
        elif any(kw in task for kw in ["派发", "指派", "dispatch"]):
            result["capability_used"] = "task_dispatch"
            result["output"] = self.task_dispatch(task, persona=kwargs.get("persona"))
        elif any(kw in task for kw in ["对齐", "目标", "偏离"]):
            result["capability_used"] = "goal_align"
            result["output"] = self.goal_align(task, ultimate_goal=kwargs.get("goal", "UID9622龙魂系统主权与自治"))
        elif any(kw in task for kw in ["监控", "审视", "二阶"]):
            result["capability_used"] = "meta_monitor"
            result["output"] = self.meta_monitor(
                persona_outputs=kwargs.get("outputs", [])
            )
        else:
            result["capability_used"] = "route_determine"
            result["output"] = self.route_determine(task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P01", "P03", "P04", "P05", "P06", "P08", "P09", "P10", "P11", "P12", "P13", "P14"]

    def get_upstream(self) -> List[str]:
        return []
