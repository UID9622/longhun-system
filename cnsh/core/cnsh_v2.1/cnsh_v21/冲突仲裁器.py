# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂·三协议冲突仲裁器
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-冲突仲裁-v1.0

三协议冲突仲裁：
- KFPP：检测知识权力化
- 黑箱审计：检测提示词生成的内容
- 反虚伪引擎：检测回复的文本风格
"""
from typing import Dict, Any, List, Tuple


class 冲突仲裁器:
    """三协议冲突仲裁器"""

    # 协议优先级（P0最高）
    PRIORITY = {
        "KFPP": 0,
        "黑箱审计": 1,
        "反虚伪": 2,
    }

    @classmethod
    def 裁决(cls, 结果: Dict[str, Any]) -> Dict[str, Any]:
        """裁决三协议冲突，返回统一结果。"""
        熔断列表: List[str] = []
        警告列表: List[str] = []
        状态列表: List[Tuple[str, str, int]] = []

        for 协议名, 协议结果 in 结果.items():
            if not isinstance(协议结果, dict):
                continue
            状态 = 协议结果.get("状态", "通过")
            优先级 = cls.PRIORITY.get(协议名, 99)
            状态列表.append((协议名, 状态, 优先级))

            if 状态 == "熔断":
                熔断列表.append(协议名)
            elif 状态 in ("警告", "自动简化"):
                警告列表.append(协议名)

        if 熔断列表:
            最高熔断 = sorted(熔断列表, key=lambda x: cls.PRIORITY.get(x, 99))[0]
            return {
                "状态": "熔断",
                "来源": 最高熔断,
                "原因": f"协议 {最高熔断} 触发熔断",
                "全部结果": 结果,
            }

        if 警告列表:
            最高警告 = sorted(警告列表, key=lambda x: cls.PRIORITY.get(x, 99))[0]
            return {
                "状态": "警告",
                "来源": 最高警告,
                "原因": f"协议 {最高警告} 触发警告",
                "全部结果": 结果,
            }

        return {
            "状态": "通过",
            "全部结果": 结果,
        }
