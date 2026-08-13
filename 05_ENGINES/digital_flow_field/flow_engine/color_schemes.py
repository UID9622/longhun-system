# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂系统 · 工程实现层
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-COLOR-v2.0-UID9622
# 署名: UID9622（诸葛鑫·Lucky）

"""数字根颜色映射方案。

内置三套配色：
- nine: 九色高对比
- wuxing: 五行（水黑、火红、木绿、金白/金、土黄）
- grayscale: 灰度（数字根越大越亮）
"""

from __future__ import annotations

from typing import Dict


SCHEMES: Dict[str, Dict[int, str]] = {
    "nine": {
        1: "#e6194b",  # 红
        2: "#3cb44b",  # 绿
        3: "#ffe119",  # 黄
        4: "#4363d8",  # 蓝
        5: "#f58231",  # 橙
        6: "#911eb4",  # 紫
        7: "#46f0f0",  # 青
        8: "#f032e6",  # 洋红
        9: "#bcf60c",  # 荧光绿
    },
    "wuxing": {
        # 1、6 属水
        1: "#0a0a0a",  # 玄黑
        6: "#1a1a2e",  # 深水
        # 2、7 属火
        2: "#c41e3a",  # 火红
        7: "#ff4500",  # 炽红
        # 3、8 属木
        3: "#228b22",  # 木绿
        8: "#32cd32",  # 叶绿
        # 4、9 属金
        4: "#d4af37",  # 金
        9: "#f5f5dc",  # 白金
        # 5 属土
        5: "#d2b48c",  # 土黄
    },
    "grayscale": {
        1: "#222222",
        2: "#3b3b3b",
        3: "#555555",
        4: "#6e6e6e",
        5: "#888888",
        6: "#a1a1a1",
        7: "#bbbbbb",
        8: "#d4d4d4",
        9: "#eeeeee",
    },
}


SCHEME_NAMES: Dict[str, str] = {
    "nine": "九色",
    "wuxing": "五行",
    "grayscale": "灰度",
}


def get_color(root: int, scheme: str = "nine") -> str:
    """获取数字根对应颜色（无效根回退到中性灰）。"""
    if root < 1 or root > 9:
        return "#888888"
    return SCHEMES.get(scheme, SCHEMES["nine"]).get(root, "#888888")


def list_schemes() -> Dict[str, str]:
    """返回可用配色方案名称。"""
    return SCHEME_NAMES.copy()
