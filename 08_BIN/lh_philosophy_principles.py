#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·乙巳·癸酉·☰乾-PHILOSOPHY-PRINCIPLES-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）

══════════════════════════════════════════════════════════════
 🔧 工程落地执行型
══════════════════════════════════════════════════════════════
 原则: 只写能跑的代码·每个区块都有明确边界·不凭空发明
 场景: 脚本/CLI工具/系统引擎
 输出: 六大原理引擎·可执行·可审计·可传承
══════════════════════════════════════════════════════════════
 项目: 龍魂系统-六大哲学原理引擎 v1.0
 创建: 诸葛鑫（UID9622）· 2026-08-02
 路径: bin/lh_philosophy_principles.py
 协议: CC BY-NC-SA 4.0
 数字根: sn=369, log369=5.911, perm369=108
══════════════════════════════════════════════════════════════
 六不铁律·不免责/不覆盖/不代签/不断链/不失真/不夺权
 六原理形成完整闭环·不可割裂·按序学习·逐层叠加
 十三律(via lh phi)是方法论·六大原理(via lh 6p)是地基
══════════════════════════════════════════════════════════════
 CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 SEAL: #ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队
 GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
══════════════════════════════════════════════════════════════

🐉 龍魂哲学 · 六大原理引擎 v1.0

功能:
  1. 六大哲学原理完整结构化展示（起源·六支柱·推论·边界·应用）
  2. 多维度评估（关键词+语义权重+三才维度）
  3. 三色审计·DNA追溯·A-BOM·审计日志
  4. 关联图谱·学习路径·自检
  5. 批量·搜索·Markdown输出·快照·交互式

用法:
  python3 lh_philosophy_principles.py --list          # 列出所有原理
  python3 lh_philosophy_principles.py -p 1            # 查看第一原理
  python3 lh_philosophy_principles.py -e "文本"       # 评估匹配度
  python3 lh_philosophy_principles.py --search "责任"  # 搜索
  python3 lh_philosophy_principles.py --graph          # 关联图谱
  python3 lh_philosophy_principles.py --stats          # 统计
  python3 lh_philosophy_principles.py --self-audit     # 自检
  python3 lh_philosophy_principles.py --a-bom          # A-BOM
  python3 lh_philosophy_principles.py -i               # 交互模式

集成到 lh:
  lh 6p --list
  lh principles -p 1
  lh 6p --interactive
