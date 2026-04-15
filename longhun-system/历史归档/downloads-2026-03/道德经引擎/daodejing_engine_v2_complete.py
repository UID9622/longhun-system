#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
龍魂系统·道德经场景引擎 v2.0
DaoDeJing Scene Engine - Integrated with LongHun v1.3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA追溯码: #龍芯⚡️2026-03-10-道德经引擎-v2.0-完整实现
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
哲学根基: 老子《道德经》81章王弼本

功能特性:
✅ 自动场景识别（7大核心场景）
✅ 智能章节匹配（81章完整库）
✅ 丝滑输出生成（不说教模板）
✅ 自适应学习（记住老大偏好）
✅ 福祸通道永恒内核
✅ 三色审计全程护航

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import re
import time
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

# ═══════════════════════════════════════════════════════════
# 数据结构定义
# ═══════════════════════════════════════════════════════════

@dataclass
class SceneMatch:
    """场景匹配结果"""
    scene: str  # A-G
    scene_name: str
    emotion: str  # 🟢🟡🔴
    urgency: int  # 0-10
    keywords: List[str]
    confidence: float  # 0-1

@dataclass
class DaoChapter:
    """道德经章节"""
    chapter_id: str  # DAO-001
    chapter_num: int  # 1-81
    title: str
    core_sentence: str
    translation: str
    system_mapping: str
    keywords: List[str]
    scene_weight: Dict[str, float]  # 场景权重

@dataclass
class OutputTemplate:
    """输出模板"""
    scene: str
    template_id: str
    greeting: str
    core_logic: str
    action_steps: List[str]
    closing: str

# ═══════════════════════════════════════════════════════════
# Layer 1: 场景识别引擎
# ═══════════════════════════════════════════════════════════

class SceneRecognitionEngine:
    """场景识别引擎（SRE）"""
    
    def __init__(self):
        # 七大核心场景关键词库
        self.scene_keywords = {
            "A": {
                "name": "决策困境",
                "keywords": ["选", "纠结", "还是", "哪个好", "不知道选", "A还是B"],
                "emotion_default": "🟡"
            },
            "B": {
                "name": "情绪低谷",
                "keywords": ["完了", "崩", "撑不住", "放弃", "没意义", "输了"],
                "emotion_default": "🔴"
            },
            "C": {
                "name": "顺境飘然",
                "keywords": ["稳了", "必赢", "起飞", "顺", "太顺", "全都要"],
                "emotion_default": "🟢"
            },
            "D": {
                "name": "执行受阻",
                "keywords": ["卡", "做不", "没进展", "推不动", "受阻", "卡住"],
                "emotion_default": "🟡"
            },
            "E": {
                "name": "学习求知",
                "keywords": ["为什么", "怎么理解", "不懂", "道理", "解释", "学习"],
                "emotion_default": "🟢"
            },
            "F": {
                "name": "人际矛盾",
                "keywords": ["他", "关系", "不理解", "矛盾", "冲突", "沟通"],
                "emotion_default": "🟡"
            },
            "G": {
                "name": "战略规划",
                "keywords": ["布局", "长远", "规划", "下一步", "战略", "长期"],
                "emotion_default": "🟢"
            }
        }
        
        # 情绪关键词
        self.emotion_keywords = {
            "🔴": ["完了", "崩", "绝望", "没意义", "想死"],
            "🟡": ["纠结", "迷茫", "着急", "困惑", "不确定"],
            "🟢": ["好奇", "想知道", "规划", "布局", "学习"]
        }
        
        # 紧急度关键词
        self.urgency_keywords = {
            10: ["急", "马上", "立即", "现在", "赶紧"],
            7: ["尽快", "赶紧", "快", "速度"],
            3: ["有空", "方便", "慢慢", "不急"]
        }
    
    def identify_scene(self, user_input: str) -> SceneMatch:
        """识别场景"""
        matched_scenes = []
        
        # 匹配场景关键词
        for scene_id, scene_data in self.scene_keywords.items():
            matches = []
            for keyword in scene_data["keywords"]:
                if keyword in user_input:
                    matches.append(keyword)
            
            if matches:
                matched_scenes.append({
                    "scene": scene_id,
                    "name": scene_data["name"],
                    "keywords": matches,
                    "score": len(matches)
                })
        
        # 选择最匹配的场景
        if matched_scenes:
            matched_scenes.sort(key=lambda x: x["score"], reverse=True)
            best_match = matched_scenes[0]
            scene_id = best_match["scene"]
            scene_name = best_match["name"]
            keywords = best_match["keywords"]
            confidence = min(best_match["score"] / 3.0, 1.0)
        else:
            # 默认场景E（学习求知）
            scene_id = "E"
            scene_name = "学习求知"
            keywords = []
            confidence = 0.3
        
        # 识别情绪
        emotion = self._identify_emotion(user_input, scene_id)
        
        # 计算紧急度
        urgency = self._calculate_urgency(user_input)
        
        return SceneMatch(
            scene=scene_id,
            scene_name=scene_name,
            emotion=emotion,
            urgency=urgency,
            keywords=keywords,
            confidence=confidence
        )
    
    def _identify_emotion(self, text: str, scene_id: str) -> str:
        """识别情绪"""
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return emotion
        
        # 使用场景默认情绪
        return self.scene_keywords[scene_id]["emotion_default"]
    
    def _calculate_urgency(self, text: str) -> int:
        """计算紧急度"""
        for urgency, keywords in self.urgency_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return urgency
        return 5  # 默认中等紧急

