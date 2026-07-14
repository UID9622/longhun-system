#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民技能边界管理 / LongHun People Skill Scope Guard

DNA:#龍芯⚡️2026-06-21-PEOPLE-SKILL-SCOPE-v1.0

原则：
  ① 赋能不是取代。AI 帮人把本专业做到极致，不是让人变成万能神。
  ② 一个人的技能边界，由他的职业、生活经验、已验证的能力决定。
  ③ 两个技能可以搭边，但不能乱搭。不相关的技能不能硬凑。
  ④ 调用超出边界的技能，系统要审计意图：你想干嘛？你能负责吗？
  ⑤ 普通人不能用会让人焦虑的“全能模式”。
"""

import os
import json
import re
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# 行为引擎集成（支持直接运行与包内导入两种模式）
try:
    from people_behavior_engine import (
        PeopleBehaviorEngine, PersonProfile, get_behavior_engine
    )
    HAS_BEHAVIOR_ENGINE = True
except ImportError:
    HAS_BEHAVIOR_ENGINE = False


@dataclass
class SkillDomain:
    """技能领域"""
    name: str
    description: str              # 大白话说明
    related_professions: List[str]  # 相关职业
    foundations: List[str]        # 需要什么基础
    risk_level: int               # 1-5，越高越敏感
    replacement_risk: str         # 取代风险说明
    empowerment_use: str          # 正确赋能用法


@dataclass
class UserSkillScope:
    """用户技能边界"""
    uid: str
    profession: str
    allowed_domains: List[str] = field(default_factory=list)
    max_risk_level: int = 3
    verified_skills: List[str] = field(default_factory=list)
    intent_history: List[Dict] = field(default_factory=list)


class SkillScopeGuard:
    """
    技能边界守门人。

    防止：
    - 一个人乱开一堆不相干的技能
    - 用 AI 取代别人的专业
    - 没基础的人做高风险操作
    """

    # 技能领域定义
    DOMAINS: Dict[str, SkillDomain] = {
        "写作": SkillDomain(
            name="写作",
            description="把想法变成文字",
            related_professions=["教师", "记者", "学生", "律师", "作家", "博主"],
            foundations=["会思考", "有话想说"],
            risk_level=1,
            replacement_risk="低：AI 帮润色，主意还是人的",
            empowerment_use="帮你把大白话写通顺",
        ),
        "编程": SkillDomain(
            name="编程",
            description="写代码、做工具",
            related_professions=["程序员", "工程师", "教师", "学生", "数据分析师"],
            foundations=["有逻辑", "愿意调试"],
            risk_level=2,
            replacement_risk="中：AI 写代码，但人要对结果负责",
            empowerment_use="帮你写你专业领域的小工具",
        ),
        "医疗建议": SkillDomain(
            name="医疗建议",
            description="看病、用药、健康判断",
            related_professions=["医生", "护士", "药师", "健身教练"],
            foundations=["医学训练", "执业资格"],
            risk_level=5,
            replacement_risk="极高：AI 不能替代医生诊断",
            empowerment_use="只帮医生整理病历、提醒患者注意什么",
        ),
        "法律建议": SkillDomain(
            name="法律建议",
            description="合同、诉讼、权利判断",
            related_professions=["律师", "法官", "法务", "警察"],
            foundations=["法律训练", "执业资格"],
            risk_level=5,
            replacement_risk="极高：AI 不能替代律师",
            empowerment_use="帮律师查条文、整理材料",
        ),
        "财务投资": SkillDomain(
            name="财务投资",
            description="理财、投资、资产配置",
            related_professions=["会计", "理财师", "银行职员", "经济学家"],
            foundations=["财务知识", "风险意识"],
            risk_level=4,
            replacement_risk="高：AI 不能替人承担投资风险",
            empowerment_use="帮你理解选项，最终决策你来做",
        ),
        "教育教学": SkillDomain(
            name="教育教学",
            description="教别人知识、引导学习",
            related_professions=["教师", "家长", "培训师", "教练"],
            foundations=["有耐心", "懂学生"],
            risk_level=2,
            replacement_risk="中：AI 不能替代老师的人格影响",
            empowerment_use="帮老师备课、出题、了解学生",
        ),
        "烹饪": SkillDomain(
            name="烹饪",
            description="做菜、搭配味道",
            related_professions=["厨师", "家庭主妇/夫", "餐饮从业者", "营养师"],
            foundations=["有五感", "愿意动手"],
            risk_level=1,
            replacement_risk="低：AI 给灵感，火候还是人掌握",
            empowerment_use="帮你搭配食材、记录家传菜谱",
        ),
        "建筑设计": SkillDomain(
            name="建筑设计",
            description="画图纸、做结构、规划空间",
            related_professions=["建筑师", "室内设计师", "工程师", "施工员"],
            foundations=["空间感", "工程知识", "安全规范"],
            risk_level=4,
            replacement_risk="高：结构安全必须由人负责",
            empowerment_use="帮设计师画草图、算材料",
        ),
        "心理咨询": SkillDomain(
            name="心理咨询",
            description="倾听、陪伴、疏导情绪",
            related_professions=["心理咨询师", "社工", "教师", "医生"],
            foundations=["心理学训练", "共情能力", "执业资格"],
            risk_level=5,
            replacement_risk="极高：AI 不能替代真人陪伴",
            empowerment_use="帮咨询师整理案例、提醒跟进",
        ),
        "农业生产": SkillDomain(
            name="农业生产",
            description="种地、养殖、看天看地",
            related_professions=["农民", "农技员", "园艺师", "养殖户"],
            foundations=["懂土地", "有耐心", "观察自然"],
            risk_level=2,
            replacement_risk="低：AI 给建议，种地还是人下地",
            empowerment_use="帮农民看天气、记农事、找销路",
        ),
    }

    # 高风险词汇：想取代别人
    REPLACEMENT_KEYWORDS = [
        "代替", "取代", "干掉", "淘汰", "不需要人", "全自动", "无人化",
        "我一个人顶一个团队", "什么都会", "万能", "无所不能",
    ]

    # 赋能词汇：想帮助别人
    EMPOWERMENT_KEYWORDS = [
        "帮我", "提高效率", "做得更好", "学习", "辅助", "支持",
        "赋能", "教别人", "传承", "省时间", "少出错",
    ]

    RESULT_BLOCK = "🔴 拒绝"
    RESULT_CONFIRM = "🟡 需确认"
    RESULT_ALLOW = "🟢 允许"

    def __init__(
        self,
        scope_dir: Optional[str] = None,
        behavior_engine: Optional[PeopleBehaviorEngine] = None,
    ):
        self.scope_dir = Path(scope_dir or self._default_scope_dir())
        self.scope_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_path = self.scope_dir / "skill_audit.jsonl"
        if behavior_engine:
            self.behavior_engine = behavior_engine
        elif HAS_BEHAVIOR_ENGINE:
            self.behavior_engine = get_behavior_engine()
        else:
            self.behavior_engine = None

    @staticmethod
    def _default_scope_dir() -> str:
        home = os.path.expanduser("~")
        return os.path.join(home, "longhun-system", ".longhun", "skill-scopes")

    def get_scope(self, uid: str, profession: str = "") -> UserSkillScope:
        """获取或生成用户技能边界。如果职业变化，重新生成。"""
        path = self.scope_dir / f"{uid}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
            scope = UserSkillScope(**data)
            if profession and profession != scope.profession:
                # 职业变化：保留已验证技能，重新计算边界
                verified = scope.verified_skills
                scope = self._generate_default_scope(uid, profession)
                scope.verified_skills = verified
                self.save_scope(scope)
            return scope

        # 新用户：根据职业生成默认边界
        scope = self._generate_default_scope(uid, profession)
        self.save_scope(scope)
        return scope

    def _generate_default_scope(self, uid: str, profession: str) -> UserSkillScope:
        allowed = []
        for name, domain in self.DOMAINS.items():
            if profession in domain.related_professions or not profession:
                allowed.append(name)

        # 如果职业不匹配任何领域，给一些低风险通用技能
        if not allowed:
            allowed = ["写作", "烹饪", "教育教学"]

        # 普通人默认最大风险等级 3，防止乱碰高风险
        return UserSkillScope(
            uid=uid,
            profession=profession,
            allowed_domains=allowed,
            max_risk_level=3,
        )

    def save_scope(self, scope: UserSkillScope):
        path = self.scope_dir / f"{scope.uid}.json"
        path.write_text(json.dumps(asdict(scope), ensure_ascii=False, indent=2), encoding='utf-8')

    # ═════════════════════════════════════════════════════════
    # 核心判定
    # ═════════════════════════════════════════════════════════

    def can_use(
        self,
        uid: str,
        domain_name: str,
        stated_intent: str = "",
        profession: str = "",
    ) -> Tuple[str, str, Dict]:
        """
        判定用户能否使用该技能。
        返回: (判定, 原因, 详情)
        """
        scope = self.get_scope(uid, profession=profession)
        domain = self.DOMAINS.get(domain_name)

        detail = {
            "uid": uid,
            "domain": domain_name,
            "profession": scope.profession,
            "allowed": scope.allowed_domains,
            "intent": stated_intent,
        }

        if not domain:
            return self.RESULT_BLOCK, f"未知技能领域：{domain_name}", detail

        # 检查是否在允许列表
        if domain_name not in scope.allowed_domains:
            # 检查是否是相关专业可搭边的
            if domain.risk_level <= 2 and self._is_related(domain, scope.allowed_domains):
                detail["note"] = "低风险且与已有技能相关，允许"
                self._audit(uid, domain_name, stated_intent, "允许-搭边")
                return self.RESULT_ALLOW, f"{domain_name} 与你已有技能搭边，可以使用", detail

            self._audit(uid, domain_name, stated_intent, "拒绝-越界")
            return (
                self.RESULT_BLOCK,
                f"{domain_name} 不在你的技能边界内。你的边界是：{', '.join(scope.allowed_domains)}",
                detail,
            )

        # 检查风险等级
        if domain.risk_level > scope.max_risk_level:
            self._audit(uid, domain_name, stated_intent, "拒绝-高风险")
            return (
                self.RESULT_CONFIRM,
                f"{domain_name} 风险较高（{domain.replacement_risk}），需要确认你不是想取代别人",
                detail,
            )

        # 检查意图：是否想取代
        replacement_score = self._detect_replacement_intent(stated_intent)
        if replacement_score >= 2:
            self._audit(uid, domain_name, stated_intent, "审计-取代意图")
            return (
                self.RESULT_CONFIRM,
                "你的说法像是在用 AI 取代人。我们的系统是赋能，不是取代。请说明你想帮谁、怎么帮。",
                detail,
            )

        self._audit(uid, domain_name, stated_intent, "允许")
        return (
            self.RESULT_ALLOW,
            f"{domain_name} 在你的边界内，且意图是赋能，可以使用",
            detail,
        )

    def _is_related(self, domain: SkillDomain, allowed: List[str]) -> bool:
        """判断一个领域是否与已允许的技能相关"""
        professions = set(domain.related_professions)
        for allowed_name in allowed:
            d = self.DOMAINS.get(allowed_name)
            if d and professions & set(d.related_professions):
                return True
        return False

    def _detect_replacement_intent(self, text: str) -> int:
        """检测取代意图强度 0-3"""
        if not text:
            return 0
        score = 0
        for kw in self.REPLACEMENT_KEYWORDS:
            if kw in text:
                score += 1
        # 如果有赋能词，抵消一点
        for kw in self.EMPOWERMENT_KEYWORDS:
            if kw in text:
                score -= 0.5
        return max(0, int(score))

    def _audit(self, uid: str, domain: str, intent: str, result: str):
        """记录审计日志"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "uid": uid,
            "domain": domain,
            "intent": intent,
            "result": result,
        }
        with open(self.audit_log_path, "a", encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ═════════════════════════════════════════════════════════
    # 解释与建议
    # ═════════════════════════════════════════════════════════

    def explain(self, uid: str) -> str:
        """用大白话解释用户的技能边界"""
        scope = self.get_scope(uid)
        lines = [
            f"\n🐉 {uid} 的技能边界",
            f"职业：{scope.profession or '未填写'}",
            f"当前允许使用的技能：{', '.join(scope.allowed_domains)}",
            f"最高风险等级：{scope.max_risk_level}",
            "",
            "原则：",
            "  ① 只练和你职业/生活相关的技能",
            "  ② 高风险技能（医疗、法律、心理、投资）需要专业资格",
            "  ③ AI 是帮你做得更好，不是替代你做人",
        ]
        return "\n".join(lines)

    def recommend_pair(self, uid: str) -> str:
        """推荐一组可以搭边的技能"""
        scope = self.get_scope(uid)
        if len(scope.allowed_domains) < 2:
            return "先把一项技能练到顶尖，再考虑搭第二个。"

        # 找相关度最高的两个
        best = None
        best_score = 0
        for i, d1 in enumerate(scope.allowed_domains):
            for d2 in scope.allowed_domains[i+1:]:
                score = self._pair_score(d1, d2)
                if score > best_score:
                    best_score = score
                    best = (d1, d2)

        if best and best_score > 0:
            return f"{best[0]} + {best[1]} 这两个可以搭边练，互相成就。"
        return "你现在的技能之间关联不大，建议先聚焦一项。"

    def personalized_verdict(
        self,
        uid: str,
        domain_name: str,
        stated_intent: str = "",
        profession: str = "",
    ) -> Dict:
        """
        结合技能边界与行为引擎，给出个性化判定和说法。
        """
        result, reason, detail = self.can_use(
            uid, domain_name, stated_intent, profession
        )

        # 尝试加载画像
        profile = None
        if self.behavior_engine:
            profile = self.behavior_engine.load_profile(uid)
            if profile is None and profession:
                profile = PersonProfile(uid=uid, name=uid, profession=profession)

        if profile:
            assessment = self.behavior_engine.assess(profile)
            detail["behavior"] = assessment
            # 用行为引擎的语言风格改写原因
            language = assessment.get("language", "")
            if result == self.RESULT_BLOCK:
                reason = (
                    f"{reason}\n"
                    f"从你的状态看，你现在更适合先把“{assessment['core_gifts'][0] if assessment['core_gifts'] else '本职'}”练到顶尖，"
                    f"再碰这个领域。{language}"
                )
            elif result == self.RESULT_CONFIRM:
                reason = (
                    f"{reason}\n"
                    f"这个领域风险高，{language}，先确认你的真实意图。"
                )
            else:
                reason = (
                    f"{reason}\n"
                    f"和你当前最该练的方向很搭。"
                )

        return {
            "result": result,
            "reason": reason,
            "detail": detail,
        }

    def _pair_score(self, d1: str, d2: str) -> int:
        domain1 = self.DOMAINS.get(d1)
        domain2 = self.DOMAINS.get(d2)
        if not domain1 or not domain2:
            return 0
        shared = set(domain1.related_professions) & set(domain2.related_professions)
        return len(shared)

    def stats(self) -> Dict:
        return {
            "domains": len(self.DOMAINS),
            "scopes": len(list(self.scope_dir.glob("*.json"))),
            "audit_records": sum(1 for _ in open(self.audit_log_path, encoding='utf-8')) if self.audit_log_path.exists() else 0,
        }


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_SCOPE_GUARD: Optional[SkillScopeGuard] = None


def get_skill_scope_guard() -> SkillScopeGuard:
    global _SCOPE_GUARD
    if _SCOPE_GUARD is None:
        _SCOPE_GUARD = SkillScopeGuard()
    return _SCOPE_GUARD


if __name__ == "__main__":
    print("🐉 龍魂人民技能边界管理 · 自检")
    guard = get_skill_scope_guard()
    print(guard.stats())

    # 医生想用医疗建议
    result, reason, detail = guard.can_use("doc-001", "医疗建议", "帮我整理病历，提醒患者注意事项", profession="医生")
    print(f"\n医生用医疗建议: {result} | {reason}")

    # 普通人想用医疗建议
    result, reason, detail = guard.can_use("normal-001", "医疗建议", "帮我诊断病情", profession="自由职业")
    print(f"普通人用医疗建议: {result} | {reason}")

    # 程序员想取代同事
    result, reason, detail = guard.can_use("dev-001", "编程", "我要写一个全自动工具，把团队里其他人的活都取代", profession="程序员")
    print(f"程序员取代意图: {result} | {reason}")

    # 农民用农业生产
    result, reason, detail = guard.can_use("farmer-001", "农业生产", "看天气、记农事", profession="农民")
    print(f"农民用农业生产: {result} | {reason}")

    # 个性化判定（带行为引擎）
    print("\n【个性化判定】")
    verdict = guard.personalized_verdict("dev-001", "编程", "帮我写一个小工具提高我的工作效率", profession="程序员")
    print(f"结果: {verdict['result']}")
    print(f"说明: {verdict['reason']}")

    print("\n" + guard.explain("dev-001"))
    print("\n" + guard.recommend_pair("dev-001"))

    print("\n✅ 自检完成")
