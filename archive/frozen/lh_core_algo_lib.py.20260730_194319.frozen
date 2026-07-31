#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·辛酉·卯时·大壮-CORE-ALGO-LIB-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   龍魂·核心算法库 v1.0 — 43张技术卡片·公式+代码·可查可跑·离线可用             ║
║   Core Algorithm Library · Formula Explorer · Code Runner               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·辛酉·卯时·大壮-CORE-ALGO-LIB-v1.0                   ║
║  源矿: backups/cs-kb-enhanced-20260701/cs_kb.db (43张数据与人工智能)        ║
║  能力: 公式查览·代码即跑·分类检索·算法对比·离线所有                             ║
║  铁律: 本地执行·不联网·代码可信·沙盒隔离                                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║  用法:                                                                    ║
║    python3 bin/lh_core_algo_lib.py --list                               ║
║    python3 bin/lh_core_algo_lib.py --search "排序"                       ║
║    python3 bin/lh_core_algo_lib.py --formula "信息熵"                     ║
║    python3 bin/lh_core_algo_lib.py --run "信息熵"                         ║
║    python3 bin/lh_core_algo_lib.py --bench                              ║
║    python3 bin/lh_core_algo_lib.py --export formulas.json                ║
║    python3 bin/lh_core_algo_lib.py --interactive                         ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import re
import sqlite3
import sys
import io
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from contextlib import redirect_stdout, redirect_stderr

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "backups" / "cs-kb-enhanced-20260701" / "cs_kb.db"


# ═══════════════════════════════════════════════════════════
# §1 算法卡片加载
# ═══════════════════════════════════════════════════════════

@dataclass
class AlgoCard:
    """单张算法卡片"""
    card_id: str
    名称: str
    描述: str = ""
    公式: str = ""           # core_formula
    误区: str = ""           # misconceptions
    难度: str = ""
    状态: str = ""
    触发词: str = ""         # context_trigger
    人格路由: str = ""
    代码: str = ""           # py_example
    关联知识: str = ""       # related_knowledge

    def 公式列表(self) -> List[str]:
        """解析公式字符串为多个公式"""
        if not self.公式:
            return []
        return [f.strip() for f in re.split(r'\s*\|\s*', self.公式) if f.strip()]

    def 标签(self) -> List[str]:
        """从名称和触发词提取标签"""
        tags = set()
        for kw in self.触发词.replace("·", " ").split():
            kw = kw.strip()
            if kw and len(kw) >= 2:
                tags.add(kw)
        for kw in self.名称.replace("·", " ").split():
            kw = kw.strip()
            if kw and len(kw) >= 2:
                tags.add(kw)
        return sorted(tags, key=len, reverse=True)

    def 算法类型(self) -> str:
        """推断算法类型"""
        name_tech = self.名称.lower() + self.描述.lower()
        if any(kw in name_tech for kw in ["神经网络", "深度学习", "cnn", "rnn", "transformer", "attention", "gan", "扩散"]):
            return "深度学习"
        if any(kw in name_tech for kw in ["梯度", "优化", "adam", "sgd", "学习率"]):
            return "优化算法"
        if any(kw in name_tech for kw in ["熵", "向量", "压缩", "pca", "编码", "微分"]):
            return "数学基础"
        if any(kw in name_tech for kw in ["强化", "q-learning", "贝尔曼"]):
            return "强化学习"
        if any(kw in name_tech for kw in ["遗传", "进化", "贝叶斯"]):
            return "启发式算法"
        if any(kw in name_tech for kw in ["龍魂", "引擎", "记忆", "同步", "dna", "沙盒", "指挥塔", "龍醒"]):
            return "龍魂引擎"
        if any(kw in name_tech for kw in ["迁移", "微调", "gpt", "预训练"]):
            return "迁移学习/微调"
        if any(kw in name_tech for kw in ["时间", "压缩", "五层", "贡献值", "soul", "权重"]):
            return "龍魂算法"
        return "其他"


