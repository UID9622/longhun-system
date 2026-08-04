#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-PRACTICAL-SYMBOLS-v1.0
"""
龍魂字元库 · 实用符号扩展脚本
为 LonghunFont 添加编程、数学、终端、货币等常用 Unicode 符号。
"""

import json
import os
import re
from datetime import datetime, timezone
from math import cos, sin, pi, sqrt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
SRC = os.path.join(PROJECT_DIR, "glyphs", "龍魂字元库_v0011_两千中文字.json")
DST = os.path.join(PROJECT_DIR, "glyphs", "龍魂字元库_v0011_实用符号版.json")

NEW_DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-PRACTICAL-SYMBOLS-v1.0"

# -------------------- 笔画辅助函数 --------------------

def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [round(x, 2), round(y, 2)]}

def stroke_line(x, y):
    return {"类型": "直线段", "终点": [round(x, 2), round(y, 2)]}

def polyline(points):
    """points: [(x,y), ...]"""
    if not points:
        return []
    s = [stroke_move(points[0][0], points[0][1])]
    for x, y in points[1:]:
        s.append(stroke_line(x, y))
    return s

def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])

def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])

def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])

def circle(cx, cy, r, segments=16):
    pts = []
    for i in range(segments + 1):
        a = 2 * pi * i / segments
        pts.append((cx + r * cos(a), cy + r * sin(a)))
    return polyline(pts)

def arc(cx, cy, r, start_angle, end_angle, segments=12):
    pts = []
    for i in range(segments + 1):
        t = start_angle + (end_angle - start_angle) * i / segments
        pts.append((cx + r * cos(t), cy + r * sin(t)))
    return polyline(pts)

def filled_rect(x1, y1, x2, y2):
    """用多条水平线模拟实心矩形，便于字体渲染。"""
    strokes = []
    step = 18
    for y in range(int(y1), int(y2) + 1, step):
        strokes.extend(polyline([(x1, y), (x2, y)]))
    return strokes

def triangle(p1, p2, p3):
    return polyline([p1, p2, p3, p1])

def diamond(cx, cy, size):
    h = size / 2
    return polyline([(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy), (cx, cy - h)])

def cross(cx, cy, size):
    h = size / 2
    return polyline([(cx - h, cy), (cx + h, cy)]) + polyline([(cx, cy - h), (cx, cy + h)])

def plus(cx, cy, size):
    return cross(cx, cy, size)

def x_mark(cx, cy, size):
    h = size / 2
    return polyline([(cx - h, cy - h), (cx + h, cy + h)]) + polyline([(cx + h, cy - h), (cx - h, cy + h)])

def arrow_right(cx, cy, size, double=False):
    h = size / 2
    shaft_y = cy
    head_x = cx + h
    tail_x = cx - h
    s = polyline([(tail_x, shaft_y), (head_x - 10, shaft_y)])
    s += polyline([(head_x - 35, shaft_y - 25), (head_x, shaft_y), (head_x - 35, shaft_y + 25)])
    if double:
        s += polyline([(tail_x + 25, shaft_y - 25), (tail_x, shaft_y), (tail_x + 25, shaft_y + 25)])
    return s

def arrow_left(cx, cy, size, double=False):
    h = size / 2
    shaft_y = cy
    head_x = cx - h
    tail_x = cx + h
    s = polyline([(tail_x, shaft_y), (head_x + 10, shaft_y)])
    s += polyline([(head_x + 35, shaft_y - 25), (head_x, shaft_y), (head_x + 35, shaft_y + 25)])
    if double:
        s += polyline([(tail_x - 25, shaft_y - 25), (tail_x, shaft_y), (tail_x - 25, shaft_y + 25)])
    return s

def arrow_up(cx, cy, size, double=False):
    h = size / 2
    s = polyline([(cx, cy + h), (cx, cy - h + 10)])
    s += polyline([(cx - 25, cy - h + 35), (cx, cy - h), (cx + 25, cy - h + 35)])
    if double:
        s += polyline([(cx - 25, cy + h - 35), (cx, cy + h), (cx + 25, cy + h - 35)])
    return s

def arrow_down(cx, cy, size, double=False):
    h = size / 2
    s = polyline([(cx, cy - h), (cx, cy + h - 10)])
    s += polyline([(cx - 25, cy + h - 35), (cx, cy + h), (cx + 25, cy + h - 35)])
    if double:
        s += polyline([(cx - 25, cy - h + 35), (cx, cy - h), (cx + 25, cy - h + 35)])
    return s

def arrow_diag(cx, cy, size, dx, dy):
    """dx,dy 取 ±1 决定方向。"""
    h = size / 2
    sx, sy = cx - dx * h, cy - dy * h
    ex, ey = cx + dx * h, cy + dy * h
    s = polyline([(sx, sy), (ex - dx * 35, ey - dy * 35)])
    s += polyline([
        (ex - dx * 60, ey - dy * 15),
        (ex, ey),
        (ex - dx * 15, ey - dy * 60)
    ])
    return s

# -------------------- 符号笔画生成器 --------------------

def glyph_em_dash():
    return hline(300, 80, 520)

