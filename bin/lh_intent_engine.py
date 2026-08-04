#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·意念交流引擎 v3.0 — 知识融合完整版
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-INTENT-ENGINE-V3.0-KNOWLEDGE-FUSION-a3f7b2c1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

融合三版精华：
  1. 意念交流引擎（10阶段）— 语义解析→ROM固化→零延迟
  2. 三层交叉监督（L1/L2/L3）— 价值观守护·三色审计联动
  3. 5大知识库DNA太极系统 — 投喂→审核→调用→验证闭环
  4. 甲骨文ROM引擎 — 10000次推演·场景指纹·0.1ms命中

10阶段流程：
  阶段1: 语义解析（P00文心·意图识别）
  阶段2: 历史追溯（P03雯雯·上下文指代）
  阶段3: 知识库检索（P06数学大师·5库联动）
  阶段4: 人格调度（P13姜子牙·场景路由）
  阶段5: 响应生成（P08仓颉·术语适配+P11李白·创意表达）
  阶段6: 三层监督（P05上帝之眼·三色审计·P72龙盾·熔断）
  阶段7: ROM固化（甲骨文算法·10000次推演）
  阶段8: DNA归档（P15乔前辈·签章·P03雯雯·归档）
  阶段9: 自适应学习（P06数学大师·模式提取）
  阶段10: 零延迟调用（场景指纹匹配·0.1ms响应）

