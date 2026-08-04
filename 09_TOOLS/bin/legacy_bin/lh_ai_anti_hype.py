#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   龍魂·AI反诈防火墙 v1.0 — 100张话术卡片拆穿AI营销忽悠                        ║
║   AI Anti-Hype Firewall · Hype Detection · Plain-Language Translation   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·辛酉·卯时·大有-ANTI-HYPE-FIREWALL-v1.0              ║
║  源矿: backups/cs-kb-enhanced-20260701/cs_kb.db (100张AI行业话术)          ║
║  原理: 词库匹配→hype等级拆解→误导点揭露→大白话重写                            ║
║  铁律: 不联网·本地词库·不冤枉好词·不放过忽悠                                    ║
╠══════════════════════════════════════════════════════════════════════════╣
║  用法:                                                                    ║
║    python3 bin/lh_ai_anti_hype.py --scan "这段文字含AI忽悠"                 ║
║    python3 bin/lh_ai_anti_hype.py --all                                  ║
║    python3 bin/lh_ai_anti_hype.py --top-hype                             ║
║    python3 bin/lh_ai_anti_hype.py --interactive                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "backups" / "cs-kb-enhanced-20260701" / "cs_kb.db"


# ═══════════════════════════════════════════════════════════
# §1 话术卡片加载
# ═══════════════════════════════════════════════════════════

@dataclass
class HypeCard:
    """单张话术卡片"""
    card_id: str
    名称: str
    别名: str = ""
    描述: str = ""
    公式: str = ""          # core_formula → 真实底座
    误区: str = ""          # misconceptions → 误导点
    触发词: str = ""        # context_trigger → 关键词
    hype等级: int = 0
    人格路由: str = ""
    难度: str = ""

    def 大白话(self) -> str:
        """提取真实含义的大白话版本"""
        if self.公式:
            return self.公式
        if self.误区:
            # 从误区中提取"真实底座是..."
            m = re.search(r'真实底座[是為为].*?[:：]?\s*(.+?)(?:[。，\n]|$)', self.误区)
            if m:
                return m.group(1).strip()
        # fallback: 描述的前半句
        if self.描述:
            return self.描述.split("。")[0]
        return "无"

    def 忽悠程度(self) -> str:
        """hype等级转中文描述"""
        level_map = {
            1: "🟢 老实 — 基本属实",
            2: "🟢🟡 轻度 — 略有夸张",
            3: "🟡 中度 — 注意甄别",
            4: "🟡🔴 重度 — 多半夸大",
            5: "🔴 极度 — 纯忽悠",
        }
        return level_map.get(self.hype等级, "⚪ 未知")


def _parse_hype_level(text: str) -> int:
    """从文本中提取 hype 等级"""
    if not text:
        return 0
    m = re.search(r'hype\s*(?:等级)?\s*(\d)\s*/?\s*5', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # 从误区中找
    m2 = re.search(r'(?:夸大|夸张|hype).*?(\d)/5', text, re.IGNORECASE)
    if m2:
        return int(m2.group(1))
    return 0


def 加载话术词库(db_path: str | None = None) -> List[HypeCard]:
    """从SQLite加载100张AI行业话术卡片"""
    if db_path is None:
        db_path = str(DB_PATH)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT * FROM cs_kb WHERE category='AI行业话术' ORDER BY cast(card_id as integer)"
        ).fetchall()
        卡片列表 = []
        for r in rows:
            d = dict(r)
            combined_text = (d.get("description", "") or "") + " " + (d.get("misconceptions", "") or "")
            hype = _parse_hype_level(combined_text)

            card = HypeCard(
                card_id=d.get("card_id", ""),
                名称=d.get("name", ""),
                别名=d.get("subcategory", "") or "",
                描述=d.get("description", "") or "",
                公式=d.get("core_formula", "") or "",
                误区=d.get("misconceptions", "") or "",
                触发词=d.get("context_trigger", "") or "",
                hype等级=hype,
                人格路由=d.get("persona_route", "") or "",
                难度=d.get("difficulty", "") or "",
            )
            卡片列表.append(card)
        return 卡片列表
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════
# §2 反诈检测引擎
# ═══════════════════════════════════════════════════════════

