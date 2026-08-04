#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂20人格协作可视化引擎 v1.0
==============================
权重热力图·意图路由桑基图·协作力导向图·审计链路图·四层饼图。
对接 personas/ + bin/personas/ + 治理白皮书。

DNA: #龍芯⚡️丙午·癸未·丁未-人格协作可视化-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 engines/lh_persona_orchestra_visual.py heatmap --output persona_heat.png
  python3 engines/lh_persona_orchestra_visual.py graph --output persona_graph.png
  python3 engines/lh_persona_orchestra_visual.py audit --output persona_audit.png
  python3 engines/lh_persona_orchestra_visual.py full --output-dir persona_viz/
  python3 engines/lh_persona_orchestra_visual.py narrate  # 输出解说词
"""

import argparse, math, os, sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False

# ─── 常量 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·癸未·丁未-人格协作可视化-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ─── 龍魂色板 ───
BLACK = (8, 8, 8)
GOLD = (201, 168, 76)
LIGHT_GOLD = (230, 200, 120)
WHITE = (220, 220, 220)
RED = (196, 30, 58)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# ─── 人格标识 ───
PERSONAS = [
    ("P00", "文心",    (232, 213, 183)),  # 白金
    ("P01", "诸葛亮",  (74, 124, 89)),     # 军绿
    ("P02", "宝宝",    (232, 160, 191)),   # 暖粉
    ("P03", "雯雯",    (91, 143, 168)),    # 青蓝
    ("P04", "鲁班",    (139, 139, 139)),   # 铁灰
    ("P05", "上帝之眼",(212, 160, 23)),    # 赤金
    ("P06", "数学大师",(107, 63, 160)),    # 深紫
    ("P07", "管仲",    (123, 160, 91)),    # 铜绿
    ("P08", "仓颉",    (46, 94, 78)),      # 墨绿
    ("P09", "孙思邈",  (232, 224, 213)),   # 药白
    ("P10", "苏东坡",  (107, 174, 214)),   # 天蓝
    ("P11", "李白",    (255, 215, 0)),     # 烈金
    ("P12", "屈原",    (196, 30, 58)),     # 赤红
    ("P13", "姜子牙",  (139, 105, 20)),    # 紫金
    ("P14", "吕蒙",    (80, 200, 120)),    # 亮绿
    ("P15", "乔前辈",  (192, 192, 192)),   # 银灰
    ("P72", "龙盾",    (139, 0, 0)),       # 暗红
    ("P77", "黑天使",  (80, 80, 80)),      # 深灰（非纯黑以可见）
    ("S1",  "法律引擎",(0, 51, 102)),      # 法蓝
    ("S2",  "洛书369", (44, 0, 62)),       # 紫黑
]

# ─── 四层分类 ───
LAYERS = {
    "战略层":  [(232, 213, 183), ["P00", "P01"]],
    "执行层":  [(139, 139, 139), ["P02", "P03", "P04", "P07", "P14"]],
    "文化层":  [(255, 215, 0),   ["P08", "P09", "P10", "P11", "P12"]],
    "守护层":  [(196, 30, 58),   ["P05", "P06", "P13", "P15", "P72"]],
    "安全/子系统": [(80, 80, 80), ["P77", "S1", "S2"]],
}
LAYER_WEIGHTS = {"战略层": 25, "执行层": 36, "文化层": 15, "守护层": 19, "安全/子系统": 5}


def _load_font(size: int):
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
# 1. 权重热力图 (20x20)
# ═══════════════════════════════════════════════════════════════════

# 协作频率矩阵（从协议中提取）
COLLAB_MATRIX = {
    "P00": {"P01": 0.9, "P02": 0.3, "P03": 0.4, "P04": 0.5, "P05": 0.6, "P06": 0.3, "P07": 0.2, "P08": 0.4, "P09": 0.2, "P10": 0.3, "P11": 0.3, "P12": 0.1, "P13": 0.3, "P14": 0.2, "P15": 0.2, "P72": 0.1, "P77": 0.05, "S1": 0.1, "S2": 0.1},
    "P01": {"P00": 0.8, "P02": 0.2, "P03": 0.3, "P04": 0.6, "P05": 0.5, "P06": 0.7, "P07": 0.5, "P08": 0.3, "P09": 0.3, "P10": 0.2, "P11": 0.5, "P12": 0.3, "P13": 0.4, "P14": 0.3, "P15": 0.3, "P72": 0.2, "P77": 0.1, "S1": 0.1, "S2": 0.2},
    "P02": {"P00": 0.3, "P01": 0.2, "P03": 0.4, "P04": 0.3, "P05": 0.2, "P06": 0.1, "P07": 0.1, "P08": 0.5, "P09": 0.3, "P10": 0.6, "P11": 0.5, "P12": 0.3, "P14": 0.2, "S3": 0.2},
    "P03": {"P00": 0.4, "P01": 0.3, "P02": 0.4, "P04": 0.5, "P05": 0.5, "P06": 0.3, "P08": 0.4, "P10": 0.3, "P12": 0.3, "P13": 0.3, "P14": 0.3, "P15": 0.8, "P72": 0.2},
    "P04": {"P00": 0.5, "P01": 0.5, "P02": 0.3, "P03": 0.5, "P05": 0.6, "P06": 0.5, "P07": 0.3, "P08": 0.4, "P09": 0.3, "P10": 0.2, "P11": 0.4, "P12": 0.2, "P13": 0.3, "P14": 0.5, "P15": 0.4, "P72": 0.3, "P77": 0.2},
    "P05": {"P00": 0.6, "P01": 0.5, "P02": 0.2, "P03": 0.5, "P04": 0.6, "P06": 0.6, "P07": 0.4, "P08": 0.3, "P09": 0.5, "P10": 0.2, "P11": 0.3, "P12": 0.6, "P13": 0.5, "P14": 0.4, "P15": 0.5, "P72": 0.7, "P77": 0.6, "S1": 0.3, "S2": 0.3, "S3": 0.3},
    "P06": {"P00": 0.3, "P01": 0.7, "P03": 0.3, "P04": 0.5, "P05": 0.6, "P07": 0.5, "P08": 0.2, "P09": 0.3, "P11": 0.3, "P13": 0.3, "P15": 0.5, "P72": 0.3, "P77": 0.2, "S2": 0.7},
    "P07": {"P00": 0.2, "P01": 0.5, "P04": 0.3, "P05": 0.4, "P06": 0.5, "P13": 0.3},
    "P08": {"P00": 0.4, "P01": 0.3, "P02": 0.5, "P03": 0.4, "P04": 0.4, "P05": 0.3, "P06": 0.2, "P10": 0.6, "P11": 0.5, "P15": 0.3},
    "P09": {"P00": 0.2, "P01": 0.3, "P02": 0.3, "P03": 0.3, "P04": 0.3, "P05": 0.5, "P06": 0.3, "P12": 0.2, "P72": 0.3},
    "P10": {"P00": 0.3, "P01": 0.2, "P02": 0.6, "P03": 0.3, "P04": 0.2, "P05": 0.2, "P08": 0.6, "P11": 0.7, "P12": 0.4},
    "P11": {"P00": 0.3, "P01": 0.5, "P02": 0.5, "P03": 0.3, "P04": 0.4, "P05": 0.3, "P06": 0.3, "P08": 0.5, "P10": 0.7, "P12": 0.3},
    "P12": {"P00": 0.1, "P01": 0.3, "P02": 0.3, "P03": 0.3, "P04": 0.2, "P05": 0.6, "P06": 0.2, "P10": 0.4, "P11": 0.3, "P13": 0.3, "P72": 0.8, "P77": 0.3, "S1": 0.3, "S3": 0.5},
    "P13": {"P00": 0.3, "P01": 0.4, "P03": 0.3, "P04": 0.3, "P05": 0.5, "P06": 0.3, "P07": 0.3, "P12": 0.3, "P15": 0.6, "P72": 0.4, "P77": 0.2},
    "P14": {"P00": 0.2, "P01": 0.3, "P04": 0.5, "P05": 0.4, "P06": 0.2, "P15": 0.2, "P77": 0.3},
    "P15": {"P00": 0.2, "P01": 0.3, "P03": 0.8, "P04": 0.4, "P05": 0.5, "P06": 0.5, "P13": 0.6, "P72": 0.3},
    "P72": {"P05": 0.7, "P06": 0.3, "P12": 0.8, "P13": 0.4, "P15": 0.3, "P77": 0.5, "S3": 0.3},
    "P77": {"P04": 0.2, "P05": 0.6, "P06": 0.2, "P12": 0.3, "P13": 0.2, "P14": 0.3, "P72": 0.5},
}

PERSONA_IDS = [p[0] for p in PERSONAS]


def generate_heatmap(output_path: str = "persona_heatmap.png", width: int = 1920, height: int = 1080) -> str:
    """生成20x20人格权重热力图"""
    if not PIL_OK or not NUMPY_OK:
        raise ImportError("需要 pillow 和 numpy")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    font_title = _load_font(28)
    font_cell = _load_font(9)
    font_label = _load_font(12)

    n = len(PERSONA_IDS)
    margin = 80
    cell_size = min((width - margin * 2) // n, (height - margin * 2 - 60) // n)

    # 标题
    draw.text((40, 15), "20人格协作权重热力图", fill=GOLD, font=font_title)
    draw.text((40, 50), "X轴=发起人格  Y轴=接收人格  颜色=协作权重(0黑→金→白金1)", fill=LIGHT_GOLD, font=font_label)

    for y_idx, y_id in enumerate(PERSONA_IDS):
        for x_idx, x_id in enumerate(PERSONA_IDS):
            val = COLLAB_MATRIX.get(x_id, {}).get(y_id, 0.0)
            px = margin + x_idx * cell_size
            py = margin + 30 + y_idx * cell_size

            if val == 0:
                color = (15, 15, 15)
            else:
                r = int(8 + val * (232 - 8))
                g = int(8 + val * (213 - 8))
                b = int(8 + val * (183 - 8))
                color = (r, g, b)

            draw.rectangle([px, py, px + cell_size - 1, py + cell_size - 1], fill=color)

            # 最强关系标数值
            if val >= 0.7:
                draw.text((px+2, py+2), f"{val:.1f}", fill=WHITE, font=font_cell)

    # 标签
    for i, (pid, pname, pcolor) in enumerate(PERSONAS):
        # X轴
        draw.text((margin + i * cell_size + 2, margin + 10), pid,
                  fill=pcolor if pname != "黑天使" else LIGHT_GOLD, font=font_cell)
        # Y轴
        draw.text((10, margin + 35 + i * cell_size), pid, fill=pcolor if pname != "黑天使" else LIGHT_GOLD, font=font_cell)

    # 图例
    legend_x = margin + n * cell_size + 20
    legend_y = margin + 30
    draw.text((legend_x, legend_y), "强度", fill=GOLD, font=font_label)
    for i, val in enumerate([1.0, 0.75, 0.5, 0.25, 0.0]):
        r = int(8 + val * (232 - 8))
        g = int(8 + val * (213 - 8))
        b = int(8 + val * (183 - 8))
        draw.rectangle([legend_x, legend_y + 25 + i*20, legend_x + 30, legend_y + 45 + i*20],
                       fill=(r, g, b), outline=GRAY)
        draw.text((legend_x + 40, legend_y + 25 + i*20), f"{val:.0%}", fill=GRAY, font=font_label)

    draw.text((40, height - 30), f"DNA: {DNA}", fill=GRAY, font=font_label)
    img.save(output_path, quality=95)
    return output_path


# ═══════════════════════════════════════════════════════════════════
# 2. 协作力导向图
# ═══════════════════════════════════════════════════════════════════

def generate_graph(output_path: str = "persona_graph.png", width: int = 1920, height: int = 1080) -> str:
    """生成20人格协作力导向网络图"""
    if not PIL_OK:
        raise ImportError("需要 pillow")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    font_title = _load_font(28)
    font_node = _load_font(11)
    font_label = _load_font(10)

    draw.text((40, 20), "20人格协作力导向网络图", fill=GOLD, font=font_title)

    # 五层环形布局
    layer_radius = {
        "战略层": 80,
        "执行层": 190,
        "守护层": 300,
        "文化层": 400,
        "安全/子系统": 480,
    }
    layer_angles = {k: [] for k in LAYERS}

    center_x, center_y = width // 2, height // 2 + 30

    for layer_name, (layer_color, ids) in LAYERS.items():
        r = layer_radius[layer_name]
        n = len(ids)
        for i, pid in enumerate(ids):
            angle = (i / n) * 2 * math.pi - math.pi / 2
            px = int(center_x + r * math.cos(angle))
            py = int(center_y + r * math.sin(angle))
            layer_angles[layer_name].append((pid, px, py))

    # 先画边（信息素连线）
    for pid, targets in COLLAB_MATRIX.items():
        src_pos = _find_position(pid, layer_angles)
        if not src_pos:
            continue
        for tgt_id, val in targets.items():
            if val < 0.15:  # 过滤弱关系
                continue
            tgt_pos = _find_position(tgt_id, layer_angles)
            if not tgt_pos:
                continue
            alpha = int(val * 200)
            width = max(1, int(val * 3))
            draw.line([src_pos, tgt_pos], fill=(*GOLD[:3], alpha), width=width)

    # 再画节点
    for layer_name, (layer_color, ids) in LAYERS.items():
        for pid, px, py in layer_angles[layer_name]:
            pcolor = _persona_color(pid)
            node_r = 22 if layer_name == "战略层" else 16

            # 辉光
            draw.ellipse([px-node_r-3, py-node_r-3, px+node_r+3, py+node_r+3],
                         fill=(*GOLD[:3], 60) if layer_name == "战略层" else (*GOLD[:3], 20))

            draw.ellipse([px-node_r, py-node_r, px+node_r, py+node_r], fill=pcolor, outline=GOLD, width=1)

            # 标签
            pname = _persona_name(pid)
            draw.text((px-15, py-6), pid, fill=WHITE, font=font_node)

    # 图例
    draw.text((40, height - 30), f"DNA: {DNA}  |  节点大小=层级重要性  连线=协作关系  颜色=人格专属色",
              fill=GRAY, font=font_label)

    img.save(output_path, quality=95)
    return output_path


def _find_position(pid: str, layer_angles: Dict) -> Tuple[int, int]:
    for angles in layer_angles.values():
        for p, x, y in angles:
            if p == pid:
                return (x, y)
    return None


def _persona_color(pid: str) -> Tuple[int, int, int]:
    for p, name, color in PERSONAS:
        if p == pid:
            return color
    return GRAY


def _persona_name(pid: str) -> str:
    for p, name, _ in PERSONAS:
        if p == pid:
            return name
    return pid


# ═══════════════════════════════════════════════════════════════════
# 3. 审计链路图
# ═══════════════════════════════════════════════════════════════════

def generate_audit_chart(output_path: str = "persona_audit.png", width: int = 1920, height: int = 600) -> str:
    """生成审计链路流程图"""
    if not PIL_OK:
        raise ImportError("需要 pillow")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)
    font_title = _load_font(28)
    font_node = _load_font(16)
    font_label = _load_font(12)
    font_big = _load_font(20)

    draw.text((40, 20), "20人格审计 & 协作链路图", fill=GOLD, font=font_title)

    # 三条链路
    chains = [
        {
            "name": "生产链路",
            "y": 120,
            "nodes": [
                ("P04", "鲁班\n写代码", (139, 139, 139)),
                ("→", "", GRAY),
                ("P05", "上帝之眼\n三色审计", (212, 160, 23)),
                ("→", "", GRAY),
                ("P06", "数学大师\n镜像验算", (107, 63, 160)),
                ("→", "", GRAY),
                ("P15", "乔前辈\nDNA签章", (192, 192, 192)),
                ("→", "", GRAY),
                ("P03", "雯雯\n归档", (91, 143, 168)),
                ("🔴→", "", RED),
                ("P72", "龙盾\n熔断", (139, 0, 0)),
            ],
        },
        {
            "name": "意图链路",
            "y": 260,
            "nodes": [
                ("用户", "输入", GOLD),
                ("→", "", GRAY),
                ("P00", "文心\n意图解析", (232, 213, 183)),
                ("→", "", GRAY),
                ("P01", "诸葛亮\n推演决策", (74, 124, 89)),
                ("→", "", GRAY),
                ("执行层", "P02-P14\n分发执行", (139, 139, 139)),
                ("→", "", GRAY),
                ("P13", "姜子牙\n权限判定", (139, 105, 20)),
            ],
        },
        {
            "name": "部署链路",
            "y": 400,
            "nodes": [
                ("P14", "吕蒙\n部署", (80, 200, 120)),
                ("→", "", GRAY),
                ("P77", "黑天使\n攻击面扫描", (80, 80, 80)),
                ("→", "", GRAY),
                ("P05", "上帝之眼\n部署审计", (212, 160, 23)),
                ("→", "", GRAY),
                ("P15", "乔前辈\n签章发布", (192, 192, 192)),
                ("🔴→", "", RED),
                ("P72", "龙盾\n异常熔断", (139, 0, 0)),
            ],
        },
    ]

    for chain in chains:
        name, y, nodes = chain["name"], chain["y"], chain["nodes"]
        draw.text((40, y-25), name, fill=GOLD, font=font_big)

        x = 40
        for pid, label, color in nodes:
            if pid == "→" or pid == "🔴→":
                draw.text((x, y), pid, fill=RED if "🔴" in pid else GRAY, font=font_node)
                x += 40
            else:
                # 节点框
                node_w = 120
                node_h = 50
                draw.rectangle([x, y, x+node_w, y+node_h], fill=color, outline=GOLD, width=1)
                draw.text((x+10, y+5), label, fill=WHITE if sum(color) < 500 else BLACK, font=font_label)
                x += node_w + 10

    draw.text((40, height - 25), f"DNA: {DNA}", fill=GRAY, font=font_label)
    img.save(output_path, quality=95)
    return output_path


# ═══════════════════════════════════════════════════════════════════
# 4. 四层饼图
# ═══════════════════════════════════════════════════════════════════

def generate_pie_chart(output_path: str = "persona_pie.png", width: int = 800, height: int = 800) -> str:
    """生成四层权重饼图"""
    if not PIL_OK:
        raise ImportError("需要 pillow")

    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2
    outer_r = 300

    angles = []
    start = -90
    for name, weight in LAYER_WEIGHTS.items():
        angle = weight / 100 * 360
        end = start + angle
        angles.append((name, start, end, weight))
        start = end

    layer_colors = {
        "战略层":   (232, 213, 183),
        "执行层":   (91, 143, 168),
        "文化层":   (255, 215, 0),
        "守护层":   (196, 30, 58),
        "安全/子系统": (80, 80, 80),
    }

    for name, start, end, weight in angles:
        color = layer_colors.get(name, GOLD)
        draw.pieslice([cx-outer_r, cy-outer_r, cx+outer_r, cy+outer_r],
                      start=start, end=end, fill=color, outline=BLACK, width=2)

        # 标签
        mid_angle = math.radians((start + end) / 2)
        label_r = outer_r * 0.65
        lx = cx + label_r * math.cos(mid_angle)
        ly = cy + label_r * math.sin(mid_angle)
        draw.text((lx - 25, ly - 8), f"{name}\n{weight}%", fill=WHITE if sum(color) < 500 else BLACK,
                  font=_load_font(14))

    # 中心标题
    draw.text((cx - 80, cy - 15), "20人格\n四层权重", fill=GOLD, font=_load_font(22))

    img.save(output_path, quality=95)
    return output_path


# ═══════════════════════════════════════════════════════════════════
# 5. 全系列 & 解说词
# ═══════════════════════════════════════════════════════════════════

def generate_full(output_dir: str = "persona_viz") -> List[str]:
    """生成全系列人格可视化图"""
    os.makedirs(output_dir, exist_ok=True)
    files = [
        generate_heatmap(os.path.join(output_dir, "persona_heatmap.png")),
        generate_graph(os.path.join(output_dir, "persona_graph.png")),
        generate_audit_chart(os.path.join(output_dir, "persona_audit.png")),
        generate_pie_chart(os.path.join(output_dir, "persona_pie.png")),
    ]
    script_path = os.path.join(output_dir, "persona_narration.txt")
    with open(script_path, "w") as f:
        f.write(generate_narration())
    files.append(script_path)
    return files


def generate_narration() -> str:
    return textwrap.dedent(f"""\
    DNA: #龍芯⚡️丙午·癸未·丁未-人格播报-v1.0
    创建者: 诸葛鑫（UID9622）
    协议: CC BY-NC-SA 4.0

    【旁白】
    龍魂体系，20人格矩阵，四层架构，全部落地，0红色。

    【旁白】
    战略层——文心元认知统筹占百分之十，诸葛亮多路径推演占百分之十五。
    执行层——宝宝情感温度、雯雯结构归档、鲁班技术执行、管仲资源调度、吕蒙快速部署，共占百分之三十六。
    文化层——仓颉符号命名、孙思邈系统诊断、苏东坡沟通桥梁、李白创意爆发、屈原底线守卫，共占百分之十五。
    守护层——上帝之眼三色审计、数学大师权重计算、姜子牙权限调度、乔前辈DNA签章、龙盾四级熔断，共占百分之十九。
    安全专项——黑天使军团，红蓝对抗，只对自身系统。
    子系统——法律引擎、洛书369、人民维权助手。

    【旁白】
    三条核心链路。生产链路——鲁班写代码，上帝之眼审计，数学大师验算，乔前辈签章，雯雯归档。异常则龙盾熔断。
    意图链路——用户输入，文心解析，诸葛亮推演，执行层分发，姜子牙判定权限。
    部署链路——吕蒙部署，黑天使扫描，上帝之眼审计，乔前辈签章发布。

    【旁白】
    16核心全部落地，守护全开。以上，20人格协作图谱报告。
    # DNA: {DNA}
    """)


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂20人格协作可视化引擎 v1.0")
    sub = parser.add_subparsers(dest="命令")

    p_heat = sub.add_parser("heatmap", help="权重热力图")
    p_heat.add_argument("--output", "-o", default="persona_heatmap.png")

    p_graph = sub.add_parser("graph", help="协作力导向图")
    p_graph.add_argument("--output", "-o", default="persona_graph.png")

    p_audit = sub.add_parser("audit", help="审计链路图")
    p_audit.add_argument("--output", "-o", default="persona_audit.png")

    p_pie = sub.add_parser("pie", help="四层饼图")
    p_pie.add_argument("--output", "-o", default="persona_pie.png")

    p_full = sub.add_parser("full", help="全系列")
    p_full.add_argument("--output-dir", "-d", default="persona_viz")

    sub.add_parser("narrate", help="输出解说词")

    args = parser.parse_args()

    if not PIL_OK:
        print("[ERROR] 需要 pillow: pip install pillow")
        sys.exit(1)
    if not NUMPY_OK and args.命令 in ("heatmap",):
        print("[ERROR] 热力图需要 numpy: pip install numpy")
        sys.exit(1)

    if args.命令 == "heatmap":
        print(f"[OK] → {generate_heatmap(args.output)}")
    elif args.命令 == "graph":
        print(f"[OK] → {generate_graph(args.output)}")
    elif args.命令 == "audit":
        print(f"[OK] → {generate_audit_chart(args.output)}")
    elif args.命令 == "pie":
        print(f"[OK] → {generate_pie_chart(args.output)}")
    elif args.命令 == "full":
        for f in generate_full(args.output_dir):
            print(f"[OK] {f}")
    elif args.命令 == "narrate":
        print(generate_narration())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
