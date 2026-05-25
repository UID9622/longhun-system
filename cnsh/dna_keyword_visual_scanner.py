#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·DNA关键字双视觉扫描脚本 v1.0
DNA Keyword Visual Scanner: 本地关键字DNA提取与双视角展示

DNA: #龍芯⚡️2026-05-25-DNA-KEYWORD-VISUAL-SCANNER-v1.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

设计：
1️⃣ DNA关键字提取 - 从关键字获取完整DNA+指标
2️⃣ 双视觉协议 - 微观视角(单字) + 宏观视角(聚合)
3️⃣ 本地表格展示 - 纯文本ASCII艺术展示

本地计算·永不外送·纯数学·零ML依赖

理论指导: 曾仕强老师（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承

用法:
    python3 dna_keyword_visual_scanner.py "关键字1" "关键字2" "关键字3"
    python3 dna_keyword_visual_scanner.py --batch keywords.txt
    python3 dna_keyword_visual_scanner.py --demo
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))

from cnsh_keyword_extraction import KeywordExtractionEngine


@dataclass
class DNAVisualReport:
    """DNA视觉报告"""
    keywords: List[str]
    vectors: List[Any]

    def render_dna_table(self) -> str:
        """DNA信息表（微观视角）"""
        lines = []
        lines.append("\n" + "="*120)
        lines.append("📊 DNA关键字功能表（微观视角·逐个扫描）")
        lines.append("="*120)

        # 表头
        header = "| # | 关键字 | DNA | dr | 五行 | 宫位 | 369频 | 太极 | 强度 | 中心共 | 卦位 |"
        lines.append(header)
        lines.append("|" + "-"*118 + "|")

        # 数据行
        for i, (kw, v) in enumerate(zip(self.keywords, self.vectors), 1):
            dr = v.digital_root
            wuxing = v.wuxing.value[0]
            pos = v.luoshu_position
            freq = v.frequency_369.name[:6]
            taichi = f"{v.taichi_phase:.2f}"
            strength = f"{v.keyword_strength:.2f}"
            resonance = f"{v.resonance_with_center:.2f}"
            gua = f"{v.gua64_code:02d}"
            dna_short = v.dna[-16:]  # 后16字符

            row = f"| {i} | {kw:6s} | {dna_short} | {dr} | {wuxing:2s} | {pos}宫 | {freq:6s} | {taichi} | {strength} | {resonance} | {gua} |"
            lines.append(row)

        lines.append("="*120 + "\n")
        return "\n".join(lines)

    def render_aggregate_view(self) -> str:
        """聚合视图（宏观视角）"""
        lines = []
        lines.append("="*120)
        lines.append("🔍 聚合视图（宏观视角·集合分析）")
        lines.append("="*120 + "\n")

        # 五行分布
        lines.append("【五行分布】")
        wuxing_list = [v.wuxing for v in self.vectors]
        wuxing_counter = Counter(wuxing_list)
        wuxing_map = {
            "木": "🌳生长",
            "火": "🔥燃烧",
            "土": "🪨承载",
            "金": "⚒️ 收敛",
            "水": "💧流动"
        }

        for wuxing, count in wuxing_counter.most_common():
            symbol = wuxing.value[0]
            desc = wuxing_map.get(symbol, symbol)
            bar = "█" * count
            percent = count / len(self.vectors) * 100
            lines.append(f"  {desc:8s}: {bar} x{count} ({percent:.1f}%)")

        # 宫位分布
        lines.append("\n【宫位分布（河图洛书）】")
        palace_map = {1:"坎北", 2:"坤SW", 3:"震东", 4:"巽SE", 5:"中", 6:"乾NW", 7:"兑西", 8:"艮NE", 9:"离南"}
        luoshu_counter = Counter([v.luoshu_position for v in self.vectors])

        for pos in sorted(luoshu_counter.keys()):
            count = luoshu_counter[pos]
            palace_name = palace_map.get(pos, "?")
            bar = "◆" * count
            percent = count / len(self.vectors) * 100
            lines.append(f"  第{pos}宫({palace_name}): {bar} x{count} ({percent:.1f}%)")

        # 369频率分布
        lines.append("\n【369频率分布】")
        freq_counter = Counter([v.frequency_369.name for v in self.vectors])

        for freq, count in freq_counter.most_common():
            bar = "●" * count
            percent = count / len(self.vectors) * 100
            lines.append(f"  {freq:10s}: {bar} x{count} ({percent:.1f}%)")

        # 数字根分布
        lines.append("\n【数字根分布】")
        dr_counter = Counter([v.digital_root for v in self.vectors])

        for dr in sorted(dr_counter.keys()):
            count = dr_counter[dr]
            bar = "◎" * count
            percent = count / len(self.vectors) * 100
            lines.append(f"  dr={dr}: {bar} x{count} ({percent:.1f}%)")

        # 统计信息
        lines.append("\n【统计指标】")
        avg_strength = sum(v.keyword_strength for v in self.vectors) / len(self.vectors)
        avg_resonance = sum(v.resonance_with_center for v in self.vectors) / len(self.vectors)
        avg_taichi = sum(v.taichi_phase for v in self.vectors) / len(self.vectors)
        harmony = self._calculate_harmony()

        lines.append(f"  关键字总数: {len(self.vectors)}")
        lines.append(f"  平均强度: {avg_strength:.3f}/1.0")
        lines.append(f"  平均中心共振: {avg_resonance:.3f}/1.0")
        lines.append(f"  平均太极相位: {avg_taichi:.3f} ({'阳主' if avg_taichi > 0.5 else '阴主' if avg_taichi < 0.5 else '平衡'})")
        lines.append(f"  组合和谐度: {harmony:.3f}/1.0")

        lines.append("\n" + "="*120 + "\n")
        return "\n".join(lines)

    def _calculate_harmony(self) -> float:
        """计算和谐度"""
        if not self.vectors:
            return 0.0

        # 方差越小和谐度越高
        avg_dr = sum(v.digital_root for v in self.vectors) / len(self.vectors)
        variance = sum((v.digital_root - avg_dr) ** 2 for v in self.vectors) / len(self.vectors)
        harmony = 1.0 - min(variance ** 0.5 / 5.0, 1.0)
        return max(0.0, harmony)

    def render_dna_chain(self) -> str:
        """DNA链追踪"""
        lines = []
        lines.append("\n" + "="*120)
        lines.append("🔗 DNA链追踪（可追溯性）")
        lines.append("="*120)

        for i, (kw, v) in enumerate(zip(self.keywords, self.vectors), 1):
            lines.append(f"\n{i}. 【{kw}】")
            lines.append(f"   DNA: {v.dna}")
            lines.append(f"   数字根: dr={v.digital_root} | 五行: {v.wuxing.value[0]} | 宫位: 第{v.luoshu_position}宫 | 强度: {v.keyword_strength:.2f}")

        lines.append("\n" + "="*120 + "\n")
        return "\n".join(lines)

    def render_full_report(self) -> str:
        """生成完整报告"""
        report = ""
        report += self.render_dna_table()
        report += self.render_aggregate_view()
        report += self.render_dna_chain()
        return report


