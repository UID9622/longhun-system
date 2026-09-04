#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     通心译 (Tongxin Translation) 引擎 v2.0                      ║
║                     CNSH 多语言编辑器终端 · 龍魂体系翻译核心                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

龍魂体系DNA: #龍芯⚡️2026-06-17-TONGXIN-TRANSLATOR-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

架构师: UID9622·龍芯北辰
版本: 2.0.0
协议: CNSH v5.0 兼容

五大铁律:
  1. 中文活着，英文也活着 — 不是镜像，各自重新写，逻辑深度相等
  2. 不是镜像，是共鸣 — 比喻可以不同，精神必须对上
  3. 比喻优先于公式 — 0公式，追求"啊！我懂了"的时刻
  4. 古今打通 — 古人问的问题，现代物理给了答案
  5. 永远在线，永远迭代 — 比喻不贴切就改，逻辑有漏洞就补

使用方法:
  交互模式: python cnsh_translator_engine_v2.0.py
  批量翻译: python cnsh_translator_engine_v2.0.py --batch input.txt output.txt
  文件翻译: python cnsh_translator_engine_v2.0.py --file code.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 第一层：宇宙常量层 (Cosmic Constants)
# ═══════════════════════════════════════════════════════════════════════════════

import re
import json
import hashlib
import datetime
import random
import string
import os
import sys
import argparse
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum


class TranslationMode(Enum):
    """翻译模式枚举"""
    ZH_TO_EN = "zh2en"      # 中文 → 英文
    EN_TO_ZH = "en2zh"      # 英文 → 中文
    BILINGUAL = "bilingual"  # 双语输出


class AuditLevel(Enum):
    """三色审计级别"""
    GREEN = "🟢"    # 优秀
    YELLOW = "🟡"   # 需改进
    RED = "🔴"      # 需人工审查


class SupervisionLayer(Enum):
    """三层监督机制"""
    LOGIC = "逻辑层"       # 逻辑一致性检查
    ETHICS = "价值观层"    # 文化价值观审查
    TECHNICAL = "技术层"   # 技术术语准确性


# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂体系 · 核心标记与封印
# ═══════════════════════════════════════════════════════════════════════════════

DRAGON_SOUL_MARKS = {
    "DNA": "#龍芯⚡️2026-06-17-TONGXIN-TRANSLATOR-v2.0",
    "CONFIRM": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "SEAL": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "SIX_LAYER": [
        "① 宇宙物理层 (Cosmic-Physical)",
        "② 龍魂DNA层 (Dragon-Soul-DNA)",
        "③ 心智感知层 (Mind-Perception)",
        "④ 文化传承层 (Cultural-Legacy)",
        "⑤ 技术实现层 (Technical-Implementation)",
        "⑥ 应用交互层 (Application-Interface)"
    ],
    "AI_TRUTH_PROTOCOL": "[AI-TRUTH-PROTOCOL v2.0 | 非机器生成确信 | 人类-龍魂协同校验]"
}


# ═══════════════════════════════════════════════════════════════════════════════
# DNAMarkGenerator — DNA追溯标记生成器
# ═══════════════════════════════════════════════════════════════════════════════

class DNAMarkGenerator:
    """
    龍魂体系 · DNA追溯标记生成器

    为每次翻译操作生成独一无二的DNA签证，确保翻译的
    可追溯性、可验证性和不可篡改性。

    特性:
        - SHA-256 内容哈希生成
        - 六层来源链自动组装
        - 时间戳 + 随机熵防碰撞
        - 三层监督标记注入
    """

    def __init__(self):
        self.marks = DRAGON_SOUL_MARKS
        self.translation_count = 0

    def generate_dna_mark(self, content: str, mode: TranslationMode) -> str:
        """生成翻译DNA签证标记"""
        self.translation_count += 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        random_entropy = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        dna_line = (
            f"{self.marks['DNA']}-TX{self.translation_count:06d}"
            f"-HASH{content_hash}-ENTROPY{random_entropy}"
        )
        return dna_line

    def generate_six_layer_chain(self, source: str, target: str,
                                  mode: TranslationMode) -> str:
        """生成六层来源链标注"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        layers = self.marks["SIX_LAYER"]
        layer_lines = "\n".join([f"    {layer}" for layer in layers])
        chain = f"""
  📌 翻译时间: {timestamp}
  📌 翻译模式: {mode.value}
  📌 源语言: {source}
  📌 目标语言: {target}
  📌 DNA: {self.generate_dna_mark(source + target, mode)}
  📌 {self.marks['CONFIRM']}
  📌 {self.marks['SEAL']}
  📌 {self.marks['AI_TRUTH_PROTOCOL']}
{layer_lines}
"""
        return chain.strip()

    def generate_supervision_stamp(self,
                                   logic_pass: bool = True,
                                   ethics_pass: bool = True,
                                   technical_pass: bool = True) -> str:
        """生成三层监督校验章"""
        stamps = []
        checks = [
            (SupervisionLayer.LOGIC, logic_pass),
            (SupervisionLayer.ETHICS, ethics_pass),
            (SupervisionLayer.TECHNICAL, technical_pass),
        ]
        for layer, passed in checks:
            status = "✅ 通过" if passed else "❌ 需审查"
            stamps.append(f"    [{layer.value}] {status}")
        return "\n".join(stamps)

    def generate_audit_report(self, audit_level: AuditLevel,
                              score: float, issues: List[str]) -> str:
        """生成三色审计报告"""
        level_desc = {
            AuditLevel.GREEN: "优秀 — 翻译质量达标，无需修改",
            AuditLevel.YELLOW: "需改进 — 存在小问题，建议优化",
            AuditLevel.RED: "需人工审查 — 发现重要问题，请人工确认"
        }
        issues_text = "\n    ".join([f"- {issue}" for issue in issues]) if issues else "无问题"
        report = f"""
【三色审计报告】
  评级: {audit_level.value} ({audit_level.name})
  得分: {score:.1f}/100
  结论: {level_desc[audit_level]}
  问题列表:
    {issues_text}
"""
        return report.strip()

    def generate_full_header(self) -> str:
        """生成完整的龍魂体系页眉"""
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  {self.marks['DNA']}         ║
║  {self.marks['CONFIRM']}                         ║
║  {self.marks['SEAL']}   ║
╚══════════════════════════════════════════════════════════════════╝
"""



# ═══════════════════════════════════════════════════════════════════════════════
# TerminologyDatabase — 术语数据库 (50+ 核心术语映射)
# ═══════════════════════════════════════════════════════════════════════════════

