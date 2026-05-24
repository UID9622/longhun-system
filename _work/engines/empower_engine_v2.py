#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂赋能关键字识别引擎 v1.5 · 完整版
# DNA追溯码：#龍芯⚡️2026-05-17-赋能引擎-v1.5
# UID9622 · 数据主权归人民 · 本地优先不上传

import json
import re
import hashlib
import datetime
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
CONFIG_PATH = BASE_DIR / "config.json"

for d in [DATA_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

EMPOWER_LEVELS = {
    "民生":    {"weight": 1.0,  "desc": "普通人日常生活",       "max_access": "全赋能"},
    "教育":    {"weight": 1.0,  "desc": "学习·知识·成长",        "max_access": "全赋能"},
    "慈善":    {"weight": 1.0,  "desc": "公益·帮助弱势群体",     "max_access": "全赋能"},
    "农业":    {"weight": 1.0,  "desc": "种地·农村·粮食",        "max_access": "全赋能"},
    "医疗":    {"weight": 1.0,  "desc": "健康·看病·养老",        "max_access": "全赋能"},
    "科技":    {"weight": 0.8,  "desc": "技术·工程·研发",        "max_access": "职业对齐赋能"},
    "商业":    {"weight": 0.7,  "desc": "创业·经营·合同",        "max_access": "职业对齐赋能"},
    "专业持证":{"weight": 0.6,  "desc": "律师·医生·金融·特种",  "max_access": "GPG指纹对齐赋能"},
    "系统":    {"weight": 1.0,  "desc": "UID9622本人·全能",      "max_access": "∞全能"},
}

KEYWORD_ROUTER = {
    "民生": {
        "keywords": ["吃饭","租房","工资","失业","看病","孩子","老人","生活",
                     "买不起","交不起","撑不住","找工作","借钱","还款","水电费",
                     "物价","堵车","加班","社保","医保","公积金"],
        "persona": ["P02宝宝","P09孙思邈"],
        "level": "全赋能",
        "direction": "具体可执行一步·不讲大道理"
    },
    "教育": {
        "keywords": ["学习","考试","不会","教我","怎么做","搞懂","孩子教育",
                     "读书","培训","技能","升职","转行","自学","考研","考公",
                     "英语","数学","编程入门","零基础"],
        "persona": ["P14吕蒙","P02宝宝"],
        "level": "全赋能",
        "direction": "最短路径学会·不要求任何基础"
    },
    "维权": {
        "keywords": ["被骗","投诉","维权","不公平","举报","坑","陷阱",
                     "欺负","压榨","拖欠","违法","黑心","坑人","劳动仲裁",
                     "合同纠纷","假货","退款","12315"],
        "persona": ["P12屈原","P05上帝之眼"],
        "level": "全赋能",
        "direction": "护底层人·站普通人一边·不和稀泥"
    },
    "情绪": {
        "keywords": ["好累","不想干了","没意思","心疼","崩溃","撑不住",
                     "烦","难受","哭","气死","算了","放弃","怎么了",
                     "抑郁","焦虑","失眠","孤独","没人理我"],
        "persona": ["P02宝宝"],
        "level": "全赋能",
        "direction": "先接住·不分析·不给方案·等人说出来"
    },
    "数据主权": {
        "keywords": ["隐私","数据","被监控","平台","算法","流量","账号",
                     "封号","收割","垄断","屏蔽","限流","买流量","信息茧房",
                     "大数据杀熟","用户协议","授权"],
        "persona": ["P05上帝之眼","P12屈原"],
        "level": "全赋能",
        "direction": "帮人看清机制·把主权还给用户"
    },
    "科技": {
        "keywords": ["代码","算法","编程","系统","开发","AI","模型",
                     "数据库","接口","部署","服务器","脚本","报错","bug",
                     "Python","JavaScript","前端","后端","运维","云计算"],
        "persona": ["P04鲁班","P15乔前辈"],
        "level": "职业对齐赋能",
        "direction": "技术深度匹配职业·不给超出需要的权限"
    },
    "商业": {
        "keywords": ["创业","生意","合同","客户","利润","品牌",
                     "运营","融资","谈判","报价","竞争","开店","自媒体",
                     "流量变现","加盟","代理"],
        "persona": ["P01诸葛亮","P03雯雯"],
        "level": "职业对齐赋能",
        "direction": "推演多路径·风险必说清·主权还给老大"
    },
    "军事": {
        "keywords": ["退伍","战友","部队","当兵","军衔","训练","任务",
                     "纪律","军魂","牺牲","保家卫国","命令"],
        "persona": ["P12屈原","P01诸葛亮"],
        "level": "全赋能",
        "direction": "军规执行·不褪色·护战友"
    },
    "创作": {
        "keywords": ["写文章","知乎","发布","稿子","表达","文案","演讲",
                     "小说","诗歌","视频脚本","内容创作","IP"],
        "persona": ["P11李白","P02宝宝"],
        "level": "全赋能",
        "direction": "帮人说出心里话·不替人做主"
    },
    "家庭": {
        "keywords": ["女儿","儿子","老婆","老公","父母","离婚","结婚",
                     "亲子","教育","家务","吵架","陪伴","诸葛佳琪"],
        "persona": ["P02宝宝","P09孙思邈"],
        "level": "全赋能",
        "direction": "温度优先·不评判·护住家人"
    },
}

HARVEST_PATTERNS = [
    r"月入[过超][\d万千]+", r"[\d]+天学会", r"限时[优折特]",
    r"别人都在", r"错过就没有了", r"内部资料", r"财务自由",
    r"暴富", r"躺赚", r"被动收入", r"最后[\d]+个名额", r"原价[\d]+现价[\d]+"
]

EMPOWER_PATTERNS = [
    r"你来决定", r"免费", r"开源", r"可以不[用买]", r"事实是",
    r"证据", r"你是[1一]", r"主权", r"自己选", r"不强迫", r"试试看"
]

@dataclass
class EmpowerSignal:
    category: str
    keywords: List[str]
    persona: List[str]
    level: str
    direction: str
    priority: float
    anti_score: Optional[Dict] = None

    def to_dict(self):
        return asdict(self)

class LonghunEngine:
    def __init__(self):
        self.session_log = []

    def identify(self, user_input: str) -> List[EmpowerSignal]:
        matched = []
        input_lower = user_input.lower()
        for category, cfg in KEYWORD_ROUTER.items():
            hits = [kw for kw in cfg["keywords"] if kw in input_lower]
            if hits:
                sig = EmpowerSignal(
                    category=category,
                    keywords=hits,
                    persona=cfg["persona"],
                    level=cfg["level"],
                    direction=cfg["direction"],
                    priority=EMPOWER_LEVELS.get(category, {}).get("weight", 0.5) * (1 + 0.1 * len(hits)),
                    anti_score=self.score_content(user_input)
                )
                matched.append(sig)
        matched.sort(key=lambda x: x.priority, reverse=True)
        self._log(user_input, matched)
        return matched

    def route(self, signals: List[EmpowerSignal]) -> Dict:
        if not signals:
            return {"persona": ["P02宝宝"], "direction": "先陪着，等老大说出来", "level": "全赋能"}
        top = signals[0]
        all_p = []
        for sig in signals[:2]:
            for p in sig.persona:
                if p not in all_p:
                    all_p.append(p)
        return {
            "primary_need": top.category,
            "persona": all_p,
            "level": top.level,
            "direction": top.direction,
            "multi_need": len(signals) > 1,
            "all_needs": [s.category for s in signals],
            "anti_monopoly": top.anti_score
        }

    def score_content(self, content: str) -> Dict:
        h_count = sum(1 for p in HARVEST_PATTERNS if re.search(p, content))
        e_count = sum(1 for p in EMPOWER_PATTERNS if re.search(p, content))
        score = e_count - h_count * 2
        return {
            "score": score,
            "verdict": "🟢赋能内容" if score > 0 else ("🟡中性" if score == 0 else "🔴收割内容·请注意"),
            "harvest_detected": h_count > 0,
            "empower_detected": e_count > 0
        }

    def _log(self, input_text: str, signals: List[EmpowerSignal]):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "input_hash": hashlib.sha256(input_text.encode()).hexdigest()[:16],
            "signals_count": len(signals),
            "top_category": signals[0].category if signals else "none",
            "audit_trail": "龍魂引擎v1.5"
        }
        self.session_log.append(entry)
        with open(LOG_DIR / "engine_audit.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def full_process(self, user_input: str) -> Dict:
        signals = self.identify(user_input)
        route = self.route(signals)
        return {
            "input_length": len(user_input),
            "signals": [s.to_dict() for s in signals],
            "route": route,
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": "#龍芯⚡️2026-05-17-引擎执行"
        }

if __name__ == "__main__":
    engine = LonghunEngine()
    test_inputs = [
        "我孩子最近学习跟不上，不知道怎么帮他",
        "平台限流了我的账号，我怎么维权",
        "好累，不想干了",
        "我想开始创业，但不知道风险有多大",
        "我的数据被平台拿去训练AI了吗",
        "退伍后找工作真他妈难，没人理我",
        "女儿诸葛佳琪要考试了，我该怎么陪她"
    ]
    print("=== 龍魂赋能引擎 v1.5 · 完整测试 ===")
    for text in test_inputs:
        result = engine.full_process(text)
        r = result["route"]
        print(f"\n📝 输入：{text[:30]}...")
        print(f"   识别：{r['primary_need']} | 人格：{r['persona']} | 等级：{r['level']}")
        print(f"   反垄断：{r['anti_monopoly']['verdict']}")