class DNAKeywordVisualScanner:
    """DNA关键字双视觉扫描器"""

    def __init__(self):
        self.engine = KeywordExtractionEngine()

    def scan_keywords(self, keywords: List[str]) -> DNAVisualReport:
        """扫描关键字组"""
        vectors = []
        valid_keywords = []

        for kw in keywords:
            try:
                v = self.engine.extract_keyword(kw)
                vectors.append(v)
                valid_keywords.append(kw)
            except Exception as e:
                print(f"⚠️  关键字'{kw}'解析失败: {e}")

        return DNAVisualReport(keywords=valid_keywords, vectors=vectors)

    def scan_batch_file(self, filepath: str) -> DNAVisualReport:
        """批量扫描文件"""
        keywords = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                kw = line.strip()
                if kw and not kw.startswith('#'):
                    keywords.append(kw)

        return self.scan_keywords(keywords)


def demo():
    """演示模式"""
    print("\n" + "="*120)
    print("🐉 龍魂·DNA关键字双视觉扫描脚本 v1.0")
    print("="*120)
    print("\n📍 演示模式：扫描v2.5可能方向的关键字\n")

    demo_keywords = [
        "语义",      # 协议层
        "语法",      # 协议层
        "翻译",      # 派生
        "规则",      # 派生
        "生长",      # 木系
        "承载",      # 土系
    ]

    scanner = DNAKeywordVisualScanner()
    report = scanner.scan_keywords(demo_keywords)

    print(report.render_full_report())

    print("✅ 演示扫描完成")
    print("🐉 龍魂 · DNA·双视觉·本地分析 · UID9622不免责\n")


def main():
    """主程序"""
    print("\n" + "="*120)
    print("🐉 龍魂·DNA关键字双视觉扫描脚本 v1.0")
    print("="*120)

    scanner = DNAKeywordVisualScanner()

    # 命令行参数处理
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            demo()
        elif sys.argv[1] == "--batch" and len(sys.argv) > 2:
            filepath = sys.argv[2]
            print(f"\n📂 批量扫描文件: {filepath}\n")
            report = scanner.scan_batch_file(filepath)
            print(report.render_full_report())
        else:
            # 直接扫描命令行关键字
            keywords = sys.argv[1:]
            print(f"\n🔍 扫描关键字: {', '.join(keywords)}\n")
            report = scanner.scan_keywords(keywords)
            print(report.render_full_report())
    else:
        # 交互模式
        print("\n💬 交互模式（输入关键字，空行结束）\n")
        keywords = []

        while True:
            try:
                kw = input("输入关键字: ").strip()
                if not kw:
                    if keywords:
                        break
                    else:
                        print("请输入至少一个关键字")
                        continue
                keywords.append(kw)
            except KeyboardInterrupt:
                print("\n\n已取消")
                sys.exit(0)

        print(f"\n🔍 扫描关键字: {', '.join(keywords)}\n")
        report = scanner.scan_keywords(keywords)
        print(report.render_full_report())


if __name__ == "__main__":
    main()
