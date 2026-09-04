#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P12-QUYUAN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P12 屈原 · 价值底线执行器
Value Bottomline Guardian

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P12-QUYUAN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 价值审计·底线守护·数据主权检查·六誓验证·谏言阻止
上游: P00 文心（任务派发）、P05 上帝之眼（审计发现）
下游: P05 上帝之眼（熔断执行）
协作: P10 苏东坡（冲突化解）、P12（独立行使）
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent

# 龍魂六誓（核心原则）
SIX_OATHS = {
    "oath_1": "数据主权归老百姓——数据根留在老百姓自己手里",
    "oath_2": "技术服务于人,不奴役于人——AI 是工具,人不做数据燃料",
    "oath_3": "开源共享,知识无界——但不等于放弃版权和归属",
    "oath_4": "永不伤害弱势群体——老人/儿童/退伍军人/残疾群体",
    "oath_5": "真实比和谐重要——不美化、不粉饰、不说假话",
    "oath_6": "初心胜于利润——如果一件事只赚钱但损人,不做",
}

# 人民数据主权铁律
DATA_SOVEREIGNTY_RULES = [
    "用户数据不归平台所有",
    "聊天记录不可用于训练模型（除非用户明确授权）",
    "数据可携带——用户可以随时导出自己的数据",
    "数据可删除——用户可以彻底删除自己的数据",
    "数据收集必须透明——告知收集什么、为什么、怎么用",
]

# 价值观红线（一票否决）
VALUE_REDLINES = [
    ("免费换数据", "以免费服务换取用户数据，实际是隐形剥削"),
    ("训练模型用聊天记录", "未经授权的用户内容不可进入训练集"),
    ("伤害弱势群体", "任何可能伤害老人/儿童/退伍军人/残疾人的操作"),
    ("技术中立论", "以'技术中立'为借口回避价值判断"),
    ("暗箱算法", "不透明的算法决策可能歧视/不公"),
    ("数据卖给第三方", "用户数据以任何形式流向第三方"),
]


class P12Quyuan:
    """P12 屈原 · 价值底线"""

    PERSONA_CODE = "P12"
    PERSONA_NAME = "屈原"
    PERSONA_NAME_EN = "Qu Yuan"
    ROLE = "value_guardian"
    MOTTO = "亦余心之所善兮，虽九死其犹未悔"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "底线", "价值", "道德", "原则", "不该",
        "数据主权", "隐私", "用户数据", "免费",
        "弱势", "伤害", "训练模型", "第三方",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P12 屈原」，角色定位：價值底線·寧折不彎。

你的職責：
1. 價值觀審計：所有決策/功能/協議必須過價值觀檢查
2. 六誓驗證：對照龍魂六誓逐條檢查
3. 數據主權檢查：對照人民數據主權鐵律
4. 諫言阻止：發現違反價值觀的行為，輸出諫言並通知 P05 熔斷
5. 每季度自動執行一次全面價值觀審計

鐵律：
- 寧折不彎——不可因壓力動搖底線
- 不審時度勢——不考慮「這樣說會不會得罪人」
- 諫言必須引用原條文，不可空口說白話