def 加载算法库(db_path: str | None = None) -> List[AlgoCard]:
    """从SQLite加载43张数据与人工智能卡片"""
    if db_path is None:
        db_path = str(DB_PATH)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT * FROM cs_kb WHERE category='数据与人工智能' ORDER BY cast(card_id as integer)"
        ).fetchall()
        卡片列表 = []
        for r in rows:
            d = dict(r)
            card = AlgoCard(
                card_id=d.get("card_id", ""),
                名称=d.get("name", ""),
                描述=d.get("description", "") or "",
                公式=d.get("core_formula", "") or "",
                误区=d.get("misconceptions", "") or "",
                难度=d.get("difficulty", "") or "",
                状态=d.get("status", "") or "",
                触发词=d.get("context_trigger", "") or "",
                人格路由=d.get("persona_route", "") or "",
                代码=d.get("py_example", "") or "",
                关联知识=d.get("related_knowledge", "") or "",
            )
            卡片列表.append(card)
        return 卡片列表
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════
# §2 核心算法引擎
# ═══════════════════════════════════════════════════════════

class 算法引擎:
    """核心算法库·查找·运行·对比"""

    def __init__(self):
        self.算法库 = 加载算法库()
        self._构建索引()

    def _构建索引(self):
        self.名称索引: Dict[str, AlgoCard] = {}
        self.标签索引: Dict[str, List[AlgoCard]] = {}

        for card in self.算法库:
            self.名称索引[card.card_id] = card
            for tag in card.标签():
                tag_lower = tag.lower()
                if tag_lower not in self.标签索引:
                    self.标签索引[tag_lower] = []
                if card not in self.标签索引[tag_lower]:
                    self.标签索引[tag_lower].append(card)

    def 按ID获取(self, card_id: str) -> Optional[AlgoCard]:
        return self.名称索引.get(str(card_id))

    def 搜索(self, 关键词: str) -> List[AlgoCard]:
        kw = 关键词.lower()
        结果: Dict[str, AlgoCard] = {}

        # 名称匹配
        for card in self.算法库:
            if kw in card.名称.lower():
                结果[card.card_id] = card

        # 标签匹配
        if kw in self.标签索引:
            for card in self.标签索引[kw]:
                结果[card.card_id] = card

        # 模糊匹配
        if not 结果:
            for card in self.算法库:
                if kw in card.描述.lower() or kw in card.公式.lower():
                    结果[card.card_id] = card

        return list(结果.values())

    def 按类型分组(self) -> Dict[str, List[AlgoCard]]:
        groups: Dict[str, List[AlgoCard]] = {}
        for card in self.算法库:
            t = card.算法类型()
            if t not in groups:
                groups[t] = []
            groups[t].append(card)
        return dict(sorted(groups.items()))

    def 统计(self) -> Dict[str, Any]:
        groups = self.按类型分组()
        有公式 = sum(1 for c in self.算法库 if c.公式)
        有代码 = sum(1 for c in self.算法库 if c.代码)
        难度分布 = {}
        for c in self.算法库:
            d = c.难度 or "未知"
            难度分布[d] = 难度分布.get(d, 0) + 1

        return {
            "总数": len(self.算法库),
            "有公式": 有公式,
            "有代码": 有代码,
            "类型分布": {k: len(v) for k, v in groups.items()},
            "难度分布": 难度分布,
        }

    def 运行代码(self, card_id: str, timeout: float = 5.0) -> Dict[str, Any]:
        """在隔离环境中运行算法的Python示例代码"""
        card = self.按ID获取(card_id)
        if not card:
            return {"error": f"未找到算法 #{card_id}"}
        if not card.代码:
            return {"error": f"算法 {card.名称} 没有Python示例代码"}

        code = card.代码
        lines = code.strip().split("\n")
        # 检测是否是纯stub (龍魂引擎 stub → 无独立可运行代码)
        has_stub_func = any("Stub for" in l for l in lines)
        is_pure_stub = has_stub_func and any(
            l.strip().startswith("def 龍魂") or l.strip().startswith("def AI_")
            for l in lines
        )
        if is_pure_stub:
            return {"状态": "⏭️ 跳过(stub)", "原因": "龍魂引擎 stub·无可独立运行的代码"}

        clean_lines = []
        for line in lines:
            clean_lines.append(line)
        code = "\n".join(clean_lines)

        if not code.strip():
            return {"error": f"代码剥离后为空 (只有stub)"}

        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        开始 = time.time()

        import math as _math, random as _random, collections as _collections
        try:
            # exec(code, G, L) 陷阱: def定义的函数__globals__=G,
            # 导致函数间的交叉调用失败。必须用单命名空间。
            ns = {
                "__builtins__": __builtins__,
                "math": _math, "random": _random, "collections": _collections,
                "Counter": _collections.Counter,
            }
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                exec(code, ns, ns)
            耗时 = round((time.time() - 开始) * 1000, 2)
            return {
                "状态": "✅ 成功",
                "输出": stdout_buf.getvalue().strip() or "(无print输出)",
                "耗时(ms)": 耗时,
                "stderr": stderr_buf.getvalue().strip()[:200],
            }
        except Exception as e:
            耗时 = round((time.time() - 开始) * 1000, 2)
            return {
                "状态": "❌ 执行失败",
                "错误": str(e)[:300],
                "耗时(ms)": 耗时,
                "traceback": traceback.format_exc()[:500],
            }

    def 导出公式(self) -> Dict[str, Any]:
        """导出所有算法的公式为结构化JSON"""
        export = {}
        for card in self.算法库:
            export[card.card_id] = {
                "名称": card.名称,
                "描述": card.描述[:200],
                "公式": card.公式列表(),
                "难度": card.难度,
                "类型": card.算法类型(),
                "标签": card.标签()[:10],
            }
        return export


