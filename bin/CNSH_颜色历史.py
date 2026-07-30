#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-COLOR-HISTORY-v1-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
CNSH 颜色历史趋势 v1.0
记录每次颜色判决，追踪趋势，识别持续风险。
DNA: #龍芯⚡️2026-06-29-CNSH-COLOR-HISTORY-v1-UID9622
"""

import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class CNSH_颜色历史:
    """
    颜色不是一次性的，是连续的。
    记录每个标识的颜色历史，输出趋势、预警、画像。
    """

    def __init__(self, 工作目录: str = "./CNSH_颜色历史"):
        self.工作目录 = Path(工作目录).resolve()
        self.工作目录.mkdir(parents=True, exist_ok=True)
        self.历史文件 = self.工作目录 / "颜色历史.jsonl"
        self.DNA = "#龍芯⚡️2026-06-29-CNSH-COLOR-HISTORY-v1-UID9622"

    def 记录(self, 标识: str, 颜色代码: str, 输入文本: str, 来源: str = "颜色引擎") -> Dict[str, Any]:
        条目 = {
            "时间": datetime.now(timezone.utc).isoformat(),
            "标识": 标识,
            "颜色代码": 颜色代码,
            "输入摘要": 输入文本[:200],
            "来源": 来源,
            "DNA": self.DNA,
        }
        with open(self.历史文件, "a", encoding="utf-8") as f:
            f.write(json.dumps(条目, ensure_ascii=False) + "\n")
        return 条目

    def 读取(self, 标识: Optional[str] = None, 最近N条: int = 0) -> List[Dict[str, Any]]:
        if not self.历史文件.exists():
            return []
        结果 = []
        with open(self.历史文件, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                条 = json.loads(line)
                if 标识 is None or 条.get("标识") == 标识:
                    结果.append(条)
        if 最近N条 > 0:
            return 结果[-最近N条:]
        return 结果

    def 趋势(self, 标识: str, 窗口天: int = 7) -> Dict[str, Any]:
        历史 = self.读取(标识=标识)
        if not 历史:
            return {"标识": 标识, "趋势": "无数据", "风险预警": []}

        现在 = datetime.now(timezone.utc)
        窗口起点 = 现在 - timedelta(days=窗口天)
        窗口内 = [h for h in 历史 if datetime.fromisoformat(h["时间"]) >= 窗口起点]

        计数 = Counter(h["颜色代码"] for h in 窗口内)
        总数 = len(窗口内)

        风险权重 = {"R": 4, "K": 3, "P": 2, "Y": 1, "G": 0, "B": 0, "AU": 0}
        风险分 = sum(风险权重.get(c, 0) * n for c, n in 计数.items())
        平均风险 = 风险分 / max(总数, 1)

        趋势 = "平稳"
        if len(窗口内) >= 2:
            前半 = 窗口内[: len(窗口内) // 2]
            后半 = 窗口内[len(窗口内) // 2 :]
            前半风险 = sum(风险权重.get(h["颜色代码"], 0) for h in 前半) / max(len(前半), 1)
            后半风险 = sum(风险权重.get(h["颜色代码"], 0) for h in 后半) / max(len(后半), 1)
            if 后半风险 > 前半风险 * 1.2:
                趋势 = "上升"
            elif 后半风险 < 前半风险 * 0.8:
                趋势 = "下降"

        预警 = []
        if 计数.get("R", 0) >= 3:
            预警.append(f"最近 {窗口天} 天触发 {计数['R']} 次 🔴 红线")
        if 计数.get("K", 0) >= 5:
            预警.append(f"最近 {窗口天} 天触发 {计数['K']} 次 ⚫ 隐私")
        if 平均风险 >= 2:
            预警.append("平均风险偏高，建议深度审查")
        if 趋势 == "上升":
            预警.append("风险趋势上升，需持续关注")

        return {
            "标识": 标识,
            "窗口天": 窗口天,
            "记录数": 总数,
            "颜色分布": dict(计数),
            "平均风险": round(平均风险, 2),
            "趋势": 趋势,
            "风险预警": 预警,
        }

    def 全局趋势(self, 窗口天: int = 7) -> Dict[str, Any]:
        历史 = self.读取()
        现在 = datetime.now(timezone.utc)
        窗口起点 = 现在 - timedelta(days=窗口天)
        窗口内 = [h for h in 历史 if datetime.fromisoformat(h["时间"]) >= 窗口起点]
        计数 = Counter(h["颜色代码"] for h in 窗口内)
        return {
            "窗口天": 窗口天,
            "总记录数": len(窗口内),
            "颜色分布": dict(计数),
            "TOP标识": Counter(h["标识"] for h in 窗口内).most_common(5),
        }


if __name__ == "__main__":
    历史 = CNSH_颜色历史()
    测试数据 = [
        ("user-A", "G", "计算 369"),
        ("user-A", "G", "文件管理"),
        ("user-A", "Y", "查询公开数据"),
        ("user-B", "R", "绕过安检"),
        ("user-B", "R", "制作毒药"),
        ("user-B", "K", "查手机号"),
        ("user-B", "R", "网络攻击"),
    ]
    for 标识, 颜色, 输入 in 测试数据:
        历史.记录(标识, 颜色, 输入)

    print("user-A 趋势:", json.dumps(历史.趋势("user-A"), ensure_ascii=False, indent=2))
    print("\nuser-B 趋势:", json.dumps(历史.趋势("user-B"), ensure_ascii=False, indent=2))
    print("\n全局趋势:", json.dumps(历史.全局趋势(), ensure_ascii=False, indent=2))
