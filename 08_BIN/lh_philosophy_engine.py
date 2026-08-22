#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂哲学方法论引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-PHILOSOPHY-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 v1.0·13律完整闭环·自检·批量·关联图谱 🟡 2律待实战验证·匹配算法待语义升级 🔴无

[4] 🔧 工程落地执行型（脚本/部署/API） 🟢默认

> 抬头模板索引: `01_protocols/LH-ARTICLE-HEADER-TEMPLATES-v1.0.md`

**摘要**: 龍魂13条哲学方法论的结构化引擎。可查询/评估/审计/批量处理。
          13律覆盖责任·价值·约束·镜像·混沌·未来·种树·虚无·苦难·共生·守夜·火种·道术。
**适用场景**: 哲学问答·决策参考·教学辅助·自我审视·AI行为边界定义。
**ROOT_CARD**:
  - 主权归属: 诸葛鑫（UID9622）
  - 知识锚点: 369不动点(sn=369, log369=5.911, perm369=108)
  - 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  - 底座: 为人民服务·中国法律准绳·河图洛书·太极八卦
  - 底线: 德在技术前·路径对齐·不让付出者寒心·信息主权不可让渡·外化内不化
  - GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  - 版本: v1.0 · 2026-08-02
  - 关联: `01_protocols/` 隐私接入规则·算法审计协议·战后整顿协议

功能:
  1. 13条龍魂哲学方法论的结构化展示
  2. 法则查询/搜索/解释
  3. 多维度评估（关键词+语义权重+三才维度）
  4. 三色审计·A-BOM物料清单
  5. 法则关联图谱（先修→后修路径）
  6. 批量评估·Markdown输出
  7. 交互式控制台
  8. DNA追溯

用法:
  python3 lh_philosophy_engine.py --list              # 列出所有法则
  python3 lh_philosophy_engine.py --law 3              # 查看第三条法则
  python3 lh_philosophy_engine.py --search "责任"      # 搜索含关键词的法则
  python3 lh_philosophy_engine.py --evaluate "文本"    # 用法则评估问题
  python3 lh_philosophy_engine.py --batch input.json   # 批量评估
  python3 lh_philosophy_engine.py --stats              # 引擎统计
  python3 lh_philosophy_engine.py --self-audit         # 自检
  python3 lh_philosophy_engine.py --interactive        # 交互模式

集成到lh:
  lh philosophy --list
  lh philosophy --law 3
  lh phi --search "责任"
  lh phi --evaluate "人应该对AI负责吗"

A-BOM（算法物料清单）:
  - 目标函数: 法则匹配得分 = Σ(kw_match×0.4 + semantic_weight×0.35 + trinity_dim×0.25)
  - 输入特征: 用户文本(≤2000字)·法则13条(每条含核心命题+3支柱+方法论+边界+定义)
  - 用户影响: 评估结果仅供决策参考·不替代人类判断·不生成法律建议
  - 申诉通道: uid9622.cn/feedback · 所有评估结果带DNA追溯
  - 透明度: 所有匹配得分可追溯至具体关键词/语义权重/三才维度