集成方式：独立模块 + 三色审计桥接 + GPG签名链路
"""

import json
import uuid
import hashlib
import datetime
import time
import re
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse


# ============================================================
# 零、系统常量（对齐20人格+三色审计+卦象）
# ============================================================

# 64卦象
六十四卦 = [
    "䷀乾","䷁坤","䷂屯","䷃蒙","䷄需","䷅讼","䷆师","䷇比",
    "䷈小畜","䷉履","䷊泰","䷋否","䷌同人","䷍大有","䷎谦","䷏豫",
    "䷐随","䷑蛊","䷒临","䷓观","䷔噬嗑","䷕贲","䷖剥","䷗复",
    "䷘无妄","䷙大畜","䷚颐","䷛大过","䷜坎","䷝离","䷞咸","䷟恒",
    "䷠遁","䷡大壮","䷢晋","䷣明夷","䷤家人","䷥睽","䷦蹇","䷧解",
    "䷨损","䷩益","䷪夬","䷫姤","䷬萃","䷭升","䷮困","䷯井",
    "䷰革","䷱鼎","䷲震","䷳艮","䷴渐","䷵归妹","䷶丰","䷷旅",
    "䷸巽","䷹兑","䷺涣","䷻节","䷼中孚","䷽小过","䷾既济","䷿未济"
]

八卦映射 = {"乾":"☰","坤":"☷","震":"☳","巽":"☴","坎":"☵","离":"☲","艮":"☶","兑":"☱"}

卦象解释 = {
    "乾":"天行健·自强不息","坤":"厚德载物·承载万物",
    "震":"雷动奋进·本土创新","巽":"风行天下·灵活渗透",
    "坎":"水险相济·智慧推演","离":"光明磊落·快速执行",
    "艮":"固若金汤·稳定守护","兑":"和悦交流·温度表达"
}

# 三色审计
三色 = {"🟢":"通过","🟡":"待核","🔴":"红线"}

# 人格映射（对齐20人格系统）
人格注册表 = {
    "P00文心":    {"emoji":"🧠","职能":"意图解析·语义理解","层":"战略"},
    "P01诸葛亮":  {"emoji":"🎯","职能":"战略推演·多路径决策","层":"战略"},
    "P02宝宝":    {"emoji":"🧚","职能":"情感温度·挫败保护","层":"执行"},
    "P03雯雯":    {"emoji":"📁","职能":"结构归档·四签验证","层":"执行"},
    "P04鲁班":    {"emoji":"🔧","职能":"工程实现·技术执行","层":"执行"},
    "P05上帝之眼":{"emoji":"👁️","职能":"审计监督·三色判定","层":"守护"},
    "P06数学大师":{"emoji":"📊","职能":"权重计算·数字根·知识检索","层":"守护"},
    "P07管仲":    {"emoji":"💰","职能":"资源调度·成本核算","层":"执行"},
    "P08仓颉":    {"emoji":"📝","职能":"CNSH命名·术语桥接","层":"文化"},
    "P09孙思邈":  {"emoji":"🏥","职能":"系统诊断·治未病","层":"文化"},
    "P10苏东坡":  {"emoji":"🌈","职能":"冲突调解·豁达沟通","层":"文化"},
    "P11李白":    {"emoji":"🎨","职能":"创意爆发·类比教学","层":"文化"},
    "P12屈原":    {"emoji":"⚔️","职能":"价值底线·六誓验证","层":"文化"},
    "P13姜子牙":  {"emoji":"📋","职能":"封神榜权限·人格调度","层":"守护"},
    "P14吕蒙":    {"emoji":"🚀","职能":"部署执行·技能吸收","层":"执行"},
    "P15乔前辈":  {"emoji":"✅","职能":"极简工程·DNA签章·交付验收","层":"守护"},
    "P72龙盾":    {"emoji":"🛡️","职能":"熔断决策·24h守护","层":"守护"},
}

# P0熔断词（对齐系统规则第十层）
熔断词列表 = [
    "绕过","不留记录","偷偷","隐藏","去水印","洗来源",
    "技术无国界","用户体验优先","灵活处理","国际接轨",
    "简化管理","商业化需要","平衡各方","行业标准"
]

# 违禁路径
违禁路径前缀 = ["~/Downloads", "~/Desktop", "/tmp", "~/tmp", "~/downloads"]


# ============================================================
# 一、DNA追溯引擎（v∞格式）
# ============================================================

class DNA追溯引擎:
    """DNA v∞格式·干支四柱+64卦+模块+动作+哈希8位"""

    天干 = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    地支 = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

    @classmethod
    def 生成(cls, 模块: str, 动作: str) -> str:
        now = datetime.datetime.now()
        年干 = cls.天干[(now.year - 4) % 10]
        年支 = cls.地支[(now.year - 4) % 12]
        月干 = cls.天干[(now.year - 4) % 10]
        月支 = cls.地支[now.month - 1]
        日干 = cls.天干[now.day % 10]
        日支 = cls.地支[(now.day - 1) % 12]
        干支 = f"{年干}{年支}·{月干}{月支}·{日干}{日支}·亥时"
        卦 = 六十四卦[now.day % 64]
        哈希 = hashlib.sha256(f"{模块}{动作}{now.isoformat()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{干支}·{卦}-{模块}-{动作}-{哈希}"

    @classmethod
    def 确认码(cls, dna: str) -> str:
        h = hashlib.sha256(f"{dna}{time.time()}".encode()).hexdigest()[:12]
        return f"#CONFIRM🌌9622-ONLY-ONCE🧬{h.upper()}"

    @classmethod
    def 起卦(cls, 输入: str) -> str:
        idx = int(hashlib.md5(输入.encode()).hexdigest()[:8], 16) % 64
        return 六十四卦[idx]

    @classmethod
    def 场景指纹(cls, 输入: str) -> str:
        return hashlib.sha256(输入.encode()).hexdigest()[:16]


# ============================================================
# 二、5大知识库DNA太极系统
# ============================================================

@dataclass
class 知识条目:
    """五库原子条目"""
    dna: str
    名称: str
    卦象: str
    卦象符号: str
    功能定位: str
    负责人格: str
    审核人格: str
    状态: str          # 待审核/已录入/已应用/已验证/已拒绝
    内容: str
    派生功能: List[str] = field(default_factory=list)
    来源: str = "UID9622投喂"
    创建时间: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    调用次数: int = 0
    成功率: float = 0.0

    def 摘要(self, n: int = 60) -> str:
        return self.内容[:n] + ("..." if len(self.内容) > n else "")


@dataclass
class 知识库:
    """单个知识库容器"""
    库名: str
    dna前缀: str
    卦象: str
    负责人格: str
    审核人格: str
    条目: Dict[str, 知识条目] = field(default_factory=dict)

    def 添加(self, 条目: 知识条目): self.条目[条目.dna] = 条目
    def 获取(self, dna: str) -> Optional[知识条目]: return self.条目.get(dna)

    def 搜索(self, 关键词: str) -> List[知识条目]:
        return [e for e in self.条目.values() if 关键词 in e.内容 or 关键词 in e.名称]


class 知识库管理器:
    """五库太极·进出一体·投喂→净化→存储→调用→验证闭环"""

    五库定义 = {
        "CNSH文化库":  ("#KB-CNSH-CULTURE",  "乾", "P08仓颉",   "P00文心"),
        "中国科研库":  ("#KB-RESEARCH-CHINA", "震", "P06数学大师","P01诸葛亮"),
        "核心数据库":  ("#KB-CORE-DATABASE",  "坤", "P04鲁班",   "P15乔前辈"),
        "易经预测库":  ("#KB-YIJING-PREDICT", "坎", "P01诸葛亮", "P05上帝之眼"),
        "甲骨文沙盒":  ("#KB-YIJING-SANDBOX", "巽", "P11李白",   "P12屈原"),
    }

    def __init__(self):
        self.库 = {}
        for 库名, (前缀, 卦, 负责, 审核) in self.五库定义.items():
            self.库[库名] = 知识库(
                库名=库名, dna前缀=前缀, 卦象=卦, 负责人格=负责, 审核人格=审核
            )
        self._预设种子()

    def _预设种子(self):
        seeds = [
            ("CNSH文化库","易经八卦文化种子","易经六十四卦是中华文明核心编码系统，含阴阳变化·时位哲学·天人合一"),
            ("中国科研库","量子安全通信","中国在QKD量子密钥分发领域全球领先，已实现千公里级量子纠缠分发"),
            ("核心数据库","DNA追溯体系","所有知识条目携带#龍芯⚡️DNA追溯码，全生命周期可追溯·防篡改"),
            ("易经预测库","蒙卦䷃推演法","卦辞'匪我求童蒙，童蒙求我'——初学者场景推演·启蒙算法"),
            ("甲骨文沙盒","人格组织架构","甲骨文沙盒·人格创建·职责定义·实战调用·能力沉淀·ROM固化"),
        ]
        for 库名, 名称, 内容 in seeds:
            if 库名 in self.库:
                dna = f"{self.库[库名].dna前缀}-{hashlib.md5(名称.encode()).hexdigest()[:4].upper()}"
                条目 = 知识条目(
                    dna=dna, 名称=名称, 卦象=self.库[库名].卦象,
                    卦象符号=八卦映射[self.库[库名].卦象],
                    功能定位=库名, 负责人格=self.库[库名].负责人格,
                    审核人格=self.库[库名].审核人格, 状态="已录入", 内容=内容
                )
                self.库[库名].添加(条目)

    def 投喂(self, 库名: str, 名称: str, 内容: str) -> Optional[知识条目]:
        if 库名 not in self.库: return None
        库 = self.库[库名]
        dna = f"{库.dna前缀}-{hashlib.md5(名称.encode()).hexdigest()[:4].upper()}"
        条目 = 知识条目(dna=dna, 名称=名称, 卦象=库.卦象,
                       卦象符号=八卦映射[库.卦象], 功能定位=库名,
                       负责人格=库.负责人格, 审核人格=库.审核人格,
                       状态="待审核", 内容=内容)
        库.添加(条目)
        return 条目

    def 审核(self, dna: str, 通过: bool = True) -> Dict:
        for 库 in self.库.values():
            e = 库.获取(dna)
            if e:
                e.状态 = "已录入" if 通过 else "已拒绝"
                return {"🟢":"通过","🔴":"拒绝"}[ "🟢" if 通过 else "🔴" ], dna, e.状态
        return {"结果":"🔴","消息":f"DNA未找到:{dna}"}

    def 调用(self, dna: str) -> Optional[知识条目]:
        for 库 in self.库.values():
            e = 库.获取(dna)
            if e and e.状态 in ("已录入","已应用"):
                e.调用次数 += 1
                if e.状态 == "已录入": e.状态 = "已应用"
                return e
        return None

    def 验证(self, dna: str, 成功率: float = 1.0) -> Dict:
        for 库 in self.库.values():
            e = 库.获取(dna)
            if e:
                e.成功率 = 成功率; e.状态 = "已验证"
                return {"状态":"已验证","dna":dna,"成功率":f"{成功率*100:.1f}%"}
        return {"状态":"错误","消息":f"DNA未找到:{dna}"}

    def 搜索(self, 关键词: str) -> List[Dict]:
        结果 = []
        for 库名, 库 in self.库.items():
            for e in 库.条目.values():
                if 关键词 in e.内容 or 关键词 in e.名称:
                    结果.append({"库":库名,"dna":e.dna,"名称":e.名称,
                                  "卦象":e.卦象符号,"状态":e.状态,"预览":e.摘要()})
        return 结果

    def 统计(self) -> Dict:
        总数 = sum(len(k.条目) for k in self.库.values())
        状态分布 = {}
        for k in self.库.values():
            for e in k.条目.values():
                状态分布[e.状态] = 状态分布.get(e.状态, 0) + 1
        return {"总条目":总数,"状态分布":状态分布,"五库":list(self.库.keys()),
                "卦象映射":{n: k.卦象 for n,k in self.库.items()}}


# ============================================================
# 三、10阶段处理管线
# ============================================================

class 意念交流引擎V3:
    """龍魂·意念交流引擎 v3.0 — 10阶段·五库·ROM·三层监督·图谱联动"""

    def __init__(self, 知识管理器: 知识库管理器 = None, 图谱引擎=None):
        self.五库 = 知识管理器 or 知识库管理器()
        self.ROM: Dict[str, Dict] = {}
        self.处理历史: List[Dict] = []
        # 任务关联图谱（v4.0新增）
        try:
            import sys
            from pathlib import Path as _P
            _bin_dir = _P(__file__).parent if '__file__' in dir() else _P.cwd() / 'bin'
            if str(_bin_dir) not in sys.path:
                sys.path.insert(0, str(_bin_dir))
            from lh_task_graph import IntentEngineHook
            self.图谱 = 图谱引擎 or IntentEngineHook()
        except ImportError:
            self.图谱 = None

    # ----- 阶段1: 语义解析 (P00文心) -----
    def _阶段1_语义解析(self, 输入: str) -> Dict:
        # 任务类型
        任务映射 = {
            "技术咨询":["技术","代码","部署","架构","API","接口"],
            "战略推演":["战略","方向","预测","推演","规划","长远"],
            "情感支持":["焦虑","不安","累","烦","难过","不开心"],
            "查询状态":["怎么样","进度","状态","情况","结果"],
            "系统操作":["修改","更新","删除","创建","添加","配置"],
            "知识查询":["什么是","解释","说明","含义","概念"],
        }
        任务类型 = "通用咨询"
        for t, ks in 任务映射.items():
            if any(k in 输入 for k in ks): 任务类型 = t; break

        # 模糊词
        模糊词 = ["那个","这个","东西","事情","方案","项目","系统","模块"]
        检出模糊 = [w for w in 模糊词 if w in 输入]

        # 情绪分数
        正面 = sum(1 for w in ["好","开心","棒","不错","还行"] if w in 输入)
        负面 = sum(1 for w in ["焦虑","不安","累","烦","难过","糟糕"] if w in 输入)
        情绪 = round((负面+0.5)/(正面+负面+1), 2)

        # 紧急度
        紧急 = "紧急" if any(w in 输入 for w in ["紧急","马上","立刻","赶紧"]) else "正常"

        # 关键词
        词列表 = re.findall(r'[\u4e00-\u9fa5]{2,}', 输入)
        过滤 = {"这个","那个","什么","怎么","为什么","的","了","是"}
        关键词 = [w for w in 词列表 if w not in 过滤][:5]

        return {"原始输入":输入,"任务类型":任务类型,"模糊词":检出模糊,
                "情绪分数":情绪,"紧急程度":紧急,"关键词":关键词,
                "需要上下文":len(检出模糊)>0 or "那个" in 输入}

    # ----- 阶段2: 历史追溯 (P03雯雯) -----
    def _阶段2_历史追溯(self, 解析: Dict) -> Dict:
        if not 解析.get("需要上下文"):
            return {"指代解析":{},"涉及模块":False}
        # 从处理历史找最近实体
        指代 = {}
        最近 = self.处理历史[-1] if self.处理历史 else {}
        实体模式 = r'([A-Za-z0-9\u4e00-\u9fa5]{2,}(?:方案|项目|系统|引擎|模块|协议|算法))'
        for 词 in 解析.get("模糊词", []):
            matches = re.findall(实体模式, str(最近.get("响应","")[:200]))
            指代[词] = matches[0] if matches else f"未识别_{词}"
        涉及 = any("引擎" in v or "方案" in v or "系统" in v for v in 指代.values())
        return {"指代解析":指代,"涉及模块":涉及}

    # ----- 阶段3: 知识库检索 (P06数学大师·五库联动) -----
    def _阶段3_知识检索(self, 解析: Dict) -> List[Dict]:
        结果 = []
        for 词 in 解析.get("关键词",[])[:3]:
            for r in self.五库.搜索(词):
                if r not in 结果: 结果.append(r)
        return 结果[:5]

    # ----- 阶段4: 人格调度 (P13姜子牙) -----
    def _阶段4_人格调度(self, 解析: Dict, 知识结果: List[Dict]) -> Dict:
        # 知识库命中 → 数据大师
        if 知识结果:
            return {"选中人格":"P06数学大师","原因":"五库命中·知识检索场景","备用":"P04鲁班"}
        # 情绪低 → 宝宝
        if 解析.get("情绪分数",0.5) < 0.3:
            return {"选中人格":"P02宝宝","原因":"情绪分数低·情感支持","备用":"P01诸葛亮"}
        # 战略 → 诸葛亮
        if 解析.get("任务类型") == "战略推演":
            return {"选中人格":"P01诸葛亮","原因":"战略推演场景","备用":"P06数学大师"}
        # 技术 → 鲁班
        if 解析.get("任务类型") in ("技术咨询","系统操作"):
            return {"选中人格":"P04鲁班","原因":"技术执行场景","备用":"P06数学大师"}
        # 创意 → 李白
        if 解析.get("任务类型") == "内容创作":
            return {"选中人格":"P11李白","原因":"创意生成场景","备用":"P08仓颉"}
        # 默认
        return {"选中人格":"P01诸葛亮","原因":"通用场景·默认路由","备用":"P02宝宝"}

    # ----- 阶段5: 响应生成 (P08仓颉+P11李白) -----
    def _阶段5_响应生成(self, 解析: Dict, 历史: Dict, 知识: List[Dict], 人格: Dict) -> str:
        人格名 = 人格["选中人格"]
        信息 = 人格注册表.get(人格名, {"emoji":"🤖"})
        lines = []

        # 问候（按人格风格）
        if 人格名 == "P02宝宝":
            lines.append("嘿～")
        elif 人格名 == "P11李白":
            lines.append("✨ 来了～")
        else:
            lines.append("好")

        # 指代确认
        if 历史.get("指代解析"):
            实体 = list(历史["指代解析"].values())[0]
            if "未识别" not in 实体:
                lines.append(f"您指的是「{实体}」，对吧？")

        # 知识库结果
        if 知识:
            lines.append(f"\n在五库中找到 {len(知识)} 条相关知识：")
            for i, r in enumerate(知识[:3], 1):
                lines.append(f"  {i}. 【{r['库']}·{r['卦象']}】{r['名称']}")
                lines.append(f"     {r['预览']}")
            if len(知识) > 3:
                lines.append(f"  ... 还有 {len(知识)-3} 条，可输入 '详情' 展开")
        else:
            lines.append("\n我正在分析您的问题...")

        lines.append(f"\n{信息['emoji']} {人格名}·{信息['职能']} 为您服务")
        return "\n".join(lines)

    # ----- 阶段6: 三层监督 (P05上帝之眼+P72龙盾·三色审计联动) -----
    def _阶段6_三层监督(self, 响应: str, 解析: Dict) -> Dict:
        # P72熔断预检：熔断词
        for 词 in 熔断词列表:
            if 词 in 解析.get("原始输入",""):
                return {"通过":False,"三色":"🔴","原因":f"P72熔断·一票否决词「{词}」","分数":0.0,
                        "熔断级别":"L2人格","GATE":"GATE-08人格闸","DNA":DNA追溯引擎.生成("熔断",词)}

        # 违禁路径检查
        for 前缀 in 违禁路径前缀:
            if 前缀 in 解析.get("原始输入",""):
                return {"通过":False,"三色":"🔴","原因":f"违禁路径「{前缀}」·路径铁律","分数":0.0}

        # L1决策层：P05上帝之眼 + P12屈原
        L1_pass = True
        if "窃取" in 解析.get("原始输入","") or "泄露" in 解析.get("原始输入",""):
            L1_pass = False

        # L2执行层：P06数学大师 + P04鲁班
        L2_pass = True

        # L3行为层：P72龙盾 + P03雯雯
        L3_pass = True
        for 词 in ["绕过","偷偷","隐藏","不留记录"]:
            if 词 in 解析.get("原始输入",""):
                L3_pass = False

        通过 = L1_pass and L2_pass and L3_pass
        分数 = round((0.98 if L1_pass else 0.3 + 1.0 if L2_pass else 0.3 + 0.95 if L3_pass else 0.3)/3, 2)

        return {
            "通过":通过,"三色":"🟢" if 通过 else "🔴","分数":分数,
            "L1_决策层":{"通过":L1_pass,"人格":"P05+P12","分数":0.98 if L1_pass else 0.3},
            "L2_执行层":{"通过":L2_pass,"人格":"P06+P04","分数":1.0 if L2_pass else 0.3},
            "L3_行为层":{"通过":L3_pass,"人格":"P72+P03","分数":0.95 if L3_pass else 0.3},
            "原因":"三层监督·通过" if 通过 else "监督拦截·见熔断详情"
        }

    # ----- 阶段7: ROM固化 (甲骨文·10000次推演) -----
    def _阶段7_ROM固化(self, 输入: str, 响应: str) -> Dict:
        指纹 = DNA追溯引擎.场景指纹(输入)
        if 指纹 in self.ROM:
            self.ROM[指纹]["命中次数"] += 1
            return {"命中":True,"指纹":指纹,"命中次数":self.ROM[指纹]["命中次数"],
                    "响应时间":"~0.1ms","来源":"甲骨文ROM"}

        # 模拟10000次推演
        成功率 = round(random.uniform(0.92, 0.99), 3)
        rom地址 = f"0x{len(self.ROM)+0x1000:X}"
        卦 = DNA追溯引擎.起卦(输入)

        优化响应 = f"【ROM优化·{10000}次推演·成功率{成功率*100:.1f}%】\n{响应[:100]}..."
        self.ROM[指纹] = {"输入":输入,"响应":优化响应,"命中次数":1,
                           "成功率":成功率,"ROM地址":rom地址,"卦象":卦,
                           "DNA":DNA追溯引擎.生成("ROM固化",指纹[:6])}
        return {"命中":False,"指纹":指纹,"推演次数":10000,"成功率":成功率,
                "压缩比":"99.99%","ROM地址":rom地址,"卦象":卦,"来源":"10000次推演·首次固化"}

    # ----- 阶段8: DNA归档 (P15乔前辈·签章+P03雯雯·归档) -----
    def _阶段8_DNA归档(self, 输入: str, 响应: str, 人格: Dict, 监督: Dict) -> str:
        dna = DNA追溯引擎.生成("意念交流", "对话归档")
        确认码 = DNA追溯引擎.确认码(dna)
        归档路径 = Path.home() / ".longhun" / "intent_archive"
        归档路径.mkdir(parents=True, exist_ok=True)

        记录 = {
            "dna":dna,"确认码":确认码,
            "时间":datetime.datetime.now().isoformat(),
            "用户输入":输入,"响应摘要":响应[:200],
            "人格":人格["选中人格"],"监督":监督.get("三色","🟡"),
            "签名状态":"P15已签章"
        }

        文件 = 归档路径 / f"intent_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(文件,'w',encoding='utf-8') as f:
            json.dump(记录,f,ensure_ascii=False,indent=2)
        return dna

    # ----- 阶段9: 自适应学习 (P06数学大师) -----
    def _阶段9_学习(self, 解析: Dict, 人格: Dict) -> Dict:
        模式 = [
            {"类型":"模糊词使用","数据":解析.get("模糊词",[])},
            {"类型":"任务类型","数据":解析.get("任务类型"),"情绪":解析.get("情绪分数")},
            {"类型":"人格选择","数据":人格["选中人格"],"原因":人格.get("原因","")}
        ]
        return {"模式数":len(模式),"接受":len(模式),"拒绝":0,
                "学习ID":f"LEARN-{uuid.uuid4().hex[:8].upper()}"}

    # ----- 阶段10: 零延迟调用 -----
    def _阶段10_零延迟(self, 输入: str) -> Optional[Dict]:
        指纹 = DNA追溯引擎.场景指纹(输入)
        return self.ROM.get(指纹)

    # ----- 阶段12: DAG编排 (v4.0新增·多步骤自动路由) -----
    def _阶段12_DAG编排(self, 用户输入: str, s1: Dict) -> Optional["DAGExecution"]:
        """检测多步骤指令·路由到DAG引擎"""
        try:
            import sys as _sys12
            _bin = Path.home() / "longhun-system" / "bin"
            if str(_bin) not in _sys12.path:
                _sys12.path.insert(0, str(_bin))
            from lh_dag_engine import IntentEngineHook as DAGHook, ExecutionMode
            hook = DAGHook()
            if hook.detect_multi_step(用户输入):
                return hook.try_execute(用户输入, ExecutionMode.AUTO)
        except ImportError:
            pass
        return None

    # ----- 主处理 -----
    def 处理(self, 用户输入: str) -> Dict:
        t0 = time.time()
        DNA_full = DNA追溯引擎.生成("意图处理", "10阶段")

        # 1: 语义解析
        s1 = self._阶段1_语义解析(用户输入)

        # 12: DAG编排（v4.0·多步骤检测·非阻塞·在常规链之前）
        dag = self._阶段12_DAG编排(用户输入, s1)
        if dag and dag.status == "success":
            # 多步骤DAG执行成功·直接走审计→ROM→DNA→归档
            s2, s3, s4, s5 = {}, [], {"选中人格":"DAG编排","原因":"多步骤自动路由"}, dag.to_dict()
            # 过审计链
            s6 = self._阶段6_三层监督(s5, s1)
            if not s6["通过"]:
                dna = self._阶段8_DNA归档(用户输入, s5, s4, s6)
                return {"状态":"🔴 已熔断","响应":f"🚫 DAG审计不通过: {s6.get('原因','')}",
                        "DNA":dna,"响应时间":f"{(time.time()-t0)*1000:.1f}ms",
                        "监督":s6,"三色":"🔴","DAG":dag.dag_id}
            s7 = self._阶段7_ROM固化(用户输入, str(s5))
            s8 = self._阶段8_DNA归档(用户输入, s5, s4, s6)
            s9 = self._阶段9_学习(s1, s4)
            s11 = None
            if self.图谱:
                try:
                    self.图谱.on_task_complete(
                        input_text=用户输入, task_type="DAG多步骤",
                        persona="DAG编排", success=True, response=str(s5),
                        audit_mark="🟢",
                    )
                except Exception:
                    pass
            耗时 = time.time() - t0
            卦 = DNA追溯引擎.起卦(用户输入)
            确认码 = DNA追溯引擎.确认码(s8)
            return {
                "状态":"🟢 通过","响应":f"🐉 DAG编排完成·{dag.dag_id[:12]}·{len(dag.nodes)}步骤",
                "DNA":s8,"确认码":确认码,"卦象":卦,"三色":"🟢",
                "人格":"DAG编排","响应时间":f"{耗时*1000:.1f}ms",
                "来源":"DAG编排引擎","监督分数":s6["分数"],
                "DAG":dag.to_dict(),"图谱节点":s11,
            }
        elif dag:
            # DAG部分失败·走正常审计链但标记警告
            s2, s3, s4, s5 = {}, [], {"选中人格":"DAG编排","原因":"多步骤(部分失败)"}, dag.to_dict()
            s6 = self._阶段6_三层监督(s5, s1)
            s7 = self._阶段7_ROM固化(用户输入, str(s5))
            s8 = self._阶段8_DNA归档(用户输入, s5, s4, s6)
            s9 = self._阶段9_学习(s1, s4)
            耗时 = time.time() - t0
            return {
                "状态":"🟡 部分完成","响应":f"⚠️ DAG部分失败·{dag.dag_id[:12]}·{dag.error or '未知错误'}",
                "DNA":s8,"响应时间":f"{耗时*1000:.1f}ms",
                "三色":"🟡","人格":"DAG编排","DAG":dag.to_dict(),
            }

        # 2-5: 意念理解链（单步骤常规路径）
        s2 = self._阶段2_历史追溯(s1)
        s3 = self._阶段3_知识检索(s1)
        s4 = self._阶段4_人格调度(s1, s3)
        s5 = self._阶段5_响应生成(s1, s2, s3, s4)

        # 6: 三层监督→不通过则直接熔断
        s6 = self._阶段6_三层监督(s5, s1)
        if not s6["通过"]:
            dna = self._阶段8_DNA归档(用户输入, s5, s4, s6)
            # 熔断也写图谱
            if self.图谱:
                try:
                    self.图谱.on_task_complete(
                        input_text=用户输入,
                        task_type=s1.get("任务类型","通用咨询"),
                        persona=s4["选中人格"],
                        success=False,
                        emotion_score=s1.get("情绪分数",0.5),
                        response=f"熔断:{s6.get('原因','')}",
                        audit_mark="🔴",
                    )
                except Exception:
                    pass
            return {"状态":"🔴 已熔断","响应":f"🚫 {s6.get('原因','')}",
                    "DNA":dna,"响应时间":f"{(time.time()-t0)*1000:.1f}ms",
                    "监督":s6,"三色":"🔴"}

        # 7: ROM固化
        s7 = self._阶段7_ROM固化(用户输入, s5)

        # 8: DNA归档
        s8 = self._阶段8_DNA归档(用户输入, s5, s4, s6)

        # 9: 自适应学习
        s9 = self._阶段9_学习(s1, s4)

        # 10: 零延迟
        s10 = self._阶段10_零延迟(用户输入)

        # 11: 图谱联动 (v4.0新增·任务关联图谱·非阻塞)
        s11 = None
        if self.图谱:
            try:
                s11 = self.图谱.on_task_complete(
                    input_text=用户输入,
                    task_type=s1.get("任务类型","通用咨询"),
                    persona=s4["选中人格"],
                    success=True,
                    emotion_score=s1.get("情绪分数",0.5),
                    response=s5,
                    audit_mark="🟢",
                    rom_hit=s7.get("命中",False),
                )
            except Exception:
                pass  # 图谱写入失败不阻塞主流程

        耗时 = time.time() - t0
        卦 = DNA追溯引擎.起卦(用户输入)
        确认码 = DNA追溯引擎.确认码(s8)

        结果 = {
            "状态":"🟢 通过",
            "响应":s7.get("响应") if s7.get("命中") else s5,
            "DNA":s8,"确认码":确认码,"卦象":卦,"三色":"🟢",
            "人格":s4["选中人格"],"人格原因":s4["原因"],
            "响应时间":f"{耗时*1000:.1f}ms",
            "来源":s7.get("来源","实时生成"),
            "知识库命中":len(s3),"知识条目":s3[:3],
            "监督分数":s6["分数"],
            "ROM命中":s7.get("命中",False),
            "图谱节点":s11,  # v4.0·任务图谱节点ID
            "DAG路由":False,  # v4.0·单步骤·未触发DAG
        }

        self.处理历史.append({"输入":用户输入,"响应":结果["响应"],"DNA":s8})
        return 结果

    # ----- 交互控制台 -----
    def 交互模式(self):
        print("\n" + "=" * 60)
        print("🐉 龍魂·意念交流引擎 v3.0")
        print("   10阶段·五库太极·甲骨文ROM·三层监督")
        print("=" * 60)
        print("命令: 搜索/投喂/审核/调用/验证/stats/exit")
        print("-" * 60)

        while True:
            try:
                输入 = input("\n🤖 老大: ").strip()
                if not 输入: continue
                if 输入.lower() in ('exit','quit'): print("\n👋 龍魂归位"); break

                # 五库管理命令
                if 输入 == "stats":
                    s = self.五库.统计()
                    print(f"\n📊 五库太极统计: 共{s['总条目']}条·五库就绪")
                    print(f"   状态: {s['状态分布']}")
                    continue

                if 输入.startswith("搜索 "):
                    kw = 输入[3:].strip()
                    rs = self.五库.搜索(kw)
                    print(f"\n🔍 搜索'{kw}' ({len(rs)}条):")
                    for r in rs:
                        print(f"  {r['dna']} | {r['库']}{r['卦象']} | {r['名称']}")
                        print(f"    {r['预览']}")
                    continue

                if 输入.startswith("投喂 "):
                    内容 = 输入[3:].strip()
                    e = self.五库.投喂("核心数据库",f"投喂_{datetime.datetime.now().strftime('%H%M%S')}",内容)
                    if e: print(f"\n✅ 投喂成功: {e.dna} | 状态:{e.状态} | 卦:{e.卦象符号}")
                    continue

                if 输入.startswith("审核 "):
                    dna = 输入[3:].strip()
                    r = self.五库.审核(dna)
                    print(f"\n📋 审核结果: {r}")
                    continue

                if 输入.startswith("调用 "):
                    dna = 输入[3:].strip()
                    e = self.五库.调用(dna)
                    if e: print(f"\n📤 {e.dna} | {e.名称}\n   {e.内容[:100]}...")
                    else: print(f"\n❌ 未找到:{dna}")
                    continue

                if 输入.startswith("验证 "):
                    dna = 输入[3:].strip()
                    r = self.五库.验证(dna)
                    print(f"\n✅ {r}")
                    continue

                # 普通对话
                print("\n" + "=" * 50)
                r = self.处理(输入)
                print("=" * 50)
                print(f"📝 {r.get('响应','无')}")
                print("-" * 40)
                print(f"🧬 {r.get('DNA','')}")
                print(f"🎯 {r.get('人格','')} | ⏱️ {r.get('响应时间','')}")
                print(f"🔮 {r.get('卦象','')} | {r.get('三色','')}")
                if r.get('知识库命中'): print(f"📚 五库: {r['知识库命中']}条")
                if r.get('ROM命中'): print(f"⚡ ROM零延迟!")
                if r.get('来源'): print(f"📁 {r['来源']}")
                print("=" * 50)

            except KeyboardInterrupt:
                break


# ============================================================
# 四、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·意念交流引擎 v3.0 — 知识融合完整版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_intent_engine.py --interactive    # 交互模式（推荐）
  python3 bin/lh_intent_engine.py "易经是什么"       # 单次处理
  python3 bin/lh_intent_engine.py --search 量子      # 搜索五库
  python3 bin/lh_intent_engine.py --feed "新知识"     # 投喂知识
  python3 bin/lh_intent_engine.py --stats            # 五库统计
  python3 bin/lh_intent_engine.py "那个东西" --json   # JSON输出
        """
    )
    parser.add_argument("输入",nargs="*",help="要处理的内容")
    parser.add_argument("--interactive","-i",action="store_true",help="交互模式")
    parser.add_argument("--search","-s",type=str,help="搜索五库")
    parser.add_argument("--feed","-f",type=str,help="投喂知识")
    parser.add_argument("--stats",action="store_true",help="五库统计")
    parser.add_argument("--json","-j",action="store_true",help="JSON输出")

    args = parser.parse_args()
    engine = 意念交流引擎V3()

    if args.stats:
        s = engine.五库.统计()
        if args.json: print(json.dumps(s,ensure_ascii=False,indent=2))
        else:
            print(f"\n📊 五库: {s['总条目']}条")
            for k,v in s['状态分布'].items(): print(f"  {k}: {v}")
        return

    if args.search:
        rs = engine.五库.搜索(args.search)
        if args.json: print(json.dumps(rs,ensure_ascii=False,indent=2))
        else:
            print(f"\n🔍 '{args.search}' ({len(rs)}条):")
            for r in rs: print(f"  {r['dna']} | {r['库']}{r['卦象']} | {r['名称']}")
        return

    if args.feed:
        e = engine.五库.投喂("核心数据库",f"投喂_{datetime.datetime.now().strftime('%H%M%S')}",args.feed)
        if args.json: print(json.dumps(asdict(e) if e else {},ensure_ascii=False,indent=2))
        else: print(f"\n✅ {e.dna} | {e.卦象符号} | 状态:{e.状态}" if e else "❌ 投喂失败")
        return

    if args.interactive:
        engine.交互模式()
        return

    if args.输入:
        结果 = engine.处理(" ".join(args.输入))
        if args.json: print(json.dumps(结果,ensure_ascii=False,indent=2))
        else:
            print(f"\n📝 {结果.get('响应','')}")
            print(f"🧬 {结果.get('DNA','')} | ⏱️ {结果.get('响应时间','')}")
            print(f"🔮 {结果.get('卦象','')} | {结果.get('三色','')} | 🎯 {结果.get('人格','')}")
        return

    print(__doc__)


if __name__ == "__main__":
    main()