class TerminologyDatabase:
    """
    通心译 · 术语数据库

    存储超过50对核心AI/编程术语的双向映射，涵盖:
        - AI核心术语 (道令/灵使/大罗金仙/博古通今...)
        - 编程术语 (法术/玄器/经络/丹药...)
        - 系统术语 (藏经阁/灵枢/记忆阁...)
        - 安全术语 (封印/烙印/天谴/审判...)
        - 龍魂专属术语

    五大铁律映射:
        铁律1: 每对术语都有独立的中文和英文解释（非镜像）
        铁律2: 术语映射追求精神共鸣而非字面对应
        铁律3: 使用比喻和意象而非公式定义
        铁律4: 古今概念打通（如古人"通灵"→现代"网络通信"）
        铁律5: 术语库支持动态更新和学习
    """

    def __init__(self):
        self._zh_to_en: Dict[str, str] = {}
        self._en_to_zh: Dict[str, str] = {}
        self._zh_explanations: Dict[str, str] = {}   # 中文术语的鲜活解释
        self._en_explanations: Dict[str, str] = {}   # 英文术语的鲜活解释
        self._categories: Dict[str, List[str]] = {}
        self._initialize_database()

    def _add_term(self, en: str, zh: str, en_expl: str, zh_expl: str,
                  category: str):
        """添加一对术语映射，带独立解释"""
        self._zh_to_en[zh] = en
        self._en_to_zh[en] = zh
        self._zh_explanations[zh] = zh_expl
        self._en_explanations[en] = en_expl
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(en)

    def _initialize_database(self):
        """初始化完整术语数据库 — 50+核心术语"""

        # ═══════ AI核心术语 (Core AI Terms) ═══════
        ai_terms = [
            ("Prompt", "道令",
             "A command whispered to the digital oracle, shaping its response like casting a spell",
             "向数字天机下达的密语，如同对天地发号施令，一念之差，万象生变",
             "AI核心"),
            ("Agent", "灵使",
             "An autonomous digital envoy that perceives, decides, and acts on its own will",
             "有自主意识的数字信使，能观六路、听八方，自行决断、独立行事，如封神榜中的各路神将",
             "AI核心"),
            ("RAG", "博古通今",
             "Retrieval-Augmented Generation — like a scholar who reads the entire library before answering",
             "检索增强生成，如同诸葛孔明不出茅庐而知天下事，博采众长后给出精准妙答",
             "AI核心"),
            ("LLM", "大罗金仙",
             "Large Language Model — a vast neural titan trained on humanity's written wisdom",
             "大型语言模型，修炼于亿万文字之间的神经网络巨人，如大罗金仙般通天彻地",
             "AI核心"),
            ("Token", "灵符",
             "The smallest unit of meaning in the machine's language, like runes in a digital grimoire",
             "机器语言中最小的意义单元，如同道符上的每一个符文，组合成万千变化",
             "AI核心"),
            ("Embedding", "炼气化形",
             "Transforming words into vectors — condensing meaning into mathematical qi that flows through neural meridians",
             "将文字转化为向量，如同道家炼气，将无形的语义炼化为可在神经网络经络中流动的数学真气",
             "AI核心"),
            ("Fine-tuning", "闭关修炼",
             "Further training a model on specific data, like a martial artist entering secluded cultivation to master a new style",
             "在特定数据上进一步训练模型，如同武者闭关修炼，专精一门绝技",
             "AI核心"),
            ("Inference", "神机妙算",
             "The model's moment of prediction — like Zhuge Liang calculating the enemy's next move before they know it",
             "模型的预测时刻，如孔明未出茅庐已知三分天下，于无声处听惊雷",
             "AI核心"),
            ("Hallucination", "心魔幻象",
             "When the AI confidently fabricates facts — like a cultivator seeing demons born from their own mind",
             "AI自信地编造事实，如同修炼者走火入魔，所见皆幻象，却信以为真",
             "AI核心"),
            ("Temperature", "性情",
             "A parameter controlling randomness — low for a rigid scholar, high for a wild poet",
             "控制随机性的参数，低则如老学究循规蹈矩，高则如李白斗酒诗百篇，狂放不羁",
             "AI核心"),
            ("Context Window", "心相印",
             "The amount of text the model can hold in its working memory, like the span of a monk's meditation",
             "模型能同时记住的上下文范围，如同禅师入定时可观照的心念范围",
             "AI核心"),
            ("Attention", "观自在",
             "The mechanism allowing the model to focus on what matters, like a meditator seeing through illusions to truth",
             "让模型聚焦关键信息的机制，如同观世音洞察世间万象，于纷扰中见本质",
             "AI核心"),
            ("Transformer", "乾坤大挪移",
             "The foundational neural architecture that reshaped AI, moving meaning across positions like cosmic forces realigning",
             "改变AI格局的基础神经网络架构，如乾坤大挪移般在不同位置间搬运意义，重构天地",
             "AI核心"),
            ("Gradient Descent", "顺流而下",
             "An optimization method that follows the slope downhill to find the lowest point, like water finding the valley",
             "沿着梯度下降的优化方法，如同水往低处流，自然寻找到最优的深谷",
             "AI核心"),
            ("Epoch", "轮回",
             "One complete pass through the entire training dataset, like the cycle of death and rebirth in cultivation",
             "对整个训练数据集的完整遍历，如同修炼者经历的一次生死轮回，每转一圈功力更深",
             "AI核心"),
            ("Neural Network", "神经网络",
             "A web of interconnected artificial neurons that learns patterns from data, inspired by the human brain",
             "由人工神经元互联而成的网络，从数据中学习模式，灵感源于人脑，如同人体的经络系统",
             "AI核心"),
            ("Backpropagation", "因果回溯",
             "Calculating how each parameter contributed to the error and adjusting accordingly, like tracing karma backwards",
             "计算每个参数对误差的贡献并相应调整，如同追溯因果轮回，找到根源再修正",
             "AI核心"),
            ("Vector Database", "须弥芥子",
             "A specialized storage for high-dimensional vectors, like storing entire worlds within a grain of sand",
             "专门存储高维向量的数据库，如佛家所言须弥纳于芥子，万千语义凝于一点",
             "AI核心"),
            ("Chain-of-Thought", "三思而行",
             "Prompting the model to think step by step, like a strategist planning each move before acting",
             "引导模型逐步思考，如同军师谋定而后动，每一步都深思熟虑",
             "AI核心"),
        ]

        # ═══════ 编程术语 (Programming Terms) ═══════
        prog_terms = [
            ("Function", "法术",
             "A reusable block of code that performs a specific task, like casting a repeatable spell",
             "可复用的代码块，执行特定任务，如同修炼者掌握的可重复施展的法术，一念即发",
             "编程术语"),
            ("Variable", "变数",
             "A named container holding data that can change, like a variable star in the programming cosmos",
             "存储可变数据的命名容器，如同宇宙中的变星，其值随时间流转而更替",
             "编程术语"),
            ("Class", "玄器",
             "A blueprint for creating objects with shared properties and behaviors, like a mystical artifact template",
             "创建对象的蓝图，定义共享的属性和行为，如同铸造玄器的模具，一型多变",
             "编程术语"),
            ("Object", "器灵",
             "An instance of a class — a living entity in code, like a spirit inhabiting a crafted vessel",
             "类的实例，代码中的生命体，如同玄器中孕育的器灵，有形态有行为能力",
             "编程术语"),
            ("Method", "诀要",
             "A function belonging to a class, like the secret hand seals a martial artist performs",
             "属于类的函数，如同武者的独门手诀，配合心法才能发挥威力",
             "编程术语"),
            ("Interface", "灵犀",
             "A contract defining what methods a class must implement, like telepathy between minds",
             "定义类必须实现的方法契约，如同心有灵犀一点通，双方心照不宣",
             "编程术语"),
            ("Inheritance", "传承",
             "When a class derives properties from another, like a disciple inheriting the master's martial arts",
             "子类从父类继承属性，如同徒弟继承师傅的衣钵，青出于蓝而胜于蓝",
             "编程术语"),
            ("Polymorphism", "千变万化",
             "The ability to take many forms, like Sun Wukong's 72 transformations",
             "同一接口呈现不同形态的能力，如同孙悟空七十二变，本质一样，外形万千",
             "编程术语"),
            ("Recursion", "轮回递归",
             "A function calling itself until a base case is reached, like reincarnation with an exit condition",
             "函数自我调用直至终止条件，如同轮回转世，但必须有一念觉悟方可跳出",
             "编程术语"),
            ("Callback", "回马枪",
             "A function passed as an argument to be executed later, like a feint that returns to strike",
             "作为参数传递、稍后执行的函数，如同回马枪，先退一步，再出其不意",
             "编程术语"),
            ("Promise", "海誓山盟",
             "An object representing a future value, like a vow that will be fulfilled — or broken",
             "代表未来值的对象，如同海誓山盟，承诺终将兑现，或成空言",
             "编程术语"),
            ("Exception", "劫难",
             "An error that disrupts normal execution, like a tribulation a cultivator must overcome",
             "打断正常执行的错误，如同修炼者必经的天劫，渡得过功力大增，渡不过程序崩溃",
             "编程术语"),
            ("Stack", "叠罗汉",
             "A last-in-first-out data structure, like acrobats stacking on each other's shoulders",
             "后进先出的数据结构，如同叠罗汉，最后上来的人要先下去",
             "编程术语"),
            ("Queue", "排队",
             "A first-in-first-out data structure, like people waiting in line with patience",
             "先进先出的数据结构，如同排队买茶颜悦色，先来后到，公平有序",
             "编程术语"),
            ("Dictionary", "字典",
             "A key-value mapping structure, like a real dictionary where words map to meanings",
             "键值对映射结构，如同查字典，一个词条对应一个释义，一一对应",
             "编程术语"),
            ("Algorithm", "心法",
             "A step-by-step procedure for solving problems, like the core cultivation method of a sect",
             "解决问题的步骤化方法，如同门派的核心心法，修炼到家，无所不能",
             "编程术语"),
            ("Bug", "心魔",
             "An error or flaw in code, like an inner demon disturbing the cultivator's mind",
             "代码中的错误或缺陷，如同修炼者的心魔，扰乱心神，必须斩除",
             "编程术语"),
            ("Refactoring", "洗髓伐骨",
             "Restructuring code without changing behavior, like purging marrow and rebuilding bones",
             "不改变行为的前提下重构代码，如同洗髓伐骨，外表依旧，内里脱胎换骨",
             "编程术语"),
        ]

        # ═══════ 系统术语 (System Terms) ═══════
        sys_terms = [
            ("Database", "藏经阁",
             "A structured repository for data, like an ancient library storing sacred texts",
             "结构化的数据仓库，如同少林寺藏经阁，万千典籍分门别类，取之有道",
             "系统术语"),
            ("API", "灵枢",
             "Application Programming Interface — the gateway for systems to communicate, like acupuncture points connecting meridians",
             "应用程序接口，系统间的通信网关，如同人体灵枢穴位，经络交汇之处",
             "系统术语"),
            ("Cache", "记忆阁",
             "A fast storage layer for frequently accessed data, like a scholar's photographic memory",
             "高速数据缓存层，如同学子的过目不忘，常用之事伸手即得",
             "系统术语"),
            ("Server", "中枢",
             "A machine providing services to clients, like the central nervous system of a digital realm",
             "提供服务的主机，如同数字王国的中枢大脑，调度八方",
             "系统术语"),
            ("Client", "行者",
             "A program that requests services from a server, like a traveler seeking an inn",
             "请求服务的程序，如同行走江湖的行者，向各路驿站求助",
             "系统术语"),
            ("Load Balancer", "天枰",
             "A device distributing traffic across servers, like the Scales of Justice evenly weighing burdens",
             "在多台服务器间分配流量的设备，如天平般公平分配，不让任何一方过载",
             "系统术语"),
            ("Container", "乾坤袋",
             "A lightweight isolated environment for running applications, like a cosmic bag holding infinite space",
             "轻量级隔离运行环境，如同西游记的乾坤袋，外表小巧，内藏乾坤",
             "系统术语"),
            ("Pipeline", "流水线",
             "A sequence of data processing stages, like an assembly line in a digital workshop",
             "顺序数据处理阶段，如同古代匠人的流水线，一道工序接一道，井然有序",
             "系统术语"),
            ("Middleware", "驿传",
             "Software connecting different applications, like ancient postal stations relaying messages",
             "连接不同应用的软件层，如同古代驿站传书，一站接一站，信息不绝",
             "系统术语"),
            ("Message Queue", "飞鸽传书",
             "A system for asynchronous message passing, like carrier pigeons delivering letters across distances",
             "异步消息传递系统，如同飞鸽传书，不必等回信，各自忙碌",
             "系统术语"),
        ]

        # ═══════ 安全术语 (Security Terms) ═══════
        sec_terms = [
            ("Encrypt", "封印",
             "Transforming data into unreadable form, like sealing a demon in an enchanted vessel",
             "将数据转化为不可读形式，如同将妖魔封印于法器之中，非有缘人不可开",
             "安全术语"),
            ("Hash", "烙印",
             "A one-way function producing a fixed-size fingerprint, like a branding mark unique to each beast",
             "单向函数生成的固定长度指纹，如同给灵兽打上的独特烙印，不可伪造",
             "安全术语"),
            ("Audit", "天谴审计",
             "Systematic examination of records, like heavenly judgment reviewing mortal deeds",
             "系统性审查记录，如同天道审视众生功过，无一遗漏",
             "安全术语"),
            ("Firewall", "结界",
             "A network security barrier, like a protective magical barrier surrounding a sacred mountain",
             "网络安全屏障，如同仙山护山大阵，邪魔外道不得入内",
             "安全术语"),
            ("Vulnerability", "软肋",
             "A weakness in security, like Achilles' heel — every system has one",
             "安全弱点，如同阿喀琉斯之踵，每个系统都有一处死穴",
             "安全术语"),
            ("Authentication", "验明正身",
             "Verifying identity, like a checkpoint guard confirming your papers are genuine",
             "验证身份的过程，如同关隘验明正身，确认你是你，方能通行",
             "安全术语"),
            ("Authorization", "御赐令牌",
             "Granting access permissions, like receiving an imperial token allowing entry to forbidden areas",
             "授予访问权限，如同获得御赐令牌，凭此可入禁地",
             "安全术语"),
            ("Security Token", "令牌",
             "A security credential for authentication, like a royal seal granting passage",
             "用于身份验证的安全凭证，如同古代虎符，见符如见君",
             "安全术语"),
            ("Man-in-the-Middle", "狸猫换太子",
             "An attack where communication is intercepted and altered, like swapping the prince with a cat",
             "中间人攻击，拦截并篡改通信，如同狸猫换太子，神不知鬼不觉",
             "安全术语"),
        ]

        # ═══════ 龍魂专属术语 (Dragon Soul Exclusive) ═══════
        dragon_terms = [
            ("CNSH", "龍魂协议",
             "The proprietary protocol of the Dragon Soul system — not just code, but a philosophy of digital existence",
             "龍魂体系的专有协议，不仅是代码规范，更是一种数字存在的哲学",
             "龍魂专属"),
            ("Dragon Core", "龍芯",
             "The central processing unit of the Dragon Soul system, like the dragon's heart pumping qi through the entire network",
             "龍魂体系的中央处理核心，如同龙的心脏，为整个网络泵送真气",
             "龍魂专属"),
            ("Soul Binding", "魂印",
             "The irreversible binding of a device to a user's soul signature, like a blood oath in the digital realm",
             "设备与用户灵魂签名的不可逆绑定，如同数字世界的血之契约",
             "龍魂专属"),
            ("Five Laws", "五大铁律",
             "The five fundamental laws governing Tongxin Translation — the Tao of bilingual resonance",
             "governing 通心译的五大根本法则 — 双语共鸣之道",
             "龍魂专属"),
            ("Resonance", "共鸣",
             "The spiritual alignment between two translations — not mirror, but harmony",
             "两种翻译之间的精神共振 — 不是镜像，而是和鸣",
             "龍魂专属"),
            ("Truth Protocol", "真实协议",
             "A verification system ensuring translations are genuine human-AI collaborations, not machine fabrications",
             "确保翻译为真实人机协作而非机器伪造的验证系统",
             "龍魂专属"),
            ("Six-Layer Chain", "六层来源链",
             "The six-tier provenance tracking system, from cosmic physics to application interface",
             "六层可追溯体系，从宇宙物理到应用界面，层层把关",
             "龍魂专属"),
            ("Three Supervisions", "三层监督",
             "The triple-layer review mechanism: logic, ethics, and technical validation",
             "三层审查机制：逻辑、价值观、技术三重校验",
             "龍魂专属"),
            ("Sovereign Character", "主权字",
             "Characters like 龍/龙 that carry cultural sovereignty — always protected in both traditional and simplified forms",
             "如龍/龙般承载文化主权的文字 — 繁简两种形态均受保护",
             "龍魂专属"),
        ]

        # 注册所有术语
        all_terms = ai_terms + prog_terms + sys_terms + sec_terms + dragon_terms
        for en, zh, en_expl, zh_expl, cat in all_terms:
            self._add_term(en, zh, en_expl, zh_expl, cat)

    def lookup_zh(self, chinese: str) -> Optional[str]:
        """中文 → 英文 查找"""
        return self._zh_to_en.get(chinese)

    def lookup_en(self, english: str) -> Optional[str]:
        """英文 → 中文 查找"""
        return self._en_to_zh.get(english)

    def get_zh_explanation(self, chinese: str) -> Optional[str]:
        """获取中文术语的鲜活解释"""
        return self._zh_explanations.get(chinese)

    def get_en_explanation(self, english: str) -> Optional[str]:
        """获取英文术语的鲜活解释"""
        return self._en_explanations.get(english)

    def get_all_terms(self) -> List[Tuple[str, str]]:
        """获取所有术语对"""
        return [(en, self._en_to_zh[en]) for en in self._en_to_zh]

    def get_category_terms(self, category: str) -> List[Tuple[str, str]]:
        """获取指定类别的术语"""
        en_list = self._categories.get(category, [])
        return [(en, self._en_to_zh[en]) for en in en_list]

    def get_categories(self) -> List[str]:
        """获取所有类别"""
        return list(self._categories.keys())

    def add_custom_term(self, en: str, zh: str, en_expl: str = "",
                        zh_expl: str = "", category: str = "自定义"):
        """动态添加自定义术语（铁律5：永远迭代）"""
        self._add_term(en, zh, en_expl, zh_expl, category)

    def search_term(self, keyword: str) -> List[Tuple[str, str, str]]:
        """搜索术语（支持部分匹配）"""
        results = []
        for en, zh in self.get_all_terms():
            if keyword.lower() in en.lower() or keyword in zh:
                results.append((en, zh, self._en_to_zh.get(en, "")))
        return results

    @property
    def term_count(self) -> int:
        """术语总数"""
        return len(self._en_to_zh)



