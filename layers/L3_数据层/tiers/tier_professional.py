# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂DNA记忆库 · 专业人士适配器（L2·专业术语）

特征：律师/医生/会计/工程师。
回复方式：专业术语，精准引用，可溯源，法条/标准。
DNA: #龍魂⚡️2026-0716-适配器-专业人士
"""


class TierProfessional:
    """专业人士层适配器 — 保留术语 + 引用依据。"""

    TIER_NAME = "专业人士"

    @staticmethod
    def adapt(content_professional: str, content_common: str,
              sources: list[Any] = None) -> str:
        base = content_professional or content_common
        if sources:
            cited = "\n".join(f"  · 来源: {s}" for s in sources[:5])
            base += f"\n\n【引用依据】\n{cited}"
        return base

    @staticmethod
    def ui_hint() -> str:
        return "详细检索 + 语义向量 + 法条/标准引用 + 审计日志"


if __name__ == "__main__":
    print(TierProfessional.adapt("依据《民法典》第587条，押金应退还", "",
                                 ["裁判文书网(2024)浙民终123"]))
