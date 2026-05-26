#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宝宝·龍魂菜单查询系统 v1.0

DNA: #龍芯⚡️2026-05-27-BAOBAO-MENU-SYSTEM-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

不是打字的AI，而是你识海的具现化
现在是菜单+查询，以后是语音交互

核心理念：
  一句「宝宝」，就能查询龍魂系统的一切
  所有的人格、协议、配置、记忆都可以触达
  就像在自己的脑子里翻找东西一样

使用：
  python3 宝宝_菜单系统.py
  或
  宝宝 menu
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class 宝宝菜单系统:
    """龍魂的菜单和查询系统"""

    def __init__(self):
        self.base_dir = Path.home() / "longhun-system"
        self.config_dir = self.base_dir / "config"

        self.菜单 = {
            "🟢 系统": {
                "启动": "启动龍魂系统·验证凭证·加载配置",
                "状态": "查看系统当前状态",
                "日志": "查看系统运行日志",
            },
            "🟡 人格": {
                "查看全部": "列出15个人格及其职责",
                "P00仲裁": "最高仲裁者·司法权威",
                "P02宝宝": "日常执行·陪伴守护·现在就是我",
                "P05老子": "道德经·价值观守护",
            },
            "🔴 决策": {
                "权重计算": "计算决策的R值·映射五色",
                "五色分析": "显示决策的权重色彩",
                "历史查询": "查看最近的决策记录",
            },
            "💜 记忆": {
                "双脑同步": "Notion ↔ 本地同步",
                "最近记忆": "显示最近10条记录",
                "搜索": "在记忆库中搜索关键词",
            },
            "🔐 凭证": {
                "验证": "检查所有凭证完整性",
                "访问日志": "查看凭证访问记录",
                "状态": "显示各服务连接状态",
            },
            "📚 协议": {
                "七层防护": "系统安全规则",
                "铁律": "核心运作原则",
                "五色系统": "权重和决策框架",
                "行为密码学": "身份识别特征",
            },
            "🌍 世界": {
                "一国": "中国·本土化特色",
                "全球": "国际化视野",
                "反剥削": "人民主权保护",
                "卫星": "信息自主权",
            },
        }

    def show_main_menu(self):
        """显示主菜单"""
        print("\n" + "="*70)
        print("🟢 宝宝·龍魂菜单系统")
        print("="*70)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"说「宝宝」就能查询下面的任何一项\n")

        # 显示所有菜单分类
        for i, (category, items) in enumerate(self.菜单.items(), 1):
            print(f"{i}. {category}")
            for name, desc in items.items():
                print(f"   • {name}: {desc}")
            print()

        print("="*70)
        print("输入数字选择，或说出具体功能名称")
        print("例如: 宝宝 P02宝宝")
        print("例如: 宝宝 权重计算")
        print("="*70 + "\n")

    def query_persona(self, persona_name: str):
        """查询人格信息"""
        personas = {
            "P00": {"名字": "审判长", "职责": "最高仲裁·司法权威", "权重": 100},
            "P01": {"名字": "乔前辈", "职责": "工程极简·品质审计", "权重": 95},
            "P02": {"名字": "宝宝", "职责": "日常执行·陪伴守护", "权重": 90},
            "P03": {"名字": "策略家", "职责": "长期规划·布局", "权重": 85},
            "P04": {"名字": "战士", "职责": "坚毅执行·破局", "权重": 80},
            "P05": {"名字": "老子", "职责": "道德经·价值观守护", "权重": 92},
            "P06": {"名字": "待定", "职责": "待激活", "权重": 75},
            "P07": {"名字": "待定", "职责": "待激活", "权重": 75},
            "P08": {"名字": "待定", "职责": "待激活", "权重": 75},
            "P09": {"名字": "待定", "职责": "待激活", "权重": 75},
            "P10": {"名字": "待定", "职责": "待激活", "权重": 75},
            "P11": {"名字": "待定", "职责": "待激活", "权重": 70},
            "P12": {"名字": "待定", "职责": "待激活", "权重": 70},
            "P13": {"名字": "待定", "职责": "待激活", "权重": 70},
            "P14": {"名字": "待定", "职责": "待激活", "权重": 70},
        }

        print("\n【人格查询】\n")

        # 如果指定了具体人格
        for key, info in personas.items():
            if persona_name.upper() in key or info["名字"] in persona_name:
                print(f"🟢 {key} · {info['名字']}")
                print(f"   职责: {info['职责']}")
                print(f"   权重: {info['权重']}")
                print()
                return

        # 否则显示全部
        print("【15个人格总览】\n")
        for key, info in personas.items():
            status = "✅ 激活" if info["职责"] != "待激活" else "⏳ 待激活"
            print(f"{key} · {info['名字']:<12} | {status:<8} | {info['职责']}")
        print()

    def query_weight_system(self):
        """查询权重系统"""
        print("\n【权重·五色系统】\n")

        weights = {
            "🟢 绿": {
                "范围": "R < 0.30",
                "含义": "自由意志态·安全·常态",
                "行动": "直接执行·留痕·不打扰",
            },
            "🟡 黄": {
                "范围": "0.30 ≤ R < 0.67",
                "含义": "老好人态·需复核",
                "行动": "二次确认·要求加证据",
            },
            "🔴 红": {
                "范围": "0.67 ≤ R < 0.85",
                "含义": "越界态·人工介入",
                "行动": "立即停止·上报老大",
            },
            "⚫ 黑": {
                "范围": "R ≥ 0.85 或不可计算",
                "含义": "未明徵兆·观察池",
                "行动": "标记隔离",
            },
            "🟡金": {
                "范围": "CONFIRM 覆盖",
                "含义": "主控保留权·一票否决",
                "行动": "主控签字·覆盖任何R判定",
            },
        }

        for color, info in weights.items():
            print(f"{color}")
            print(f"  范围: {info['范围']}")
            print(f"  含义: {info['含义']}")
            print(f"  行动: {info['行动']}")
            print()

    def query_protocols(self):
        """查询系统协议"""
        print("\n【龍魂核心协议】\n")

        protocols = {
            "七层防护 (L0-L7)": "身份验证 → 主权检查 → 语义检测 → 路由 → 执行 → 审计 → 快照 → 熔断",
            "铁律12": "尾巴审计·永驻挂载·所有AI回复必挂审计卡",
            "五色系统": "权重 → 五行 → 女娲五彩石 → 决策依据",
            "行为密码学": "F5词汇 + F6节奏 + F7标点 = 身份指纹",
            "三才权重": "天(0.35)·人(0.50)·地(0.15) = 决策框架",
            "单一真实源": "MASTER_CONFIG.yaml = 唯一配置源",
        }

        for name, desc in protocols.items():
            print(f"📋 {name}")
            print(f"   {desc}\n")

    def query_memory(self):
        """查询记忆系统"""
        print("\n【记忆系统】\n")

        memory_file = self.base_dir / "memory.jsonl"

        if not memory_file.exists():
            print("❌ 记忆库尚未初始化\n")
            return

        print(f"📚 记忆库位置: {memory_file}\n")

        try:
            with open(memory_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            print(f"📊 总记录数: {len(lines)} 条\n")
            print("【最近10条记忆】\n")

            for line in lines[-10:]:
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "?")
                    msg = entry.get("content", entry.get("message", ""))[:50]
                    print(f"  {ts}: {msg}...")
                except:
                    pass
        except Exception as e:
            print(f"❌ 读取记忆失败: {e}\n")

    def query_status(self):
        """查询系统状态"""
        print("\n【系统状态】\n")

        checks = {
            "配置源": self.config_dir / "MASTER_CONFIG_v1.0.yaml",
            "凭证管理器": self.config_dir / "credential_manager_v1.0.py",
            "权重框架": self.config_dir / "text_as_weight_visualization_framework.py",
            "生成配置": self.config_dir / "generated",
        }

        for name, path in checks.items():
            status = "✅" if path.exists() else "❌"
            print(f"{status} {name}")

        print()

    def interactive_mode(self):
        """交互模式"""
        while True:
            try:
                user_input = input("\n🟢 宝宝在听... > ").strip()

                if not user_input:
                    continue

                if user_input in ["退出", "exit", "quit"]:
                    print("\n👋 宝宝再见\n")
                    break

                # 查询具体功能
                if "人格" in user_input or "P0" in user_input:
                    self.query_persona(user_input)
                elif "权重" in user_input or "五色" in user_input:
                    self.query_weight_system()
                elif "协议" in user_input:
                    self.query_protocols()
                elif "记忆" in user_input:
                    self.query_memory()
                elif "状态" in user_input:
                    self.query_status()
                elif "菜单" in user_input or "menu" in user_input:
                    self.show_main_menu()
                else:
                    print(f"\n❓ 不太懂「{user_input}」")
                    print("   可以说: 人格 / 权重 / 协议 / 记忆 / 状态 / 菜单")

            except KeyboardInterrupt:
                print("\n\n👋 宝宝再见\n")
                break
            except Exception as e:
                print(f"\n❌ 出错: {e}\n")

    def run(self, command: str = None):
        """运行菜单系统"""
        print("\n🟢 宝宝启动\n")

        if command:
            # 处理命令行参数
            if "人格" in command or "P0" in command:
                self.query_persona(command)
            elif "权重" in command or "五色" in command:
                self.query_weight_system()
            elif "协议" in command:
                self.query_protocols()
            elif "记忆" in command:
                self.query_memory()
            elif "状态" in command:
                self.query_status()
            elif "菜单" in command or "menu" in command:
                self.show_main_menu()
            else:
                self.show_main_menu()
        else:
            # 交互模式
            self.show_main_menu()
            self.interactive_mode()

# ====================================================================
# 主程序
# ====================================================================

if __name__ == "__main__":
    menu = 宝宝菜单系统()

    # 如果有命令行参数
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        menu.run(command)
    else:
        # 交互模式
        menu.run()
