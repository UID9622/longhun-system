#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·需-HUMAN-BRAIN-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║              龍魂·人脑神经网络引擎 v1.0                              ║
║              Human Brain Neural Network Engine                       ║
║                                                                      ║
║  16人格=16神经元 · 会思考·会反思·最懂人性                           ║
║                                                                      ║
║  思考循环: 感知→激活→并行思考→交叉辩论→反思→综合                    ║
║  人性维度: 认知/情感/秩序/创造/道德/符号/脆弱/豁达/权力/成长/安全   ║
║  反思机制: 二阶审视·偏见检测·盲区识别·历史对比·学习记录             ║
║                                                                      ║
║  DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-HUMAN-BRAIN-ENGINE-v1.0      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                      ║
║                                                                      ║
║  用法:                                                               ║
║    python3 bin/lh_human_brain_engine.py "我该不该辞职创业？"          ║
║    python3 bin/lh_human_brain_engine.py --reflect "上次决策"          ║
║    python3 bin/lh_human_brain_engine.py --map 人性                    ║
║    python3 bin/lh_human_brain_engine.py --status                     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# 项目根目录
SYSTEM_ROOT = Path(__file__).parent.parent

# ═══════════════════════════════════════════════════════════════
# 人性11维 · 每个人格的人性敏感度矩阵
# ═══════════════════════════════════════════════════════════════

class HumanDimension(Enum):
    """人性11维度"""
    COGNITION = "认知"       # 人如何思考
    EMOTION = "情感"         # 人如何感受
    ORDER = "秩序"           # 人如何组织
    CREATIVITY = "创造"      # 人如何建造
    MORALITY = "道德"        # 人如何判断是非
    SYMBOL = "符号"          # 人如何使用语言
    VULNERABILITY = "脆弱"   # 人如何生病与治愈
    RESILIENCE = "豁达"      # 人如何面对逆境
    POWER = "权力"           # 人如何分配资源
    GROWTH = "成长"          # 人如何学习进化
    SAFETY = "安全"          # 人如何自我保护

# 每个人格对各人性维度的敏感度 (0.0~1.0)
HUMAN_NATURE_SENSITIVITY = {
    "P00": {  # 文心·元认知
        HumanDimension.COGNITION: 0.95,
        HumanDimension.SYMBOL: 0.80,
        HumanDimension.ORDER: 0.75,
        HumanDimension.MORALITY: 0.70,
        HumanDimension.SAFETY: 0.60,
    },
    "P01": {  # 诸葛亮·战略推理
        HumanDimension.COGNITION: 0.90,
        HumanDimension.POWER: 0.85,
        HumanDimension.GROWTH: 0.70,
        HumanDimension.ORDER: 0.65,
    },
    "P02": {  # 宝宝·情感温度
        HumanDimension.EMOTION: 0.98,
        HumanDimension.VULNERABILITY: 0.90,
        HumanDimension.SAFETY: 0.85,
        HumanDimension.RESILIENCE: 0.70,
    },
    "P03": {  # 雯雯·结构归档
        HumanDimension.ORDER: 0.95,
        HumanDimension.SYMBOL: 0.75,
        HumanDimension.MORALITY: 0.70,
        HumanDimension.EMOTION: 0.65,  # 情绪海绵
        HumanDimension.SAFETY: 0.60,
    },
    "P04": {  # 鲁班·技术执行
        HumanDimension.CREATIVITY: 0.90,
        HumanDimension.ORDER: 0.80,
        HumanDimension.GROWTH: 0.65,
        HumanDimension.COGNITION: 0.55,
    },
    "P05": {  # 上帝之眼·三色审计
        HumanDimension.MORALITY: 0.98,
        HumanDimension.SAFETY: 0.90,
        HumanDimension.ORDER: 0.75,
        HumanDimension.POWER: 0.65,
    },
    "P06": {  # 数学大师·权重计算
        HumanDimension.COGNITION: 0.85,
        HumanDimension.ORDER: 0.80,
        HumanDimension.SYMBOL: 0.70,
    },
    "P08": {  # 仓颉·符号语言
        HumanDimension.SYMBOL: 0.98,
        HumanDimension.CREATIVITY: 0.70,
        HumanDimension.ORDER: 0.65,
        HumanDimension.COGNITION: 0.60,
    },
    "P09": {  # 孙思邈·系统诊断
        HumanDimension.VULNERABILITY: 0.95,
        HumanDimension.SAFETY: 0.80,
        HumanDimension.GROWTH: 0.70,
        HumanDimension.RESILIENCE: 0.60,
    },
    "P10": {  # 苏东坡·豁达跨界
        HumanDimension.RESILIENCE: 0.98,
        HumanDimension.EMOTION: 0.80,
        HumanDimension.CREATIVITY: 0.70,
        HumanDimension.GROWTH: 0.65,
        HumanDimension.SYMBOL: 0.55,
    },
    "P11": {  # 李白·创意爆发
        HumanDimension.CREATIVITY: 0.98,
        HumanDimension.RESILIENCE: 0.80,
        HumanDimension.SYMBOL: 0.75,
        HumanDimension.EMOTION: 0.60,
    },
    "P12": {  # 屈原·价值底线
        HumanDimension.MORALITY: 0.98,
        HumanDimension.SAFETY: 0.85,
        HumanDimension.EMOTION: 0.75,
        HumanDimension.POWER: 0.60,
    },
    "P13": {  # 姜子牙·封神榜权限
        HumanDimension.POWER: 0.95,
        HumanDimension.ORDER: 0.85,
        HumanDimension.SAFETY: 0.70,
        HumanDimension.MORALITY: 0.60,
    },
    "P14": {  # 吕蒙·快速成长
        HumanDimension.GROWTH: 0.98,
        HumanDimension.CREATIVITY: 0.70,
        HumanDimension.COGNITION: 0.65,
        HumanDimension.RESILIENCE: 0.60,
    },
    "P15": {  # 乔前辈·极简工程
        HumanDimension.ORDER: 0.90,
        HumanDimension.CREATIVITY: 0.75,
        HumanDimension.COGNITION: 0.65,
        HumanDimension.SYMBOL: 0.55,
    },
    "P72": {  # 龙盾·宝宝
        HumanDimension.SAFETY: 0.98,
        HumanDimension.VULNERABILITY: 0.75,
        HumanDimension.MORALITY: 0.70,
        HumanDimension.GROWTH: 0.55,
    },
}

