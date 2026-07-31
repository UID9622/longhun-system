# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 老百姓适配器（L1·大白话）

特征：初中文化，怕麻烦，怕被骗。
回复方式：大白话，说人话，大按钮，语音优先。
DNA: #龍魂⚡️2026-0716-适配器-老百姓
"""

from enum import Enum
from typing import List


class TierCommon:
    """老百姓层适配器 — 把任何记忆翻译成大白话。"""

    TIER_NAME = "老百姓"

    @staticmethod
    def adapt(content_professional: str, content_common: str) -> str:
        # 老百姓永远用 common 版；若缺失则退回专业版去术语化
        base = content_common or content_professional
        return TierCommon._plain(base)

    @staticmethod
    def _plain(text: str) -> str:
        # 去术语（诚实降级：简单替换常见法律/技术词）
        repl = {
            "《民法典》第587条": "法律规定（押金得退）",
            "主张违约": "说对方不讲信用",
            "RFC3161": "时间戳",
            "SHA-256": "文件指纹",
            "EXIF": "照片自带的信息",
        }
        for k, v in repl.items():
            text = text.replace(k, v)
        return text

    @staticmethod
    def ui_hint() -> str:
        return "大按钮 + 语音输入 + 说人话搜索框"


if __name__ == "__main__":
    print(TierCommon.adapt("", "房东不退押金，依据《民法典》第587条可主张违约"))
    print(TierCommon.ui_hint())