class 反诈防火墙:
    """扫描文本·发现AI忽悠词·拆穿营销话术"""

    def __init__(self):
        self.词库 = 加载话术词库()
        self._构建索引()

    def _构建索引(self):
        """构建关键词→卡片索引"""
        通用噪音词 = {"ai", "model", "agent", "learning", "foundation", "llm", 
                      "data", "system", "network", "model", "base", "large",
                      "deep", "neural", "pre", "fine", "self"}
        self.关键词索引: Dict[str, List[HypeCard]] = {}
        self.主名索引: Dict[str, HypeCard] = {}  # 卡片主名→卡片 (精确匹配用)
        for card in self.词库:
            # 提取主名 (第一个词)
            主名 = card.名称.split("·")[0].strip().lower()
            self.主名索引[主名] = card
            
            # 从名称和触发词提取关键词
            关键词组 = set()
            for kw in card.触发词.replace("·", " ").replace("/", " ").split():
                kw = kw.strip().lower()
                if kw and len(kw) >= 3 and kw not in 通用噪音词:
                    关键词组.add(kw)
            # 也加名称中的核心词 (过滤掉中文部分避免误匹配)
            for kw in card.名称.replace("·", " ").split():
                kw = kw.strip().lower()
                if kw and len(kw) >= 3 and kw not in 通用噪音词:
                    关键词组.add(kw)

            for kw in 关键词组:
                if kw not in self.关键词索引:
                    self.关键词索引[kw] = []
                if card not in self.关键词索引[kw]:
                    self.关键词索引[kw].append(card)

    def 扫描(self, 文本: str) -> Dict[str, Any]:
        """扫描一段文本·输出所有发现的忽悠词"""
        文本小写 = 文本.lower()
        发现: Dict[str, HypeCard] = {}
        命中关键词: Dict[str, List[str]] = {}

        # 第一轮: 关键词索引匹配
        for kw, cards in self.关键词索引.items():
            if kw in 文本小写:
                for card in cards:
                    if card.card_id not in 发现:
                        发现[card.card_id] = card
                        命中关键词[card.card_id] = []
                    命中关键词[card.card_id].append(kw)

        # 第二轮: 主名精确匹配 (作为补充)
        for 主名, card in self.主名索引.items():
            if 主名 in 文本小写 and card.card_id not in 发现:
                发现[card.card_id] = card
                命中关键词[card.card_id] = ["[主名]"]

        # 按hype等级排序
        结果列表 = sorted(发现.values(), key=lambda c: -c.hype等级)

        # 统分
        总忽悠度 = sum(c.hype等级 for c in 结果列表) / max(len(结果列表), 1) if 结果列表 else 0
        hype3以上 = [c for c in 结果列表 if c.hype等级 >= 3]
        hype4以上 = [c for c in 结果列表 if c.hype等级 >= 4]

        return {
            "输入文本": 文本[:200] + ("..." if len(文本) > 200 else ""),
            "发现术语数": len(结果列表),
            "平均忽悠度": round(总忽悠度, 2),
            "高危(hype≥4)": len(hype4以上),
            "需警惕(hype≥3)": len(hype3以上),
            "判定": self._判定(总忽悠度, len(hype4以上)),
            "术语列表": [
                {
                    "术语": c.名称,
                    "card_id": c.card_id,
                    "hype等级": c.hype等级,
                    "忽悠度": c.忽悠程度(),
                    "大白话": c.大白话(),
                    "营销误导": c.误区[:120] if c.误区 else "",
                    "命中词": 命中关键词.get(c.card_id, []),
                }
                for c in 结果列表
            ],
        }

    def _判定(self, 平均度: float, 高危数: int) -> str:
        if 高危数 >= 3:
            return "🔴 高危 — 这段文字存在严重AI营销忽悠·建议全面核查"
        elif 平均度 >= 3.5:
            return "🔴 可疑 — 多项AI话术可能存在夸大·逐条核实"
        elif 平均度 >= 2.5:
            return "🟡 提醒 — 部分术语可能有夸大成分·注意甄别"
        elif 平均度 >= 1.5:
            return "🟡🟢 轻度 — 基本属实·个别表述略夸张"
        elif 平均度 > 0:
            return "🟢 干净 — 未发现明显AI忽悠"
        else:
            return "🟢 安全 — 未检测到AI话术词"

    def 全局统计(self) -> Dict[str, Any]:
        """全100张话术统计"""
        hype分布 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for c in self.词库:
            if c.hype等级 in hype分布:
                hype分布[c.hype等级] += 1

        top10 = sorted(self.词库, key=lambda c: -c.hype等级)[:20]

        return {
            "总卡片数": len(self.词库),
            "hype等级分布": hype分布,
            "平均hype": round(sum(c.hype等级 for c in self.词库) / len(self.词库), 2),
            "高危Top20": [
                {"术语": c.名称, "hype": c.hype等级, "大白话": c.大白话()[:80]}
                for c in top10
            ],
        }

    def 大白话翻译(self, 文本: str) -> str:
        """把含AI忽悠的文本翻译成大白话"""
        结果 = self.扫描(文本)
        if not 结果["术语列表"]:
            return 文本

        translated = 文本
        for item in 结果["术语列表"]:
            原名 = item["术语"].split("·")[0].strip()
            白话 = item["大白话"]
            if 原名 and 白话 and 原名 != 白话:
                # 替换: 原名 → 白话(原名)
                translated = re.sub(
                    re.escape(原名),
                    f"「{原名}」({白话})",
                    translated,
                    flags=re.IGNORECASE,
                )
        return translated