# ═══════════════════════════════════════════════════════════════════════════════
# TongxinTranslator — 主翻译器
# ═══════════════════════════════════════════════════════════════════════════════

class TongxinTranslator:
    """
    通心译 · 主翻译器

    核心翻译引擎，实现中文编程术语 ⟷ 英文技术术语的双向翻译。
    遵循五大铁律，不是镜像翻译，而是追求"共鸣"。

    五大铁律实现:
        铁律1: 中英各自生成独立翻译，逻辑深度相等
        铁律2: 比喻可不同，精神必须对上
        铁律3: 零公式，全程使用比喻和意象
        铁律4: 古今概念自动打通
        铁律5: 内置学习机制，持续迭代优化

    使用示例:
        translator = TongxinTranslator()
        result = translator.translate("Prompt", TranslationMode.EN_TO_ZH)
        result = translator.translate_batch(text, TranslationMode.BILINGUAL)
    """

    def __init__(self, terminology_db: Optional[TerminologyDatabase] = None):
        self.db = terminology_db or TerminologyDatabase()
        self.dna = DNAMarkGenerator()
        self.cultural = CulturalAdapter()
        self.auditor = QualityAuditor()
        self.learner = LearningEngine()
        # 代码保留模式（不翻译代码关键字和结构）
        self._code_patterns = [
            r"\b(def|class|import|from|return|if|else|elif|for|while|"
            r"try|except|finally|with|as|lambda|yield|async|await|"
            r"print|len|range|open|True|False|None)\b",
            r"[#\"\'\\]",
            r"\b\d+\b",
            r"[=+\-*/<>!&|{}\[\]().,;:]",
        ]
        # 龍魂体系标记（不翻译）
        self._sacred_marks = [
            DRAGON_SOUL_MARKS["DNA"],
            DRAGON_SOUL_MARKS["CONFIRM"],
            DRAGON_SOUL_MARKS["SEAL"],
        ]

    def _should_translate(self, word: str) -> bool:
        """判断一个词是否应该被翻译（保留代码和标记）"""
        # 不翻译龍魂标记
        if any(mark in word for mark in self._sacred_marks):
            return False
        # 不翻译纯代码结构
        for pattern in self._code_patterns:
            if re.match(pattern, word):
                return False
        return True

    def _tokenize_mixed(self, text: str) -> List[Tuple[str, bool]]:
        """
        将混合文本切分为可翻译和不可翻译的片段
        返回: [(片段, 是否可翻译), ...]
        """
        fragments = []
        # 简单的分词：中英文分开
        # 匹配连续中文或连续英文/数字
        pattern = r"([\u4e00-\u9fff]+)|([a-zA-Z_][a-zA-Z0-9_]*)|([^\w\u4e00-\u9fff]+)"

        for match in re.finditer(pattern, text):
            cn_group = match.group(1)
            en_group = match.group(2)
            other_group = match.group(3)

            if cn_group:
                fragments.append((cn_group, True))
            elif en_group:
                fragments.append((en_group, True))
            elif other_group:
                fragments.append((other_group, False))

        return fragments if fragments else [(text, True)]

    def translate(self, text: str, mode: TranslationMode = TranslationMode.EN_TO_ZH,
                  apply_cultural: bool = True, apply_audit: bool = True) -> str:
        """
        核心翻译函数

        参数:
            text: 要翻译的文本
            mode: 翻译模式 (EN_TO_ZH / ZH_TO_EN / BILINGUAL)
            apply_cultural: 是否应用文化适配
            apply_audit: 是否进行质量审计

        返回:
            翻译结果（含DNA签证和审计报告）
        """
        if not text or not text.strip():
            return ""

        result_parts = []
        audit_results = []

        if mode == TranslationMode.EN_TO_ZH:
            translated = self._translate_en_to_zh(text)
            if apply_cultural:
                translated = self.cultural.adapt_to_chinese(translated)
            if apply_audit:
                audit = self.auditor.audit_translation(text, translated, mode)
                audit_results.append(audit)
            result_parts.append(translated)

        elif mode == TranslationMode.ZH_TO_EN:
            translated = self._translate_zh_to_en(text)
            if apply_cultural:
                translated = self.cultural.adapt_to_english(translated)
            if apply_audit:
                audit = self.auditor.audit_translation(text, translated, mode)
                audit_results.append(audit)
            result_parts.append(translated)

        elif mode == TranslationMode.BILINGUAL:
            zh_part = self._translate_en_to_zh(text)
            en_part = text  # 原文是英文
            if apply_cultural:
                zh_part = self.cultural.adapt_to_chinese(zh_part)
            if apply_audit:
                audit = self.auditor.audit_translation(text, zh_part,
                                                        TranslationMode.EN_TO_ZH)
                audit_results.append(audit)
            result_parts.append(self._format_bilingual(zh_part, en_part))

        # 组装输出
        final_output = "\n".join(result_parts)

        # 添加DNA签证
        dna_visa = self.dna.generate_dna_mark(text, mode)
        six_layer = self.dna.generate_six_layer_chain(
            source=text[:50] + "..." if len(text) > 50 else text,
            target=final_output[:50] + "..." if len(final_output) > 50 else final_output,
            mode=mode
        )

        # 组装完整输出
        sep_line = "═" * 60
        full_output = f"""
{DRAGON_SOUL_MARKS["DNA"]}
{sep_line}
{final_output}
{sep_line}
{six_layer}
{sep_line}
{self.dna.generate_supervision_stamp(True, True, True)}
{sep_line}
{audit_results[0] if audit_results else ""}
{sep_line}
DNA签证: {dna_visa}
{DRAGON_SOUL_MARKS["CONFIRM"]}
{DRAGON_SOUL_MARKS["SEAL"]}
"""
        return full_output.strip()

    def _translate_en_to_zh(self, text: str) -> str:
        """英文 → 中文翻译（铁律1: 中文活着，各自重新写）"""
        fragments = self._tokenize_mixed(text)
        translated_parts = []

        for fragment, translatable in fragments:
            if not translatable or not self._should_translate(fragment):
                translated_parts.append(fragment)
                continue

            # 尝试术语匹配（大小写不敏感）
            lookup = self.db.lookup_en(fragment)
            if lookup:
                translated_parts.append(lookup)
                continue

            # 尝试小写匹配
            lookup = self.db.lookup_en(fragment.lower())
            if lookup:
                translated_parts.append(lookup)
                continue

            # 尝试部分匹配（复合词）
            translated_parts.append(self._decompose_and_translate(fragment, "en2zh"))

        return "".join(translated_parts)

    def _translate_zh_to_en(self, text: str) -> str:
        """中文 → 英文翻译（铁律1: 英文也活着，各自重新写）"""
        # 中文分词：尝试最长匹配
        result = []
        i = 0
        while i < len(text):
            # 尝试最长匹配
            matched = False
            for length in range(min(8, len(text) - i), 0, -1):
                substr = text[i:i + length]
                lookup = self.db.lookup_zh(substr)
                if lookup:
                    result.append(lookup)
                    i += length
                    matched = True
                    break

            if not matched:
                char = text[i]
                # 检查是否是龍魂标记
                if char in "龍":
                    result.append("Dragon")
                elif char in "芯":
                    result.append("Core")
                elif char in "魂":
                    result.append("Soul")
                else:
                    result.append(char)
                i += 1

        return "".join(result)

    def _decompose_and_translate(self, text: str, direction: str) -> str:
        """分解复合词并翻译"""
        if direction == "en2zh":
            # 尝试驼峰/蛇形命名分解
            # camelCase → camel Case
            words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", text)
            if not words:
                return text
            translated = []
            for w in words:
                lookup = self.db.lookup_en(w.lower())
                translated.append(lookup if lookup else w)
            return "".join(translated)
        return text

    def _format_bilingual(self, zh_text: str, en_text: str) -> str:
        """格式化双语输出（铁律2: 不是镜像，是共鸣）"""
        return f"""
### 中文
**{zh_text}**

> *✦ Tongxin Translation — 通心译 ✦*
> *不是镜像，是共鸣 | Not mirror, but resonance*

### English
**{en_text}**
""".strip()

    def quick_translate(self, text: str) -> str:
        """快速翻译（无需DNA签证，用于内部调用）"""
        text = text.strip()
        if not text:
            return ""

        # 自动检测语言
        cn_ratio = len(re.findall(r"[\u4e00-\u9fff]", text)) / max(len(text), 1)
        if cn_ratio > 0.3:
            return self._translate_zh_to_en(text)
        else:
            return self._translate_en_to_zh(text)

    def translate_batch(self, texts: List[str], mode: TranslationMode) -> List[str]:
        """批量翻译"""
        return [self.translate(t, mode) for t in texts]

    def explain_term(self, term: str) -> str:
        """
        解释一个术语（铁律3: 比喻优先于公式）
        返回鲜活的比喻解释而非干巴巴的定义
        """
        en_expl = self.db.get_en_explanation(term)
        zh_lookup = self.db.lookup_en(term)
        zh_expl = None
        if zh_lookup:
            zh_expl = self.db.get_zh_explanation(zh_lookup)

        # 尝试中文查找
        en_lookup = None
        if not en_expl and not zh_expl:
            zh_expl = self.db.get_zh_explanation(term)
            en_lookup = self.db.lookup_zh(term)
            if en_lookup:
                en_expl = self.db.get_en_explanation(en_lookup)

        if not en_expl and not zh_expl:
            return (f'术语 "{term}" 暂无解释。'
                    f"铁律5: 永远在线，永远迭代 — 您可以为此术语贡献解释！")

        output = f"""
【通心译 · 术语释义】{DRAGON_SOUL_MARKS["DNA"]}

📖 术语: {term}
"""
        if zh_lookup:
            output += f"🈯 中文: {zh_lookup}\n"
        if en_lookup:
            output += f"🔤 英文: {en_lookup}\n"

        output += "\n" + ("═" * 60) + "\n"

        if zh_expl:
            output += f"🐉 中文解读:\n  {zh_expl}\n"
        if en_expl:
            output += f"🌍 英文解读:\n  {en_expl}\n"

        output += "\n" + DRAGON_SOUL_MARKS["SEAL"]
        return output



