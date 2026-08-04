#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂工具库 v1.0

系统级通用工具函数（时间、转换、验证等）

DNA:#龍芯⚡️2026-06-07-UTILS-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List


def calculate_dr(text: str) -> int:
    """
    计算数字根（Digital Root）
    意图: 五行分类的基础
    """
    # 计算所有中文字符的 Unicode 数值总和
    total = sum(ord(c) for c in text if '\u4e00' <= c <= '\u9fff')

    # 反复相加直到得到个位数
    while total >= 10:
        total = sum(int(digit) for digit in str(total))

    return total


def map_to_wuxing(dr: int) -> str:
    """
    将数字根映射到五行
    意图: 确定操作的五行属性
    """
    mapping = {
        1: "金",
        2: "木",
        3: "火",
        4: "火",
        5: "土",
        6: "金",
        7: "金",
        8: "水",
        9: "水",
        0: "土",
    }
    return mapping.get(dr, "未知")


def time_decay(layer: str, days_elapsed: int) -> float:
    """
    时间衰减计算
    意图: L0永恒不衰减，L4快速失效
    """
    alpha_map = {
        "L0": 0.0,      # 永恒
        "L1": 0.01,     # 百年级
        "L2": 0.1,      # 十年级
        "L3": 1.0,      # 日常
        "L4": float('inf'),  # 瞬时
    }

    alpha = alpha_map.get(layer, 1.0)

    if alpha == float('inf'):
        return 0.0  # 立即失效

    return (days_elapsed ** (-alpha))


def fingerprint(content: str, algo: str = "md5") -> str:
    """
    计算内容指纹
    意图: 篡改检测
    """
    if algo == "md5":
        return hashlib.md5(content.encode()).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(content.encode()).hexdigest()
    else:
        return hashlib.md5(content.encode()).hexdigest()


def safe_json_load(data: str, default: Any = None) -> Any:
    """
    安全 JSON 加载
    意图: 防止 JSON 解析错误
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return default


def safe_json_dump(obj: Any, ensure_ascii: bool = False) -> str:
    """
    安全 JSON 导出
    意图: 正确处理中文和特殊字符
    """
    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=2)
    except (TypeError, ValueError):
        return "{}"


def timestamp_now() -> str:
    """获取当前时间戳（ISO 8601）"""
    return datetime.now().isoformat()


def date_now() -> str:
    """获取当前日期（YYYY-MM-DD）"""
    return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    text = "龍魂系统"
    dr = calculate_dr(text)
    wuxing = map_to_wuxing(dr)
    print(f"文本: {text}")
    print(f"数字根: {dr}")
    print(f"五行: {wuxing}")

    decay = time_decay("L0", 365)
    print(f"L0 一年后衰减: {decay}")

    decay = time_decay("L4", 1)
    print(f"L4 一天后衰减: {decay}")
