#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 学生适配器（L3·引导式）

特征：半懂不懂，要学过程。
回复方式：例子+对比+为什么，引导式，步骤清单，练习。
DNA: #龍魂⚡️2026-0716-适配器-学生
"""


class TierStudent:
    """学生层适配器 — 引导式 + 为什么 + 步骤清单。"""

    TIER_NAME = "学生"

    @staticmethod
    def adapt(content_student: str, content_common: str) -> str:
        base = content_student or content_common
        steps = (
            "\n\n【学习路径】\n"
            "  1. 先搞懂：这事是什么？\n"
            "  2. 再看例子：别人怎么处理的？\n"
            "  3. 动手试：你自己归类一次\n"
            "  4. 对比：系统和你分的一样不？"
        )
        return base + steps

    @staticmethod
    def ui_hint() -> str:
        return "引导式 + 步骤清单 + 练习模式 + 关联笔记"


if __name__ == "__main__":
    print(TierStudent.adapt("为什么房东不退押金？看案例对比", ""))
