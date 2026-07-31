# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人民行为引擎 CLI

DNA:#龍芯⚡️2026-06-21-BEHAVIOR-CLI-v1.0

用法：
  python behavior_cli.py UID9622
  python behavior_cli.py --demo
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from people_behavior_engine import PeopleBehaviorEngine, PersonProfile


def demo():
    engine = PeopleBehaviorEngine()
    profile = PersonProfile(
        uid="USER-DEMO",
        name="阿秀",
        age_stage="青年",
        profession="厨师",
        daily_rhythm="早晚班",
        current_pain="我想做点什么，但不知道从何开始",
        current_strength="我对味道很敏感，朋友都说我做饭好吃",
        learning_style="做中学",
        goals=["开个自己的小店", "做出别人没吃过的味道"],
    )
    engine.save_profile(profile)
    show_path(engine, profile)


def show_path(engine, profile):
    print(f"\n🐉 {profile.name} 的专属赋能路径")
    print("=" * 50)
    path = engine.recommend_path(profile)
    print(f"\n当前阶段：{path['current_stage']}")
    print(f"核心优势：{path['core_gifts']}")
    print(f"当前专练：{path['current_focus']}")
    print(f"为什么：{path['why']}")
    print(f"\n下一步：{path['next_step']}")
    print(f"怎么跟你讲：{path['language']}")
    print(f"时间建议：{path['time_advice']}")
    print("\n镜子反馈示例：")
    print(engine.mirror(profile.current_pain, profile))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("🐉 人民行为引擎 CLI")
        print("  python behavior_cli.py --demo     # 看示例")
        print("  python behavior_cli.py <用户ID>   # 查看用户路径")
        return

    engine = PeopleBehaviorEngine()

    if sys.argv[1] == "--demo":
        demo()
        return

    uid = sys.argv[1]
    profile = engine.load_profile(uid)
    if not profile:
        print(f"⚠️  未找到 {uid} 的画像")
        print("  可以先创建：")
        print("  python behavior_cli.py --demo")
        return

    show_path(engine, profile)


if __name__ == "__main__":
    main()
