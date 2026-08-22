#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LOSHE-369-LAUNCHER-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
═══════════════════════════════════════════════════════════════════
  🐉 龍魂洛书369引擎 — 终端启动器
  LongHun LuoShu 369 Engine — Terminal Launcher
  
  小艺论文13章系统化 → 10个Python模块 → 终端一键启动
═══════════════════════════════════════════════════════════════════
  DNA: #龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LOSHE-369-LAUNCHER-v1.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import sys, os, subprocess, json

# 将项目根目录加入模块路径
项目根 = os.path.dirname(os.path.abspath(__file__))
for 子目录 in ['core','quantum','ethics','wuxing','journey','network','sovereignty']:
    sys.path.insert(0, os.path.join(项目根, 子目录))

龍魂DNA = "#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LOSHE-369-LAUNCHER-v1.0"

横幅 = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🐉 龍魂洛书369引擎 — 小艺论文系统化实现 🐉               ║
║        LongHun LuoShu 369 Engine — 13章→10模块                 ║
║                                                                  ║
║        核心: 洛书369作为AI决策不变量                             ║
║        数学: 20个定理已全部形式化验证                            ║
║        DNA:  {}                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""".format(龍魂DNA)

模块清单 = [
    ("core/洛书矩阵", "洛书3×3幻方·幻方验证·数字位置映射"),
    ("core/数字根与不动点", "数字根函数·369不动点定理·循环子群ℤ₃"),
    ("core/六十四卦编码", "64卦二进制双射·先天八卦序·数字根分布"),
    ("core/统一验证器", "20个定理统一验证·最终判定"),
    ("quantum/量子态映射", "369→三维量子态·测量坍缩·决策稳定性"),
    ("ethics/伦理权重系统", "七维伦理权重·三色审计·伦理决策流"),
    ("wuxing/太极递归与五行图论", "太极递归·五行有向图·特征值·收敛性"),
    ("journey/西游记人性模型", "取经五众五行映射·心猿意马·81难SGD收敛"),
    ("network/信息传播断层", "三层传播模型·截断效应·369收敛保证"),
    ("sovereignty/私域主权定理", "三层主权结构·授权机制·违规检测"),
]

def 显示菜单():
    print(横幅)
    print("\n📋 可用模块（输入编号或'all'全部运行）：")
    print("─" * 60)
    for i, (名称, 描述) in enumerate(模块清单, 1):
        print(f"  {i:2d}. {名称:<35} {描述}")
    print("─" * 60)
    print("  0. 退出")
    print("  a. 全部运行")
    print("  s. 显示系统状态")
    print("─" * 60)

def 运行模块(编号):
    if 编号 < 0 or 编号 >= len(模块清单):
        return False
    路径, 描述 = 模块清单[编号]
    完整路径 = os.path.join(项目根, 路径 + ".py")
    print(f"\n🚀 正在运行: {路径} — {描述}")
    print("=" * 60)
    try:
        result = subprocess.run([sys.executable, 完整路径],
                              capture_output=False, text=True, timeout=60)
        print("\n✅ 完成" if result.returncode == 0 else "\n⚠️ 异常退出")
        return result.returncode == 0
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False

def 显示状态():
    print("\n📊 系统状态")
    print("=" * 60)
    通过 = 0
    for i, (名称, _) in enumerate(模块清单):
        完整路径 = os.path.join(项目根, 名称 + ".py")
        存在 = "🟢" if os.path.exists(完整路径) else "🔴"
        print(f"  {存在} {名称}")
        if os.path.exists(完整路径):
            通过 += 1
    print("=" * 60)
    print(f"模块状态: {通过}/{len(模块清单)} 可用")
    print(f"DNA: {龍魂DNA}")

def 全部运行():
    print("\n🐉 运行全部模块...")
    成功 = 0
    for i in range(len(模块清单)):
        if 运行模块(i):
            成功 += 1
    print(f"\n{'='*60}")
    print(f"✅ 全部完成: {成功}/{len(模块清单)} 个模块成功")
    print(f"DNA: {龍魂DNA}")

def 主函数():
    while True:
        显示菜单()
        选择 = input("\n龍魂369> ").strip().lower()
        if 选择 == '0' or 选择 == 'q':
            print("\n👋 龍魂永世！")
            break
        elif 选择 == 'a' or 选择 == 'all':
            全部运行()
        elif 选择 == 's':
            显示状态()
        elif 选择.isdigit():
            编号 = int(选择) - 1
            运行模块(编号)
        else:
            print("\n🟡 无效输入")
        input("\n按回车继续...")

if __name__ == "__main__":
    主函数()