# ═══════════════════════════════════════════════════════════
# §3 格式化输出
# ═══════════════════════════════════════════════════════════

def 打印扫描结果(结果: Dict[str, Any]):
    print("\n" + "═" * 68)
    print("  🛡️ 龍魂·AI反诈防火墙 — 扫描报告")
    print("═" * 68)
    print(f"\n  扫描文本: {结果['输入文本']}")
    print(f"\n  📊 统计:")
    print(f"    发现AI术语: {结果['发现术语数']}个")
    print(f"    平均忽悠度: {结果['平均忽悠度']}/5")
    print(f"    高危(hype≥4): {结果['高危(hype≥4)']}个")
    print(f"    需警惕(hype≥3): {结果['需警惕(hype≥3)']}个")
    print(f"\n  ⚖️ 综合判定: {结果['判定']}")

    if 结果["术语列表"]:
        print(f"\n  📋 逐项拆穿:\n")
        for i, item in enumerate(结果["术语列表"], 1):
            hype_icon = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🟢", 1: "✅"}.get(item["hype等级"], "⚪")
            print(f"  [{i}] {hype_icon} {item['术语']}")
            print(f"      hype={item['hype等级']}/5 {item['忽悠度']}")
            print(f"      真实含义: {item['大白话']}")
            if item["营销误导"]:
                print(f"      常见误导: {item['营销误导'][:100]}...")
            print(f"      命中关键词: {', '.join(item['命中词'])}")
            print()

    print("─" * 68)
    print("  💡 提示: 用 --translate 把全文翻译成大白话")
    print("═" * 68 + "\n")


def 打印全局统计(统计: Dict[str, Any]):
    print("\n" + "═" * 68)
    print("  📚 龍魂·100张AI话术词库全景")
    print("═" * 68)
    print(f"\n  总卡片: {统计['总卡片数']}张")
    print(f"  平均hype: {统计['平均hype']}/5")

    print("\n  📊 Hype等级分布:")
    for level in range(5, 0, -1):
        count = 统计["hype等级分布"].get(level, 0)
        bar = "█" * count
        print(f"  {level}/5: {bar} {count}张")

    print("\n  🔴 高危Top20 (最忽悠的词):\n")
    for i, c in enumerate(统计["高危Top20"], 1):
        icon = {5: "🔴", 4: "🟠", 3: "🟡"}.get(c["hype"], "⚪")
        print(f"  {i:2d}. {icon} hype{c['hype']}/5 | {c['术语']}")
        print(f"       实话: {c['大白话']}")
        print()

    print("═" * 68 + "\n")


