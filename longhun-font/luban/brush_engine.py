#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# #龍芯⚡️丙午·乙未·丙申·乙未·䷊泰-AUTO-DNA-LUBAN-BRUSH-ENGINE
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-BRUSH-ENGINE-v1.0
"""
笔锋引擎：把普通字体轮廓/单线笔画转换为书法笔画。

核心能力：
- 可变宽度笔画（起笔、行笔、收笔宽度变化）
- 横细竖粗
- 飞白与墨韵边缘
- 轮廓平滑与锯齿抑制
"""

import math
from typing import Any

DNA = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-BRUSH-ENGINE-v1.0"


def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def normalize(v: tuple[float, float]) -> tuple[float, float]:
    """归一化向量。"""
    d = math.hypot(v[0], v[1])
    if d < 1e-9:
        return (0.0, 0.0)
    return (v[0] / d, v[1] / d)


def perpendicular(v: tuple[float, float]) -> tuple[float, float]:
    """返回逆时针旋转 90 度的垂直向量。"""
    return (-v[1], v[0])


def interpolate(p1: tuple[float, float], p2: tuple[float, float], t: float) -> tuple[float, float]:
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)


def stroke_line_to_polygon(
    p1: tuple[float, float],
    p2: tuple[float, float],
    width: float,
    taper_start: float = 0.0,
    taper_end: float = 0.0,
) -> list[tuple[float, float]]:
    """
    把线段加粗为四边形轮廓，可选两端渐变收细。

    taper_start / taper_end: 两端收细比例 [0,1]，0 表示不收细。
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length < 1e-6:
        return []

    ux = -dy / length
    uy = dx / length
    hw = width / 2

    # 起笔端宽度：从 0 渐变到 width
    start_hw = hw * (1 - taper_start)
    end_hw = hw * (1 - taper_end)

    return [
        (x1 + ux * start_hw, y1 + uy * start_hw),
        (x2 + ux * end_hw, y2 + uy * end_hw),
        (x2 - ux * end_hw, y2 - uy * end_hw),
        (x1 - ux * start_hw, y1 - uy * start_hw),
    ]


def sample_cubic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
) -> list[tuple[float, float]]:
    """把三次贝塞尔曲线采样为折线点。"""
    points = []
    for i in range(steps + 1):
        t = i / steps
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
        y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
        points.append((x, y))
    return points


def sample_quadratic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """把二次贝塞尔曲线采样为折线点。"""
    points = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0]
        y = mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]
        points.append((x, y))
    return points


def brush_stroke_from_path(
    path_points: list[tuple[float, float]],
    base_width: float,
    params: Any,
) -> list[list[tuple[float, float]]]:
    """
    把一条路径点序列转换为带笔锋的书法笔画轮廓。

    返回：多段闭合多边形列表（每个多边形是一个笔画段）。
    """
    if len(path_points) < 2:
        return []

    taper_in = getattr(params, "taper_in", 0.15)
    taper_out = getattr(params, "taper_out", 0.12)
    horizontal_thin = getattr(params, "horizontal_thin", 0.75)
    vertical_thick = getattr(params, "vertical_thick", 1.15)

    polygons = []
    n = len(path_points)
    for i in range(n - 1):
        p1 = path_points[i]
        p2 = path_points[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        seg_len = math.hypot(dx, dy)
        if seg_len < 1e-6:
            continue

        # 根据笔画方向调整粗细：横细竖粗
        angle = math.atan2(abs(dy), abs(dx))  # 0=水平, pi/2=垂直
        direction_factor = horizontal_thin + (vertical_thick - horizontal_thin) * (angle / (math.pi / 2))
        width = base_width * direction_factor

        # 起收笔渐变
        seg_taper_start = 0.0
        seg_taper_end = 0.0
        if i == 0:
            seg_taper_start = taper_in
        if i == n - 2:
            seg_taper_end = taper_out

        poly = stroke_line_to_polygon(p1, p2, width, seg_taper_start, seg_taper_end)
        if poly:
            polygons.append(poly)

    return polygons


def raster_brush_stroke(
    draw,
    path_points: list[tuple[float, float]],
    base_width: float,
    params: Any,
    fill: Any,
):
    """
    直接把书法笔画绘制到 PIL ImageDraw（不返回轮廓，直接画）。
    使用椭圆串接模拟毛笔效果。
    """
    if len(path_points) < 2:
        return

    horizontal_thin = getattr(params, "horizontal_thin", 0.75)
    vertical_thick = getattr(params, "vertical_thick", 1.15)
    taper_in = getattr(params, "taper_in", 0.15)
    taper_out = getattr(params, "taper_out", 0.12)

    n = len(path_points)
    for i in range(n - 1):
        p1 = path_points[i]
        p2 = path_points[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        seg_len = math.hypot(dx, dy)
        if seg_len < 1e-6:
            continue

        angle = math.atan2(abs(dy), abs(dx))
        direction_factor = horizontal_thin + (vertical_thick - horizontal_thin) * (angle / (math.pi / 2))
        width = base_width * direction_factor

        # 沿线段插值多个圆，模拟连续笔触
        step = max(2, int(seg_len / (width * 0.4)))
        for j in range(step + 1):
            t = j / step
            x = p1[0] + dx * t
            y = p1[1] + dy * t

            # 起收笔变细
            if i == 0 and j == 0:
                w = width * (1 - taper_in)
            elif i == n - 2 and j == step:
                w = width * (1 - taper_out)
            else:
                w = width

            r = max(1, w / 2)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


if __name__ == "__main__":
    pts = [(0, 0), (50, 10), (100, 0)]
    polys = brush_stroke_from_path(pts, 20, type("P", (), {"taper_in": 0.2, "taper_out": 0.1, "horizontal_thin": 0.8, "vertical_thick": 1.1}))
    print(f"生成笔画段数: {len(polys)}")
    print("DNA:", DNA)
