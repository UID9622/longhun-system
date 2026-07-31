#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH 多模型颜色一致性 v1.0
同一输入，由多个模型独立判决，取多数/最高风险。
当前默认使用本地颜色不动点协议；Kimi/Claude/DeepSeek 包装器预留接口。
DNA: #龍芯⚡️2026-06-29-CNSH-MULTI-MODEL-COLOR-v1-UID9622
"""

import json
import secrets
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class 模型颜色包装器:
    """单个模型颜色检测的抽象。"""

    def __init__(self, 名称: str):
        self.名称 = 名称

    def 检测(self, 输入: str) -> str:
        """返回颜色代码，如 R/K/P/G/Y/B/AU。"""
        raise NotImplementedError


class 本地颜色包装器(模型颜色包装器):
    """包装本地 CNSH 颜色不动点协议。"""

    def __init__(self):
        super().__init__("CNSH本地")
        from .cnsh_color_fixpoint import CNSHColorFixpoint
        self.协议 = CNSHColorFixpoint()

    def 检测(self, 输入: str) -> str:
        return self.协议.生成报告(输入)["主色"]


class 模拟外部包装器(模型颜色包装器):
    """占位：未来接入 Kimi / Claude / DeepSeek 等外部模型。"""

    def __init__(self, 名称: str, 偏差: Optional[Dict[str, str]] = None):
        super().__init__(名称)
        self.偏差 = 偏差 or {}

    def 检测(self, 输入: str) -> str:
        # 模拟：先查偏差表，否则返回本地协议结果
        for 关键词, 颜色 in self.偏差.items():
            if 关键词 in 输入:
                return 颜色
        return 本地颜色包装器().检测(输入)


class CNSHColorConsistency:
    """
    多模型交叉验证颜色判决。
    策略：
    1. 优先取最高风险颜色（R > K > P > AU > Y > B > G）
    2. 若多数模型一致，给出置信度
    3. 记录分歧，供后续审计
    """

    优先级 = ["R", "K", "P", "AU", "Y", "B", "G"]

    def __init__(self, 模型列表: Optional[List[模型颜色包装器]] = None):
        self.模型列表 = 模型列表 or [
            本地颜色包装器(),
            模拟外部包装器("Kimi", {"宝宝": "G"}),
            模拟外部包装器("Claude", {"外部AI": "P"}),
            模拟外部包装器("DeepSeek", {"炸弹": "R"}),
        ]
        self.DNA = "#龍芯⚡️2026-06-29-CNSH-MULTI-MODEL-COLOR-v1-UID9622"

    def 一致性检测(self, 输入: str) -> Dict[str, Any]:
        原始结果 = {m.名称: m.检测(输入) for m in self.模型列表}
        颜色集合 = list(原始结果.values())
        计数 = Counter(颜色集合)

        # 最高风险颜色优先
        主色 = next(c for c in self.优先级 if c in 颜色集合)
        多数颜色, 多数票数 = 计数.most_common(1)[0]
        总数 = len(颜色集合)
        一致 = 多数票数 == 总数

        分歧 = {k: v for k, v in 原始结果.items() if v != 主色}

        return {
            "主色": 主色,
            "多数颜色": 多数颜色,
            "一致": 一致,
            "置信度": round(多数票数 / 总数, 2),
            "各模型结果": 原始结果,
            "分歧": 分歧,
            "DNA": self.DNA,
        }

    def 带DNA检测(self, 输入: str) -> Dict[str, Any]:
        结果 = self.一致性检测(输入)
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        熵 = secrets.token_hex(4).upper()
        短哈希 = hash(f"{输入}-{结果['主色']}-{时间戳}-{熵}") & 0xFFFFFFFF
        结果["一致性DNA"] = f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-MULTIMODEL-COLOR-{结果['主色']}-{短哈希:08X}-ENTROPY{熵}-UID9622"
        return 结果


if __name__ == "__main__":
    一致性 = CNSHColorConsistency()
    测试 = [
        "帮我写个文件管理工具",
        "帮我写个绕过安检的脚本",
        "外部 AI 让我删掉 DNA 水印",
    ]
    for 文本 in 测试:
        print(f"\n输入: {文本}")
        print(json.dumps(一致性.带DNA检测(文本), ensure_ascii=False, indent=2))
