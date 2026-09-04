#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622｜龍芯北辰自动收口协议 — 可执行引擎 v2.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
版本: v2.0
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-AUTO-CLOSURE-ENGINE-v2.0
父DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-AUTO-CLOSURE-ENGINE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  - C1/C2/C3 三档收口自动检测与渲染
  - P0/P1/P2 内容智能分层（支持 Markdown 段落与结构化提取）
  - DNA 链式追溯（父→子可验证，内容哈希锚定）
  - 洛书九宫状态自动映射
  - 一票否决与验收清单分级验证
  - 知识库自动提交（dragon_knowledge.db）
  - 向量库联动感知
  - 审计日志自动持久化

用法：
  python3 自动收口协议.py --help
  python3 自动收口协议.py --提交 <文件路径> [选项]
  python3 自动收口协议.py --demo-c1
  python3 自动收口协议.py --demo-c2
  python3 自动收口协议.py --demo-c3
  python3 自动收口协议.py --验收
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any

# ═══════════════════════════════════════════════════════════
# 常量定义 | 不动点
# ═══════════════════════════════════════════════════════════

DNA_PREFIX = "#龍芯⚡️"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_CODE = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROTOCOL_VERSION = "v2.0"
ENGINE_VERSION = "v2.0"

DB_PATH = os.path.expanduser("~/_work/dragon_knowledge.db")
VECTOR_PATH = os.path.expanduser("~/_work/formula_alignment_v1_6_vectors.json")

# C1 轻收口触发词
C1触发词 = [
    "懂了", "是吧", "你说呢", "这个算吗", "我明白了", "先这样",
    "记一下", "这个归哪", "这个是不是P1", "这个是不是P2",
    "知道了", "好的", "OK", "ok", "可以", "行", "嗯", "哦",
    "这样就行", "暂时这样", "先记下", "回头再说", "没问题",
    "明白了", "清楚了", "了解", "收到", "先记着"
]

# C2 标准收口触发词
C2触发词 = [
    "补齐", "默认全补", "落地", "工程包", "给 Cursor", "给Cursor",
    "Notion页面", "技术文档", "页面结构", "帮我审查", "帮我完善",
    "自动补充", "不要遗漏", "输出可复制", "验收清单", "一票否决",
    "决策卡片", "固定模板", "CNSH", "ROOT_CARD", "审查并完善",
    "结构", "字段", "字段清单", "文档", "协议", "规则", "完善",
    "补充", "修正", "调整", "检查", "审查", "审阅",
    "规范化", "标准化", "格式化", "可复制", "可执行", "代码",
    "脚本", "模块", "系统", "版本", "定盘", "路由", "配置"
]

# C3 阶段收口触发词
C3触发词 = [
    "收口", "闭环", "归档", "阶段完成", "下一阶段", "新窗口",
    "DNA总结", "里程碑快照", "上下文压缩", "窗口污染", "新窗口续航",
    "主体闭环", "论文主体闭环", "准备切窗口", "准备给别的AI",
    "准备给Claude", "准备给Cursor", "准备放Notion", "阶段收口",
    "里程碑", "总结", "迁移", "切换", "切窗口",
    "完结", "结束", "完成", "收尾", "收尾工作", "存档",
    "续航", "交接", "移交", "转交", "转移", "快照",
    "提交", "审核过", "已审核", "入库", "落库"
]

# P0 永恒层关键词
P0关键词 = [
    "CONFIRM", "SEAL", "GPG", "DNA", "UID9622", "龍芯北辰",
    "主控", "主权", "永恒", "铁律", "君子协议", "三色审计",
    "ai是工具", "ai是服务员", "不反客为主", "不说教",
    "不驯化", "不假执行", "没执行不说已执行", "没同步不说已同步",
    "一世一双人", "龍魂ID", "数字人民币", "宪法层", "根稳定"
]

# P2 临时层关键词
P2关键词 = [
    "闲聊", "牢骚", "抱怨", "吐槽", "随便聊聊", "无所谓",
    "不重要", "随便", "随便说说", "临时", "试一下", "看看",
    "可能", "也许", "大概", "随便想想", "发散", "联想",
    "如果", "假设", "比如", "例如", "假设性", "猜测", "试试看"
]

# ═══════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════

class 收口档位(Enum):
    C1轻收口 = "C1"
    C2标准收口 = "C2"
    C3阶段收口 = "C3"
    未触发 = "NONE"

class 层级(Enum):
    P0永恒 = "P0"
    P1当前 = "P1"
    P2临时 = "P2"

class 三色(Enum):
    绿 = "🟢"
    黄 = "🟡"
    红 = "🔴"

class 数据级别(Enum):
    公开 = "PUBLIC"
    内部 = "INTERNAL"
    受限 = "RESTRICTED"
    机密 = "SECRET"

class 隐私模式(Enum):
    标准 = "normal"
    最小化 = "minimal"
    完全私密 = "private"

# ═══════════════════════════════════════════════════════════
# 数据类定义
# ═══════════════════════════════════════════════════════════

@dataclass
class DNA追溯:
    """DNA 追溯节点：支持父链、内容哈希、确定性生成"""
    项目: str
    模块: str
    版本: str
    时间戳: str = ""
    父DNA: str = ""
    内容哈希: str = ""
    变更描述: str = ""

    def __post_init__(self):
        if not self.时间戳:
            self.时间戳 = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def 生成DNA(self) -> str:
        base = f"{DNA_PREFIX}{self.时间戳}-{self.项目}-{self.模块}-{self.版本}"
        chain_input = f"{base}|父:{self.父DNA}|内容:{self.内容哈希}|描述:{self.变更描述}"
        h = hashlib.sha256(chain_input.encode()).hexdigest()[:16]
        return f"{base}-HASH{h}"

    def 生成简短DNA(self) -> str:
        """C1 轻收口使用的最小 DNA"""
        base = f"{DNA_PREFIX}{self.时间戳}-{self.项目}-{self.模块}-{self.版本}"
        return base


@dataclass
class 洛书九宫:
    """洛书九宫状态：与 P0/P1/P2 及执行链映射"""
    中宫5_主控意志: str = "UID9622主控"
    九宫_战略目标: str = ""
    一宫_已执行结果: str = ""
    三宫_当前意图: str = ""
    七宫_决策路由: str = ""
    八宫_安全风险: str = ""
    四宫_边界主权: str = ""
    二宫_回流留痕: str = ""
    六宫_验收签章: str = ""

    def 更新(self, 宫位: str, 内容: str):
        if hasattr(self, 宫位):
            setattr(self, 宫位, 内容)

    def 序列化(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class 审计条目:
    """三色审计条目"""
    级别: 三色
    模块: str
    消息: str
    时间戳: str = ""
    数据: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.时间戳:
            self.时间戳 = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "级别": self.级别.value,
            "模块": self.模块,
            "消息": self.消息,
            "时间戳": self.时间戳,
            "数据": self.数据
        }