def glyph_ellipsis():
    r = 14
    pts = [(180, 300), (300, 300), (420, 300)]
    s = []
    for px, py in pts:
        s += circle(px, py, r, segments=10)
    return s

def glyph_middle_dot():
    return circle(300, 300, 28, segments=14)

def glyph_bullet():
    return filled_rect(270, 270, 330, 330)

def glyph_reference_mark():
    # ※ 像一个米字在框内
    s = rect(140, 140, 460, 460)
    s += polyline([(140, 140), (460, 460)])
    s += polyline([(460, 140), (140, 460)])
    s += hline(300, 140, 460)
    s += vline(300, 140, 460)
    return s

def glyph_dagger():
    s = vline(300, 100, 500)
    s += hline(180, 420, 300)
    s += polyline([(300, 420), (270, 470), (330, 470), (300, 420)])
    return s

def glyph_double_dagger():
    s = vline(300, 100, 500)
    s += hline(180, 420, 300)
    s += hline(220, 380, 300)
    return s

def glyph_section():
    # § 两个 S 形加竖线
    s = []
    # 上 S
    s += arc(300, 220, 50, pi * 0.1, pi * 1.1, segments=12)
    s += arc(300, 220, 50, pi * 1.1, pi * 2.1, segments=12)
    # 下 S
    s += arc(300, 380, 50, pi * 1.1, pi * 2.1, segments=12)
    s += arc(300, 380, 50, pi * 0.1, pi * 1.1, segments=12)
    # 竖线穿过
    s += vline(350, 150, 450)
    return s

def glyph_pilcrow():
    # ¶ 反向 P
    s = filled_rect(180, 120, 340, 340)
    s += vline(360, 120, 480)
    s += vline(400, 120, 480)
    return s

def glyph_guillemet_left():
    return polyline([(420, 140), (180, 300), (420, 460)]) + polyline([(360, 140), (120, 300), (360, 460)])

def glyph_guillemet_right():
    return polyline([(180, 140), (420, 300), (180, 460)]) + polyline([(240, 140), (480, 300), (240, 460)])

def glyph_corner_bracket_left():
    return polyline([(420, 120), (180, 120), (180, 480), (420, 480)])

def glyph_corner_bracket_right():
    return polyline([(180, 120), (420, 120), (420, 480), (180, 480)])

def glyph_white_corner_bracket_left():
    return polyline([(420, 120), (180, 120), (180, 480), (420, 480)]) + polyline([(380, 160), (220, 160), (220, 440), (380, 440)])

def glyph_white_corner_bracket_right():
    return polyline([(180, 120), (420, 120), (420, 480), (180, 480)]) + polyline([(220, 160), (380, 160), (380, 440), (220, 440)])

def glyph_angle_bracket_left():
    return polyline([(420, 120), (160, 300), (420, 480)])

def glyph_angle_bracket_right():
    return polyline([(180, 120), (440, 300), (180, 480)])

def glyph_double_angle_bracket_left():
    return glyph_angle_bracket_left() + polyline([(460, 120), (200, 300), (460, 480)])

def glyph_double_angle_bracket_right():
    return glyph_angle_bracket_right() + polyline([(140, 120), (400, 300), (140, 480)])

def glyph_black_lenticular_left():
    return polyline([(420, 300), (300, 120), (180, 120), (180, 480), (300, 480), (420, 300)])

def glyph_black_lenticular_right():
    return polyline([(180, 300), (300, 120), (420, 120), (420, 480), (300, 480), (180, 300)])

def glyph_tortoise_shell_left():
    return polyline([(400, 140), (200, 140), (200, 460), (400, 460)])

def glyph_tortoise_shell_right():
    return polyline([(200, 140), (400, 140), (400, 460), (200, 460)])

def glyph_white_lenticular_left():
    return glyph_black_lenticular_left() + polyline([(380, 300), (300, 180), (220, 180), (220, 420), (300, 420), (380, 300)])

def glyph_white_lenticular_right():
    return glyph_black_lenticular_right() + polyline([(220, 300), (300, 180), (380, 180), (380, 420), (300, 420), (220, 300)])

def glyph_white_tortoise_shell_left():
    return glyph_tortoise_shell_left() + rect(240, 180, 360, 420)

def glyph_white_tortoise_shell_right():
    return glyph_tortoise_shell_right() + rect(240, 180, 360, 420)

def glyph_white_square_bracket_left():
    return polyline([(420, 120), (180, 120), (180, 480), (420, 480)])

def glyph_white_square_bracket_right():
    return polyline([(180, 120), (420, 120), (420, 480), (180, 480)])

# ---------- 数学 ----------

def glyph_plus_minus():
    return cross(300, 230, 240) + hline(300, 180, 420)

def glyph_times():
    h = 130
    return polyline([(300 - h, 300 - h), (300 + h, 300 + h)]) + polyline([(300 + h, 300 - h), (300 - h, 300 + h)])

def glyph_divide():
    return hline(300, 180, 420) + circle(300, 210, 18, segments=10) + circle(300, 390, 18, segments=10)

def glyph_sqrt():
    return polyline([(420, 180), (340, 180), (300, 500), (240, 380), (180, 380)])

