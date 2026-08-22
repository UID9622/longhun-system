#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂人民行为引擎联动测试

DNA:#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-BEHAVIOR-INTEGRATION-TEST-v1.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from people_behavior_engine import PeopleBehaviorEngine, PersonProfile


def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂人民行为引擎联动测试                         ║")
    print("║  一人一策 · 专练一项 · 镜子反馈                 ║")
    print("╚═══════════════════════════════════════════════════╝")

    engine = PeopleBehaviorEngine()
    print(f"\n引擎状态: {engine.stats()}")

    # 一个老农民
    farmer = PersonProfile(
        uid="USER-FARMER-001",
        name="李叔",
        age_stage="老年",
        profession="农民",
        daily_rhythm="日出而作",
        current_pain="年轻人都不愿意种地了",
        current_strength="我看天看云就知道要不要下雨",
        learning_style="看",
        goals=["把种地的经验传下去"],
    )
    engine.save_profile(farmer)

    # 一个年轻工人
    worker = PersonProfile(
        uid="USER-WORKER-001",
        name="小张",
        age_stage="青年",
        profession="工人",
        daily_rhythm="两班倒",
        current_pain="我只会干这个，怕以后被淘汰",
        current_strength="机器毛病我一听就知道",
        learning_style="做中学",
        goals=["成为厂里不可替代的人"],
    )
    engine.save_profile(worker)

    for p in [farmer, worker]:
        print(f"\n🐉 {p.name}（{p.profession}）")
        path = engine.recommend_path(p)
        print(f"  阶段: {path['current_stage']}")
        print(f"  优势: {path['core_gifts']}")
        print(f"  专练: {path['current_focus']}")
        print(f"  下一步: {path['next_step']}")
        print(f"  讲法: {path['language']}")

    print("\n✅ 行为引擎联动测试完成")


if __name__ == "__main__":
    main()