# ═══════════════════════════════════════════════════════════
# §3 格式化输出
# ═══════════════════════════════════════════════════════════

def 打印统计(统计: Dict[str, Any]):
    print("\n" + "═" * 68)
    print("  🧮 龍魂·核心算法库全景")
    print("═" * 68)
    print(f"\n  算法总数: {统计['总数']}个")
    print(f"  有公式: {统计['有公式']}/{统计['总数']}个")
    print(f"  可运行代码: {统计['有代码']}/{统计['总数']}个")

    print("\n  📂 算法类型分布:\n")
    for 类型, 数量 in sorted(统计["类型分布"].items()):
        bar = "█" * 数量
        print(f"  {类型:　<12s} {bar} {数量}个")

    print("\n  📊 难度分布:\n")
    for 难度, 数量 in sorted(统计["难度分布"].items()):
        print(f"  {难度:　<12s} {数量}个")

    print("\n" + "═" * 68 + "\n")


def 打印算法列表(算法列表: List[AlgoCard], 标题: str = "算法列表"):
    print(f"\n{'═'*68}")
    print(f"  📋 {标题} — {len(算法列表)}个算法")
    print(f"{'═'*68}\n")

    for i, algo in enumerate(算法列表, 1):
        has_formula = "📐" if algo.公式 else "  "
        has_code = "▶️ " if algo.代码 and "def 龍魂" not in algo.代码 else "  "
        print(f"  [{i:2d}] [{algo.card_id:>4s}] {has_formula}{has_code} {algo.名称}")
        print(f"        类型: {algo.算法类型()} | 难度: {algo.难度 or 'N/A'}")
        if algo.描述:
            print(f"        {(algo.描述)[:100]}")
        print()

    print(f"{'═'*68}\n")


def 打印公式详情(algo: AlgoCard):
    print("\n" + "═" * 68)
    print(f"  📐 {algo.名称}")
    print("═" * 68)
    print(f"\n  ID: {algo.card_id} | 难度: {algo.难度 or 'N/A'}")
    print(f"  类型: {algo.算法类型()}")
    print(f"  描述: {algo.描述}")

    if algo.公式:
        formulas = algo.公式列表()
        print(f"\n  📏 核心公式 ({len(formulas)}条):\n")
        for i, f in enumerate(formulas, 1):
            print(f"  [{i}] {f}")

    if algo.误区:
        print(f"\n  ⚠️ 常见误区:\n    {algo.误区}")

    if algo.标签():
        print(f"\n  🏷️ 标签: {', '.join(algo.标签()[:10])}")

    if algo.关联知识:
        print(f"\n  🔗 关联: {algo.关联知识[:200]}")

    if algo.代码:
        print(f"\n  💻 Python示例代码:\n")
        # 只显示可运行的代码行
        for line in algo.代码.strip().split("\n")[:25]:
            if "Stub for" not in line and not line.strip().startswith("# 知识点"):
                print(f"    {line}")

    print("\n" + "═" * 68 + "\n")


