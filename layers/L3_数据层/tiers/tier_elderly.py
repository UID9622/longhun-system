# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 老年人适配器（L4·超大字+语音）

特征：眼睛不好，打字慢。
回复方式：超大字，慢语速，重复，语音播报，大按钮。
DNA: #龍魂⚡️2026-0716-适配器-老年人
"""


class TierElderly:
    """老年人层适配器 — 超大字 + 语音播报 + 慢。"""

    TIER_NAME = "老年人"

    @staticmethod
    def adapt(content_elderly: str, content_common: str) -> str:
        base = content_elderly or content_common
        # 老年人版：短句、重复关键、加语音标记
        return f"🔊[语音播报] {base}\n\n（字已调大，慢慢看，不急）"

    @staticmethod
    def ui_hint() -> str:
        return "超大字体 + 语音输入 + 语音播报 + [字更大][慢点说]按钮"


if __name__ == "__main__":
    print(TierElderly.adapt("房东押金那事，我帮你记着呢", ""))
