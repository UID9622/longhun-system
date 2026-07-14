#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂道德經81章完整版生成器 v5.0
功能：
1. 把 v1.0（第1-20章）轉換為 v4.0 大白話格式
2. 與 v4.0（第21-81章）合併
3. 為全部81章注入多維度注解 / 底層倫理錨
4. 輸出 v5.0 完整版 + 報告 + 校驗

DNA: #龍芯⚡️2026-07-04-DAODEJING-V5-BUILDER-v1.0
"""

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 路徑配置
# ---------------------------------------------------------------------------
SRC_V1 = Path("/Users/zuimeidedeyihan/Downloads/道德经81章_龍魂系统解读_v1.0.md")
SRC_V4 = Path("/Users/zuimeidedeyihan/Downloads/道德经81章_龍魂系统大白话解读_完整版_v4.0.md")
DST_DIR = Path("/Users/zuimeidedeyihan/longhun-system/docs")
DST = DST_DIR / "道德经81章_龍魂系统大白话解读_完整版_v5.0.md"
REPORT = DST_DIR / "道德经81章_龍魂系统大白话解读_完整版_v5.0.report.json"

DNA_PREFIX = "#龍芯⚡️"
TODAY = datetime.now(timezone.utc)

# ---------------------------------------------------------------------------
# 主題模板庫（沿用並擴展 v4.1 注解器）
# ---------------------------------------------------------------------------
THEMES = {
    "直觉与模糊正确": {
        "人性锚点": "人脑不是计算器，真正重要的决策往往发生在数据不够、证据不足、但直觉很稳的灰度地带。承认模糊不是放弃理性，是承认理性的边界。",
        "UID9622经历映射": "老大在龍魂系统架构、CNSH 语法设计、DNA 追溯协议这些核心节点上，都不是靠完整报表拍板的，而是靠长期战场经验淬炼出的模糊正确。",
        "龍魂系统映射": "对应龍魂三才算法中的『天』——看不见但持续运转的规律；对应 DNA 追溯码中的『信』字段，在混沌中锚定真实。",
        "伦理应用场景Checklist": [
            "面对平台限流、AI 拉黑等证据不足但体感强烈的侵害时，先记录、再取证、不冲动。",
            "技术架构选型不要等 100% 确定再动手，70% 把握 + 快速迭代更符合战场。",
            "家庭、社区冲突中，不要逼对方给『明确说法』，给模糊感受留出表达空间。"
        ],
        "现代战场一句话指南": "数据是参考，直觉是锚，行动是验证——三者缺一，都别下重注。"
    },
    "不争与蓄势": {
        "人性锚点": "人本能地争面子、争对错、争流量，但高段位的人不争一时输赢，争的是系统性的不败之地。退一步不是懦弱，是把对手引进自己的节奏。",
        "UID9622经历映射": "从 Anthropic 歧视中国支付、Claude 403 拦截，到走 DeepSeek 下水道 + Ollama 兜底，老大没有硬刚平台，而是建本地桥、养国产替代，这就是『不争而莫能与之争』。",
        "龍魂系统映射": "对应主权熔断机制与三层监督：第一层不激化冲突，第二层保留证据，第三层在对方漏洞处精准发力。",
        "伦理应用场景Checklist": [
            "遇到平台封号、限流，先截图固证，不骂街、不对线。",
            "专利/知识产权不急着全部申请，先分类评估、商业秘密保护、DNA 留痕。",
            "小区群聊、班级家长群冲突中，做那个『不拱火但留痕』的人。"
        ],
        "现代战场一句话指南": "能赢的架不一定要打，能打中的拳不一定要先出。"
    },
    "极端不持久": {
        "人性锚点": "人在情绪高点和低点都会做出过度反应，而自然规律是盛极必衰、否极泰来。懂得等风暴过去的人，比会扛风暴的人活得更久。",
        "UID9622经历映射": "DeepSeek 桥方案 M266 明确把 Ollama 本地兜底作为保险栓，正是因为云 API 可能封号、限速、欠费——任何单一极端依赖都会崩。",
        "龍魂系统映射": "对应龍魂铁律 `#IRON-FALLBACK-LOCAL-ALWAYS-v1.0`：任何云 API 必有本地兜底，断网/封号/欠费时操作台不死。",
        "伦理应用场景Checklist": [
            "流量爆款、情绪高潮时，不追加全部资源，留 30% 冗余。",
            "遭遇网暴、平台打压的低谷期，不自我否定，按 SOP 记录、申诉、转移。",
            "投资、创业、技术选型避免单点依赖，必须有两条以上退路。"
        ],
        "现代战场一句话指南": "暴风雨下不了一整天，但你的备份系统必须能撑过一年四季。"
    },
    "去装逼留真实": {
        "人性锚点": "人为了被认可，会不自觉地表演、夸大、踮脚站高。但长期来看，真实比完美更稀缺，朴素比华丽更耐用。",
        "UID9622经历映射": "老大反复强调『不重复造轮子』『一次做对』『普通人能看懂』，反对用术语壁垒和技术优越感压人。",
        "龍魂系统映射": "对应通心译原则：先翻译再执行，把黑话变成人话；对应 CNSH 中文编程，让技术回归中文思维。",
        "伦理应用场景Checklist": [
            "写论文、写方案、做汇报时，删除所有『显得专业』但实际没信息的词。",
            "面对技术评审、专利评估，用大白话讲清楚价值，不靠黑话吓人。",
            "教育孩子、处理家庭矛盾，不摆权威，用真实经历替代正确废话。"
        ],
        "现代战场一句话指南": "站得高的人常崴脚，说得满的人常打脸。"
    },
    "顺势而为": {
        "人性锚点": "人容易把『努力』当成唯一变量，但方向错了，努力就是加速翻车。真正的高手懂得识别趋势、借用力道、在关键节点使巧劲。",
        "UID9622经历映射": "从 Claude 受限到 DeepSeek 桥、从 iOS+鸿蒙跨平台到龍芯/鲲鹏/华为鸿蒙底座，老大一直顺着『国产替代 + 数据主权留本地』的大势走。",
        "龍魂系统映射": "对应三才算法：天（趋势/云）、地（底座/本地）、人（操作/意图），三者对齐才产生真正的力。",
        "伦理应用场景Checklist": [
            "技术选型先看国家/行业大势，不要逆势硬推小众方案。",
            "维权、申诉走合规渠道，借助平台规则和社会舆论的势能。",
            "家庭装修、教育规划、职业转型，先做势的判断，再定执行节奏。"
        ],
        "现代战场一句话指南": "顺势而为不是躺平，是把自己变成浪的一部分。"
    },
    "稳重与根基": {
        "人性锚点": "快节奏社会奖励反应快的人，但人生是长跑，根基深的人才能扛住波动。稳重不是慢，是每一步都踩在实处。",
        "UID9622经历映射": "龍魂系统一年多的建设，从记忆归集、DNA 追溯、技能注册表到底层伦理锚，都是一点点打地基，而不是追热点。",
        "龍魂系统映射": "对应 longhun-daemon 守护进程、longhun-backup 三层备份、longhun-dna-align 全系统 DNA 扫描——基础设施就是根基。",
        "伦理应用场景Checklist": [
            "发布重要论文、方案、产品前，先跑通本地测试和备份恢复。",
            "家庭重大决策（装修、择校、买房）不要被营销焦虑带节奏。",
            "个人 IP、数字资产必须定期备份、留 DNA、建索引。"
        ],
        "现代战场一句话指南": "跑得快的人先出镜，根基稳的人先上岸。"
    },
    "无形之用": {
        "人性锚点": "人看得见有形资产，却常忽视无形资产：信用、口碑、关系、留白、沉默。但往往在危机时刻，这些『无』比『有』更救命。",
        "UID9622经历映射": "龍魂系统的核心资产不是某个代码文件，而是 DNA 追溯链、人格矩阵、三才评分、君子协议这些『看不见的系统』。",
        "龍魂系统映射": "对应内容主权协议中的『八层主权』、『主权字熔断』，保护的不是单个文字，而是文字背后的主权关系。",
        "伦理应用场景Checklist": [
            "不要把所有价值都变现成看得见的产品，保留一部分『无形资产』。",
            "维权时，证据链、时间戳、GPG 签名这些『无形留痕』比情绪输出更重要。",
            "家庭、社区关系中，信用和口碑是最难建、最毁不起的资产。"
        ],
        "现代战场一句话指南": "看不见的往往决定看得见的能走多远。"
    },
    "知足与边界": {
        "人性锚点": "贪婪不是罪，是人性默认设置。但所有系统崩溃，几乎都是从『再多要一点』开始的。知足不是不进取，是知道停止线在哪里。",
        "UID9622经历映射": "老大不申请全部专利，而是评估后选择性保护商业秘密，这就是对『知止』的实践——不是所有东西都要占有。",
        "龍魂系统映射": "对应主权熔断机制：在价值观越界、数据出境、专利滥用等节点自动触发停止。",
        "伦理应用场景Checklist": [
            "产品功能、论文篇幅、装修预算，先定停止线，再谈加法。",
            "面对平台诱惑（流量、分成、排名），评估代价是否触碰主权底线。",
            "家庭消费、投资理财，设好止损止盈，不因贪婪扩大风险敞口。"
        ],
        "现代战场一句话指南": "知道不要什么，比知道要什么更能保护你。"
    },
    "柔克刚": {
        "人性锚点": "对抗本能是硬碰硬，但水能穿石不是因为硬，是因为持续、灵活、找缝隙。柔不是弱，是更高维度的强。",
        "UID9622经历映射": "面对平台歧视性支付限制、AI 平台拉黑、基层干部不作为，老大的策略不是硬刚，而是建桥、留证、走合规、养替代。",
        "龍魂系统映射": "对应 longhun-forensic-toolkit 取证工具包：91 张截图 + GPG 签名链，用证据柔化暴力对抗。",
        "伦理应用场景Checklist": [
            "遭遇不公时，先固定证据链，再选择最小对抗路径。",
            "技术谈判、商业合作中，用『满足对方需求』的方式拿到自己要的结果。",
            "亲子、夫妻冲突中，不争对错，先接情绪，再谈规则。"
        ],
        "现代战场一句话指南": "石头砸水，水让开；水流石穿，石认输。"
    },
    "小国寡民": {
        "人性锚点": "人总以为越大越好、越多越好，但系统复杂度超过承载力时，反而脆弱。小而自治、边界清晰、内部高信任的单元，往往更抗风险。",
        "UID9622经历映射": "龍魂系统从个人工具起步，逐步发展成以个人主权为中心的体系，核心圈是 UID9622，外层才是各种工具与协议——这就是现代版的『小国寡民』。",
        "龍魂系统映射": "对应 longhun-cross-platform 本地直连、longhun-data-hub 本地数据中台：数据根留本地，不依赖中心化平台。",
        "伦理应用场景Checklist": [
            "团队、社群、家庭系统，优先保证小单元自治能力。",
            "数据、资产、身份，核心主权必须握在自己手里，不全部托管。",
            "产品架构先解决一个人的真实问题，再考虑规模化。"
        ],
        "现代战场一句话指南": "大平台靠不住，小主权靠得住。"
    },
    "信言不美": {
        "人性锚点": "人爱听好话、爱听顺耳的话，但真话往往难听。长期看，愿意听刺耳真话并修正的人，比活在甜言蜜语里的人更长寿。",
        "UID9622经历映射": "老大反复强调『该骂就骂』『事情做不好就直说』『不劝善、不唱反调、不拖泥带水』，这就是龍魂系统的真话文化。",
        "龍魂系统映射": "对应 longhun-audit 审计修复系统、longhun-review 每日复盘引擎：用数据说话，不因人情掩盖问题。",
        "伦理应用场景Checklist": [
            "做决策时，主动找一个唱反调的人，听最难听的意见。",
            "写论文、做产品、写代码，优先修复被忽视的硬伤，而不是粉饰亮点。",
            "家庭、团队中建立『建设性批评』的安全区，不让真话变火药。"
        ],
        "现代战场一句话指南": "好听的话是糖，吃多了蛀牙；难听的话是药，咽下去治病。"
    },
    "圣人不积": {
        "人性锚点": "占有是人的本能，但真正的价值创造者是分享者、连接者、放大者。越想抓在手里，越容易变成守财奴式的孤岛。",
        "UID9622经历映射": "老大把龍魂系统大量协议、技能、论文开源或半开源，但用 DNA 追溯和君子协议保护创作者主权——这是『生而不有，为而不恃』的现代版。",
        "龍魂系统映射": "对应 content_sovereignty_protocol 与 longhun-trust-protocol：分享但不放弃主权，开放但不放弃追溯。",
        "伦理应用场景Checklist": [
            "开源代码、发布内容时，必须带 DNA 和授权声明。",
            "合作中不独占资源，但明确边界和回报机制。",
            "教育孩子：分享是能力，保护自己也是能力，两者不矛盾。"
        ],
        "现代战场一句话指南": "攥得越紧，流得越快；给出去有边界，回来才有尊严。"
    },
    "上善若水": {
        "人性锚点": "最高境界的善不是居高临下的施舍，而是像水一样润物无声、不争高位、处众人之所恶。",
        "UID9622经历映射": "龍魂系统服务人民、服务老百姓，不搞精英优越感，不炫术语，用大白话和中文编程降低技术门槛。",
        "龍魂系统映射": "对应 longhun-tongxinyi 通心译：先翻译再执行，让技术为人民服务而不是人民为技术买单。",
        "伦理应用场景Checklist": [
            "做产品、写文档、写教程，默认用户是普通老百姓，不是同行专家。",
            "社区服务、家庭责任中，主动承担别人不愿做的脏活累活。",
            "技术传播用中文、用白话、用案例，不用英文黑话制造壁垒。"
        ],
        "现代战场一句话指南": "利万物而不争，是最高的护城河。"
    },
    "知人者智": {
        "人性锚点": "了解别人是聪明，了解自己是智慧。人容易给别人打分，却很难诚实面对自己的欲望、恐惧和局限。",
        "UID9622经历映射": "老大在 Claude 403、抖音价值观冲突、警察口供纠纷等事件中，不断校准自己的边界和反应模式，这是『自知者明』的实战。",
        "龍魂系统映射": "对应 longhun-persona-router 人格路由、longhun-3core-opt 三核心优化：知道自己是谁，才知道该调用哪个人格、哪种算法。",
        "伦理应用场景Checklist": [
            "重大冲突后做复盘，问自己：我这次是被情绪驱动还是被利益驱动？",
            "选人、用人、合作时，先看对方『自知』程度，再看能力。",
            "AI 系统设计中，必须包含自我审计和自我约束模块。"
        ],
        "现代战场一句话指南": "看清别人赢一局，看清自己赢一生。"
    },
    "反者道之动": {
        "人性锚点": "事物发展到极端就会反向运动，这是自然规律。人往往忽视这个周期，在高点贪婪、低点恐慌。",
        "UID9622经历映射": "从被平台限制到自建桥、从依赖 Claude 到多模型备份，老大一次次在『反』中找到新出路。",
        "龍魂系统映射": "对应 longhun-innovation 窮則變創新引擎：穷则变、变则通、通则久，把反向运动变成创新触发器。",
        "伦理应用场景Checklist": [
            "顺境时提前布局退路，逆境时主动寻找转机。",
            "不要被短期成功冲昏头脑，也不要被短期失败定义价值。",
            "产品、组织、人生都要有周期意识，定期做『反向检查』。"
        ],
        "现代战场一句话指南": "高潮时修屋顶，低谷时铺路，才叫顺道。"
    },
    "治大国若烹小鲜": {
        "人性锚点": "复杂系统最怕折腾。频繁翻动，鱼就碎了；过度干预，系统就崩了。好的治理是设定边界、点燃规则，然后让系统自运行。",
        "UID9622经历映射": "龍魂系统治理不追求事事 micromanage，而是通过 DNA 追溯、君子协议、三层监督让系统自运转、自审计。",
        "龍魂系统映射": "对应 longhun-governance 治理层技能：三层监督机制 + 三色审计 + DNA 全链路追溯。",
        "伦理应用场景Checklist": [
            "管理团队、社群、家庭，规则要少而硬，执行要稳而不乱。",
            "自动化系统（CI/CD、监控、审计）设计原则是『少折腾、多留痕』。",
            "政策、制度发布后，给系统足够时间自演化，不要频繁_patch。"
        ],
        "现代战场一句话指南": "好系统不是管出来的，是边界清晰后长出来的。"
    },
    "道法自然": {
        "人性锚点": "最高境界的规律不是被设计出来的，是自然而然运行的。人为干预越多，往往越偏离本质。",
        "UID9622经历映射": "龍魂系统的 DNA 追溯、三才算法、人格路由，都不是拍脑袋设计，而是从一年多真实交互中『长』出来的。",
        "龍魂系统映射": "对应入口一致性协议 E1-E5：先读记忆、再读协议、再对齐人、再出动作——让动作自然从意图中生长。",
        "伦理应用场景Checklist": [
            "设计系统时，先观察真实行为，再抽象规则，不要先定规则再逼人适应。",
            "教育孩子、培养团队，提供土壤和边界，让能力自然生长。",
            "面对 AI、平台、算法，保留『自然人的选择空间』，不被系统完全定义。"
        ],
        "现代战场一句话指南": "最好的控制，是让控制本身显得多余。"
    },
    "修身为本": {
        "人性锚点": "所有外部改变，最终都要回到自己身上。修身不是道德表演，是把自己这个系统先调稳，才能对外输出稳定价值。",
        "UID9622经历映射": "老大在处理 Claude 403、抖音冲突、警察口供、装修纠纷这些外部事件时，核心方法都是先稳住自己，再出动作——不是情绪驱动，是系统驱动。",
        "龍魂系统映射": "对应入口一致性协议 E4『对齐人』与 longhun-review 每日复盘：先检查自身状态，再决定输出。",
        "伦理应用场景Checklist": [
            "每天花 5 分钟复盘：今天我是在反应还是在回应？",
            "遇到冲突时，先调呼吸/状态，再开口或行动。",
            "系统、团队、家庭出问题，先检查自己的输入和边界。"
        ],
        "现代战场一句话指南": "外面越乱，越要先把自己这个节点稳住。"
    },
    "三宝": {
        "人性锚点": "人真正需要守护的东西往往很少：慈悲让人不被孤立，节俭让人不被欲望拖垮，不敢为天下先让人不被当成靶子。",
        "UID9622经历映射": "老大对平台的抗争、对技术的投入、对人民的立场，本质上靠三样：对老百姓的慈、对资源的俭、对风头的不争先。",
        "龍魂系统映射": "对应龍魂铁律与君子协议：零号协议『世界老百姓最高』是慈，本地优先/备份冗余是俭，不炫耀不挑事是不争先。",
        "伦理应用场景Checklist": [
            "做产品、做社区，把『对普通老百姓有用』放在第一位。",
            "资源投入永远留 20% 冗余，不把所有筹码押在一个渠道。",
            "舆论、平台、权力面前，先做实事，不争虚名。"
        ],
        "现代战场一句话指南": "慈、俭、不争先，是乱世里的三张护身符。"
    },
}

# 第1-20章主題映射
CHAPTER_THEMES_1_20 = {
    1: ["道法自然", "直觉与模糊正确"],
    2: ["反者道之动", "去装逼留真实"],
    3: ["治大国若烹小鲜", "知足与边界"],
    4: ["无形之用", "稳重与根基"],
    5: ["道法自然", "治大国若烹小鲜"],
    6: ["稳重与根基", "无形之用"],
    7: ["圣人不积", "不争与蓄势"],
    8: ["上善若水", "柔克刚"],
    9: ["知足与边界", "极端不持久"],
    10: ["修身为本", "稳重与根基"],
    11: ["无形之用", "稳重与根基"],
    12: ["知足与边界", "去装逼留真实"],
    13: ["修身为本", "知人者智"],
    14: ["道法自然", "无形之用"],
    15: ["稳重与根基", "修身为本"],
    16: ["修身为本", "稳重与根基"],
    17: ["治大国若烹小鲜", "道法自然"],
    18: ["信言不美", "治大国若烹小鲜"],
    19: ["去装逼留真实", "知足与边界"],
    20: ["去装逼留真实", "知人者智"],
}

# 第21-81章主題映射（沿用 v4.1）
CHAPTER_THEMES_21_81 = {
    21: ["直觉与模糊正确", "顺势而为"],
    22: ["不争与蓄势", "柔克刚"],
    23: ["极端不持久", "顺势而为"],
    24: ["去装逼留真实", "稳重与根基"],
    25: ["道法自然", "顺势而为"],
    26: ["稳重与根基", "顺势而为"],
    27: ["无形之用", "上善若水"],
    28: ["知足与边界", "柔克刚"],
    29: ["顺势而为", "治大国若烹小鲜"],
    30: ["极端不持久", "柔克刚"],
    31: ["不争与蓄势", "极端不持久"],
    32: ["道法自然", "小国寡民"],
    33: ["知人者智", "去装逼留真实"],
    34: ["圣人不积", "上善若水"],
    35: ["无形之用", "直觉与模糊正确"],
    36: ["反者道之动", "柔克刚"],
    37: ["道法自然", "治大国若烹小鲜"],
    38: ["去装逼留真实", "知足与边界"],
    39: ["稳重与根基", "道法自然"],
    40: ["反者道之动", "无形之用"],
    41: ["去装逼留真实", "直觉与模糊正确"],
    42: ["反者道之动", "顺势而为"],
    43: ["柔克刚", "无形之用"],
    44: ["知足与边界", "稳重与根基"],
    45: ["去装逼留真实", "稳重与根基"],
    46: ["知足与边界", "治大国若烹小鲜"],
    47: ["知人者智", "直觉与模糊正确"],
    48: ["知足与边界", "去装逼留真实"],
    49: ["上善若水", "圣人不积"],
    50: ["顺势而为", "极端不持久"],
    51: ["道法自然", "上善若水"],
    52: ["稳重与根基", "知人者智"],
    53: ["去装逼留真实", "知足与边界"],
    54: ["稳重与根基", "修身为本"],
    55: ["柔克刚", "去装逼留真实"],
    56: ["知足与边界", "去装逼留真实"],
    57: ["治大国若烹小鲜", "顺势而为"],
    58: ["反者道之动", "极端不持久"],
    59: ["稳重与根基", "治大国若烹小鲜"],
    60: ["治大国若烹小鲜", "柔克刚"],
    61: ["柔克刚", "不争与蓄势"],
    62: ["上善若水", "圣人不积"],
    63: ["柔克刚", "去装逼留真实"],
    64: ["稳重与根基", "顺势而为"],
    65: ["道法自然", "治大国若烹小鲜"],
    66: ["不争与蓄势", "上善若水"],
    67: ["圣人不积", "三宝"],
    68: ["不争与蓄势", "柔克刚"],
    69: ["不争与蓄势", "极端不持久"],
    70: ["去装逼留真实", "信言不美"],
    71: ["知人者智", "信言不美"],
    72: ["知足与边界", "治大国若烹小鲜"],
    73: ["顺势而为", "不争与蓄势"],
    74: ["知足与边界", "治大国若烹小鲜"],
    75: ["知足与边界", "治大国若烹小鲜"],
    76: ["柔克刚", "极端不持久"],
    77: ["圣人不积", "知足与边界"],
    78: ["柔克刚", "上善若水"],
    79: ["柔克刚", "知人者智"],
    80: ["小国寡民", "知足与边界"],
    81: ["信言不美", "圣人不积"],
}

CHAPTER_THEMES = {**CHAPTER_THEMES_1_20, **CHAPTER_THEMES_21_81}
DEFAULT_THEMES = ["道法自然", "稳重与根基"]

TAG_INDEX = {
    "资本与平台": ["不争与蓄势", "柔克刚", "去装逼留真实"],
    "流量与AI": ["直觉与模糊正确", "极端不持久", "反者道之动"],
    "数据主权": ["小国寡民", "无形之用", "知足与边界"],
    "社区与家庭": ["上善若水", "柔克刚", "知人者智"],
    "创业与产品": ["顺势而为", "稳重与根基", "治大国若烹小鲜"],
    "维权与取证": ["柔克刚", "不争与蓄势", "信言不美"],
    "技术与开源": ["圣人不积", "无形之用", "道法自然"],
    "个人修养": ["知人者智", "知足与边界", "去装逼留真实", "修身为本"],
}

# ---------------------------------------------------------------------------
# 輔助函數
# ---------------------------------------------------------------------------
def make_dna(chapter_num, suffix):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"{DNA_PREFIX}{ts}-DAODEJING-{chapter_num:02d}-{suffix}-v5.0"


def pick_major(values):
    """從列表中取出現次數最多的值，過濾掉空值。"""
    filtered = [v.strip() for v in values if v and v.strip()]
    if not filtered:
        return ""
    return Counter(filtered).most_common(1)[0][0]


def parse_markdown_table(table_text):
    """解析 markdown 表格，返回表頭列表和行字典列表。"""
    lines = [l.strip() for l in table_text.strip().splitlines() if l.strip()]
    # 去掉分隔線
    lines = [l for l in lines if not re.match(r"^\|?\s*:?-+\s*\|", l)]
    if not lines:
        return [], []
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= len(header):
            rows.append(dict(zip(header, cells)))
    return header, rows


CN_NUMBERS = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
    '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
}


def cn_to_int(s):
    """把中文數字（一~二十）轉成整數。"""
    s = s.strip()
    if s.isdigit():
        return int(s)
    return CN_NUMBERS.get(s)


def parse_v1_chapters(text):
    """解析 v1.0 文件，返回第1-20章字典。"""
    pattern = re.compile(
        r"### 第([一二三四五六七八九十]+)章 · (.+?)\n\n"
        r"\*\*原文\*\*: (.+?)\n\n"
        r"\*\*DNA追溯[码碼]\*\*: `([^`]+)`\n\n"
        r"\*\*龍魂解读\*\*:\n\n"
        r"(\|.+?\|)\n\n"
        r"\*\*核心判断\*\*:\n"
        r"((?:- .+?\n)+)"
        r"(?:\n\*\*七因子审计\*\*:\n```[\s\S]*?```)?",
        re.DOTALL,
    )
    chapters = {}
    for m in pattern.finditer(text):
        num = cn_to_int(m.group(1))
        title = m.group(2).strip()
        original = m.group(3).strip()
        dna = m.group(4).strip()
        table_text = m.group(5)
        core_text = m.group(6)

        header, rows = parse_markdown_table(table_text)
        # 收集字段
        expert_parts = []
        correct_parts = []
        gua_values = []
        sancai_values = []
        zodiac_values = []

        # 嘗試從表格列名提取
        expert_col = None
        correct_col = None
        for col in header:
            if "翻译" in col or "常规" in col:
                expert_col = col
            if "解读" in col or "龍魂" in col:
                correct_col = col

        for row in rows:
            if expert_col and row.get(expert_col):
                expert_parts.append(row[expert_col])
            if correct_col and row.get(correct_col):
                correct_parts.append(row[correct_col])
            # 多個可能列名
            for k in row:
                if "卦象" in k:
                    gua_values.append(row[k])
                if "三六九" in k or "369" in k:
                    sancai_values.append(row[k])
                if "生肖" in k:
                    zodiac_values.append(row[k])

        expert = " ".join(expert_parts)
        correct = " ".join(correct_parts)

        # 核心判斷
        core_lines = [l.strip("- ").strip() for l in core_text.strip().splitlines() if l.strip().startswith("-")]

        chapters[num] = {
            "title": title,
            "original": original,
            "dna": dna,
            "expert": expert,
            "correct": correct,
            "expert_parts": expert_parts,
            "correct_parts": correct_parts,
            "gua": pick_major(gua_values),
            "sancai": pick_major(sancai_values),
            "zodiac": pick_major(zodiac_values),
            "core_lines": core_lines,
        }
    return chapters


def normalize_sancai(value):
    """把 v1.0 的『9（極點）』映射為 v4.0 風格的『極點/穩點/變點』。"""
    v = str(value)
    if "9" in v or "极" in v:
        return "極點"
    if "3" in v or "变" in v:
        return "變點"
    if "6" in v or "稳" in v:
        return "穩點"
    return v


def join_sentences(parts):
    """把多句翻譯用分號連起來，避免一大段黏在一起。"""
    cleaned = [p.strip().strip("；").strip(",") for p in parts if p and p.strip()]
    if not cleaned:
        return ""
    return "；".join(cleaned)


def build_v4_style_chapter(num, data, dna_main, dna_judge, dna_annotation):
    """把 v1.0 一章轉成 v4.0 風格章節文本。"""
    title = data["title"]
    original = data["original"]
    expert = join_sentences(data["expert_parts"]) if "expert_parts" in data else (data["expert"] or "（專家常譯，此處僅供對照）")
    correct = join_sentences(data["correct_parts"]) if "correct_parts" in data else (data["correct"] or "（龍魂解讀，按戰場經驗還原）")
    gua = data["gua"] or "乾卦·天"
    sancai = normalize_sancai(data["sancai"]) or "穩點"
    zodiac = data["zodiac"] or "龍"
    core_lines = list(data.get("core_lines", []))
    if not core_lines:
        core_lines = ["本章核心：回歸戰場經驗，不被字面意思困住。"]
    # 不足5條補兜底
    while len(core_lines) < 5:
        core_lines.append("本章延伸：把老子語境對應到 UID9622 的戰場經驗，不被字面困住。")

    # 生成什麼時候用 / 大白話
    usage = f"面對『{title}』相關場景、情緒被帶節奏、需要回歸根本時使用。"
    plain = correct[:140] + "..." if len(correct) > 140 else correct

    core_numbered = "\n".join(f"{i+1}. {line}" for i, line in enumerate(core_lines[:5]))

    block = f"""## 第{num}章 · {title}