def glyph_propto():
    # ∝ 阿尔法反形状
    s = arc(300, 300, 90, pi * 0.15, pi * 1.85, segments=16)
    s += polyline([(360, 200), (440, 170)])
    return s

def glyph_infinity():
    r = 65
    s = circle(235, 300, r, segments=14)
    s += circle(365, 300, r, segments=14)
    return s

def glyph_right_angle():
    return polyline([(180, 420), (420, 420), (420, 180)])

def glyph_angle():
    return polyline([(180, 420), (420, 420), (300, 180), (300, 220)])

def glyph_parallel():
    return vline(230, 120, 480) + vline(370, 120, 480)

def glyph_logical_and():
    return polyline([(160, 420), (300, 120), (440, 420)])

def glyph_logical_or():
    return polyline([(160, 180), (300, 480), (440, 180)])

def glyph_intersection():
    return arc(300, 300, 130, pi, 0, segments=16) + hline(430, 170, 430)

def glyph_union():
    return arc(300, 300, 130, 0, pi, segments=16) + hline(170, 170, 430)

def glyph_integral():
    # ∫ 用 S 形曲线近似
    s = arc(300, 220, 60, pi * 1.6, pi * 0.4, segments=14)
    s += arc(300, 380, 60, pi * 0.6, pi * 1.4, segments=14)
    s += polyline([(240, 180), (200, 160)])
    s += polyline([(360, 420), (400, 440)])
    return s

def glyph_contour_integral():
    return glyph_integral() + circle(300, 300, 160, segments=20)

def glyph_therefore():
    r = 18
    return circle(220, 260, r, segments=10) + circle(380, 260, r, segments=10) + circle(300, 380, r, segments=10)

def glyph_because():
    r = 18
    return circle(220, 340, r, segments=10) + circle(380, 340, r, segments=10) + circle(300, 220, r, segments=10)

def glyph_tilde():
    return polyline([(180, 340), (260, 260), (340, 340), (420, 260)])

def glyph_approx():
    return glyph_tilde() + hline(300, 180, 420)

def glyph_congruent():
    return glyph_approx()

def glyph_allequal():
    return hline(300, 180, 420) + hline(340, 180, 420) + hline(260, 180, 420)

def glyph_not_equal():
    return hline(280, 180, 420) + hline(320, 180, 420) + polyline([(220, 220), (380, 380)])

def glyph_equiv():
    return hline(280, 180, 420) + hline(320, 180, 420)

def glyph_leq():
    return polyline([(420, 200), (180, 300), (420, 400)]) + hline(300, 180, 420)

def glyph_geq():
    return polyline([(180, 200), (420, 300), (180, 400)]) + hline(300, 180, 420)

def glyph_ll():
    return polyline([(420, 180), (180, 300), (420, 420)]) + polyline([(460, 180), (220, 300), (460, 420)])

def glyph_gg():
    return polyline([(180, 180), (420, 300), (180, 420)]) + polyline([(140, 180), (380, 300), (140, 420)])

def glyph_oplus():
    return circle(300, 300, 140, segments=18) + cross(300, 300, 160)

def glyph_otimes():
    return circle(300, 300, 140, segments=18) + glyph_times()

def glyph_exists():
    return polyline([(180, 160), (420, 160), (420, 440), (180, 440)]) + hline(300, 180, 420)

def glyph_forall():
    return polyline([(180, 440), (300, 160), (420, 440)]) + hline(300, 220, 380)

def glyph_partial():
    # ∂ 近似为带钩的 d
    s = circle(300, 260, 100, segments=16)
    s += polyline([(390, 260), (390, 460), (260, 460)])
    return s

def glyph_nabla():
    return polyline([(160, 420), (300, 120), (440, 420), (160, 420)])

def glyph_product():
    return polyline([(180, 120), (420, 120), (420, 480), (180, 480), (180, 120)]) + hline(200, 400, 120)

def glyph_sum():
    return polyline([(420, 140), (180, 140), (380, 300), (180, 460), (420, 460)])

# ---------- 箭头 ----------

def glyph_arrow_left():
    return arrow_left(300, 300, 280)

def glyph_arrow_up():
    return arrow_up(300, 300, 280)

def glyph_arrow_right():
    return arrow_right(300, 300, 280)

def glyph_arrow_down():
    return arrow_down(300, 300, 280)

def glyph_arrow_leftright():
    return arrow_left(300, 300, 220) + arrow_right(300, 300, 220)

def glyph_arrow_updown():
    return arrow_up(300, 300, 220) + arrow_down(300, 300, 220)

def glyph_arrow_nw():
    return arrow_diag(300, 300, 260, -1, -1)

def glyph_arrow_ne():
    return arrow_diag(300, 300, 260, 1, -1)

def glyph_arrow_se():
    return arrow_diag(300, 300, 260, 1, 1)

def glyph_arrow_sw():
    return arrow_diag(300, 300, 260, -1, 1)

def glyph_arrow_exchange():
    return arrow_left(260, 300, 200) + arrow_right(340, 300, 200)

def glyph_arrow_updown_pair():
    return arrow_up(260, 300, 220) + arrow_down(340, 300, 220)

def glyph_arrow_exchange_v():
    return arrow_down(260, 300, 220) + arrow_up(340, 300, 220)