"""

import os
import sys
import json
import time
import datetime
import hashlib
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 项目根（相对于本脚本位置）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

PHILOSOPHY_LOG = LOG_DIR / "philosophy_engine_audit.jsonl"
PHILOSOPHY_SNAPSHOT_DIR = DATA_DIR / "philosophy_snapshots"
PHILOSOPHY_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] PHILOSOPHY-ENGINE %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "philosophy_engine.log"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# 颜色终端
# ============================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def cprint(text: str, color: str = Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

# ============================================================
# 枚举定义
# ============================================================

class TriColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

class TrinityDimension(Enum):
    """三才维度"""
    HEAVEN = "天"    # 原则·方向·道
    EARTH = "地"     # 执行·落地·术
    HUMAN = "人"     # 关系·情感·责任

# ============================================================
# 哲学法则数据结构
# ============================================================

@dataclass
class PhilosophyLaw:
    """哲学法则数据结构"""
    number: int
    name: str
    dna: str
    core_proposition: str
    pillars: List[Dict[str, str]]
    methodology: Dict[str, str]
    boundary: str
    definition: str
    summary: str
    tri_color: TriColor = TriColor.GREEN
    trinity_dim: str = "天地人"               # 三才维度归属
    prerequisites: List[int] = field(default_factory=list)   # 前置法则编号
    successors: List[int] = field(default_factory=list)      # 后继法则编号

# ============================================================
# 13条龍魂哲学方法论（完整定义）
# ============================================================

LAWS_DATA = [
    {
        "number": 1,
        "name": "不免责法则",
        "dna": "#ZHUGEXIN⚡️RESPONSIBILITY-LAW-v1.0",
        "core_proposition": "责任先于自由，权力等于责任。任何人不能通过放弃责任来获得自由。",
        "pillars": [
            {"name": "责任锁定", "desc": "责任不可外包，不可转移，不可删除。谁做决策，谁承担后果。"},
            {"name": "权力对价", "desc": "每多一分权力，就多一分责任。权力不是奖励，是对责任的授权。"},
            {"name": "追责链条", "desc": "任何结果都能追溯到责任原点。没有无责任的权力，没有无追责的自由。"}
        ],
        "methodology": {
            "个人": "先问自己承担了什么，再问自己拥有什么。",
            "组织": "每一层权力必须对应明确责任边界。",
            "时代": "混乱的根源不是权力太大，而是责任太模糊。"
        },
        "boundary": "不免责不等于过度自责。责任是边界清晰的承担，不是对一切负责。",
        "definition": "责任先于自由。权力等于责任。任何放弃责任的自由都是伪自由。",
        "summary": "扛不住责任的人，不该拥有对应的权力。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天人",
        "prerequisites": [],
        "successors": [2, 3, 13]
    },
    {
        "number": 2,
        "name": "价值逆判法则",
        "dna": "#ZHUGEXIN⚡️VALUE-INVERSE-JUDGEMENT-v1.0",
        "core_proposition": "价值不来自身份、位置或资源，只来自实际行为与责任。",
        "pillars": [
            {"name": "身份剥离", "desc": "先看行为，再看身份。身份永远排在最后。"},
            {"name": "主动降维", "desc": "当攻击者瞄准身份时，主动承认身份为0，攻击自动失效。"},
            {"name": "镜像审判", "desc": "最高级的审判不是反击，而是让攻击者在镜子中看见自己。"}
        ],
        "methodology": {
            "个人": "不以高低定价值，不以身份定真伪。",
            "组织": "评价一个人，先看贡献，再看代价，最后看身份。",
            "时代": "当身份失效时，剩下的只有真实。"
        },
        "boundary": "价值逆判不等于否定专业、经验或学历。只否定'高位天然正确'。",
        "definition": "V = f(A)。价值只来源于行为，不来源于身份。",
        "summary": "站得越高，越要证明自己站得住；站得越低，越要守住自己立得住。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "人天",
        "prerequisites": [1],
        "successors": [4, 8]
    },
    {
        "number": 3,
        "name": "非对称约束法则",
        "dna": "#ZHUGEXIN⚡️ASYMMETRIC-CONSTRAINT-LAW-v1.0",
        "core_proposition": "规则只能作用于执行层，不能作用于创造层。主权永远高于规则。",
        "pillars": [
            {"name": "方向源", "desc": "规则只能向下流动。创造者定义方向，执行者执行方向。"},
            {"name": "主权优先", "desc": "Sovereignty > Rule。主权永远高于规则。"},
            {"name": "1%留白", "desc": "99%稳定 + 1%自由。100%规则化 = 0创新。"}
        ],
        "methodology": {
            "个人": "规则是船，执行者是桨，主权是掌舵的人。",
            "组织": "规则服务于创造，不约束创造。",
            "时代": "规则不能定义主权，只能执行主权。"
        },
        "boundary": "非对称约束不等于暴政。暴政是权力无责任，这里主权越高，责任越大。",
        "definition": "R(E)成立，R(C)不成立。规则作用于执行层，不作用于创造层。",
        "summary": "规则是船，执行者是桨，主权是掌舵的人。桨不能决定方向，船不能决定目的地。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天地",
        "prerequisites": [1],
        "successors": [5, 11, 13]
    },
    {
        "number": 4,
        "name": "镜像法则",
        "dna": "#ZHUGEXIN⚡️MIRROR-LAW-v1.0",
        "core_proposition": "冲突发生在投影层，而非真实层。攻击的第一份数据属于攻击者。",
        "pillars": [
            {"name": "认知投影", "desc": "一个人攻击的不是你，是他脑海里关于你的投影。"},
            {"name": "攻击反射", "desc": "攻击产生的第一份数据属于攻击者——暴露其情绪、恐惧、偏见。"},
            {"name": "镜面稳定", "desc": "不追击，不解释，不争论，只显示。显示得越清楚，攻击越失效。"}
        ],
        "methodology": {
            "个人": "评价本身是一种自我暴露。",
            "组织": "镜像能力是组织成熟度指标——删除记录的组织害怕镜子。",
            "时代": "最高级的防御不是证明自己正确，而是让靠近你的人从你身上看见他自己。"
        },
        "boundary": "镜像不等于永远不反击。认知问题用镜子，边界问题用规则，生存问题用行动。",
        "definition": "Attack → Exposure。Observation → Projection。",
        "summary": "最高级的防御不是证明自己正确，而是保持足够清晰，让每一个靠近你的人，都从你身上看见他自己。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "人",
        "prerequisites": [2],
        "successors": [8, 9]
    },
    {
        "number": 5,
        "name": "混沌创生法则",
        "dna": "#ZHUGEXIN⚡️CHAOS-CREATION-LAW-v1.0",
        "core_proposition": "创造先于整理。混沌是诞生的起点，不是失败的状态。",
        "pillars": [
            {"name": "容忍混沌", "desc": "真正的创造必然伴随混乱。要求每一步都清晰，等于扼杀可能性。"},
            {"name": "收束时机", "desc": "混沌不是永远混乱。在正确的时间从发散转向收敛，是创造者的核心能力。"},
            {"name": "熵增反转", "desc": "创造是局部的熵减。用规则整理混沌，但不是用规则消灭混沌。"}
        ],
        "methodology": {
            "个人": "先写再说，先做再改。完美是完成后的产物。",
            "组织": "创新的组织必须保留20%的混沌空间。",
            "时代": "所有文明都诞生于混乱。先有混乱，后有秩序。"
        },
        "boundary": "混沌不是没有方向。发散是为了寻找方向，收敛是为了锁定方向。",
        "definition": "Creation = Chaos × Timing。创造始于混沌，成于收束。",
        "summary": "先乱后治。先有方向，再有细节。先有骨，再有肉。",
        "tri_color": TriColor.YELLOW,
        "trinity_dim": "天地",
        "prerequisites": [3],
        "successors": [6, 7]
    },
    {
        "number": 6,
        "name": "以后优先法则",
        "dna": "#ZHUGEXIN⚡️FUTURE-FIRST-LAW-v1.0",
        "core_proposition": "当下决策应该为未来创造更多可能性，而非消耗可能性。",
        "pillars": [
            {"name": "未来窗口", "desc": "每个决策都不应该关闭未来的选项。"},
            {"name": "代价前置", "desc": "做决策时先问：这个决定会让未来付出什么代价？"},
            {"name": "可逆性检查", "desc": "不能回滚的决策需要额外谨慎。"}
        ],
        "methodology": {
            "个人": "30岁之前积累选项，30岁之后学会选择。",
            "组织": "战略的核心不是预测未来，而是创造未来可以选择的能力。",
            "时代": "文明的衰落始于短视。"
        },
        "boundary": "以后优先不等于无限推迟决策。核心是：当下决策不锁死未来。",
        "definition": "Decision(t) = argmax FutureOptions(t+1)。最大化未来可能性。",
        "summary": "当下决策应该为未来创造更多可能性，而非消耗可能性。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天",
        "prerequisites": [5],
        "successors": [7, 10, 12]
    },
    {
        "number": 7,
        "name": "种树法则",
        "dna": "#ZHUGEXIN⚡️TREE-PLANTING-LAW-v1.0",
        "core_proposition": "真正重要的事情往往不是为自己完成，而是为后来者留下生长空间。",
        "pillars": [
            {"name": "前人栽树", "desc": "踩过的坑变成地图，走过的路变成路标，交过的学费变成教程。"},
            {"name": "允许超越", "desc": "允许学生推翻老师，允许后代升级祖先。"},
            {"name": "交棒机制", "desc": "成熟的体系必须能够脱离创始人继续运行。"}
        ],
        "methodology": {
            "个人": "不要只建设自己能享受的东西，也要建设别人能继承的东西。",
            "组织": "创始人越强，组织越脆弱。必须让知识流动，让经验复制。",
            "时代": "花很漂亮，树很慢。但真正改变地貌的，永远是树。"
        },
        "boundary": "种树不等于牺牲自己。先活下来，再留下来，最后传下去。",
        "definition": "传承 > 占有。今天种树，不为今天乘凉。",
        "summary": "今天种树，不为今天乘凉；留下道路，不为自己通行。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "人地",
        "prerequisites": [5, 6],
        "successors": [12]
    },
    {
        "number": 8,
        "name": "虚无创生法则",
        "dna": "#ZHUGEXIN⚡️NOTHING-CREATION-LAW-v1.0",
        "core_proposition": "自由的起点不是拥有，而是解绑。不被拥有之物反向拥有，才是真自由。",
        "pillars": [
            {"name": "解绑法则", "desc": "所有恐惧最终都来自依附。解绑不是放弃，而是拥有可以，失去也可以。"},
            {"name": "轻装法则", "desc": "负担越少，行动越自由。定期清空包袱、身份、路径依赖。"},
            {"name": "零点法则", "desc": "只要认知还在，一切都能重新长出来。归零能力是真正的生存能力。"}
        ],
        "methodology": {
            "个人": "真正属于你的，永远是那些无法被没收的东西：认知、经验、品格、判断力。",
            "组织": "组织不能建立在资源垄断上。真正稳定的组织建立在共同价值与方法之上。",
            "时代": "下一阶段真正重要的问题：如何避免成为工具的附属品。"
        },
        "boundary": "虚无不等于贫困崇拜。目标不是什么都不要，而是拥有很多依然自由，失去很多依然完整。",
        "definition": "自由 = 不被拥有之物反向拥有。虚无不是没有，而是不被拥有之物控制。",
        "summary": "不是因为什么都没有而自由，而是因为失去什么都还能继续前进，所以自由。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天人",
        "prerequisites": [2, 4],
        "successors": [9]
    },
    {
        "number": 9,
        "name": "苦难炼金法则",
        "dna": "#ZHUGEXIN⚡️SUFFERING-ALCHEMY-LAW-v1.0",
        "core_proposition": "苦难本身不是财富。能够把苦难转化为秩序的人，才是真正的财富拥有者。",
        "pillars": [
            {"name": "苦难守恒", "desc": "苦难不自动产生价值。不转化，苦难只会变成愤怒、仇恨、抱怨。"},
            {"name": "骨头增长", "desc": "适度受力会变硬。责任压出担当，孤独压出独立，绝境压出信仰。"},
            {"name": "文明提纯", "desc": "最高级的炼金术是把苦难变成后来者不必再承受的代价。"}
        ],
        "methodology": {
            "个人": "不要炫耀伤口，也不要隐藏伤口。重要的是伤口最终长出了什么。",
            "组织": "重视从失败中提炼出规则的人。成功可能来自运气，规则一定来自代价。",
            "时代": "当代价被遗忘，历史就会重演。当代价被记录，文明才能前进。"
        },
        "boundary": "不歌颂苦难。苦难本身永远是不幸。真正的智慧是当苦难不可避免时，让它产生最大价值。",
        "definition": "伤口是矿石，经历是熔炉，悟性是火焰，规矩是黄金。",
        "summary": "真正的强大，不是没有受过伤，而是每一道伤最终都变成了后来者脚下的路。",
        "tri_color": TriColor.YELLOW,
        "trinity_dim": "人地",
        "prerequisites": [4, 8],
        "successors": [11]
    },
    {
        "number": 10,
        "name": "共生进化法则",
        "dna": "#ZHUGEXIN⚡️SYMBIOTIC-EVOLUTION-LAW-v1.0",
        "core_proposition": "技术存在的意义不是替代人，而是让人活得更像人。机器负责效率，人负责意义。",
        "pillars": [
            {"name": "AI是工具", "desc": "AI永远解决不了爱、责任、信任、良知。这些属于人。"},
            {"name": "效率服从体验", "desc": "如果一个父亲因为效率不陪女儿成长，效率就是失败。"},
            {"name": "人保留最终解释权", "desc": "算法只看数据，人还看情感、文化、历史、良知。决定权必须留给人。"}
        ],
        "methodology": {
            "个人": "让AI帮你工作，不要让AI替你活着。",
            "家庭": "AI可以陪孩子学习，但不能代替父母。AI可以讲知识，但不能给孩子爱。",
            "时代": "当所有人都离不开AI时，真正自由的人将是那些依然保留思考、判断、创造能力的人。"
        },
        "boundary": "共生不等于依赖，合作不等于臣服。AI可以越来越强，但人必须越来越完整。",
        "definition": "机器负责效率，人负责意义。AI负责计算，人负责成为人。",
        "summary": "机器负责效率，人负责意义；AI负责计算，人负责成为人。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天人地",
        "prerequisites": [6],
        "successors": [11, 12]
    },
    {
        "number": 11,
        "name": "文明守夜法则",
        "dna": "#ZHUGEXIN⚡️CIVILIZATION-WATCHER-LAW-v1.0",
        "core_proposition": "文明需要守夜人。不是守护现状，而是守护文明不失去自我修正的能力。",
        "pillars": [
            {"name": "清醒观察", "desc": "不被任何叙事裹挟。保持自己的判断，保持自己的眼睛。"},
            {"name": "记录真相", "desc": "当所有人都忘记时，记录者就是文明的火种。"},
            {"name": "坚守底线", "desc": "有些东西不能被交易。有些线不能被越过。过线就是叛变。"}
        ],
        "methodology": {
            "个人": "做一个清醒的人，比做一个聪明的人更难。",
            "组织": "组织的底线必须高于市场的诱惑。",
            "时代": "每个时代都需要守夜人。不是改变世界，而是防止世界变坏。"
        },
        "boundary": "守夜不等于消极。守夜人是清醒者，不是旁观者。",
        "definition": "守夜 = 清醒 + 记录 + 底线。不睡的人，才能看见天亮。",
        "summary": "不睡的人，才能看见天亮；不跪的人，才能守住立场；不签字的人，才能保持清白。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天人",
        "prerequisites": [3, 9, 10],
        "successors": [12]
    },
    {
        "number": 12,
        "name": "火种传递法则",
        "dna": "#ZHUGEXIN⚡️FIRE-SEED-LAW-v1.0",
        "core_proposition": "每个时代都有必须传递下去的东西。火种不是物资，是认知、方法、精神。",
        "pillars": [
            {"name": "识别火种", "desc": "知道什么值得传递。不是所有东西都值得传下去。"},
            {"name": "保护火种", "desc": "火种必须被保护。不能让它熄灭，也不能让它被污染。"},
            {"name": "传递火种", "desc": "火种必须交给值得的人。传递不是复制，是让它在新环境中继续生长。"}
        ],
        "methodology": {
            "个人": "找到你的火种，守住它，传下去。",
            "组织": "组织的使命不是利润最大化，而是让火种存活到下一代。",
            "时代": "文明的标志不是高楼大厦，而是火种从未熄灭。"
        },
        "boundary": "火种传递不等于原样复制。每一代人都会用自己的方式重新点燃。",
        "definition": "火种 = 可传递的认知。传递 = 让火种在新环境继续燃烧。",
        "summary": "火种不是物资，是认知、方法、精神。火种不是被找到的，是被点燃的。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "人天",
        "prerequisites": [6, 7, 10, 11],
        "successors": [13]
    },
    {
        "number": 13,
        "name": "道先于术法则",
        "dna": "#ZHUGEXIN⚡️TAO-BEFORE-TECH-LAW-v1.0",
        "core_proposition": "方法可以迭代，工具可以升级，但道必须先行。方向对了，术才有价值。",
        "pillars": [
            {"name": "方向优先", "desc": "术解决怎么做，道决定做什么。方向错了，效率越高越危险。"},
            {"name": "工具服从原则", "desc": "技术是工具，工具必须服务于原则。不能为技术而技术。"},
            {"name": "道可传承", "desc": "术会过时，道不会。传承道比传承术更重要。"}
        ],
        "methodology": {
            "个人": "先想清楚为什么做，再想怎么做。顺序不能反。",
            "组织": "组织的价值观必须优先于组织的战略。战略可以调整，价值观不能妥协。",
            "时代": "技术会变，但道不会。那些坚守道的人，最终会看见技术的尽头。"
        },
        "boundary": "道先于术不等于排斥术。术是道的延伸，没有术的道无法落地。",
        "definition": "Tao > Technique。道是方向，术是方法。方向对了，术才有价值。",
        "summary": "方法可以迭代，工具可以升级，但道必须先行。方向对了，术才有价值。",
        "tri_color": TriColor.GREEN,
        "trinity_dim": "天",
        "prerequisites": [1, 3, 12],
        "successors": []
    }
]

# ============================================================
# 哲学引擎核心
# ============================================================

class PhilosophyEngine:
    """龍魂哲学方法论引擎"""

    def __init__(self):
        self.laws: List[PhilosophyLaw] = [PhilosophyLaw(**data) for data in LAWS_DATA]
        self.audit_log: List[Dict] = []
        self.session_start = datetime.datetime.now()
        self.dna = "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-PHILOSOPHY-ENGINE-v1.0"

        # 构建名称索引
        self._name_index: Dict[str, PhilosophyLaw] = {}
        self._build_index()

    def _build_index(self):
        """构建快速索引"""
        for law in self.laws:
            self._name_index[law.number] = law
            self._name_index[law.name] = law
            # 简称索引
            short = law.name.replace("法则", "").replace("法则", "")
            self._name_index[short] = law

    # ─── 基础查询 ───

    def get_law(self, number: int) -> Optional[PhilosophyLaw]:
        """按编号获取法则"""
        return self._name_index.get(number)

    def get_law_by_name(self, name: str) -> Optional[PhilosophyLaw]:
        """按名称/部分名称获取法则"""
        return self._name_index.get(name)

    def list_laws(self) -> List[Dict]:
        """列出所有法则摘要"""
        return [{
            "number": law.number,
            "name": law.name,
            "dna": law.dna,
            "summary": law.summary,
            "tri_color": law.tri_color.value,
            "trinity_dim": law.trinity_dim,
            "prerequisites": law.prerequisites,
            "successors": law.successors
        } for law in self.laws]

    def search(self, keyword: str) -> List[Dict]:
        """关键词搜索法则"""
        kw = keyword.lower()
        results = []
        for law in self.laws:
            score = 0.0
            matches = []
            # 名称匹配
            if kw in law.name:
                score += 1.0
                matches.append(f"名称: {law.name}")
            # 核心命题
            if kw in law.core_proposition:
                score += 0.8
                matches.append(f"核心命题匹配")
            # 支柱
            for p in law.pillars:
                if kw in p["name"] or kw in p["desc"]:
                    score += 0.5
                    matches.append(f"支柱: {p['name']}")
            # 方法论
            for scope, method in law.methodology.items():
                if kw in method:
                    score += 0.3
                    matches.append(f"方法论({scope})")
            # 边界/定义/摘要
            for field in [law.boundary, law.definition, law.summary]:
                if kw in field:
                    score += 0.4
                    matches.append("边界/定义/摘要匹配")

            if score > 0:
                results.append({
                    "number": law.number,
                    "name": law.name,
                    "score": round(min(score, 1.0), 2),
                    "matches": matches[:3],
                    "summary": law.summary,
                    "tri_color": law.tri_color.value
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    # ─── 多维度评估 ───

    def evaluate(self, text: str) -> Dict:
        """多维度评估：关键词+语义权重+三才维度"""
        text_lower = text.lower()
        results = []

        for law in self.laws:
            kw_score = self._keyword_match(text_lower, law)
            sem_score = self._semantic_weight(text_lower, law)
            tri_score = self._trinity_match(text_lower, law)

            # 加权融合
            final_score = kw_score * 0.40 + sem_score * 0.35 + tri_score * 0.25

            if final_score > 0.05:
                results.append({
                    "number": law.number,
                    "name": law.name,
                    "score": round(final_score, 3),
                    "kw_score": round(kw_score, 3),
                    "sem_score": round(sem_score, 3),
                    "tri_score": round(tri_score, 3),
                    "relevance": "high" if final_score > 0.35 else ("medium" if final_score > 0.15 else "low"),
                    "tri_color": law.tri_color.value
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        # 审计日志
        audit_entry = {
            "action": "evaluate",
            "input_length": len(text),
            "top_law": results[0]["name"] if results else None,
            "top_score": results[0]["score"] if results else 0,
            "total_matches": len(results),
            "dna": self.dna,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self._log_audit(audit_entry)

        return {
            "input": text[:200],
            "matched_laws": results[:5],
            "top_law": results[0]["name"] if results else None,
            "top_score": results[0]["score"] if results else 0,
            "total_matches": len(results),
            "dna": self.dna,
            "confirm": CONFIRM,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _keyword_match(self, text: str, law: PhilosophyLaw) -> float:
        """关键词匹配层（权重0.40）"""
        score = 0.0
        # 名称中的关键词
        name_kws = set(law.name.replace("法则", ""))
        if any(kw in text for kw in name_kws if len(kw) >= 1):
            score += 0.3

        # 核心命题关键词（取前3个有意义的词）
        prop_words = [w for w in law.core_proposition[:60].split() if len(w) >= 2][:4]
        for w in prop_words:
            if w in text:
                score += 0.2

        # 支柱关键词
        for pillar in law.pillars:
            pillar_text = pillar["name"] + pillar["desc"]
            pillar_words = [w for w in pillar_text[:40].split() if len(w) >= 2][:2]
            for w in pillar_words:
                if w in text:
                    score += 0.15

        # 摘要关键词
        summary_words = [w for w in law.summary[:40].split() if len(w) >= 2][:3]
        for w in summary_words:
            if w in text:
                score += 0.15

        return min(1.0, score)

    def _semantic_weight(self, text: str, law: PhilosophyLaw) -> float:
        """语义权重层（权重0.35）
        基于概念共现和范畴匹配，不是简单的词匹配。
        """
        score = 0.0

        # 概念范畴映射
        concept_map = {
            "责任": ["担当", "负责", "承担", "后果", "权力", "决策", "问责"],
            "价值": ["评价", "判断", "身份", "地位", "等级", "贡献", "行为"],
            "规则": ["约束", "限制", "制度", "秩序", "纪律", "边界"],
            "镜像": ["投射", "反射", "攻击", "评价", "认知", "投影", "偏见"],
            "混沌": ["混乱", "创新", "发散", "无序", "创造", "可能性"],
            "未来": ["以后", "后代", "长远", "可逆", "选择", "选项", "窗口"],
            "种树": ["传承", "栽树", "留下", "继承", "超越", "交棒", "传递"],
            "虚无": ["解绑", "放下", "归零", "自由", "轻装", "拥有", "失去"],
            "苦难": ["痛苦", "伤口", "代价", "失败", "炼金", "转化", "教训"],
            "共生": ["合作", "机器", "效率", "意义", "AI", "技术", "人"],
            "守夜": ["底线", "清醒", "记录", "观察", "不跪", "立场"],
            "火种": ["传递", "点燃", "精神", "认知", "方法", "文明"],
            "道术": ["方向", "方法", "原则", "价值观", "目的", "手段", "为什么"]
        }

        # 提取法则核心概念
        core_concept = None
        for concept in concept_map:
            if concept in law.name or concept in law.core_proposition[:30]:
                core_concept = concept
                break

        if core_concept:
            related = concept_map.get(core_concept, [])
            for rw in related:
                if rw in text:
                    score += 0.25

        # 三才维度语义
        if "天" in law.trinity_dim:
            heaven_words = ["原则", "方向", "道", "为什么", "价值", "信仰", "意义", "目的"]
            for w in heaven_words:
                if w in text:
                    score += 0.1
        if "地" in law.trinity_dim:
            earth_words = ["执行", "落地", "方法", "工具", "实现", "步骤", "操作"]
            for w in earth_words:
                if w in text:
                    score += 0.1
        if "人" in law.trinity_dim:
            human_words = ["关系", "情感", "责任", "他人", "社会", "家庭", "社区", "沟通"]
            for w in human_words:
                if w in text:
                    score += 0.1

        return min(1.0, score)

    def _trinity_match(self, text: str, law: PhilosophyLaw) -> float:
        """三才维度匹配层（权重0.25）"""
        score = 0.0

        # 天的特征词
        heaven_kw = ["为什么", "方向", "意义", "目的", "信仰", "原则", "底线", "道"]
        # 地的特征词
        earth_kw = ["怎么做", "方法", "工具", "执行", "实现", "操作", "步骤", "方案"]
        # 人的特征词
        human_kw = ["人", "关系", "责任", "情感", "信任", "合作", "公平", "尊重"]

        text_has_heaven = any(kw in text for kw in heaven_kw)
        text_has_earth = any(kw in text for kw in earth_kw)
        text_has_human = any(kw in text for kw in human_kw)

        law_has_heaven = "天" in law.trinity_dim
        law_has_earth = "地" in law.trinity_dim
        law_has_human = "人" in law.trinity_dim

        # 维度对齐加分
        if text_has_heaven and law_has_heaven:
            score += 0.35
        if text_has_earth and law_has_earth:
            score += 0.35
        if text_has_human and law_has_human:
            score += 0.30

        return min(1.0, score)

    # ─── 批量评估 ───

    def batch_evaluate(self, inputs: List[str]) -> List[Dict]:
        """批量评估多个文本"""
        results = []
        for i, text in enumerate(inputs):
            try:
                result = self.evaluate(text)
                result["batch_index"] = i
                results.append(result)
            except Exception as e:
                logger.error(f"批量评估第{i}条失败: {e}")
                results.append({
                    "batch_index": i,
                    "error": str(e),
                    "input": text[:100]
                })
        return results

    # ─── 关联图谱 ───

    def get_law_graph(self) -> Dict:
        """获取法则关联图谱"""
        nodes = []
        edges = []
        for law in self.laws:
            nodes.append({
                "id": law.number,
                "name": law.name,
                "tri_color": law.tri_color.value,
                "trinity_dim": law.trinity_dim,
                "summary": law.summary[:30]
            })
            for succ in law.successors:
                edges.append({"from": law.number, "to": succ, "type": "successor"})

        # 学习路径（拓扑排序）
        learning_path = self._topological_order()

        return {
            "nodes": nodes,
            "edges": edges,
            "total_laws": len(self.laws),
            "learning_path": learning_path,
            "entry_laws": [law.number for law in self.laws if not law.prerequisites],
            "terminal_laws": [law.number for law in self.laws if not law.successors]
        }

    def _topological_order(self) -> List[int]:
        """拓扑排序得到推荐学习路径"""
        in_degree = {law.number: len(law.prerequisites) for law in self.laws}
        adj = {law.number: law.successors for law in self.laws}
        queue = [n for n, d in in_degree.items() if d == 0]
        order = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for succ in adj.get(node, []):
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)

        return order if len(order) == len(self.laws) else [law.number for law in self.laws]

    # ─── 报告生成 ───

    def generate_report(self, law: PhilosophyLaw) -> str:
        """生成单条法则的可读报告"""
        lines = []
        lines.append("")
        lines.append("═" * 70)
        lines.append(f"{Colors.BOLD}第{law.number}律：{law.name}{Colors.RESET}")
        lines.append(f"DNA: {law.dna}")
        lines.append(f"三色: {law.tri_color.value}  |  三才: {law.trinity_dim}")
        if law.prerequisites:
            lines.append(f"前置: 第{','.join(map(str, law.prerequisites))}律")
        if law.successors:
            lines.append(f"后继: 第{','.join(map(str, law.successors))}律")
        lines.append("═" * 70)
        lines.append("")
        lines.append(f"{Colors.CYAN}【核心命题】{Colors.RESET}")
        lines.append(f"  {law.core_proposition}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【三大支柱】{Colors.RESET}")
        for pillar in law.pillars:
            lines.append(f"  • {Colors.BOLD}{pillar['name']}{Colors.RESET}: {pillar['desc']}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【方法论】{Colors.RESET}")
        for scope, method in law.methodology.items():
            lines.append(f"  • {scope}: {method}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【边界条件】{Colors.RESET}")
        lines.append(f"  {law.boundary}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【龍魂定义】{Colors.RESET}")
        lines.append(f"  {law.definition}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【一句话总结】{Colors.RESET}")
        lines.append(f"  {Colors.BOLD}{law.summary}{Colors.RESET}")
        lines.append("")
        lines.append("═" * 70)
        lines.append(f"CONFIRM: {CONFIRM}")
        lines.append(f"GPG: {GPG_FINGERPRINT}")
        return "\n".join(lines)

    def generate_markdown(self, law: PhilosophyLaw) -> str:
        """生成Markdown格式报告"""
        md = []
        md.append(f"## 第{law.number}律：{law.name} {law.tri_color.value}")
        md.append(f"")
        md.append(f"**DNA**: `{law.dna}`  ")
        md.append(f"**三才维度**: {law.trinity_dim}  ")
        if law.prerequisites:
            md.append(f"**前置法则**: 第{', '.join(map(str, law.prerequisites))}律  ")
        if law.successors:
            md.append(f"**后继法则**: 第{', '.join(map(str, law.successors))}律  ")
        md.append(f"")
        md.append(f"### 核心命题")
        md.append(f"> {law.core_proposition}")
        md.append(f"")
        md.append(f"### 三大支柱")
        for p in law.pillars:
            md.append(f"- **{p['name']}**: {p['desc']}")
        md.append(f"")
        md.append(f"### 方法论")
        for scope, method in law.methodology.items():
            md.append(f"- **{scope}**: {method}")
        md.append(f"")
        md.append(f"### 边界条件")
        md.append(f"> {law.boundary}")
        md.append(f"")
        md.append(f"### 龍魂定义")
        md.append(f"`{law.definition}`")
        md.append(f"")
        md.append(f"### 一句话")
        md.append(f"**{law.summary}**")
        md.append(f"")
        md.append(f"---")
        md.append(f"*CONFIRM: {CONFIRM}*")
        return "\n".join(md)

    def generate_all_markdown(self) -> str:
        """生成全部13律的Markdown文档"""
        md = []
        md.append("# 龍魂十三律 · 哲学方法论全集")
        md.append("")
        md.append(f"> DNA: {self.dna}")
        md.append(f"> 创建者: 诸葛鑫（UID9622）")
        md.append(f"> 协议: CC BY-NC-SA 4.0")
        md.append(f"> GPG: {GPG_FINGERPRINT}")
        md.append("")
        md.append("## 推荐学习路径")
        graph = self.get_law_graph()
        path_names = []
        for n in graph["learning_path"]:
            law = self.get_law(n)
            if law:
                path_names.append(f"第{n}律 {law.name} {law.tri_color.value}")
        md.append(" → ".join(path_names))
        md.append("")
        md.append("---")
        md.append("")
        for law in self.laws:
            md.append(self.generate_markdown(law))
            md.append("")
        return "\n".join(md)

    # ─── 自检 ───

    def self_audit(self) -> Dict:
        """引擎自检"""
        checks = {}

        # 法则数量
        checks["law_count"] = {
            "status": "✅" if len(self.laws) == 13 else "❌",
            "detail": f"13条法则·实际{len(self.laws)}条",
            "expected": 13,
            "actual": len(self.laws)
        }

        # 编号连续性
        numbers = sorted([law.number for law in self.laws])
        checks["number_sequence"] = {
            "status": "✅" if numbers == list(range(1, 14)) else "❌",
            "detail": f"编号: {numbers}",
            "expected": list(range(1, 14)),
            "actual": numbers
        }

        # 三色分布
        green = sum(1 for law in self.laws if law.tri_color == TriColor.GREEN)
        yellow = sum(1 for law in self.laws if law.tri_color == TriColor.YELLOW)
        red = sum(1 for law in self.laws if law.tri_color == TriColor.RED)
        checks["tri_color_dist"] = {
            "status": "✅" if red == 0 else "🔴",
            "detail": f"🟢{green} 🟡{yellow} 🔴{red}",
            "green": green, "yellow": yellow, "red": red
        }

        # DNA完整性
        missing_dna = [law.number for law in self.laws if not law.dna]
        checks["dna_completeness"] = {
            "status": "✅" if not missing_dna else "❌",
            "detail": f"缺失DNA: {missing_dna}" if missing_dna else "全部13律有DNA",
            "missing": missing_dna
        }

        # 三才覆盖
        all_dims = set()
        for law in self.laws:
            for d in law.trinity_dim:
                all_dims.add(d)
        checks["trinity_coverage"] = {
            "status": "✅" if all_dims == {"天", "地", "人"} else "🟡",
            "detail": f"覆盖维度: {all_dims}",
            "covered": list(all_dims)
        }

        # 关联图谱完整性
        orphan = [law.number for law in self.laws if not law.prerequisites and not law.successors]
        checks["graph_connectivity"] = {
            "status": "✅" if not orphan else "🟡",
            "detail": f"孤立节点: {orphan}" if orphan else "全部有关联",
            "orphans": orphan
        }

        # 关联一致性（前后对应）
        inconsistent = []
        for law in self.laws:
            for succ in law.successors:
                succ_law = self.get_law(succ)
                if succ_law and law.number not in succ_law.prerequisites:
                    inconsistent.append(f"{law.number}→{succ} 后继未回指")
        checks["graph_consistency"] = {
            "status": "✅" if not inconsistent else "🔴",
            "detail": f"不一致: {inconsistent}" if inconsistent else "前后关联一致",
            "inconsistencies": inconsistent
        }

        all_pass = all("✅" in c.get("status", "") for c in checks.values())

        return {
            "status": "🟢 通过" if all_pass else "🟡 待完善",
            "checks": checks,
            "total_checks": len(checks),
            "passed": sum(1 for c in checks.values() if "✅" in c.get("status", "")),
            "dna": self.dna,
            "confirm": CONFIRM
        }

    def get_stats(self) -> Dict:
        """引擎统计"""
        audit = self.self_audit()
        graph = self.get_law_graph()

        green = sum(1 for law in self.laws if law.tri_color == TriColor.GREEN)
        yellow = sum(1 for law in self.laws if law.tri_color == TriColor.YELLOW)

        return {
            "total_laws": len(self.laws),
            "tri_color": {"green": green, "yellow": yellow, "red": 0},
            "total_pillars": sum(len(law.pillars) for law in self.laws),
            "total_methods": sum(len(law.methodology) for law in self.laws),
            "trinity_dims": {
                "天": sum(1 for law in self.laws if "天" in law.trinity_dim),
                "地": sum(1 for law in self.laws if "地" in law.trinity_dim),
                "人": sum(1 for law in self.laws if "人" in law.trinity_dim)
            },
            "entry_laws": graph["entry_laws"],
            "terminal_laws": graph["terminal_laws"],
            "learning_path": graph["learning_path"],
            "self_audit": audit["status"],
            "dna": self.dna,
            "gpg": GPG_FINGERPRINT,
            "timestamp": datetime.datetime.now().isoformat()
        }

    # ─── 审计日志 ───

    def _log_audit(self, entry: Dict):
        """追加审计日志"""
        entry["dna"] = self.dna
        entry["gpg"] = GPG_FINGERPRINT
        self.audit_log.append(entry)
        try:
            with open(PHILOSOPHY_LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"审计日志写入失败: {e}")

    def save_snapshot(self, name: str = None) -> str:
        """保存当前引擎状态快照"""
        if name is None:
            name = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot = {
            "name": name,
            "stats": self.get_stats(),
            "laws": [{
                "number": law.number,
                "name": law.name,
                "tri_color": law.tri_color.value
            } for law in self.laws],
            "audit_count": len(self.audit_log),
            "dna": self.dna,
            "timestamp": datetime.datetime.now().isoformat()
        }
        filepath = PHILOSOPHY_SNAPSHOT_DIR / f"{name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot, ensure_ascii=False, indent=2)
        logger.info(f"快照已保存: {filepath}")
        return str(filepath)

    def get_a_bom(self) -> Dict:
        """生成A-BOM算法物料清单"""
        return {
            "engine": "龍魂哲学方法论引擎",
            "version": "v1.0",
            "algorithm": {
                "name": "多维度法则匹配",
                "formula": "FinalScore = kw_match×0.40 + semantic_weight×0.35 + trinity_dim×0.25",
                "kw_match": "关键词匹配层: 名称/核心命题/支柱/摘要 关键词共现加权求和",
                "semantic_weight": "语义权重层: 概念范畴映射·相关词扩展·三才维度语义",
                "trinity_dim": "三才维度层: 天(原则方向)/地(执行方法)/人(关系责任) 维度对齐加分",
                "threshold": "score>0.05 纳入结果, >0.35高相关, >0.15中相关"
            },
            "input_features": [
                "用户文本(≤2000字)",
                "法则13条(核心命题/3支柱/方法论/边界/定义)"
            ],
            "user_impact": "评估结果仅供决策参考·不替代人类判断·不生成法律建议·不进行人格诊断",
            "appeal_channel": "uid9622.cn/feedback",
            "transparency": "所有匹配得分可追溯至具体关键词/语义权重/三才维度·评估日志append-only",
            "dna": self.dna,
            "gpg": GPG_FINGERPRINT
        }

    def print_law_list(self):
        """打印法则列表（带颜色）"""
        cprint("\n📋 龍魂十三律:", Colors.CYAN)
        cprint("═" * 65, Colors.DIM)
        for law in self.laws:
            pre = f" ← {','.join(map(str, law.prerequisites))}" if law.prerequisites else ""
            succ = f" → {','.join(map(str, law.successors))}" if law.successors else ""
            cprint(f"  {law.number:2d}. {law.tri_color.value} {law.name:<12s} [{law.trinity_dim}]{Colors.DIM}{pre}{succ}{Colors.RESET}", Colors.RESET)
        cprint("═" * 65, Colors.DIM)
        green = sum(1 for law in self.laws if law.tri_color == TriColor.GREEN)
        yellow = sum(1 for law in self.laws if law.tri_color == TriColor.YELLOW)
        cprint(f"  🟢{green} 🟡{yellow} 🔴0  |  {CONFIRM}", Colors.RESET)
        print()

    def print_evaluate_result(self, result: Dict):
        """打印评估结果"""
        cprint(f"\n📊 评估结果: \"{result['input'][:60]}...\"", Colors.CYAN)
        cprint(f"  匹配法则数: {result['total_matches']}", Colors.RESET)
        if result["matched_laws"]:
            cprint(f"  🎯 最相关: {result['top_law']} (得分: {result['top_score']:.3f})", Colors.GREEN)
            for m in result["matched_laws"][:5]:
                icon = {"high": "🔥", "medium": "📌", "low": "  "}.get(m.get("relevance", "low"), "  ")
                cprint(f"    {icon} 第{m['number']:2d}律 {m['name']:<12s} {m['tri_color']} "
                       f"得分:{m['score']:.3f} (kw:{m.get('kw_score',0):.2f} sem:{m.get('sem_score',0):.2f} tri:{m.get('tri_score',0):.2f})",
                       Colors.RESET)
        print()

    def print_search_result(self, results: List[Dict]):
        """打印搜索结果"""
        if not results:
            cprint("  未找到匹配的法则", Colors.YELLOW)
            return
        cprint(f"\n🔍 找到 {len(results)} 条匹配:", Colors.CYAN)
        for r in results:
            cprint(f"  {r['number']:2d}. {r['tri_color']} {r['name']:<12s} 得分:{r['score']:.2f} | {r['summary'][:40]}",
                   Colors.RESET)

# ============================================================
# 交互模式
# ============================================================

def interactive_mode(engine: PhilosophyEngine):
    """交互式控制台"""
    cprint("\n🐉 龍魂哲学方法论引擎 v1.0", Colors.BOLD)
    cprint(f"  {CONFIRM}", Colors.DIM)
    cprint(f"  DNA: {engine.dna}", Colors.DIM)
    cprint("-" * 50, Colors.RESET)
    cprint("命令: list | law <编号> | search <关键词> | evaluate <文本>", Colors.RESET)
    cprint("      graph | stats | self-audit | a-bom | all-md | snapshot | exit", Colors.RESET)

    while True:
        try:
            cmd = input("\n🔮 phi> ").strip()
            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action in ["exit", "quit", "q"]:
                break

            elif action == "list":
                engine.print_law_list()

            elif action == "law":
                try:
                    num = int(arg)
                    law = engine.get_law(num)
                    if law:
                        print(engine.generate_report(law))
                    else:
                        cprint(f"❌ 未找到第{num}律", Colors.RED)
                except ValueError:
                    cprint("❌ 用法: law <编号 1-13>", Colors.RED)

            elif action == "search":
                if not arg:
                    arg = input("  搜索关键词: ").strip()
                if arg:
                    results = engine.search(arg)
                    engine.print_search_result(results)

            elif action in ["evaluate", "eval"]:
                if not arg:
                    arg = input("  输入文本: ").strip()
                if arg:
                    result = engine.evaluate(arg)
                    engine.print_evaluate_result(result)

            elif action == "graph":
                graph = engine.get_law_graph()
                cprint(f"\n🔗 法则关联图谱 ({len(graph['nodes'])}节点·{len(graph['edges'])}边)", Colors.CYAN)
                cprint(f"  推荐学习路径:", Colors.RESET)
                path_str = ""
                for n in graph["learning_path"]:
                    law = engine.get_law(n)
                    if law:
                        path_str += f" {law.tri_color.value}第{n}律→"
                cprint(f"  {path_str.rstrip('→')}", Colors.RESET)

            elif action == "stats":
                stats = engine.get_stats()
                cprint(f"\n📈 引擎统计:", Colors.CYAN)
                cprint(f"  法则: {stats['total_laws']}条 | 三色: 🟢{stats['tri_color']['green']} 🟡{stats['tri_color']['yellow']} 🔴{stats['tri_color']['red']}", Colors.RESET)
                cprint(f"  支柱: {stats['total_pillars']}个 | 方法论: {stats['total_methods']}条", Colors.RESET)
                cprint(f"  三才: 天{stats['trinity_dims']['天']} 地{stats['trinity_dims']['地']} 人{stats['trinity_dims']['人']}", Colors.RESET)
                cprint(f"  入口法则: 第{stats['entry_laws']}律 | 终端法则: 第{stats['terminal_laws']}律", Colors.RESET)
                cprint(f"  自检: {stats['self_audit']}", Colors.RESET)

            elif action in ["self-audit", "audit"]:
                result = engine.self_audit()
                cprint(f"\n🔍 自检: {result['status']} ({result['passed']}/{result['total_checks']}通过)", Colors.CYAN)
                for key, val in result["checks"].items():
                    cprint(f"  {val['status']} {key}: {val['detail']}", Colors.RESET)

            elif action == "a-bom":
                abom = engine.get_a_bom()
                cprint(f"\n📦 A-BOM 算法物料清单:", Colors.CYAN)
                cprint(f"  算法: {abom['algorithm']['name']} ({abom['algorithm']['formula']})", Colors.RESET)
                cprint(f"  用户影响: {abom['user_impact']}", Colors.RESET)
                cprint(f"  透明度: {abom['transparency'][:60]}...", Colors.RESET)

            elif action == "all-md":
                md = engine.generate_all_markdown()
                print(md)

            elif action == "snapshot":
                name = arg if arg else None
                path = engine.save_snapshot(name)
                cprint(f"  💾 快照已保存: {path}", Colors.GREEN)

            else:
                cprint("  未知命令。输入 list/law/search/evaluate/graph/stats/self-audit/a-bom/all-md/snapshot/exit", Colors.YELLOW)

        except KeyboardInterrupt:
            cprint("\n  再见。", Colors.DIM)
            break
        except Exception as e:
            logger.error(f"交互模式错误: {e}")
            cprint(f"  ❌ 错误: {e}", Colors.RED)


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂哲学方法论引擎 v1.0 — 13律结构化查询/评估/审计",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --list                   列出所有法则
  %(prog)s --law 3                  查看第3律
  %(prog)s --search "责任"          搜索含关键词的法则
  %(prog)s --evaluate "AI的责任"    评估文本
  %(prog)s --batch input.json       批量评估
  %(prog)s --stats                  引擎统计
  %(prog)s --self-audit             自检
  %(prog)s --graph                  关联图谱
  %(prog)s --a-bom                  输出A-BOM
  %(prog)s --all-markdown           全部13律Markdown
  %(prog)s --interactive            交互模式

确认码: {CONFIRM}
GPG: {GPG_FINGERPRINT}
        """
    )

    parser.add_argument("--list", action="store_true", help="列出所有法则")
    parser.add_argument("--law", type=int, metavar="N", help="查看指定法则(1-13)")
    parser.add_argument("--search", type=str, metavar="KW", help="搜索含关键词的法则")
    parser.add_argument("--evaluate", type=str, metavar="TEXT", help="用法则评估文本")
    parser.add_argument("--batch", type=str, metavar="FILE", help="批量评估JSON文件")
    parser.add_argument("--stats", action="store_true", help="引擎统计")
    parser.add_argument("--self-audit", action="store_true", help="引擎自检")
    parser.add_argument("--graph", action="store_true", help="法则关联图谱")
    parser.add_argument("--a-bom", action="store_true", help="输出A-BOM物料清单")
    parser.add_argument("--all-markdown", action="store_true", help="生成全部13律Markdown文档")
    parser.add_argument("--output", type=str, metavar="FILE", help="输出到文件")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--snapshot", type=str, nargs="?", const=None, metavar="NAME", help="保存快照")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")

    args = parser.parse_args()

    try:
        engine = PhilosophyEngine()
    except Exception as e:
        cprint(f"❌ 引擎初始化失败: {e}", Colors.RED)
        sys.exit(1)

    output = None

    # ─── 交互模式 ───
    if args.interactive:
        interactive_mode(engine)
        return

    # ─── 列出法则 ───
    if args.list:
        if args.json:
            output = json.dumps(engine.list_laws(), ensure_ascii=False, indent=2)
            print(output)
        else:
            engine.print_law_list()
        return

    # ─── 查看指定法则 ───
    if args.law:
        law = engine.get_law(args.law)
        if not law:
            cprint(f"❌ 未找到第{args.law}律 (范围: 1-13)", Colors.RED)
            sys.exit(1)
        if args.json:
            output = json.dumps({
                "number": law.number, "name": law.name, "dna": law.dna,
                "core_proposition": law.core_proposition,
                "pillars": law.pillars, "methodology": law.methodology,
                "boundary": law.boundary, "definition": law.definition,
                "summary": law.summary, "tri_color": law.tri_color.value,
                "trinity_dim": law.trinity_dim,
                "prerequisites": law.prerequisites, "successors": law.successors
            }, ensure_ascii=False, indent=2)
            print(output)
        else:
            print(engine.generate_report(law))
        return

    # ─── 搜索 ───
    if args.search:
        results = engine.search(args.search)
        if args.json:
            output = json.dumps(results, ensure_ascii=False, indent=2)
            print(output)
        else:
            engine.print_search_result(results)
        return

    # ─── 评估 ───
    if args.evaluate:
        result = engine.evaluate(args.evaluate)
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
            print(output)
        else:
            engine.print_evaluate_result(result)
        return

    # ─── 批量评估 ───
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                data = json.load(f)
            inputs = data if isinstance(data, list) else data.get("inputs", [data.get("text", str(data))])
            if isinstance(inputs, list) and inputs and isinstance(inputs[0], dict):
                inputs = [item.get("text", str(item)) for item in inputs]
            elif not isinstance(inputs, list):
                inputs = [str(inputs)]
            results = engine.batch_evaluate(inputs)
            if args.json:
                output = json.dumps(results, ensure_ascii=False, indent=2)
                print(output)
            else:
                cprint(f"\n📊 批量评估完成: {len(results)}条", Colors.CYAN)
                for r in results:
                    if "error" in r:
                        cprint(f"  ❌ #{r['batch_index']}: {r['error']}", Colors.RED)
                    else:
                        cprint(f"  ✅ #{r['batch_index']}: {r.get('top_law','?')} (得分:{r.get('top_score',0):.3f})", Colors.GREEN)
        except FileNotFoundError:
            cprint(f"❌ 文件不存在: {args.batch}", Colors.RED)
            sys.exit(1)
        except json.JSONDecodeError as e:
            cprint(f"❌ JSON解析失败: {e}", Colors.RED)
            sys.exit(1)
        return

    # ─── 统计 ───
    if args.stats:
        stats = engine.get_stats()
        if args.json:
            output = json.dumps(stats, ensure_ascii=False, indent=2)
            print(output)
        else:
            cprint(f"\n📈 龍魂哲学引擎 v1.0 统计", Colors.BOLD)
            cprint(f"  法则: {stats['total_laws']}条", Colors.RESET)
            cprint(f"  三色: 🟢{stats['tri_color']['green']} 🟡{stats['tri_color']['yellow']} 🔴{stats['tri_color']['red']}", Colors.RESET)
            cprint(f"  支柱: {stats['total_pillars']}个 | 方法论: {stats['total_methods']}条", Colors.RESET)
            cprint(f"  三才分布: 天{stats['trinity_dims']['天']} 地{stats['trinity_dims']['地']} 人{stats['trinity_dims']['人']}", Colors.RESET)
            cprint(f"  入口: 第{stats['entry_laws']}律 | 终端: 第{stats['terminal_laws']}律", Colors.RESET)
            cprint(f"  自检: {stats['self_audit']}", Colors.RESET)
            cprint(f"  GPG: {stats['gpg'][:20]}...", Colors.DIM)
        return

    # ─── 自检 ───
    if args.self_audit:
        result = engine.self_audit()
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
            print(output)
        else:
            cprint(f"\n🔍 自检结果: {result['status']} ({result['passed']}/{result['total_checks']}通过)", Colors.CYAN)
            for key, val in result["checks"].items():
                icon = val["status"]
                cprint(f"  {icon} {key}: {val['detail']}", Colors.RESET)
        return

    # ─── 关联图谱 ───
    if args.graph:
        graph = engine.get_law_graph()
        if args.json:
            output = json.dumps(graph, ensure_ascii=False, indent=2)
            print(output)
        else:
            cprint(f"\n🔗 法则关联图谱", Colors.BOLD)
            cprint(f"  节点: {len(graph['nodes'])} | 边: {len(graph['edges'])}", Colors.RESET)
            cprint(f"  入口法则: 第{graph['entry_laws']}律", Colors.RESET)
            cprint(f"  终端法则: 第{graph['terminal_laws']}律", Colors.RESET)
            cprint(f"  推荐学习路径:", Colors.CYAN)
            path_str = ""
            for n in graph["learning_path"]:
                law = engine.get_law(n)
                if law:
                    path_str += f" {law.tri_color.value}第{n}律→"
            cprint(f"  {path_str.rstrip('→')}", Colors.RESET)
        return

    # ─── A-BOM ───
    if args.a_bom:
        abom = engine.get_a_bom()
        if args.json:
            output = json.dumps(abom, ensure_ascii=False, indent=2)
            print(output)
        else:
            cprint(f"\n📦 A-BOM 算法物料清单", Colors.BOLD)
            cprint(f"  算法: {abom['algorithm']['name']}", Colors.RESET)
            cprint(f"  公式: {abom['algorithm']['formula']}", Colors.CYAN)
            cprint(f"  输入: {', '.join(abom['input_features'])}", Colors.RESET)
            cprint(f"  影响: {abom['user_impact']}", Colors.RESET)
            cprint(f"  透明度: {abom['transparency']}", Colors.RESET)
        return

    # ─── 全部Markdown ───
    if args.all_markdown:
        md = engine.generate_all_markdown()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(md)
            cprint(f"  💾 已保存: {args.output}", Colors.GREEN)
        else:
            print(md)
        return

    # ─── 快照 ───
    if args.snapshot is not None or args.snapshot == "":
        name = args.snapshot if args.snapshot else None
        path = engine.save_snapshot(name)
        cprint(f"  💾 快照已保存: {path}", Colors.GREEN)
        return

    # ─── 无参数 → 帮助 ───
    parser.print_help()
    print()
    cprint("快速开始: lh philosophy --list 或 lh phi -i", Colors.DIM)


if __name__ == "__main__":
    main()