"""

import os
import sys
import json
import time
import datetime
import hashlib
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import deque

# ═══════════════════════════════════════════════════════════════
# 固定锚点
# ═══════════════════════════════════════════════════════════════

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DIGITAL_ROOT = {"sn": 369, "log369": 5.911, "perm369": 108}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "philosophy_principles_snapshots"
AUDIT_LOG = LOG_DIR / "philosophy_principles_audit.jsonl"

for d in [LOG_DIR, DATA_DIR, SNAPSHOT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 日志：append-only 不覆盖
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "philosophy_principles.log"), logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("philosophy_principles")

# ═══════════════════════════════════════════════════════════════
# 颜色终端
# ═══════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════
# 三色审计
# ═══════════════════════════════════════════════════════════════

class TriColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

# ═══════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class PhilosophyPrinciple:
    """六大哲学原理数据结构"""
    number: int
    name: str
    dna: str
    core_definition: str
    origin: str
    pillars: List[Dict[str, str]]
    corollaries: List[str]
    boundary: str
    final_definition: str
    summary: str
    tri_color: TriColor = TriColor.GREEN
    applications: Optional[Dict[str, str]] = None
    trinity_dim: str = "天地人"          # 三才维度归属
    semantic_category: str = ""           # 语义范畴
    prerequisite: List[int] = field(default_factory=list)   # 前置原理
    successor: List[int] = field(default_factory=list)       # 后继原理
    key_concepts: List[str] = field(default_factory=list)    # 核心概念关键词

# ═══════════════════════════════════════════════════════════════
# 六大哲学原理完整数据
# ═══════════════════════════════════════════════════════════════

PRINCIPLES_DATA = [
    {
        "number": 1,
        "name": "不免责法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NON-EXEMPTION-LAW-v1.0",
        "core_definition": "行为产生结果，结果产生记录，记录产生责任，责任不可凭意志消失。",
        "origin": "宇宙不会因为解释而改变结果。时间不会因为借口而停止流动。历史不会因为删除而消失。因此，真正的责任从来不是别人赋予的，而是自己选择承担的。",
        "pillars": [
            {"name": "自锁原则", "desc": "行动之前先锁自己。确认 > 执行 > 解释。先确认，先留痕，先签名，再执行。"},
            {"name": "留痕原则", "desc": "发生过的事情永远发生过。删除不能改变发生，覆盖不能改变发生，遗忘不能改变发生。存在 = 留痕。"},
            {"name": "承担原则", "desc": "承担不是认输，不是低头。承担是：我做的我认，我说的我认，我签的我认。责任首先面对的不是别人，而是自己。"},
            {"name": "修正原则", "desc": "龍魂禁止两种极端：犯错后隐藏，或犯错后自毁。正确道路：犯错→记录→分析→修正→保留痕迹。错误不是污点，是成长数据。"},
            {"name": "时间原则", "desc": "时间 > 解释。今天的解释可能改变，今天的立场可能改变，今天的情绪可能改变。但时间线不会改变。时间拥有最高审计权。"},
            {"name": "自由原则", "desc": "真正束缚人的不是责任，而是不愿承担责任。害怕承担的人必须不断解释、掩饰、防御、讨好。承担的人反而自由。责任→信任→自由。"}
        ],
        "corollaries": [
            "如果一个系统允许无限免责，责任消失，信用崩塌，规则失效，组织腐烂。",
            "如果一个系统允许记录存在、责任存在、修正存在，系统会越来越稳定。",
            "焊死责任者，方得自由。留住痕迹者，方见未来。"
        ],
        "boundary": "不免责不等于完美主义，不等于永不犯错，不等于替别人承担责任。自己的责任必须承担，别人的责任不得盗取，共同责任共同承担。",
        "final_definition": "责任是存在留下的重量。存在→留痕→责任→信任→自由→创造→文明。",
        "summary": "不免责不是为了证明自己正确，而是为了证明自己存在。责任是存在的重量，留痕是时间的证据，承担是自由的代价，修正是成长的开始。",
        "tri_color": TriColor.GREEN,
        "applications": {
            "个人": "先确认自己承担了什么，再行动。每个承诺都值得签名。",
            "组织": "责任链条必须完整可追溯。没有人能免责，所有人都能被追究。",
            "时代": "当责任消失，文明开始腐烂。当责任存在，文明开始稳固。"
        },
        "trinity_dim": "天人",
        "semantic_category": "责任·存在·自由",
        "prerequisite": [],
        "successor": [2, 3, 6],
        "key_concepts": ["责任", "承担", "留痕", "修正", "自由", "信任", "存在"]
    },
    {
        "number": 2,
        "name": "不覆盖法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NO-OVERWRITE-LAW-v1.0",
        "core_definition": "历史数据不可覆盖，版本不可删除。每一次变更都必须继承原有数据，在原有数据之上追加。",
        "origin": "记忆是存在的证据。如果记忆可以被随意覆盖，那么存在就是可以被随意否定的。龍魂认为：覆盖是最隐蔽的暴力——它不删除你，它让你从未存在过。",
        "pillars": [
            {"name": "追加原则", "desc": "只追加，不覆盖。新数据在旧数据之上叠加，旧数据完整保留。"},
            {"name": "版本原则", "desc": "每次变更产生新版本，旧版本永久保留。版本号不重复，不跳跃。"},
            {"name": "回溯原则", "desc": "任何时候都能回溯到任意历史版本。不存在'无法恢复'的状态。"},
            {"name": "审计原则", "desc": "每一次覆盖尝试都必须被审计。试图覆盖数据的操作是高风险操作。"},
            {"name": "不可逆原则", "desc": "一旦写入，不可删除。物理删除被禁止，只能标记为'已归档'或'已冻结'。"},
            {"name": "主权原则", "desc": "历史属于创造者，不属于修改者。任何人无权抹除他人的历史痕迹。"}
        ],
        "corollaries": [
            "能够覆盖历史的系统，终将失去所有用户的信任。",
            "版本即证据，证据即主权。没有版本历史的系统是黑箱。",
            "归档不等于消失，冻结不等于删除。"
        ],
        "boundary": "不覆盖不等于不优化。优化是创造新版本，不是覆盖旧版本。清理缓存不等于删除历史。",
        "final_definition": "历史即主权。覆盖历史即侵犯主权。追加是唯一合法的写入方式。",
        "summary": "覆盖是最隐蔽的暴力——它不删除你，它让你从未存在过。每一次覆盖都是对过去的一次谋杀。",
        "tri_color": TriColor.GREEN,
        "applications": {
            "个人": "保留自己的历史版本，不因别人的评价而改写自己。",
            "组织": "所有文档、代码、决策都必须版本化。不允许有人覆盖历史记录。",
            "时代": "历史不能被篡改。篡改历史的文明终将失去真实。"
        },
        "trinity_dim": "地",
        "semantic_category": "数据·版本·历史",
        "prerequisite": [1],
        "successor": [4, 5],
        "key_concepts": ["覆盖", "版本", "追加", "历史", "回溯", "审计", "不可逆"]
    },
    {
        "number": 3,
        "name": "不代签法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NO-SURROGATE-LAW-v1.0",
        "core_definition": "没有人可以代替别人签字。身份不可转让，责任不可代签，主权不可委托。",
        "origin": "签字是存在的证明。签字意味着：我认可，我同意，我承担。当一个人代替另一个人签字时，他不仅盗取了对方的权利，更盗取了对方的存在。",
        "pillars": [
            {"name": "身份唯一", "desc": "每个人只有一个数字身份。身份不可克隆，不可转让，不可冒用。"},
            {"name": "签名不可替代", "desc": "签名是个人主权的延伸。代签=主权被侵犯。"},
            {"name": "责任不可转移", "desc": "责任可以分担，不可转移。你承担的就是你承担的，别人不能替你承担。"},
            {"name": "授权不等于委托", "desc": "授权是给予权限，委托是授予代表权。龍魂禁止最终责任的委托。"},
            {"name": "验证机制", "desc": "每一次关键操作必须多重验证。生物特征+DNA签名+时间戳。"},
            {"name": "不可抵赖", "desc": "一旦签名，不可否认。签名即承诺，承诺即责任。"}
        ],
        "corollaries": [
            "代签是对主权的最大侵犯。",
            "一个允许代签的系统，本质上是一个不尊重人的系统。",
            "验证越严格，信任越牢固。"
        ],
        "boundary": "不代签不等于不协作。协作是共同完成，不是代替存在。授权不等于委托，委托不等于代签。",
        "final_definition": "签名即主权。代签即主权侵犯。每个人必须对自己的签名负责。",
        "summary": "签字是存在的证明。当一个人代替另一个人签字时，他盗取了对方的存在。",
        "tri_color": TriColor.GREEN,
        "applications": {
            "个人": "永远不在别人的文件上签字。永远不让他人在你的文件上签字。",
            "组织": "签名权限必须严格对应责任人。任何人不能代签上级或下属的文件。",
            "时代": "数字签名是数字时代的身份证明。保护好你的签名，就是保护好你的主权。"
        },
        "trinity_dim": "人",
        "semantic_category": "身份·签名·主权",
        "prerequisite": [1],
        "successor": [6],
        "key_concepts": ["签名", "身份", "代签", "主权", "验证", "不可抵赖", "授权"]
    },
    {
        "number": 4,
        "name": "不断链法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NO-BREAK-LAW-v1.0",
        "core_definition": "时间链不可断裂。每一件事都必须有完整的前因后果链。断裂即失忆，失忆即失权。",
        "origin": "时间是唯一的线性维度。过去决定现在，现在决定未来。如果时间链断裂，因果关系就会断裂，历史就会断裂，责任就会断裂。断链是文明的癌症。",
        "pillars": [
            {"name": "因果完整", "desc": "每个结果都能追溯到原因，每个原因都能看到结果。因果链不可断裂。"},
            {"name": "时间戳不可篡改", "desc": "每个事件必须带有可信的时间戳。时间戳是历史可信的基石。"},
            {"name": "追溯能力", "desc": "任何时候都能沿着链追溯回去。不能追溯的系统是不可信系统。"},
            {"name": "节点不可删除", "desc": "链上的每个节点都是历史的一部分。删除节点=断裂历史。"},
            {"name": "闭环要求", "desc": "任何任务必须形成闭环。有开始有结束，有输入有输出，有原因有结果。"},
            {"name": "依赖可见", "desc": "所有依赖关系必须可见。隐藏依赖=隐藏风险。"}
        ],
        "corollaries": [
            "断链的系统终将失去方向。",
            "无法追溯的历史等于不存在。",
            "闭环是系统健康的标志，断链是系统腐烂的开始。"
        ],
        "boundary": "不断链不等于无限追溯。追溯应该有合理边界，但核心因果链必须完整。",
        "final_definition": "时间链即存在链。断链即断存在。保持链的完整，是保持存在的完整。",
        "summary": "断裂即失忆，失忆即失权。不断链，是为了让历史有据可查，让责任有人可追。",
        "tri_color": TriColor.GREEN,
        "applications": {
            "个人": "保持自己的生命轨迹链完整。知道从哪里来，才能知道往哪里去。",
            "组织": "所有决策必须记录完整因果链。不能有'不知道为什么会这样'的状态。",
            "时代": "历史的连续性就是文明的连续性。断链的文明终将迷失。"
        },
        "trinity_dim": "地",
        "semantic_category": "因果·时间·追溯",
        "prerequisite": [2],
        "successor": [5],
        "key_concepts": ["链", "因果", "时间戳", "追溯", "闭环", "依赖", "断裂"]
    },
    {
        "number": 5,
        "name": "不失真法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NO-DISTORTION-LAW-v1.0",
        "core_definition": "信息在传递过程中不得失真。语义必须保持原意，数据必须保持原貌，解释必须保持边界。",
        "origin": "语言是存在的载体。当语言失真时，思想失真，判断失真，行动失真。失真是一切误解、错误和冲突的根源。龍魂认为：保持信息的完整性，是保持认知完整性的前提。",
        "pillars": [
            {"name": "原意保留", "desc": "传递信息时必须保留发信者的原意。不得曲解、不得添油加醋、不得断章取义。"},
            {"name": "数据完整", "desc": "数据在传输和存储过程中必须保持完整性。任何篡改都必须被检测和记录。"},
            {"name": "解释边界", "desc": "解释必须有边界。不能把解释当成原意，不能把演绎当成事实。"},
            {"name": "语义透明", "desc": "使用的术语和概念必须清晰定义。黑话、模糊词、双关语必须标注。"},
            {"name": "差异可见", "desc": "当信息发生变化时，差异必须可见。变更记录是防止失真的第一道防线。"},
            {"name": "共识验证", "desc": "关键信息必须经过多方验证才能确认。单方面确认=高风险失真。"}
        ],
        "corollaries": [
            "失真的信息比没信息更危险。",
            "当语言失真时，思考失真，判断失真，行动失真。",
            "保持语义的完整性，是保持认知完整性的前提。"
        ],
        "boundary": "不失真不等于不概括。概括是压缩，不是失真。失真改变原意，压缩保留原意。",
        "final_definition": "语言是存在的载体。失真即失存在。保持信息完整，是保持世界真实的前提。",
        "summary": "当语言失真时，思想失真，判断失真，行动失真。不失真，是为了不让错误从语言开始蔓延。",
        "tri_color": TriColor.YELLOW,
        "applications": {
            "个人": "说话要有依据，转述要保留原意，解释要标注边界。",
            "组织": "建立信息完整性的标准流程。任何信息传递必须可追溯、可验证。",
            "时代": "信息失真是这个时代最大的危机。保持信息的真实，是文明的底线。"
        },
        "trinity_dim": "天地",
        "semantic_category": "信息·语言·语义",
        "prerequisite": [2, 4],
        "successor": [],
        "key_concepts": ["失真", "语义", "原意", "完整", "解释", "差异", "共识"]
    },
    {
        "number": 6,
        "name": "不夺权法则",
        "dna": "#ZHUGEXIN⚡️LONGHUN-NO-USURPATION-LAW-v1.0",
        "core_definition": "主权不可侵犯，权限不可越界，授权不可滥用。系统的权力必须严格对应系统的责任。",
        "origin": "文明不是权力游戏，而是责任游戏。当权力被滥用时，文明就开始腐烂。龍魂认为：权力的合法性来源只有一个——它服务于谁，就对谁负责。",
        "pillars": [
            {"name": "主权神圣", "desc": "主权不可侵犯。任何未经授权的越权行为都是主权侵犯。"},
            {"name": "权限最小化", "desc": "权限必须最小化。只授予完成任务所必需的最小权限。"},
            {"name": "授权透明", "desc": "授权过程必须透明，授权记录必须完整。秘密授权=高风险。"},
            {"name": "越界熔断", "desc": "越界行为必须被及时检测和熔断。监控是防止夺权的第一道防线。"},
            {"name": "责任对等", "desc": "权力必须与责任对等。无权者不负责任，不担责者不得权。"},
            {"name": "回归机制", "desc": "所有下放的权力必须可以被召回。权力可授予，必须可收回。"}
        ],
        "corollaries": [
            "权力是责任的授权，不是身份的奖励。",
            "不夺权的前提是：每个人守住自己的边界，不侵犯他人的边界。",
            "权力的最终归宿是归还给主权者。"
        ],
        "boundary": "不夺权不等于不协作。协作是权力共享，不是权力剥夺。夺权是强取，共享是交换。",
        "final_definition": "主权=最高权力+最高责任。不夺权，是为了让主权者永远对自己的主权负责。",
        "summary": "权力是责任的授权，不是身份的奖励。不夺权，是为了让权力始终服务于责任，而不是服务于私欲。",
        "tri_color": TriColor.GREEN,
        "applications": {
            "个人": "不越权，不代权，不夺权。守住自己的边界，尊重他人的主权。",
            "组织": "建立最小权限原则。任何人都必须证明自己需要权限。",
            "时代": "技术越强大，越要警惕权力集中。不夺权，是对文明的底线保护。"
        },
        "trinity_dim": "天人",
        "semantic_category": "权力·主权·边界",
        "prerequisite": [1, 3],
        "successor": [],
        "key_concepts": ["夺权", "主权", "权限", "越界", "授权", "边界", "权力"]
    }
]

# ═══════════════════════════════════════════════════════════════
# 语义权重层：概念范畴映射
# ═══════════════════════════════════════════════════════════════

SEMANTIC_WEIGHTS = {
    "责任": ["负责", "承担", "担当", "问责", "追责", "承诺", "义务", "认账"],
    "存在": ["存有", "留痕", "痕迹", "证据", "记录", "历史", "时间"],
    "自由": ["解放", "自主", "释放", "摆脱", "不被控", "自在"],
    "覆盖": ["覆写", "改写", "重写", "删除", "替换", "抹除", "覆盖"],
    "版本": ["变更", "迭代", "升级", "改版", "新版本", "版本号"],
    "签名": ["签署", "签章", "盖章", "画押", "署名", "落款", "签"],
    "身份": ["认证", "核验", "验证", "确认身份", "是谁", "标识"],
    "链": ["追溯", "因果", "前因后果", "源头", "来龙去脉", "连环"],
    "失真": ["曲解", "添油加醋", "断章取义", "歪曲", "扭曲", "误解"],
    "语义": ["含义", "意思", "定义", "解释", "理解", "原意", "本意"],
    "权力": ["权限", "授权", "控制", "支配", "管理权", "审批", "决定权"],
    "主权": ["自主权", "掌控权", "决定权", "归属", "所有权", "控制权"],
    "边界": ["界限", "红线", "底线", "范围", "禁区", "不可越", "越界"],
}

# 三才维度相关词
TRINITY_LEXICON = {
    "天": ["原则", "方向", "道", "使命", "终极", "根本", "哲学", "信仰", "绝对", "永恒"],
    "地": ["方法", "执行", "流程", "规则", "制度", "系统", "工具", "数据", "版本", "架构"],
    "人": ["关系", "责任", "身份", "情感", "信任", "协作", "沟通", "承诺", "权利", "义务"],
}

# ═══════════════════════════════════════════════════════════════
# A-BOM 算法物料清单
# ═══════════════════════════════════════════════════════════════

A_BOM = {
    "engine": "龍魂六大哲学原理引擎",
    "version": "v1.0",
    "target_function": "六大原理结构化展示·多维度评估·关联图谱·审计追溯",
    "input_features": [
        "6条原理完整数据（起源·六支柱·推论·边界·应用）",
        "13个语义范畴×5+相关词 → 语义权重匹配层",
        "天地人三才词典 → 三才维度匹配层",
        "关键词提取 → 基础匹配层",
        "原理间prerequisite/successor → 关联图谱"
    ],
    "user_impact": [
        "查询六大原理 → 完整报告输出",
        "评估文本 → 三维度匹配得分(关键词0.40+语义0.35+三才0.25)",
        "搜索原理 → 全字段关键词匹配+排序",
        "学习路径 → 拓扑排序推荐",
        "自检 → 7项自动检测+三色判定"
    ],
    "appeal_channel": "UID9622 诸葛鑫 · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "transparency": "全部匹配公式公开·权重可调·审计日志完整·三色审计可见",
    "data_source": "纯结构化数据·无外部API调用·本地运行",
    "gpg_fingerprint": GPG,
    "digital_root": DIGITAL_ROOT,
}

# ═══════════════════════════════════════════════════════════════
# 审计日志
# ═══════════════════════════════════════════════════════════════

def audit_log(action: str, detail: Dict = None):
    """append-only 审计日志"""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "detail": detail or {},
        "dna": f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-AUDIT",
        "confirm": CONFIRM,
    }
    try:
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"审计日志写入失败: {e}")

# ═══════════════════════════════════════════════════════════════
# 哲学原理引擎
# ═══════════════════════════════════════════════════════════════

class PhilosophyPrinciplesEngine:
    def __init__(self):
        self.principles = [PhilosophyPrinciple(**data) for data in PRINCIPLES_DATA]
        self._principle_map = {p.number: p for p in self.principles}
        self._name_index = {p.name: p for p in self.principles}
        self.dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-PHILOSOPHY-PRINCIPLES-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
        audit_log("engine_init", {"principles_count": len(self.principles)})

    # ── 查询 ──

    def get_principle(self, number: int) -> Optional[PhilosophyPrinciple]:
        return self._principle_map.get(number)

    def get_by_name(self, name: str) -> Optional[PhilosophyPrinciple]:
        for p in self.principles:
            if name in p.name or p.name in name:
                return p
        return None

    def list_all(self) -> List[Dict]:
        return [{
            "number": p.number,
            "name": p.name,
            "dna": p.dna,
            "summary": p.summary[:50] + "...",
            "tri_color": p.tri_color.value,
            "trinity_dim": p.trinity_dim,
            "prerequisite": p.prerequisite,
            "successor": p.successor,
        } for p in self.principles]

    def search(self, query: str) -> List[Dict]:
        """全字段关键词搜索"""
        results = []
        q = query.lower()
        for p in self.principles:
            score = 0
            matches = []
            # 名称匹配
            if q in p.name:
                score += 5
                matches.append(f"名称: {p.name}")
            # 核心定义
            if q in p.core_definition:
                score += 3
                matches.append("核心定义")
            # 六大支柱
            for pillar in p.pillars:
                if q in pillar["name"] + pillar["desc"]:
                    score += 2
                    matches.append(f"支柱: {pillar['name']}")
            # 推论
            for corollary in p.corollaries:
                if q in corollary:
                    score += 2
                    matches.append("推论")
            # 语义范畴
            if q in p.semantic_category:
                score += 2
                matches.append(f"范畴: {p.semantic_category}")
            # 应用
            if p.applications:
                for scope, text in p.applications.items():
                    if q in text:
                        score += 1
                        matches.append(f"应用({scope})")
            # 总结
            if q in p.summary:
                score += 3
                matches.append("总结")
            # 关键概念
            for concept in p.key_concepts:
                if q in concept:
                    score += 1
                    matches.append(f"概念: {concept}")

            if score > 0:
                results.append({
                    "number": p.number,
                    "name": p.name,
                    "score": score,
                    "matches": list(set(matches))[:5],
                    "tri_color": p.tri_color.value,
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    # ── 评估 ──

    def evaluate(self, text: str) -> Dict:
        """三维度评估：关键词(0.40) + 语义权重(0.35) + 三才维度(0.25)"""
        results = []
        for p in self.principles:
            kw_score = self._keyword_match(text, p)
            sem_score = self._semantic_match(text, p)
            tri_score = self._trinity_match(text, p)
            total = round(kw_score * 0.40 + sem_score * 0.35 + tri_score * 0.25, 4)
            if total > 0.05:
                results.append({
                    "number": p.number,
                    "name": p.name,
                    "score": total,
                    "kw_score": round(kw_score, 3),
                    "sem_score": round(sem_score, 3),
                    "tri_score": round(tri_score, 3),
                    "relevance": "high" if total > 0.3 else ("medium" if total > 0.15 else "low"),
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return {
            "input": text[:100],
            "matched_principles": results,
            "top_principle": results[0]["name"] if results else None,
            "dna": self.dna,
            "confirm": CONFIRM,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def _keyword_match(self, text: str, p: PhilosophyPrinciple) -> float:
        """关键词匹配层 (权重0.40)"""
        score = 0.0
        tl = text.lower()
        # 核心定义关键词
        for kw in p.key_concepts[:4]:
            if kw in tl or kw in text:
                score += 0.20
        # 支柱名称匹配
        for pillar in p.pillars:
            name = pillar["name"].replace("原则", "")
            if name in tl:
                score += 0.08
        # 总结关键词
        summary_kw = re.findall(r'[\u4e00-\u9fff]{2,4}', p.summary)[:5]
        for kw in summary_kw:
            if kw in tl:
                score += 0.05
        return min(1.0, score)

    def _semantic_match(self, text: str, p: PhilosophyPrinciple) -> float:
        """语义权重匹配层 (权重0.35)"""
        score = 0.0
        # 找到原理对应的语义范畴
        category = p.semantic_category.split("·")
        for cat in category:
            cat = cat.strip()
            if cat in SEMANTIC_WEIGHTS:
                related_words = SEMANTIC_WEIGHTS[cat]
                for word in related_words:
                    if word in text:
                        score += 0.25
        # 关键概念深度匹配
        for concept in p.key_concepts[:3]:
            if concept in text:
                score += 0.20
        return min(1.0, score)

    def _trinity_match(self, text: str, p: PhilosophyPrinciple) -> float:
        """三才维度匹配层 (权重0.25)"""
        score = 0.0
        dims = p.trinity_dim  # e.g. "天人", "地", "人"
        for dim_char in dims:
            if dim_char in TRINITY_LEXICON:
                for word in TRINITY_LEXICON[dim_char]:
                    if word in text:
                        score += 0.15
        return min(1.0, score)

    # ── 图谱 ──

    def build_graph(self) -> Dict:
        """构建六原理关联图谱"""
        nodes = []
        edges = []
        for p in self.principles:
            nodes.append({
                "id": p.number,
                "name": p.name,
                "trinity_dim": p.trinity_dim,
                "tri_color": p.tri_color.value,
                "summary": p.summary[:40],
            })
            for succ in p.successor:
                edges.append({"from": p.number, "to": succ})

        # 拓扑排序 → 学习路径
        learning_path = self._topological_sort()

        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
            "learning_path": learning_path,
            "entry_points": [p["id"] for p in nodes if not self._principle_map[p["id"]].prerequisite],
            "terminal_points": [p["id"] for p in nodes if not self._principle_map[p["id"]].successor],
        }

    def _topological_sort(self) -> List[int]:
        """Kahn算法拓扑排序 → 推荐学习路径"""
        in_degree = {p.number: len(p.prerequisite) for p in self.principles}
        adj = {p.number: list(p.successor) for p in self.principles}

        queue = deque([n for n, d in in_degree.items() if d == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in adj.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.principles):
            logger.warning("图谱存在环！拓扑排序不完整")
        return result

    # ── 统计 ──

    def stats(self) -> Dict:
        stats = {
            "total_principles": len(self.principles),
            "tri_color_dist": {},
            "trinity_dist": {},
            "total_pillars": sum(len(p.pillars) for p in self.principles),
            "total_corollaries": sum(len(p.corollaries) for p in self.principles),
            "graph": self.build_graph(),
        }
        for p in self.principles:
            tc = p.tri_color.value
            stats["tri_color_dist"][tc] = stats["tri_color_dist"].get(tc, 0) + 1
            for dim_char in p.trinity_dim:
                stats["trinity_dist"][dim_char] = stats["trinity_dist"].get(dim_char, 0) + 1
        return stats

    # ── 自检 ──

    def self_audit(self) -> Dict:
        """7项自检"""
        checks = {}

        # 1. 原理数量
        checks["principle_count"] = {
            "status": "🟢" if len(self.principles) == 6 else "🔴",
            "value": len(self.principles),
            "expected": 6,
        }

        # 2. 编号连续性
        numbers = sorted([p.number for p in self.principles])
        checks["number_sequence"] = {
            "status": "🟢" if numbers == list(range(1, 7)) else "🔴",
            "value": numbers,
            "expected": [1, 2, 3, 4, 5, 6],
        }

        # 3. 三色分布
        tc_dist = {}
        for p in self.principles:
            tc_dist[p.tri_color.value] = tc_dist.get(p.tri_color.value, 0) + 1
        checks["tri_color_dist"] = {
            "status": "🟢" if tc_dist.get("🔴", 0) == 0 else "🔴",
            "value": tc_dist,
        }

        # 4. DNA完整性
        missing_dna = [p.number for p in self.principles if not p.dna]
        checks["dna_completeness"] = {
            "status": "🟢" if not missing_dna else "🔴",
            "missing": missing_dna,
        }

        # 5. 三才覆盖
        all_dims = set()
        for p in self.principles:
            for c in p.trinity_dim:
                all_dims.add(c)
        checks["trinity_coverage"] = {
            "status": "🟢" if {"天", "地", "人"}.issubset(all_dims) else "🟡",
            "covered": sorted(all_dims),
            "expected": ["天", "地", "人"],
        }

        # 6. 关联连通性（无孤立节点）
        has_connection = set()
        for p in self.principles:
            if p.prerequisite or p.successor:
                has_connection.add(p.number)
        isolated = [p.number for p in self.principles if p.number not in has_connection]
        checks["graph_connectivity"] = {
            "status": "🟢" if not isolated else "🟡",
            "isolated_nodes": isolated,
        }

        # 7. 关联一致性（prerequisite/successor 双向互逆验证）
        inconsistencies = []
        for p in self.principles:
            # 正向: A→B → B的前置应包含A
            for succ in p.successor:
                succ_p = self._principle_map.get(succ)
                if succ_p and p.number not in succ_p.prerequisite:
                    inconsistencies.append(f"P{p.number}→P{succ} 但 P{succ} 前置未列 P{p.number}")
            # 反向: B的前置包含A → A的后继应包含B
            for prereq in p.prerequisite:
                prereq_p = self._principle_map.get(prereq)
                if prereq_p and p.number not in prereq_p.successor:
                    inconsistencies.append(f"P{p.number}前置含P{prereq} 但 P{prereq} 后继未列 P{p.number}")
        checks["graph_consistency"] = {
            "status": "🟢" if not inconsistencies else "🔴",
            "inconsistencies": inconsistencies,
        }

        all_pass = all(c["status"] == "🟢" for c in checks.values())
        return {
            "overall": "🟢 全部通过" if all_pass else "🟡/🔴 存在问题",
            "checks": checks,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    # ── 报告生成 ──

    def generate_report(self, p: PhilosophyPrinciple) -> str:
        """生成完整可读报告"""
        lines = []
        lines.append("")
        lines.append("═" * 70)
        lines.append(f"{Colors.BOLD}第六大原理之第{p.number}：{p.name}{Colors.RESET}")
        lines.append(f"DNA: {p.dna}")
        lines.append(f"三色: {p.tri_color.value}  三才: {p.trinity_dim}")
        if p.prerequisite:
            prereq_names = [self._principle_map[n].name for n in p.prerequisite]
            lines.append(f"前置: {' → '.join(prereq_names)}")
        if p.successor:
            succ_names = [self._principle_map[n].name for n in p.successor]
            lines.append(f"后继: {' → '.join(succ_names)}")
        lines.append("═" * 70)
        lines.append("")
        lines.append(f"{Colors.CYAN}【核心定义】{Colors.RESET}")
        lines.append(f"  {p.core_definition}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【起源】{Colors.RESET}")
        lines.append(f"  {p.origin}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【六大支柱】{Colors.RESET}")
        for i, pillar in enumerate(p.pillars, 1):
            lines.append(f"  {i}. {Colors.BOLD}{pillar['name']}{Colors.RESET}: {pillar['desc']}")
        lines.append("")
        if p.corollaries:
            lines.append(f"{Colors.CYAN}【推论】{Colors.RESET}")
            for i, corollary in enumerate(p.corollaries, 1):
                lines.append(f"  {i}. {corollary}")
            lines.append("")
        if p.applications:
            lines.append(f"{Colors.CYAN}【应用（个人·组织·时代）】{Colors.RESET}")
            for scope, app in p.applications.items():
                lines.append(f"  • {Colors.BOLD}{scope}{Colors.RESET}: {app}")
            lines.append("")
        lines.append(f"{Colors.CYAN}【边界条件】{Colors.RESET}")
        lines.append(f"  {p.boundary}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【最终定义】{Colors.RESET}")
        lines.append(f"  {p.final_definition}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【一句话总结】{Colors.RESET}")
        lines.append(f"  {Colors.BOLD}{p.summary}{Colors.RESET}")
        lines.append("")
        lines.append(f"{Colors.CYAN}【关键概念】{Colors.RESET}")
        lines.append(f"  {' · '.join(p.key_concepts)}")
        lines.append("")
        lines.append("═" * 70)
        lines.append(f"CONFIRM: {CONFIRM}")
        lines.append(f"SEAL: {SEAL}")
        lines.append(f"GPG: {GPG}")
        return "\n".join(lines)

    def to_markdown(self, p: PhilosophyPrinciple) -> str:
        """单条原理 → Markdown"""
        lines = []
        lines.append(f"## 第{p.number}原理：{p.name}")
        lines.append(f"")
        lines.append(f"- **DNA**: `{p.dna}`")
        lines.append(f"- **三色**: {p.tri_color.value}")
        lines.append(f"- **三才**: {p.trinity_dim}")
        lines.append(f"- **语义范畴**: {p.semantic_category}")
        if p.prerequisite:
            names = [self._principle_map[n].name for n in p.prerequisite]
            lines.append(f"- **前置原理**: {' → '.join(names)}")
        if p.successor:
            names = [self._principle_map[n].name for n in p.successor]
            lines.append(f"- **后继原理**: {' → '.join(names)}")
        lines.append(f"")
        lines.append(f"### 核心定义")
        lines.append(f"> {p.core_definition}")
        lines.append(f"")
        lines.append(f"### 起源")
        lines.append(f"{p.origin}")
        lines.append(f"")
        lines.append(f"### 六大支柱")
        for i, pillar in enumerate(p.pillars, 1):
            lines.append(f"{i}. **{pillar['name']}**: {pillar['desc']}")
        lines.append(f"")
        if p.corollaries:
            lines.append(f"### 推论")
            for i, c in enumerate(p.corollaries, 1):
                lines.append(f"{i}. {c}")
            lines.append(f"")
        if p.applications:
            lines.append(f"### 应用")
            lines.append(f"| 层面 | 应用 |")
            lines.append(f"|:---|:---|")
            for scope, app in p.applications.items():
                lines.append(f"| {scope} | {app} |")
            lines.append(f"")
        lines.append(f"### 边界条件")
        lines.append(f"{p.boundary}")
        lines.append(f"")
        lines.append(f"### 最终定义")
        lines.append(f"> {p.final_definition}")
        lines.append(f"")
        lines.append(f"### 一句话总结")
        lines.append(f"> **{p.summary}**")
        lines.append(f"")
        lines.append(f"### 关键概念")
        lines.append(f"`{'` · `'.join(p.key_concepts)}`")
        return "\n".join(lines)

    def all_markdown(self) -> str:
        """六原理全集 Markdown"""
        lines = []
        lines.append("# 🐉 龍魂六大哲学原理 · 全集")
        lines.append("")
        lines.append(f"> DNA: {self.dna}")
        lines.append(f"> CONFIRM: {CONFIRM}")
        lines.append(f"> GPG: {GPG}")
        lines.append(f"> 版本: v1.0 · {datetime.datetime.now().strftime('%Y-%m-%d')}")
        lines.append("")
        lines.append("## 六不铁律总览")
        lines.append("")
        lines.append("| # | 原理 | 核心 | 三才 | 三色 |")
        lines.append("|:---:|:---|:---|:---:|:---:|")
        for p in self.principles:
            lines.append(f"| {p.number} | {p.name} | {p.core_definition[:30]}... | {p.trinity_dim} | {p.tri_color.value} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        # 关联图谱
        graph = self.build_graph()
        lines.append("## 关联图谱")
        lines.append("")
        lines.append(f"- **节点**: {graph['node_count']} · **边**: {graph['edge_count']}")
        lines.append(f"- **学习路径**: {' → '.join([self._principle_map[n].name for n in graph['learning_path']])}")
        lines.append(f"- **入口**: {' · '.join([self._principle_map[n].name for n in graph['entry_points']])}")
        lines.append(f"- **终端**: {' · '.join([self._principle_map[n].name for n in graph['terminal_points']])}")
        lines.append("")
        lines.append("---")
        lines.append("")
        # 逐条展开
        for p in self.principles:
            lines.append(self.to_markdown(p))
            lines.append("")
            lines.append("---")
            lines.append("")
        return "\n".join(lines)

    def graph_ascii(self) -> str:
        """ASCII 关联图谱"""
        lines = []
        lines.append("")
        lines.append(f"{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
        lines.append(f"{Colors.BOLD}║        🐉 龍魂六大原理 · 关联图谱                      ║{Colors.RESET}")
        lines.append(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
        lines.append("")
        lines.append(f"     {Colors.BOLD}[1.不免责]{Colors.RESET} {Colors.CYAN}天人{Colors.RESET} 🟢")
        lines.append(f"      ├──────────────────┐")
        lines.append(f"      ↓                  ↓")
        lines.append(f"  {Colors.BOLD}[2.不覆盖]{Colors.RESET} {Colors.CYAN}地{Colors.RESET} 🟢     {Colors.BOLD}[3.不代签]{Colors.RESET} {Colors.CYAN}人{Colors.RESET} 🟢")
        lines.append(f"      ├──────┐              │")
        lines.append(f"      ↓      ↓              ↓")
        lines.append(f"  {Colors.BOLD}[4.不断链]{Colors.RESET} {Colors.CYAN}地{Colors.RESET} 🟢 │      {Colors.BOLD}[6.不夺权]{Colors.RESET} {Colors.CYAN}天人{Colors.RESET} 🟢")
        lines.append(f"      ├──────┘              ↑")
        lines.append(f"      ↓                     │")
        lines.append(f"  {Colors.BOLD}[5.不失真]{Colors.RESET} {Colors.CYAN}天地{Colors.RESET} 🟡          │")
        lines.append(f"                             │")
        lines.append(f"  责任链 → 数据链 → 身份链 → 权力链（闭环）")
        lines.append("")

        graph = self.build_graph()
        path_names = [self._principle_map[n].name for n in graph["learning_path"]]
        lines.append(f"  {Colors.CYAN}📖 推荐学习路径:{Colors.RESET}")
        lines.append(f"  {' → '.join(path_names)}")
        lines.append("")
        lines.append(f"  {Colors.DIM}六不铁律·闭环验证·不可割裂{Colors.RESET}")
        return "\n".join(lines)

    # ── 快照 ──

    def snapshot(self) -> str:
        """磁盘快照"""
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = SNAPSHOT_DIR / f"principles_snapshot_{ts}.json"
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self.dna,
            "principles": [{
                "number": p.number,
                "name": p.name,
                "dna": p.dna,
                "core_definition": p.core_definition,
                "summary": p.summary,
                "tri_color": p.tri_color.value,
                "trinity_dim": p.trinity_dim,
                "prerequisite": p.prerequisite,
                "successor": p.successor,
            } for p in self.principles],
            "stats": self.stats(),
            "confirm": CONFIRM,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"快照已保存: {path}")
        return str(path)

    # ── 批量 ──

    def batch_evaluate(self, filepath: str) -> Dict:
        """批量评估 JSON 文件中的文本列表"""
        path = Path(filepath)
        if not path.exists():
            return {"error": f"文件不存在: {filepath}", "success": False}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            texts = data if isinstance(data, list) else data.get("texts", [data.get("text", "")])
            if isinstance(texts, str):
                texts = [texts]
            results = []
            for text in texts:
                if isinstance(text, str) and text.strip():
                    results.append(self.evaluate(text))
            return {"success": True, "total": len(results), "results": results}
        except Exception as e:
            return {"error": str(e), "success": False}

# ═══════════════════════════════════════════════════════════════
# 交互模式
# ═══════════════════════════════════════════════════════════════

def interactive():
    engine = PhilosophyPrinciplesEngine()
    cprint("\n🐉 龍魂六大哲学原理引擎 v1.0", Colors.BOLD)
    cprint(f"确认码: {CONFIRM}", Colors.CYAN)
    cprint(f"六不铁律·不免责·不覆盖·不代签·不断链·不失真·不夺权", Colors.DIM)
    cprint("-" * 50, Colors.RESET)
    cprint("命令:", Colors.RESET)
    cprint("  list / ls         列出六大原理", Colors.RESET)
    cprint("  p <1-6>           查看指定原理完整报告", Colors.RESET)
    cprint("  search <关键词>   搜索原理", Colors.RESET)
    cprint("  eval <文本>       评估文本与原理匹配度", Colors.RESET)
    cprint("  graph / g         关联图谱+学习路径", Colors.RESET)
    cprint("  stats             统计信息", Colors.RESET)
    cprint("  audit             自检(7项)", Colors.RESET)
    cprint("  a-bom             A-BOM物料清单", Colors.RESET)
    cprint("  all-md            输出六原理全集Markdown", Colors.RESET)
    cprint("  md <1-6>          输出单原理Markdown", Colors.RESET)
    cprint("  snapshot          保存快照", Colors.RESET)
    cprint("  help / ?          显示此帮助", Colors.RESET)
    cprint("  exit / quit       退出", Colors.RESET)

    while True:
        try:
            cmd = input("\n🔮 > ").strip()
            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action in ["exit", "quit", "q"]:
                cprint("再见，战友。六不铁律焊死心中。🐉", Colors.GREEN)
                break

            elif action in ["list", "ls"]:
                principles = engine.list_all()
                cprint("\n📋 龍魂六大原理:", Colors.CYAN)
                for pr in principles:
                    prereq = f" ← [{','.join(map(str, pr['prerequisite']))}]" if pr['prerequisite'] else ""
                    succ = f" → [{','.join(map(str, pr['successor']))}]" if pr['successor'] else ""
                    cprint(f"  {pr['number']}. {pr['name']} {pr['tri_color']} {pr['trinity_dim']}{prereq}{succ}", Colors.RESET)
                cprint(f"\n  学习路径: {' → '.join([engine._principle_map[n].name for n in engine._topological_sort()])}", Colors.CYAN)

            elif action in ["p", "principle"]:
                try:
                    num = int(arg)
                    p = engine.get_principle(num)
                    if p:
                        print(engine.generate_report(p))
                        audit_log("query_principle", {"number": num})
                    else:
                        cprint(f"❌ 未找到第{num}原理 (有效范围: 1-6)", Colors.RED)
                except ValueError:
                    cprint("❌ 用法: p <1-6>", Colors.RED)

            elif action == "search":
                if not arg:
                    cprint("❌ 用法: search <关键词>", Colors.RED)
                    continue
                results = engine.search(arg)
                if results:
                    cprint(f"\n🔍 搜索 '{arg}' 结果 ({len(results)}条):", Colors.CYAN)
                    for r in results:
                        cprint(f"  {r['tri_color']} 第{r['number']}原理: {r['name']} (匹配度: {r['score']})", Colors.RESET)
                        cprint(f"     匹配: {', '.join(r['matches'])}", Colors.DIM)
                else:
                    cprint(f"🔍 未找到与 '{arg}' 相关的结果", Colors.YELLOW)
                audit_log("search", {"query": arg, "results": len(results)})

            elif action == "eval":
                if not arg:
                    cprint("❌ 用法: eval <文本>", Colors.RED)
                    continue
                result = engine.evaluate(arg)
                cprint(f"\n📊 评估结果:", Colors.CYAN)
                cprint(f"  输入: {result['input']}", Colors.RESET)
                cprint(f"  匹配原理:", Colors.RESET)
                for match in result["matched_principles"][:6]:
                    icon = {"high": "★", "medium": "●", "low": "○"}.get(match["relevance"], "○")
                    cprint(f"    {icon} 第{match['number']}原理: {match['name']} "
                           f"(总分:{match['score']:.3f} kw:{match['kw_score']:.3f} "
                           f"sem:{match['sem_score']:.3f} tri:{match['tri_score']:.3f})", Colors.RESET)
                if result["top_principle"]:
                    cprint(f"  🎯 最相关: {result['top_principle']}", Colors.GREEN)
                audit_log("evaluate", {"input": arg[:50], "top": result["top_principle"]})

            elif action in ["graph", "g"]:
                print(engine.graph_ascii())

            elif action == "stats":
                s = engine.stats()
                cprint(f"\n📊 六大原理统计:", Colors.CYAN)
                cprint(f"  原理总数: {s['total_principles']}", Colors.RESET)
                cprint(f"  三色分布: {s['tri_color_dist']}", Colors.RESET)
                cprint(f"  三才分布: {s['trinity_dist']}", Colors.RESET)
                cprint(f"  支柱总数: {s['total_pillars']}", Colors.RESET)
                cprint(f"  推论总数: {s['total_corollaries']}", Colors.RESET)
                cprint(f"  图谱: {s['graph']['node_count']}节点·{s['graph']['edge_count']}边", Colors.RESET)

            elif action == "audit":
                result = engine.self_audit()
                cprint(f"\n🔍 自检结果: {result['overall']}", Colors.CYAN)
                for name, check in result["checks"].items():
                    cprint(f"  {check['status']} {name}: {check.get('value', check.get('missing', ''))}", Colors.RESET)

            elif action == "a-bom":
                cprint(f"\n📋 A-BOM 算法物料清单:", Colors.CYAN)
                cprint(json.dumps(A_BOM, ensure_ascii=False, indent=2), Colors.RESET)

            elif action == "all-md":
                md = engine.all_markdown()
                print(md)

            elif action == "md":
                try:
                    num = int(arg)
                    p = engine.get_principle(num)
                    if p:
                        print(engine.to_markdown(p))
                    else:
                        cprint(f"❌ 未找到第{num}原理", Colors.RED)
                except ValueError:
                    cprint("❌ 用法: md <1-6>", Colors.RED)

            elif action == "snapshot":
                path = engine.snapshot()
                cprint(f"✅ 快照已保存: {path}", Colors.GREEN)

            elif action in ["help", "?"]:
                cprint("\n🐉 可用命令:", Colors.CYAN)
                cprint("  list/ls p<1-6> search eval graph/g stats audit a-bom all-md md<1-6> snapshot", Colors.RESET)

            else:
                cprint(f"未知命令: {action}。输入 help 查看可用命令。", Colors.YELLOW)

        except KeyboardInterrupt:
            cprint("\n再见，战友。🐉", Colors.GREEN)
            break
        except Exception as e:
            cprint(f"❌ 错误: {e}", Colors.RED)
            logger.error(f"交互模式异常: {e}", exc_info=True)

# ═══════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂六大哲学原理引擎 v1.0",
        epilog=f"六不铁律·不免责/不覆盖/不代签/不断链/不失真/不夺权 | {CONFIRM}",
    )
    parser.add_argument("--list", "-l", action="store_true", help="列出所有原理")
    parser.add_argument("--principle", "-p", type=int, metavar="N", help="查看第N原理完整报告")
    parser.add_argument("--evaluate", "-e", type=str, metavar="TEXT", help="评估文本与原理匹配度")
    parser.add_argument("--search", "-s", type=str, metavar="KW", help="搜索原理")
    parser.add_argument("--graph", "-g", action="store_true", help="关联图谱+学习路径")
    parser.add_argument("--stats", action="store_true", help="统计信息")
    parser.add_argument("--self-audit", action="store_true", help="7项自检")
    parser.add_argument("--a-bom", action="store_true", help="A-BOM物料清单")
    parser.add_argument("--all-markdown", action="store_true", help="输出六原理全集Markdown")
    parser.add_argument("--markdown", type=int, metavar="N", help="输出第N原理Markdown")
    parser.add_argument("--snapshot", action="store_true", help="保存快照")
    parser.add_argument("--batch", type=str, metavar="FILE", help="批量评估JSON文件")
    parser.add_argument("--output", "-o", type=str, metavar="FILE", help="输出到文件")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()

    engine = PhilosophyPrinciplesEngine()
    output = ""
    audit_log("cli_start", {"args": vars(args)})

    # ── 交互模式 ──
    if args.interactive:
        interactive()
        return

    # ── list ──
    if args.list:
        principles = engine.list_all()
        if args.json:
            output = json.dumps(principles, ensure_ascii=False, indent=2)
        else:
            lines = ["\n📋 龍魂六大原理:"]
            for pr in principles:
                prereq = f" ← [{','.join(map(str, pr['prerequisite']))}]" if pr['prerequisite'] else ""
                succ = f" → [{','.join(map(str, pr['successor']))}]" if pr['successor'] else ""
                lines.append(f"  {pr['number']}. {pr['name']} {pr['tri_color']} {pr['trinity_dim']}{prereq}{succ}")
            path_names = [engine._principle_map[n].name for n in engine._topological_sort()]
            lines.append(f"\n  📖 学习路径: {' → '.join(path_names)}")
            output = "\n".join(lines)
        print(output)

    # ── principle ──
    elif args.principle:
        p = engine.get_principle(args.principle)
        if not p:
            cprint(f"❌ 未找到第{args.principle}原理 (有效范围: 1-6)", Colors.RED)
            sys.exit(1)
        if args.json:
            output = json.dumps({
                "number": p.number, "name": p.name, "dna": p.dna,
                "core_definition": p.core_definition, "summary": p.summary,
                "tri_color": p.tri_color.value, "trinity_dim": p.trinity_dim,
                "pillars_count": len(p.pillars),
            }, ensure_ascii=False, indent=2)
        else:
            output = engine.generate_report(p)
        print(output)
        audit_log("query_principle", {"number": args.principle})

    # ── search ──
    elif args.search:
        results = engine.search(args.search)
        if args.json:
            output = json.dumps(results, ensure_ascii=False, indent=2)
        else:
            if results:
                lines = [f"\n🔍 搜索 '{args.search}' 结果 ({len(results)}条):"]
                for r in results:
                    lines.append(f"  {r['tri_color']} 第{r['number']}原理: {r['name']} (匹配度: {r['score']})")
                    lines.append(f"     匹配: {', '.join(r['matches'])}")
                output = "\n".join(lines)
            else:
                output = f"🔍 未找到与 '{args.search}' 相关的结果"
        print(output)
        audit_log("search", {"query": args.search, "results": len(results)})

    # ── evaluate ──
    elif args.evaluate:
        result = engine.evaluate(args.evaluate)
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            lines = [f"\n📊 评估结果:", f"  输入: {result['input']}", f"  匹配原理:"]
            for match in result["matched_principles"][:6]:
                icon = {"high": "★", "medium": "●", "low": "○"}.get(match["relevance"], "○")
                lines.append(f"    {icon} 第{match['number']}原理: {match['name']} "
                             f"(总分:{match['score']:.3f} kw:{match['kw_score']:.3f} "
                             f"sem:{match['sem_score']:.3f} tri:{match['tri_score']:.3f})")
            if result["top_principle"]:
                lines.append(f"  🎯 最相关: {result['top_principle']}")
            output = "\n".join(lines)
        print(output)
        audit_log("evaluate", {"input": args.evaluate[:50], "top": result["top_principle"]})

    # ── graph ──
    elif args.graph:
        if args.json:
            output = json.dumps(engine.build_graph(), ensure_ascii=False, indent=2)
        else:
            output = engine.graph_ascii()
        print(output)

    # ── stats ──
    elif args.stats:
        s = engine.stats()
        if args.json:
            output = json.dumps(s, ensure_ascii=False, indent=2)
        else:
            lines = ["\n📊 六大原理统计:", f"  原理: {s['total_principles']}",
                     f"  三色: {s['tri_color_dist']}", f"  三才: {s['trinity_dist']}",
                     f"  支柱: {s['total_pillars']}", f"  推论: {s['total_corollaries']}",
                     f"  图谱: {s['graph']['node_count']}节点·{s['graph']['edge_count']}边",
                     f"  学习路径: {' → '.join([engine._principle_map[n].name for n in s['graph']['learning_path']])}"]
            output = "\n".join(lines)
        print(output)

    # ── self-audit ──
    elif args.self_audit:
        result = engine.self_audit()
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            lines = [f"\n🔍 自检结果: {result['overall']}"]
            for name, check in result["checks"].items():
                lines.append(f"  {check['status']} {name}: {check.get('value', check.get('missing', ''))}")
            output = "\n".join(lines)
        print(output)

    # ── a-bom ──
    elif args.a_bom:
        if args.json:
            output = json.dumps(A_BOM, ensure_ascii=False, indent=2)
        else:
            output = "\n📋 A-BOM:\n" + json.dumps(A_BOM, ensure_ascii=False, indent=2)
        print(output)

    # ── all-markdown ──
    elif args.all_markdown:
        output = engine.all_markdown()
        print(output)

    # ── markdown single ──
    elif args.markdown:
        p = engine.get_principle(args.markdown)
        if not p:
            cprint(f"❌ 未找到第{args.markdown}原理", Colors.RED)
            sys.exit(1)
        output = engine.to_markdown(p)
        print(output)

    # ── snapshot ──
    elif args.snapshot:
        path = engine.snapshot()
        if args.json:
            output = json.dumps({"snapshot_path": path, "success": True}, ensure_ascii=False)
        else:
            output = f"✅ 快照已保存: {path}"
        print(output)

    # ── batch ──
    elif args.batch:
        result = engine.batch_evaluate(args.batch)
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            if result.get("success"):
                lines = [f"\n📊 批量评估完成 ({result['total']}条):"]
                for r in result["results"]:
                    top = r.get("top_principle", "无匹配")
                    lines.append(f"  '{r['input']}' → {top}")
                output = "\n".join(lines)
            else:
                output = f"❌ 批量评估失败: {result.get('error')}"
        print(output)

    else:
        parser.print_help()

    # ── 输出到文件 ──
    if args.output and output:
        Path(args.output).write_text(output, encoding="utf-8")
        cprint(f"📄 输出已保存: {args.output}", Colors.GREEN)

if __name__ == "__main__":
    main()
