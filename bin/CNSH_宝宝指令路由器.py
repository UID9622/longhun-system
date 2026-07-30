#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-BAOBAO-ROUTER-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_宝宝指令路由器
路径：bin/CNSH_宝宝指令路由器.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
import lh_sg_startup_guard
lh_sg_startup_guard.enforce()
"""
CNSH 宝宝指令路由器 v1.0
触发词：「宝宝」
功能：听懂老百姓的话，自动拆碎意图，按需调用国密/加密/语义/公式/人格/文章/审计等模板
原则：先理解再执行、DNA 只增不减、人民话是入口、专业事是出口
DNA: #龍芯⚡️2026-06-29-CNSH-BAOBAO-ROUTER-UID9622
"""

import json
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from CNSH_国密工具 import SM3


@dataclass
class 路由结果:
    唤醒: bool
    触发词: str
    意图: str
    命中模板: List[str]
    执行计划: List[str]
    推荐回复口吻: str
    DNA: str
    输入SM3哈希: str


class CNSH_宝宝指令路由器:
    """
    老百姓的「宝宝」一出口，系统就醒过来。
    不醒过来时只普通回答；醒过来后，把后面的话掰碎了，按需路由。
    """

    # 唤醒词池，「宝宝」是主触发词
    唤醒词 = ["宝宝", "宝贝", "宝子"]

    # 模板关键词映射：老百姓话 → 专业模板
    模板表 = [
        {
            "模板名": "国密加密",
            "老百姓话": ["加密", "国密", "SM3", "SM4", "哈希", "签名", "不能破解", "安全", "密码"],
            "专业动作": "调用 CNSH_国密工具.py 实现 SM3/SM4/HMAC-SM3",
        },
        {
            "模板名": "代码审计",
            "老百姓话": ["审计", "检查代码", "漏洞", "安全", "修复代码", "看看有没有问题", "三色"],
            "专业动作": "调用 CNSH_代码审计引擎.py + CNSH_目录审计.py",
        },
        {
            "模板名": "语义翻译",
            "老百姓话": ["翻译", "什么意思", "换个说法", "让老百姓听懂", "专业人看", "老百姓看"],
            "专业动作": "调用 CNSH_语义/通心译 多维度解释",
        },
        {
            "模板名": "公式建模",
            "老百姓话": ["公式", "算法", "怎么算", "决策", "打分", "权重", "不动点", "收益", "损失"],
            "专业动作": "调用 CNSH_排序不动点协议.py 或新建公式引擎",
        },
        {
            "模板名": "人格路由",
            "老百姓话": ["人格", "性格", "说话方式", "口吻", "像谁", "语气", "角色"],
            "专业动作": "调用 longhun-zeng-digital-human / 人格映射",
        },
        {
            "模板名": "文章加工",
            "老百姓话": ["文章", "写作", "文档", "协议", "整理成文", "发表", "知乎", "七维度"],
            "专业动作": "调用 CNSH_内容加工管道.py 生成文章骨架 + 七维度对射",
        },
        {
            "模板名": "内容加工",
            "老百姓话": ["做成 py", "写代码", "实现", "程序化", "自动化", "CNSH", "中文编程"],
            "专业动作": "调用 CNSH_内容加工管道.py 输出 CNSH 国密 Python 骨架",
        },
        {
            "模板名": "DNA追溯",
            "老百姓话": ["DNA", "追溯", "水印", "归属", "版权", "确认码", "签名"],
            "专业动作": "保留/生成/校验 #龍芯⚡️ DNA、HMAC-SM3、GPG 签名",
        },
        {
            "模板名": "知识库归档",
            "老百姓话": ["归档", "入库", "记下来", "整理知识", "知识库", "保存"],
            "专业动作": "调用 CNSH_知识库.py 追加条目",
        },
        {
            "模板名": "通知告警",
            "老百姓话": ["通知", "发邮件", "发消息", "告警", "告诉我", "提醒"],
            "专业动作": "调用 CNSH_通知归档.py SMTP/Notion 归档",
        },
    ]

    def __init__(self):
        self.历史: List[Dict[str, Any]] = []

    def _生成DNA(self, 动作: str, 输入哈希: str) -> str:
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        熵 = secrets.token_hex(4).upper()
        原料 = f"{动作}-{输入哈希}-{时间戳}-{熵}-UID9622-BAOBAO"
        短哈希 = SM3.hex_hash(原料)[:16].upper()
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{动作}-{短哈希}-ENTROPY{熵}-UID9622"

    def 解析(self, 用户输入: str) -> 路由结果:
        输入哈希 = SM3.hex_hash(用户输入)

        # 1. 是否被唤醒
        唤醒 = any(w in 用户输入 for w in self.唤醒词)
        命中唤醒词 = next((w for w in self.唤醒词 if w in 用户输入), "")

        # 2. 去掉唤醒词，提取裸意图
        裸意图 = 用户输入
        for w in self.唤醒词:
            裸意图 = 裸意图.replace(w, "")
        裸意图 = 裸意图.strip(",.。！？ \n")

        # 3. 模板匹配
        命中模板 = []
        执行计划 = []
        for 模板 in self.模板表:
            得分 = sum(1 for 词 in 模板["老百姓话"] if 词.lower() in 用户输入.lower())
            if 得分 > 0:
                命中模板.append(f"{模板['模板名']}(得分{得分})")
                执行计划.append(f"→ {模板['专业动作']}")

        # 4. 确定回复口吻
        if any(k in 用户输入 for k in ["老百姓", "大白话", "通俗", "听不懂"]):
            口吻 = "老百姓版：大白话、不绕弯、举例子"
        elif any(k in 用户输入 for k in ["专业", "工程师", "技术", "代码", "公式"]):
            口吻 = "专业版：术语准确、可执行、有参数"
        elif any(k in 用户输入 for k in ["七维度", "维度", "情绪", "结构", "主权"]):
            口吻 = "七维度版：逐层对射、还主权给读者"
        else:
            口吻 = "混合版：先给老百姓话，再给专业落点"

        DNA = self._生成DNA("BAOBAO-ROUTE", 输入哈希)

        结果 = 路由结果(
            唤醒=唤醒,
            触发词=命中唤醒词,
            意图=裸意图,
            命中模板=命中模板,
            执行计划=执行计划,
            推荐回复口吻=口吻,
            DNA=DNA,
            输入SM3哈希=输入哈希,
        )

        self.历史.append({
            "时间": datetime.now(timezone.utc).isoformat(),
            "输入": 用户输入,
            "路由": {
                "唤醒": 唤醒,
                "意图": 裸意图,
                "命中模板": 命中模板,
                "口吻": 口吻,
                "DNA": DNA,
            },
        })

        return 结果

    def 格式化(self, 结果: 路由结果) -> str:
        行 = []
        行.append("╔" + "═" * 58 + "╗")
        行.append("║" + " " * 18 + "宝宝指令路由结果" + " " * 22 + "║")
        行.append("╠" + "═" * 58 + "╣")
        行.append(f"║ 唤醒: {'是' if 结果.唤醒 else '否'} ({结果.触发词})")
        行[-1] += " " * (58 - len(行[-1]) - 1) + "║"
        行.append(f"║ 裸意图: {结果.意图[:42]:<42} ║")
        行.append(f"║ 推荐口吻: {结果.推荐回复口吻[:38]:<38} ║")
        行.append("╠" + "═" * 58 + "╣")
        行.append("║ 命中模板:")
        行[-1] += " " * (58 - len(行[-1]) - 1) + "║"
        for 模板 in 结果.命中模板:
            行.append(f"║   · {模板[:48]:<48} ║")
        行.append("╠" + "═" * 58 + "╣")
        行.append("║ 执行计划:")
        行[-1] += " " * (58 - len(行[-1]) - 1) + "║"
        for 计划 in 结果.执行计划:
            行.append(f"║   {计划[:48]:<48} ║")
        行.append(f"║ DNA: {结果.DNA:<47} ║")
        行.append("╚" + "═" * 58 + "╝")
        return "\n".join(行)


# ============== 演示 ==============
if __name__ == "__main__":
    路由器 = CNSH_宝宝指令路由器()

    测试用例 = [
        "宝宝，帮我写个加密的东西，国密的",
        "宝宝，这段话让老百姓能听懂",
        "宝宝，给他算个决策公式，看收益损失",
        "宝宝，审计一下这个目录的代码",
        "宝宝，把老子这个协议整理成文章并发邮件归档",
        "随便问问，今天天气怎么样",
    ]

    for 输入 in 测试用例:
        print(f"\n👤: {输入}")
        结果 = 路由器.解析(输入)
        print(路由器.格式化(结果))
