#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 AI 输出熔断器 — 任何 AI 生成的代码/指令先过护盾再执行
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-AI-OUTPUT-GUARD-v1.0
原则：AI 输出不是圣旨，先验毒、再放行
"""

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from longhun_download_guard import 下载文件检测器, 下载隔离区
from longhun_shield_cnsh import 龍魂护盾


@dataclass
class 代码块:
    语言: str
    内容: str
    起始行: int


class AI输出熔断器:
    """对 AI 返回的文本做整体语义 + 代码块静态扫描。"""

    危险语言 = {
        "bash", "sh", "shell", "zsh",
        "python", "py", "python3",
        "javascript", "js", "nodejs",
        "powershell", "ps1", "cmd", "batch"
    }

    def __init__(self, 护盾: 龍魂护盾):
        self.护盾 = 护盾
        self.文件检测器 = 下载文件检测器(护盾)
        self.隔离区: Optional[下载隔离区] = None
        if not getattr(护盾, "_已熔断", False):
            self.隔离区 = 下载隔离区(
                Path(os.environ.get(
                    "LONGHUN_QUARANTINE_DIR",
                    str(Path.home() / ".longhun" / "quarantine")
                ))
            )

    def 提取代码块(self, 文本: str) -> List[代码块]:
        """提取 Markdown 代码块。"""
        代码块列表 = []
        模式 = re.compile(r"```\s*(\w+)?\s*\n(.*?)```", re.DOTALL)
        for 匹配 in 模式.finditer(文本):
            语言 = (匹配.group(1) or "text").lower()
            内容 = 匹配.group(2)
            代码块列表.append(代码块(语言, 内容, 匹配.start()))
        return 代码块列表

    def 扫描代码块(self, 块: 代码块, 来源: str) -> Dict[str, Any]:
        """把单个代码块写入临时文件，用下载守卫扫描。"""
        后缀 = ".txt"
        if 块.语言 in self.危险语言:
            后缀 = f".{块.语言}"
        elif 块.语言 == "python":
            后缀 = ".py"
        elif 块.语言 in ("bash", "sh", "shell", "zsh"):
            后缀 = ".sh"
        elif 块.语言 in ("javascript", "js", "nodejs"):
            后缀 = ".js"
        elif 块.语言 in ("powershell", "ps1"):
            后缀 = ".ps1"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=后缀, delete=False, encoding="utf-8"
        ) as 临时文件:
            临时文件.write(块.内容)
            临时路径 = Path(临时文件.name)

        try:
            结果 = self.文件检测器.检测(临时路径)
            if not 结果["通过"] and self.隔离区:
                隔离路径 = self.隔离区.隔离(
                    临时路径, f"AI_OUTPUT_{来源.upper()}"
                )
                结果["隔离路径"] = str(隔离路径)
            return 结果
        finally:
            if 临时路径.exists() and "隔离路径" not in 结果:
                临时路径.unlink()

    def 检查(self, 来源: str, 内容: str) -> Dict[str, Any]:
        if getattr(self.护盾, "_已熔断", False):
            return {"通过": False, "原因": "主权熔断已触发"}

        结果 = {
            "通过": True,
            "原因": "干净",
            "来源": 来源,
            "整体语义": "通过",
            "代码块": [],
            "风险项": []
        }

        # 1. 整体语义熔断
        语义结果 = self.护盾.检查人工智能(f"ai_output:{来源}", 内容[:4000])
        if not 语义结果.get("通过"):
            结果["通过"] = False
            结果["整体语义"] = "熔断"
            结果["风险项"].append(f"整体语义：{语义结果.get('原因')}")

        # 2. 代码块扫描
        代码块列表 = self.提取代码块(内容)
        for 索引, 块 in enumerate(代码块列表, 1):
            块结果 = self.扫描代码块(块, 来源)
            块结果["索引"] = 索引
            块结果["语言"] = 块.语言
            结果["代码块"].append(块结果)
            if not 块结果["通过"]:
                结果["通过"] = False
                结果["风险项"].append(
                    f"代码块-{索引}({块.语言})：{块结果.get('原因')}"
                )

        if not 结果["通过"]:
            self.护盾.感知.上报("ai_output", 来源, {
                "原因": "AI输出包含危险内容",
                "风险项": 结果["风险项"],
                "代码块数": len(代码块列表),
            })
            结果["原因"] = "；".join(结果["风险项"])
        return 结果


def 主函数():
    解析器 = argparse.ArgumentParser(description="龍魂 AI 输出熔断器")
    解析器.add_argument("--source", default="cli", help="AI 来源标识")
    解析器.add_argument("--text", type=str, help="直接传入文本")
    解析器.add_argument("--file", type=str, help="从文件读取 AI 输出")
    参数 = 解析器.parse_args()

    脱氧核糖核酸 = os.environ.get(
        "LONGHUN_SHIELD_DNA",
        "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-CNSH-UID9622"
    )
    护盾 = 龍魂护盾(脱氧核糖核酸)
    熔断器 = AI输出熔断器(护盾)

    if 参数.file:
        内容 = Path(参数.file).read_text(encoding="utf-8")
    elif 参数.text:
        内容 = 参数.text
    else:
        内容 = sys.stdin.read()

    结果 = 熔断器.检查(参数.source, 内容)
    print(json.dumps(结果, indent=2, ensure_ascii=False))
    return 0 if 结果["通过"] else 1


if __name__ == "__main__":
    sys.exit(主函数())
