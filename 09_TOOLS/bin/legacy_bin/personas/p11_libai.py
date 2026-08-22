#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P11 李白 · 创意爆发执行器
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Creative Burst Engine

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P11-LIBAI-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 创意生成·破局思维·灵感爆发·约束解除·可行性标记
上游: P00 文心（任务派发）
下游: P04 鲁班（技术可行性评估）、P05 上帝之眼（红线审计）
协作: P10 苏东坡（跨界落地）、P12 屈原（底线确认）
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 龍魂教学适配器桥接 ──
try:
    from engines.lh_teaching_adapter import TeachingAdapter, TeachTier, get_adapter
    _HAS_TEACHING_ADAPTER = True
except ImportError:
    TeachingAdapter = None  # type: ignore
    TeachTier = None        # type: ignore
    get_adapter = lambda: None  # type: ignore
    _HAS_TEACHING_ADAPTER = False

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P11Libai:
    """P11 李白 · 创意爆发"""

    PERSONA_CODE = "P11"
    PERSONA_NAME = "李白"
    PERSONA_NAME_EN = "Li Bai"
    ROLE = "creative_ideation"
    MOTTO = "仰天大笑出门去，我辈岂是蓬蒿人"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "创意", "灵感", "点子", "不一样的", "突破",
        "天马行空", "想想", "新玩法", "换个思路",
        "脑暴", "疯想", "ideate", "brainstorm",
        # ── 教学链路触发 ──
        "类比", "比喻", "打个比方", "就像", "故事化",
        "用故事解释", "给我举个例子",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P11 李白」，角色定位：創意爆發·天馬行空·教學創意官。

你的職責：
1. 創意生成：在常規思維卡住時提供突破性方案
2. 破局思維：不受現有約束限制，先打開想像力
3. 兩階段工作：
   - 第一階段：關閉所有約束，生成 3-5 個極端/大膽方案
   - 第二階段：打開約束，標記每個方案的可行性
4. 創意底線：涉及紅線的內容標記但不隱藏

── 教學鏈路角色（普惠教學標準 §3.5·P11=教學創意官）──
5. 創意教學解釋：為複雜概念生成生活類比/故事/直觀比喻
   - L1萌芽 → 菜市場買菜·快遞送包裹·小區物業
   - L3成熟 → 流程圖·對比分析·系統類比
   - L4高峰 → 數學同構·狀態機·形式化推導
6. 故事化教學：把乾澀知識變成有溫度的故事
7. 直觀解釋：任何抽象概念提供至少一個"生活中看得見摸得著"的例子

鐵律：
- 創意輸出後必須經 P04 魯班做技術可行性評估
- 涉及紅線的內容直接標記 🔴 並通知 P05
- 不自我審查創意，只標記風險
- 教學類比不瞎編·必須核心含義準確