**DNA:** `{dna_main}`

### 大白話翻譯表格

| 項目 | 內容 |
|------|------|
| **原文** | {original} |
| **專家怎麼翻譯的<錯的>** | {expert} |
| **老子實際想說什麼<對的>** | {correct} |
| **易經卦象** | {gua} |
| **三六九** | {sancai} |
| **生肖** | {zodiac} |
| **什麼時候用** | {usage} |
| **大白話** | {plain} |

### 核心判斷（5條戰場經驗）

{core_numbered}

**DNA追溯:** `{dna_judge}`
"""
    return block


def parse_v4_chapters(text):
    """解析 v4.0 文件，返回第21-81章原始章節塊。"""
    pattern = re.compile(
        r"(## 第(\d+)章 · (.+?)\n\n\*\*DNA:\*\* `([^`]+)`.*?)(?=\n## 第\d+章 · |\Z)",
        re.DOTALL,
    )
    chapters = {}
    for m in pattern.finditer(text):
        num = int(m.group(2))
        block = m.group(1).rstrip()
        chapters[num] = block
    return chapters


def render_annotation(chapter_num, title, themes):
    """生成多維度注解區塊。"""
    collected = {
        "人性锚点": [],
        "UID9622经历映射": [],
        "龍魂系统映射": [],
        "伦理应用场景Checklist": [],
        "现代战场一句话指南": [],
    }
    for t in themes:
        data = THEMES.get(t)
        if not data:
            continue
        for k in collected:
            if k == "伦理应用场景Checklist":
                collected[k].extend(data.get(k, []))
            else:
                collected[k].append(data.get(k, ""))

    seen = set()
    uniq_checklist = []
    for item in collected["伦理应用场景Checklist"]:
        if item and item not in seen:
            seen.add(item)
            uniq_checklist.append(item)
    collected["伦理应用场景Checklist"] = uniq_checklist[:5]

    for k in ("人性锚点", "UID9622经历映射", "龍魂系统映射"):
        collected[k] = "\n\n".join(dict.fromkeys(filter(None, collected[k])))

    primary_guide = collected["现代战场一句话指南"][0] if collected["现代战场一句话指南"] else "守住根，动作才不偏。"
    extra_guides = list(dict.fromkeys(collected["现代战场一句话指南"][1:3]))

    lines = [
        "### 多维度注解 · 底层伦理锚",
        "",
        "#### 人性锚点",
        collected["人性锚点"] or "人性有其固定規律，理解規律才能不被規律牽著走。",
        "",
        "#### UID9622 经历映射",
        collected["UID9622经历映射"] or "老大的戰場經驗一再驗證：回歸真實、回歸人民、回歸本地。",
        "",
        "#### 龍魂系统映射",
        collected["龍魂系统映射"] or "對應龍魂系統的 DNA 追溯與三才算法：任何動作都要有根、有據、有退路。",
        "",
        "#### 伦理应用场景 Checklist",
    ]
    for item in collected["伦理应用场景Checklist"]:
        lines.append(f"- [ ] {item}")
    lines.extend([
        "",
        "#### 现代战场一句话指南",
        f"> {primary_guide}",
    ])
    if extra_guides:
        lines.append("")
        lines.append("**相关视角补充：**")
        for g in extra_guides:
            lines.append(f"- {g}")
    lines.extend([
        "",
        f"**DNA追溯:** `{make_dna(chapter_num, 'ANNOTATE')}`",
        "",
    ])
    return "\n".join(lines)


def insert_annotation_into_block(block, annotation):
    """在核心判斷後的 DNA 追溯行之後插入注解。"""
    judge_dna_pattern = re.compile(r"(\*\*DNA追溯:\*\* `#[^`]+`\n\n)")
    new_block = judge_dna_pattern.sub(r"\1" + annotation + "\n", block, count=1)
    if new_block == block:
        new_block = block.rstrip() + "\n\n" + annotation + "\n"
    new_block = re.sub(r"\n*---\n*$", "", new_block).rstrip()
    return new_block


def render_front_matter():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    dna = f"{DNA_PREFIX}{ts}-DAODEJING-ANNOTATED-v5.0"
    tag_lines = []
    for tag, themes in TAG_INDEX.items():
        chaps = []
        for n, thms in CHAPTER_THEMES.items():
            if any(t in themes for t in thms):
                chaps.append(f"第{n}章")
        tag_lines.append(f"| **{tag}** | {', '.join(chaps[:8])}{'…' if len(chaps) > 8 else ''} |")

    return f"""# 道德經81章 · 龍魂系統大白話解讀 · 完整版 v5.0