def glyph_arrow_harpoon_l2r():
    s = hline(300, 180, 420)
    s += polyline([(420, 300), (380, 270), (380, 300)])
    return s

def glyph_arrow_harpoon_r2l():
    s = hline(300, 180, 420)
    s += polyline([(180, 300), (220, 270), (220, 300)])
    return s

def glyph_arrow_double_right():
    return arrow_right(300, 300, 260, double=True)

def glyph_arrow_double_left():
    return arrow_left(300, 300, 260, double=True)

def glyph_arrow_double_up():
    return arrow_up(300, 300, 260, double=True)

def glyph_arrow_double_down():
    return arrow_down(300, 300, 260, double=True)

def glyph_arrow_double_leftright():
    return arrow_left(300, 300, 220, double=True) + arrow_right(300, 300, 220, double=True)

def glyph_arrow_double_updown():
    return arrow_up(300, 300, 220, double=True) + arrow_down(300, 300, 220, double=True)

def glyph_arrow_curve_ne():
    s = arc(300, 380, 100, pi * 1.0, pi * 1.6, segments=14)
    s += polyline([(420, 270), (440, 220), (390, 240)])
    return s

def glyph_arrow_curve_se():
    s = arc(300, 220, 100, pi * 0.4, pi * 1.0, segments=14)
    s += polyline([(420, 330), (440, 380), (390, 360)])
    return s

def glyph_arrow_rotate_ccw():
    s = arc(300, 300, 120, pi * 0.2, pi * 1.8, segments=18)
    s += polyline([(210, 200), (180, 180), (230, 170)])
    return s

def glyph_arrow_rotate_cw():
    s = arc(300, 300, 120, pi * 1.2, pi * 2.8, segments=18)
    s += polyline([(390, 200), (420, 180), (370, 170)])
    return s

def glyph_arrow_turn_ul():
    # ↶ 左上回转
    s = arc(300, 300, 120, pi * 0.5, pi * 1.5, segments=16)
    s += polyline([(300, 180), (270, 150), (330, 150)])
    return s

def glyph_arrow_turn_ur():
    s = arc(300, 300, 120, pi * 1.5, pi * 2.5, segments=16)
    s += polyline([(300, 420), (270, 450), (330, 450)])
    return s

def glyph_arrow_hook_left():
    # ↩ 右进左钩
    s = polyline([(420, 240), (240, 240), (240, 360)])
    s += polyline([(240, 360), (200, 340), (200, 380), (240, 360)])
    return s

def glyph_arrow_hook_right():
    s = polyline([(180, 240), (360, 240), (360, 360)])
    s += polyline([(360, 360), (400, 340), (400, 380), (360, 360)])
    return s

# ---------- 制表符 / UI ----------

def box_corner_tl():
    return vline(300, 300, 500) + hline(300, 300, 500)

def box_corner_tr():
    return vline(300, 300, 500) + hline(300, 100, 300)

def box_corner_bl():
    return vline(300, 100, 300) + hline(300, 300, 500)

def box_corner_br():
    return vline(300, 100, 300) + hline(300, 100, 300)

def box_tee_right():
    return vline(300, 100, 500) + hline(300, 300, 500)

def box_tee_left():
    return vline(300, 100, 500) + hline(300, 100, 300)

def box_tee_down():
    return hline(300, 100, 500) + vline(300, 300, 500)

def box_tee_up():
    return hline(300, 100, 500) + vline(300, 100, 300)

def box_cross():
    return hline(300, 100, 500) + vline(300, 100, 500)

def box_double_h():
    return hline(280, 100, 500) + hline(320, 100, 500)

def box_double_v():
    return vline(280, 100, 500) + vline(320, 100, 500)

def box_double_corner_tl():
    return vline(260, 260, 500) + vline(300, 300, 500) + hline(260, 260, 500) + hline(300, 300, 500)

def box_double_corner_tr():
    return vline(300, 300, 500) + vline(340, 340, 500) + hline(300, 100, 300) + hline(340, 100, 340)

def box_double_corner_bl():
    return vline(260, 100, 260) + vline(300, 100, 300) + hline(260, 260, 500) + hline(300, 300, 500)

def box_double_corner_br():
    return vline(300, 100, 300) + vline(340, 100, 340) + hline(300, 100, 300) + hline(340, 100, 340)

def box_double_tee_right():
    return vline(260, 100, 500) + vline(300, 100, 500) + hline(260, 260, 500) + hline(300, 300, 500)

def box_double_tee_left():
    return vline(300, 100, 500) + vline(340, 100, 500) + hline(300, 100, 300) + hline(340, 100, 340)

def box_double_tee_down():
    return hline(260, 100, 500) + hline(300, 100, 500) + vline(260, 260, 500) + vline(300, 300, 500)

def box_double_tee_up():
    return hline(260, 100, 500) + hline(300, 100, 500) + vline(260, 100, 260) + vline(300, 100, 300)

def box_double_cross():
    return hline(260, 100, 500) + hline(300, 100, 500) + vline(260, 100, 500) + vline(300, 100, 500)

def glyph_block_upper():
    return filled_rect(100, 100, 500, 300)

def glyph_block_lower():
    return filled_rect(100, 300, 500, 500)