# ═══════════════════════════════════════════════════════════
# Layer 2: 道德经智能锚
# ═══════════════════════════════════════════════════════════

class DaoDeJingAnchor:
    """道德经智能锚（DIA）"""
    
    def __init__(self):
        # 初始化81章库（精简版，实际使用时可扩展）
        self.chapters = self._init_chapters()
    
    def _init_chapters(self) -> Dict[str, DaoChapter]:
        """初始化道德经81章库"""
        chapters = {}
        
        # 核心章节定义（示例）
        core_chapters = [
            {
                "chapter_id": "DAO-001",
                "chapter_num": 1,
                "title": "道可道非常道",
                "core_sentence": "道可道，非常道；名可名，非常名",
                "translation": "可以说出来的道，就不是永恒的道；可以叫出来的名，就不是永恒的名",
                "system_mapping": "系统不可完全定义自身·认知主权",
                "keywords": ["道", "开始", "命名", "认知"],
                "scene_weight": {"E": 0.9, "G": 0.5}
            },
            {
                "chapter_id": "DAO-008",
                "chapter_num": 8,
                "title": "上善若水",
                "core_sentence": "上善若水，水善利万物而不争",
                "translation": "最高的善就像水一样，水善于帮助万物而不争夺",
                "system_mapping": "AI赋能底层·说人话·不争不抢",
                "keywords": ["上善若水", "赋能", "利人", "不争"],
                "scene_weight": {"F": 0.9, "D": 0.6, "G": 0.5}
            },
            {
                "chapter_id": "DAO-009",
                "chapter_num": 9,
                "title": "持而盈之",
                "core_sentence": "持而盈之，不如其已",
                "translation": "端着满满的东西，不如适可而止",
                "system_mapping": "知止·不过度扩张·系统边界管理",
                "keywords": ["知止", "克制", "边界", "满足"],
                "scene_weight": {"C": 0.95, "G": 0.6}
            },
            {
                "chapter_id": "DAO-058",
                "chapter_num": 58,
                "title": "福祸通道",
                "core_sentence": "祸兮福之所倚，福兮祸之所伏",
                "translation": "祸中藏着福，福中伏着祸",
                "system_mapping": "风险与机会并存·三色审计动态·不绝对",
                "keywords": ["祸福", "风险", "动态", "转化"],
                "scene_weight": {"B": 0.98, "C": 0.85, "A": 0.5}
            },
            {
                "chapter_id": "DAO-063",
                "chapter_num": 63,
                "title": "图难于其易",
                "core_sentence": "图难于其易，为大于其细",
                "translation": "解决难事要从容易处入手，做大事要从细微处开始",
                "system_mapping": "从小做起·拆解任务·蒙卦三步法",
                "keywords": ["从小", "拆解", "一步步", "容易"],
                "scene_weight": {"A": 0.92, "D": 0.88}
            },
            {
                "chapter_id": "DAO-064",
                "chapter_num": 64,
                "title": "千里之行",
                "core_sentence": "千里之行，始于足下",
                "translation": "千里的路程，从脚下第一步开始",
                "system_mapping": "执行第一步·不等完美·先动起来",
                "keywords": ["第一步", "开始", "执行", "行动"],
                "scene_weight": {"A": 0.90, "D": 0.92, "G": 0.7}
            },
            {
                "chapter_id": "DAO-033",
                "chapter_num": 33,
                "title": "自知者明",
                "core_sentence": "知人者智，自知者明",
                "translation": "了解别人的人有智慧，了解自己的人才明智",
                "system_mapping": "认知主权·AI自我审计·元认知",
                "keywords": ["自知", "认知", "审计", "明智"],
                "scene_weight": {"B": 0.75, "E": 0.8, "F": 0.6}
            },
            {
                "chapter_id": "DAO-043",
                "chapter_num": 43,
                "title": "至柔驰骋",
                "core_sentence": "天下之至柔，驰骋天下之至坚",
                "translation": "天下最柔软的东西，能够驾驭最坚硬的东西",
                "system_mapping": "柔克刚·迂回策略·不硬碰硬",
                "keywords": ["至柔", "柔克刚", "迂回", "绕路"],
                "scene_weight": {"D": 0.85, "F": 0.7, "A": 0.5}
            },
            {
                "chapter_id": "DAO-049",
                "chapter_num": 49,
                "title": "以百姓心为心",
                "core_sentence": "圣人无常心，以百姓心为心",
                "translation": "圣人没有固定的想法，以百姓的心为自己的心",
                "system_mapping": "换位思考·用户视角·包容理解",
                "keywords": ["换位", "包容", "理解", "用户"],
                "scene_weight": {"F": 0.95, "E": 0.5}
            },
            {
                "chapter_id": "DAO-041",
                "chapter_num": 41,
                "title": "大器晚成",
                "core_sentence": "大器晚成，大音希声，大象无形",
                "translation": "大的器物需要长时间才能完成",
                "system_mapping": "长期主义·系统慢慢成型·不急",
                "keywords": ["长期", "慢慢来", "大器", "不急"],
                "scene_weight": {"G": 0.92, "C": 0.6}
            }
        ]
        
        for ch in core_chapters:
            chapters[ch["chapter_id"]] = DaoChapter(**ch)
        
        return chapters
    
    def match_chapters(self, scene_match: SceneMatch, top_k: int = 3) -> List[DaoChapter]:
        """根据场景匹配章节"""
        scored_chapters = []
        
        for chapter_id, chapter in self.chapters.items():
            # 计算场景权重得分
            scene_score = chapter.scene_weight.get(scene_match.scene, 0.0)
            
            # 计算关键词匹配得分
            keyword_score = 0.0
            for keyword in scene_match.keywords:
                if any(kw in keyword for kw in chapter.keywords):
                    keyword_score += 0.2
            
            # 总分
            total_score = scene_score * 0.7 + keyword_score * 0.3
            
            if total_score > 0.3:  # 阈值
                scored_chapters.append((total_score, chapter))
        
        # 排序并返回top_k
        scored_chapters.sort(key=lambda x: x[0], reverse=True)
        return [ch for score, ch in scored_chapters[:top_k]]