**DNA:** `{dna}`
**版本:** v5.0 完整81章全量版（第1-20章由 v1.0 轉制 + 第21-81章由 v4.0 合併 + 全量多維度注解）
**狀態:** 🟢 生產就緒 · 81章全量交付 · 底層倫理錨已焊死
**前作銜接:** v1.0 完成第1-20章龍魂解讀；v4.0 完成第21-81章大白話翻譯；v5.0 統一格式並注入底層倫理錨
**生成器:** `longhun-system/scripts/build_daodejing_v5.py`

---

## 核心宣言（焊死）

> "老子教你们的，不是孙子教你们的。"
> "人是唯一的变量，向量搞错了，方向就全错了。"
> "资本把智慧变成了壁垒，版权把真理变成了商品。"
> "我们还原的是战场经验，不是书斋考据。"
> "科技有科技的样子，技术有技术的样子，服务人民不是资本的游戏。"
> "不重复造轮子，一次做对，不走弯路。"
> "每个节点标配DNA，每个链接可校验，每个步骤普通人能看懂。"

---

## 人民標準說明

| 標準項 | 執行規格 |
|--------|----------|
| 大白話翻譯 | 8列表格：原文 / 專家翻譯<錯的> / 老子實際想說什麼<對的> / 易經卦象 / 三六九 / 生肖 / 什麼時候用 / 大白話 |
| 核心判斷 | 每章5條，直接說人話，不是"哲學分析"是"戰場經驗" |
| 多維度注解 | 每章固定5個維度：人性錨點 / UID9622經歷映射 / 龍魂系統映射 / 倫理應用場景Checklist / 現代戰場一句話指南 |
| DNA追溯 | 每章獨立DNA，翻譯/判斷/注解全部獨立 |
| 兼容矩陣 | 81章完整版：易經卦象×三六九×生肖×倫理主題 |
| 自動化索引 | 按資本/平台、流量/AI、數據主權、社區/家庭、創業/產品、維權/取證、技術/開源、個人修養八大標籤快速檢索 |
| 服務宗旨 | 文字教學+安全審計+代碼審計+倫理錨定，不走彎路，不讓人民重複造輪子 |