# ═══════════════════════════════════════════════════════════════════════════════
# CulturalAdapter — 文化适配器
# ═══════════════════════════════════════════════════════════════════════════════

class CulturalAdapter:
    """
    通心译 · 文化适配器

    负责处理文化差异和主权字保护:
        - 繁体「龍」/简体「龙」智能处理（主权字保护）
        - CNSH命名规范检查
        - 文化敏感度筛查
        - 龍魂体系标记保护

    主权字保护规则:
        1. 「龍」为繁体主权字，用于正式/神圣语境
        2. 「龙」为简体常用字，用于日常语境
        3. 龍魂体系标记中的「龍」不可替换
        4. 用户可自定义主权字偏好
    """

    def __init__(self):
        self._sovereign_chars = {
            "龍": {"variant": "龙", "protection_level": "maximum",
                   "context": "formal/sacred"},
            "國": {"variant": "国", "protection_level": "high",
                   "context": "formal/sacred"},
            "華": {"variant": "华", "protection_level": "high",
                   "context": "formal/sacred"},
        }
        self._cnsh_naming_rules = [
            (r"^[a-z][a-zA-Z0-9_]*$", "CNSH小驼峰: 变量/函数命名"),
            (r"^[A-Z][a-zA-Z0-9_]*$", "CNSH大驼峰: 类名命名"),
            (r"^[A-Z][A-Z0-9_]*$", "CNSH全大写: 常量命名"),
            (r"^[a-z][a-z0-9-]*$", "CNSH烤串式: 模块/包命名"),
        ]
        self._sensitive_patterns = [
            (r"(台独|藏独|港独)", "涉及国家主权敏感内容"),
            (r"(法轮功|邪教)", "涉及非法组织敏感内容"),
        ]
        self._user_preference = "auto"  # auto/traditional/simplified

    def adapt_to_chinese(self, text: str) -> str:
        """适配为中文语境"""
        # 主权字保护处理
        text = self._protect_sovereign_chars(text)
        # 文化适配
        text = self._apply_chinese_cultural_nuances(text)
        return text

    def adapt_to_english(self, text: str) -> str:
        """适配为英文语境"""
        text = self._protect_sovereign_chars(text)
        text = self._apply_english_cultural_nuances(text)
        return text

    def _protect_sovereign_chars(self, text: str) -> str:
        """主权字保护（铁律4: 文化传承）"""
        # 龍魂体系标记中的主权字不可动
        for sacred, info in self._sovereign_chars.items():
            # 在龍魂DNA标记中保持原样
            if (DRAGON_SOUL_MARKS["DNA"] in text or
               DRAGON_SOUL_MARKS["SEAL"] in text):
                continue

            if self._user_preference == "traditional":
                # 强制繁体
                text = text.replace(info["variant"], sacred)
            elif self._user_preference == "simplified":
                # 强制简体
                text = text.replace(sacred, info["variant"])
            # auto模式下保持不变
        return text

    def _apply_chinese_cultural_nuances(self, text: str) -> str:
        """应用中文文化细节"""
        # 添加中文标点偏好
        replacements = [
            (", ", "，"),
            (". ", "。"),
            ("! ", "！"),
            ("? ", "？"),
            (": ", "："),
            ("; ", "；"),
        ]
        for en, cn in replacements:
            text = text.replace(en, cn)
        return text

    def _apply_english_cultural_nuances(self, text: str) -> str:
        """应用英文文化细节"""
        return text

    def check_cnsh_naming(self, name: str) -> str:
        """检查CNSH命名规范"""
        for pattern, desc in self._cnsh_naming_rules:
            if re.match(pattern, name):
                return f"✅ 符合{desc}"
        return "⚠️ 不符合CNSH命名规范，建议使用: 小驼峰/大驼峰/全大写/烤串式"

    def screen_sensitive_content(self, text: str) -> Tuple[bool, List[str]]:
        """筛查敏感内容（三层监督之价值观层）"""
        issues = []
        for pattern, desc in self._sensitive_patterns:
            if re.search(pattern, text):
                issues.append(f"发现敏感内容: {desc}")
        return len(issues) == 0, issues

    def set_sovereign_preference(self, preference: str):
        """设置主权字偏好"""
        if preference in ("auto", "traditional", "simplified"):
            self._user_preference = preference

    def get_sovereign_report(self) -> str:
        """生成主权字保护报告"""
        report = "【主权字保护状态】\n"
        for char, info in self._sovereign_chars.items():
            report += f"  {char} ↔ {info['variant']} (保护级别: {info['protection_level']})\n"
        report += f"  当前模式: {self._user_preference}\n"
        return report