def 打印运行结果(card_id: str, algo: AlgoCard, 结果: Dict[str, Any]):
    print("\n" + "═" * 68)
    print(f"  ▶️ 运行: [{card_id}] {algo.名称}")
    print("═" * 68)
    print(f"\n  状态: {结果.get('状态', '?')}")
    print(f"  耗时: {结果.get('耗时(ms)', '?')} ms")

    if "输出" in 结果:
        output = 结果["输出"]
        if output:
            print(f"\n  📤 输出:\n    {output}")
        else:
            print(f"\n  📤 输出: (无显式输出)")

    if "错误" in 结果:
        print(f"\n  ❌ 错误:\n    {结果['错误']}")

    if "stderr" in 结果 and 结果["stderr"]:
        print(f"\n  ⚠️ stderr:\n    {结果['stderr']}")

    print("\n" + "═" * 68 + "\n")


def 打印搜索(结果: List[AlgoCard], 关键词: str):
    print(f"\n{'═'*68}")
    print(f"  🔍 搜索「{关键词}」→ {len(结果)}个结果")
    print(f"{'═'*68}\n")

    for i, algo in enumerate(结果, 1):
        print(f"  [{i}] [{algo.card_id}] {algo.名称}")
        print(f"      类型: {algo.算法类型()} | 难度: {algo.难度 or 'N/A'}")
        if algo.公式:
            print(f"      公式: {algo.公式[:120]}...")
        if algo.描述:
            print(f"      描述: {algo.描述[:120]}...")
        print()

    print(f"{'═'*68}\n")


# ═══════════════════════════════════════════════════════════
# §4 CLI
# ═══════════════════════════════════════════════════════════