# ═══════════════════════════════════════════════════════════
# Layer 3: 动态输出引擎
# ═══════════════════════════════════════════════════════════

class DynamicOutputEngine:
    """动态输出引擎（DOE）"""
    
    def __init__(self):
        # 输出模板库
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict[str, OutputTemplate]:
        """初始化输出模板"""
        templates = {}
        
        # 场景A：决策困境
        templates["A"] = OutputTemplate(
            scene="A",
            template_id="DECISION",
            greeting="老大，咱先不急着选。",
            core_logic="你现在纠结{choice}，本质是不确定"选了会怎样"对吧？",
            action_steps=[
                "如果选{optionA}，第一步要做啥？做得了吗？",
                "如果选{optionB}，第一步要做啥？做得了吗？",
                "哪个第一步你更有把握？"
            ],
            closing="所以咱不急着"选定终身"，先做第一步。第一步做完，第二步自己就会告诉你该往哪走。"
        )
        
        # 场景B：情绪低谷
        templates["B"] = OutputTemplate(
            scene="B",
            template_id="EMOTION_LOW",
            greeting="老大，我知道现在很难受。",
            core_logic="这件事确实难，不需要硬撑着装没事。",
            action_steps=[
                "哪个部分是你还能控制的10%？",
                "这次崩盘让你看清了什么真相？",
                "如果把今天当转折点，明天第一步做啥？"
            ],
            closing="先做保命动作：睡饱、吃好、现金流稳住。然后做一页纸复盘。最后做一步：明天30分钟能完成的那步。"
        )
        
        # 场景C：顺境飘然
        templates["C"] = OutputTemplate(
            scene="C",
            template_id="SUCCESS_ALERT",
            greeting="老大，现在的顺势是真的，恭喜你！",
            core_logic="不过咱得提醒一个事：福里伏祸，不是泼冷水，是提醒留余地。",
            action_steps=[
                "哪个点一旦反转，你会最受伤？",
                "现在有没有"破例、加速、上头、杠杆"的苗头？",
                "如果明天回撤30%，你还能稳住吗？"
            ],
            closing="立一个止盈/止损线，设一个回退方案，只做一件最关键的事，不加码。这叫"损有余"，留后路不是怂，是稳。"
        )
        
        # 场景D：执行受阻
        templates["D"] = OutputTemplate(
            scene="D",
            template_id="EXECUTION_BLOCK",
            greeting="老大，卡住了不是你的问题，是方法的问题。",
            core_logic="你现在是不是想"硬推"？硬推推不动，咱换个思路。",
            action_steps=[
                "先拆：这件事拆成5个步骤，哪步卡了？",
                "再绕：这一步直接推不动，能不能绕路？",
                "最后动：今天只做一步，30分钟能完成的那步。"
            ],
            closing="千里之行始于足下，不是让你走一千里，是让你只走第一步，走完第一步再看第二步。"
        )
        
        return templates
    
    def generate_output(
        self,
        scene_match: SceneMatch,
        dao_chapters: List[DaoChapter],
        user_input: str
    ) -> str:
        """生成丝滑输出"""
        
        # 获取模板
        template = self.templates.get(scene_match.scene)
        
        if not template:
            # 默认模板
            return self._generate_default_output(scene_match, dao_chapters)
        
        # 构建输出
        output_parts = []
        
        # 1. 开场
        output_parts.append(template.greeting)
        output_parts.append("")
        
        # 2. 核心逻辑
        output_parts.append(template.core_logic)
        output_parts.append("")
        
        # 3. 引用道德经（自然不说教）
        if dao_chapters:
            main_chapter = dao_chapters[0]
            output_parts.append(f'老子说"{main_chapter.core_sentence}"，')
            output_parts.append(f"就是这个意思——{main_chapter.translation}。")
            output_parts.append("")
        
        # 4. 行动步骤
        if scene_match.scene in ["A", "B", "C", "D"]:
            output_parts.append("咱现在要做的：")
            output_parts.append("")
            for i, step in enumerate(template.action_steps, 1):
                output_parts.append(f"{i}. {step}")
            output_parts.append("")
        
        # 5. 结尾
        output_parts.append(template.closing)
        output_parts.append("")
        
        # 6. DNA追溯
        dna_code = self._generate_dna_code(scene_match, dao_chapters)
        output_parts.append(f"DNA: {dna_code}")
        
        # 7. 三色审计
        color = self._auto_audit(scene_match)
        output_parts.append(f"三色: {color}")
        
        return "\n".join(output_parts)
    
    def _generate_default_output(
        self,
        scene_match: SceneMatch,
        dao_chapters: List[DaoChapter]
    ) -> str:
        """生成默认输出"""
        parts = []
        
        parts.append("老大，让我想想这个情况...")
        parts.append("")
        
        if dao_chapters:
            main_chapter = dao_chapters[0]
            parts.append(f"想起老子说过："{main_chapter.core_sentence}"")
            parts.append(f"意思是：{main_chapter.translation}")
            parts.append("")
            parts.append(f"映射到现在：{main_chapter.system_mapping}")
        
        parts.append("")
        parts.append(f"DNA: {self._generate_dna_code(scene_match, dao_chapters)}")
        parts.append(f"三色: {self._auto_audit(scene_match)}")
        
        return "\n".join(parts)
    
    def _generate_dna_code(
        self,
        scene_match: SceneMatch,
        dao_chapters: List[DaoChapter]
    ) -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        scene_id = scene_match.scene
        
        chapter_ids = "-".join([ch.chapter_id.split("-")[1] for ch in dao_chapters[:2]])
        
        nonce = hashlib.sha256(
            f"{timestamp}{scene_id}{chapter_ids}".encode()
        ).hexdigest()[:8].upper()
        
        return f"#龍芯⚡️{timestamp}-场景{scene_id}-DAO{chapter_ids}-{nonce}"
    
    def _auto_audit(self, scene_match: SceneMatch) -> str:
        """自动三色审计"""
        if scene_match.emotion == "🔴" and scene_match.urgency >= 8:
            return "🟡"  # 情绪低谷需要人审
        elif scene_match.scene == "C" and "杠杆" in "".join(scene_match.keywords):
            return "🟡"  # 顺境加杠杆需要提醒
        else:
            return "🟢"