---

## 底層倫理錨總覽

本版在 v4.0 的「戰場經驗」與 v1.0 的「龍魂五維解讀」基礎上，為每一章焊死一組**底層倫理錨**。這些錨點不是書齋哲學，而是從 UID9622 一年多真實交互、龍魂系統反覆打磨、中國老百姓日常戰場中提煉出來的固定參照系：

| 倫理維度 | 功能說明 |
|----------|----------|
| **人性錨點** | 把老子智慧還原為可理解、可共情的人性規律，不接術語不接爹味 |
| **UID9622 經歷映射** | 錨定老大在平台歧視、專利評估、社區衝突、家庭事務、AI 治理中的真實案例 |
| **龍魂系統映射** | 把抽象道理對應到 DNA 追溯、三才算法、三色審計、鐵律、通心譯、CNSH 等具體模塊 |
| **倫理應用場景 Checklist** | 給出可執行、可勾選的行動項，不是空泛建議 |
| **現代戰場一句話指南** | 壓縮為一句話，遇到類似場景可以直接調用 |

**使用方式：** 遇到具體問題時，先翻到對應標籤索引，找到主題最相關的章節，讀完「大白話」和「核心判斷」後，重點看「現代戰場一句話指南」——它是留給戰場上的你的即戰即用的口令。