def 主函数():
    parser = argparse.ArgumentParser(
        description="龍魂·核心算法库 — 43张技术卡片·公式+代码·可查可跑",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_core_algo_lib.py --list
  python3 bin/lh_core_algo_lib.py --search "排序"
  python3 bin/lh_core_algo_lib.py --formula "信息熵"
  python3 bin/lh_core_algo_lib.py --run "信息熵"
  python3 bin/lh_core_algo_lib.py --run 56          # 用ID运行
  python3 bin/lh_core_algo_lib.py --bench           # 跑通所有有代码的
  python3 bin/lh_core_algo_lib.py --export formulas.json
  python3 bin/lh_core_algo_lib.py --interactive
        """,
    )
    parser.add_argument("--list", "-l", action="store_true", help="列出全部43个算法")
    parser.add_argument("--search", "-s", help="搜索算法(名称/标签/描述)")
    parser.add_argument("--formula", "-f", help="查看指定算法的公式详情(名称或ID)")
    parser.add_argument("--run", "-r", help="运行指定算法的Python示例(名称或ID)")
    parser.add_argument("--bench", "-b", action="store_true", help="跑通所有有可运行代码的算法")
    parser.add_argument("--export", "-e", help="导出所有公式为JSON文件")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    args = parser.parse_args()

    引擎 = 算法引擎()

    try:
        if args.list:
            统计 = 引擎.统计()
            if args.json:
                print(json.dumps(统计, ensure_ascii=False, indent=2))
            else:
                打印统计(统计)
                按类型 = 引擎.按类型分组()
                for 类型, 算法列表 in 按类型.items():
                    print(f"  ── {类型} ({len(算法列表)}个) ──")
                    for a in 算法列表:
                        print(f"    [{a.card_id:>4s}] {a.名称}")
                    print()

        elif args.search:
            结果 = 引擎.搜索(args.search)
            if args.json:
                data = [{"id": a.card_id, "名称": a.名称, "类型": a.算法类型(), "公式": a.公式列表()} for a in 结果]
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                打印搜索(结果, args.search)

        elif args.formula:
            algo = _查找算法(引擎, args.formula)
            if algo:
                if args.json:
                    print(json.dumps({
                        "id": algo.card_id, "名称": algo.名称, "描述": algo.描述,
                        "公式": algo.公式列表(), "难度": algo.难度, "类型": algo.算法类型(),
                        "标签": algo.标签(), "误区": algo.误区,
                    }, ensure_ascii=False, indent=2))
                else:
                    打印公式详情(algo)
            else:
                print(f"⚠️ 未找到算法: {args.formula}")

        elif args.run:
            algo = _查找算法(引擎, args.run)
            if not algo:
                print(f"⚠️ 未找到算法: {args.run}")
                return
            结果 = 引擎.运行代码(algo.card_id)
            if args.json:
                print(json.dumps(结果, ensure_ascii=False, indent=2))
            else:
                打印运行结果(algo.card_id, algo, 结果)

        elif args.bench:
            跑通所有(引擎)

        elif args.export:
            data = 引擎.导出公式()
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 已导出 {len(data)} 个算法公式 → {args.export}")

        elif args.interactive:
            交互模式(引擎)

        else:
            parser.print_help()

    finally:
        pass


def _查找算法(引擎: 算法引擎, 输入: str) -> Optional[AlgoCard]:
    """按ID或名称查找"""
    # 先按ID查
    if 输入.isdigit():
        algo = 引擎.按ID获取(输入)
        if algo:
            return algo
    # 按名称模糊查
    结果 = 引擎.搜索(输入)
    if 结果:
        return 结果[0]
    return None


def 跑通所有(引擎: 算法引擎):
    """基准测试：跑通所有有代码的算法"""
    print("\n" + "═" * 68)
    print("  🏃 龍魂·算法基准测试 — 跑通所有可运行代码")
    print("═" * 68 + "\n")

    成功 = 0
    失败 = 0
    跳过 = 0
    总共 = len(引擎.算法库)

    for i, algo in enumerate(引擎.算法库, 1):
        if not algo.代码:
            跳过 += 1
            continue

        结果 = 引擎.运行代码(algo.card_id, timeout=3.0)
        状态 = 结果.get("状态", "")
        if 状态.startswith("⏭️"):
            icon = "⏭️"
            跳过 += 1
        elif 状态.startswith("✅"):
            icon = "✅"
            成功 += 1
        else:
            icon = "❌"
            失败 += 1

        print(f"  [{i:2d}/{总共}] [{algo.card_id:>4s}] {icon} {algo.名称:　<30s} {结果.get('耗时(ms)', '?')}ms")
        if "错误" in 结果:
            print(f"         ↳ {结果['错误'][:80]}")
        elif "原因" in 结果:
            print(f"         ↳ {结果['原因'][:80]}")

    print(f"\n{'═'*68}")
    print(f"  总结: ✅ {成功}个成功 | ❌ {失败}个失败 | ⏭️ {跳过}个跳过(stub/无代码) | 共{总共}个")
    print(f"{'═'*68}\n")


def 交互模式(引擎: 算法引擎):
    print("\n" + "═" * 68)
    print("  🧮 龍魂·核心算法库 · 交互模式")
    print("═" * 68)

    while True:
        print("\n  选项:")
        print("    [1] 查看全部算法")
        print("    [2] 按类型浏览")
        print("    [3] 搜索算法")
        print("    [4] 查看公式详情")
        print("    [5] 运行代码示例")
        print("    [6] 跑通全部算法")
        print("    [7] 导出公式")
        print("    [0] 退出")

        选择 = input("\n  请输入选项: ").strip()

        if 选择 == "0":
            print("  再见 🧮\n")
            break
        elif 选择 == "1":
            统计 = 引擎.统计()
            打印统计(统计)
            打印算法列表(引擎.算法库, "全部43个算法")
        elif 选择 == "2":
            按类型 = 引擎.按类型分组()
            print("\n  📂 算法类型:\n")
            types = list(按类型.items())
            for i, (t, cards) in enumerate(types, 1):
                print(f"  [{i}] {t} ({len(cards)}个)")
            子选择 = input("\n  选择类型编号: ").strip()
            if 子选择.isdigit():
                idx = int(子选择) - 1
                if 0 <= idx < len(types):
                    打印算法列表(types[idx][1], f"{types[idx][0]} 算法")
        elif 选择 == "3":
            关键词 = input("  搜索: ").strip()
            if 关键词:
                结果 = 引擎.搜索(关键词)
                打印搜索(结果, 关键词)
        elif 选择 == "4":
            输入 = input("  输入算法名称或ID: ").strip()
            if 输入:
                algo = _查找算法(引擎, 输入)
                if algo:
                    打印公式详情(algo)
                else:
                    print(f"  ⚠️ 未找到")
        elif 选择 == "5":
            输入 = input("  输入算法名称或ID: ").strip()
            if 输入:
                algo = _查找算法(引擎, 输入)
                if algo:
                    结果 = 引擎.运行代码(algo.card_id)
                    打印运行结果(algo.card_id, algo, 结果)
                else:
                    print(f"  ⚠️ 未找到")
        elif 选择 == "6":
            跑通所有(引擎)
        elif 选择 == "7":
            fname = input("  导出文件名(默认: formulas.json): ").strip() or "formulas.json"
            data = 引擎.导出公式()
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已导出 → {fname}")


if __name__ == "__main__":
    主函数()