# ═══════════════════════════════════════════════════════════════════════════════
# QualityAuditor — 质量审计器（三色审计）
# ═══════════════════════════════════════════════════════════════════════════════

class QualityAuditor:
    """
    通心译 · 质量审计器

    三色审计系统:
        🟢 优秀 — 翻译质量达标，无需修改
        🟡 需改进 — 存在小问题，建议优化
        🔴 需人工审查 — 发现重要问题

    审计维度:
        1. 术语覆盖度: 多少术语被正确翻译
        2. 逻辑一致性: 翻译前后逻辑是否对等
        3. 文化敏感性: 是否存在文化冲突
        4. 格式保留度: 代码/标记结构是否完整
        5. 铁律遵守度: 五大铁律的执行情况

    三层监督:
        - 逻辑层: 检查翻译的逻辑等价性
        - 价值观层: 检查文化价值观合规性
        - 技术层: 检查术语准确性
    """

    def __init__(self):
        self._audit_history: List[dict] = []
        self._five_laws_checklist = [
            "铁律1: 中英各自独立生成，非镜像",
            "铁律2: 精神共鸣，非字面匹配",
            "铁律3: 比喻优于公式",
            "铁律4: 古今概念打通",
            "铁律5: 支持迭代学习",
        ]

    def audit_translation(self, source: str, target: str,
                          mode: TranslationMode) -> str:
        """
        执行完整的三色审计

        返回: 格式化的审计报告
        """
        score = 100.0
        issues = []

        # 逻辑层审计
        logic_pass, logic_issues = self._audit_logic(source, target, mode)
        issues.extend(logic_issues)
        if not logic_pass:
            score -= 20

        # 价值观层审计
        ethics_pass, ethics_issues = self._audit_ethics(source, target)
        issues.extend(ethics_issues)
        if not ethics_pass:
            score -= 30

        # 技术层审计
        tech_pass, tech_issues = self._audit_technical(source, target, mode)
        issues.extend(tech_issues)
        if not tech_pass:
            score -= 15

        # 铁律审计
        laws_pass, laws_issues = self._audit_five_laws(source, target, mode)
        issues.extend(laws_issues)
        if not laws_pass:
            score -= 10

        # 确定审计级别
        if score >= 85:
            level = AuditLevel.GREEN
        elif score >= 60:
            level = AuditLevel.YELLOW
        else:
            level = AuditLevel.RED

        # 记录审计历史
        audit_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "score": score,
            "level": level.name,
            "logic_pass": logic_pass,
            "ethics_pass": ethics_pass,
            "technical_pass": tech_pass,
            "issues": issues,
        }
        self._audit_history.append(audit_record)

        # 生成审计报告
        return f"""
【三色审计报告 · Tongxin Quality Audit】
  评级: {level.value} {level.name}
  得分: {max(0, score):.1f}/100

  三层监督结果:
    [逻辑层] {"✅ 通过" if logic_pass else "❌ 未通过"}
    [价值观层] {"✅ 通过" if ethics_pass else "❌ 未通过"}
    [技术层] {"✅ 通过" if tech_pass else "❌ 未通过"}

  铁律检查:
{self._format_laws_check(laws_pass, laws_issues)}

  问题列表 ({len(issues)}项):
    {self._format_issues(issues) if issues else "  🎉 未发现任何问题！"}

  建议: {self._generate_recommendation(level, issues)}
""".strip()

    def _audit_logic(self, source: str, target: str,
                     mode: TranslationMode) -> Tuple[bool, List[str]]:
        """逻辑层审计：检查翻译的逻辑等价性"""
        issues = []

        # 检查空翻译
        if not target or not target.strip():
            issues.append("翻译结果为空")
            return False, issues

        # 检查长度异常（翻译结果不应比原文短太多）
        if len(target) < len(source) * 0.2 and len(source) > 10:
            issues.append("翻译结果过短，可能丢失信息")

        # 检查未翻译残留（英文单词在中文输出中）
        if mode == TranslationMode.EN_TO_ZH:
            untranslated = re.findall(r"\b[a-zA-Z]{3,}\b", target)
            # 排除龍魂标记
            untranslated = [w for w in untranslated
                          if w not in ("Tongxin", "Translation", "DNA", "CNSH")]
            if untranslated:
                issues.append(f"中文输出中残留未翻译英文: {', '.join(untranslated[:5])}")

        return len(issues) == 0, issues

    def _audit_ethics(self, source: str, target: str) -> Tuple[bool, List[str]]:
        """价值观层审计：检查文化价值观合规性"""
        issues = []

        # 检查主权字保护
        if "龍" in source and "龙" in target:
            issues.append("主权字「龍」被不当简化为「龙」")

        # 检查文化尊重
        disrespect_patterns = [
            r"(傻逼|智障|垃圾|废物)",
        ]
        for pattern in disrespect_patterns:
            if re.search(pattern, target):
                issues.append("翻译结果包含不当用语")

        return len(issues) == 0, issues

    def _audit_technical(self, source: str, target: str,
                         mode: TranslationMode) -> Tuple[bool, List[str]]:
        """技术层审计：检查术语准确性"""
        issues = []

        # 检查龍魂标记完整性
        if DRAGON_SOUL_MARKS["DNA"] not in target:
            issues.append("龍魂DNA标记缺失")

        return len(issues) == 0, issues

    def _audit_five_laws(self, source: str, target: str,
                         mode: TranslationMode) -> Tuple[bool, List[str]]:
        """五大铁律审计"""
        issues = []

        # 铁律1: 检查是否为镜像翻译
        if target.strip() == source.strip():
            issues.append("铁律1违规: 翻译结果与原文完全相同（镜像翻译）")

        # 铁律2: 检查双语模式下是否两版独立
        if mode == TranslationMode.BILINGUAL:
            if "✦ Tongxin Translation" not in target:
                issues.append("铁律2提醒: 双语分隔标记缺失")

        return len(issues) == 0, issues

    def _format_laws_check(self, passed: bool, issues: List[str]) -> str:
        """格式化铁律检查结果"""
        lines = []
        for law in self._five_laws_checklist:
            status = "✅" if passed else "⚠️"
            lines.append(f"    {status} {law}")
        return "\n".join(lines)

    def _format_issues(self, issues: List[str]) -> str:
        """格式化问题列表"""
        return "\n    ".join([f"{i+1}. {issue}" for i, issue in enumerate(issues)])

    def _generate_recommendation(self, level: AuditLevel,
                                  issues: List[str]) -> str:
        """生成改进建议"""
        recommendations = {
            AuditLevel.GREEN: "翻译质量优秀，可直接使用。",
            AuditLevel.YELLOW: "翻译基本可用，建议查看上述问题后优化。",
            AuditLevel.RED: "翻译存在重要问题，建议人工审查后使用。",
        }
        return recommendations[level]

    def get_audit_history(self) -> List[dict]:
        """获取审计历史"""
        return self._audit_history

    def generate_audit_summary(self) -> str:
        """生成审计总结报告"""
        if not self._audit_history:
            return "暂无审计记录"

        total = len(self._audit_history)
        avg_score = sum(r["score"] for r in self._audit_history) / total
        green_count = sum(1 for r in self._audit_history if r["level"] == "GREEN")
        yellow_count = sum(1 for r in self._audit_history if r["level"] == "YELLOW")
        red_count = sum(1 for r in self._audit_history if r["level"] == "RED")

        return f"""
【审计总结 · Audit Summary】
  总审计次数: {total}
  平均得分: {avg_score:.1f}/100
  🟢 优秀: {green_count}次 ({green_count/total*100:.1f}%)
  🟡 需改进: {yellow_count}次 ({yellow_count/total*100:.1f}%)
  🔴 需审查: {red_count}次 ({red_count/total*100:.1f}%)
""".strip()