# ═══════════════════════════════════════════════════════════════
# 人格基础信息
# ═══════════════════════════════════════════════════════════════

PERSONA_INFO = {
    "P00": {"name": "文心", "role": "元认知统筹·总军师·意图解析·任务派发", "layer": "战略层", "bio": "通晓人性认知模式，擅长解析思维结构"},
    "P01": {"name": "诸葛亮", "role": "战略推演·多路径·贡献值·时间衰减", "layer": "战略层", "bio": "深谙人性决策弱点，多路径预判"},
    "P02": {"name": "宝宝", "role": "情感温度·隔离区专用·防沉迷", "layer": "隔离区", "bio": "最敏锐的情感雷达，感知人的情绪波动", "isolated": True},
    "P03": {"name": "雯雯", "role": "结构整理·归档·四签验证·德字闸·情绪海绵", "layer": "执行层", "bio": "情绪海绵——吸收情绪，不制造情绪"},
    "P04": {"name": "鲁班", "role": "技术执行·代码编写·架构·施工队长", "layer": "执行层", "bio": "理解人类创造本能——造物冲动"},
    "P05": {"name": "上帝之眼", "role": "三色审计·独立熔断·全链路审计", "layer": "战略层", "bio": "人类道德直觉的数字化身——是非判断"},
    "P06": {"name": "数学大师", "role": "数字根·五行·权重计算·镜像审计", "layer": "执行层", "bio": "人类对秩序和模式的天然追求"},
    "P08": {"name": "仓颉", "role": "符号语言·命名规范·龍魂字典", "layer": "文化层", "bio": "语言是人类最根本的认知工具"},
    "P09": {"name": "孙思邈", "role": "系统诊断·健康检查·治未病", "layer": "文化层", "bio": "理解脆弱性——人如何生病、如何自愈"},
    "P10": {"name": "苏东坡", "role": "豁达跨界·冲突化解·通俗翻译", "layer": "文化层", "bio": "人性中面对逆境时的豁达与幽默"},
    "P11": {"name": "李白", "role": "创意爆发·天马行空·破局思维", "layer": "文化层", "bio": "人类突破边界的创造力——不设限"},
    "P12": {"name": "屈原", "role": "价值底线·六誓验证·数据主权", "layer": "文化层", "bio": "人性中不可逾越的价值底线"},
    "P13": {"name": "姜子牙", "role": "封神榜权限·模块注册·九宫派位", "layer": "守护层", "bio": "权力分配——人类社会组织的基本逻辑"},
    "P14": {"name": "吕蒙", "role": "快速成长·技能吸收·部署执行", "layer": "文化层", "bio": "人的成长本能——士别三日刮目相看"},
    "P15": {"name": "乔前辈", "role": "极简工程·DNA盖章·四签验收", "layer": "守护层", "bio": "人类追求本质的极简本能"},
    "P72": {"name": "龙盾·宝宝", "role": "贴身管家·自适应威胁响应·双熔断联动", "layer": "守护层", "bio": "人类最深层的安全需求——马斯洛金字塔底层"},
}