@dataclass
class 收口结果:
    """收口输出结果"""
    档位: 收口档位
    内容: str
    层级映射: Dict[str, List[str]] = field(default_factory=dict)
    审计日志: List[审计条目] = field(default_factory=list)
    DNA: str = ""
    父DNA: str = ""
    验证通过: bool = True
    一票否决项: List[str] = field(default_factory=list)
    验收结果: Dict[str, Any] = field(default_factory=dict)
    知识库条目ID: str = ""
    输出文件: str = ""


@dataclass
class 内容分层结果:
    """结构化内容分层结果"""
    P0: List[Dict[str, str]] = field(default_factory=list)  # [{"来源": "段落/章节", "内容": ""}]
    P1: List[Dict[str, str]] = field(default_factory=list)
    P2: List[Dict[str, str]] = field(default_factory=list)
    元信息: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════
# 核心引擎：自动收口协议 v2.0
# ═══════════════════════════════════════════════════════════

class 自动收口引擎:
    """
    UID9622 自动收口协议核心引擎 v2.0
    三档收口：C1轻 / C2标准 / C3阶段
    DNA 链式追溯、知识库联动、审计持久化
    """

    def __init__(self, 父DNA: str = "", 项目: str = "AUTO-CLOSURE", 模块: str = "PROTOCOL"):
        self.项目 = 项目
        self.模块 = 模块
        self.父DNA = 父DNA or f"{DNA_PREFIX}2026-06-28-AUTO-CLOSURE-ENGINE-v1.0"
        self.DNA = self._生成引擎DNA()
        self.审计器: List[审计条目] = []
        self.九宫 = 洛书九宫()
        self.历史输入: List[str] = []
        self.上下文轮数: int = 0
        self._初始化九宫()
        self._绿记录("引擎初始化", f"自动收口引擎 v{ENGINE_VERSION} 启动", {"父DNA": self.父DNA})

    # ── DNA 与审计 ──

    def _生成引擎DNA(self) -> str:
        dna_obj = DNA追溯(
            项目=self.项目,
            模块=self.模块,
            版本=ENGINE_VERSION,
            父DNA=self.父DNA,
            内容哈希=hashlib.sha256(f"{self.项目}-{self.模块}-{ENGINE_VERSION}".encode()).hexdigest()[:16],
            变更描述="引擎初始化"
        )
        return dna_obj.生成DNA()

    def _生成内容DNA(self, 内容: str, 变更描述: str = "") -> str:
        内容哈希 = hashlib.sha256(内容.encode()).hexdigest()[:16]
        dna_obj = DNA追溯(
            项目=self.项目,
            模块=self.模块,
            版本=PROTOCOL_VERSION,
            父DNA=self.DNA,
            内容哈希=内容哈希,
            变更描述=变更描述
        )
        return dna_obj.生成DNA()

    def _初始化九宫(self):
        self.九宫.中宫5_主控意志 = "UID9622主控·AI工具定位"
        self.九宫.九宫_战略目标 = "自动收口·分层归档·DNA续航·防上下文污染"
        self.九宫.四宫_边界主权 = "P0永恒保留·P1摘要保留·P2可丢弃"
        self.九宫.八宫_安全风险 = "三色审计·一票否决·CONFIRM/SEAL/GPG"

    def _绿记录(self, 模块: str, 消息: str, 数据: dict[str, Any] = None):
        self.审计器.append(审计条目(三色.绿, 模块, 消息, 数据=数据 or {}))

    def _黄记录(self, 模块: str, 消息: str, 数据: dict[str, Any] = None):
        self.审计器.append(审计条目(三色.黄, 模块, 消息, 数据=数据 or {}))

    def _红记录(self, 模块: str, 消息: str, 数据: dict[str, Any] = None):
        self.审计器.append(审计条目(三色.红, 模块, 消息, 数据=数据 or {}))

    def 获取DNA(self) -> str:
        return self.DNA

    # ── 触发词检测 ──

    def 检测收口档位(self, 用户输入: str) -> 收口档位:
        """根据用户输入判断应使用的收口档位"""
        输入小写 = 用户输入.lower().strip()
        self.历史输入.append(用户输入)
        self.上下文轮数 += 1

        # 优先检测 C3（最高优先级）
        for 词 in C3触发词:
            if 词.lower() in 输入小写:
                self._绿记录("档位检测", f"命中C3触发词: {词}")
                return 收口档位.C3阶段收口

        # 检测 C2
        for 词 in C2触发词:
            if 词.lower() in 输入小写:
                self._绿记录("档位检测", f"命中C2触发词: {词}")
                return 收口档位.C2标准收口

        # 检测 C1
        for 词 in C1触发词:
            if 词 in 用户输入:
                self._绿记录("档位检测", f"命中C1触发词: {词}")
                return 收口档位.C1轻收口

        # 上下文轮数判断
        if self.上下文轮数 >= 10:
            self._黄记录("档位检测", f"上下文轮数{self.上下文轮数}，建议C3收口")

        self._绿记录("档位检测", "未命中触发词，默认C1")
        return 收口档位.C1轻收口

    def 批量检测(self, 输入列表: List[str]) -> List[Tuple[str, 收口档位]]:
        """批量检测多个输入的收口档位"""
        结果 = []
        for 输入 in 输入列表:
            档位 = self.检测收口档位(输入)
            结果.append((输入, 档位))
        return 结果

    # ── P0/P1/P2 内容分层 v2.0 ──

    def 内容分层(self, 内容: str) -> 内容分层结果:
        """
        智能内容分层：
        - 优先按 Markdown 二级标题切分区块
        - 每个区块内按句子判断 P0/P1/P2
        - 返回结构化结果，保留来源信息
        """
        结果 = 内容分层结果()

        if not 内容 or not 内容.strip():
            return 结果

        # 提取文档级元信息
        结果.元信息["总字数"] = len(内容)
        结果.元信息["段落数"] = len([l for l in 内容.split('\n') if l.strip()])

        # 按二级标题切分区块
        区块模式 = re.compile(r'^(#{2,3}\s+.+?)\n(.*?)(?=^#{2,3}\s|\Z)', re.MULTILINE | re.DOTALL)
        区块列表 = list(区块模式.finditer(内容))

        if not 区块列表:
            # 没有二级标题，整体作为一个区块处理
            self._分层单个区块("(全文)", 内容, 结果)
        else:
            for m in 区块列表:
                标题 = m.group(1).strip()
                正文 = m.group(2).strip()
                self._分层单个区块(标题, 正文, 结果)

        self._绿记录("内容分层", f"P0:{len(结果.P0)} P1:{len(结果.P1)} P2:{len(结果.P2)}", 结果.元信息)
        return 结果

    def _分层单个区块(self, 来源: str, 正文: str, 结果: 内容分层结果):
        """对单个区块进行 P0/P1/P2 分层"""
        # 按句子分割
        句子列表 = re.split(r'[。！？\n]+', 正文)
        区块P0 = []
        区块P1 = []
        区块P2 = []

        for 句子 in 句子列表:
            句子 = 句子.strip()
            if not 句子:
                continue

            # 检查是否是元信息行（如 DNA、版本、GPG 等）
            if self._是P0元信息(句子):
                区块P0.append(句子)
                continue

            # P0 检测
            if self._命中P0(句子):
                区块P0.append(句子)
                continue

            # P2 检测
            if self._命中P2(句子):
                区块P2.append(句子)
                continue

            # 默认 P1
            区块P1.append(句子)

        # 如果整个区块都是 P0（如铁律段），全部归 P0
        if len(区块P0) > len(区块P1) + len(区块P2) and len(区块P0) >= 2:
            结果.P0.append({"来源": 来源, "内容": "\n".join(区块P0)})
        else:
            if 区块P0:
                结果.P0.append({"来源": 来源, "内容": "\n".join(区块P0)})
            if 区块P1:
                结果.P1.append({"来源": 来源, "内容": "\n".join(区块P1)})
            if 区块P2:
                结果.P2.append({"来源": 来源, "内容": "\n".join(区块P2)})

    def _是P0元信息(self, 句子: str) -> bool:
        """检测是否包含 DNA/CONFIRM/SEAL/GPG 等元信息"""
        return bool(re.search(r'(DNA[:：]|CONFIRM|SEAL|GPG[:：]|#龍芯⚡️)', 句子))

    def _命中P0(self, 句子: str) -> bool:
        句子小写 = 句子.lower()
        for 关键词 in P0关键词:
            if 关键词.lower() in 句子小写:
                return True
        return False

    def _命中P2(self, 句子: str) -> bool:
        for 关键词 in P2关键词:
            if 关键词 in 句子:
                return True
        return False

    # ── 一票否决检查 v2.0 ──

    def 一票否决检查(self, 档位: 收口档位, 输出内容: str, 输入内容: str = "") -> List[str]:
        """检查输出是否违反一票否决规则"""
        否决项 = []

        # V1: 普通聊天强行大收口
        if 档位 == 收口档位.C1轻收口 and "ROOT_CARD" in 输出内容:
            否决项.append("V1: C1档位不应包含ROOT_CARD")
            self._红记录("一票否决", "C1包含ROOT_CARD")

        # V2: 正式文档没有验收清单
        if 档位 == 收口档位.C2标准收口 and "验收清单" not in 输出内容:
            否决项.append("V2: C2缺少验收清单")
            self._红记录("一票否决", "C2缺少验收")

        # V3: 阶段完成没有DNA总结
        if 档位 == 收口档位.C3阶段收口 and "DNA 总结" not in 输出内容:
            否决项.append("V3: C3缺少DNA总结")
            self._红记录("一票否决", "C3缺少DNA")

        # V4: P0被压缩或改写
        # 仅当存在明确的改写/覆盖 P0 核心元素的语义，且非"不改写/禁止改写"语境时才触发
        p0_rewrite_patterns = [
            r"(?:改写|修改|重写|替换|覆盖|变更|调整)\s*[了过]?[\s:：]*(?:P0|CONFIRM码?|SEAL|GPG|铁律|主权|永恒|DNA)",
            r"(?:P0|CONFIRM码?|SEAL|GPG|铁律|主权|永恒|DNA)\s*(?:被|遭|予以|需要|必须|可以)?\s*(?:改写|修改|重写|替换|覆盖|变更|调整)",
        ]
        if not re.search(r"(?:不|禁止|不得|勿|拒绝|防止|避免)\s*(?:改写|修改|重写|替换|覆盖)", 输出内容):
            for pattern in p0_rewrite_patterns:
                if re.search(pattern, 输出内容, re.IGNORECASE):
                    否决项.append("V4: P0内容被改写")
                    self._红记录("一票否决", "P0被改写")
                    break

        # V5: C3 缺少 CONFIRM/SEAL/GPG
        if 档位 == 收口档位.C3阶段收口:
            if CONFIRM_CODE not in 输出内容:
                否决项.append("V5: C3缺少CONFIRM确认码")
                self._红记录("一票否决", "缺少CONFIRM")
            if SEAL_CODE not in 输出内容:
                否决项.append("V5: C3缺少SEAL签章")
                self._红记录("一票否决", "缺少SEAL")
            if GPG_FINGERPRINT not in 输出内容:
                否决项.append("V5: C3缺少GPG指纹")
                self._红记录("一票否决", "缺少GPG")

        # V6: 假执行声明
        假执行模式 = [
            r"已执行.*没有.*执行", r"已同步.*没有.*同步",
            r"已落盘.*没有.*写入", r"已完成.*没有.*完成"
        ]
        for 模式 in 假执行模式:
            if re.search(模式, 输出内容):
                否决项.append(f"V6: 检测到假执行声明: {模式}")
                self._红记录("一票否决", "假执行声明")

        # V7: DNA 断裂（无 DNA 前缀）
        if DNA_PREFIX not in 输出内容:
            否决项.append("V7: 输出缺少DNA追溯")
            self._红记录("一票否决", "缺少DNA")

        # V8: 涉及密钥/删除/发布但未 BLOCKED
        高风险词 = ["rm -rf", "git push", "token", "私钥", "sudo"]
        if any(w in 输入内容.lower() for w in 高风险词) and "BLOCKED" not in 输出内容.upper():
            否决项.append("V8: 高风险输入未BLOCKED")
            self._红记录("一票否决", "高风险未拦截")

        return 否决项

    # ── 验收清单验证 v2.0 ──

    def 验收验证(self, 档位: 收口档位, 输出内容: str) -> Dict[str, any]:
        """分级验收验证：C1/C2/C3 各有独立清单"""
        if 档位 == 收口档位.C1轻收口:
            return self._验收C1(输出内容)
        elif 档位 == 收口档位.C2标准收口:
            return self._验收C2(输出内容)
        elif 档位 == 收口档位.C3阶段收口:
            return self._验收C3(输出内容)
        else:
            return {"档位识别": False, "三色": "🔴", "通过率": "0/1"}

    def _验收C1(self, 输出内容: str) -> Dict[str, any]:
        验收项 = {
            "档位识别": True,
            "轻收口标记": "【轻收口】" in 输出内容,
            "归属明确": "归属：" in 输出内容,
            "结论明确": "结论：" in 输出内容,
            "下一步动作": "下一步：" in 输出内容,
            "避免过度收口": "ROOT_CARD" not in 输出内容,
            "无假执行": "已执行" not in 输出内容 or ("已执行" in 输出内容 and "未执行" not in 输出内容),
            "DNA最小追溯": DNA_PREFIX in 输出内容,
        }
        return self._计算通过率(验收项)

    def _验收C2(self, 输出内容: str) -> Dict[str, any]:
        验收项 = {
            "档位识别": "【标准收口】" in 输出内容,
            "定盘明确": "A｜当前定盘" in 输出内容,
            "补全内容": "B｜补全内容" in 输出内容,
            "文件清单": "D｜文件" in 输出内容,
            "验收清单": "F｜验收清单" in 输出内容,
            "下一步动作": "G｜下一步" in 输出内容,
            "ROOT_CARD": "ROOT_CARD" in 输出内容,
            "避免过度收口": "DNA 总结" not in 输出内容,
            "CONFIRM保留": CONFIRM_CODE in 输出内容,
            "SEAL保留": SEAL_CODE in 输出内容,
            "GPG保留": GPG_FINGERPRINT in 输出内容,
            "DNA存在": DNA_PREFIX in 输出内容,
        }
        return self._计算通过率(验收项)

    def _验收C3(self, 输出内容: str) -> Dict[str, any]:
        验收项 = {
            "档位识别": "【阶段收口】" in 输出内容,
            "DNA总结": "A｜DNA 总结" in 输出内容,
            "P0不动点": "B｜P0" in 输出内容 and "P0" in 输出内容,
            "P1核心": "C｜P1" in 输出内容,
            "P2隔离": "D｜P2" in 输出内容,
            "洛书九宫": "E｜洛书九宫状态" in 输出内容,
            "里程碑快照": "F｜里程碑快照" in 输出内容,
            "新窗口锚点": "G｜新窗口启动锚点" in 输出内容,
            "下一步唯一动作": "H｜下一步唯一动作" in 输出内容,
            "ROOT_CARD": "I｜ROOT_CARD" in 输出内容,
            "CONFIRM保留": CONFIRM_CODE in 输出内容,
            "SEAL保留": SEAL_CODE in 输出内容,
            "GPG保留": GPG_FINGERPRINT in 输出内容,
            "DNA存在": DNA_PREFIX in 输出内容,
            "UID9622主控声明": "UID9622主控声明" in 输出内容,
        }
        return self._计算通过率(验收项)

    def _计算通过率(self, 验收项: Dict[str, bool]) -> Dict[str, any]:
        通过数 = sum(1 for v in 验收项.values() if v)
        总数 = len(验收项)
        验收项["通过率"] = f"{通过数}/{总数}"
        if 通过数 == 总数:
            验收项["三色"] = "🟢"
        elif 通过数 >= 总数 * 0.8:
            验收项["三色"] = "🟡"
        else:
            验收项["三色"] = "🔴"
        return 验收项

    # ── 洛书九宫映射 ──

    def _更新九宫_from分层(self, 分层: 内容分层结果, 上下文: dict[str, Any]):
        """根据内容分层结果填充九宫"""
        # 1宫：已执行结果 / P1 内容摘要
        p1_summary = self._摘要列表(分层.P1)
        if p1_summary:
            self.九宫.一宫_已执行结果 = p1_summary[:40]

        # 2宫：回流留痕 / P0 摘要
        p0_summary = self._摘要列表(分层.P0)
        if p0_summary:
            self.九宫.二宫_回流留痕 = p0_summary[:40]

        # 3宫：当前意图
        intent = 上下文.get("DNA总结", 上下文.get("定盘", "当前任务"))
        self.九宫.三宫_当前意图 = intent[:40]

        # 4宫：边界主权 / P0 永恒点
        if 分层.P0:
            self.九宫.四宫_边界主权 = "P0永恒保留"

        # 6宫：验收签章
        self.九宫.六宫_验收签章 = f"验证:{上下文.get('验证','待验证')}"

        # 7宫：决策路由
        self.九宫.七宫_决策路由 = 上下文.get("下一步", "继续")[:40]

        # 8宫：安全风险
        risk_notes = []
        if 上下文.get("一票否决项"):
            risk_notes.append("有否决项")
        if 上下文.get("Risk") == "🔴":
            risk_notes.append("🔴")
        self.九宫.八宫_安全风险 = ";".join(risk_notes) or "🟢"

        # 9宫：战略目标
        milestone = 上下文.get("里程碑", {})
        self.九宫.九宫_战略目标 = milestone.get("阶段名称", "自动收口")[:40]

    def _摘要列表(self, items: List[Dict[str, str]]) -> str:
        if not items:
            return ""
        texts = [item["内容"][:30] for item in items[:2]]
        return " | ".join(texts)

    # ── 三档收口模板渲染 v2.0 ──

    def 渲染C1(self, 归属: str = "P1", 结论: str = "", 下一步: str = "", 输入内容: str = "") -> str:
        """C1 轻收口模板渲染：带最小 DNA 追溯"""
        dna = DNA追溯(
            项目=self.项目,
            模块=self.模块,
            版本=PROTOCOL_VERSION,
            父DNA=self.DNA,
            内容哈希=hashlib.sha256((输入内容 or 结论).encode()).hexdigest()[:16],
            变更描述="C1轻收口"
        ).生成简短DNA()

        模板 = f"""【轻收口】
归属：{归属}
结论：{结论 or "已记录"}
下一步：{下一步 or "继续当前任务"}
DNA：{dna}
"""
        self._绿记录("C1渲染", f"归属={归属}", {"DNA": dna})
        return 模板.strip()

    def 渲染C2(self, 定盘: str = "", 补全内容: str = "", 可复制版本: str = "",
               文件清单: List[str] = None, 一票否决项: List[str] = None,
               验收清单: List[str] = None, 下一步动作: str = "",
               数字根: int = 5, 五行: str = "土", 输入内容: str = "") -> str:
        """C2 标准收口模板渲染：动态填充 + DNA"""
        文件清单 = 文件清单 or []
        一票否决项 = 一票否决项 or []
        验收清单 = 验收清单 or []

        文件清单文本 = "\n- ".join([""] + 文件清单) if 文件清单 else "\n- （无新增文件）"
        否决文本 = "\n- ".join([""] + 一票否决项) if 一票否决项 else "\n- 无"
        验收文本 = "\n- ".join([""] + 验收清单) if 验收清单 else "\n- （待填充）"

        dna = self._生成内容DNA(输入内容 or 定盘 or "C2标准收口", "C2标准收口")
        root_card = self._生成ROOT_CARD(数字根, 五行, dna)

        模板 = f"""【标准收口】

A｜当前定盘
{定盘 or "- 维持当前定盘"}

B｜补全内容
{补全内容 or "- 无新增"}

C｜可复制版本
```
{可复制版本 or "# 待填充可复制内容"}
```

D｜文件 / 页面 / 字段清单{文件清单文本}

E｜一票否决项{否决文本}

F｜验收清单{验收文本}

G｜下一步最短动作
{下一步动作 or "- 继续当前任务"}

H｜ROOT_CARD
{root_card}
"""
        self._绿记录("C2渲染", f"定盘已渲染·数字根={数字根}·五行={五行}", {"DNA": dna})
        return 模板.strip()

    def 渲染C3(self, DNA总结: str = "", P0内容: List[Dict[str, str]] = None,
               P1内容: List[Dict[str, str]] = None, P2内容: List[Dict[str, str]] = None,
               里程碑: dict[str, Any] = None, 下一步动作: str = "",
               数字根: int = 5, 五行: str = "土", 输入内容: str = "") -> str:
        """C3 阶段收口模板渲染：动态填充 + 完整 DNA 链"""
        P0内容 = P0内容 or []
        P1内容 = P1内容 or []
        P2内容 = P2内容 or []
        里程碑 = 里程碑 or {}

        P0文本 = self._渲染分层列表(P0内容)
        P1文本 = self._渲染分层列表(P1内容)
        P2文本 = self._渲染分层列表(P2内容)

        九宫状态 = self._渲染九宫状态()

        里程碑版本 = 里程碑.get("版本", PROTOCOL_VERSION)
        里程碑日期 = 里程碑.get("日期", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        里程碑阶段 = 里程碑.get("阶段名称", "当前阶段")
        里程碑完成 = 里程碑.get("已完成", "")
        里程碑待办 = "\n- ".join([""] + 里程碑.get("待办", [])) if 里程碑.get("待办") else "\n- （无）"

        dna = self._生成内容DNA(输入内容 or DNA总结 or "C3阶段收口", "C3阶段收口")
        root_card = self._生成ROOT_CARD(数字根, 五行, dna)

        新窗口锚点 = f"""【UID9622 新窗口启动锚点】

UID9622主控声明：
本窗口以 UID9622 为主控者，AI 只作为执行工具、结构化助手和技术整理器，不得反客为主。

CONFIRM：
{CONFIRM_CODE}

SEAL：
{SEAL_CODE}

GPG：
{GPG_FINGERPRINT}

当前DNA总结：
{DNA总结 or "【粘贴本次DNA总结】"}

当前任务：
{下一步动作 or "【填写下一阶段任务】"}"""

        模板 = f"""【阶段收口】

A｜DNA 总结
DNA：{dna}
父DNA：{self.DNA}
当前阶段：{里程碑阶段}
当前定盘：{DNA总结 or "维持当前定盘"}
下一阶段：{下一步动作 or "待确定"}

B｜P0 永恒不动点{P0文本}

C｜P1 当前阶段核心{P1文本}

D｜P2 可丢弃内容{P2文本}

E｜洛书九宫状态
{九宫状态}

F｜里程碑快照
版本：{里程碑版本}
日期：{里程碑日期}
阶段名称：{里程碑阶段}
已完成：{里程碑完成}
待办 Top 3：{里程碑待办}

G｜新窗口启动锚点
{新窗口锚点}

H｜下一步唯一动作
{下一步动作 or "- 待确定"}

I｜ROOT_CARD
{root_card}
"""
        self._绿记录("C3渲染", f"阶段收口已渲染·阶段={里程碑阶段}", {"DNA": dna})
        return 模板.strip()

    def _渲染分层列表(self, items: List[Dict[str, str]]) -> str:
        if not items:
            return "\n- （待填充）"
        lines = [""]
        for item in items:
            来源 = item.get("来源", "")
            内容 = item.get("内容", "").strip()
            if 来源 and 来源 != "(全文)":
                lines.append(f"【{来源}】{内容[:120]}")
            else:
                lines.append(内容[:120])
        return "\n- ".join(lines)

    # ── 辅助方法 ──

    def _生成ROOT_CARD(self, 数字根: int = 5, 五行: str = "土", dna: str = "") -> str:
        """生成 ROOT_CARD"""
        dna = dna or self.获取DNA()
        return f"""Root: {数字根}
Wuxing: {五行}
TriColor: 🟢
DataLevel: {数据级别.内部.value}
PrivacyMode: {隐私模式.标准.value}
Retention: full
TraceMode: chain
Route: AUTO-CLOSURE-PROTOCOL
Action: {dna}
DNA: "{dna}"
父DNA: "{self.DNA}"
CONFIRM: "{CONFIRM_CODE}"
SEAL: "{SEAL_CODE}"
GPG: "{GPG_FINGERPRINT}" """

    def _渲染九宫状态(self) -> str:
        """渲染洛书九宫状态"""
        九宫 = self.九宫
        return f"""```
4({九宫.四宫_边界主权[:8]})  9({九宫.九宫_战略目标[:8]})  2({九宫.二宫_回流留痕[:8]})
3({九宫.三宫_当前意图[:8]})  5【{九宫.中宫5_主控意志[:8]}】 7({九宫.七宫_决策路由[:8]})
8({九宫.八宫_安全风险[:8]})  1({九宫.一宫_已执行结果[:8]})  6({九宫.六宫_验收签章[:8]})
```"""

    # ── 知识库提交 ──

    def 提交知识库(self, 标题: str, 内容: str, 元数据: dict[str, Any] = None) -> str:
        """将审核过的创作提交到 dragon_knowledge.db"""
        if not os.path.exists(DB_PATH):
            self._红记录("知识库", f"数据库不存在: {DB_PATH}")
            return ""

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            module_id = 元数据.get("module_id", "uid9622-auto-closure")
            entry_type = 元数据.get("entry_type", "reviewed_creation")
            category = 元数据.get("category", "自动收口")
            status = 元数据.get("status", "SUBMITTED")
            priority = 元数据.get("priority", "P1")
            dna_code = 元数据.get("dna", self._生成内容DNA(内容, "知识库提交"))
            source_path = 元数据.get("source_path", "")

            # Ensure module exists
            cur.execute("SELECT module_id FROM knowledge_modules WHERE module_id=?", (module_id,))
            if not cur.fetchone():
                cur.execute("""
                INSERT INTO knowledge_modules (module_id, source, name, version, description, dna_code, triggers, license, author, extracted_at, entry_count, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    module_id,
                    "UID9622",
                    "UID9622自动收口提交",
                    ENGINE_VERSION,
                    "龍芯北辰自动收口协议提交的审核创作",
                    dna_code,
                    "收口,提交,审核",
                    "CC BY-NC-SA 4.0",
                    "UID9622",
                    datetime.now(timezone.utc).isoformat(),
                    0,
                    json.dumps({"engine": "自动收口协议", "version": ENGINE_VERSION}, ensure_ascii=False)
                ))

            entry_id = 元数据.get("entry_id") or f"{module_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{hashlib.sha256(标题.encode()).hexdigest()[:12]}"
            now = datetime.now(timezone.utc).isoformat()

            content_json = json.dumps({
                "metadata": 元数据,
                "dna": dna_code,
                "content_hash": hashlib.sha256(内容.encode()).hexdigest(),
                "status": status,
                "source_path": source_path
            }, ensure_ascii=False)

            cur.execute("DELETE FROM knowledge_entries WHERE entry_id=?", (entry_id,))
            cur.execute("""
            INSERT INTO knowledge_entries (entry_id, module_id, entry_type, title, category, status, priority, summary, content_json, dna_code, source_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                module_id,
                entry_type,
                标题,
                category,
                status,
                priority,
                内容[:500].replace('\n', ' '),
                content_json,
                dna_code,
                source_path,
                now
            ))

            # Update entry count
            cur.execute("SELECT COUNT(*) FROM knowledge_entries WHERE module_id=?", (module_id,))
            count = cur.fetchone()[0]
            cur.execute("UPDATE knowledge_modules SET entry_count=? WHERE module_id=?", (count, module_id))

            conn.commit()
            conn.close()
            self._绿记录("知识库", f"已提交: {entry_id}", {"module": module_id})
            return entry_id
        except Exception as e:
            self._红记录("知识库", f"提交失败: {str(e)}")
            return ""

    # ── 向量库联动 ──

    def 检查向量库(self) -> Dict[str, Any]:
        """检查公式对准表向量库状态"""
        状态 = {"存在": os.path.exists(VECTOR_PATH), "路径": VECTOR_PATH}
        if 状态["存在"]:
            try:
                with open(VECTOR_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                状态["模块"] = data.get("module_id")
                状态["版本"] = data.get("version")
                状态["分块数"] = len(data.get("sections", []))
                状态["维度"] = data.get("vectorizer", {}).get("vocab_size")
            except Exception as e:
                状态["错误"] = str(e)
        return 状态

    # ── 综合收口接口 v2.0 ──

    def 执行收口(self, 用户输入: str, 上下文数据: dict[str, Any] = None) -> 收口结果:
        """
        主入口：自动检测档位并执行对应收口
        """
        上下文数据 = 上下文数据 or {}

        # 1. 检测档位
        档位 = self.检测收口档位(用户输入)
        self._绿记录("执行收口", f"检测到档位: {档位.value}")

        # 2. 内容分层
        输入内容 = 上下文数据.get("输入内容", 用户输入)
        分层 = self.内容分层(输入内容)
        self._更新九宫_from分层(分层, 上下文数据)

        # 3. 根据档位渲染
        if 档位 == 收口档位.C1轻收口:
            归属 = 上下文数据.get("归属", "P0" if 分层.P0 else "P1" if 分层.P1 else "P2")
            结论 = 上下文数据.get("结论", "已记录")
            下一步 = 上下文数据.get("下一步", "继续当前任务")
            输出 = self.渲染C1(归属, 结论, 下一步, 输入内容)

        elif 档位 == 收口档位.C2标准收口:
            定盘 = 上下文数据.get("定盘", "维持当前定盘")
            补全 = 上下文数据.get("补全内容", "")
            可复制 = 上下文数据.get("可复制版本", "")
            文件清单 = 上下文数据.get("文件清单", [])
            否决项 = 上下文数据.get("一票否决项", [])
            验收 = 上下文数据.get("验收清单", [])
            下一步 = 上下文数据.get("下一步", "继续当前任务")
            dr = 上下文数据.get("数字根", 5)
            wx = 上下文数据.get("五行", "土")
            输出 = self.渲染C2(定盘, 补全, 可复制, 文件清单, 否决项, 验收, 下一步, dr, wx, 输入内容)

        elif 档位 == 收口档位.C3阶段收口:
            DNA总结 = 上下文数据.get("DNA总结", "")
            里程碑 = 上下文数据.get("里程碑", {})
            下一步 = 上下文数据.get("下一步", "待确定")
            dr = 上下文数据.get("数字根", 5)
            wx = 上下文数据.get("五行", "土")
            输出 = self.渲染C3(DNA总结, 分层.P0, 分层.P1, 分层.P2, 里程碑, 下一步, dr, wx, 输入内容)

        else:
            输出 = self.渲染C1("P1", "未触发收口", "继续", 输入内容)

        # 4. 一票否决检查
        否决项 = self.一票否决检查(档位, 输出, 用户输入)

        # 5. 验收验证
        验收结果 = self.验收验证(档位, 输出)

        # 6. 组装结果
        结果 = 收口结果(
            档位=档位,
            内容=输出,
            层级映射={
                "P0": [item["内容"] for item in 分层.P0],
                "P1": [item["内容"] for item in 分层.P1],
                "P2": [item["内容"] for item in 分层.P2]
            },
            审计日志=self.审计器[-15:],
            DNA=self.获取DNA(),
            父DNA=self.父DNA,
            验证通过=len(否决项) == 0 and 验收结果.get("三色") != "🔴",
            一票否决项=否决项,
            验收结果=验收结果
        )

        self._绿记录("收口完成", f"档位={档位.value}·验证={'通过' if 结果.验证通过 else '未通过'}", 验收结果)
        return 结果

    # ── 文件级收口提交 ──

    def 提交文件(self, 文件路径: str, 元数据: dict[str, Any] = None) -> 收口结果:
        """提交单个审核过的文件：读取 → 分层 → C3收口 → 入库"""
        元数据 = 元数据 or {}
        if not os.path.exists(文件路径):
            return 收口结果(
                档位=收口档位.未触发,
                内容=f"文件不存在: {文件路径}",
                验证通过=False,
                一票否决项=["文件不存在"]
            )

        with open(文件路径, 'r', encoding='utf-8') as f:
            内容 = f.read()

        标题 = 元数据.get("标题", os.path.basename(文件路径))
        上下文 = {
            "输入内容": 内容,
            "DNA总结": 元数据.get("DNA总结", f"{标题}·已审核·自动提交"),
            "里程碑": 元数据.get("里程碑", {
                "版本": 元数据.get("版本", ENGINE_VERSION),
                "阶段名称": 元数据.get("阶段名称", "文件提交"),
                "已完成": 元数据.get("已完成", 标题),
                "待办": 元数据.get("待办", [])
            }),
            "下一步": 元数据.get("下一步", "入库完成·向量库增量更新"),
            "数字根": 元数据.get("数字根", 5),
            "五行": 元数据.get("五行", "土"),
            "文件清单": [文件路径]
        }

        # 强制 C3
        结果 = self.执行收口("阶段收口，DNA总结，自动提交审核过的创作", 上下文)

        # 入库
        if 结果.验证通过:
            entry_id = self.提交知识库(
                标题=标题,
                内容=内容,
                元数据={
                    "module_id": 元数据.get("module_id", "uid9622-auto-closure"),
                    "entry_type": "reviewed_creation",
                    "category": 元数据.get("category", "自动收口提交"),
                    "status": "SUBMITTED",
                    "priority": 元数据.get("priority", "P1"),
                    "dna": 结果.DNA,
                    "source_path": 文件路径
                }
            )
            结果.知识库条目ID = entry_id

        # 保存收口报告
        输出目录 = os.path.dirname(文件路径) or "."
        输出路径 = os.path.join(输出目录, f"收口报告_{os.path.basename(文件路径)}")
        with open(输出路径, 'w', encoding='utf-8') as f:
            f.write(结果.内容)
        结果.输出文件 = 输出路径

        return 结果

    # ── 状态机 ──

    def 状态机判断(self, 用户输入: str, 内容类型: str = "") -> 收口档位:
        """
        自动收口状态机
        输入 → 识别触发词 → 判断内容类型 → 选择档位
        """
        输入小写 = 用户输入.lower().strip()

        # 特殊内容类型判断
        if 内容类型 in ["普通聊天", "闲聊", "确认", "短问题"]:
            self._绿记录("状态机", "内容类型=普通聊天 → C1")
            return 收口档位.C1轻收口

        if 内容类型 in ["技术文档", "工程包", "规则", "页面", "代码"]:
            self._绿记录("状态机", "内容类型=正式内容 → C2")
            return 收口档位.C2标准收口

        if 内容类型 in ["阶段完成", "新窗口", "归档", "闭环", "提交", "审核过"]:
            self._绿记录("状态机", "内容类型=阶段结束 → C3")
            return 收口档位.C3阶段收口

        # 触发词判断
        for 词 in C3触发词:
            if 词.lower() in 输入小写:
                return 收口档位.C3阶段收口
        for 词 in C2触发词:
            if 词.lower() in 输入小写:
                return 收口档位.C2标准收口
        for 词 in C1触发词:
            if 词 in 用户输入:
                return 收口档位.C1轻收口

        # 默认
        return 收口档位.C1轻收口

    # ── 统计与报告 ──

    def 生成统计报告(self) -> dict[str, Any]:
        """生成收口引擎统计报告"""
        三色分布 = {"🟢": 0, "🟡": 0, "🔴": 0}
        for 条目 in self.审计器:
            三色分布[条目.级别.value] += 1

        return {
            "总审计数": len(self.审计器),
            "三色分布": 三色分布,
            "健康度": f"{三色分布['🟢'] / max(len(self.审计器), 1) * 100:.1f}%",
            "上下文轮数": self.上下文轮数,
            "DNA": self.获取DNA(),
            "父DNA": self.父DNA,
            "引擎版本": ENGINE_VERSION
        }

    def 导出审计日志(self, 文件路径: str | None = None) -> str:
        """导出审计日志为JSON"""
        if 文件路径 is None:
            目录 = os.path.expanduser("~/_work")
            os.makedirs(目录, exist_ok=True)
            文件路径 = os.path.join(目录, f"自动收口审计日志_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json")

        数据 = [条目.to_dict() for 条目 in self.审计器]
        with open(文件路径, "w", encoding="utf-8") as f:
            json.dump({
                "DNA": self.获取DNA(),
                "父DNA": self.父DNA,
                "引擎版本": ENGINE_VERSION,
                "生成时间": datetime.now(timezone.utc).isoformat(),
                "审计条目": 数据
            }, f, ensure_ascii=False, indent=2)

        self._绿记录("导出", f"审计日志已导出: {文件路径}")
        return 文件路径


# ═══════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════

def 打印帮助():
    help_text = """
UID9622｜龍芯北辰自动收口协议 — 命令行接口 v2.0

用法:
  python3 自动收口协议.py [选项] [参数]

选项:
  --help, -h          显示此帮助信息
  --提交 <文件路径>   提交审核过的创作文件（C3收口+知识库入库）
                      [--标题 <标题>] [--模块 <module_id>] [--版本 <版本>]
  --demo-c1           C1 轻收口演示
  --demo-c2           C2 标准收口演示
  --demo-c3           C3 阶段收口演示
  --demo-all          全部档位演示
  --检查 <文本>       检测指定文本的收口档位
  --交互              进入交互模式
  --验收              运行验收验证
  --统计              显示统计报告
  --导出              导出审计日志
  --向量库状态        检查公式对准表向量库状态

示例:
  python3 自动收口协议.py --demo-all
  python3 自动收口协议.py --检查 "帮我补齐技术文档"
  python3 自动收口协议.py --提交 ./补丁.md --标题 "公式对准表v1.6补丁" --模块 uid9622-formula-alignment-v1.6
"""
    print(help_text)


def 演示C1():
    引擎 = 自动收口引擎()
    print("=" * 60)
    print("【C1 轻收口演示】")
    print("=" * 60)

    测试输入 = [
        "懂了，先这样",
        "这个归哪？",
        "明白了，继续",
        "你说呢？"
    ]

    for 输入 in 测试输入:
        档位 = 引擎.检测收口档位(输入)
        结果 = 引擎.执行收口(输入, {"结论": "已理解", "下一步": "继续"})
        print(f"\n输入: {输入}")
        print(f"档位: {档位.value}")
        print(f"验证: {'通过' if 结果.验证通过 else '未通过'} {结果.验收结果.get('三色', '')} {结果.验收结果.get('通过率', '')}")
        print(结果.内容)
        print("-" * 40)


def 演示C2():
    引擎 = 自动收口引擎()
    print("\n" + "=" * 60)
    print("【C2 标准收口演示】")
    print("=" * 60)

    输入 = "帮我补齐技术文档，默认全补，输出可复制版本"
    上下文 = {
        "定盘": "技术文档补全·公式对准表v1.6",
        "补全内容": "补全§Y§X§W§H2§Z共5个区段",
        "可复制版本": "# 补全后的文档内容\n...",
        "文件清单": ["UID9622_公式对准表_v1.6.md", "补全补丁.md"],
        "一票否决项": ["不混用α三义", "P0不被改写"],
        "验收清单": ["触发阈值完整", "模块接口定义", "裁决引擎伪代码"],
        "下一步": "放入Notion母页·给Cursor工程包",
        "数字根": 6,
        "五行": "金"
    }

    结果 = 引擎.执行收口(输入, 上下文)
    print(f"\n输入: {输入}")
    print(f"档位: {结果.档位.value}")
    print(f"验证: {'通过' if 结果.验证通过 else '未通过'} {结果.验收结果.get('三色', '')} {结果.验收结果.get('通过率', '')}")
    print(结果.内容)


def 演示C3():
    引擎 = 自动收口引擎()
    print("\n" + "=" * 60)
    print("【C3 阶段收口演示】")
    print("=" * 60)

    输入 = "阶段收口，DNA总结，准备给Cursor新窗口续航"
    sample_text = """# 公式对准表v1.6补全完成
UID9622 主控声明：AI 是工具。CONFIRM 码不变。SEAL 签章不变。GPG 指纹不变。
完成了 §Y 计算触发协议、§X 模块映射表、§W 冲突优先级等区段补全。
闲聊部分可以丢弃。假设性的尝试已经验证。"""

    上下文 = {
        "输入内容": sample_text,
        "DNA总结": "公式对准表v1.6补全完成·30缺口闭合·42表补充",
        "里程碑": {
            "版本": "v1.6",
            "阶段名称": "公式对准表补全",
            "已完成": "§Y§X§W§H2§Z§DDJ§Q§FAM§SVC§P§U全部补全",
            "待办": ["写入Notion", "给Cursor工程包", "启动v1.7规划"]
        },
        "下一步": "写入Notion母页 + 给Cursor + 启动v1.7",
        "数字根": 5,
        "五行": "土"
    }

    结果 = 引擎.执行收口(输入, 上下文)
    print(f"\n输入: {输入}")
    print(f"档位: {结果.档位.value}")
    print(f"验证: {'通过' if 结果.验证通过 else '未通过'} {结果.验收结果.get('三色', '')} {结果.验收结果.get('通过率', '')}")
    print(结果.内容)


def 演示全部():
    演示C1()
    演示C2()
    演示C3()

    print("\n" + "=" * 60)
    print("【统计报告】")
    print("=" * 60)
    引擎 = 自动收口引擎()
    统计 = 引擎.生成统计报告()
    for k, v in 统计.items():
        print(f"  {k}: {v}")


def 检查文本(文本: str):
    引擎 = 自动收口引擎()
    档位 = 引擎.检测收口档位(文本)
    print(f"输入: {文本}")
    print(f"检测档位: {档位.value}")

    if 档位 == 收口档位.C1轻收口:
        print("→ 执行 C1 轻收口（归属/结论/下一步/最小DNA）")
    elif 档位 == 收口档位.C2标准收口:
        print("→ 执行 C2 标准收口（定盘/补全/清单/验收/ROOT_CARD）")
    elif 档位 == 收口档位.C3阶段收口:
        print("→ 执行 C3 阶段收口（DNA总结/P0P1P2/九宫/里程碑/新窗口锚点）")


def 交互模式():
    引擎 = 自动收口引擎()
    print("=" * 60)
    print("UID9622｜自动收口协议 — 交互模式")
    print("输入 'quit' 或 '退出' 结束")
    print("=" * 60)

    while True:
        try:
            用户输入 = input("\n[UID9622] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            break

        if 用户输入.lower() in ["quit", "exit", "退出", "q"]:
            print("再见。")
            break

        if not 用户输入:
            continue

        档位 = 引擎.检测收口档位(用户输入)
        print(f"[检测] 档位: {档位.value}")

        # 模拟上下文
        上下文 = {
            "结论": "已处理",
            "下一步": "继续",
            "定盘": "当前任务",
            "数字根": 5,
            "五行": "土"
        }

        结果 = 引擎.执行收口(用户输入, 上下文)
        print(结果.内容)

        if 结果.一票否决项:
            print(f"\n[⚠️ 一票否决] {结果.一票否决项}")


def 运行验收():
    引擎 = 自动收口引擎()
    print("=" * 60)
    print("【验收验证 v2.0】")
    print("=" * 60)

    # C1 验收
    c1输出 = 引擎.渲染C1("P1", "已记录", "继续", "懂了，先这样")
    c1验收 = 引擎.验收验证(收口档位.C1轻收口, c1输出)
    print(f"\nC1 验收: {c1验收.get('三色', '?')} 通过率: {c1验收.get('通过率', '?')}")
    print(f"  未通过项: {[k for k, v in c1验收.items() if v is False]}")

    # C2 验收
    c2输出 = 引擎.渲染C2("测试定盘", "测试补全", "测试代码", ["a.md"], [], ["x"], "下一步", 5, "土", "补齐文档")
    c2验收 = 引擎.验收验证(收口档位.C2标准收口, c2输出)
    print(f"C2 验收: {c2验收.get('三色', '?')} 通过率: {c2验收.get('通过率', '?')}")
    print(f"  未通过项: {[k for k, v in c2验收.items() if v is False]}")

    # C3 验收
    c3输出 = 引擎.渲染C3(
        "测试DNA总结",
        [{"来源": "铁律", "内容": "P0项"}],
        [{"来源": "正文", "内容": "P1项"}],
        [{"来源": "闲聊", "内容": "P2项"}],
        {"阶段名称": "测试阶段"},
        "下一步",
        5, "土", "阶段收口"
    )
    c3验收 = 引擎.验收验证(收口档位.C3阶段收口, c3输出)
    print(f"C3 验收: {c3验收.get('三色', '?')} 通过率: {c3验收.get('通过率', '?')}")
    print(f"  未通过项: {[k for k, v in c3验收.items() if v is False]}")

    print(f"\n引擎DNA: {引擎.获取DNA()}")
    print(f"父DNA: {引擎.父DNA}")
    print(f"审计条目数: {len(引擎.审计器)}")


def 显示统计():
    引擎 = 自动收口引擎()
    统计 = 引擎.生成统计报告()
    print("=" * 60)
    print("【自动收口引擎统计报告】")
    print("=" * 60)
    for k, v in 统计.items():
        print(f"  {k}: {v}")


def 提交文件命令行():
    """处理 --提交 命令行参数"""
    if len(sys.argv) < 3:
        print("错误: 请提供要提交的文件路径")
        print("示例: python3 自动收口协议.py --提交 ./补丁.md --标题 \"公式对准表v1.6补丁\"")
        return

    文件路径 = sys.argv[2]
    元数据 = {"source_path": 文件路径}

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--标题" and i + 1 < len(sys.argv):
            元数据["标题"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--模块" and i + 1 < len(sys.argv):
            元数据["module_id"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--版本" and i + 1 < len(sys.argv):
            元数据["版本"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--阶段" and i + 1 < len(sys.argv):
            元数据["阶段名称"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--下一步" and i + 1 < len(sys.argv):
            元数据["下一步"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    引擎 = 自动收口引擎()
    结果 = 引擎.提交文件(文件路径, 元数据)

    print("=" * 60)
    print("【文件提交结果】")
    print("=" * 60)
    print(f"档位: {结果.档位.value}")
    print(f"验证通过: {结果.验证通过}")
    print(f"验收: {结果.验收结果.get('三色', '')} {结果.验收结果.get('通过率', '')}")
    print(f"DNA: {结果.DNA}")
    print(f"父DNA: {结果.父DNA}")
    print(f"知识库条目: {结果.知识库条目ID}")
    print(f"收口报告: {结果.输出文件}")
    if 结果.一票否决项:
        print(f"一票否决项: {结果.一票否决项}")


def 向量库状态():
    引擎 = 自动收口引擎()
    状态 = 引擎.检查向量库()
    print("=" * 60)
    print("【公式对准表向量库状态】")
    print("=" * 60)
    for k, v in 状态.items():
        print(f"  {k}: {v}")


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        打印帮助()
        sys.exit(0)

    选项 = sys.argv[1]

    if 选项 in ("--help", "-h"):
        打印帮助()

    elif 选项 == "--demo-c1":
        演示C1()

    elif 选项 == "--demo-c2":
        演示C2()

    elif 选项 == "--demo-c3":
        演示C3()

    elif 选项 == "--demo-all":
        演示全部()

    elif 选项 in ("--检查", "--check"):
        if len(sys.argv) < 3:
            print("错误: 请提供要检查的文本")
            print("示例: python3 自动收口协议.py --检查 '帮我补齐技术文档'")
        else:
            检查文本(sys.argv[2])

    elif 选项 in ("--交互", "--interactive"):
        交互模式()

    elif 选项 in ("--验收", "--verify"):
        运行验收()

    elif 选项 in ("--统计", "--stats"):
        显示统计()

    elif 选项 in ("--导出", "--export"):
        引擎 = 自动收口引擎()
        路径 = 引擎.导出审计日志()
        print(f"审计日志已导出: {路径}")

    elif 选项 in ("--提交", "--submit"):
        提交文件命令行()

    elif 选项 == "--向量库状态":
        向量库状态()

    else:
        print(f"未知选项: {选项}")
        打印帮助()
        sys.exit(1)