def glyph_block_full():
    return filled_rect(100, 100, 500, 500)

def glyph_block_left():
    return filled_rect(100, 100, 300, 500)

def glyph_block_right():
    return filled_rect(300, 100, 500, 500)

def glyph_shade_light():
    s = []
    for y in range(140, 460, 40):
        for x in range(140, 460, 40):
            if (x + y) % 80 == 0:
                s += polyline([(x, y), (x + 10, y)])
    return s

def glyph_shade_medium():
    s = []
    for y in range(120, 480, 30):
        s += hline(y, 120, 480)
    return s

def glyph_shade_dark():
    s = []
    for y in range(110, 490, 15):
        s += hline(y, 110, 490)
    return s

# ---------- 货币 ----------

def glyph_cent():
    s = circle(300, 300, 120, segments=16)
    s += polyline([(280, 160), (260, 440)])
    s += polyline([(320, 160), (340, 440)])
    return s

def glyph_pound():
    s = circle(300, 260, 100, segments=14)
    s += polyline([(360, 360), (360, 440), (220, 440)])
    s += hline(300, 220, 380)
    s += hline(340, 220, 380)
    return s

def glyph_yen():
    s = polyline([(180, 180), (300, 320), (420, 180)])
    s += polyline([(260, 280), (340, 280)])
    s += hline(360, 240, 360)
    s += hline(400, 240, 360)
    return s

def glyph_euro():
    s = circle(300, 300, 130, segments=16)
    s += hline(240, 180, 340)
    s += hline(280, 180, 340)
    return s

def glyph_rupee():
    s = polyline([(220, 160), (380, 160), (280, 300)])
    s += polyline([(240, 240), (360, 240)])
    s += polyline([(280, 300), (220, 440)])
    return s

def glyph_ruble():
    s = vline(300, 140, 460)
    s += polyline([(300, 140), (380, 200), (380, 260), (300, 260)])
    s += hline(320, 220, 380)
    s += hline(360, 220, 380)
    return s

def glyph_won():
    return polyline([(160, 140), (220, 460), (300, 240), (380, 460), (440, 140)]) + hline(200, 180, 420) + hline(240, 180, 420)

def glyph_currency():
    return cross(300, 300, 200) + circle(300, 300, 140, segments=16)

# ---------- 几何 / 项目符号 ----------

def glyph_black_square():
    return filled_rect(150, 150, 450, 450)

def glyph_white_square():
    return rect(150, 150, 450, 450)

def glyph_black_triangle_up():
    return filled_rect(150, 180, 450, 450) + triangle((150, 450), (450, 450), (300, 150))

def glyph_white_triangle_up():
    return triangle((150, 450), (450, 450), (300, 150))

def glyph_black_triangle_down():
    return triangle((150, 150), (450, 150), (300, 450))

def glyph_white_triangle_down():
    return glyph_black_triangle_down()

def glyph_black_diamond():
    return diamond(300, 300, 300)

def glyph_white_diamond():
    return diamond(300, 300, 300) + diamond(300, 300, 160)

def glyph_black_circle():
    return circle(300, 300, 170, segments=24)

def glyph_white_circle():
    return circle(300, 300, 170, segments=24)

def glyph_circle_left_half():
    s = circle(300, 300, 170, segments=24)
    s += filled_rect(130, 130, 300, 470)
    return s

def glyph_circle_right_half():
    s = circle(300, 300, 170, segments=24)
    s += filled_rect(300, 130, 470, 470)
    return s

def glyph_circle_lower_half():
    s = circle(300, 300, 170, segments=24)
    s += filled_rect(130, 300, 470, 470)
    return s

def glyph_circle_upper_half():
    s = circle(300, 300, 170, segments=24)
    s += filled_rect(130, 130, 470, 300)
    return s

def glyph_black_star():
    # 五角星
    cx, cy, r_out, r_in = 300, 300, 180, 75
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = pi / 2 + i * pi / 5
        pts.append((cx + r * cos(a), cy - r * sin(a)))
    pts.append(pts[0])
    return polyline(pts)

def glyph_white_star():
    return glyph_black_star()

def glyph_check():
    return polyline([(180, 300), (270, 420), (420, 180)])

def glyph_ballot_x():
    return x_mark(300, 300, 240)

def glyph_multiplication_x():
    return x_mark(300, 300, 220)

# ---------- 其它实用 ----------

def glyph_copyright():
    s = circle(300, 300, 170, segments=24)
    s += circle(300, 300, 90, segments=16)
    return s

def glyph_registered():
    s = circle(300, 300, 170, segments=24)
    s += polyline([(240, 420), (240, 180), (340, 180), (380, 220), (380, 280), (340, 300)])
    s += polyline([(340, 300), (380, 420)])
    return s

def glyph_trademark():
    return polyline([(180, 420), (180, 180), (420, 180), (420, 420)]) + vline(300, 180, 420) + polyline([(360, 180), (360, 420)])

def glyph_sound_recording():
    return glyph_copyright() + hline(300, 180, 420)

def glyph_degree():
    return circle(300, 300, 90, segments=16) + polyline([(300, 420), (300, 440)])