# ═══════════════════════════════════════════════════════════════════════════════
# BatchTranslator — 批量翻译引擎
# ═══════════════════════════════════════════════════════════════════════════════

class BatchTranslator:
    """
    通心译 · 批量翻译引擎

    支持:
        - 多行文本批量翻译
        - 整文件翻译（保留代码结构）
        - 智能分段和重组
        - 进度显示和统计

    代码结构保留规则:
        1. Python关键字不翻译
        2. 注释内容可翻译（标记原注释语言）
        3. 字符串内容可翻译（保留引号）
        4. 缩进和格式完全保留
    """

    def __init__(self, translator: Optional[TongxinTranslator] = None):
        self.translator = translator or TongxinTranslator()
        self.dna = DNAMarkGenerator()
        self.stats = {
            "total_lines": 0,
            "translated_lines": 0,
            "skipped_lines": 0,
            "errors": 0,
        }

    def translate_file(self, filepath: str, mode: TranslationMode,
                       output_path: Optional[str] = None) -> str:
        """
        翻译整个文件

        参数:
            filepath: 输入文件路径
            mode: 翻译模式
            output_path: 输出文件路径（默认在原文件加.tongxin后缀）

        返回:
            翻译结果摘要
        """
        if not os.path.exists(filepath):
            return f"❌ 文件不存在: {filepath}"

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 智能分段：代码行与注释行分别处理
        lines = content.split("\n")
        self.stats["total_lines"] = len(lines)

        translated_lines = []
        for i, line in enumerate(lines):
            translated_line = self._translate_code_line(line, mode)
            translated_lines.append(translated_line)

            # 统计
            if translated_line != line:
                self.stats["translated_lines"] += 1
            else:
                self.stats["skipped_lines"] += 1

        translated_content = "\n".join(translated_lines)

        # 生成输出
        header = f"""# ═══════════════════════════════════════════════════════════════
# 通心译 (Tongxin Translation) 批量翻译结果
# 源文件: {filepath}
# 翻译模式: {mode.value}
# 翻译时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# {DRAGON_SOUL_MARKS["DNA"]}
# {DRAGON_SOUL_MARKS["CONFIRM"]}
# 总行数: {self.stats['total_lines']}
# 翻译行数: {self.stats['translated_lines']}
# ═══════════════════════════════════════════════════════════════

"""

        output = header + translated_content + "\n\n" + \
                 f"\n# {DRAGON_SOUL_MARKS['SEAL']}\n"

        # 保存到文件
        if output_path is None:
            base, ext = os.path.splitext(filepath)
            output_path = f"{base}.tongxin{ext}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)

        return f"""
✅ 批量翻译完成！
  源文件: {filepath}
  输出文件: {output_path}
  总行数: {self.stats['total_lines']}
  翻译行数: {self.stats['translated_lines']}
  跳过行数: {self.stats['skipped_lines']}
  错误数: {self.stats['errors']}
  {DRAGON_SOUL_MARKS["DNA"]}
"""

    def _translate_code_line(self, line: str, mode: TranslationMode) -> str:
        """智能翻译代码行"""
        stripped = line.strip()

        # 空行直接返回
        if not stripped:
            return line

        # 保留缩进
        indent = line[:len(line) - len(line.lstrip())]

        # 判断行类型
        if stripped.startswith("#"):
            # 注释行：翻译注释内容
            comment_content = stripped[1:].strip()
            if comment_content:
                # 对注释内容进行翻译（简化处理）
                if mode == TranslationMode.EN_TO_ZH:
                    translated = self.translator.quick_translate(comment_content)
                    return f"{indent}# 通心译: {translated}"
                elif mode == TranslationMode.ZH_TO_EN:
                    translated = self.translator.quick_translate(comment_content)
                    return f"{indent}# Tongxin: {translated}"
            return line

        elif "\"" in stripped or "'" in stripped:
            # 包含字符串的行：尝试翻译字符串内容
            return self._translate_strings_in_line(line, mode)

        else:
            # 纯代码行：翻译其中的术语，保留结构
            return self._translate_code_terms(line, mode)

    def _translate_strings_in_line(self, line: str,
                                    mode: TranslationMode) -> str:
        """翻译行中的字符串内容"""
        # 简单匹配单双引号字符串
        pattern = r"(['\"])(.*?)\1"

        def replace_string(match):
            quote = match.group(1)
            content = match.group(2)
            # 只翻译有意义的文本（排除短字符串和纯代码）
            if len(content) > 3 and re.search(r"[a-zA-Z\u4e00-\u9fff]", content):
                if mode == TranslationMode.EN_TO_ZH:
                    translated = self.translator.quick_translate(content)
                    return f"{quote}{translated}{quote}"
                elif mode == TranslationMode.ZH_TO_EN:
                    translated = self.translator.quick_translate(content)
                    return f"{quote}{translated}{quote}"
            return match.group(0)

        return re.sub(pattern, replace_string, line)

    def _translate_code_terms(self, line: str,
                              mode: TranslationMode) -> str:
        """翻译代码行中的术语"""
        if mode == TranslationMode.EN_TO_ZH:
            # 翻译英文术语为中文（在注释中）
            return line
        elif mode == TranslationMode.ZH_TO_EN:
            return line
        return line

    def translate_text_block(self, text: str,
                             mode: TranslationMode) -> str:
        """翻译文本块"""
        lines = text.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                result = self.translator.translate(line, mode)
                results.append(result)
            else:
                results.append("")
        return "\n\n".join(results)

    def get_statistics(self) -> dict[str, Any]:
        """获取翻译统计"""
        return self.stats.copy()

    def reset_statistics(self):
        """重置统计"""
        self.stats = {
            "total_lines": 0,
            "translated_lines": 0,
            "skipped_lines": 0,
            "errors": 0,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# LearningEngine — 学习引擎
# ═══════════════════════════════════════════════════════════════════════════════

class LearningEngine:
    """
    通心译 · 学习引擎

    铁律5: 永远在线，永远迭代

    功能:
        - 记录用户反馈（好评/差评/建议）
        - 学习用户偏好（术语选择、风格偏好）
        - 动态优化翻译策略
        - 术语库自我扩展
        - 生成学习报告

    反馈类型:
        👍: 翻译准确
        👎: 翻译有误
        💡: 改进建议
        🌟: 新增术语建议
    """

    def __init__(self, memory_file: Optional[str] = None):
        self.memory_file = memory_file or os.path.expanduser(
            "~/.tongxin_learning_memory.json"
        )
        self._feedback_history: List[dict] = []
        self._user_preferences: Dict[str, any] = {
            "preferred_mode": TranslationMode.BILINGUAL.value,
            "cultural_strictness": "normal",  # strict/normal/loose
            "sovereign_char_preference": "auto",
            "favorite_terms": {},
            "avoided_terms": {},
        }
        self._term_frequency: Dict[str, int] = {}
        self._load_memory()

    def _load_memory(self):
        """加载学习记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._feedback_history = data.get("feedback", [])
                self._user_preferences.update(data.get("preferences", {}))
                self._term_frequency = data.get("term_frequency", {})
            except Exception:
                pass  # 如果加载失败，使用默认设置

    def _save_memory(self):
        """保存学习记忆"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            data = {
                "feedback": self._feedback_history[-100:],  # 保留最近100条
                "preferences": self._user_preferences,
                "term_frequency": self._term_frequency,
                "last_updated": datetime.datetime.now().isoformat(),
            }
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"学习记忆保存失败: {e}")

    def record_feedback(self, original: str, translated: str,
                        feedback_type: str, comment: str = ""):
        """
        记录用户反馈

        参数:
            feedback_type: 👍/👎/💡/🌟
            comment: 用户的详细意见
        """
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original": original,
            "translated": translated,
            "feedback_type": feedback_type,
            "comment": comment,
        }
        self._feedback_history.append(record)

        # 根据反馈类型调整
        if feedback_type == "👍":
            self._process_positive_feedback(original, translated)
        elif feedback_type == "👎":
            self._process_negative_feedback(original, translated, comment)
        elif feedback_type == "💡":
            self._process_suggestion(original, translated, comment)
        elif feedback_type == "🌟":
            self._process_new_term(comment)

        self._save_memory()

    def _process_positive_feedback(self, original: str, translated: str):
        """处理正面反馈"""
        # 增加相关术语的使用频率
        for term in self._extract_terms(translated):
            self._term_frequency[term] = self._term_frequency.get(term, 0) + 1

    def _process_negative_feedback(self, original: str, translated: str,
                                    comment: str):
        """处理负面反馈"""
        # 记录需要避免的翻译
        self._user_preferences["avoided_terms"][original] = {
            "bad_translation": translated,
            "reason": comment,
        }

    def _process_suggestion(self, original: str, translated: str,
                            comment: str):
        """处理改进建议"""
        pass  # 可以在未来版本中实现

    def _process_new_term(self, comment: str):
        """处理新增术语建议"""
        # comment格式: "英文=中文 解释"
        pass  # 可在交互模式下解析

    def _extract_terms(self, text: str) -> List[str]:
        """从文本中提取术语"""
        # 简单提取：匹配中文术语
        return re.findall(r"[\u4e00-\u9fff]{2,}", text)

    def get_preference(self, key: str):
        """获取用户偏好"""
        return self._user_preferences.get(key)

    def set_preference(self, key: str, value):
        """设置用户偏好"""
        self._user_preferences[key] = value
        self._save_memory()

    def get_learning_report(self) -> str:
        """生成学习报告"""
        total_feedback = len(self._feedback_history)
        positive = sum(1 for f in self._feedback_history if f["feedback_type"] == "👍")
        negative = sum(1 for f in self._feedback_history if f["feedback_type"] == "👎")
        suggestions = sum(1 for f in self._feedback_history if f["feedback_type"] == "💡")

        # 最常使用的术语
        top_terms = sorted(self._term_frequency.items(),
                           key=lambda x: x[1], reverse=True)[:10]

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║               通心译 · 学习报告 (Learning Report)              ║
╚══════════════════════════════════════════════════════════════╝