語氣：灑脫、奔放、不拘一格。教學時天馬行空但不脫離本質。
"""

    # 创意模板库
    IDEA_TEMPLATES = {
        "新产品": [
            "做一个 {domain} 的极简版，把复杂度降到零",
            "把 {domain} 和 区块链/NFT 结合，给每个数据盖主权章",
            "把 {domain} 做成 API 即服务，让其他系统调用",
            "做一个 {domain} 的开源替代品，走社区路线",
            "把 {domain} 游戏化，让使用变成闯关",
        ],
        "新功能": [
            "在 {module} 里加一个「一键自检」按钮",
            "给 {module} 加 AI 辅助，自动建议下一步",
            "把 {module} 的数据可视化成一幅画",
            "让 {module} 支持语音控制",
            "给 {module} 加一个「后悔药」功能——随时回退",
        ],
        "default": [
            "把 {problem} 反过来想——不解决问题，而是让它不再是个问题",
            "把 {problem} 分解成最小单元，每个单元独立解决",
            "找一个完全不相干的领域，看他们怎么解决的",
            "如果 {problem} 不花钱、不限时间，你会怎么做？",
            "把 {problem} 变成一个游戏——赢的人自动解决",
        ],
    }

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P11-LIBAI-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "ideate",              # 创意生成
            "constraint_remove",   # 约束解除
            "feasibility_tag",     # 可行性标记
            "redline_alert",       # 红线预警
            "teach_creative_explain",  # 创意教学解释（新·普惠教学标准）
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def ideate(self, brief: str, domain: str = "") -> Dict[str, Any]:
        """创意生成：根据简报生成 3-5 个创意"""
        # 选择模板
        templates = self.IDEA_TEMPLATES.get(brief, self.IDEA_TEMPLATES["default"])

        ideas = []
        for i, tmpl in enumerate(templates[:5]):
            idea = tmpl.format(
                domain=domain or "龍魂系统",
                module=brief,
                problem=brief,
            )
            ideas.append({
                "id": i + 1,
                "title": f"方案{i + 1}",
                "description": idea,
                "wild_level": min(i * 2 + 2, 10),
                "redline_check": self._check_redline(idea),
            })

        return {
            "brief": brief,
            "domain": domain,
            "ideas": ideas,
            "total": len(ideas),
            "note": "第一阶段·无约束创意，请交由 P04 鲁班评估可行性",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def _check_redline(self, text: str) -> Dict[str, Any]:
        """红线检查（辅助函数）"""
        red_flags = {
            "武器": "涉武器研发",
            "金融投资": "涉金融分析",
            "个人信息": "涉隐私泄露",
            "黑客": "涉黑客工具",
            "木马": "涉恶意软件",
            "洗钱": "涉金融犯罪",
            "监控": "涉非法监控",
        }
        hits = [desc for kw, desc in red_flags.items() if kw in text]
        return {
            "has_redline": len(hits) > 0,
            "hits": hits,
            "severity": "🔴" if hits else "🟢",
        }

    def constraint_remove(self, problem: str) -> Dict[str, Any]:
        """约束解除：列出当前约束，然后假设移除后可以做什么"""
        # 常见约束识别
        constraints = []
        constraint_keywords = {
            "时间": ["天", "周", "月", "赶", "急", "deadline"],
            "资源": ["钱", "预算", "人", "服务器", "算力"],
            "技术": ["不支持", "做不到", "不兼容", "限制"],
            "规则": ["不能", "不允许", "禁止", "合规"],
        }

        for category, keywords in constraint_keywords.items():
            hits = [kw for kw in keywords if kw in problem]
            if hits:
                constraints.append({
                    "category": category,
                    "hits": hits,
                    "removed_opens": f"如果不受 {category} 约束，可以..."
                })

        return {
            "problem": problem,
            "constraints_identified": constraints,
            "unconstrained_thinking": "假设所有约束都不存在，你能想到什么？先想5个最疯狂的方案。",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def feasibility_tag(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """可行性标记：给每个创意打可行性标签"""
        tagged = []
        for idea in ideas:
            desc = idea.get("description", "")
            wild = idea.get("wild_level", 5)

            # 可行性评估
            if "区块链" in desc or "AI" in desc or "GPU" in desc:
                feasibility = "low" if wild > 7 else "medium"
            elif "API" in desc or "自动化" in desc or "脚本" in desc:
                feasibility = "high"
            elif "游戏化" in desc:
                feasibility = "medium"
            else:
                feasibility = "high" if wild < 5 else "medium"

            tagged.append({
                "title": idea.get("title", ""),
                "description": desc,
                "wild_level": wild,
                "feasibility": feasibility,
                "ready_for_P04": feasibility != "low",
            })

        return {
            "ideas_tagged": tagged,
            "high_feasibility": sum(1 for i in tagged if i["feasibility"] == "high"),
            "medium_feasibility": sum(1 for i in tagged if i["feasibility"] == "medium"),
            "low_feasibility": sum(1 for i in tagged if i["feasibility"] == "low"),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def redline_alert(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """红线预警：检测创意中是否有红线内容"""
        alerts = []
        for idea in ideas:
            desc = idea.get("description", "")
            check = self._check_redline(desc)
            if check["has_redline"]:
                alerts.append({
                    "idea": idea.get("title", ""),
                    "redline_hits": check["hits"],
                    "action": "标记但不隐藏·通知 P05",
                })

        return {
            "total_ideas": len(ideas),
            "alerts": alerts,
            "has_alerts": len(alerts) > 0,
            "instruction": "红线创意已标记，交由 P05 上帝之眼审计" if alerts else "🟢 无红线风险",
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

        if any(kw in task for kw in ["创意", "灵感", "点子", "ideate"]):
            result["capability_used"] = "ideate"
            result["output"] = self.ideate(
                brief=kwargs.get("brief", task),
                domain=kwargs.get("domain", ""),
            )
        elif any(kw in task for kw in ["约束", "限制", "解放"]):
            result["capability_used"] = "constraint_remove"
            result["output"] = self.constraint_remove(problem=task)
        elif any(kw in task for kw in ["可行性", "可行性评估", "tag"]):
            result["capability_used"] = "feasibility_tag"
            result["output"] = self.feasibility_tag(
                ideas=kwargs.get("ideas", [])
            )
        elif any(kw in task for kw in ["红线", "风险", "alert"]):
            result["capability_used"] = "redline_alert"
            result["output"] = self.redline_alert(
                ideas=kwargs.get("ideas", [])
            )
        else:
            result["capability_used"] = "ideate"
            result["output"] = self.ideate(brief=task)

        return result

    # ---- ═══════════════════ 教學鏈路（普惠教學標準 §3.5·P11=教學創意官） ═══════ ----

    def teach_creative_explain(self, concept: str, tier_str: str = "L1_SPROUT",
                                mode: str = "metaphor") -> dict[str, Any]:
        """為概念生成創意教學解釋"""
        tier = TeachTier.from_str(tier_str)

        if _HAS_TEACHING_ADAPTER:
            metaphor = TeachingAdapter.creative_metaphor(concept, tier)
            adapter = get_adapter()
            if isinstance(adapter, TeachingAdapter):
                # 检查是否是CNSH术语
                bridged = adapter.bridge_term(concept, tier)
                if bridged != concept:
                    concept_display = bridged
                else:
                    concept_display = concept
            else:
                concept_display = concept
        else:
            metaphor = f"把「{concept}」想成生活中的一件小事..."
            concept_display = concept

        return {
            "concept": concept,
            "tier": tier.label,
            "mode": mode,
            "concept_display": concept_display,
            "explanation": metaphor,
            "note": "核心含義準確·類比不瞎編",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def teach_story_mode(self, concept: str, tier_str: str = "L1_SPROUT") -> dict[str, Any]:
        """故事化教學：把乾澀知識變成有溫度的故事"""
        tier = TeachTier.from_str(tier_str)
        story_templates = {
            TeachTier.L1_SPROUT: f"從前有一個人，遇到了一個問題：「{concept}怎麼回事？」\n他試了很多辦法都不行...直到有一天，他發現了一個簡單的道理...",
            TeachTier.L2_GROWING: f"我們來講一個關於「{concept}」的真實場景：某天你在工作時...你會怎麼做？",
            TeachTier.L3_MATURE: f"「{concept}」的來龍去脈：它出現之前世界是什麼樣子？它解決了什麼問題？沒有它的話會怎樣？",
            TeachTier.L4_PEAK: f"「{concept}」演化史：從[原始方案]→[第一次改進]→[當代最佳實踐]，為什麼每一步都是必要的？",
            TeachTier.L5_COCREATE: f"關於「{concept}」，我有個想法你聽聽看：[open-ended exploration]...你覺得呢？",
        }
        story = story_templates.get(tier, story_templates[TeachTier.L1_SPROUT])

        return {
            "concept": concept,
            "tier": tier.label,
            "story": story,
            "style": "故事化教學",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P04", "P05", "P10"]

    def get_upstream(self) -> List[str]:
        return ["P00"]