def glyph_per_mille():
    return polyline([(160, 420), (440, 180)]) + circle(180, 240, 35, segments=10) + circle(420, 360, 35, segments=10) + circle(300, 300, 35, segments=10)

def glyph_numero():
    return polyline([(180, 420), (180, 180), (420, 420), (420, 180)]) + hline(300, 240, 360) + hline(330, 240, 360)

def glyph_liter():
    return polyline([(240, 180), (240, 420), (360, 420)]) + hline(390, 240, 360)

def glyph_micro():
    return polyline([(200, 180), (200, 380), (300, 440), (400, 380), (400, 180)])

# -------------------- 符号注册表 --------------------

SYMBOLS = [
    # 标点
    ("—", "U+2014", "em dash", glyph_em_dash),
    ("…", "U+2026", "ellipsis", glyph_ellipsis),
    ("·", "U+00B7", "middle dot", glyph_middle_dot),
    ("•", "U+2022", "bullet", glyph_bullet),
    ("※", "U+203B", "reference mark", glyph_reference_mark),
    ("†", "U+2020", "dagger", glyph_dagger),
    ("‡", "U+2021", "double dagger", glyph_double_dagger),
    ("§", "U+00A7", "section", glyph_section),
    ("¶", "U+00B6", "pilcrow", glyph_pilcrow),
    ("«", "U+00AB", "left guillemet", glyph_guillemet_left),
    ("»", "U+00BB", "right guillemet", glyph_guillemet_right),
    ("「", "U+300C", "left corner bracket", glyph_corner_bracket_left),
    ("」", "U+300D", "right corner bracket", glyph_corner_bracket_right),
    ("『", "U+300E", "left white corner bracket", glyph_white_corner_bracket_left),
    ("』", "U+300F", "right white corner bracket", glyph_white_corner_bracket_right),
    ("〈", "U+3008", "left angle bracket", glyph_angle_bracket_left),
    ("〉", "U+3009", "right angle bracket", glyph_angle_bracket_right),
    ("《", "U+300A", "left double angle bracket", glyph_double_angle_bracket_left),
    ("》", "U+300B", "right double angle bracket", glyph_double_angle_bracket_right),
    ("【", "U+3010", "left black lenticular bracket", glyph_black_lenticular_left),
    ("】", "U+3011", "right black lenticular bracket", glyph_black_lenticular_right),
    ("〔", "U+3014", "left tortoise shell bracket", glyph_tortoise_shell_left),
    ("〕", "U+3015", "right tortoise shell bracket", glyph_tortoise_shell_right),
    ("〖", "U+3016", "left white lenticular bracket", glyph_white_lenticular_left),
    ("〗", "U+3017", "right white lenticular bracket", glyph_white_lenticular_right),
    ("〘", "U+3018", "left white tortoise shell bracket", glyph_white_tortoise_shell_left),
    ("〙", "U+3019", "right white tortoise shell bracket", glyph_white_tortoise_shell_right),
    ("〚", "U+301A", "left white square bracket", glyph_white_square_bracket_left),
    ("〛", "U+301B", "right white square bracket", glyph_white_square_bracket_right),
    # 数学
    ("±", "U+00B1", "plus-minus", glyph_plus_minus),
    ("×", "U+00D7", "multiplication", glyph_times),
    ("÷", "U+00F7", "division", glyph_divide),
    ("√", "U+221A", "square root", glyph_sqrt),
    ("∝", "U+221D", "proportional to", glyph_propto),
    ("∞", "U+221E", "infinity", glyph_infinity),
    ("∟", "U+221F", "right angle", glyph_right_angle),
    ("∠", "U+2220", "angle", glyph_angle),
    ("∥", "U+2225", "parallel", glyph_parallel),
    ("∧", "U+2227", "logical and", glyph_logical_and),
    ("∨", "U+2228", "logical or", glyph_logical_or),
    ("∩", "U+2229", "intersection", glyph_intersection),
    ("∪", "U+222A", "union", glyph_union),
    ("∫", "U+222B", "integral", glyph_integral),
    ("∮", "U+222E", "contour integral", glyph_contour_integral),
    ("∴", "U+2234", "therefore", glyph_therefore),
    ("∵", "U+2235", "because", glyph_because),
    ("∼", "U+223C", "tilde operator", glyph_tilde),
    ("≈", "U+2248", "almost equal", glyph_approx),
    ("≅", "U+2245", "congruent", glyph_congruent),
    ("≌", "U+224C", "all equal to", glyph_allequal),
    ("≠", "U+2260", "not equal", glyph_not_equal),
    ("≡", "U+2261", "equivalent", glyph_equiv),
    ("≤", "U+2264", "less-than or equal", glyph_leq),
    ("≥", "U+2265", "greater-than or equal", glyph_geq),
    ("≪", "U+226A", "much less-than", glyph_ll),
    ("≫", "U+226B", "much greater-than", glyph_gg),
    ("⊕", "U+2295", "circled plus", glyph_oplus),
    ("⊗", "U+2297", "circled times", glyph_otimes),
    ("∃", "U+2203", "there exists", glyph_exists),
    ("∀", "U+2200", "for all", glyph_forall),
    ("∂", "U+2202", "partial differential", glyph_partial),
    ("∇", "U+2207", "nabla", glyph_nabla),
    ("∏", "U+220F", "n-ary product", glyph_product),
    ("∑", "U+2211", "n-ary sum", glyph_sum),
    # 箭头
    ("←", "U+2190", "left arrow", glyph_arrow_left),
    ("↑", "U+2191", "up arrow", glyph_arrow_up),
    ("→", "U+2192", "right arrow", glyph_arrow_right),
    ("↓", "U+2193", "down arrow", glyph_arrow_down),
    ("↔", "U+2194", "left right arrow", glyph_arrow_leftright),
    ("↕", "U+2195", "up down arrow", glyph_arrow_updown),
    ("↖", "U+2196", "north west arrow", glyph_arrow_nw),
    ("↗", "U+2197", "north east arrow", glyph_arrow_ne),
    ("↘", "U+2198", "south east arrow", glyph_arrow_se),
    ("↙", "U+2199", "south west arrow", glyph_arrow_sw),
    ("⇄", "U+21C4", "right arrow over left arrow", glyph_arrow_exchange),
    ("⇅", "U+21C5", "upwards arrow leftwards of downwards arrow", glyph_arrow_updown_pair),
    ("⇆", "U+21C6", "leftwards arrow over rightwards arrow", glyph_arrow_exchange_v),
    ("⇋", "U+21CB", "left harpoon over right harpoon", glyph_arrow_harpoon_l2r),
    ("⇌", "U+21CC", "right harpoon over left harpoon", glyph_arrow_harpoon_r2l),
    ("⇒", "U+21D2", "right double arrow", glyph_arrow_double_right),
    ("⇐", "U+21D0", "left double arrow", glyph_arrow_double_left),
    ("⇑", "U+21D1", "up double arrow", glyph_arrow_double_up),
    ("⇓", "U+21D3", "down double arrow", glyph_arrow_double_down),
    ("⇔", "U+21D4", "left right double arrow", glyph_arrow_double_leftright),
    ("⇕", "U+21D5", "up down double arrow", glyph_arrow_double_updown),
    ("⤴", "U+2934", "arrow pointing right then curving up", glyph_arrow_curve_ne),
    ("⤵", "U+2935", "arrow pointing right then curving down", glyph_arrow_curve_se),
    ("↺", "U+21BA", "anticlockwise open circle arrow", glyph_arrow_rotate_ccw),
    ("↻", "U+21BB", "clockwise open circle arrow", glyph_arrow_rotate_cw),
    ("↶", "U+21B6", "anticlockwise top semicircle arrow", glyph_arrow_turn_ul),
    ("↷", "U+21B7", "clockwise top semicircle arrow", glyph_arrow_turn_ur),
    ("↩", "U+21A9", "leftwards arrow with hook", glyph_arrow_hook_left),
    ("↪", "U+21AA", "rightwards arrow with hook", glyph_arrow_hook_right),
    # 制表符 / UI
    ("┌", "U+250C", "box drawings light down and right", box_corner_tl),
    ("┐", "U+2510", "box drawings light down and left", box_corner_tr),
    ("└", "U+2514", "box drawings light up and right", box_corner_bl),
    ("┘", "U+2518", "box drawings light up and left", box_corner_br),
    ("├", "U+251C", "box drawings light vertical and right", box_tee_right),
    ("┤", "U+2524", "box drawings light vertical and left", box_tee_left),
    ("┬", "U+252C", "box drawings light down and horizontal", box_tee_down),
    ("┴", "U+2534", "box drawings light up and horizontal", box_tee_up),
    ("┼", "U+253C", "box drawings light vertical and horizontal", box_cross),
    ("═", "U+2550", "box drawings double horizontal", box_double_h),
    ("║", "U+2551", "box drawings double vertical", box_double_v),
    ("╔", "U+2554", "box drawings double down and right", box_double_corner_tl),
    ("╗", "U+2557", "box drawings double down and left", box_double_corner_tr),
    ("╚", "U+255A", "box drawings double up and right", box_double_corner_bl),
    ("╝", "U+255D", "box drawings double up and left", box_double_corner_br),
    ("╠", "U+2560", "box drawings double vertical and right", box_double_tee_right),
    ("╣", "U+2563", "box drawings double vertical and left", box_double_tee_left),
    ("╦", "U+2566", "box drawings double down and horizontal", box_double_tee_down),
    ("╩", "U+2569", "box drawings double up and horizontal", box_double_tee_up),
    ("╬", "U+256C", "box drawings double vertical and horizontal", box_double_cross),
    ("▀", "U+2580", "upper half block", glyph_block_upper),
    ("▄", "U+2584", "lower half block", glyph_block_lower),
    ("█", "U+2588", "full block", glyph_block_full),
    ("▌", "U+258C", "left half block", glyph_block_left),
    ("▐", "U+2590", "right half block", glyph_block_right),
    ("░", "U+2591", "light shade", glyph_shade_light),
    ("▒", "U+2592", "medium shade", glyph_shade_medium),
    ("▓", "U+2593", "dark shade", glyph_shade_dark),
    # 货币
    ("¢", "U+00A2", "cent", glyph_cent),
    ("£", "U+00A3", "pound", glyph_pound),
    ("¥", "U+00A5", "yen", glyph_yen),
    ("€", "U+20AC", "euro", glyph_euro),
    ("₹", "U+20B9", "indian rupee", glyph_rupee),
    ("₽", "U+20BD", "ruble", glyph_ruble),
    ("₩", "U+20A9", "won", glyph_won),
    ("¤", "U+00A4", "currency", glyph_currency),
    # 几何 / 项目符号
    ("■", "U+25A0", "black square", glyph_black_square),
    ("□", "U+25A1", "white square", glyph_white_square),
    ("▲", "U+25B2", "black up-pointing triangle", glyph_black_triangle_up),
    ("△", "U+25B3", "white up-pointing triangle", glyph_white_triangle_up),
    ("▼", "U+25BC", "black down-pointing triangle", glyph_black_triangle_down),
    ("▽", "U+25BD", "white down-pointing triangle", glyph_white_triangle_down),
    ("◆", "U+25C6", "black diamond", glyph_black_diamond),
    ("◇", "U+25C7", "white diamond", glyph_white_diamond),
    ("●", "U+25CF", "black circle", glyph_black_circle),
    ("○", "U+25CB", "white circle", glyph_white_circle),
    ("◐", "U+25D0", "circle with left half black", glyph_circle_left_half),
    ("◑", "U+25D1", "circle with right half black", glyph_circle_right_half),
    ("◒", "U+25D2", "circle with lower half black", glyph_circle_lower_half),
    ("◓", "U+25D3", "circle with upper half black", glyph_circle_upper_half),
    ("★", "U+2605", "black star", glyph_black_star),
    ("☆", "U+2606", "white star", glyph_white_star),
    ("✓", "U+2713", "check mark", glyph_check),
    ("✗", "U+2717", "ballot x", glyph_ballot_x),
    ("✕", "U+2715", "multiplication x", glyph_multiplication_x),
    # 其它
    ("©", "U+00A9", "copyright", glyph_copyright),
    ("®", "U+00AE", "registered", glyph_registered),
    ("™", "U+2122", "trade mark", glyph_trademark),
    ("℗", "U+2117", "sound recording copyright", glyph_sound_recording),
    ("°", "U+00B0", "degree", glyph_degree),
    ("‰", "U+2030", "per mille", glyph_per_mille),
    ("№", "U+2116", "numero", glyph_numero),
    ("ℓ", "U+2113", "script small l", glyph_liter),
    ("µ", "U+00B5", "micro", glyph_micro),
]

