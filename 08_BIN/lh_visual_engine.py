# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-2a387e4d
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
龍魂视觉引擎 v1.0 —— 文本→图示自动生成器
================================================================================
功能：分析解说文本，自动生成对应的流程图、架构图、知识图谱、对比图、
      时间线、概念图、数据图表、卡通解说角色
技术：Pillow原生绘制，零外部依赖，暗色龍魂金风格
场景：为视频工坊提供每场景的配套视觉

DNA: #龍芯⚡️丙午·乙未·癸亥·未时·䷝离-VISUAL-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
================================================================================
"""

import re
import math
import random
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =============================================================================
# 常量
# =============================================================================
VIDEO_W, VIDEO_H = 1920, 1080
VISUAL_W, VISUAL_H = 1500, 760  # 视觉图区域

# 默认配色（龍魂黑金）
DEFAULT_COLORS = {
    "bg": (14, 12, 24),
    "card_bg": (22, 20, 38, 220),
    "accent": (212, 175, 55),
    "accent2": (180, 130, 40),
    "text": (255, 250, 240),
    "text_dim": (180, 175, 165),
    "line": (80, 75, 70),
    "highlight": (255, 200, 50),
    "red": (220, 60, 50),
    "blue": (60, 150, 220),
    "green": (80, 200, 120),
    "purple": (160, 100, 220),
    "orange": (240, 150, 50),
}


def find_font(size: int) -> ImageFont.FreeTypeFont:
    """自动找中文字体"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


# =============================================================================
# 1. 文本分析 → 视觉类型判定
# =============================================================================

FLOW_KEYWORDS = [
    "步骤", "流程", "首先", "然后", "接着", "最后", "第一步", "第二步",
    "输入", "输出", "处理", "执行", "开始", "结束", "过程", "环节",
    "顺序", "依次", "先", "后", "再", "接着是", "之后",
]

ARCH_KEYWORDS = [
    "架构", "分层", "层次结构", "模块化", "组件化", "框架", "微服务",
    "底层", "上层", "中间层", "服务层", "数据层", "应用层", "表示层",
    "前端系统", "后端系统", "中间件", "缓存层", "网关", "消息队列",
]

TREE_KEYWORDS = [
    "分类", "分为", "类型", "包括", "包含", "分支", "子类", "种类",
    "有两种", "有三种", "分几类", "类别", "分为几", "大类", "小类",
]

COMPARE_KEYWORDS = [
    "对比", "比较", "区别", "不同", "相比", "优势", "劣势", "优于",
    "不如", "差异", "和...比", "相对于", "vs", "传统",
]

TIMELINE_KEYWORDS = [
    "历史", "发展", "进程", "阶段", "时期", "年代", "过去", "现在",
    "未来", "演变", "历程", "从...到", "以来", "起初", "后来",
]

CONCEPT_KEYWORDS = [
    "概念", "理论", "定义", "核心", "本质", "原理", "机制",
    "思想", "哲学", "理念", "范式", "模型",
]

DATA_KEYWORDS = [
    "数据", "数字", "比例", "增长", "下降", "统计", "百分比",
    "达到", "超过", "%", "倍", "亿", "万", "增加", "减少",
]

CHARACTER_KEYWORDS = [
    "我说", "我认为", "我觉得", "大家好", "欢迎", "今天",
    "我们来", "我们看", "请注意", "记住", "总之", "总结",
]