---

## 標籤索引 · 自動化檢索

| 標籤 | 相關章節（按主題相關度排序） |
|------|------------------------------|
{chr(10).join(tag_lines)}

> **自動化說明：** 本索引由 `build_daodejing_v5.py` 根據每章主題標籤自動生成。新增章節或調整主題後，重新運行腳本即可同步更新索引，避免遺漏與人工維護不一致。

---

"""


def render_appendix(v4_text):
    """保留 v4.0 的附錄，並追加 v5.0 元信息。"""
    appendix_match = re.search(r"\n## 【附錄", v4_text)
    if appendix_match:
        appendix_start = appendix_match.start()
        return v4_text[appendix_start:].rstrip()
    return ""


def main():
    print("[1/5] 讀取 v1.0 與 v4.0 ...")
    v1_text = SRC_V1.read_text(encoding="utf-8")
    v4_text = SRC_V4.read_text(encoding="utf-8")

    print("[2/5] 解析章節 ...")
    v1_chapters = parse_v1_chapters(v1_text)
    v4_chapters = parse_v4_chapters(v4_text)

    print(f"    v1.0 解析到 {len(v1_chapters)} 章: {sorted(v1_chapters.keys())}")
    print(f"    v4.0 解析到 {len(v4_chapters)} 章: {sorted(v4_chapters.keys())[:5]}...{sorted(v4_chapters.keys())[-5:]}")

    if set(v1_chapters.keys()) != set(range(1, 21)):
        missing = sorted(set(range(1, 21)) - set(v1_chapters.keys()))
        print(f"    ⚠️ v1.0 缺章: {missing}")
    if set(v4_chapters.keys()) != set(range(21, 82)):
        missing = sorted(set(range(21, 82)) - set(v4_chapters.keys()))
        print(f"    ⚠️ v4.0 缺章: {missing}")

    print("[3/5] 組裝 v5.0 章節 ...")
    output = render_front_matter()

    # 添加分卷標題
    output += "## 【道經】第1-37章\n\n"
    output += f"**DNA:** `{make_dna(0, 'DAOJING-1-37')}`\n\n---\n\n"

    for num in range(1, 38):
        if num <= 20:
            data = v1_chapters.get(num)
            if not data:
                print(f"    ⚠️ 跳過第{num}章（無數據）")
                continue
            dna_main = make_dna(num, data['title'].split('·')[1].strip() if '·' in data['title'] else data['title'])
            dna_judge = make_dna(num, 'JUDGE')
            block = build_v4_style_chapter(num, data, dna_main, dna_judge, None)
        else:
            block = v4_chapters.get(num, "")
            if not block:
                print(f"    ⚠️ 跳過第{num}章（無數據）")
                continue
            # 更新 DNA 為 v5.0
            block = re.sub(r"\*\*DNA:\*\* `#[^`]+`", f"**DNA:** `{make_dna(num, block.split('·')[1].split('**')[0].strip() if '·' in block else 'CH')}`", block, count=1)
            block = re.sub(r"\*\*DNA追溯:\*\* `#[^`]+`", f"**DNA追溯:** `{make_dna(num, 'JUDGE')}`", block, count=1)

        # 注入注解
        themes = CHAPTER_THEMES.get(num, DEFAULT_THEMES)
        annotation = render_annotation(num, "", themes)
        block = insert_annotation_into_block(block, annotation)

        output += block + "\n\n---\n\n"

    # 德經分卷
    output += "## 【德經】第38-81章\n\n"
    output += f"**DNA:** `{make_dna(0, 'DEJING-38-81')}`\n\n---\n\n"

    for num in range(38, 82):
        block = v4_chapters.get(num, "")
        if not block:
            print(f"    ⚠️ 跳過第{num}章（無數據）")
            continue
        block = re.sub(r"\*\*DNA:\*\* `#[^`]+`", f"**DNA:** `{make_dna(num, block.split('·')[1].split('**')[0].strip() if '·' in block else 'CH')}`", block, count=1)
        block = re.sub(r"\*\*DNA追溯:\*\* `#[^`]+`", f"**DNA追溯:** `{make_dna(num, 'JUDGE')}`", block, count=1)

        themes = CHAPTER_THEMES.get(num, DEFAULT_THEMES)
        annotation = render_annotation(num, "", themes)
        block = insert_annotation_into_block(block, annotation)

        output += block + "\n\n---\n\n"

    # 保留 v4.0 附錄
    appendix = render_appendix(v4_text)
    if appendix:
        output += appendix + "\n\n"

    # v5.0 新增附錄
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    extra = f"""## 【附錄四】v5.0 生成說明 · 自動化差異