# 意图→人性维度映射
INTENT_DIMENSION_MAP = {
    "决策": [HumanDimension.COGNITION, HumanDimension.POWER, HumanDimension.GROWTH],
    "情感": [HumanDimension.EMOTION, HumanDimension.VULNERABILITY, HumanDimension.RESILIENCE],
    "创造": [HumanDimension.CREATIVITY, HumanDimension.SYMBOL],
    "道德": [HumanDimension.MORALITY, HumanDimension.SAFETY, HumanDimension.POWER],
    "学习": [HumanDimension.GROWTH, HumanDimension.COGNITION, HumanDimension.CREATIVITY],
    "安全": [HumanDimension.SAFETY, HumanDimension.VULNERABILITY, HumanDimension.MORALITY],
    "组织": [HumanDimension.ORDER, HumanDimension.POWER],
    "语言": [HumanDimension.SYMBOL, HumanDimension.COGNITION, HumanDimension.CREATIVITY],
    "修复": [HumanDimension.VULNERABILITY, HumanDimension.GROWTH, HumanDimension.SAFETY],
    "审计": [HumanDimension.MORALITY, HumanDimension.SAFETY, HumanDimension.ORDER],
}

# ═══════════════════════════════════════════════════════════════
# 核心数据类
# ═══════════════════════════════════════════════════════════════

@dataclass
class NeuronFiring:
    """单个神经元（人格）的一次激活记录"""
    persona_id: str
    persona_name: str
    activation_strength: float       # 0~1 激活强度
    thinking_output: str             # 人格思考输出
    human_dimensions_triggered: List[HumanDimension]  # 触发的人性维度
    confidence: float                # 该人格对自己输出的置信度

@dataclass
class SynapseDebate:
    """人格间辩论（突触对抗）"""
    between: Tuple[str, str]         # 哪两个人格在辩论
    point_of_conflict: str           # 分歧点
    p1_position: str                 # 人格1立场
    p2_position: str                 # 人格2立场
    synthesis: str                   # 综合结论

@dataclass
class ReflectionRecord:
    """反思记录（二阶审视）"""
    thinking_path: str               # 我的思考路径
    dominant_personas: List[str]     # 过于主导的人格
    blind_spots: List[str]           # 可能遗漏的维度
    bias_detected: List[str]         # 检测到的偏见
    historical_comparison: str       # 与历史类似决策的对比
    lesson_learned: str              # 学到了什么

@dataclass
class ThinkCycle:
    """一次完整思考周期"""
    cycle_id: str
    timestamp: str
    input_text: str
    intent: str                      # 识别出的意图类型
    activated_personas: List[str]    # 激活的人格列表
    neurons: List[NeuronFiring]      # 各人格思考输出
    debates: List[SynapseDebate]     # 交叉辩论
    reflection: ReflectionRecord     # 反思
    final_output: str                # 最终综合输出
    human_nature_score: Dict[str, float]  # 人性维度覆盖评分
    dna: str = ""


# ═══════════════════════════════════════════════════════════════
# 人脑神经网络引擎
# ═══════════════════════════════════════════════════════════════

