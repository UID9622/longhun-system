# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_PATH_VISUALIZE-v1.0-1c46eb96
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂翻译引擎 · 1650万路径3D可视化协议 v1.0
龍魂系统 · 视觉路由层
UID9622 | 龍芯北辰 | 2026-07-18
DNA锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能:
    1. 六维空间投影到3D（XYZ三轴）
    2. 龍魂五行配色（金/木/水/火/土）
    3. 三色审计透明度（🟢通行/🟡待审/🔴熔断）
    4. 路径轨迹动画（从输入到节点的流动）
    5. 交互式旋转/缩放/点击查询
    6. DNA签章水印（所有输出嵌入UID）

依赖:
    pip install matplotlib numpy

用法:
    python3 lh_path_visualize.py --mode full    # 全量渲染（1650万点，慢）
    python3 lh_path_visualize.py --mode sample 10000  # 采样1万点（快）
    python3 lh_path_visualize.py --mode trace "测试文本"  # 单条路径追踪
"""

import os
import sys
import json
import math
import random
import argparse
import hashlib
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import numpy as np

# 尝试导入matplotlib，如果失败则生成静态数据
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.patches import FancyBboxPatch
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ matplotlib未安装，将生成静态JSON数据")

# ═══════════════════════════════════════════════════════════════
# P0 焊死底座
# ═══════════════════════════════════════════════════════════════
P0_ANCHOR = {
    "uid": "9622",
    "creator": "龍芯北辰",
    "dna": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
}

# ═══════════════════════════════════════════════════════════════
# 龍魂视觉常量
# ═══════════════════════════════════════════════════════════════

# 五行配色（RGB 0-1）
WUXING_COLORS = {
    "金": (1.0, 0.84, 0.0),      # 金色 #FFD700
    "木": (0.13, 0.55, 0.13),     # 青绿 #228B22
    "水": (0.0, 0.0, 0.55),       # 深蓝 #00008B
    "火": (0.89, 0.15, 0.21),     # 朱红 #E32636
    "土": (0.85, 0.65, 0.13),     # 土黄 #DAA520
}

# 三色审计透明度
AUDIT_ALPHA = {
    "🟢": 1.0,    # 通行 - 完全不透明
    "🟡": 0.45,   # 待审 - 半透明
    "🔴": 0.15,   # 熔断 - 几乎透明
}

# 三才权重
SANCAI_WEIGHTS = {"天": 0.35, "地": 0.15, "人": 0.50}

# 数字根→五行映射
DR_WUXING = {
    0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
    5: "土", 6: "水", 7: "火", 8: "木", 9: "金"
}

# 数字根→三色审计
DR_AUDIT = {
    3: "🔴", 9: "🔴",  # 熔断
    6: "🟡",           # 待审
}

# ═══════════════════════════════════════════════════════════════
# 六维空间引擎
# ═══════════════════════════════════════════════════════════════

@dataclass
class PathNode:
    """路径节点"""
    d: int      # 数字根 (0-5)
    l: int      # 洛书 (0-8)
    b: int      # 八卦 (0-7)
    g: int      # 64卦 (0-63)
    w: int      # 五行 (0-4)
    tg: int     # 干支 (0-119)

    # 派生属性
    path_id: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    color: Tuple[float, float, float] = (0.5, 0.5, 0.5)
    alpha: float = 1.0
    size: float = 10.0
    wuxing: str = ""
    audit: str = "🟢"

    def __post_init__(self):
        self._compute_derived()

    def _compute_derived(self):
        """计算派生属性"""
        # 数字根真实值
        dr_values = [0, 1, 2, 3, 4, 5]  # 简化映射
        dr = dr_values[self.d] if self.d < len(dr_values) else 0

        # 五行
        self.wuxing = DR_WUXING.get(dr, "土")
        self.color = WUXING_COLORS[self.wuxing]

        # 三色审计
        self.audit = DR_AUDIT.get(dr, "🟢")
        self.alpha = AUDIT_ALPHA[self.audit]

        # 3D投影坐标
        # X轴: 数字根(6) × 洛书(9) = 54
        self.x = self.d * 9 + self.l
        # Y轴: 八卦(8) × 64卦(64) = 512
        self.y = self.b * 64 + self.g
        # Z轴: 五行(5) × 干支(120) = 600
        self.z = self.w * 120 + self.tg

        # PathID
        self.path_id = (
            self.d * 9 * 8 * 64 * 5 * 120 +
            self.l * 8 * 64 * 5 * 120 +
            self.b * 64 * 5 * 120 +
            self.g * 5 * 120 +
            self.w * 120 +
            self.tg
        )

        # 点大小（根据三才权重调整）
        human_weight = SANCAI_WEIGHTS["人"]
        self.size = 10 + human_weight * 20  # 10-30


class LongHunPathEngine:
    """龍魂路径引擎"""

    TOTAL_PATHS = 16_588_800

    def __init__(self):
        self.nodes: List[PathNode] = []

    def generate_sample(self, n: int = 10000, seed: int = 9622) -> List[PathNode]:
        """
        采样生成路径节点
        使用确定性随机，保证可复现
        """
        random.seed(seed)
        np.random.seed(seed)

        nodes = []
        for _ in range(n):
            d = random.randint(0, 5)
            l = random.randint(0, 8)
            b = random.randint(0, 7)
            g = random.randint(0, 63)
            w = random.randint(0, 4)
            tg = random.randint(0, 119)

            node = PathNode(d=d, l=l, b=b, g=g, w=w, tg=tg)
            nodes.append(node)

        self.nodes = nodes
        return nodes

    def trace_path(self, text: str) -> PathNode:
        """
        追踪单条文本的路径
        """
        # 计算数字根
        digits = [int(c) for c in text if c.isdigit()]
        if not digits:
            dr = 0
        else:
            n = sum(digits)
            while n >= 10:
                n = sum(int(c) for c in str(n))
            dr = n

        # 映射到六维
        d = min(dr, 5)  # 0-5
        l = hash(text) % 9
        b = hash(text + "bagua") % 8
        g = hash(text + "64gua") % 64
        w = min(dr, 4)  # 0-4
        tg = hash(text + "tiangan") % 120

        return PathNode(d=d, l=l, b=b, g=g, w=w, tg=tg)

    def get_stats(self) -> Dict:
        """获取路径统计"""
        if not self.nodes:
            return {}

        stats = {
            "total_nodes": len(self.nodes),
            "wuxing_distribution": {},
            "audit_distribution": {},
            "x_range": (min(n.x for n in self.nodes), max(n.x for n in self.nodes)),
            "y_range": (min(n.y for n in self.nodes), max(n.y for n in self.nodes)),
            "z_range": (min(n.z for n in self.nodes), max(n.z for n in self.nodes)),
        }

        for node in self.nodes:
            stats["wuxing_distribution"][node.wuxing] = stats["wuxing_distribution"].get(node.wuxing, 0) + 1
            stats["audit_distribution"][node.audit] = stats["audit_distribution"].get(node.audit, 0) + 1

        return stats


# ═══════════════════════════════════════════════════════════════
# 3D可视化渲染器
# ═══════════════════════════════════════════════════════════════

class LongHunVisualizer:
    """龍魂3D可视化渲染器"""

    def __init__(self, engine: LongHunPathEngine):
        self.engine = engine
        self.fig = None
        self.ax = None

    def render_3d(self, title: str = "龍魂翻译引擎 · 1650万路径宇宙"):
        """渲染3D散点图"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ matplotlib未安装，无法渲染")
            return

        nodes = self.engine.nodes
        if not nodes:
            print("❌ 无节点数据")
            return

        # 创建图形
        self.fig = plt.figure(figsize=(16, 12), dpi=100)
        self.fig.patch.set_facecolor('#0a0a0a')  # 黑色背景

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0a0a0a')

        # 提取坐标
        xs = [n.x for n in nodes]
        ys = [n.y for n in nodes]
        zs = [n.z for n in nodes]
        colors = [n.color for n in nodes]
        alphas = [n.alpha for n in nodes]
        sizes = [n.size for n in nodes]

        # 按透明度分组渲染（避免重叠问题）
        # 🟢 通行节点
        green_nodes = [n for n in nodes if n.audit == "🟢"]
        if green_nodes:
            self._render_group(green_nodes, "🟢 通行", 1.0)

        # 🟡 待审节点
        yellow_nodes = [n for n in nodes if n.audit == "🟡"]
        if yellow_nodes:
            self._render_group(yellow_nodes, "🟡 待审", 0.45)

        # 🔴 熔断节点
        red_nodes = [n for n in nodes if n.audit == "🔴"]
        if red_nodes:
            self._render_group(red_nodes, "🔴 熔断", 0.15)

        # 设置坐标轴
        self.ax.set_xlabel('X: 数字根×洛书 (54)', color='white', fontsize=12)
        self.ax.set_ylabel('Y: 八卦×64卦 (512)', color='white', fontsize=12)
        self.ax.set_zlabel('Z: 五行×干支 (600)', color='white', fontsize=12)

        # 设置标题
        self.ax.set_title(
            f'{title}\n采样: {len(nodes):,} / 16,588,800 路径',
            color='gold', fontsize=14, fontweight='bold', pad=20
        )

        # 设置刻度颜色
        self.ax.tick_params(colors='white')

        # 添加网格
        self.ax.grid(True, alpha=0.2, color='gray')

        # 添加龍魂水印
        self.fig.text(
            0.5, 0.02,
            f'UID9622 | 龍芯北辰 | {P0_ANCHOR["dna"]}',
            color='gray', fontsize=8, ha='center'
        )

        # 添加图例
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=WUXING_COLORS["金"], 
                   markersize=8, label='金·规则', alpha=0.8),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=WUXING_COLORS["木"], 
                   markersize=8, label='木·创新', alpha=0.8),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=WUXING_COLORS["水"], 
                   markersize=8, label='水·记忆', alpha=0.8),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=WUXING_COLORS["火"], 
                   markersize=8, label='火·文明', alpha=0.8),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=WUXING_COLORS["土"], 
                   markersize=8, label='土·普惠', alpha=0.8),
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', 
                      facecolor='black', edgecolor='gold', labelcolor='white')

        plt.tight_layout()

    def _render_group(self, nodes: List[PathNode], label: str, alpha_mult: float):
        """渲染一组节点"""
        xs = [n.x for n in nodes]
        ys = [n.y for n in nodes]
        zs = [n.z for n in nodes]
        colors = [n.color for n in nodes]
        sizes = [n.size for n in nodes]

        self.ax.scatter(
            xs, ys, zs,
            c=colors,
            s=sizes,
            alpha=alpha_mult,
            edgecolors='none',
            label=label
        )

    def render_trace(self, text: str):
        """渲染单条路径追踪"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ matplotlib未安装")
            return

        node = self.engine.trace_path(text)

        self.fig = plt.figure(figsize=(14, 10), dpi=100)
        self.fig.patch.set_facecolor('#0a0a0a')

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0a0a0a')

        # 渲染背景采样点（淡化）
        if self.engine.nodes:
            bg_xs = [n.x for n in self.engine.nodes[:1000]]
            bg_ys = [n.y for n in self.engine.nodes[:1000]]
            bg_zs = [n.z for n in self.engine.nodes[:1000]]
            self.ax.scatter(bg_xs, bg_ys, bg_zs, c='gray', s=2, alpha=0.1)

        # 渲染路径轨迹（从原点到节点）
        self.ax.plot(
            [0, node.x], [0, node.y], [0, node.z],
            color='gold', linewidth=2, alpha=0.8, linestyle='--'
        )

        # 渲染目标节点（高亮）
        self.ax.scatter(
            [node.x], [node.y], [node.z],
            c=[node.color],
            s=[200],
            alpha=1.0,
            edgecolors='gold',
            linewidths=2
        )

        # 添加标注
        self.ax.text(
            node.x, node.y, node.z,
            f'  PathID: {node.path_id}\n  五行: {node.wuxing}\n  审计: {node.audit}',
            color='white', fontsize=10
        )

        # 设置坐标轴
        self.ax.set_xlabel('X: 数字根×洛书', color='white')
        self.ax.set_ylabel('Y: 八卦×64卦', color='white')
        self.ax.set_zlabel('Z: 五行×干支', color='white')
        self.ax.set_title(
            f'路径追踪: "{text[:30]}..."\nPathID: {node.path_id}',
            color='gold', fontsize=14
        )
        self.ax.tick_params(colors='white')

        # 水印
        self.fig.text(
            0.5, 0.02,
            f'UID9622 | 龍芯北辰 | {P0_ANCHOR["dna"]}',
            color='gray', fontsize=8, ha='center'
        )

        plt.tight_layout()

    def save(self, filepath: str):
        """保存图片"""
        if self.fig:
            self.fig.savefig(filepath, dpi=150, bbox_inches='tight',
                           facecolor='#0a0a0a', edgecolor='none')
            print(f"💾 已保存: {filepath}")

    def show(self):
        """显示图形"""
        if self.fig:
            plt.show()


# ═══════════════════════════════════════════════════════════════
# 静态数据导出器（无matplotlib时使用）
# ═══════════════════════════════════════════════════════════════
class StaticExporter:
    """静态数据导出器"""

    def export_json(self, nodes: List[PathNode], filepath: str):
        """导出JSON格式"""
        data = []
        for n in nodes[:10000]:  # 限制1万条
            data.append({
                "path_id": n.path_id,
                "x": n.x, "y": n.y, "z": n.z,
                "color": n.color,
                "alpha": n.alpha,
                "wuxing": n.wuxing,
                "audit": n.audit,
                "digital_root": [0,1,2,3,4,5][n.d] if n.d < 6 else 0,
            })

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 已导出JSON: {filepath} ({len(data)} 条)")

    def export_csv(self, nodes: List[PathNode], filepath: str):
        """导出CSV格式"""
        import csv

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['path_id', 'x', 'y', 'z', 'wuxing', 'audit', 'alpha'])

            for n in nodes[:10000]:
                writer.writerow([
                    n.path_id, n.x, n.y, n.z,
                    n.wuxing, n.audit, n.alpha
                ])

        print(f"💾 已导出CSV: {filepath} ({min(len(nodes), 10000)} 条)")


# ═══════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="龍魂翻译引擎 · 1650万路径3D可视化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 采样1万点渲染
  python3 lh_path_visualize.py --mode sample --count 10000 --output longhun_universe.png

  # 追踪单条路径
  python3 lh_path_visualize.py --mode trace --text "龍魂系统测试" --output trace.png

  # 导出静态数据（无matplotlib时使用）
  python3 lh_path_visualize.py --mode export --format json --output paths.json
        """
    )

    parser.add_argument("--mode", type=str, required=True,
                       choices=["sample", "trace", "export"],
                       help="运行模式")
    parser.add_argument("--count", type=int, default=10000,
                       help="采样数量（sample模式）")
    parser.add_argument("--text", type=str, default="龍魂系统",
                       help="追踪文本（trace模式）")
    parser.add_argument("--format", type=str, default="json",
                       choices=["json", "csv"],
                       help="导出格式（export模式）")
    parser.add_argument("--output", type=str, default="longhun_visual.png",
                       help="输出文件路径")
    parser.add_argument("--dna-verify", type=str, default="LK9X-772Z",
                       help="DNA验证码")

    args = parser.parse_args()

    # DNA验证
    if args.dna_verify != P0_ANCHOR["confirm"].split("🧬")[-1]:
        print("❌ DNA验证失败")
        sys.exit(1)

    # 创建引擎
    engine = LongHunPathEngine()

    if args.mode == "sample":
        print(f"🐉 生成 {args.count:,} 个采样节点...")
        engine.generate_sample(args.count)

        stats = engine.get_stats()
        print(f"   五行分布: {stats.get('wuxing_distribution', {})}")
        print(f"   审计分布: {stats.get('audit_distribution', {})}")

        if MATPLOTLIB_AVAILABLE:
            viz = LongHunVisualizer(engine)
            viz.render_3d()
            viz.save(args.output)
            viz.show()
        else:
            print("⚠️ matplotlib未安装，使用静态导出")
            exporter = StaticExporter()
            exporter.export_json(engine.nodes, args.output.replace('.png', '.json'))

    elif args.mode == "trace":
        print(f'🐉 追踪路径: "{args.text}"')
        node = engine.trace_path(args.text)

        print(f"   PathID: {node.path_id}")
        print(f"   坐标: ({node.x}, {node.y}, {node.z})")
        print(f"   五行: {node.wuxing}")
        print(f"   审计: {node.audit}")

        # 生成背景采样
        engine.generate_sample(5000)

        if MATPLOTLIB_AVAILABLE:
            viz = LongHunVisualizer(engine)
            viz.render_trace(args.text)
            viz.save(args.output)
            viz.show()
        else:
            print("⚠️ matplotlib未安装")

    elif args.mode == "export":
        print(f"🐉 生成采样数据...")
        engine.generate_sample(10000)

        exporter = StaticExporter()
        if args.format == "json":
            exporter.export_json(engine.nodes, args.output)
        else:
            exporter.export_csv(engine.nodes, args.output)


if __name__ == "__main__":
    main()