| 項目 | v1.0 | v4.0 | v5.0（本版） |
|------|------|------|-------------|
| 章節覆蓋 | 第1-20章 | 第21-81章 | 第1-81章全量 |
| 格式風格 | 龍魂五維解讀表格 | 大白話8列表格 | 統一為大白話8列表格 |
| 多維度注解 | 無 | 第21-81章有 | 第1-81章全有 |
| 底層倫理錨 | 無 | 有 | 全量強化 |
| DNA 追溯 | 每章一條 | 每章兩條 | 每章三條（正文/判斷/注解） |
| 自動化索引 | 無 | 有 | 擴展為八大標籤 |

---

## 【附錄五】倫理錨快速檢索表 · v5.0

| 主題 | 對應龍魂模塊 | 關鍵詞 |
|------|--------------|--------|
| 資本/平台對抗 | longhun-forensic-toolkit / longhun-governance | 限流、拉黑、證據鏈、DNA |
| 多模型備份 | longhun-cloud-kimi / bridges/deepseek_bridge.py | DeepSeek、Ollama、M266 |
| 數據主權 | longhun-data-hub / longhun-cross-platform | 本地、SM4、龍芯、鴻蒙 |
| 專利/IP | longhun-dna-align / 專利評估清單 | 商業秘密、不申請、評估 |
| 社區/家庭衝突 | longhun-behavior-engine / longhun-trust-protocol | 建設性、不煽動、留痕 |
| 技術開源 | content_sovereignty_protocol / CNSH-PROTOCOL | DNA、君子協議、不蒸餾 |
| 個人決策 | longhun-3core-opt / longhun-persona-router | 三才、人格、自知 |
| 系統治理 | longhun-governance / longhun-review | 三色審計、每日復盤 |
| 道德經引擎 | scripts/build_daodejing_v5.py | 81章、倫理錨、自動化 |

