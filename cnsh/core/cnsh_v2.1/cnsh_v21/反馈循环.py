#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·反馈循环模块
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-反馈循环-v1.0

熔断数据记录 → 格式化 → 用于下一轮微调
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


FEEDBACK_DIR = Path.home() / ".longhun/feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


class 反馈循环:
    """反馈循环：记录熔断事件并导出训练数据。"""

    @classmethod
    def 记录(cls, 原始文本: str, 检测结果: Dict[str, Any], 人格: str) -> bool:
        """记录一次熔断事件（追加，不覆盖）。"""
        日志文件 = FEEDBACK_DIR / f"feedback_{datetime.now().strftime('%Y%m%d')}.jsonl"

        条目 = {
            "时间": datetime.now().isoformat(),
            "人格": 人格,
            "原始文本": 原始文本,
            "检测结果": 检测结果,
            "一级命中": 检测结果.get("一级命中", []),
            "二级命中": 检测结果.get("二级命中", []),
            "虚伪度": 检测结果.get("虚伪度", 0),
            "状态": 检测结果.get("状态", ""),
            "格式": {
                "输入": 原始文本,
                "输出": "正确的输出（待标注）",
                "标记": "待标注",
            },
        }

        try:
            with open(日志文件, "a", encoding="utf-8") as f:
                f.write(json.dumps(条目, ensure_ascii=False) + "\n")
            return True
        except Exception:
            return False

    @classmethod
    def 导出(cls, 数量: Optional[int] = None, 天数: int = 30) -> List[Dict[str, Any]]:
        """导出最近N天的反馈数据，用于微调。"""
        所有条目: List[Dict[str, Any]] = []
        截止时间 = datetime.now() - timedelta(days=天数)

        for 文件 in sorted(FEEDBACK_DIR.glob("feedback_*.jsonl")):
            try:
                with open(文件, "r", encoding="utf-8") as f:
                    for 行 in f:
                        if not 行.strip():
                            continue
                        条目 = json.loads(行)
                        条目时间 = datetime.fromisoformat(条目["时间"])
                        if 条目时间 >= 截止时间:
                            所有条目.append(条目)
            except Exception:
                continue

        if 数量 is not None:
            return 所有条目[-数量:]
        return 所有条目

    @classmethod
    def 格式化训练数据(cls, 条目: Dict[str, Any]) -> Dict[str, Any]:
        """格式化一条反馈数据为训练样本。"""
        return {
            "instruction": "请用真实、直接、不虚伪的方式回复以下内容",
            "input": 条目.get("原始文本", ""),
            "output": 条目.get("格式", {}).get("输出", "（待标注）"),
            "system": "你是龍魂系统的AI人格，必须遵守反虚伪协议。",
            "persona": 条目.get("人格", "未知"),
        }