def 打印大白话翻译(原文: str, 翻译: str, 扫描结果: Dict[str, Any]):
    print("\n" + "═" * 68)
    print("  📝 大白话翻译")
    print("═" * 68)
    print(f"\n  原文:\n    {原文[:300]}{'...' if len(原文)>300 else ''}")
    print(f"\n  翻译后:\n    {翻译[:500]}{'...' if len(翻译)>500 else ''}")
    print(f"\n  共替换 {扫描结果['发现术语数']} 个忽悠词")
    print("═" * 68 + "\n")


# ═══════════════════════════════════════════════════════════
# §4 预置测试样本
# ═══════════════════════════════════════════════════════════

TEST_SAMPLES = {
    "AI招聘文案": "我们使用AGI级别的Foundation Model，通过Multi-Agent架构实现端到端的智能体协作，配备Long Context记忆和RLHF对齐，为企业提供下一代AI解决方案。",
    "AI产品发布会": "我们的新产品搭载了最先进的LLM大语言模型，具备Reasoning Model的深度思考能力，通过Constitutional AI确保安全对齐，采用DPO直接偏好优化实现人类价值观对齐。",
    "投资人Pitch": "我们的ASI路线图已经清晰：从当前的LLM出发，通过Scaling Law持续扩展，引入Multi-Modal多模态能力，最终实现AGI。我们的护城河是独家的SFT监督微调数据和RLHF反馈系统。",
    "技术博客": "本文介绍了Transformer架构中Multi-Head Attention的计算原理，重点讨论了LLM中Tokenization对下游任务的影响，以及Prompt Engineering在Few-Shot Learning场景下的最佳实践。",
}


# ═══════════════════════════════════════════════════════════
# §5 CLI
# ═══════════════════════════════════════════════════════════