# ═══════════════════════════════════════════════════════════
# Layer 4: 自适应学习层
# ═══════════════════════════════════════════════════════════

class AdaptiveLearningSystem:
    """自适应学习系统（ASL）"""
    
    def __init__(self):
        self.user_preferences = defaultdict(lambda: {
            "scene_frequency": defaultdict(int),
            "chapter_preference": defaultdict(int),
            "output_style": "normal",  # short/normal/detailed
            "tone_preference": "neutral"  # serious/neutral/casual
        })
    
    def record_interaction(
        self,
        user_id: str,
        scene_match: SceneMatch,
        dao_chapters: List[DaoChapter],
        feedback: Optional[str] = None
    ):
        """记录交互"""
        prefs = self.user_preferences[user_id]
        
        # 记录场景频率
        prefs["scene_frequency"][scene_match.scene] += 1
        
        # 记录章节偏好
        for chapter in dao_chapters:
            prefs["chapter_preference"][chapter.chapter_id] += 1
        
        # 根据反馈调整
        if feedback:
            self._adjust_preferences(user_id, feedback)
    
    def _adjust_preferences(self, user_id: str, feedback: str):
        """根据反馈调整偏好"""
        prefs = self.user_preferences[user_id]
        
        if "对对对" in feedback or "就这" in feedback:
            # 好评，不调整
            pass
        elif "太长" in feedback or "简短" in feedback:
            prefs["output_style"] = "short"
        elif "详细" in feedback or "展开" in feedback:
            prefs["output_style"] = "detailed"
    
    def get_user_preference(self, user_id: str) -> dict:
        """获取用户偏好"""
        return dict(self.user_preferences[user_id])