def detect_visual_type(text: str) -> str:
    """
    分析文本关键词，返回最佳视觉类型
    
    返回: flowchart/architecture/tree/comparison/timeline/concept/chart/character/default
    """
    scores = {
        "flowchart": 0,
        "architecture": 0,
        "tree": 0,
        "comparison": 0,
        "timeline": 0,
        "concept": 0,
        "chart": 0,
        "character": 0,
    }

    for kw in FLOW_KEYWORDS:
        if kw in text:
            scores["flowchart"] += 1
    for kw in ARCH_KEYWORDS:
        if kw in text:
            scores["architecture"] += 2  # 架构词更具体
    for kw in TREE_KEYWORDS:
        if kw in text:
            scores["tree"] += 1.5
    for kw in COMPARE_KEYWORDS:
        if kw in text:
            scores["comparison"] += 2
    for kw in TIMELINE_KEYWORDS:
        if kw in text:
            scores["timeline"] += 1.5
    for kw in CONCEPT_KEYWORDS:
        if kw in text:
            scores["concept"] += 1
    for kw in DATA_KEYWORDS:
        if kw in text:
            scores["chart"] += 1.5
    for kw in CHARACTER_KEYWORDS:
        if kw in text:
            scores["character"] += 0.5

    # 取最高分
    best = max(scores, key=scores.get)
    if scores[best] >= 1:
        return best
    return "default"


def extract_concepts(text: str, max_items: int = 7) -> List[str]:
    """从文本中提取关键概念/短语"""
    # 按标点切分
    parts = re.split(r'[，。！？、；：\n]', text)
    concepts = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # 取较短的短语（2-15字）
        if 2 <= len(p) <= 15:
            concepts.append(p)
        elif len(p) > 15:
            # 长句取关键片段
            sub = re.split(r'[的之和与及或]', p)
            for s in sub:
                s = s.strip()
                if 2 <= len(s) <= 12 and s not in concepts:
                    concepts.append(s)

    # 去重，优先保留有意义的
    seen = set()
    result = []
    for c in concepts:
        if c not in seen and len(c) >= 2:
            seen.add(c)
            result.append(c)
    return result[:max_items]


# =============================================================================
# 2. 图示绘制引擎
# =============================================================================

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Pillow 原生圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=radius, fill=fill, outline=outline, width=width
    )


def draw_arrow(draw, start, end, color, width=3, arrow_size=12):
    """绘制带箭头的线"""
    x1, y1 = start
    x2, y2 = end
    # 画线
    draw.line([start, end], fill=color, width=width)

    # 画箭头
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1:
        return
    ux, uy = dx / length, dy / length

    # 箭头两边
    ax1 = x2 - arrow_size * ux + arrow_size * 0.4 * uy
    ay1 = y2 - arrow_size * uy - arrow_size * 0.4 * ux
    ax2 = x2 - arrow_size * ux - arrow_size * 0.4 * uy
    ay2 = y2 - arrow_size * uy + arrow_size * 0.4 * ux

    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)


