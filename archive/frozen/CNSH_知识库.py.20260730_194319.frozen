#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-KB-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_知识库
路径：bin/CNSH_知识库.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 知识库 v1.0
统一收集 CNSH 加工产物：模块、DNA、核心概念、审计结果、使用方式。
原则：只追加、不覆盖、不删除。
DNA: #龍芯⚡️2026-06-29-CNSH-KB-UID9622
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from CNSH_国密工具 import SM3


class CNSH_知识库:
    def __init__(self, 路径: str = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "CNSH_知识库.json")):
        self.路径 = Path(路径)
        self._数据 = self._加载()

    def _加载(self) -> Dict[str, Any]:
        if not self.路径.exists():
            return {
                "库名": "CNSH 龍魂知识库",
                "DNA": "#龍芯⚡️2026-06-29-CNSH-KB-UID9622",
                "创建时间": datetime.now(timezone.utc).isoformat(),
                "条目": [],
            }
        with open(self.路径, "r", encoding="utf-8") as f:
            return json.load(f)

    def 追加(
        self,
        标题: str,
        文件路径: str,
        核心概念: List[str],
        DNA: str,
        三色摘要: Optional[Dict[str, int]] = None,
        输入SM3哈希: Optional[str] = None,
        备注: str = "",
    ) -> str:
        条目 = {
            "时间": datetime.now(timezone.utc).isoformat(),
            "标题": 标题,
            "文件路径": 文件路径,
            "核心概念": 核心概念,
            "DNA": DNA,
            "三色摘要": 三色摘要 or {"🟢": 0, "🟡": 0, "🔴": 0},
            "输入SM3哈希": 输入SM3哈希,
            "备注": 备注,
        }
        条目JSON = json.dumps(条目, sort_keys=True, ensure_ascii=False)
        条目["条目SM3哈希"] = SM3.hex_hash(条目JSON)
        self._数据["条目"].append(条目)
        self._保存()
        return 条目["条目SM3哈希"]

    def _保存(self):
        with open(self.路径, "w", encoding="utf-8") as f:
            json.dump(self._数据, f, ensure_ascii=False, indent=2)

    def 查询(self, 关键词: str) -> List[Dict[str, Any]]:
        结果 = []
        for 条目 in self._数据["条目"]:
            文本 = json.dumps(条目, ensure_ascii=False)
            if 关键词.lower() in 文本.lower():
                结果.append(条目)
        return 结果

    def 统计(self) -> Dict[str, Any]:
        条目 = self._数据["条目"]
        return {
            "总条目数": len(条目),
            "最近更新时间": 条目[-1]["时间"] if 条目 else None,
            "DNA": self._数据["DNA"],
        }


if __name__ == "__main__":
    kb = CNSH_知识库()
    哈希 = kb.追加(
        标题="排序不动点协议",
        文件路径="CNSH_排序不动点协议.py",
        核心概念=["人民第一", "护弱底线", "三次审计", "排序不动点"],
        DNA="#龍芯⚡️2026-04-19-ORDER-ANCHOR-v1.0",
        三色摘要={"🟢": 5, "🟡": 0, "🔴": 0},
        输入SM3哈希="demo_hash",
        备注="协议已翻译成 CNSH 国密 Python",
    )
    print(f"知识库已追加，条目哈希: {哈希}")
    print(json.dumps(kb.统计(), ensure_ascii=False, indent=2))