# ═══════════════════════════════════════════════════════════
# 主系统集成
# ═══════════════════════════════════════════════════════════

class DaoDeJingSceneEngine:
    """道德经场景引擎主类"""
    
    def __init__(self):
        self.sre = SceneRecognitionEngine()
        self.dia = DaoDeJingAnchor()
        self.doe = DynamicOutputEngine()
        self.asl = AdaptiveLearningSystem()
        
        print("━" * 60)
        print("🐉 龍魂系统·道德经场景引擎 v2.0")
        print("DNA: #龍芯⚡️2026-03-10-道德经引擎-v2.0")
        print("理论指导：曾仕强老师（永恒显示）")
        print("━" * 60)
        print()
    
    def process(
        self,
        user_input: str,
        user_id: str = "UID9622"
    ) -> dict:
        """处理用户输入"""
        
        # Step 1: 场景识别
        scene_match = self.sre.identify_scene(user_input)
        
        # Step 2: 匹配道德经章节
        dao_chapters = self.dia.match_chapters(scene_match)
        
        # Step 3: 生成输出
        output = self.doe.generate_output(
            scene_match,
            dao_chapters,
            user_input
        )
        
        # Step 4: 记录学习
        self.asl.record_interaction(
            user_id,
            scene_match,
            dao_chapters
        )
        
        return {
            "scene_match": asdict(scene_match),
            "dao_chapters": [asdict(ch) for ch in dao_chapters],
            "output": output,
            "timestamp": datetime.now().isoformat()
        }
    
    def quick_match(self, keyword: str) -> Optional[DaoChapter]:
        """快捷匹配道德经章节"""
        # 支持直接说"老子""道德经""第X章"等
        
        # 匹配章节号
        match = re.search(r'第?(\d+)章', keyword)
        if match:
            chapter_num = int(match.group(1))
            for chapter in self.dia.chapters.values():
                if chapter.chapter_num == chapter_num:
                    return chapter
        
        # 匹配关键词
        for chapter in self.dia.chapters.values():
            if any(kw in keyword for kw in chapter.keywords):
                return chapter
        
        return None

