#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂蚁群分布可视化引擎 v1.0
============================
蚁后-工蚁拓扑图·信息素热力图·涌现仪表盘·八卦门控图。
对接 lh_ant_colony_daemon.py / orchestrator / router / 8gate。

DNA: #龍芯⚡️丙午·癸未·丁未-蚁群可视化引擎-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 engines/lh_ant_colony_visual.py topo --output ant_topo.png
  python3 engines/lh_ant_colony_visual.py heatmap --output ant_heat.png
  python3 engines/lh_ant_colony_visual.py dashboard --output ant_dash.png
  python3 engines/lh_ant_colony_visual.py full --output-dir ant_viz/
  python3 engines/lh_ant_colony_visual.py narrate  # 输出解说词

依赖: pillow numpy
"""

import argparse, json, math, os, sys, textwrap
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
    PIL_OK = True
except ImportError:
    PIL_OK = False
    print("[WARN] pillow 未安装: pip install pillow", file=sys.stderr)

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False

# ─── 常量 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·癸未·丁未-蚁群可视化-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ─── 龍魂色板（焊死） ───
BLACK = (8, 8, 8)
DARK = (20, 20, 20)
GOLD = (201, 168, 76)
LIGHT_GOLD = (230, 200, 120)
WHITE = (220, 220, 220)
RED = (196, 30, 58)
ORANGE = (212, 160, 23)
GREEN = (80, 200, 120)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# 蚁群族群颜色
COLONY_COLORS = [
    (201, 168, 76),   # 金
    (100, 180, 220),  # 蓝
    (180, 120, 200),  # 紫
    (80, 200, 150),   # 绿
    (220, 150, 100),  # 橙
    (150, 150, 220),  # 淡紫
    (100, 200, 200),  # 青
    (220, 180, 120),  # 暖金
    (180, 100, 140),  # 粉
    (120, 180, 100),  # 草绿
    (200, 150, 180),  # 淡粉
    (140, 160, 200),  # 灰蓝
]

# 信息素热力色
HEAT_COLORS = [
    (10, 10, 30),     # 深黑蓝（无信息素）
    (20, 30, 80),     # 深蓝
    (50, 80, 160),    # 蓝
    (100, 150, 200),  # 青
    (180, 180, 80),   # 黄
    (201, 168, 76),   # 金
    (220, 100, 40),   # 橙
    (200, 30, 30),    # 红（最高浓度）
]


def _load_font(size: int):
    """加载字体，优雅降级"""
    font_paths = [
        str(PROJECT_ROOT / "longhun-font" / "fonts" / "NotoSansSC-Regular.ttf"),
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ═══════════════════════════════════════════════════════════════════
# 1. 蚁后-工蚁分布拓扑图
# ═══════════════════════════════════════════════════════════════════

def generate_topology(
    output_path: str = "ant_topology.png",
    width: int = 1920,
    height: int = 1080,
    data: Optional[Dict] = None,
) -> str:
    """生成蚁后-工蚁分布拓扑图"""
    if not PIL_OK:
        raise ImportError("需要 pillow")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    font_title = _load_font(32)
    font_node = _load_font(14)
    font_label = _load_font(12)

    # 默认数据
    if data is None:
        data = {
            "queen": {"health": 92, "status": "活跃", "tasks_pending": 3},
            "colonies": [
                {"name": "视觉蚁群", "active_ants": 8, "health": 95, "tasks": 12},
                {"name": "安全蚁群", "active_ants": 6, "health": 88, "tasks": 5},
                {"name": "数据蚁群", "active_ants": 10, "health": 97, "tasks": 20},
                {"name": "审计蚁群", "active_ants": 4, "health": 100, "tasks": 3},
                {"name": "部署蚁群", "active_ants": 5, "health": 90, "tasks": 7},
                {"name": "知识蚁群", "active_ants": 7, "health": 93, "tasks": 15},
                {"name": "搜索蚁群", "active_ants": 3, "health": 85, "tasks": 2},
                {"name": "训练蚁群", "active_ants": 2, "health": 80, "tasks": 1},
                {"name": "监控蚁群", "active_ants": 4, "health": 98, "tasks": 0},
                {"name": "同步蚁群", "active_ants": 3, "health": 91, "tasks": 4},
                {"name": "集成蚁群", "active_ants": 6, "health": 87, "tasks": 9},
                {"name": "路由蚁群", "active_ants": 5, "health": 94, "tasks": 6},
            ],
            "pheromone": {"density": 0.62, "evaporation_rate": 0.05, "emergence_index": 0.58},
        }

    # 标题
    draw.text((40, 20), "🐜 龍魂蚁群分布拓扑图", fill=GOLD, font=font_title)
    draw.text((40, 60), f"蚁后健康: {data['queen']['health']}分 | "
              f"累计工蚁: {sum(c['active_ants'] for c in data['colonies'])} | "
              f"信息素密度: {data['pheromone']['density']:.0%} | "
              f"涌现指数: {data['pheromone']['emergence_index']:.2f}",
              fill=LIGHT_GOLD, font=font_label)

    # 蚁后（居中偏上）
    cx, cy = width // 2, 180
    queen_r = 45
    queen_color = _health_color(data['queen']['health'])
    # 外圈辉光
    for r in range(queen_r + 15, queen_r, -3):
        alpha = int(40 * (r - queen_r) / 15)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*GOLD[:3], alpha) if PIL_OK else GOLD)
    draw.ellipse([cx-queen_r, cy-queen_r, cx+queen_r, cy+queen_r], fill=queen_color, outline=GOLD, width=2)
    draw.text((cx-20, cy-8), "蚁后", fill=WHITE, font=font_node)
    draw.text((cx-40, cy+20), f"健康{data['queen']['health']}",
              fill=LIGHT_GOLD, font=font_label)

    # 12个工蚁群排列
    colonies = data['colonies'][:12]
    n = len(colonies)
    ring_r = 250
    for i, col in enumerate(colonies):
        angle = (i / n) * 2 * math.pi - math.pi / 2
        nx = cx + ring_r * math.cos(angle)
        ny = cy + 120 + ring_r * math.sin(angle) * 0.7  # 椭圆压扁

        node_r = 18 + col['active_ants'] * 2  # 工蚁数→节点大小
        node_r = max(15, min(node_r, 40))

        col_color = COLONY_COLORS[i % len(COLONY_COLORS)]

        # 连线到蚁后（信息素边）
        line_alpha = int(100 + data['pheromone']['density'] * 80)
        draw.line([(cx, cy), (nx, ny)], fill=(*GOLD[:3], line_alpha), width=max(1, int(data['pheromone']['density'] * 4)))

        # 节点
        node_health_color = _health_color(col['health'])
        draw.ellipse([nx-node_r, ny-node_r, nx+node_r, ny+node_r], fill=col_color, outline=node_health_color, width=2)
        draw.text((nx-15, ny-4), f"{col['active_ants']}🐜", fill=WHITE, font=font_label)

        # 标签
        draw.text((nx-20, ny+15), col['name'], fill=LIGHT_GOLD, font=font_label)

    # 底部图例/信息
    y_bottom = height - 100
    draw.text((40, y_bottom), "节点大小=工蚁数量 | 连线粗细=信息素浓度 | 边框颜色=健康度(绿/黄/红)",
              fill=GRAY, font=font_label)
    draw.text((40, y_bottom + 25), f"DNA: {DNA}", fill=GRAY, font=font_label)
    draw.text((40, y_bottom + 45), f"生成时间: {datetime.now().isoformat()}", fill=GRAY, font=font_label)

    img.save(output_path, quality=95)
    return output_path


def _health_color(health: float) -> Tuple[int, int, int]:
    """健康度→颜色"""
    if health >= 90:
        return GREEN
    elif health >= 60:
        return ORANGE
    else:
        return RED


# ═══════════════════════════════════════════════════════════════════
# 2. 信息素热力图
# ═══════════════════════════════════════════════════════════════════

def generate_heatmap(
    output_path: str = "ant_heatmap.png",
    width: int = 1920,
    height: int = 1080,
    data: Optional[Dict] = None,
) -> str:
    """生成信息素热力图"""
    if not PIL_OK or not NUMPY_OK:
        raise ImportError("需要 pillow 和 numpy")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)

    if data is None:
        # 模拟信息素分布数据
        np.random.seed(42)
        data = {
            "grid_size": 40,
            "pheromone_grid": (np.random.rand(40, 40) * 0.8).tolist(),
            "active_trails": [
                {"from": (10, 10), "to": (25, 15), "intensity": 0.9},
                {"from": (25, 15), "to": (30, 30), "intensity": 0.7},
                {"from": (30, 30), "to": (15, 25), "intensity": 0.5},
                {"from": (15, 25), "to": (10, 10), "intensity": 0.6},
            ],
            "summary": {"max_density": 0.85, "avg_density": 0.45, "active_tasks": 8},
        }

    # 绘制热力网格
    grid = np.array(data['pheromone_grid']) if 'pheromone_grid' in data else np.random.rand(40, 40) * 0.6
    cell_w = width / grid.shape[1]
    cell_h = height / grid.shape[0]

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            val = grid[y, x]
            color_idx = int(val * (len(HEAT_COLORS) - 1))
            color = HEAT_COLORS[min(color_idx, len(HEAT_COLORS) - 1)]
            x0, y0 = int(x * cell_w), int(y * cell_h)
            x1, y1 = int((x + 1) * cell_w), int((y + 1) * cell_h)
            draw.rectangle([x0, y0, x1, y1], fill=color)

    # 信息素轨迹（流线箭头）
    for trail in data.get('active_trails', []):
        fx, fy = trail['from']
        tx, ty = trail['to']
        fx, fy = int(fx * cell_w), int(fy * cell_h)
        tx, ty = int(tx * cell_w), int(ty * cell_h)
        alpha = int(100 + trail['intensity'] * 155)
        draw.line([(fx, fy), (tx, ty)], fill=(*GOLD[:3], alpha), width=int(trail['intensity'] * 5))

    # 图例
    draw.text((20, 20), "🐜 龍魂蚁群信息素热力图", fill=GOLD, font=_load_font(28))
    draw.text((20, 60),
              f"最大浓度: {data['summary']['max_density']:.2f} | "
              f"平均: {data['summary']['avg_density']:.2f} | "
              f"活跃任务: {data['summary']['active_tasks']}",
              fill=LIGHT_GOLD, font=_load_font(14))

    img.save(output_path, quality=95)
    return output_path


# ═══════════════════════════════════════════════════════════════════
# 3. 涌现仪表盘
# ═══════════════════════════════════════════════════════════════════

def generate_dashboard(
    output_path: str = "ant_dashboard.png",
    width: int = 1920,
    height: int = 1080,
    data: Optional[Dict] = None,
) -> str:
    """生成蚁群涌现仪表盘"""
    if not PIL_OK or not NUMPY_OK:
        raise ImportError("需要 pillow 和 numpy")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    font_title = _load_font(32)
    font_metric = _load_font(20)
    font_label = _load_font(14)
    font_big = _load_font(48)

    if data is None:
        data = {
            "metrics": {
                "queen_health": 92, "active_ants": 63, "task_completion": 87,
                "pheromone_density": 62, "emergence_index": 0.58,
                "meltdown_status": False, "energy_saving": False,
            },
            "emergence_history": [0.42, 0.45, 0.48, 0.51, 0.49, 0.55, 0.58] +
                                  [0.56 + abs(0.02 * math.sin(i)) for i in range(23)],
            "recent_events": [
                "视觉引擎完成3个图示生成",
                "安全巡检通过·0异常",
                "数据矿场新采集142条",
                "训练检查点保存 epoch 850",
                "信息素蒸发周期完成",
            ],
            "timestamp": datetime.now().isoformat(),
        }

    m = data['metrics']

    # 标题
    draw.text((40, 20), "🐜 龍魂蚁群涌现仪表盘", fill=GOLD, font=font_title)

    # ── 左侧：7个环形指标 ──
    ring_metrics = [
        ("蚁后健康", m['queen_health'], GREEN if m['queen_health'] >= 80 else ORANGE),
        ("工蚁活跃", m['active_ants'], GOLD),
        ("任务完成率", m['task_completion'], GREEN if m['task_completion'] >= 80 else ORANGE),
        ("信息素密度", m['pheromone_density'], GOLD),
        ("涌现指数", int(m['emergence_index'] * 100), GOLD if m['emergence_index'] > 0.5 else GRAY),
        ("熔断状态", 0 if not m['meltdown_status'] else 100, GREEN if not m['meltdown_status'] else RED),
        ("节能模式", 0 if not m['energy_saving'] else 100, GREEN if not m['energy_saving'] else GRAY),
    ]

    for i, (name, value, color) in enumerate(ring_metrics):
        rx, ry = 80, 120 + i * 110
        # 环形背景
        draw.ellipse([rx, ry, rx+60, ry+60], outline=DARK_GRAY, width=4)
        # 环形前景（简单处理：画弧线模拟）
        angle = int(value / 100 * 360) if not isinstance(value, str) and value <= 100 else 360
        if angle > 0:
            draw.arc([rx, ry, rx+60, ry+60], start=-90, end=-90+angle, fill=color, width=4)
        # 数值
        val_str = f"{value}%" if value <= 100 else str(value)
        draw.text((rx+70, ry+5), name, fill=LIGHT_GOLD, font=font_metric)
        draw.text((rx+70, ry+28), val_str, fill=color, font=font_label)

    # ── 中间：涌现曲线 ──
    chart_x, chart_y = 320, 100
    chart_w, chart_h = 800, 350
    draw.rectangle([chart_x, chart_y, chart_x+chart_w, chart_y+chart_h], outline=DARK_GRAY, width=1)

    history = data['emergence_history']
    if len(history) > 1:
        points = []
        for i, val in enumerate(history):
            px = chart_x + int(i / max(len(history)-1, 1) * chart_w)
            py = chart_y + chart_h - int(val * chart_h)
            py = max(chart_y, min(chart_y + chart_h, py))
            points.append((px, py))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=GOLD, width=2)

    # 涌现阈值线
    threshold_y = chart_y + chart_h - int(0.7 * chart_h)
    draw.line([(chart_x, threshold_y), (chart_x+chart_w, threshold_y)], fill=RED, width=1)
    draw.text((chart_x+chart_w-80, threshold_y-20), "涌现线 0.7", fill=RED, font=font_label)
    draw.text((chart_x+10, chart_y+10), f"涌现指数: {m['emergence_index']:.2f}",
              fill=GOLD, font=font_metric)

    # ── 右侧：最新事件流 ──
    event_x = chart_x + chart_w + 20
    draw.text((event_x, chart_y), "最近事件", fill=GOLD, font=font_metric)
    for i, evt in enumerate(data['recent_events']):
        color = GREEN if "通过" in evt or "完成" in evt else LIGHT_GOLD
        draw.text((event_x, chart_y + 35 + i * 40), f"• {evt}", fill=color, font=font_label)

    # 底部信息
    draw.text((40, height - 40), f"DNA: {DNA}  |  数据采集: {data['timestamp']}",
              fill=GRAY, font=font_label)

    img.save(output_path, quality=95)
    return output_path


# ═══════════════════════════════════════════════════════════════════
# 4. 全系列生成
# ═══════════════════════════════════════════════════════════════════

def generate_full(output_dir: str = "ant_viz") -> List[str]:
    """生成全系列蚁群可视化图"""
    os.makedirs(output_dir, exist_ok=True)
    files = [
        generate_topology(os.path.join(output_dir, "ant_topology.png")),
        generate_heatmap(os.path.join(output_dir, "ant_heatmap.png")),
        generate_dashboard(os.path.join(output_dir, "ant_dashboard.png")),
    ]
    # 生成解说词
    script_path = os.path.join(output_dir, "ant_narration.txt")
    with open(script_path, "w") as f:
        f.write(generate_narration())
    files.append(script_path)
    return files


# ═══════════════════════════════════════════════════════════════════
# 5. 解说词生成（给视频工坊用）
# ═══════════════════════════════════════════════════════════════════

def generate_narration(data: Optional[Dict] = None) -> str:
    """生成蚁群状态语音解说词"""
    if data is None:
        data = {
            "queen": {"health": 92},
            "colonies": [{"name": "视觉蚁群", "active_ants": 8}] * 12,
            "pheromone": {"density": 0.62, "emergence_index": 0.58},
        }

    lines = [
        "DNA: #龍芯⚡️丙午·癸未·丁未-蚁群播报-v1.0",
        "创建者: 诸葛鑫（UID9622）",
        "协议: CC BY-NC-SA 4.0",
        "",
        "【旁白】",
        f"UID9622蚁群系统，当前状态播报。",
        f"蚁后健康{data['queen']['health']}分。",
        f"活跃工蚁共{sum(c['active_ants'] for c in data['colonies'])}个。",
        f"信息素网络密度{data['pheromone']['density']:.0%}。",
        f"涌现指数{data['pheromone']['emergence_index']:.2f}——"
        f"{'涌现中，集群智能活跃。' if data['pheromone']['emergence_index'] > 0.6 else '正常协作状态。'}",
        "",
        "【旁白】",
        "系统各蚁群运行正常，无异常告警。",
        "以上，蚁群状态实时报告。完毕。",
        "",
        f"# 本脚本由 lh_ant_colony_visual.py narrate 自动生成",
        f"# DNA: {DNA}",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂蚁群分布可视化引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"DNA: {DNA}"
    )
    sub = parser.add_subparsers(dest="命令", help="子命令")

    p_topo = sub.add_parser("topo", help="生成蚁群拓扑图")
    p_topo.add_argument("--output", "-o", default="ant_topology.png")

    p_heat = sub.add_parser("heatmap", help="生成信息素热力图")
    p_heat.add_argument("--output", "-o", default="ant_heatmap.png")

    p_dash = sub.add_parser("dashboard", help="生成涌现仪表盘")
    p_dash.add_argument("--output", "-o", default="ant_dashboard.png")

    p_full = sub.add_parser("full", help="生成全系列")
    p_full.add_argument("--output-dir", "-d", default="ant_viz")

    sub.add_parser("narrate", help="输出解说词（供视频工坊使用）")

    args = parser.parse_args()

    if not PIL_OK:
        print("[ERROR] 需要 pillow: pip install pillow")
        sys.exit(1)

    if args.命令 == "topo":
        out = generate_topology(args.output)
        print(f"[OK] 蚁群拓扑图 → {out}")
    elif args.命令 == "heatmap":
        out = generate_heatmap(args.output)
        print(f"[OK] 信息素热力图 → {out}")
    elif args.命令 == "dashboard":
        out = generate_dashboard(args.output)
        print(f"[OK] 涌现仪表盘 → {out}")
    elif args.命令 == "full":
        files = generate_full(args.output_dir)
        print(f"[OK] 全系列生成完成 ({len(files)} 文件):")
        for f in files:
            print(f"  {f}")
    elif args.命令 == "narrate":
        print(generate_narration())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