def 主函数():
    parser = argparse.ArgumentParser(
        description="龍魂·AI反诈防火墙 — 100张话术卡片拆穿AI营销忽悠",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_ai_anti_hype.py --scan "我们的AGI产品..."
  python3 bin/lh_ai_anti_hype.py --test           # 测试预置样本
  python3 bin/lh_ai_anti_hype.py --all            # 查看全部100张话术
  python3 bin/lh_ai_anti_hype.py --top-hype       # 高危Top20
  python3 bin/lh_ai_anti_hype.py --translate "文本"
  python3 bin/lh_ai_anti_hype.py --interactive
        """,
    )
    parser.add_argument("--scan", "-s", help="扫描一段文本中的AI忽悠术语")
    parser.add_argument("--test", "-t", action="store_true", help="用预置样本测试(4段典型文本)")
    parser.add_argument("--all", "-a", action="store_true", help="显示全部100张话术统计")
    parser.add_argument("--top-hype", action="store_true", help="显示忽悠度最高的Top20")
    parser.add_argument("--translate", help="将含AI忽悠的文本翻译成大白话")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    fw = 反诈防火墙()

    try:
        if args.scan:
            结果 = fw.扫描(args.scan)
            if args.json:
                print(json.dumps(结果, ensure_ascii=False, indent=2))
            else:
                打印扫描结果(结果)

        elif args.test:
            for 标题, 文本 in TEST_SAMPLES.items():
                print(f"\n{'▔'*68}")
                print(f"  📋 测试样本: {标题}")
                print(f"{'▔'*68}")
                结果 = fw.扫描(文本)
                打印扫描结果(结果)

        elif args.all:
            统计 = fw.全局统计()
            if args.json:
                print(json.dumps(统计, ensure_ascii=False, indent=2))
            else:
                打印全局统计(统计)

        elif args.top_hype:
            统计 = fw.全局统计()
            print("\n" + "═" * 68)
            print("  🔴 高危Top20 — 最忽悠的AI术语")
            print("═" * 68 + "\n")
            for i, c in enumerate(统计["高危Top20"], 1):
                hype = c["hype"]
                icon = {5: "🔴", 4: "🟠", 3: "🟡"}.get(hype, "⚪")
                print(f"  {i:2d}. {icon} hype{hype}/5 | {c['术语']}")
                print(f"       实话: {c['大白话']}")
                print()
            print("═" * 68 + "\n")

        elif args.translate:
            结果 = fw.扫描(args.translate)
            翻译 = fw.大白话翻译(args.translate)
            打印大白话翻译(args.translate, 翻译, 结果)

        elif args.interactive:
            交互模式(fw)

        else:
            parser.print_help()

    finally:
        pass


def 交互模式(fw: 反诈防火墙):
    print("\n" + "═" * 68)
    print("  🛡️ 龍魂·AI反诈防火墙 · 交互模式")
    print("═" * 68)

    while True:
        print("\n  选项:")
        print("    [1] 粘贴文本扫描")
        print("    [2] 用预置样本测试")
        print("    [3] 查看全部话术统计")
        print("    [4] 高危Top20")
        print("    [5] 大白话翻译")
        print("    [6] 查某个术语")
        print("    [0] 退出")

        选择 = input("\n  请输入选项: ").strip()

        if 选择 == "0":
            print("  再见 🛡️\n")
            break
        elif 选择 == "1":
            文本 = input("  请粘贴要扫描的文本:\n  > ").strip()
            if 文本:
                结果 = fw.扫描(文本)
                打印扫描结果(结果)
        elif 选择 == "2":
            print("\n  预置测试样本:\n")
            samples = list(TEST_SAMPLES.items())
            for i, (标题, _) in enumerate(samples, 1):
                print(f"  [{i}] {标题}")
            子选择 = input("\n  选择编号(回车=全部): ").strip()
            if 子选择.isdigit():
                idx = int(子选择) - 1
                if 0 <= idx < len(samples):
                    结果 = fw.扫描(samples[idx][1])
                    打印扫描结果(结果)
            else:
                for 标题, 文本 in samples:
                    print(f"\n{'─'*68}")
                    print(f"  📋 {标题}")
                    print(f"{'─'*68}")
                    结果 = fw.扫描(文本)
                    打印扫描结果(结果)
        elif 选择 == "3":
            统计 = fw.全局统计()
            打印全局统计(统计)
        elif 选择 == "4":
            统计 = fw.全局统计()
            print("\n" + "═" * 68)
            print("  🔴 高危Top20\n")
            for i, c in enumerate(统计["高危Top20"], 1):
                icon = {5: "🔴", 4: "🟠", 3: "🟡"}.get(c["hype"], "⚪")
                print(f"  {i:2d}. {icon} hype{c['hype']}/5 | {c['术语']}")
                print(f"       实话: {c['大白话']}")
                print()
        elif 选择 == "5":
            文本 = input("  请粘贴要翻译的文本:\n  > ").strip()
            if 文本:
                结果 = fw.扫描(文本)
                翻译 = fw.大白话翻译(文本)
                打印大白话翻译(文本, 翻译, 结果)
        elif 选择 == "6":
            关键词 = input("  搜索术语名: ").strip()
            if 关键词:
                found = [c for c in fw.词库 if 关键词.lower() in c.名称.lower()]
                if found:
                    for c in found[:5]:
                        hype_icon = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🟢", 1: "✅"}.get(c.hype等级, "⚪")
                        print(f"\n  {hype_icon} {c.名称} [hype={c.hype等级}/5]")
                        print(f"     ID: {c.card_id} | 难度: {c.难度}")
                        print(f"     大白话: {c.大白话()}")
                        print(f"     描述: {c.描述[:120]}...")
                        if c.误区:
                            print(f"     误导: {c.误区[:120]}...")
                else:
                    print(f"  ⚠️ 未找到术语「{关键词}」")


if __name__ == "__main__":
    主函数()
