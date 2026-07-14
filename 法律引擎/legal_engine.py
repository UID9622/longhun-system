#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 本地法律引擎
DNA: #龍芯⚡️2026-06-29-LONGHUN-LEGAL-ENGINE-v1.0

本地可引用的法律解释引擎。输入大白话问题，返回相关法条 + 通俗解释。
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "cnsh-core"))
from cnsh_unified import DNA工具

ROOT = Path(__file__).parent
LAWS_PATH = ROOT / "laws.json"


def 加载法律库() -> dict:
    return json.loads(LAWS_PATH.read_text(encoding="utf-8"))


def 匹配法律(问题: str, 法律库: dict, top_k: int = 5) -> List[Dict]:
    问题小写 = 问题.lower()
    得分列表 = []
    for 分类名, 分类数据 in 法律库["categories"].items():
        关键词 = 分类数据.get("keywords", [])
        基础分 = sum(1 for kw in 关键词 if kw in 问题小写)
        for 法条 in 分类数据.get("laws", []):
            法条分 = 基础分
            for kw in 法条.get("scenarios", []):
                if kw in 问题小写:
                    法条分 += 2
            for kw in 关键词:
                if kw in 法条.get("official", "") + 法条.get("plain", ""):
                    法条分 += 1
            if 法条分 > 0:
                得分列表.append((法条分, 法条))

    得分列表.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in 得分列表[:top_k]]


def 解释问题(问题: str, 法律库: Optional[dict] = None, 语气: str = "大白话") -> Dict:
    法律库 = 法律库 or 加载法律库()
    法条列表 = 匹配法律(问题, 法律库)

    官方文本 = []
    通俗解释 = []
    for 法条 in 法条列表:
        官方文本.append(f"{法条['name']}：{法条['official']}")
        通俗解释.append(f"{法条['name']}：{法条['plain']}")

    # 自动生成一段综合回答
    回答 = _生成综合回答(问题, 法条列表, 语气)

    return {
        "问题": 问题,
        "匹配法条": 法条列表,
        "官方条文": 官方文本,
        "大白话解释": 通俗解释,
        "综合回答": 回答,
        "dna": DNA工具.生成("LEGAL-ENGINE-QUERY", "1.0"),
    }


def _生成综合回答(问题: str, 法条列表: List[Dict], 语气: str) -> str:
    if not 法条列表:
        return "这个问题暂时没找到对应的法条，你可以描述得更具体一些，比如涉及哪个场景、对方是谁、你受到了什么影响。"

    场景 = "、".join([l["name"] for l in 法条列表[:3]])
    if 语气 == "大白话":
        lines = [
            f"简单来说，你这件事可能跟这几条法律有关：{场景}。",
            "",
            "核心意思是：",
        ]
        for 法条 in 法条列表[:3]:
            lines.append(f"• {法条['plain']}")
        lines.extend([
            "",
            "你可以这么理解：对方如果违反了上面这些规定，你可以先协商，协商不成可以投诉或起诉。",
        ])
        return "\n".join(lines)
    elif 语气 == "硬气":
        lines = [f"这件事涉及：{场景}。对方的行为已经踩线。", ""]
        for 法条 in 法条列表[:3]:
            lines.append(f"• {法条['official']}")
        lines.extend(["", "建议：固定证据，直接投诉或走法律程序，不必客气。"])
        return "\n".join(lines)
    else:
        lines = [f"相关法律依据：{场景}", ""]
        for 法条 in 法条列表[:3]:
            lines.append(f"• {法条['official']}")
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        问题 = sys.argv[1]
    else:
        问题 = "公司拖欠工资怎么办"
    结果 = 解释问题(问题)
    print(f"\n问题：{结果['问题']}")
    print(f"DNA：{结果['dna']}\n")
    print("=" * 60)
    print(结果["综合回答"])
    print("=" * 60)
    print("\n相关法条：")
    for 法条 in 结果["匹配法条"]:
        print(f"\n{法条['name']}")
        print(f"  官方：{法条['official']}")
        print(f"  大白话：{法条['plain']}")