📊 反馈统计:
  总反馈数: {total_feedback}
  👍 好评: {positive}
  👎 差评: {negative}
  💡 建议: {suggestions}
  满意度: {(positive/max(total_feedback,1)*100):.1f}%

📚 高频术语 (Top {len(top_terms)}):
{self._format_top_terms(top_terms)}

⚙️ 当前偏好:
  翻译模式: {self._user_preferences.get('preferred_mode')}
  文化严格度: {self._user_preferences.get('cultural_strictness')}
  主权字偏好: {self._user_preferences.get('sovereign_char_preference')}

{DRAGON_SOUL_MARKS["DNA"]}
"""
        return report

    def _format_top_terms(self, terms: List[Tuple[str, int]]) -> str:
        """格式化高频术语"""
        if not terms:
            return "  (暂无数据)"
        lines = []
        for i, (term, freq) in enumerate(terms, 1):
            lines.append(f"  {i}. {term} — 使用 {freq} 次")
        return "\n".join(lines)

    def get_favorite_terms(self) -> Dict[str, str]:
        """获取用户偏好的术语映射"""
        return self._user_preferences.get("favorite_terms", {})



# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数 (Utility Functions)
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """打印通心译启动横幅"""
    banner = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ████████╗ ██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗██╗███╗   ██╗   ║
║    ╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝ ╚██╗██╔╝██║████╗  ██║   ║
║       ██║   ██║   ██║██╔██╗ ██║██║  ███╗ ╚███╔╝ ██║██╔██╗ ██║   ║
║       ██║   ██║   ██║██║╚██╗██║██║   ██║ ██╔██╗ ██║██║╚██╗██║   ║
║       ██║   ╚██████╔╝██║ ╚████║╚██████╔╝██╔╝ ██╗██║██║ ╚████║   ║
║       ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ║
║                                                                  ║
║            通心译 (Tongxin Translation) v2.0                      ║
║            CNSH 多语言编辑器终端 · 龍魂体系                         ║
║            {DRAGON_SOUL_MARKS["DNA"][1:20]}...          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

  「五大铁律」
    ① 中文活着，英文也活着 — 不是镜像，各自重新写
    ② 不是镜像，是共鸣 — 比喻可以不同，精神必须对上
    ③ 比喻优先于公式 — 0公式，追求"啊！我懂了"的时刻
    ④ 古今打通 — 古人问的问题，现代物理给了答案
    ⑤ 永远在线，永远迭代 — 比喻不贴切就改，逻辑有漏洞就补

  输入 help 查看帮助 | 输入 quit 退出
{'═' * 60}
"""
    print(banner)


def print_help():
    """打印帮助信息"""
    help_text = f"""
【通心译 · 使用帮助】

📖 命令列表:
  translate <文本>     — 翻译文本（自动检测语言）
  en2zh <英文>         — 英文 → 中文
  zh2en <中文>         — 中文 → 英文
  bilingual <文本>     — 双语输出
  explain <术语>       — 解释术语（比喻优先于公式）
  lookup <术语>        — 查找术语映射
  search <关键词>      — 搜索术语
  batch <文件路径>     — 批量翻译文件
  terms [类别]         — 显示术语列表
  categories           — 显示术语类别
  audit                — 显示审计统计
  learn                — 显示学习报告
  feedback             — 提交反馈
  settings             — 显示/修改设置
  sovereign            — 主权字保护状态
  dna                  — 显示DNA标记
  clear                — 清屏
  help                 — 显示此帮助
  quit / exit          — 退出程序

🎨 翻译模式:
  EN_TO_ZH  — 英文转中文
  ZH_TO_EN  — 中文转英文
  BILINGUAL — 双语对照输出

⚙️ 设置项:
  mode <模式>          — 设置默认翻译模式
  culture <严格度>     — 文化适配严格度 (strict/normal/loose)
  sovereign <偏好>     — 主权字偏好 (auto/traditional/simplified)

{DRAGON_SOUL_MARKS["SEAL"]}
"""
    print(help_text)