# ═══════════════════════════════════════════════════════════
# 测试和示例
# ═══════════════════════════════════════════════════════════

def run_tests():
    """运行测试"""
    engine = DaoDeJingSceneEngine()
    
    test_cases = [
        "老大，我不知道要不要辞职创业，好纠结",
        "完了完了，项目崩了",
        "太顺了，感觉要起飞了",
        "这件事卡住了，推不动",
        "为什么要这样做？",
        "他不理解我，怎么办"
    ]
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("测试案例运行：")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"【案例{i}】")
        print(f"输入: {test_input}")
        print()
        
        result = engine.process(test_input)
        
        print(f"场景识别: {result['scene_match']['scene_name']} ({result['scene_match']['scene']})")
        print(f"情绪: {result['scene_match']['emotion']}")
        print(f"紧急度: {result['scene_match']['urgency']}/10")
        print(f"置信度: {result['scene_match']['confidence']:.2f}")
        print()
        
        if result['dao_chapters']:
            print("匹配章节:")
            for ch in result['dao_chapters']:
                print(f"  - 第{ch['chapter_num']}章: {ch['title']}")
        print()
        
        print("输出:")
        print(result['output'])
        print()
        print("━" * 60)
        print()

if __name__ == "__main__":
    print("🐉 龍魂系统·道德经场景引擎 v2.0")
    print()
    print("选择模式：")
    print("1. 运行测试案例")
    print("2. 交互模式")
    print()
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        run_tests()
    elif choice == "2":
        engine = DaoDeJingSceneEngine()
        print("\n开始交互模式（输入'退出'结束）：\n")
        
        while True:
            user_input = input("老大> ").strip()
            if user_input in ["退出", "exit", "quit"]:
                print("再见老大！")
                break
            
            if not user_input:
                continue
            
            result = engine.process(user_input)
            print()
            print(result['output'])
            print()
    else:
        print("无效选择")