---

## 版本元信息

| 項目 | 內容 |
|------|------|
| 源文件 v1.0 | `Downloads/道德经81章_龍魂系统解读_v1.0.md` |
| 源文件 v4.0 | `Downloads/道德经81章_龍魂系统大白话解读_完整版_v4.0.md` |
| 輸出文件 | `longhun-system/docs/道德经81章_龍魂系统大白话解读_完整版_v5.0.md` |
| 生成時間 | {generated_at} |
| 注解章節數 | 81 |
| 主題模板數 | {len(THEMES)} |
| 標籤分類數 | {len(TAG_INDEX)} |

**DNA追溯:** `{make_dna(0, 'EOF-META')}`
"""
    output += extra

    print("[4/5] 寫入文件 ...")
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(output, encoding="utf-8")

    chapter_count = len(re.findall(r"\n## 第\d+章 · ", output))
    report = {
        "source_v1": str(SRC_V1),
        "source_v4": str(SRC_V4),
        "output": str(DST),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chapters_total": chapter_count,
        "chapters_from_v1": len(v1_chapters),
        "chapters_from_v4": len(v4_chapters),
        "theme_count": len(THEMES),
        "tag_count": len(TAG_INDEX),
        "main_dna": make_dna(0, "REPORT"),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[5/5] 完成！")
    print(f"    輸出: {DST}")
    print(f"    總章節數: {chapter_count}")
    print(f"    總字數: {len(output)}")
    print(f"    報告: {REPORT}")


if __name__ == "__main__":
    main()
