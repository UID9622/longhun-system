#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·数字根计算引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-数字根引擎-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：提取任意文本中的数字，反复相加到一位数（0-9）
定位：CNSH流场压缩核 · 第一步 · 数字根→五行→三色审计
"""

import sys
import re
import argparse
from typing import Union, List, Optional, Dict, Any

# ========== 核心引擎 ==========
class 数字根引擎:
    """
    龍魂数字根计算引擎
    输入任意文本 → 提取数字 → 反复相加 → 输出一位数（0-9）
    """

    # 数字根→五行映射表（供外部调用）
    五行映射表 = {
        0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
        5: "土", 6: "水", 7: "火", 8: "木", 9: "金"
    }

    # 数字根→三色审计映射
    三色审计表 = {
        3: "🔴",  # 熔断
        9: "🔴",  # 熔断
        6: "🟡",  # 待审
        # 其他: 🟢
    }

    @staticmethod
    def 计算(输入: Union[str, int, float]) -> int:
        """
        计算数字根（核心方法）
        输入：文本、数字、或可转为字符串的对象
        输出：0-9 的数字根
        """
        文本 = str(输入)
        # 提取所有数字（包括 Unicode 上标/圆圈数字）
        import unicodedata
        数字列表 = []
        for c in 文本:
            if c.isdigit():
                try:
                    数字列表.append(int(c))
                except ValueError:
                    # Unicode 数字（如 ①②③）取 normalize 后的 digit 值
                    try:
                        d = unicodedata.digit(c)
                        数字列表.append(d)
                    except (ValueError, TypeError):
                        pass

        if not 数字列表:
            return 0

        总和 = sum(数字列表)
        # 反复相加直到一位数
        while 总和 >= 10:
            总和 = sum(int(c) for c in str(总和))

        return 总和

    @staticmethod
    def 带五行(输入: Union[str, int, float]) -> Dict[str, Any]:
        """
        计算数字根 + 附带五行信息
        返回：{数字根, 五行, 颜色, 三色审计}
        """
        dr = 数字根引擎.计算(输入)
        五行 = 数字根引擎.五行映射表.get(dr, "土")
        三色 = 数字根引擎.三色审计表.get(dr, "🟢")

        # 五行对应颜色
        颜色表 = {
            "金": "金色/白金",
            "木": "青绿",
            "水": "深蓝/青蓝",
            "火": "朱红/暖橙",
            "土": "土黄/琥珀"
        }

        return {
            "数字根": dr,
            "五行": 五行,
            "颜色": 颜色表.get(五行, "未知"),
            "三色审计": 三色,
            "原始输入": str(输入)[:100]
        }

    @staticmethod
    def 批量计算(输入列表: List[Union[str, int, float]]) -> List[int]:
        """批量计算数字根"""
        return [数字根引擎.计算(输入) for 输入 in 输入列表]

    @staticmethod
    def 从文件(文件路径: str) -> List[int]:
        """从文件读取内容并逐行计算数字根"""
        try:
            with open(文件路径, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [数字根引擎.计算(line.strip()) for line in lines if line.strip()]
        except FileNotFoundError:
            print(f"❌ 文件不存在: {文件路径}")
            return []

    @staticmethod
    def 验证(输入: Union[str, int, float], 预期: int) -> bool:
        """验证数字根是否等于预期值"""
        return 数字根引擎.计算(输入) == 预期


# ========== 命令行接口 ==========
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·数字根计算引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 计算单个数字根
  python3 lh_digital_root.py 9622
  python3 lh_digital_root.py "2026-05-01 收到转账 9622 元"

  # 批量计算
  python3 lh_digital_root.py --batch 123 456 789
  python3 lh_digital_root.py -b "甲子年" "丙午月" "庚申日"

  # 计算时附带五行信息
  python3 lh_digital_root.py --with-wuxing 9622

  # 从文件读取
  python3 lh_digital_root.py --file data.txt

  # 验证功能
  python3 lh_digital_root.py --verify 9622 5

  # 交互式模式
  python3 lh_digital_root.py --interactive
        """
    )

    parser.add_argument(
        "输入",
        nargs="*",
        help="要计算数字根的文本或数字（多个时用空格分隔）"
    )
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="批量计算模式（输入多个值，逐个输出）"
    )
    parser.add_argument(
        "-w", "--with-wuxing",
        action="store_true",
        help="附带五行信息输出"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="从文件读取内容并逐行计算"
    )
    parser.add_argument(
        "--verify",
        nargs=2,
        metavar=("输入", "预期"),
        help="验证数字根是否等于预期值"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="交互式模式，持续输入计算"
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="显示数字根→五行映射表"
    )

    args = parser.parse_args()

    # 显示映射表
    if args.table:
        print("\n" + "=" * 50)
        print("🐉 数字根→五行→三色审计 映射表")
        print("=" * 50)
        print("┌─────────┬────────┬────────────┬──────────┐")
        print("│ 数字根  │ 五行   │ 三色审计   │ 含义     │")
        print("├─────────┼────────┼────────────┼──────────┤")
        for dr in range(10):
            五行 = 数字根引擎.五行映射表[dr]
            三色 = 数字根引擎.三色审计表.get(dr, "🟢")
            含义 = {
                0: "无数字/土",
                1: "水·记忆",
                2: "火·文明",
                3: "木·创新(熔断)",
                4: "金·规则",
                5: "土·普惠",
                6: "水·记忆(待审)",
                7: "火·文明",
                8: "木·创新",
                9: "金·规则(熔断)"
            }[dr]
            print(f"│    {dr}    │  {五行}   │   {三色}    │ {含义} │")
        print("└─────────┴────────┴────────────┴──────────┘")
        print("\n🔴 熔断: 3, 9  |  🟡 待审: 6  |  🟢 通行: 其他")
        return

    # 验证模式
    if args.verify:
        输入, 预期 = args.verify
        try:
            预期 = int(预期)
            实际 = 数字根引擎.计算(输入)
            if 实际 == 预期:
                print(f"✅ 验证通过: {输入} → {实际} (预期 {预期})")
            else:
                print(f"❌ 验证失败: {输入} → {实际} (预期 {预期})")
        except ValueError:
            print("❌ 预期值必须为整数")
        return

    # 从文件读取
    if args.file:
        结果 = 数字根引擎.从文件(args.file)
        if 结果:
            print("\n".join(str(r) for r in 结果))
        return

    # 交互式模式
    if args.interactive:
        print("\n🐉 数字根计算引擎 · 交互模式")
        print("输入任意内容计算数字根，输入 'exit' 或 'q' 退出")
        print("-" * 40)
        while True:
            try:
                输入 = input("> ").strip()
                if 输入.lower() in ('exit', 'q', 'quit'):
                    print("👋 退出")
                    break
                if not 输入:
                    continue
                if args.with_wuxing:
                    结果 = 数字根引擎.带五行(输入)
                    print(f"  数字根: {结果['数字根']} | 五行: {结果['五行']} | {结果['三色审计']}")
                else:
                    print(f"  → {数字根引擎.计算(输入)}")
            except KeyboardInterrupt:
                print("\n👋 退出")
                break
        return

    # 批量模式
    if args.batch and args.输入:
        for 输入 in args.输入:
            if args.with_wuxing:
                结果 = 数字根引擎.带五行(输入)
                print(f"{输入} → {结果['数字根']} ({结果['五行']}) {结果['三色审计']}")
            else:
                print(f"{输入} → {数字根引擎.计算(输入)}")
        return

    # 单值模式
    if args.输入:
        输入 = " ".join(args.输入)
        if args.with_wuxing:
            结果 = 数字根引擎.带五行(输入)
            print(f"""
┌─────────────────────────────┐
│  🐉 数字根计算报告          │
├─────────────────────────────┤
│  原始输入: {结果['原始输入']}
│  数字根:   {结果['数字根']}
│  五行:     {结果['五行']}
│  颜色:     {结果['颜色']}
│  三色审计: {结果['三色审计']}
└─────────────────────────────┘
            """)
        else:
            print(f"{输入} → {数字根引擎.计算(输入)}")
        return

    # 无参数时显示帮助
    parser.print_help()


# ========== 模块导出 ==========
__all__ = ["数字根引擎", "计算数字根"]

# 快捷别名
计算数字根 = 数字根引擎.计算

if __name__ == "__main__":
    main()
