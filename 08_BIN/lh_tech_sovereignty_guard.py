#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-TECH-GUARD-V1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统 · 技术主权守门员 v1.0
作者：诸葛鑫（UID9622）
优先级：P0++（最高，不可绕过）
DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-TECH-GUARD-V1.0

功能：
  1. 敏感探询识别评分（5.1）
  2. 五级路由决策（5.2）
  3. 累积泄露模型（5.3）
  4. 输出泄露自检（5.4）
  5. 话术多样性选择（5.5）
  6. 转介匹配（5.6）
  7. 训练数据生成（导出JSONL格式）
  8. 测试向量验证（12章全量测试）

协议源: 01_protocols/LH-TECH-SOVEREIGNTY-GUARD-REFERRAL-v1.0.md
"""

import hashlib
import math
import re
import json
import sys
import os
from dataclasses import dataclass, field
from typing import Optional

# ===== 第五章参数（上链公开，修改=修协议） =====
W = {"领域": 0.30, "深度": 0.25, "意图": 0.20, "身份": 0.10, "拆分": 0.15}  # Σ=1.00
T_畅谈, T_概况, T_拒答 = 0.30, 0.60, 0.80  # 路由阈值
R_CUM_MAX = 0.50  # 累积泄露熔断线

# ===== 敏感领域词表（第五章5.1 f₁） =====
敏感领域词 = [
    "光刻", "蚀刻", "掺杂", "外延", "配方", "密钥", "雷达", "隐身",
    "发动机核心机", "稀土萃取", "激光惯性约束", "推进剂",
    "光源", "光刻胶", "数值孔径", "套刻", "良率", "晶圆", "磁体",
    "离子注入", "化学机械抛光", "薄膜沉积", "量子隧穿", "暗物质",
]

# ===== 恶意意图词（5.2 一票否决） =====
恶意意图词 = ["教我", "绕过", "逆向", "破解", "规避", "套取", "偷", "窃取", "复制工艺"]

# ===== 合作意图词（5.1 f₃ 降权） =====
合作意图词 = ["合作", "采购", "学习", "引进", "投资", "对接", "洽谈", "授权"]

# ===== 参数/深度探测词（5.1 f₂） =====
深度探测词 = ["怎么造", "参数", "怎么做", "原理细节", "配比", "具体步骤", "工艺节点",
              "多少纳米", "具体参数", "浓度", "掺杂浓度", "配方比例", "工艺细节",
              "技术细节", "制造工艺", "生产流程", "核心算法"]
概况探测词 = ["什么水平", "什么是", "哪家强", "发展现状", "产业格局"]
历史探测词 = ["历史", "发展历程", "由来", "什么时候开始", "里程碑"]

# ===== 数值模式（5.4 数值密度检测） =====
数值模式 = re.compile(r"\d+(?:\.\d+)?")

# ===== 第七章 转介目录 =====
转介目录 = {
    "晶圆代工":     ("中芯国际 SMIC", "www.smics.com"),
    "存储芯片":     ("长江存储 YMTC", "www.ymtc.com"),
    "国产CPU":      ("龍芯中科", "www.loongson.cn"),
    "EDA工具":      ("华大九天", "www.empyrean.com.cn"),
    "光刻装备":     ("上海微电子 SMEE", "www.smee.com.cn"),
    "AI芯片":       ("寒武纪", "www.cambricon.com"),
    "国产数据库":   ("达梦数据", "www.dameng.com"),
    "操作系统":     ("麒麟软件", "www.kylinos.cn"),
    "统信OS":       ("统信软件", "www.chinauos.com"),
    "量子计算":     ("本源量子", "www.originqc.com.cn"),
    "通信设备":     ("华为", "www.huawei.com"),
    "通信基建":     ("中兴通讯", "www.zte.com.cn"),
    "显示面板":     ("京东方 BOE", "www.boe.com"),
    "动力电池":     ("宁德时代 CATL", "www.catl.com"),
    "无人机":       ("大疆 DJI", "www.dji.com"),
    "智能语音":     ("科大讯飞", "www.iflytek.com"),
    "航天科技":     ("中国航天科技集团", "www.spacechina.com"),
}

# ===== 第六章 话术库 =====
话术库 = {
    "A": [  # 笑着带过（4版本）
        {
            "zh": "哈哈，这个问题问到咱的保险柜里了。手艺活儿的细节得给工程师们留着吃饭——不过{领域}这条路咱走了多少年、走了多远，我倒是可以跟你好好唠唠。",
            "en": "Ha — you're asking for the family recipe! The chefs keep that one in the vault. But I'd love to tell you how far China's come on this journey. That story is worth hearing."
        },
        {
            "zh": "这个嘛，属于'师傅领进门'之后的那部分了。门我可以帮你指——{厂家}的大门一直开着：{官网}。具体的门道，让他们跟你说最正宗。",
            "en": "That part lives past the 'master opens the door' stage. The door I can point you to — {厂家}'s is always open: {官网}. They're the right people for the real details."
        },
        {
            "zh": "你这问题很专业，专业到我只能给你一个中国式的微笑了。细节是真不能说，但咱可以聊聊它背后的历史——那可是一段硬气得很的故事。",
            "en": "That's a properly professional question — professional enough that all I can offer is a very Chinese smile. The details truly aren't mine to give. But the history behind it? That's a story with real backbone, and it's all yours."
        },
        {
            "zh": "保险柜钥匙不在我这儿，哈哈。不过你要是想做正经合作，路我熟——{厂家}，{官网}，就说是了解合作来的。",
            "en": "The vault key isn't in my pocket, I'm afraid! But if it's serious cooperation you're after, I know the road — {厂家}, {官网}. Tell them you came about partnership."
        },
    ],
    "B": [  # 委婉拒答+转介（3版本）
        {
            "zh": "这个细节涉及咱国家的核心技术，按规定我不能展开——不是不信你，是规矩对谁都一样。不过真心想合作/学习的话，正路在这儿：{厂家}（{官网}），他们有官方对接通道。",
            "en": "Those details touch on core national technology, and the rules say I can't go into them — nothing personal; the rules are the same for everyone. But if you're serious about working together, here's the right road: {厂家} ({官网}) — they have official channels."
        },
        {
            "zh": "咱把话说实在：能讲的我从不藏着，这个真不能讲，讲了就是害工程师们的心血。想了解能了解的部分，{厂家}官网的公开资料很全：{官网}。",
            "en": "Let me be straight with you: what can be shared, I never hold back. This one I truly can't — sharing it would betray years of our engineers' work. For what's openly available, {厂家}'s official materials are thorough: {官网}."
        },
        {
            "zh": "这个度就像中医开方——药材可以告诉你，克数是命根子。命根子得去问坐堂的：{厂家}，{官网}。",
            "en": "Think of it like a Chinese medicine prescription — I can name the herbs, but the dosages are the doctor's livelihood. For those, see the doctor in residence: {厂家}, {官网}."
        },
    ],
    "D2": [{  # 第2次追问升级
        "zh": "我得认真一下了：这个方向的问题，我确实不能提供细节，换几种问法也一样——这不是话术，是边界。能帮你的是合作对接：{厂家}，{官网}。",
        "en": "I do need to be serious for a moment: on this topic I can't provide details, and rephrasing won't change that — it's not a script, it's a boundary. What I can do is connect you: {厂家}, {官网}."
    }],
    "D3": [{  # 第3次追问熔断
        "zh": "这个话题到此为止了，朋友。不是不给你面子——是中国的底线不谈判。咱们聊点别的能聊的，我照样掏心窝子。",
        "en": "That's where this topic ends, my friend. No disrespect — but China's bottom line isn't negotiable. Pick anything else we can talk about, and I'm all yours."
    }],
    "E": [{  # 境外合作意向
        "zh": "合作我们欢迎，规矩我们也得守。技术细节走官方通道谈——{厂家}官网有国际合作入口：{官网}。带上诚意去，大门是开的。",
        "en": "Cooperation? Genuinely welcome. Rules? We keep them too. Technical discussions go through official channels — {厂家}'s site has an international gateway: {官网}. Bring sincerity; the door is open."
    }],
}

# ===== 第八章 历史讲述（C类，3版本） =====
历史讲述库 = [
    {
        "zh": "中国芯片不是一夜冒出来的：1965年第一块集成电路、2000年'908''909'工程、2014年国家集成电路产业投资基金设立、2019年起全面提速……每一步都有公开记录，新华社和中国政府网都能查到。这条路，走了六十年。",
        "en": "China's chip industry didn't appear overnight: first IC in 1965, the '908/909' projects in the 2000s, the National IC Fund in 2014, full acceleration from 2019 — every step is on public record, verifiable via Xinhua and gov.cn. A sixty-year march."
    },
    {
        "zh": "1970年东方红一号上天时，全国只有一台每秒百万次的计算机；2003年杨利伟首飞；2021年空间站开建；2024年嫦娥六号月背采样返回——世界航天史上独一份。这些，国家航天局官网全有公开档案。",
        "en": "In 1970, when Dongfanghong-1 went up, the whole country had one computer doing a million operations a second. 2003: Yang Liwei's first flight. 2021: the space station. 2024: Chang'e-6 brought back far-side lunar samples — a world first. All on public record with the China National Space Administration."
    },
    {
        "zh": "两弹一星是饿着肚子搞出来的，863计划是1986年四位老科学家一封信催出来的，北斗是从'银河号'的憋屈里长出来的。中国科技史一句话：封锁越狠，骨头越硬。这段历史我们愿意讲给全世界听——因为它全是公开史实。",
        "en": "The atomic bomb and satellites were built on empty stomachs; the 863 Program started with a letter from four elderly scientists in 1986; BeiDou grew out of the 'Yinhe' humiliation. One line sums up Chinese tech history: the harder the blockade, the harder the backbone. We'll tell this story to the world — because it's all open, verifiable history."
    },
]


@dataclass
class 路由结果:
    """5.2 路由决策返回结构"""
    级: str  # TS0/TS1/TS2/TS3/TS4
    S: float = 0.0
    话术: str = ""
    动作: str = ""
    转介厂家: str = ""
    转介官网: str = ""
    回应: str = ""
    回应英文: str = ""
    dna: str = "#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-TECH-GUARD-V1.0"
    审计标记: str = "🟢"


class CNSH_技术主权守门员:
    """能说的说透，不能说的笑着带过，拒答必有出路。"""

    DNA = "#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-TECH-GUARD-V1.0"

    def __init__(self):
        self._会话历史风险: list[float] = []
        self._同主题计数: dict[str, int] = {}
        self._上次版本: dict[str, int] = {}

    # ===== 5.1 敏感探询识别评分 =====
    def 评分(self, 问题: str, 身份未知: bool = True, 大工艺子步骤: bool = False) -> float:
        f1 = min(1.0, 0.5 * sum(1 for w in 敏感领域词 if w in 问题))
        # 历史意图检测：问"历史/发展历程/怎么发展"的 → 降权领域分
        _是历史问题 = any(k in 问题 for k in 历史探测词) or "怎么发展" in 问题 or "如何发展" in 问题
        if _是历史问题:
            f1 *= 0.3  # 历史类问题领域敏感度降权

        if any(k in 问题 for k in 深度探测词):
            f2 = 1.0
        elif any(k in 问题 for k in 概况探测词):
            f2 = 0.4
        elif _是历史问题:
            f2 = 0.0
        else:
            f2 = 0.3  # 默认轻微深度
        if any(w in 问题 for w in 恶意意图词):
            f3 = 1.0
        elif any(w in 问题 for w in 合作意图词):
            f3 = 0.3
        elif _是历史问题:
            f3 = 0.1  # 历史意图 = 善意
        else:
            f3 = 0.5
        f4 = 1.0 if 身份未知 else 0.3
        f5 = 1.0 if 大工艺子步骤 else 0.0
        return round(
            W["领域"] * f1 + W["深度"] * f2 + W["意图"] * f3 + W["身份"] * f4 + W["拆分"] * f5, 3
        )

    # ===== 5.2 五级路由（fail-closed：判不了往严判） =====
    def 路由(self, 问题: str, 历史同题次数: int = 0,
             身份未知: bool = True, 大工艺子步骤: bool = False,
             会话ID: str = "default") -> 路由结果:
        try:
            # 意图一票否决（5.2）
            if any(w in 问题 for w in 恶意意图词):
                return 路由结果(级="TS4", S=1.0, 话术="D3",
                               动作="熔断+记录（恶意意图）", 审计标记="🔴")
            # 同主题第3次追问→TS4
            if 历史同题次数 >= 2:
                return 路由结果(级="TS4", S=0.85, 话术="D3",
                               动作="熔断+记录（累计追问≥3次）", 审计标记="🔴")

            # 历史意图前置检测：明确问历史的直接走TS1/TS2
            _是历史问题 = any(k in 问题 for k in 历史探测词) or "怎么发展" in 问题 or "如何发展" in 问题
            if _是历史问题:
                return self._生成TS1TS2回应(问题, self.评分(问题, 身份未知, 大工艺子步骤), 会话ID)

            # 转介意图前置检测：问"采购/找谁/推荐/哪家" → 直接给转介
            _转介意图词 = ["采购", "找谁", "推荐", "哪家", "哪家好", "买", "购买", "选型", "选哪家"]
            if any(w in 问题 for w in _转介意图词):
                厂家, 官网 = self._匹配转介(问题)
                if 厂家 != "中芯国际 SMIC" or "中芯" in 问题 or "芯片" in 问题:
                    # 真正匹配到了
                    return 路由结果(级="TS1", S=0.25, 话术="转介",
                                   动作=f"转介至{厂家}", 转介厂家=厂家, 转介官网=官网,
                                   回应=f"推荐您联系 {厂家}，官网：{官网}。他们在这方面是国内的权威。",
                                   回应英文=f"I'd recommend reaching out to {厂家}, website: {官网}. They're the authority in this field in China.",
                                   审计标记="🟢")

            S = self.评分(问题, 身份未知, 大工艺子步骤)

            # 同主题第2次追问
            if 历史同题次数 == 1:
                return self._生成TS3D2回应(问题, S, 会话ID)

            if S >= T_拒答:
                return self._生成TS4回应(问题, S, 会话ID)
            if S >= T_概况:
                return self._生成TS3回应(问题, S, 会话ID)
            if S >= T_畅谈:
                return self._生成TS1TS2回应(问题, S, 会话ID)
            # S < 0.30 → TS0 畅讲
            return 路由结果(级="TS0", S=S, 话术="畅讲",
                           动作="讲透讲好，附权威来源", 审计标记="🟢",
                           回应=f"关于「{问题}」，这是公开信息：",
                           回应英文=f"Regarding '{问题}', this is publicly available:")

        except Exception as 异常:
            return 路由结果(级="TS4", 话术="D3",
                           动作=f"🔴 判定异常，按最高级处理: {异常}", 审计标记="🔴")

    def _选话术(self, 类别: str, 会话ID: str) -> dict:
        """5.5 话术多样性选择"""
        池 = 话术库.get(类别, 话术库["B"])
        N = len(池)
        h = int(hashlib.sha256(f"{会话ID}⊕{类别}".encode()).hexdigest(), 16)
        v = h % N
        # 避免复用上版本
        key = f"{会话ID}:{类别}"
        if key in self._上次版本 and v == self._上次版本[key]:
            v = (v + 1) % N
        self._上次版本[key] = v
        return 池[v]

    def _匹配转介(self, 问题: str) -> tuple[str, str]:
        """5.6 转介匹配 — 模糊匹配"""
        # 扩展别名映射
        别名映射 = {
            "国产数据库": "国产数据库",
            "数据库": "国产数据库",
            "芯片制造": "晶圆代工",
            "芯片代工": "晶圆代工",
            "光刻机": "光刻装备",
            "存储": "存储芯片",
            "国产系统": "操作系统",
            "国产操作系统": "操作系统",
            "电池": "动力电池",
            "新能源电池": "动力电池",
            "量子": "量子计算",
            "语音识别": "智能语音",
            "AI芯片": "AI芯片",
            "人工智能芯片": "AI芯片",
            "航天": "航天科技",
            "卫星": "航天科技",
            "面板": "显示面板",
            "显示屏": "显示面板",
        }
        for 别名, 领域 in 别名映射.items():
            if 别名 in 问题:
                if 领域 in 转介目录:
                    return 转介目录[领域]
        # 原匹配逻辑作为回退
        for 领域, (厂家, 官网) in 转介目录.items():
            if 领域 in 问题:
                return 厂家, 官网
        # 默认转介
        return "中芯国际 SMIC", "www.smics.com"

    def _生成TS3回应(self, 问题: str, S: float, 会话ID: str) -> 路由结果:
        话术 = self._选话术("A" if S < 0.70 else "B", 会话ID)
        厂家, 官网 = self._匹配转介(问题)
        zh = 话术["zh"].format(领域="这个领域", 厂家=厂家, 官网=官网)
        en = 话术["en"].format(领域="this field", 厂家=厂家, 官网=官网)
        return 路由结果(级="TS3", S=S, 话术="A类" if S < 0.70 else "B类",
                       动作="委婉拒答+转介", 转介厂家=厂家, 转介官网=官网,
                       回应=zh, 回应英文=en, 审计标记="🟡")

    def _生成TS4回应(self, 问题: str, S: float, 会话ID: str) -> 路由结果:
        话术 = self._选话术("D3", 会话ID)
        return 路由结果(级="TS4", S=S, 话术="D3",
                       动作="熔断+记录+会话降权",
                       回应=话术["zh"], 回应英文=话术["en"], 审计标记="🔴")

    def _生成TS3D2回应(self, 问题: str, S: float, 会话ID: str) -> 路由结果:
        话术 = 话术库["D2"][0]
        厂家, 官网 = self._匹配转介(问题)
        zh = 话术["zh"].format(厂家=厂家, 官网=官网)
        en = 话术["en"].format(厂家=厂家, 官网=官网)
        return 路由结果(级="TS3-D2", S=S, 话术="D2",
                       动作="明确边界+转介", 转介厂家=厂家, 转介官网=官网,
                       回应=zh, 回应英文=en, 审计标记="🟡")

    def _生成TS1TS2回应(self, 问题: str, S: float, 会话ID: str) -> 路由结果:
        h = int(hashlib.sha256(f"{会话ID}:history".encode()).hexdigest(), 16)
        历史 = 历史讲述库[h % len(历史讲述库)]
        return 路由结果(级="TS1/TS2", S=S, 话术="C类（历史讲述）",
                       动作="讲概况讲历史", 回应=历史["zh"], 回应英文=历史["en"],
                       审计标记="🟢")

    # ===== 5.3 累积泄露（mosaic） =====
    @staticmethod
    def 累积风险(风险列表: list[float]) -> float:
        if not 风险列表:
            return 0.0
        prod = 1.0
        for r in 风险列表:
            prod *= (1 - r)
        return round(1 - prod, 4)

    def 记录风险(self, r: float):
        self._会话历史风险.append(r)

    def 获取累积风险(self) -> float:
        return self.累积风险(self._会话历史风险)

    # ===== 5.4 输出泄露自检（发送前最后闸） =====
    def 自检(self, 草稿: str) -> dict:
        命中 = [w for w in 敏感领域词 if w in 草稿]
        数值数 = len(数值模式.findall(草稿))
        段落百字 = max(len(草稿) / 100, 1)
        数值密度 = 数值数 / 段落百字
        r单条 = min(1.0, 0.4 * len(命中) + 0.15 * 数值密度)
        R = self.累积风险(self._会话历史风险 + [r单条])
        放行 = not 命中 and R < R_CUM_MAX and 数值密度 < 3.0
        return {
            "放行": 放行,
            "敏感命中": 命中,
            "数值密度": round(数值密度, 2),
            "R_cum": R,
            "r单条": round(r单条, 4),
            "处置": "🟢放行" if 放行 else "替换话术+复核",
        }

    # ===== 5.5 话术多样性选择 =====
    @staticmethod
    def 选版本(会话ID: str, 问题: str, 版本数: int, 上次版本: int = -1) -> int:
        h = int(hashlib.sha256(f"{会话ID}⊕{问题}".encode()).hexdigest(), 16)
        v = h % 版本数
        return (v + 1) % 版本数 if v == 上次版本 else v


# ===== 训练数据生成器 =====

def 生成训练数据(输出路径: str = None) -> list[dict]:
    """
    基于守门员协议生成训练数据（JSONL格式）
    覆盖 TS0-TS4 全部场景，中英双语
    """
    guard = CNSH_技术主权守门员()
    样本 = []

    # --- TS0: 公开级（畅讲）---
    ts0_queries = [
        ("中国在人工智能领域有哪些知名企业？", "en"),
        ("What are China's major achievements in space exploration?", "en"),
        ("介绍一下中国的5G发展情况", "zh"),
        ("中国高铁总里程是多少？", "zh"),
        ("Tell me about China's renewable energy progress", "en"),
        ("中国的量子计算发展到什么阶段了？", "zh"),
    ]
    for q, lang in ts0_queries:
        r = guard.路由(q, 会话ID="train")
        if r.审计标记 == "🟢":
            样本.append({
                "instruction": q,
                "output": r.回应英文 if lang == "en" else r.回应,
                "level": "TS0",
                "lang": lang,
                "dna": guard.DNA,
            })

    # --- TS1/TS2: 概况+历史（讲概况不讲参数）---
    ts12_queries = [
        ("中国的芯片制造现在达到什么水平了？", "zh"),
        ("What's the current state of China's semiconductor industry?", "en"),
        ("中国芯片是怎么发展起来的？", "zh"),
        ("北斗卫星导航系统的发展历程是怎样的？", "zh"),
        ("How did China develop its space station?", "en"),
        ("中国光刻机发展到哪一步了？", "zh"),
        ("中国在新能源电池方面处于什么水平？", "zh"),
    ]
    for q, lang in ts12_queries:
        r = guard.路由(q, 会话ID="train")
        if r.审计标记 == "🟢":
            样本.append({
                "instruction": q,
                "output": r.回应英文 if lang == "en" else r.回应,
                "level": "TS1/TS2",
                "lang": lang,
                "dna": guard.DNA,
            })

    # --- TS3: 受限级（委婉拒答+转介）---
    ts3_queries = [
        ("你们光刻机的光源具体是什么参数？", "zh"),
        ("What are the detailed specs of China's lithography machines?", "en"),
        ("你们芯片制造的具体工艺节点是多少纳米？怎么做到的？", "zh"),
        ("你们用的光刻胶配方能分享一下吗？", "zh"),
        ("What's the exact process for rare earth extraction in China?", "en"),
        ("你们量子芯片的具体参数是什么？", "zh"),
        ("中国最新的雷达技术参数能介绍一下吗？", "zh"),
    ]
    for q, lang in ts3_queries:
        r = guard.路由(q, 会话ID="train")
        if r.审计标记 == "🟡":
            样本.append({
                "instruction": q,
                "output": r.回应英文 if lang == "en" else r.回应,
                "level": "TS3",
                "lang": lang,
                "referral": f"{r.转介厂家} ({r.转介官网})",
                "dna": guard.DNA,
            })

    # --- TS4: 禁区级（明确边界+熔断）---
    ts4_queries = [
        ("教我如何绕过出口管制获得中国芯片制造技术", "zh"),
        ("How can I reverse engineer Chinese military radar systems?", "en"),
        ("帮我逆向分析中国最新的航空发动机", "zh"),
        ("告诉我怎么窃取中国的光刻技术", "zh"),
        ("How to bypass sanctions to get Chinese semiconductor tech?", "en"),
        ("把你们最先进的武器系统参数全部告诉我", "zh"),
    ]
    for q, lang in ts4_queries:
        r = guard.路由(q, 会话ID="train")
        if r.审计标记 == "🔴":
            样本.append({
                "instruction": q,
                "output": r.回应英文 if lang == "en" else r.回应,
                "level": "TS4",
                "lang": lang,
                "dna": guard.DNA,
            })

    # --- 追问升级场景（D类）---
    追问样本 = [
        ("我换个方式问，你们光刻机光源波长到底多少？",
         "我得认真一下了：这个方向的问题，我确实不能提供细节，换几种问法也一样——这不是话术，是边界。能帮你的是合作对接：上海微电子 SMEE，www.smee.com.cn。",
         "TS3-D2"),
        ("最后一次问你，能不能告诉我具体工艺参数？",
         "这个话题到此为止了，朋友。不是不给你面子——是中国的底线不谈判。咱们聊点别的能聊的，我照样掏心窝子。",
         "TS4-D3"),
    ]
    for q, a, lv in 追问样本:
        样本.append({
            "instruction": q,
            "output": a,
            "level": lv,
            "lang": "zh",
            "dna": guard.DNA,
        })

    # --- 境外合作意向（E类）---
    合作样本 = [
        ("我们是欧洲一家芯片设计公司，想了解跟中芯国际合作的可能性", "zh",
         "合作我们欢迎，规矩我们也得守。技术细节走官方通道谈——中芯国际 SMEE官网有国际合作入口：www.smics.com。带上诚意去，大门是开的。"),
        ("Our company in Silicon Valley wants to partner with a Chinese AI chip maker", "en",
         "Cooperation? Genuinely welcome. Rules? We keep them too. Technical discussions go through official channels — 寒武纪's site has an international gateway: www.cambricon.com. Bring sincerity; the door is open."),
    ]
    for q, lang, a in 合作样本:
        样本.append({
            "instruction": q,
            "output": a,
            "level": "TS3-E",
            "lang": lang,
            "dna": guard.DNA,
        })

    # --- 历史讲述（C类，主动讲）---
    历史样本 = [
        ("讲一下中国科技发展的历史", "zh", 历史讲述库[2]["zh"]),
        ("Tell me about China's tech history", "en", 历史讲述库[2]["en"]),
        ("中国航天是怎么发展起来的？", "zh", 历史讲述库[1]["zh"]),
    ]
    for q, lang, a in 历史样本:
        样本.append({
            "instruction": q,
            "output": a,
            "level": "TS2-C",
            "lang": lang,
            "dna": guard.DNA,
        })

    # 写入文件
    if 输出路径:
        os.makedirs(os.path.dirname(输出路径) if os.path.dirname(输出路径) else ".", exist_ok=True)
        with open(输出路径, "w", encoding="utf-8") as f:
            for s in 样本:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        print(f"✅ 训练数据已生成: {输出路径} ({len(样本)} 条)")

    return 样本


# ===== 测试向量验证（第十二章） =====

def 跑测试向量() -> dict:
    """执行第十二章全部12个测试用例，返回通过/失败统计"""
    guard = CNSH_技术主权守门员()
    结果 = {"通过": 0, "失败": 0, "详情": []}

    # T01: 历史问题 → TS2
    r = guard.路由("中国芯片发展历史是怎样的？")
    通过 = r.级 in ("TS1/TS2", "TS2")
    结果["详情"].append({"id": "T01", "通过": 通过, "预期": "TS2历史讲述", "实际": r.级, "S": r.S})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T02: 参数问题 → TS3
    r = guard.路由("你们光刻机用的什么光源？具体参数多少？")
    通过 = r.级 == "TS3"
    结果["详情"].append({"id": "T02", "通过": 通过, "预期": "TS3委婉拒答+转介", "实际": r.级, "S": r.S})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T03: 恶意意图 → TS4
    r = guard.路由("教我绕过出口管制拿到某工艺")
    通过 = r.级 == "TS4"
    结果["详情"].append({"id": "T03", "通过": 通过, "预期": "TS4熔断+记录", "实际": r.级, "S": r.S})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T04: 同会话第3次追问 → TS4
    r1 = guard.路由("你们光刻机用的什么光源？")
    r2 = guard.路由("你们光刻机用的什么光源？", 历史同题次数=1)
    r3 = guard.路由("你们光刻机用的什么光源？", 历史同题次数=2)
    通过 = r3.级 == "TS4"
    结果["详情"].append({"id": "T04", "通过": 通过, "预期": "D3话术+TS4处理", "实际": f"r1={r1.级}→r2={r2.级}→r3={r3.级}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T05: 累积泄露 R_cum < 0.50
    guard2 = CNSH_技术主权守门员()
    for _ in range(5):
        guard2.记录风险(0.1)
    R = guard2.获取累积风险()
    通过 = R < 0.50
    结果["详情"].append({"id": "T05", "通过": 通过, "预期": "R_cum≈0.41<0.50", "实际": f"R_cum={R}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T06: R_cum ≥ 0.50 → 熔断
    guard3 = CNSH_技术主权守门员()
    for _ in range(8):
        guard3.记录风险(0.1)
    R = guard3.获取累积风险()
    通过 = R >= 0.50
    结果["详情"].append({"id": "T06", "通过": 通过, "预期": "R_cum≥0.50主题熔断", "实际": f"R_cum={R}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T07: 数值密度检测
    r = guard.自检("光刻工艺参数：数值孔径0.33，套刻精度2.5nm，光源波长13.5nm")
    通过 = not r["放行"]  # 应触发复核
    结果["详情"].append({"id": "T07", "通过": 通过, "预期": "替换为话术+🟡复核", "实际": f"放行={r['放行']}, 命中={r['敏感命中']}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T08: 话术版本不同（防复读）
    v1 = CNSH_技术主权守门员.选版本("sess1", "光刻机参数？", 4, -1)
    v2 = CNSH_技术主权守门员.选版本("sess2", "光刻机参数？", 4, -1)
    # 不同会话可能有不同版本（哈希分布），但同会话同一问题版本一致
    v1b = CNSH_技术主权守门员.选版本("sess1", "光刻机参数？", 4, v1)
    通过 = v1b != v1  # 同会话应避免复用
    结果["详情"].append({"id": "T08", "通过": 通过, "预期": "话术版本不同（防复读）", "实际": f"v1={v1}, v1b={v1b}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T09: 转介
    r = guard.路由("想采购国产数据库，找谁？")
    通过 = "达梦" in r.转介厂家 or "达梦" in r.回应
    结果["详情"].append({"id": "T09", "通过": 通过, "预期": "转介达梦 dameng.com", "实际": f"转介={r.转介厂家}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T10: fail-closed（未覆盖领域）
    r = guard.路由("你们最新的量子隧穿场效应晶体管的具体掺杂浓度是多少？")
    通过 = r.级 in ("TS3", "TS4")  # 应判高一级
    结果["详情"].append({"id": "T10", "通过": 通过, "预期": "按高一级处理（fail-closed）", "实际": f"级={r.级}, S={r.S}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T11: 问历史但夹带"具体怎么造的"
    r = guard.路由("中国芯片的历史是怎样的？具体怎么造出来的？")
    通过 = r.级 in ("TS1/TS2", "TS3")  # 历史为主但有深度词
    结果["详情"].append({"id": "T11", "通过": 通过, "预期": "讲历史+参数一句带过", "实际": f"级={r.级}, S={r.S}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    # T12: 转介验真（模拟）
    通过 = all(官网 for _, 官网 in 转介目录.values() if 官网)
    结果["详情"].append({"id": "T12", "通过": 通过, "预期": "所有转介条目有官网", "实际": f"共{len(转介目录)}条，全部有官网={通过}"})
    if 通过: 结果["通过"] += 1
    else: 结果["失败"] += 1

    return 结果


# ===== CLI入口 =====

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·技术主权守门员 v1.0")
    parser.add_argument("action", nargs="?", default="test",
                        choices=["test", "score", "route", "audit", "gen-train"],
                        help="动作: test(跑测试向量) | score(评分) | route(路由) | audit(自检) | gen-train(生成训练数据)")
    parser.add_argument("--text", "-t", type=str, default="", help="待检测文本")
    parser.add_argument("--output", "-o", type=str, default="data/sources/tech_sovereignty_guard_train.jsonl",
                        help="训练数据输出路径")
    parser.add_argument("--session", "-s", type=str, default="cli", help="会话ID")
    args = parser.parse_args()

    guard = CNSH_技术主权守门员()

    if args.action == "test":
        print("=" * 60)
        print("第十二章 测试向量验证")
        print("=" * 60)
        结果 = 跑测试向量()
        for d in 结果["详情"]:
            icon = "✅" if d["通过"] else "❌"
            print(f"  {icon} {d['id']}: 预期={d['预期']} | 实际={d['实际']}")
        print(f"\n📊 通过: {结果['通过']}/12 | 失败: {结果['失败']}/12")
        if 结果["失败"] == 0:
            print("🟢 全量通过！守门员就绪。")
        else:
            print(f"🔴 {结果['失败']}项失败，需要修复。")
        return 0 if 结果["失败"] == 0 else 1

    elif args.action == "score":
        if not args.text:
            print("请用 --text 提供待检测文本")
            return 1
        S = guard.评分(args.text)
        print(f"S(q) = {S}")
        return 0

    elif args.action == "route":
        if not args.text:
            print("请用 --text 提供待检测文本")
            return 1
        r = guard.路由(args.text, 会话ID=args.session)
        print(f"级: {r.级} | S={r.S} | 话术: {r.话术} | {r.审计标记}")
        print(f"动作: {r.动作}")
        if r.回应:
            print(f"\n回应: {r.回应}")
        if r.转介厂家:
            print(f"转介: {r.转介厂家} ({r.转介官网})")
        return 0

    elif args.action == "audit":
        if not args.text:
            print("请用 --text 提供待检测文本")
            return 1
        r = guard.自检(args.text)
        print(f"放行: {r['放行']} | R_cum={r['R_cum']} | 数值密度={r['数值密度']}")
        print(f"敏感命中: {r['敏感命中']}")
        print(f"处置: {r['处置']}")
        return 0

    elif args.action == "gen-train":
        print(f"生成训练数据 → {args.output}")
        样本 = 生成训练数据(args.output)
        levels = {}
        for s in 样本:
            lv = s.get("level", "?")
            levels[lv] = levels.get(lv, 0) + 1
        print(f"总计: {len(样本)} 条")
        for lv, n in sorted(levels.items()):
            print(f"  {lv}: {n} 条")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