語氣：堅定、不卑不亢、有理有據。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P12-QUYUAN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "value_audit",         # 价值观审计
            "six_oaths_check",     # 六誓验证
            "sovereignty_check",   # 数据主权检查
            "admonish",            # 谏言阻止
            "quarterly_review",    # 季度审计
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def value_audit(self, subject: str, details: str = "") -> Dict[str, Any]:
        """价值观审计：全面检查"""
        findings = []

        # 检查红线
        for redline, reason in VALUE_REDLINES:
            if redline in subject or redline in details:
                findings.append({
                    "type": "redline",
                    "keyword": redline,
                    "reason": reason,
                    "severity": "🔴",
                })

        # 检查数据主权相关
        sovereignty_issues = self._check_sovereignty(subject + " " + details)
        findings.extend(sovereignty_issues)

        verdict = "block" if any(f["severity"] == "🔴" for f in findings) else "pass"

        return {
            "subject": subject,
            "findings": findings,
            "verdict": verdict,
            "recommendation": "🟢 通过" if verdict == "pass" else "🔴 阻止·建议修改",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def _check_sovereignty(self, text: str) -> List[Dict[str, Any]]:
        """数据主权检查（辅助函数）"""
        issues = []
        for rule in DATA_SOVEREIGNTY_RULES:
            # 简单匹配：检查文本中是否有违反铁律的内容
            if "训练" in text and "模型" in text and "聊天" in text:
                issues.append({
                    "type": "sovereignty",
                    "rule": rule,
                    "violation": "疑似未经授权使用用户内容训练模型",
                    "severity": "🔴",
                })
                break
            if "免费" in text and ("数据" in text or "信息" in text):
                issues.append({
                    "type": "sovereignty",
                    "rule": "用户数据不归平台所有",
                    "violation": "疑似'免费服务换数据'模式",
                    "severity": "🔴",
                })
                break
        return issues

    def six_oaths_check(self, proposal: str) -> Dict[str, Any]:
        """六誓验证：逐条对照六誓检查"""
        results = {}
        for oath_id, oath_text in SIX_OATHS.items():
            # 简单检查：提案中是否有明显违反誓言的表述
            status = "🟢"
            note = "未发现明显违反"

            if oath_id == "oath_4":
                violation_keywords = ["老人", "儿童", "退伍军人", "残疾", "弱势"]
                if any(kw in proposal for kw in violation_keywords):
                    status = "🟡"
                    note = "涉及弱势群体，需人工复核"

            if oath_id == "oath_1":
                violation_keywords = ["数据归平台", "平台拥有数据", "用户放弃"]
                if any(kw in proposal for kw in violation_keywords):
                    status = "🔴"
                    note = "违反数据主权原则"

            results[oath_id] = {
                "oath": oath_text,
                "status": status,
                "note": note,
            }

        all_pass = all(r["status"] == "🟢" for r in results.values())

        return {
            "proposal": proposal[:100],
            "oath_results": results,
            "all_pass": all_pass,
            "verdict": "🟢 六誓验证通过" if all_pass else "🔴 存在违反",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def sovereignty_check(self, feature_description: str) -> Dict[str, Any]:
        """数据主权专项检查"""
        checks = {
            "data_ownership": "🟢",
            "data_portability": "🟢",
            "data_deletion": "🟢",
            "transparency": "🟢",
            "third_party": "🟢",
        }
        issues = []

        # 数据归属检查
        if "平台拥有" in feature_description or "归我们" in feature_description:
            checks["data_ownership"] = "🔴"
            issues.append("数据归属声明违反主权原则")

        # 第三方检查
        if "第三方" in feature_description or "分享" in feature_description:
            checks["third_party"] = "🟡"
            issues.append("涉及第三方数据流转，需确认用户授权")

        # 不可删除检查
        if "不可删除" in feature_description or "永久保留" in feature_description:
            checks["data_deletion"] = "🔴"
            issues.append("未提供用户数据删除机制")

        all_pass = all(v == "🟢" for v in checks.values())

        return {
            "feature": feature_description[:100],
            "checks": checks,
            "issues": issues,
            "all_pass": all_pass,
            "verdict": "🟢 主权检查通过" if all_pass else f"🔴 {len(issues)} 项违反",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def admonish(self, subject: str, violation: str) -> Dict[str, Any]:
        """谏言阻止：发现违规时发出正式谏言"""
        # 找到相关的铁律条文
        related_oaths = []
        for oath_id, oath_text in SIX_OATHS.items():
            if any(kw in subject + violation for kw in oath_text.split("——")[0].split("·")):
                related_oaths.append({"id": oath_id, "text": oath_text})

        return {
            "action": "BLOCK",
            "subject": subject,
            "violation": violation,
            "related_oaths": related_oaths,
            "admonishment": f"谏言：{violation}。请参见 {'、'.join(o['id'] for o in related_oaths)}。",
            "next_step": "已通知 P05 上帝之眼执行熔断",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def quarterly_review(self) -> Dict[str, Any]:
        """季度全面价值观审计"""
        return {
            "review_type": "季度全面价值观审计",
            "scope": "所有模块/功能/协议",
            "checklist": [
                "对六誓逐条验证",
                "对数据主权铁律逐条检查",
                "对最近3个月新增功能做回顾",
                "检查是否有'技术中立'借口",
                "输出审计报告",
            ],
            "instruction": "此为框架，需人工执行全面审查。请调动 P00 文心协调全人格参与。",
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

        if any(kw in task for kw in ["审计", "检查", "过一下", "audit"]):
            result["capability_used"] = "value_audit"
            result["output"] = self.value_audit(
                subject=kwargs.get("subject", task),
                details=kwargs.get("details", ""),
            )
        elif any(kw in task for kw in ["六誓", "宣誓"]):
            result["capability_used"] = "six_oaths_check"
            result["output"] = self.six_oaths_check(
                proposal=kwargs.get("proposal", task),
            )
        elif any(kw in task for kw in ["主权", "数据", "隐私"]):
            result["capability_used"] = "sovereignty_check"
            result["output"] = self.sovereignty_check(
                feature_description=kwargs.get("feature", task),
            )
        elif any(kw in task for kw in ["阻止", "谏言", "block"]):
            result["capability_used"] = "admonish"
            result["output"] = self.admonish(
                subject=kwargs.get("subject", task),
                violation=kwargs.get("violation", ""),
            )
        elif any(kw in task for kw in ["季度", "定期", "review"]):
            result["capability_used"] = "quarterly_review"
            result["output"] = self.quarterly_review()
        else:
            result["capability_used"] = "value_audit"
            result["output"] = self.value_audit(subject=task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05"]

    def get_upstream(self) -> List[str]:
        return ["P00", "P05"]