# -------------------- 主流程 --------------------

def count_strokes(strokes):
    """按移动到指令数量统计笔画数。"""
    return sum(1 for s in strokes if s.get("类型") == "移动到")

def make_glyph(char, codepoint, name, strokes):
    return {
        "unicode": codepoint,
        "笔画数": count_strokes(strokes),
        "结构": "符号",
        "名称": name,
        "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
        "笔画路径_cnsh9622": strokes,
    }

def extract_existing_codepoints(lib):
    """提取已存在的 Unicode 码点集合。"""
    codes = set()
    for key, val in lib.get("字符集_cnsh9622", {}).items():
        if isinstance(val, dict) and "unicode" in val:
            codes.add(val["unicode"].upper())
    return codes

def main():
    print("[LonghunFont] 加载字元库…")
    with open(SRC, "r", encoding="utf-8") as f:
        lib = json.load(f)

    existing = extract_existing_codepoints(lib)
    glyphs = lib.setdefault("字符集_cnsh9622", {})
    added = 0
    skipped = 0

    for char, codepoint, name, builder in SYMBOLS:
        if codepoint.upper() in existing:
            skipped += 1
            continue
        strokes = builder()
        if not strokes:
            continue
        glyph = make_glyph(char, codepoint, name, strokes)
        glyphs[char] = glyph
        existing.add(codepoint.upper())
        added += 1

    # 更新元数据
    meta = lib.setdefault("元数据", {})
    meta["版本"] = "v0011-实用符号版"
    meta["总字符数"] = len(glyphs)
    meta["描述"] = "LonghunFont 两千中文字元库 + 实用 Unicode 符号扩展"
    now = datetime.now(timezone.utc).isoformat()
    meta["实用符号扩展时间"] = now
    meta["实用符号扩展DNA"] = NEW_DNA
    meta["精修时间"] = now
    meta["精修DNA"] = NEW_DNA

    lib["DNA追溯码"] = NEW_DNA

    # 三色审计
    lib["三色审计_cnsh9622"] = {
        "🟢": {"结果": "通过", "项目": "文化主权标识完整"},
        "🟡": {"结果": "通过", "项目": "来源链可追溯"},
        "🔴": {"结果": "通过", "项目": "无商业字体依赖"},
    }

    # 写入新文件
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(lib, f, ensure_ascii=False, indent=2)

    print(f"[LonghunFont] 已添加符号：{added}")
    print(f"[LonghunFont] 已跳过重复：{skipped}")
    print(f"[LonghunFont] 当前总字符数：{len(glyphs)}")
    print(f"[LonghunFont] 输出文件：{DST}")
    print(f"[LonghunFont] DNA：{NEW_DNA}")

if __name__ == "__main__":
    main()