def text_bbox(draw, text, font):
    """获取文字包围盒"""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(text: str, font, max_width: int) -> List[str]:
    """中文自动换行"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        w, _ = text_bbox(ImageDraw.Draw(Image.new('RGBA', (1, 1))), test, font)
        if w > max_width:
            if current:
                lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# --- 流程图 ---

def draw_flowchart(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制横向/纵向流程图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    n = len(concepts)
    if n < 2:
        return img

    font_title = find_font(32)
    font_label = find_font(22)

    # 标题
    title = "📋 执行流程"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 30), title, font=font_title, fill=accent)

    # 横向布局
    if n <= 5:
        # 水平排列
        box_w = min(240, (width - 200) // n)
        box_h = 90
        start_y = height // 2 - box_h // 2 + 40
        spacing = (width - 100 - n * box_w) // (n + 1)

        for i, concept in enumerate(concepts):
            x = 50 + spacing + i * (box_w + spacing)
            y = start_y

            # 步骤编号圆
            circle_r = 16
            circle_x = x + box_w // 2
            circle_y = y - 25
            draw.ellipse(
                [circle_x - circle_r, circle_y - circle_r, circle_x + circle_r, circle_y + circle_r],
                fill=accent
            )
            num_w, num_h = text_bbox(draw, str(i + 1), font_label)
            draw.text(
                (circle_x - num_w // 2, circle_y - num_h // 2 - 1),
                str(i + 1), font=font_label, fill=(0, 0, 0)
            )

            # 卡片
            draw_rounded_rect(draw, [x, y, x + box_w, y + box_h], 12, card_bg, accent, 2)

            # 文字（自动换行）
            lines = wrap_text(concept, font_label, box_w - 20)
            line_h = 26
            total_h = len(lines) * line_h
            text_y = y + (box_h - total_h) // 2
            for j, line in enumerate(lines):
                lw, _ = text_bbox(draw, line, font_label)
                draw.text((x + (box_w - lw) // 2, text_y + j * line_h), line, font=font_label, fill=text_color)

            # 箭头（到下一个）
            if i < n - 1:
                arrow_start = (x + box_w + 8, y + box_h // 2)
                arrow_end = (x + box_w + spacing - 8, y + box_h // 2)
                draw_arrow(draw, arrow_start, arrow_end, accent)

    else:
        # 纵向排列
        box_w = min(500, width - 200)
        box_h = 60
        start_x = (width - box_w) // 2
        spacing = (height - 120 - n * box_h) // (n + 1)

        for i, concept in enumerate(concepts):
            x, y = start_x, 60 + spacing + i * (box_h + spacing)

            # 步骤编号
            circle_r = 14
            draw.ellipse([x - 40, y + box_h // 2 - circle_r, x - 40 + 2 * circle_r, y + box_h // 2 + circle_r], fill=accent)
            num_w, num_h = text_bbox(draw, str(i + 1), font_label)
            draw.text((x - 40 + circle_r - num_w // 2, y + box_h // 2 - num_h // 2 - 1), str(i + 1), font=font_label, fill=(0, 0, 0))

            draw_rounded_rect(draw, [x, y, x + box_w, y + box_h], 10, card_bg, accent, 2)

            lines = wrap_text(concept, font_label, box_w - 30)
            line_h = 26
            total_h = len(lines) * line_h
            text_y = y + (box_h - total_h) // 2
            for j, line in enumerate(lines):
                draw.text((x + 20, text_y + j * line_h), line, font=font_label, fill=text_color)

            if i < n - 1:
                arrow_start = (x + box_w // 2, y + box_h + 6)
                arrow_end = (x + box_w // 2, y + box_h + spacing - 6)
                draw_arrow(draw, arrow_start, arrow_end, accent)

    return img


# --- 架构图 ---

def draw_architecture(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制分层架构图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])
    dim_text = colors.get("text_dim", DEFAULT_COLORS["text_dim"])

    font_title = find_font(32)
    font_label = find_font(22)
    font_small = find_font(18)

    title = "🏗️ 系统架构"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 25), title, font=font_title, fill=accent)

    n = min(len(concepts), 6)
    layer_labels = ["展示层", "应用层", "服务层", "数据层", "基础设施", "安全层"][:n]

    # 从下往上画
    layer_h = (height - 130) // n
    box_w = width - 160
    start_x = 80

    for i in range(n):
        y = height - 50 - (i + 1) * layer_h

        # 层背景
        alpha = 100 + i * 20
        layer_color = (
            min(255, accent[0] // 3 + i * 10),
            min(255, accent[1] // 3 + i * 8),
            min(255, accent[2] // 3 + i * 6),
            180
        )
        draw.rectangle(
            [start_x, y, start_x + box_w, y + layer_h - 8],
            fill=(layer_color[0], layer_color[1], layer_color[2], 30),
            outline=(*accent, 80), width=1
        )

        # 层标签（左侧）
        label = layer_labels[i]
        label_w, label_h = text_bbox(draw, label, font_label)
        draw.text((start_x - label_w - 15, y + (layer_h - 8 - label_h) // 2), label, font=font_label, fill=dim_text)

        # 内容
        if i < len(concepts):
            concept = concepts[i]
            lines = wrap_text(concept, font_small, box_w - 60)
            total_h = len(lines) * 24
            text_y = y + (layer_h - 8 - total_h) // 2
            for j, line in enumerate(lines):
                lw, _ = text_bbox(draw, line, font_small)
                draw.text((start_x + 30, text_y + j * 24), line, font=font_small, fill=text_color)

    # 层间箭头（数据流方向）
    for i in range(n - 1):
        y1 = height - 50 - (i + 1) * layer_h + layer_h // 2
        y2 = height - 50 - (i + 2) * layer_h + layer_h // 2
        draw_arrow(draw, (start_x + box_w + 25, y1), (start_x + box_w + 25, y2), (*accent, 100), width=2, arrow_size=8)
        draw_arrow(draw, (start_x + box_w + 25, y2), (start_x + box_w + 25, y1), (*accent, 60), width=1, arrow_size=6)

    return img


# --- 知识树 ---

def draw_knowledge_tree(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制知识树/分类图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(32)
    font_label = find_font(20)

    title = "🌳 知识分类"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 25), title, font=font_title, fill=accent)

    n = len(concepts)
    if n < 2:
        return img

    # 中心根节点
    root_x, root_y = width // 2, 100
    root_r = 50
    draw.ellipse([root_x - root_r, root_y - root_r, root_x + root_r, root_y + root_r], fill=accent)
    root_text = "核心"
    rw, rh = text_bbox(draw, root_text, font_label)
    draw.text((root_x - rw // 2, root_y - rh // 2 - 1), root_text, font=font_label, fill=(0, 0, 0))

    # 分支节点（扇形排列）
    branch_count = min(n, 8)
    # 分枝从根节点向四周发散
    for i in range(branch_count):
        if i >= n:
            break
        # 角度（下半圆扇形）
        angle = math.pi * 0.15 + math.pi * 0.7 * i / max(branch_count - 1, 1)
        dist = 200 + (i % 3) * 60
        bx = int(root_x + dist * math.cos(angle))
        by = int(root_y + dist * math.sin(angle))

        # 连接线
        draw.line([(root_x, root_y + root_r), (bx, by)], fill=(*accent, 120), width=2)

        # 子节点球
        node_r = 35
        node_colors = [
            (60, 150, 220), (80, 200, 120), (240, 150, 50),
            (160, 100, 220), (220, 80, 100), (100, 180, 200),
            (200, 140, 60), (140, 160, 100)
        ]
        nc = node_colors[i % len(node_colors)]
        draw.ellipse([bx - node_r, by - node_r, bx + node_r, by + node_r], fill=nc)

        # 标签（截短）
        label = concepts[i][:6]
        lw, lh = text_bbox(draw, label, font_label)
        draw.text((bx - lw // 2, by - lh // 2 - 1), label, font=font_label, fill=(255, 255, 255))

        # 子节点下方的小标签
        sub_label = concepts[i][:8] if len(concepts[i]) > 6 else ""
        if sub_label:
            f_small = find_font(16)
            sl_w, sl_h = text_bbox(draw, sub_label, f_small)
            draw.text((bx - sl_w // 2, by + node_r + 8), sub_label,
                      font=f_small,
                      fill=colors.get("text_dim", DEFAULT_COLORS["text_dim"]))

    return img


# --- 对比图 ---

def draw_comparison(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制双栏对比图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(30)
    font_label = find_font(22)
    font_col = find_font(28)

    title = "⚖️ 对比分析"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 20), title, font=font_title, fill=accent)

    col_w = (width - 120) // 2
    col_h = height - 140

    # 左栏
    left_x, left_y = 40, 90
    draw.rectangle([left_x, left_y, left_x + col_w, left_y + col_h],
                   outline=(60, 150, 220, 150), width=3)
    draw.rectangle([left_x, left_y, left_x + col_w, left_y + 45],
                   fill=(60, 150, 220, 60))
    col_t = "方案 A"
    ct_w, ct_h = text_bbox(draw, col_t, font_col)
    draw.text((left_x + (col_w - ct_w) // 2, left_y + 8), col_t, font=font_col,
              fill=(100, 190, 255))

    # 右栏
    right_x = width - 40 - col_w
    draw.rectangle([right_x, left_y, right_x + col_w, left_y + col_h],
                   outline=(240, 150, 50, 150), width=3)
    draw.rectangle([right_x, left_y, right_x + col_w, left_y + 45],
                   fill=(240, 150, 50, 60))
    col_t2 = "方案 B"
    ct2_w, _ = text_bbox(draw, col_t2, font_col)
    draw.text((right_x + (col_w - ct2_w) // 2, left_y + 8), col_t2, font=font_col,
              fill=(255, 190, 80))

    # 填充对比项
    mid = len(concepts) // 2
    left_items = concepts[:mid] if mid > 0 else [concepts[0]] if concepts else []
    right_items = concepts[mid:] if mid > 0 else concepts[1:] if len(concepts) > 1 else []

    for side, items, start_x in [("left", left_items, left_x), ("right", right_items, right_x)]:
        for j, item in enumerate(items):
            iy = left_y + 55 + j * 45
            if iy > left_y + col_h - 40:
                break
            # 项目符号
            bullet_color = (60, 150, 220) if side == "left" else (240, 150, 50)
            draw.ellipse([start_x + 20, iy + 8, start_x + 28, iy + 16], fill=bullet_color)
            # 文字
            short = item[:14]
            draw.text((start_x + 40, iy + 3), short, font=font_label, fill=text_color)

    # vs 中间标记
    vs_font = find_font(48)
    vs_w, vs_h = text_bbox(draw, "VS", vs_font)
    draw.text(((width - vs_w) // 2, left_y + col_h // 2 - vs_h // 2), "VS",
              font=vs_font, fill=(*accent, 180))

    return img


# --- 时间线 ---

def draw_timeline(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制横向时间线"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(30)
    font_label = find_font(20)
    font_date = find_font(18)

    title = "📅 发展历程"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 20), title, font=font_title, fill=accent)

    n = min(len(concepts), 6)
    line_y = height // 2 + 30
    margin = 60

    # 水平线
    draw.line([(margin, line_y), (width - margin, line_y)], fill=(*accent, 120), width=4)

    spacing = (width - 2 * margin) // max(n - 1, 1)

    for i in range(n):
        x = margin + i * spacing
        # 节点圆
        r = 14
        node_color = accent if i == 0 or i == n - 1 else colors.get("line", DEFAULT_COLORS["line"])
        draw.ellipse([x - r, line_y - r, x + r, line_y + r], fill=node_color)

        # 上方：日期标签
        date_label = f"阶段{i + 1}"
        dw, dh = text_bbox(draw, date_label, font_date)
        draw.text((x - dw // 2, line_y - 40 - dh), date_label, font=font_date, fill=accent)

        # 下方：内容（交替上下）
        concept = concepts[i][:12]
        cw, ch = text_bbox(draw, concept, font_label)

        if i % 2 == 0:
            # 上方卡片
            card_y = line_y - 38 - dh - 10 - 32
        else:
            # 下方卡片
            card_y = line_y + 30

        card_w = min(cw + 24, 160)
        card_x = max(10, min(width - card_w - 10, x - card_w // 2))
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + 30],
                       fill=(*accent, 25), outline=(*accent, 80), width=1)
        draw.text((card_x + 12, card_y + 6), concept, font=font_label, fill=text_color)

    return img


# --- 概念图 ---

def draw_concept_map(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制中心辐射概念图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(30)
    font_label = find_font(20)

    title = "💡 概念图谱"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 20), title, font=font_title, fill=accent)

    # 中心概念
    cx, cy = width // 2, height // 2 + 20
    center_r = 60
    draw.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r],
                 fill=accent)
    center_text = concepts[0][:6] if concepts else "核心"
    cw, ch = text_bbox(draw, center_text, find_font(24))
    draw.text((cx - cw // 2, cy - ch // 2 - 1), center_text, font=find_font(24), fill=(0, 0, 0))

    # 周围卫星概念
    satellites = concepts[1:8]
    sat_count = len(satellites)
    if sat_count < 2:
        return img

    sat_colors = [
        (60, 150, 220), (80, 200, 120), (240, 150, 50),
        (160, 100, 220), (220, 80, 100), (100, 180, 200),
        (200, 140, 60),
    ]

    for i, sat in enumerate(satellites):
        angle = 2 * math.pi * i / sat_count - math.pi / 2
        dist = 180 + (i % 3) * 30
        sx = int(cx + dist * math.cos(angle))
        sy = int(cy + dist * math.sin(angle))

        # 连接线
        draw.line([(cx, cy), (sx, sy)], fill=(*accent, 60), width=1)

        # 卫星节点
        sr = 28
        sc = sat_colors[i % len(sat_colors)]
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sc)

        # 标签
        label = sat[:6]
        lw, lh = text_bbox(draw, label, find_font(16))
        draw.text((sx - lw // 2, sy - lh // 2 - 1), label, font=find_font(16), fill=(255, 255, 255))

    return img


# --- 数据图表 ---

def draw_data_chart(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """绘制数据柱状图"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])

    font_title = find_font(30)
    font_label = find_font(18)

    title = "📊 数据概览"
    title_w, _ = text_bbox(draw, title, font_title)
    draw.text(((width - title_w) // 2, 20), title, font=font_title, fill=accent)

    # 尝试提取数字
    numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(%|亿|万|倍|个)?', ' '.join(concepts))
    if not numbers:
        # 回退：概念字数+随机值作为数据
        values = [min(len(c), 80) for c in concepts[:6]]
        labels = [c[:6] for c in concepts[:6]]
    else:
        values = [float(n[0]) for n in numbers[:6]]
        labels = [f"指标{i+1}" for i in range(len(values))]

    n = min(len(values), 6)
    if n < 1:
        return img

    margin = 120
    chart_w = width - 2 * margin
    chart_h = height - 200
    bar_w = chart_w // n - 20
    max_val = max(values) if max(values) > 0 else 1

    bar_colors = [
        (60, 150, 220), (80, 200, 120), (240, 150, 50),
        (160, 100, 220), (220, 80, 100), (100, 180, 200),
    ]

    for i, (val, label) in enumerate(zip(values, labels)):
        bar_h = int((val / max_val) * chart_h * 0.9)
        bx = margin + i * (chart_w // n) + 10
        by = height - 60 - bar_h

        bc = bar_colors[i % len(bar_colors)]
        draw.rectangle([bx, by, bx + bar_w, height - 60], fill=bc)

        # 数值标签
        val_text = str(val)[:6]
        vw, vh = text_bbox(draw, val_text, font_label)
        draw.text((bx + (bar_w - vw) // 2, by - vh - 4), val_text, font=font_label, fill=accent)

        # 底部标签
        lw, lh = text_bbox(draw, label, font_label)
        draw.text((bx + (bar_w - lw) // 2, height - 50), label, font=font_label, fill=text_color)

    return img


# --- 卡通解说角色 ---

def draw_cartoon_character(text: str, colors: Dict, width: int, height: int) -> Image.Image:
    """绘制卡通解说角色 + 对话框"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(28)
    font_body = find_font(22)

    # 人物位置（左侧）
    body_x, body_y = 120, height // 2 - 20

    # 头（圆）
    head_r = 45
    head_cx, head_cy = body_x, body_y - 20
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=(255, 220, 180), outline=(200, 160, 120), width=3
    )

    # 眼睛
    eye_y = head_cy - 10
    draw.ellipse([head_cx - 18, eye_y - 8, head_cx - 8, eye_y + 2], fill=(0, 0, 0))
    draw.ellipse([head_cx + 8, eye_y - 8, head_cx + 18, eye_y + 2], fill=(0, 0, 0))

    # 眼睛高光
    draw.ellipse([head_cx - 15, eye_y - 6, head_cx - 11, eye_y - 2], fill=(255, 255, 255))
    draw.ellipse([head_cx + 11, eye_y - 6, head_cx + 15, eye_y - 2], fill=(255, 255, 255))

    # 微笑
    draw.arc([head_cx - 12, head_cy + 2, head_cx + 12, head_cy + 16],
             start=0, end=180, fill=(100, 60, 40), width=2)

    # 身体
    body_top = head_cy + head_r - 5
    draw.rounded_rectangle(
        [body_x - 35, body_top, body_x + 35, body_y + 80],
        radius=8, fill=(40, 80, 140), outline=(30, 60, 110), width=2
    )

    # 领口
    draw.polygon(
        [(body_x - 12, body_top), (body_x + 12, body_top), (body_x, body_top + 20)],
        fill=(255, 255, 255)
    )

    # 对话框（右侧大区域）
    bubble_x = 220
    bubble_y = 60
    bubble_w = width - bubble_x - 40
    bubble_h = height - 120

    # 气泡形状
    draw.rounded_rectangle(
        [bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
        radius=20, fill=card_bg[:3] + (200,), outline=(*accent, 100), width=2
    )

    # 气泡小三角
    tri_points = [(bubble_x, bubble_y + 60), (bubble_x - 15, bubble_y + 45), (bubble_x, bubble_y + 30)]
    draw.polygon(tri_points, fill=card_bg[:3] + (200,))
    draw.line([tri_points[1], tri_points[0]], fill=(*accent, 100), width=2)
    draw.line([tri_points[1], tri_points[2]], fill=(*accent, 100), width=2)

    # 气泡内文字
    font_label = find_font(20)
    lines = wrap_text(text, font_label, bubble_w - 60)
    line_h = 36
    max_lines = (bubble_h - 60) // line_h
    lines = lines[:max_lines]
    total_h = len(lines) * line_h
    start_y = bubble_y + (bubble_h - total_h) // 2

    for j, line in enumerate(lines):
        draw.text((bubble_x + 25, start_y + j * line_h), line, font=font_label, fill=text_color)

    # 标题
    title_w, _ = text_bbox(draw, "龍魂解说", font_title)
    draw.text(((width - title_w) // 2, 15), "龍魂解说", font=font_title, fill=accent)

    return img


# --- 默认抽象视觉 ---

def draw_default_visual(concepts: List[str], colors: Dict, width: int, height: int) -> Image.Image:
    """默认抽象概念卡片"""
    img = Image.new('RGBA', (width, height), colors.get("bg", DEFAULT_COLORS["bg"]))
    draw = ImageDraw.Draw(img)

    accent = colors.get("accent", DEFAULT_COLORS["accent"])
    accent2 = colors.get("accent2", DEFAULT_COLORS["accent2"])
    text_color = colors.get("text", DEFAULT_COLORS["text"])
    card_bg = colors.get("card_bg", DEFAULT_COLORS["card_bg"])

    font_title = find_font(32)
    font_label = find_font(24)
    font_body = find_font(20)

    # 装饰性几何背景
    for i in range(3):
        angle = i * 120
        rad = math.radians(angle)
        cx = int(width // 2 + 200 * math.cos(rad))
        cy = int(height // 2 + 150 * math.sin(rad))
        r = 80 + i * 20
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=(*accent, 15 + i * 10), width=2)

    # 主标题
    main_concept = concepts[0][:15] if concepts else "核心概念"
    mw, mh = text_bbox(draw, main_concept, font_title)
    draw.text(((width - mw) // 2, 40), main_concept, font=font_title, fill=accent)

    # 卡片
    card_w, card_h = 900, 450
    card_x = (width - card_w) // 2
    card_y = 100
    draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                   fill=(*card_bg[:3], 100), outline=(*accent, 60), width=1)

    # 卡片内关键词列表
    display_items = concepts[:8]
    item_h = (card_h - 60) // max(len(display_items), 1)
    for j, item in enumerate(display_items):
        iy = card_y + 25 + j * min(item_h, 60)
        if iy > card_y + card_h - 30:
            break
        # 编号
        draw.text((card_x + 40, iy + 5), f"{j + 1:02d}", font=font_label, fill=accent2)
        # 分隔线
        line_x = card_x + 90
        draw.line([(line_x, iy + 20), (line_x + 12, iy + 20)], fill=accent, width=2)
        # 文字
        draw.text((card_x + 115, iy + 6), item[:28], font=font_body, fill=text_color)

    # 底部装饰
    draw.line([(card_x + 20, card_y + card_h + 20), (card_x + card_w - 20, card_y + card_h + 20)],
              fill=(*accent, 40), width=1)

    return img


# =============================================================================
# 3. 主入口
# =============================================================================

VISUAL_GENERATORS = {
    "flowchart": draw_flowchart,
    "architecture": draw_architecture,
    "tree": draw_knowledge_tree,
    "comparison": draw_comparison,
    "timeline": draw_timeline,
    "concept": draw_concept_map,
    "chart": draw_data_chart,
    "character": draw_cartoon_character,
    "default": draw_default_visual,
}


def generate_visual(
    scene_text: str,
    colors: Dict = None,
    width: int = VISUAL_W,
    height: int = VISUAL_H,
    visual_type: str = None,
) -> Image.Image:
    """
    主入口：给定场景文本 → 生成对应视觉图
    
    Args:
        scene_text: 场景解说文本
        colors: 配色字典（从 COLOR_SCHEME 传入）
        width, height: 输出图像尺寸
        visual_type: 强制指定类型，None=自动检测
    
    Returns:
        PIL Image (RGBA)
    """
    if colors is None:
        colors = DEFAULT_COLORS
    else:
        # 转换 COLOR_SCHEME 格式
        colors = {
            "bg": colors.get("bg_top", DEFAULT_COLORS["bg"]),
            "card_bg": colors.get("subtitle_bg", DEFAULT_COLORS["card_bg"]),
            "accent": colors.get("accent", DEFAULT_COLORS["accent"]),
            "accent2": colors.get("accent2", DEFAULT_COLORS["accent2"]),
            "text": colors.get("text", DEFAULT_COLORS["text"]),
            "text_dim": (140, 135, 125),
            "line": (80, 75, 70),
        }

    # 检测类型
    if visual_type is None:
        visual_type = detect_visual_type(scene_text)

    # 提取概念
    concepts = extract_concepts(scene_text)

    # 生成
    generator = VISUAL_GENERATORS.get(visual_type, draw_default_visual)
    try:
        return generator(concepts, colors, width, height)
    except Exception as e:
        print(f"  ⚠️ 视觉生成失败 ({visual_type}): {e}，使用默认")
        return draw_default_visual(concepts, colors, width, height)


# =============================================================================
# 独立测试
# =============================================================================

if __name__ == "__main__":
    import sys

    tests = [
        ("首先准备数据，然后清洗数据，接着训练模型，最后部署上线", "流程图"),
        ("系统分为展示层、应用层、服务层、数据层四层架构", "架构图"),
        ("人工智能分为机器学习、深度学习、自然语言处理、计算机视觉等方向", "知识树"),
        ("传统方法需要人工标注，AI方法可以自动学习，效率和准确度都更高", "对比图"),
        ("从2010年的起步阶段，到2015年的快速发展，再到2020年的成熟应用", "时间线"),
        ("熵增定律是热力学第二定律的核心概念，描述了系统从有序走向无序的必然趋势", "概念图"),
        ("用户增长达到120%，日活跃用户超过500万，转化率提升3倍", "数据图"),
        ("大家好，今天我来给大家讲一讲什么是龍魂系统", "卡通解说"),
    ]

    test_dir = Path(__file__).parent.parent / "videos" / "_test_visuals"
    test_dir.mkdir(parents=True, exist_ok=True)

    for i, (text, desc) in enumerate(tests):
        vtype = detect_visual_type(text)
        img = generate_visual(text, width=VISUAL_W, height=VISUAL_H, visual_type=vtype)
        path = test_dir / f"test_{i+1:02d}_{vtype}.png"
        img.save(path)
        print(f"  [{i+1}] {desc} → {vtype} → {path.name}")