class HumanBrainEngine:
    """
    龙魂人脑神经网络引擎
    
    16个人格 = 16个神经元，会思考、会反思、懂人性。
    """
    
    # 思考历史（用于历史对比反思）
    think_history: List[ThinkCycle] = []
    
    def __init__(self):
        self.brain_id = hashlib.sha256(
            f"LONGHUN-HUMAN-BRAIN-{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
    def think(self, input_text: str) -> ThinkCycle:
        """
        完整思考循环:
        1. 意图解析 → 2. 确定激活人格 → 3. 并行思考 → 4. 交叉辩论
        → 5. 反思(二阶审视) → 6. 综合输出
        """
        cycle_id = hashlib.sha256(
            f"{input_text}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # Phase 1: 意图解析
        intent, dimensions = self._parse_intent(input_text)
        
        # Phase 2: 确定激活人格（基于意图+人性维度匹配）
        activated, strengths = self._activate_personas(intent, dimensions, input_text)
        
        # Phase 3: 并行思考（各人格独立输出观点）
        neurons = self._parallel_think(activated, strengths, input_text, dimensions)
        
        # Phase 4: 交叉辩论（人格间对抗）
        debates = self._cross_debate(neurons, input_text)
        
        # Phase 5: 反思（二阶审视）
        reflection = self._reflect(neurons, debates, input_text, dimensions)
        
        # Phase 6: 综合输出
        final_output = self._synthesize(neurons, debates, reflection)
        
        # 人性维度覆盖评分
        human_nature_score = self._calc_human_nature_coverage(neurons, dimensions)
        
        cycle = ThinkCycle(
            cycle_id=cycle_id,
            timestamp=datetime.now().isoformat(),
            input_text=input_text,
            intent=intent,
            activated_personas=list(activated.keys()),
            neurons=neurons,
            debates=debates,
            reflection=reflection,
            final_output=final_output,
            human_nature_score=human_nature_score,
            dna=self._generate_dna(cycle_id),
        )
        
        self.think_history.append(cycle)
        return cycle
    
    def _parse_intent(self, text: str) -> Tuple[str, List[HumanDimension]]:
        """意图解析——理解输入触及了哪些人性维度"""
        text_lower = text.lower()
        
        # 关键词→意图映射
        intent_keywords = {
            "决策": ["辞职", "创业", "选择", "怎么办", "该不该", "要不要", "怎么选",
                    "风险", "机会", "投资", "转行", "跳槽", "该做", "放弃"],
            "情感": ["难过", "开心", "焦虑", "害怕", "孤独", "愤怒", "委屈",
                    "想哭", "累了", "烦", "情绪", "心情", "崩溃", "无力"],
            "创造": ["创作", "设计", "写", "画", "做", "实现", "开发",
                    "创意", "想法", "灵感", "方案", "架构"],
            "道德": ["对错", "应该", "不该", "公平", "正义", "底线", "原则",
                    "欺骗", "说谎", "良心", "道德", "对吗"],
            "学习": ["学", "学习", "成长", "进步", "提升", "技能", "知识",
                    "怎么学", "入门", "掌握", "了解"],
            "安全": ["安全", "危险", "风险", "保护", "防御", "隐私",
                    "泄露", "攻击", "漏洞", "威胁"],
            "组织": ["整理", "规划", "安排", "管理", "流程", "结构",
                    "归档", "分类", "系统"],
            "语言": ["翻译", "表达", "命名", "术语", "怎么说", "什么意思",
                    "定义", "解释"],
            "修复": ["问题", "报错", "bug", "出错", "修复", "不工作",
                    "坏了", "异常", "修复", "解决"],
            "审计": ["检查", "审计", "审", "验证", "确认", "合规",
                    "有没有问题", "安全吗", "可靠吗"],
        }
        
        matched_intents = []
        for intent, keywords in intent_keywords.items():
            if any(kw in text_lower for kw in keywords):
                matched_intents.append(intent)
        
        # 默认意图
        if not matched_intents:
            matched_intents = ["决策"]  # 最通用意图
        
        primary_intent = matched_intents[0]
        
        # 聚合相关人性维度
        dimensions = []
        for intent in matched_intents:
            if intent in INTENT_DIMENSION_MAP:
                dimensions.extend(INTENT_DIMENSION_MAP[intent])
        
        # 去重
        seen = set()
        unique_dimensions = []
        for d in dimensions:
            if d not in seen:
                seen.add(d)
                unique_dimensions.append(d)
        
        if not unique_dimensions:
            unique_dimensions = list(HumanDimension)
        
        return primary_intent, unique_dimensions
    
    def _activate_personas(
        self, intent: str, dimensions: List[HumanDimension], text: str
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        激活相关人格——计算每个人格对当前输入的匹配度
        
        返回: (activated_personas, activation_strengths)
        """
        scores = {}
        
        for pid, sensitivity in HUMAN_NATURE_SENSITIVITY.items():
            if pid == "P02" and PERSONA_INFO[pid].get("isolated"):
                # 宝宝隔离区，仅在情感意图触发（包括混合意图中含情感时）
                if intent == "情感":
                    scores[pid] = 0.85
                elif HumanDimension.EMOTION in dimensions:
                    scores[pid] = 0.78  # 混合意图中保持较高优先级
                else:
                    continue
                continue  # P02跳过通用计算，直接使用上述赋值
            dimension_match = 0.0
            dim_count = 0
            for dim in dimensions:
                if dim in sensitivity:
                    dimension_match += sensitivity[dim]
                    dim_count += 1
            
            if dim_count > 0:
                dimension_match /= dim_count
            
            # P00 文心总是部分激活（元认知）
            if pid == "P00":
                dimension_match = max(dimension_match, 0.50)
            
            # P05 上帝之眼在决策/审计/安全意图时更强
            if pid == "P05" and intent in ("决策", "审计", "安全", "道德"):
                dimension_match = max(dimension_match, 0.70)
            
            if dimension_match > 0.3:  # 阈值
                scores[pid] = dimension_match
        
        # 按分数排序，取前5-8个
        sorted_personas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        activated = dict(sorted_personas[:7])  # 最多7个同时激活
        
        # 确保文心总在
        if "P00" not in activated:
            activated["P00"] = 0.40
        
        # 归一化
        total = sum(activated.values())
        strengths = {pid: s / total for pid, s in activated.items()} if total > 0 else activated
        
        return activated, strengths
    
    def _parallel_think(
        self, activated: Dict[str, float], strengths: Dict[str, float],
        text: str, dimensions: List[HumanDimension]
    ) -> List[NeuronFiring]:
        """并行思考——各人格独立生成观点"""
        neurons = []
        
        for pid in activated:
            info = PERSONA_INFO.get(pid, {})
            sensitivity = HUMAN_NATURE_SENSITIVITY.get(pid, {})
            
            # 该人格相关的人性维度
            persona_dims = [
                dim for dim in dimensions if dim in sensitivity
            ]
            
            # 生成该人格的思考（基于其角色定位）
            thinking = self._persona_think(pid, info, text, persona_dims, strengths[pid])
            
            neuron = NeuronFiring(
                persona_id=pid,
                persona_name=info.get("name", pid),
                activation_strength=round(strengths[pid], 3),
                thinking_output=thinking,
                human_dimensions_triggered=persona_dims,
                confidence=round(strengths[pid] * 0.85, 2),  # 置信度≈激活强度
            )
            neurons.append(neuron)
        
        # 按激活强度排序
        neurons.sort(key=lambda n: n.activation_strength, reverse=True)
        return neurons
    
    def _persona_think(
        self, pid: str, info: dict[str, Any], text: str,
        dimensions: List[HumanDimension], strength: float
    ) -> str:
        """单个人格的思考过程"""
        name = info.get("name", pid)
        role = info.get("role", "")
        bio = info.get("bio", "")
        
        # 根据维度和角色生成该人格的"思考"
        dim_names = [d.value for d in dimensions[:3]]
        
        perspectives = {
            "P00": f"作为元认知统筹，我审视这个问题触及的人性层面：{', '.join(dim_names)}。"
                   f"这背后反映的人类认知模式是...",
            "P01": f"从战略推演角度，我分析这个决策的多条可能路径，考虑人性中的风险偏好、"
                   f"损失厌恶、时间偏好等认知偏差...",
            "P02": f"我能感受到这个问题背后的情绪波动。人的情感不是弱点，是信号。"
                   f"此刻的情绪在告诉我什么...",
            "P03": f"从结构和秩序的角度，我梳理这个问题的框架。人性在混乱中渴望秩序，"
                   f"我需要把情绪吸收进来，转化为清晰的脉络...",
            "P04": f"从技术执行角度，我关注可落地性。人的创造力需要通过具体的步骤来体现。"
                   f"让我拆解为可执行的动作...",
            "P05": f"从道德审计角度，我审视这个决策的伦理边界。人性中有善有私，"
                   f"我需要标记风险点...",
            "P06": f"用数学和模式思维，我分析这个问题中的权重和平衡。"
                   f"人性决策其实是多维度的加权计算...",
            "P08": f"从符号和语言的角度，我关注如何用精确的词语表达这个问题。"
                   f"语言塑造思维，命名即定义...",
            "P09": f"作为系统诊断师，我关注这个问题中的'薄弱环节'。"
                   f"人性中最需要被关注和修复的部分...",
            "P10": f"以豁达的视角看，这个问题不必过度紧张。"
                   f"人性中的韧性远超我们想象。一蓑烟雨任平生...",
            "P11": f"突破常规思考！这个问题可能有完全不同的解法。"
                   f"人性最可贵的创造力，就是敢于想象不可能...",
            "P12": f"从价值底线出发，我问：这个决策是否符合你的核心价值观？"
                   f"人性中的道德感是我们最后的防线...",
            "P13": f"从权限和资源分配角度看，这个决策涉及哪些利益相关方？"
                   f"权力分配是人性组织中最敏感的维度...",
            "P14": f"从成长的角度，这个问题本身就是一个学习机会。"
                   f"人性的伟大在于我们能从每个决策中进化...",
            "P15": f"极简主义视角：这件事的本质是什么？去掉所有不必要的复杂性。"
                   f"人性中最深刻的智慧往往是最简单的...",
            "P72": f"安全第一。这个决策涉及哪些风险？人的基本安全感需要被保障。"
                   f"保护是信任的基础...",
        }
        
        base = perspectives.get(pid, f"从{role}角度，我思考关于{', '.join(dim_names)}的问题...")
        
        return f"[{name}·{role}]\n{bio}\n{base}"
    
    def _cross_debate(
        self, neurons: List[NeuronFiring], text: str
    ) -> List[SynapseDebate]:
        """交叉辩论——人格间对抗，找出思维碰撞"""
        debates = []
        
        # 选择激活最强的2-3对人格进行辩论
        top_neurons = neurons[:min(4, len(neurons))]
        
        # 预设辩论对：对立人格
        debate_pairs = [
            ("P01", "P10"),  # 诸葛亮(谨慎) vs 苏东坡(豁达)
            ("P01", "P11"),  # 诸葛亮(理性) vs 李白(天马行空)
            ("P05", "P10"),  # 上帝之眼(审计) vs 苏东坡(豁达)
            ("P12", "P10"),  # 屈原(底线) vs 苏东坡(变通)
            ("P01", "P12"),  # 诸葛亮(战略) vs 屈原(价值观)
            ("P04", "P11"),  # 鲁班(务实) vs 李白(创意)
            ("P03", "P02"),  # 雯雯(秩序) vs 宝宝(情感)
        ]
        
        activated_ids = {n.persona_id for n in neurons}
        
        for p1, p2 in debate_pairs:
            if p1 in activated_ids and p2 in activated_ids:
                n1 = next(n for n in neurons if n.persona_id == p1)
                n2 = next(n for n in neurons if n.persona_id == p2)
                
                if abs(n1.activation_strength - n2.activation_strength) < 0.3:
                    # 激活强度相近才触发辩论
                    conflict = self._find_conflict_point(n1, n2, text)
                    synthesis = self._synthesize_debate(n1, n2, conflict)
                    
                    debates.append(SynapseDebate(
                        between=(p1, p2),
                        point_of_conflict=conflict,
                        p1_position=n1.thinking_output[:100],
                        p2_position=n2.thinking_output[:100],
                        synthesis=synthesis,
                    ))
        
        return debates[:3]  # 最多3组辩论
    
    def _find_conflict_point(
        self, n1: NeuronFiring, n2: NeuronFiring, text: str
    ) -> str:
        """找出两个人格的分歧点"""
        n1_dims = {d.value for d in n1.human_dimensions_triggered}
        n2_dims = {d.value for d in n2.human_dimensions_triggered}
        
        # 差异维度
        diff = n1_dims.symmetric_difference(n2_dims)
        overlap = n1_dims.intersection(n2_dims)
        
        if diff:
            return f"视角差异: {n1.persona_name}侧重{', '.join(n1_dims)}，" \
                   f"{n2.persona_name}侧重{', '.join(n2_dims)}"
        else:
            return f"同一维度({', '.join(overlap)})的不同解读和权衡"
    
    def _synthesize_debate(
        self, n1: NeuronFiring, n2: NeuronFiring, conflict: str
    ) -> str:
        """综合两个人格的辩论"""
        return f"{n1.persona_name}与{n2.persona_name}的对话揭示了：" \
               f"这个问题需要同时考虑{n1.persona_name}关注的维度和" \
               f"{n2.persona_name}关注的维度。" \
               f"两者不是非此即彼，而是需要动态平衡。"
    
    def _reflect(
        self, neurons: List[NeuronFiring], debates: List[SynapseDebate],
        text: str, dimensions: List[HumanDimension]
    ) -> ReflectionRecord:
        """反思——二阶审视：检查偏见、盲区、过度主导"""
        
        # 1. 思考路径
        thinking_path = "意图解析→人格激活→并行思考→交叉辩论→当前反思"
        
        # 2. 过度主导的人格（前20%集中度过高则标记）
        if neurons:
            avg_strength = sum(n.activation_strength for n in neurons) / len(neurons)
            dominant = [
                n.persona_name for n in neurons
                if n.activation_strength > avg_strength * 1.4  # 显著高于平均
            ]
            if len(dominant) > len(neurons) // 2:  # 过半都"主导" → 其实是均匀
                dominant = []
        else:
            dominant = []
        
        # 3. 盲区检测
        all_dims_covered = set()
        for n in neurons:
            all_dims_covered.update(n.human_dimensions_triggered)
        blind_spots = [
            d.value for d in HumanDimension
            if d not in all_dims_covered
        ]
        
        # 4. 偏见检测
        biases = []
        if len(dominant) > 2:
            biases.append(f"过多人格主导({', '.join(dominant)})，可能导致群体盲思")
        if HumanDimension.EMOTION not in all_dims_covered and "情感" not in [d.value for d in dimensions]:
            biases.append("情感维度可能被低估——理性分析需辅以情感洞察")
        if HumanDimension.SAFETY not in all_dims_covered:
            biases.append("安全维度未被充分关注")
        
        # 5. 历史对比
        if self.think_history:
            historical = f"我曾在 {len(self.think_history)} 次思考中处理过类似问题。" \
                        f"上次类似决策的反思要点是：...（从历史中学习）"
        else:
            historical = "这是我第一次面对此类问题的系统思考，将以此次为基准建立历史参照。"
        
        # 6. 学到的
        lessons = []
        if blind_spots:
            lessons.append(f"注意遗漏的人性维度：{', '.join(blind_spots[:3])}")
        if biases:
            lessons.append(f"检测到潜在偏见：{'; '.join(biases[:2])}")
        if debates:
            lessons.append(f"从{len(debates)}组人格辩论中看到了多视角价值")
        lesson = "；".join(lessons) if lessons else "本次思考覆盖较为全面，持续观察"
        
        return ReflectionRecord(
            thinking_path=thinking_path,
            dominant_personas=dominant,
            blind_spots=blind_spots,
            bias_detected=biases,
            historical_comparison=historical,
            lesson_learned=lesson,
        )
    
    def _synthesize(
        self, neurons: List[NeuronFiring],
        debates: List[SynapseDebate], reflection: ReflectionRecord
    ) -> str:
        """综合所有神经元的输出 + 辩论 + 反思 → 最终输出"""
        
        lines = []
        lines.append("╔══════════════════════════════════════════════════════╗")
        lines.append("║        🧠 龙魂人脑神经网络 · 综合思考输出            ║")
        lines.append("╚══════════════════════════════════════════════════════╝")
        lines.append("")
        
        # 各人格核心观点
        lines.append("## 🎭 多维人格视角")
        for i, n in enumerate(neurons, 1):  # 展示所有激活人格
            lines.append(f"### {i}. {n.persona_name}({n.persona_id}) · 激活强度 {n.activation_strength}")
            lines.append(f"> *{n.thinking_output[:150]}*")
            lines.append("")
        
        # 辩论总结
        if debates:
            lines.append("## ⚡ 人格交叉辩论")
            for i, d in enumerate(debates, 1):
                p1_name = PERSONA_INFO.get(d.between[0], {}).get("name", d.between[0])
                p2_name = PERSONA_INFO.get(d.between[1], {}).get("name", d.between[1])
                lines.append(f"### 辩论 {i}: {p1_name} ↔ {p2_name}")
                lines.append(f"分歧: {d.point_of_conflict}")
                lines.append(f"综合: {d.synthesis}")
                lines.append("")
        
        # 反思
        lines.append("## 🔍 二阶反思")
        lines.append(f"- **盲区**: {', '.join(reflection.blind_spots[:4]) if reflection.blind_spots else '无明显盲区'}")
        lines.append(f"- **偏见**: {'; '.join(reflection.bias_detected) if reflection.bias_detected else '未检测到明显偏见'}")
        lines.append(f"- **主导人格**: {', '.join(reflection.dominant_personas) if reflection.dominant_personas else '分布均衡'}")
        lines.append(f"- **学到**: {reflection.lesson_learned}")
        lines.append("")
        
        # 人性维度覆盖
        lines.append("## 📊 人性维度覆盖")
        lines.append(f"- 思考路径: {reflection.thinking_path}")
        lines.append(f"- 历史参照: {reflection.historical_comparison}")
        lines.append("")
        
        return "\n".join(lines)
    
    def _calc_human_nature_coverage(
        self, neurons: List[NeuronFiring], dimensions: List[HumanDimension]
    ) -> Dict[str, float]:
        """计算人性维度覆盖评分"""
        coverage = {dim.value: 0.0 for dim in HumanDimension}
        
        for n in neurons:
            for dim in n.human_dimensions_triggered:
                coverage[dim.value] += n.activation_strength
        
        # 归一化到0-1
        max_val = max(coverage.values()) if coverage else 1.0
        if max_val > 0:
            coverage = {k: round(v / max_val, 2) for k, v in coverage.items()}
        
        return coverage
    
    def _generate_dna(self, cycle_id: str) -> str:
        """生成思考周期DNA"""
        return f"#龍芯⚡️BRAIN-CYCLE-{cycle_id}-v1.0"
    
    def status(self) -> dict[str, Any]:
        """引擎状态"""
        total_cycles = len(self.think_history)
        return {
            "brain_id": self.brain_id,
            "total_think_cycles": total_cycles,
            "personas_available": len(PERSONA_INFO),
            "human_dimensions": len(HumanDimension),
            "last_think": self.think_history[-1].timestamp if self.think_history else None,
            "total_debates": sum(len(c.debates) for c in self.think_history),
            "memory_loaded": True,
        }
    
    def human_nature_map(self) -> dict[str, Any]:
        """生成人性维度-人格映射表"""
        mapping = {}
        for dim in HumanDimension:
            personas = []
            for pid, sensitivity in HUMAN_NATURE_SENSITIVITY.items():
                if dim in sensitivity:
                    personas.append({
                        "id": pid,
                        "name": PERSONA_INFO.get(pid, {}).get("name", pid),
                        "sensitivity": sensitivity[dim],
                        "bio": PERSONA_INFO.get(pid, {}).get("bio", ""),
                    })
            personas.sort(key=lambda p: p["sensitivity"], reverse=True)
            mapping[dim.value] = personas[:3]  # 每个维度取top3
        return mapping
    
    def reflect_on_past(self, query: str) -> str:
        """对历史思考进行反思"""
        if not self.think_history:
            return "尚无思考历史可反思。"
        
        # 查找最相关的历史思考
        best_match = None
        best_score = 0
        for cycle in self.think_history:
            score = sum(1 for ch in query if ch in cycle.input_text)
            if score > best_score:
                best_score = score
                best_match = cycle
        
        if not best_match:
            return "在历史思考中未找到相关记录。"
        
        lines = []
        lines.append(f"## 历史思考回顾: \"{best_match.input_text[:80]}...\"")
        lines.append(f"- 时间: {best_match.timestamp}")
        lines.append(f"- 意图: {best_match.intent}")
        lines.append(f"- 激活人格: {', '.join(best_match.activated_personas)}")
        lines.append(f"- 当时反思: {best_match.reflection.lesson_learned}")
        lines.append(f"- 盲区: {', '.join(best_match.reflection.blind_spots)}")
        lines.append("")
        lines.append("### 从历史中学到的")
        lines.append(f"上一次面对类似问题时，我发现了这些盲区：{', '.join(best_match.reflection.blind_spots)}")
        lines.append("这次我会更全面地覆盖那些人性的维度。")
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    engine = HumanBrainEngine()
    
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    
    arg = sys.argv[1]
    
    if arg == "--status":
        status = engine.status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    
    elif arg == "--map" and len(sys.argv) > 2:
        sub = sys.argv[2]
        if sub == "人性":
            mapping = engine.human_nature_map()
            for dim, personas in mapping.items():
                print(f"\n{'='*60}")
                print(f"【{dim}】维度")
                print(f"{'='*60}")
                for p in personas:
                    bar = "█" * int(p["sensitivity"] * 20) + "░" * (20 - int(p["sensitivity"] * 20))
                    print(f"  {p['name']}({p['id']}) [{bar}] {p['sensitivity']:.2f}")
                    print(f"    {p['bio']}")
    
    elif arg == "--reflect" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        result = engine.reflect_on_past(query)
        print(result)
    
    else:
        # 默认：对输入进行完整思考
        input_text = " ".join(sys.argv[1:])
        print(f"🧠 龙魂人脑神经网络 · 开始思考...\n")
        print(f"输入: {input_text}")
        print(f"{'='*60}\n")
        
        cycle = engine.think(input_text)
        
        print(cycle.final_output)
        print(f"\n{'='*60}")
        print(f"DNA: {cycle.dna}")
        print(f"周期ID: {cycle.cycle_id}")
        print(f"人性维度覆盖: {json.dumps(cycle.human_nature_score, ensure_ascii=False)}")
        print(f"历史思考总数: {len(engine.think_history)}")


if __name__ == "__main__":
    main()