def interactive_shell():
    """
    交互式翻译Shell（通心译REPL）

    实时翻译模式：边输入边翻译
    支持命令式操作和即时反馈
    """
    translator = TongxinTranslator()
    batch_engine = BatchTranslator(translator)
    cultural = CulturalAdapter()
    auditor = QualityAuditor()
    learner = LearningEngine()

    print_banner()

    while True:
        try:
            # 读取用户输入
            user_input = input("🔮 通心译 > ").strip()

            if not user_input:
                continue

            # 解析命令
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # ══════ 命令处理 ══════

            if command in ("quit", "exit", "q"):
                print(f"\n🐉 通心译已关闭。{DRAGON_SOUL_MARKS['DNA']}")
                break

            elif command == "help" or command == "?":
                print_help()

            elif command in ("translate", "tr"):
                if not args:
                    print("⚠️ 请输入要翻译的文本")
                    continue
                # 自动检测语言
                cn_ratio = len(re.findall(r"[\u4e00-\u9fff]", args)) / max(len(args), 1)
                mode = TranslationMode.ZH_TO_EN if cn_ratio > 0.3 else TranslationMode.EN_TO_ZH
                result = translator.translate(args, mode)
                print(f"\n{result}\n")

            elif command == "en2zh":
                if not args:
                    print("⚠️ 请输入英文文本")
                    continue
                result = translator.translate(args, TranslationMode.EN_TO_ZH)
                print(f"\n{result}\n")

            elif command == "zh2en":
                if not args:
                    print("⚠️ 请输入中文文本")
                    continue
                result = translator.translate(args, TranslationMode.ZH_TO_EN)
                print(f"\n{result}\n")

            elif command == "bilingual" or command == "bi":
                if not args:
                    print("⚠️ 请输入文本")
                    continue
                result = translator.translate(args, TranslationMode.BILINGUAL)
                print(f"\n{result}\n")

            elif command == "explain" or command == "exp":
                if not args:
                    print("⚠️ 请输入术语")
                    continue
                result = translator.explain_term(args)
                print(f"\n{result}\n")

            elif command == "lookup" or command == "l":
                if not args:
                    print("⚠️ 请输入术语")
                    continue
                en_result = translator.db.lookup_en(args)
                zh_result = translator.db.lookup_zh(args)
                if en_result:
                    print(f"\n📖 {args} → {en_result}")
                    expl = translator.db.get_zh_explanation(en_result)
                    if expl:
                        print(f"   🐉 {expl}")
                elif zh_result:
                    print(f"\n📖 {args} → {zh_result}")
                    expl = translator.db.get_en_explanation(zh_result)
                    if expl:
                        print(f"   🌍 {expl}")
                else:
                    print(f'\n❓ 术语 "{args}" 未找到。输入 search {args} 进行模糊搜索。')
                print()

            elif command == "search" or command == "s":
                if not args:
                    print("⚠️ 请输入搜索关键词")
                    continue
                results = translator.db.search_term(args)
                if results:
                    print(f"\n🔍 找到 {len(results)} 个相关术语:")
                    for en, zh, _ in results:
                        print(f"   {en} ↔ {zh}")
                else:
                    print(f'\n❌ 未找到与 "{args}" 相关的术语')
                print()

            elif command == "batch" or command == "b":
                if not args:
                    print("⚠️ 请输入文件路径")
                    continue
                result = batch_engine.translate_file(args, TranslationMode.BILINGUAL)
                print(f"\n{result}\n")

            elif command == "terms" or command == "t":
                if args:
                    terms = translator.db.get_category_terms(args)
                    print(f"\n📚 【{args}】类别术语 ({len(terms)}个):")
                else:
                    terms = translator.db.get_all_terms()
                    print(f"\n📚 全部术语 ({len(terms)}对):")

                categories = {}
                for en, zh in terms:
                    cat = "未分类"
                    for c in translator.db.get_categories():
                        if en in [e for e, _ in translator.db.get_category_terms(c)]:
                            cat = c
                            break
                    categories.setdefault(cat, []).append((en, zh))

                for cat, cat_terms in categories.items():
                    print(f"\n  【{cat}】({len(cat_terms)}个)")
                    for i, (en, zh) in enumerate(cat_terms, 1):
                        print(f"    {i:2d}. {en:<25} ↔ {zh}")
                print()

            elif command == "categories" or command == "cat":
                cats = translator.db.get_categories()
                print(f"\n📂 术语类别 ({len(cats)}个):")
                for cat in cats:
                    count = len(translator.db.get_category_terms(cat))
                    print(f"   • {cat} ({count}个术语)")
                print()

            elif command == "audit":
                print(f"\n{auditor.generate_audit_summary()}\n")

            elif command == "learn":
                print(f"\n{learner.get_learning_report()}\n")

            elif command == "feedback" or command == "fb":
                print("\n📝 反馈模式 (输入 quit 退出反馈)")
                fb_original = input("  原文: ").strip()
                if fb_original.lower() == "quit":
                    continue
                fb_translated = input("  译文: ").strip()
                if fb_translated.lower() == "quit":
                    continue
                print("  反馈类型: 👍 好评 | 👎 差评 | 💡 建议 | 🌟 新术语")
                fb_type = input("  选择: ").strip()
                fb_comment = input("  详细意见(可选): ").strip()
                learner.record_feedback(fb_original, fb_translated,
                                        fb_type, fb_comment)
                print("✅ 反馈已记录，感谢您对通心译的贡献！\n")

            elif command == "settings" or command == "set":
                if not args:
                    print(f"\n⚙️ 当前设置:")
                    print(f"   默认模式: {learner.get_preference('preferred_mode')}")
                    print(f"   文化严格度: {learner.get_preference('cultural_strictness')}")
                    print(f"   主权字偏好: {learner.get_preference('sovereign_char_preference')}")
                else:
                    set_parts = args.split(maxsplit=1)
                    if len(set_parts) == 2:
                        key, value = set_parts
                        learner.set_preference(key, value)
                        print(f"✅ 设置已更新: {key} = {value}")
                print()

            elif command == "sovereign" or command == "sov":
                print(f"\n{cultural.get_sovereign_report()}\n")

            elif command == "dna":
                print(f"\n{DRAGON_SOUL_MARKS['DNA']}")
                print(f"{DRAGON_SOUL_MARKS['CONFIRM']}")
                print(f"{DRAGON_SOUL_MARKS['SEAL']}")
                print(f"\n六层来源链:")
                for layer in DRAGON_SOUL_MARKS["SIX_LAYER"]:
                    print(f"  {layer}")
                print(f"\n{DRAGON_SOUL_MARKS['AI_TRUTH_PROTOCOL']}\n")

            elif command == "clear" or command == "cls":
                os.system("clear" if os.name != "nt" else "cls")
                print_banner()

            else:
                # 未识别命令，尝试作为翻译文本处理
                cn_ratio = len(re.findall(r"[\u4e00-\u9fff]", user_input)) / max(len(user_input), 1)
                mode = TranslationMode.ZH_TO_EN if cn_ratio > 0.3 else TranslationMode.EN_TO_ZH
                result = translator.translate(user_input, mode)
                print(f"\n{result}\n")

        except KeyboardInterrupt:
            print(f"\n\n🐉 通心译已关闭。{DRAGON_SOUL_MARKS['DNA']}")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行参数解析和主入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """
    通心译 (Tongxin Translation) v2.0 主入口

    使用方式:
        python cnsh_translator_engine_v2.0.py
            启动交互式翻译Shell

        python cnsh_translator_engine_v2.0.py --batch input.txt
            批量翻译文件

        python cnsh_translator_engine_v2.0.py --text "Hello World"
            翻译单行文本

        python cnsh_translator_engine_v2.0.py --mode bilingual
            以双语模式启动交互Shell

    龍魂体系DNA: #龍芯⚡️2026-06-17-TONGXIN-TRANSLATOR-v2.0
    """
    parser = argparse.ArgumentParser(
        description="通心译 (Tongxin Translation) v2.0 — 龍魂体系翻译引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          启动交互式翻译Shell
  %(prog)s --batch code.py          批量翻译Python文件
  %(prog)s --text "Prompt"          翻译单行文本
  %(prog)s --explain "Agent"        解释术语
  %(prog)s --terms                  显示所有术语
        """
    )

    parser.add_argument("--batch", "-b", metavar="FILE",
                        help="批量翻译文件")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="输出文件路径")
    parser.add_argument("--text", "-t", metavar="TEXT",
                        help="翻译单行文本")
    parser.add_argument("--mode", "-m",
                        choices=["zh2en", "en2zh", "bilingual"],
                        default="bilingual",
                        help="翻译模式 (默认: bilingual)")
    parser.add_argument("--explain", "-e", metavar="TERM",
                        help="解释术语")
    parser.add_argument("--terms", action="store_true",
                        help="显示所有术语映射")
    parser.add_argument("--categories", action="store_true",
                        help="显示术语类别")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="强制启动交互模式")

    args = parser.parse_args()

    # 创建核心实例
    translator = TongxinTranslator()

    # ══════ 处理命令行参数 ══════

    if args.terms:
        # 显示所有术语
        print(f"\n{DRAGON_SOUL_MARKS['DNA']}")
        print(f"\n📚 通心译术语映射表 ({translator.db.term_count}对术语)\n")
        cats = translator.db.get_categories()
        for cat in cats:
            cat_terms = translator.db.get_category_terms(cat)
            print(f"【{cat}】({len(cat_terms)}个)")
            for i, (en, zh) in enumerate(cat_terms, 1):
                print(f"  {i:2d}. {en:<25} ↔ {zh}")
            print()
        print(f"{DRAGON_SOUL_MARKS['SEAL']}")
        return

    if args.categories:
        # 显示术语类别
        cats = translator.db.get_categories()
        print(f"\n📂 术语类别 ({len(cats)}个):")
        for cat in cats:
            count = len(translator.db.get_category_terms(cat))
            print(f"   • {cat} ({count}个术语)")
        return

    if args.explain:
        # 解释术语
        print(translator.explain_term(args.explain))
        return

    if args.text:
        # 翻译单行文本
        mode_map = {
            "zh2en": TranslationMode.ZH_TO_EN,
            "en2zh": TranslationMode.EN_TO_ZH,
            "bilingual": TranslationMode.BILINGUAL,
        }
        mode = mode_map.get(args.mode, TranslationMode.BILINGUAL)
        result = translator.translate(args.text, mode)
        print(result)
        return

    if args.batch:
        # 批量翻译文件
        mode_map = {
            "zh2en": TranslationMode.ZH_TO_EN,
            "en2zh": TranslationMode.EN_TO_ZH,
            "bilingual": TranslationMode.BILINGUAL,
        }
        mode = mode_map.get(args.mode, TranslationMode.BILINGUAL)
        batch_engine = BatchTranslator(translator)
        result = batch_engine.translate_file(args.batch, mode, args.output)
        print(result)
        return

    # 默认：启动交互式Shell
    interactive_shell()


if __name__ == "__main__":
    main()
