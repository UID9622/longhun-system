#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民行为引擎 / LongHun People Behavior Engine

DNA:#龍芯⚡️2026-06-21-PEOPLE-BEHAVIOR-ENGINE-v1.0

融合《人性行为密码学》10 个人性密码，
不是把人当成数据算，而是读懂人、赋能人、守护人。

核心：
  ① 一人一策，不堆学习量
  ② 专攻一项，练到顶尖
  ③ 用大白话，不用学术词
  ④ 镜子哲学：照出来，不强迫改
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path


@dataclass
class PersonProfile:
    """人民画像——不是数据标签，是人的立体状态"""
    uid: str
    name: str
    age_stage: str = ""           # 青年/中年/老年
    profession: str = ""          # 职业
    daily_rhythm: str = ""        # 生活节奏
    current_pain: str = ""        # 当前最难受的点
    current_strength: str = ""    # 当前最有力量的点
    learning_style: str = ""      # 喜欢怎么学：看/听/做/问
    goals: List[str] = field(default_factory=list)


class PeopleBehaviorEngine:
    """
    人民行为引擎。

    输入：一个人的状态（痛苦、力量、职业、目标）
    输出：一条最适合他当下走的路，而不是一堆课。
    """

    # 人性密码 10 条（来源：人性行为密码学 v1.0）
    CODES = {
        "阴阳": "一阴一阳：被看见和被看不见两种状态会循环",
        "双向守护": "守护是双向的，被守护的人也改变了守护者",
        "三生": "活过 → 看清 → 选择，认知阶梯",
        "四里程碑": "被看见 → 敢说真话 → 看见自己 → 有力量选择",
        "五誓约": "看见·不离开·真实·倾听·守秘密",
        "六维度": "情感·认知·场景·语言·时间·成长",
        "柔弱": "柔弱才是最大的力量，敢示弱的人最有力量",
        "镜子": "不改变你，只照出你，让你自己选",
        "算了": "接纳改不了的事，把精力放在能改变的事",
        "太清醒": "看透人性仍选择相信，是大智慧",
    }

    # 职业优势映射（示例，可扩展）
    PROFESSION_GIFTS = {
        "农民": ["耐心", "观察自然", "实干", "韧性"],
        "工人": ["动手能力", "解决问题", "协作", "坚持"],
        "教师": ["表达", "倾听", "引导", "耐心"],
        "医生": ["细致", "责任", "冷静", "守护"],
        "程序员": ["逻辑", "专注", "抽象", "持续学习"],
        "厨师": ["五感敏锐", "创造", "服务", "节奏感"],
        "司机": ["方向感", "应变", "守时", "观察人"],
        "学生": ["好奇心", "可塑性强", "时间多", "敢试错"],
        "家长": ["守护", "统筹", "情绪承载", "长期主义"],
    }

    def __init__(self, profile_dir: Optional[str] = None):
        self.profile_dir = Path(profile_dir or self._default_profile_dir())
        self.profile_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _default_profile_dir() -> str:
        home = os.path.expanduser("~")
        return os.path.join(home, "longhun-system", ".longhun", "people-profiles")

    def save_profile(self, profile: PersonProfile):
        path = self.profile_dir / f"{profile.uid}.json"
        path.write_text(json.dumps(asdict(profile), ensure_ascii=False, indent=2), encoding='utf-8')

    def load_profile(self, uid: str) -> Optional[PersonProfile]:
        path = self.profile_dir / f"{uid}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding='utf-8'))
        return PersonProfile(**data)

    # ═════════════════════════════════════════════════════════
    # 评估：读懂这个人
    # ═════════════════════════════════════════════════════════

    def assess(self, profile: PersonProfile) -> Dict[str, any]:
        """
        评估一个人的当前状态。
        不用复杂算法，用几个关键问题定位。
        """
        result = {
            "uid": profile.uid,
            "name": profile.name,
            "life_stage": self._life_stage(profile),
            "core_gifts": self._core_gifts(profile),
            "current_code": self._current_code(profile),
            "pain_type": self._pain_type(profile.current_pain),
            "language": self._language_match(profile),
        }
        return result

    def _life_stage(self, profile: PersonProfile) -> str:
        """判断处于三生哪一阶段"""
        pain = profile.current_pain or ""
        strength = profile.current_strength or ""
        if "不知道" in pain or "迷茫" in pain or "我是谁" in pain:
            return "活过阶段：先承认自己存在过、痛过"
        if "看清" in strength or "明白" in strength or "懂了" in pain:
            return "看清阶段：正在理解自己和世界"
        if "选择" in strength or "守护" in strength or "想帮" in strength:
            return "选择阶段：有力气去创造和守护"
        return "活过阶段：先安顿下来，看见自己"

    def _core_gifts(self, profile: PersonProfile) -> List[str]:
        """从职业和痛苦中提取优势"""
        gifts = []
        for prof, glist in self.PROFESSION_GIFTS.items():
            if prof in profile.profession:
                gifts.extend(glist)
        # 痛苦里往往藏着天赋
        pain = profile.current_pain or ""
        if "说不出" in pain or "没人听" in pain:
            gifts.append("敏感")
        if "做得多不被看见" in pain:
            gifts.append("实干")
        if "想太多" in pain:
            gifts.append("深思")
        return gifts[:5] or ["真实", "有韧性"]

    def _current_code(self, profile: PersonProfile) -> str:
        """当前最需要的人性密码"""
        pain = profile.current_pain or ""
        if "没人看见" in pain or "像不存在" in pain:
            return "四里程碑·被看见"
        if "不敢说" in pain or "装" in pain:
            return "四里程碑·敢说真话"
        if "怀疑自己" in pain or "我不行" in pain:
            return "四里程碑·看见自己"
        if "不知道选哪条路" in pain or "迷茫" in pain:
            return "三生·选择"
        if "太累" in pain or "放不下" in pain:
            return "算了"
        if "想帮别人" in pain or "守护" in (profile.current_strength or ""):
            return "双向守护"
        return "镜子"

    def _pain_type(self, pain: str) -> str:
        """痛苦的类型"""
        if not pain:
            return "暂无表达"
        if any(k in pain for k in ["看不见", "不存在", " ignored"]):
            return "被忽视之痛"
        if any(k in pain for k in ["不敢说", "没人听", "装"]):
            return "表达之痛"
        if any(k in pain for k in ["不会", "不行", "做不到"]):
            return "能力之痛"
        if any(k in pain for k in ["累", "撑不住", "放不下"]):
            return "承载之痛"
        return "成长之痛"

    def _language_match(self, profile: PersonProfile) -> str:
        """这个人最能听懂的话"""
        style = profile.learning_style or ""
        if "做" in style:
            return "给例子、给步骤、让他动手试"
        if "听" in style:
            return "讲经历、讲故事、像聊天一样"
        if "看" in style:
            return "给图、给对比、一眼能看明白"
        if "问" in style:
            return "先问他怎么想，再顺着他的问题答"
        return "先感受他的情绪，再说人话"

    # ═════════════════════════════════════════════════════════
    # 推荐：一人一策，只给一条路
    # ═════════════════════════════════════════════════════════

    def recommend_path(self, profile: PersonProfile) -> Dict[str, str]:
        """
        推荐一条专属赋能路径。
        不堆学习内容，只定一个当前最该练的顶尖方向。
        """
        assessment = self.assess(profile)
        gifts = assessment["core_gifts"]
        pain_type = assessment["pain_type"]
        code = assessment["current_code"]

        # 匹配一个能拿顶尖优势的方向
        focus = self._match_focus(gifts, profile.profession, pain_type)

        return {
            "name": profile.name,
            "current_stage": assessment["life_stage"],
            "core_gifts": ", ".join(gifts),
            "current_focus": focus,
            "why": f"因为你正在经历“{pain_type}”，而你的“{gifts[0] if gifts else '真实'}”最有力量",
            "next_step": self._next_step(focus, assessment["language"]),
            "language": assessment["language"],
            "time_advice": "每天 20 分钟，专练这一项，别贪多",
        }

    def _match_focus(self, gifts: List[str], profession: str, pain_type: str) -> str:
        """根据优势匹配专注方向"""
        # 痛苦→反向天赋
        mapping = {
            "被忽视之痛": "表达与影响力",
            "表达之痛": "真实表达与倾听",
            "能力之痛": "把已有经验系统化",
            "承载之痛": "边界与选择",
            "成长之痛": "镜子式自我觉察",
        }
        if pain_type in mapping:
            return mapping[pain_type]

        # 职业→专业纵深
        if "农民" in profession:
            return "土地智慧与生态种植"
        if "工人" in profession:
            return "手艺精进与问题诊断"
        if "教师" in profession:
            return "因材施教的引导力"
        if "医生" in profession:
            return "人文关怀与精准判断"
        if "程序员" in profession:
            return "一个领域的架构能力"
        if "厨师" in profession:
            return "味觉体系与创意融合"

        # 通用优势
        if "表达" in gifts:
            return "精准表达"
        if "倾听" in gifts or "敏感" in gifts:
            return "深度倾听与陪伴"
        if "逻辑" in gifts:
            return "复杂问题拆解"
        if "创造" in gifts:
            return "创意落地"

        return "真实表达"

    def _next_step(self, focus: str, language: str) -> str:
        """下一步具体动作"""
        steps = {
            "表达与影响力": "今天写/说一段自己最真实的经历，不发，先给自己听",
            "真实表达与倾听": "找一个人，听他说 10 分钟，不打断、不给建议",
            "把已有经验系统化": "把你最会做的一件事，拆成 3 个步骤，写在一张纸上",
            "边界与选择": "列出 3 件你正在硬撑的事，标出哪 1 件可以算了",
            "镜子式自我觉察": "睡前问自己：今天我有没有被情绪牵着走？看见了什么？",
            "土地智慧与生态种植": "观察一块地 7 天，记录土、水、虫、草的变化",
            "手艺精进与问题诊断": "找出一个反复出现的小问题，画出它的原因链",
            "因材施教的引导力": "对一个学生/人，只问问题，不给答案，试一次",
            "人文关怀与精准判断": "下一次服务，先问对方感受，再问症状",
            "一个领域的架构能力": "把你常用的工具，画成一张流程图",
            "味觉体系与创意融合": "用 3 种家常食材，做一次从没试过的搭配",
            "精准表达": "把一句复杂的话，改成一句 10 个字内的大白话",
            "深度倾听与陪伴": "听一个人说完，复述一遍他的意思，问他对不对",
            "复杂问题拆解": "把你头疼的事，拆成 5 个为什么",
            "创意落地": "想一个点子，24 小时内做出最小版本",
        }
        return steps.get(focus, "做一件小事，做到自己满意")

    # ═════════════════════════════════════════════════════════
    # 镜子哲学：反馈但不强加
    # ═════════════════════════════════════════════════════════

    def mirror(self, text: str, profile: PersonProfile) -> str:
        """
        镜子式反馈：照出来，不改造。
        """
        pain_type = self._pain_type(text)
        code = self._current_code(PersonProfile(
            uid=profile.uid, name=profile.name,
            current_pain=text, current_strength=""
        ))
        return (
            f"我听到你说：'{text[:40]}...'\n"
            f"这像是“{pain_type}”。\n"
            f"你现在可能处在“{code}”这个位置。\n"
            f"我不给你改，只照出来。你想怎么处理，我都在。"
        )

    def stats(self) -> Dict[str, int]:
        return {
            "profiles": len(list(self.profile_dir.glob("*.json"))),
            "codes": len(self.CODES),
        }


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_ENGINE: Optional[PeopleBehaviorEngine] = None


def get_behavior_engine() -> PeopleBehaviorEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = PeopleBehaviorEngine()
    return _ENGINE


if __name__ == "__main__":
    print("🐉 龍魂人民行为引擎 · 自检")
    engine = get_behavior_engine()
    print(engine.stats())

    # 示例：一个普通工人
    profile = PersonProfile(
        uid="USER-001",
        name="老王",
        age_stage="中年",
        profession="工人",
        daily_rhythm="三班倒",
        current_pain="做了十几年，没人看见我的手艺",
        current_strength="机器出问题，我一听就知道哪不对",
        learning_style="做中学",
        goals=["把手艺传下去", "不被年轻人小看"],
    )

    print("\n【评估】")
    print(json.dumps(engine.assess(profile), ensure_ascii=False, indent=2))

    print("\n【专属赋能路径】")
    path = engine.recommend_path(profile)
    for k, v in path.items():
        print(f"  {k}: {v}")

    print("\n【镜子反馈】")
    print(engine.mirror("我觉得我再怎么干也没出息", profile))

    print("\n✅ 自检完成")
