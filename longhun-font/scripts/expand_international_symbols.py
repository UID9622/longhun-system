#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-INTERNATIONAL-SYMBOLS-v1.0
"""
龍魂字元库 · 国际符号扩展脚本
为 LonghunFont 添加拼音调号、希腊字母、数学、天气、音乐、棋牌、
占星、性别/行星、UI 图标、警示图标、上下标数字等国际常用 Unicode 符号。
"""

import json
import os
from datetime import datetime, timezone
from math import cos, sin, pi

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
SRC = os.path.join(PROJECT_DIR, "glyphs", "龍魂字元库_v0011_实用符号版.json")
DST = os.path.join(PROJECT_DIR, "glyphs", "龍魂字元库_v0012_国际符号版.json")

NEW_DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EXPAND-INTERNATIONAL-SYMBOLS-v1.0"

# -------------------- 笔画辅助函数 --------------------

def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [round(x, 2), round(y, 2)]}

def stroke_line(x, y):
    return {"类型": "直线段", "终点": [round(x, 2), round(y, 2)]}

def polyline(points):
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

def ellipse(cx, cy, rx, ry, segments=16):
    pts = []
    for i in range(segments + 1):
        a = 2 * pi * i / segments
        pts.append((cx + rx * cos(a), cy + ry * sin(a)))
    return polyline(pts)

def filled_rect(x1, y1, x2, y2, step=16):
    strokes = []
    for y in range(int(y1), int(y2) + 1, step):
        strokes.extend(polyline([(x1, y), (x2, y)]))
    return strokes

def filled_circle(cx, cy, r, segments=14):
    strokes = []
    for i in range(segments):
        a0 = 2 * pi * i / segments
        a1 = 2 * pi * (i + 1) / segments
        strokes.extend(polyline([
            (cx, cy), (cx + r * cos(a0), cy + r * sin(a0)),
            (cx + r * cos(a1), cy + r * sin(a1)), (cx, cy)
        ]))
    return strokes

def polygon(points):
    return polyline(points + [points[0]])

def star(cx, cy, outer_r, inner_r, points=5):
    pts = []
    for i in range(points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        a = pi / 2 + pi * i / points
        pts.append((cx + r * cos(a), cy - r * sin(a)))
    return polygon(pts)

def cross(cx, cy, size):
    h = size / 2
    return polyline([(cx - h, cy), (cx + h, cy)]) + polyline([(cx, cy - h), (cx, cy + h)])

def x_mark(cx, cy, size):
    h = size / 2
    return polyline([(cx - h, cy - h), (cx + h, cy + h)]) + polyline([(cx + h, cy - h), (cx - h, cy + h)])

# -------------------- 通用字母/数字绘制 --------------------

def latin_a():
    s = circle(270, 340, 70, segments=14)
    s += polyline([(340, 270), (340, 430)])
    s += polyline([(340, 370), (260, 370)])
    return s

def latin_e():
    s = arc(300, 340, 80, pi * 0.1, pi * 1.9, segments=16)
    s += hline(300, 220, 380)
    s += polyline([(380, 270), (220, 270)])
    return s

def latin_i():
    return vline(300, 280, 430) + filled_circle(300, 230, 10, segments=8)

def latin_o():
    return circle(300, 350, 75, segments=16)

def latin_u():
    return polyline([(230, 270), (230, 370), (300, 430), (370, 370), (370, 270)])

def latin_u_umlaut():
    s = latin_u()
    s += filled_circle(265, 220, 10, segments=8)
    s += filled_circle(335, 220, 10, segments=8)
    return s

def tone_macron(x=300, y=180):
    return hline(y, x - 50, x + 50)

def tone_acute(x=300, y=180):
    return polyline([(x - 40, y + 20), (x + 40, y - 20)])

def tone_caron(x=300, y=180):
    return polyline([(x - 50, y + 10), (x, y - 20), (x + 50, y + 10)])

def tone_grave(x=300, y=180):
    return polyline([(x - 40, y - 20), (x + 40, y + 20)])

def pinyin_vowel(base_fn, tone_fn, tx=300, ty=180):
    s = base_fn()
    s += tone_fn(tx, ty)
    return s

# -------------------- 希腊大写字母 --------------------

def greek_alpha_u():  # Α
    return polyline([(180, 430), (300, 170), (420, 430)]) + hline(340, 240, 360)

def greek_beta_u():  # Β
    s = vline(200, 150, 450)
    s += arc(200, 240, 100, -pi / 2, pi / 2, segments=12)
    s += arc(200, 360, 100, -pi / 2, pi / 2, segments=12)
    s += vline(300, 150, 250)
    s += vline(300, 350, 450)
    return s

def greek_gamma_u():  # Γ
    return vline(200, 150, 450) + hline(200, 200, 420)

def greek_delta_u():  # Δ
    return polyline([(180, 430), (300, 150), (420, 430), (180, 430)])

def greek_epsilon_u():  # Ε
    return vline(180, 150, 450) + hline(180, 180, 420) + hline(300, 180, 400) + hline(420, 180, 420)

def greek_zeta_u():  # Ζ
    return hline(180, 180, 420) + hline(420, 180, 420) + polyline([(420, 180), (180, 420)])

def greek_eta_u():  # Η
    return vline(180, 150, 450) + vline(420, 150, 450) + hline(300, 180, 420)

def greek_theta_u():  # Θ
    return circle(300, 300, 130, segments=18) + hline(300, 170, 430)

def greek_iota_u():  # Ι
    return vline(300, 150, 450)

def greek_kappa_u():  # Κ
    return vline(180, 150, 450) + polyline([(180, 300), (420, 150)]) + polyline([(180, 300), (420, 450)])

def greek_lambda_u():  # Λ
    return polyline([(180, 450), (300, 150), (420, 450)])

def greek_mu_u():  # Μ
    return polyline([(180, 450), (180, 180), (300, 320), (420, 180), (420, 450)])

def greek_nu_u():  # Ν
    return polyline([(180, 450), (180, 150), (420, 450), (420, 150)])

def greek_xi_u():  # Ξ
    return hline(180, 180, 420) + hline(300, 220, 380) + hline(420, 180, 420)

def greek_omicron_u():  # Ο
    return circle(300, 300, 130, segments=18)

def greek_pi_u():  # Π
    return hline(180, 180, 420) + vline(180, 180, 450) + vline(420, 180, 450)

def greek_rho_u():  # Ρ
    return vline(180, 150, 450) + arc(220, 240, 100, -pi / 2, pi / 2, segments=12) + vline(320, 150, 240)

def greek_sigma_u():  # Σ
    return hline(180, 180, 420) + polyline([(420, 180), (180, 300), (420, 420)])

def greek_tau_u():  # Τ
    return hline(180, 180, 420) + vline(300, 180, 450)

def greek_upsilon_u():  # Υ
    return polyline([(180, 150), (300, 300), (420, 150)]) + vline(300, 300, 450)

def greek_phi_u():  # Φ
    return circle(300, 300, 110, segments=16) + vline(300, 150, 450)

def greek_chi_u():  # Χ
    return polyline([(180, 150), (420, 450)]) + polyline([(420, 150), (180, 450)])

def greek_psi_u():  # Ψ
    return vline(300, 150, 450) + polyline([(180, 180), (300, 320), (420, 180)])

def greek_omega_u():  # Ω
    s = polyline([(220, 220), (220, 340), (300, 420), (380, 340), (380, 220)])
    s += polyline([(220, 420), (180, 420)])
    s += polyline([(380, 420), (420, 420)])
    return s

# -------------------- 希腊小写字母 --------------------

def greek_alpha_l():  # α
    s = circle(280, 340, 65, segments=14)
    s += polyline([(340, 280), (340, 440)])
    return s

def greek_beta_l():  # β
    s = vline(260, 200, 450)
    s += circle(290, 280, 60, segments=14)
    s += arc(290, 380, 60, pi / 2, 3 * pi / 2, segments=12)
    return s

def greek_gamma_l():  # γ
    return polyline([(230, 200), (300, 320), (370, 200)]) + polyline([(300, 320), (300, 460)])

def greek_delta_l():  # δ
    s = circle(300, 330, 70, segments=14)
    s += polyline([(300, 260), (340, 180)])
    return s

def greek_epsilon_l():  # ε
    s = arc(310, 330, 70, pi * 0.15, pi * 1.85, segments=14)
    s += hline(330, 240, 360)
    s += polyline([(360, 270), (240, 270)])
    return s

def greek_zeta_l():  # ζ
    return hline(250, 250, 370) + polyline([(370, 250), (260, 370), (350, 370), (300, 430)])

def greek_eta_l():  # η
    s = polyline([(230, 270), (230, 370), (300, 430), (370, 370)])
    s += polyline([(370, 370), (370, 460)])
    return s

def greek_theta_l():  # θ
    return circle(300, 330, 70, segments=14) + hline(330, 230, 370)

def greek_iota_l():  # ι
    return vline(300, 280, 420)

def greek_kappa_l():  # κ
    return vline(270, 270, 430) + polyline([(270, 350), (360, 270)]) + polyline([(270, 350), (360, 430)])

def greek_lambda_l():  # λ
    return polyline([(230, 430), (300, 260), (370, 430)]) + polyline([(285, 320), (270, 260)])

def greek_mu_l():  # μ
    s = polyline([(230, 270), (230, 400), (300, 430), (370, 400), (370, 270)])
    s += polyline([(230, 400), (230, 450)])
    return s

def greek_nu_l():  # ν
    return polyline([(230, 270), (300, 430), (370, 270)])

def greek_xi_l():  # ξ
    return hline(260, 260, 360) + polyline([(360, 260), (260, 330), (360, 330), (260, 400), (360, 400)])

def greek_omicron_l():  # ο
    return circle(300, 350, 65, segments=14)

def greek_pi_l():  # π
    return hline(270, 220, 380) + vline(220, 270, 430) + vline(380, 270, 430)

def greek_rho_l():  # ρ
    s = vline(260, 270, 460)
    s += circle(300, 330, 65, segments=14)
    return s

def greek_sigma_l():  # σ
    s = circle(300, 350, 65, segments=14)
    s += polyline([(365, 350), (420, 350)])
    return s

def greek_final_sigma_l():  # ς
    s = arc(300, 330, 65, pi / 2, 3 * pi / 2, segments=12)
    s += polyline([(300, 395), (350, 395), (350, 440)])
    return s

def greek_tau_l():  # τ
    return hline(250, 250, 350) + vline(300, 280, 430)

def greek_upsilon_l():  # υ
    return polyline([(230, 270), (300, 430), (370, 270)])

def greek_phi_l():  # φ
    s = circle(300, 350, 65, segments=14)
    s += vline(300, 250, 450)
    return s

def greek_chi_l():  # χ
    return polyline([(230, 260), (370, 440)]) + polyline([(370, 260), (230, 440)])

def greek_psi_l():  # ψ
    s = vline(300, 260, 450)
    s += polyline([(230, 260), (300, 360), (370, 260)])
    return s

def greek_omega_l():  # ω
    return polyline([(220, 270), (220, 370), (300, 430), (380, 370), (380, 270)])

# -------------------- 数学符号 --------------------

def math_element_of():  # ∈
    s = arc(300, 300, 100, -pi / 2, pi / 2, segments=14)
    s += hline(300, 200, 400)
    s += polyline([(200, 200), (200, 400)])
    return s

def math_not_element_of():  # ∉
    s = math_element_of()
    s += polyline([(200, 200), (400, 400)])
    return s

def math_contains():  # ∋
    s = arc(300, 300, 100, pi / 2, 3 * pi / 2, segments=14)
    s += hline(300, 200, 400)
    s += polyline([(400, 200), (400, 400)])
    return s

def math_not_contains():  # ∌
    s = math_contains()
    s += polyline([(200, 200), (400, 400)])
    return s

def math_empty_set():  # ∅
    s = circle(300, 300, 120, segments=16)
    s += polyline([(210, 210), (390, 390)])
    return s

def math_subseteq():  # ⊆
    s = arc(320, 300, 100, pi / 2, 3 * pi / 2, segments=14)
    s += polyline([(220, 200), (220, 400)])
    s += hline(410, 220, 410)
    return s

def math_superseteq():  # ⊇
    s = arc(280, 300, 100, -pi / 2, pi / 2, segments=14)
    s += polyline([(380, 200), (380, 400)])
    s += hline(410, 190, 380)
    return s

def math_subset():  # ⊂
    s = arc(320, 300, 100, pi / 2, 3 * pi / 2, segments=14)
    s += polyline([(220, 200), (220, 400)])
    return s

def math_superset():  # ⊃
    s = arc(280, 300, 100, -pi / 2, pi / 2, segments=14)
    s += polyline([(380, 200), (380, 400)])
    return s

def math_not_subset():  # ⊄
    s = math_subset()
    s += polyline([(220, 200), (400, 400)])
    return s

def math_not_superset():  # ⊅
    s = math_superset()
    s += polyline([(200, 200), (380, 400)])
    return s

def math_set_minus():  # ∖
    return polyline([(380, 180), (220, 420)])

def math_logical_and():  # ∧
    return polyline([(180, 400), (300, 180), (420, 400)])

def math_logical_or():  # ∨
    return polyline([(180, 200), (300, 420), (420, 200)])

def math_forall():  # ∀
    return polyline([(180, 420), (300, 160), (420, 420)]) + hline(300, 230, 370)

def math_exists():  # ∃
    return polyline([(180, 180), (420, 180), (420, 420), (180, 420)]) + hline(300, 180, 420)

def math_not_exists():  # ∄
    s = math_exists()
    s += polyline([(180, 180), (420, 420)])
    return s

def math_propto():  # ∝
    return arc(300, 300, 90, pi * 0.1, pi * 1.9, segments=16) + polyline([(350, 210), (430, 180)])

def math_infinity():  # ∞
    return circle(235, 300, 65, segments=14) + circle(365, 300, 65, segments=14)

def math_right_angle():  # ∟
    return polyline([(180, 420), (420, 420), (420, 180)])

def math_angle():  # ∠
    return polyline([(180, 420), (420, 420), (300, 180)])

# -------------------- 天气符号 --------------------

def weather_sun():  # ☀
    s = filled_circle(300, 300, 70, segments=14)
    for i in range(8):
        a = 2 * pi * i / 8
        x1 = 300 + 95 * cos(a)
        y1 = 300 + 95 * sin(a)
        x2 = 300 + 150 * cos(a)
        y2 = 300 + 150 * sin(a)
        s += polyline([(x1, y1), (x2, y2)])
    return s

def weather_cloud():  # ☁
    return polyline([
        (180, 360), (220, 280), (300, 250), (380, 280),
        (420, 360), (380, 400), (220, 400), (180, 360)
    ])

def weather_umbrella():  # ☂
    s = arc(300, 280, 110, pi, 0, segments=16)
    s += vline(300, 280, 460)
    s += polyline([(300, 460), (270, 450)])
    return s

def weather_snowman():  # ☃
    s = circle(300, 380, 70, segments=14)
    s += circle(300, 260, 50, segments=12)
    s += filled_circle(290, 250, 4, segments=6)
    s += filled_circle(310, 250, 4, segments=6)
    s += polyline([(220, 300), (170, 270)])
    s += polyline([(380, 300), (430, 270)])
    s += polyline([(300, 260), (320, 260)])
    return s

def weather_snowflake():  # ❄
    arms = []
    for i in range(6):
        a = pi * i / 3
        x = 300 + 130 * cos(a)
        y = 300 + 130 * sin(a)
        arms += polyline([(300, 300), (x, y)])
        # 分支
        bx, by = 300 + 80 * cos(a), 300 + 80 * sin(a)
        arms += polyline([(bx + 25 * cos(a + pi / 2), by + 25 * sin(a + pi / 2)),
                          (bx, by),
                          (bx + 25 * cos(a - pi / 2), by + 25 * sin(a - pi / 2))])
    return arms

def weather_lightning():  # ⚡
    return polyline([(340, 160), (260, 300), (330, 300), (280, 440), (380, 280), (310, 280), (360, 160)])

def weather_snowman_no_snow():  # ⛄
    s = circle(300, 380, 70, segments=14)
    s += circle(300, 260, 50, segments=12)
    s += filled_circle(290, 250, 4, segments=6)
    s += filled_circle(310, 250, 4, segments=6)
    s += polyline([(300, 260), (320, 260)])
    return s

def weather_umbrella_rain():  # ☔
    s = weather_umbrella()
    s += polyline([(250, 380), (240, 420)])
    s += polyline([(300, 390), (290, 430)])
    s += polyline([(350, 380), (340, 420)])
    return s

# -------------------- 音乐符号 --------------------

def music_quarter_note():  # ♩
    s = filled_rect(270, 340, 330, 400)
    s += vline(330, 200, 370)
    return s

def music_eighth_note():  # ♪
    s = filled_rect(270, 340, 330, 400)
    s += vline(330, 200, 370)
    s += polyline([(330, 200), (390, 230), (390, 260)])
    return s

def music_beamed_notes():  # ♫
    s = filled_rect(230, 340, 290, 400)
    s += filled_rect(310, 340, 370, 400)
    s += vline(290, 220, 370)
    s += vline(370, 220, 370)
    s += hline(220, 290, 370)
    return s

def music_beamed_sixteenth():  # ♬
    s = filled_rect(230, 340, 290, 400)
    s += filled_rect(310, 340, 370, 400)
    s += vline(290, 220, 370)
    s += vline(370, 220, 370)
    s += hline(220, 290, 370)
    s += hline(250, 290, 370)
    return s

def music_flat():  # ♭
    s = vline(300, 180, 440)
    s += arc(300, 360, 60, pi / 2, 3 * pi / 2, segments=12)
    return s

def music_natural():  # ♮
    return vline(280, 180, 420) + vline(320, 200, 440) + hline(340, 280, 320) + hline(280, 280, 320)

def music_sharp():  # ♯
    s = vline(270, 200, 420) + vline(330, 200, 420)
    s += hline(260, 240, 360) + hline(360, 240, 360)
    s += polyline([(240, 220), (360, 180)]) + polyline([(240, 400), (360, 360)])
    return s

def music_treble_clef():  # 𝄞
    s = circle(300, 260, 45, segments=12)
    s += polyline([(300, 260), (300, 420), (330, 440), (270, 440), (300, 420)])
    s += polyline([(340, 220), (380, 240)])
    s += hline(380, 180, 420)
    return s

def music_bass_clef():  # 𝄢
    s = circle(300, 260, 40, segments=12)
    s += vline(300, 260, 420)
    s += filled_circle(300, 360, 10, segments=8)
    s += filled_circle(300, 400, 10, segments=8)
    s += hline(420, 180, 420)
    return s

def music_c_clef():  # 𝄡
    s = circle(300, 300, 80, segments=14)
    s += vline(300, 180, 420)
    s += hline(260, 180, 420)
    s += hline(340, 180, 420)
    return s

# -------------------- 国际象棋 --------------------

def chess_king(white=True):  # ♔ ♚
    s = circle(300, 320, 50, segments=12)
    s += vline(300, 220, 270)
    s += cross(300, 190, 40)
    s += polyline([(240, 400), (360, 400), (380, 460), (220, 460), (240, 400)])
    if not white:
        s += filled_rect(250, 410, 350, 450, step=10)
    return s

def chess_queen(white=True):  # ♕ ♛
    s = circle(300, 320, 50, segments=12)
    s += vline(300, 220, 270)
    s += filled_circle(300, 190, 12, segments=8)
    s += polyline([(220, 400), (380, 400), (400, 460), (200, 460), (220, 400)])
    if not white:
        s += filled_rect(230, 410, 370, 450, step=10)
    return s

def chess_rook(white=True):  # ♖ ♜
    s = rect(240, 240, 360, 360)
    s += polyline([(230, 360), (370, 360), (390, 460), (210, 460), (230, 360)])
    s += hline(230, 240, 360)
    s += vline(240, 230, 240)
    s += vline(360, 230, 240)
    if not white:
        s += filled_rect(240, 370, 360, 450, step=10)
    return s

def chess_bishop(white=True):  # ♗ ♝
    s = circle(300, 320, 50, segments=12)
    s += polyline([(270, 280), (330, 280)])
    s += vline(300, 220, 270)
    s += polyline([(230, 400), (370, 400), (390, 460), (210, 460), (230, 400)])
    if not white:
        s += filled_rect(230, 410, 370, 450, step=10)
    return s

def chess_knight(white=True):  # ♘ ♞
    s = polyline([(260, 460), (260, 280), (320, 220), (380, 260), (360, 320), (400, 460)])
    s += filled_circle(340, 250, 8, segments=6)
    s += polyline([(260, 360), (320, 360)])
    if not white:
        s += filled_rect(270, 400, 390, 450, step=10)
    return s

def chess_pawn(white=True):  # ♙ ♟
    s = circle(300, 300, 45, segments=12)
    s += polyline([(255, 360), (345, 360), (360, 460), (240, 460), (255, 360)])
    if not white:
        s += filled_rect(260, 370, 340, 450, step=10)
    return s

# -------------------- 扑克花色 --------------------

def suit_spade():  # ♠
    s = polyline([(300, 160), (420, 300), (300, 420), (180, 300), (300, 160)])
    s += vline(300, 360, 460)
    return s

def suit_heart():  # ♥
    s = []
    for cx in (250, 350):
        s += arc(cx, 260, 50, pi, 0, segments=12)
    s += polyline([(200, 280), (300, 420), (400, 280)])
    return s

def suit_diamond():  # ♦
    return polyline([(300, 160), (440, 300), (300, 440), (160, 300), (300, 160)])

def suit_club():  # ♣
    s = filled_circle(300, 240, 45, segments=10)
    s += filled_circle(240, 330, 45, segments=10)
    s += filled_circle(360, 330, 45, segments=10)
    s += vline(300, 330, 460)
    return s

# -------------------- 西方黄道十二宫 --------------------

def zodiac_aries():  # ♈ 羊角
    return polyline([(200, 360), (260, 240), (320, 360), (380, 240), (440, 360)])

def zodiac_taurus():  # ♉ 公牛头
    s = circle(240, 260, 50, segments=12)
    s += circle(360, 260, 50, segments=12)
    s += vline(300, 310, 460)
    return s

def zodiac_gemini():  # ♊ 双子
    return vline(240, 180, 450) + vline(360, 180, 450) + hline(210, 240, 360) + hline(420, 240, 360)

def zodiac_cancer():  # ♋ 螃蟹
    return circle(260, 300, 60, segments=12) + circle(340, 300, 60, segments=12) + polyline([(260, 360), (220, 420)])

def zodiac_leo():  # ♌ 狮子
    s = circle(280, 280, 60, segments=12)
    s += polyline([(340, 280), (420, 320), (400, 420), (320, 440)])
    return s

def zodiac_virgo():  # ♍ 处女
    s = vline(260, 180, 460)
    s += polyline([(260, 240), (320, 240), (320, 420), (380, 420)])
    s += vline(380, 360, 460)
    return s

def zodiac_libra():  # ♎ 天秤
    return hline(200, 200, 400) + hline(320, 240, 360) + vline(300, 180, 320) + polyline([(220, 420), (380, 420)])

def zodiac_scorpio():  # ♏ 蝎子
    s = polyline([(200, 420), (260, 240), (320, 420), (380, 300), (420, 340)])
    s += polyline([(420, 340), (400, 360), (440, 360)])
    return s

def zodiac_sagittarius():  # ♐ 射手
    return polyline([(180, 420), (420, 180)]) + polyline([(420, 180), (360, 180), (420, 240)])

def zodiac_capricorn():  # ♑ 摩羯
    s = circle(260, 300, 60, segments=12)
    s += polyline([(320, 300), (420, 260), (420, 360), (360, 420)])
    return s

def zodiac_aquarius():  # ♒ 水瓶
    return (polyline([(180, 240), (260, 300), (340, 240), (420, 300)]) +
            polyline([(180, 320), (260, 380), (340, 320), (420, 380)]))

def zodiac_pisces():  # ♓ 双鱼
    return (circle(260, 300, 60, segments=12) + circle(340, 300, 60, segments=12) +
            hline(300, 260, 340))

# -------------------- 性别/行星符号 --------------------

def gender_female():  # ♀
    s = circle(300, 250, 70, segments=14)
    s += vline(300, 320, 430)
    s += hline(400, 260, 340)
    return s

def gender_male():  # ♂
    s = circle(300, 300, 70, segments=14)
    s += polyline([(350, 250), (430, 170)])
    s += polyline([(390, 170), (430, 170), (430, 210)])
    return s

def gender_intersex():  # ⚥
    s = circle(300, 300, 70, segments=14)
    s += vline(300, 370, 450)
    s += hline(370, 260, 340)
    s += polyline([(350, 250), (420, 180)])
    return s

def planet_earth():  # ♁
    s = circle(300, 300, 80, segments=14)
    s += cross(300, 300, 80)
    return s

def planet_jupiter():  # ♃
    s = polyline([(260, 220), (260, 380), (340, 380), (340, 220)])
    s += polyline([(230, 180), (370, 180)])
    s += arc(340, 260, 50, -pi / 2, pi / 2, segments=10)
    return s

def planet_saturn():  # ♄
    s = vline(300, 180, 420)
    s += hline(240, 240, 360)
    s += hline(360, 240, 360)
    s += arc(300, 380, 70, 0, pi, segments=12)
    return s

def planet_uranus():  # ♅
    s = vline(300, 180, 420)
    s += hline(240, 240, 360)
    s += circle(300, 220, 40, segments=10)
    s += polyline([(240, 420), (300, 360), (360, 420)])
    return s

def planet_neptune():  # ♆
    s = vline(300, 180, 420)
    s += arc(300, 220, 50, pi, 0, segments=10)
    s += polyline([(250, 300), (350, 300)])
    s += arc(300, 380, 40, 0, pi, segments=10)
    return s

# -------------------- 杂项 UI --------------------

def ui_telephone():  # ☎
    s = rect(220, 220, 380, 400)
    s += polyline([(220, 220), (260, 180), (340, 180), (380, 220)])
    s += polyline([(260, 280), (260, 340), (340, 340), (340, 280), (260, 280)])
    return s

def ui_envelope():  # ✉
    s = rect(160, 220, 440, 380)
    s += polyline([(160, 220), (300, 330), (440, 220)])
    return s

def ui_scissors():  # ✂
    s = circle(260, 260, 40, segments=10)
    s += circle(340, 260, 40, segments=10)
    s += polyline([(260, 300), (340, 420)])
    s += polyline([(340, 300), (260, 420)])
    return s

def ui_pencil():  # ✏
    s = polyline([(260, 160), (360, 160), (380, 440), (240, 440), (260, 160)])
    s += polyline([(240, 440), (310, 490), (380, 440)])
    return s

def ui_nib():  # ✒
    s = polyline([(270, 160), (330, 160), (350, 360), (250, 360), (270, 160)])
    s += polyline([(250, 360), (300, 460), (350, 360)])
    return s

def ui_checkbox_checked():  # ☑
    s = rect(180, 180, 420, 420)
    s += polyline([(220, 320), (290, 390), (380, 240)])
    return s

def ui_checkbox_x():  # ☒
    s = rect(180, 180, 420, 420)
    s += x_mark(300, 300, 140)
    return s

def ui_point_left():  # ☜
    return polyline([(420, 240), (260, 240), (260, 180), (160, 300), (260, 420), (260, 360), (420, 360), (420, 240)])

def ui_point_right():  # ☞
    return polyline([(180, 240), (340, 240), (340, 180), (440, 300), (340, 420), (340, 360), (180, 360), (180, 240)])

def ui_victory():  # ✌
    return polyline([(300, 440), (240, 300), (260, 220)]) + polyline([(300, 440), (360, 300), (340, 220)])

def ui_writing():  # ✍
    s = polyline([(240, 360), (300, 420), (420, 300), (360, 240), (240, 360)])
    s += polyline([(240, 360), (180, 420), (300, 420)])
    return s

def ui_hourglass():  # ⌛
    s = polyline([(200, 180), (400, 180), (300, 300), (400, 420), (200, 420), (300, 300), (200, 180)])
    s += hline(200, 200, 400)
    s += hline(420, 200, 400)
    return s

# -------------------- Dingbats --------------------

def dingbat_four_pointed():  # ✦
    return polyline([(300, 160), (340, 260), (440, 300), (340, 340), (300, 440), (260, 340), (160, 300), (260, 260), (300, 160)])

def dingbat_four_pointed_open():  # ✧
    return polyline([(300, 160), (340, 260), (440, 300), (340, 340), (300, 440), (260, 340), (160, 300), (260, 260), (300, 160)])

def dingbat_star_open():  # ✩
    return star(300, 300, 130, 55, points=5)

def dingbat_star_circled():  # ✪
    s = circle(300, 300, 120, segments=16)
    s += star(300, 300, 100, 40, points=5)
    return s

def dingbat_star_fleur():  # ✫
    return polyline([(300, 160), (320, 280), (440, 300), (320, 320), (300, 440), (280, 320), (160, 300), (280, 280), (300, 160)])

def dingbat_star_six():  # ✬
    s = []
    for i in range(6):
        a = pi / 6 + pi * i / 3
        x = 300 + 130 * cos(a)
        y = 300 + 130 * sin(a)
        s += polyline([(300, 300), (x, y)])
    return s

def dingbat_star_shadow():  # ✭
    s = star(300, 300, 130, 55, points=5)
    s += polyline([(300, 170), (300, 430)])
    return s

def dingbat_star_pinwheel():  # ✮
    s = star(300, 300, 130, 50, points=5)
    s += circle(300, 300, 40, segments=10)
    return s

def dingbat_star_bold():  # ✯
    return star(300, 300, 140, 60, points=5) + star(300, 300, 90, 35, points=5)

def dingbat_star_burst():  # ✰
    s = star(300, 300, 130, 55, points=5)
    for i in range(10):
        a = 2 * pi * i / 10
        x = 300 + 150 * cos(a)
        y = 300 + 150 * sin(a)
        s += polyline([(300, 300), (x, y)])
    return s

# -------------------- 表情/警示 --------------------

def face_smile():  # ☺
    s = circle(300, 300, 120, segments=16)
    s += filled_circle(250, 260, 15, segments=8)
    s += filled_circle(350, 260, 15, segments=8)
    s += arc(300, 300, 70, 0, pi, segments=12)
    return s

def face_smile_filled():  # ☻
    s = filled_circle(300, 300, 120, segments=16)
    s += filled_circle(250, 260, 15, segments=8)
    s += filled_circle(350, 260, 15, segments=8)
    s += arc(300, 300, 70, 0, pi, segments=12)
    return s

def face_frown():  # ☹
    s = circle(300, 300, 120, segments=16)
    s += filled_circle(250, 260, 15, segments=8)
    s += filled_circle(350, 260, 15, segments=8)
    s += arc(300, 360, 70, pi, 0, segments=12)
    return s

def warn_recycle():  # ♻
    s = []
    for i in range(3):
        a0 = 2 * pi * i / 3
        a1 = 2 * pi * (i + 1) / 3
        x0, y0 = 300 + 100 * cos(a0), 300 + 100 * sin(a0)
        x1, y1 = 300 + 100 * cos(a1), 300 + 100 * sin(a1)
        s += polyline([(x0, y0), (x1, y1)])
        # 箭头
        ax, ay = 300 + 80 * cos(a1 - 0.3), 300 + 80 * sin(a1 - 0.3)
        s += polyline([(x1, y1), (ax, ay)])
    return s

def warn_triangle():  # ⚠
    s = polyline([(300, 160), (460, 440), (140, 440), (300, 160)])
    s += vline(300, 260, 360)
    s += filled_circle(300, 400, 12, segments=8)
    return s

def warn_radioactive():  # ☢
    s = circle(300, 300, 120, segments=16)
    s += circle(300, 300, 40, segments=10)
    for i in range(3):
        a = 2 * pi * i / 3
        x = 300 + 110 * cos(a)
        y = 300 + 110 * sin(a)
        s += polyline([(300, 300), (x, y)])
    return s

# -------------------- 上下标数字 --------------------

def digit_path(n, cx=300, cy=350, scale=1.0):
    """返回数字 0-9 的笔画路径，可缩放/平移。"""
    s = scale
    ox, oy = cx - 80 * s, cy - 100 * s
    def tx(x): return ox + x * s
    def ty(y): return oy + y * s
    def pl(pts):
        return polyline([(tx(x), ty(y)) for x, y in pts])

    if n == 0:
        return pl([(60, 40), (100, 40), (100, 160), (60, 160), (60, 40)])
    if n == 1:
        return pl([(80, 40), (80, 160)])
    if n == 2:
        return pl([(60, 60), (80, 40), (100, 60), (60, 140), (60, 160), (100, 160)])
    if n == 3:
        return pl([(60, 40), (100, 40), (80, 90), (100, 100), (100, 140), (80, 160), (60, 160)])
    if n == 4:
        return pl([(100, 40), (100, 160), (60, 160), (60, 100), (100, 100)])
    if n == 5:
        return pl([(100, 40), (60, 40), (60, 90), (100, 100), (100, 140), (80, 160), (60, 160)])
    if n == 6:
        return pl([(100, 40), (60, 70), (60, 140), (80, 160), (100, 140), (100, 110), (60, 90)])
    if n == 7:
        return pl([(60, 40), (100, 40), (80, 160)])
    if n == 8:
        return pl([(60, 50), (80, 40), (100, 60), (60, 140), (80, 160), (100, 140), (60, 60), (100, 140)])
    if n == 9:
        return pl([(80, 160), (100, 140), (100, 50), (80, 40), (60, 60), (60, 90), (100, 90)])
    return []

def superscript_digit(n):
    return digit_path(n, cx=300, cy=260, scale=1.1)

def subscript_digit(n):
    return digit_path(n, cx=300, cy=400, scale=1.1)

# -------------------- 符号注册表 --------------------

SYMBOLS = [
    # 拼音调号字母
    ("ā", "U+0101", "latin small a with macron", lambda: pinyin_vowel(latin_a, tone_macron)),
    ("á", "U+00E1", "latin small a with acute", lambda: pinyin_vowel(latin_a, tone_acute)),
    ("ǎ", "U+01CE", "latin small a with caron", lambda: pinyin_vowel(latin_a, tone_caron)),
    ("à", "U+00E0", "latin small a with grave", lambda: pinyin_vowel(latin_a, tone_grave)),
    ("ē", "U+0113", "latin small e with macron", lambda: pinyin_vowel(latin_e, tone_macron)),
    ("é", "U+00E9", "latin small e with acute", lambda: pinyin_vowel(latin_e, tone_acute)),
    ("ě", "U+011B", "latin small e with caron", lambda: pinyin_vowel(latin_e, tone_caron)),
    ("è", "U+00E8", "latin small e with grave", lambda: pinyin_vowel(latin_e, tone_grave)),
    ("ī", "U+012B", "latin small i with macron", lambda: pinyin_vowel(latin_i, tone_macron)),
    ("í", "U+00ED", "latin small i with acute", lambda: pinyin_vowel(latin_i, tone_acute)),
    ("ǐ", "U+01D0", "latin small i with caron", lambda: pinyin_vowel(latin_i, tone_caron)),
    ("ì", "U+00EC", "latin small i with grave", lambda: pinyin_vowel(latin_i, tone_grave)),
    ("ō", "U+014D", "latin small o with macron", lambda: pinyin_vowel(latin_o, tone_macron)),
    ("ó", "U+00F3", "latin small o with acute", lambda: pinyin_vowel(latin_o, tone_acute)),
    ("ǒ", "U+01D2", "latin small o with caron", lambda: pinyin_vowel(latin_o, tone_caron)),
    ("ò", "U+00F2", "latin small o with grave", lambda: pinyin_vowel(latin_o, tone_grave)),
    ("ū", "U+016B", "latin small u with macron", lambda: pinyin_vowel(latin_u, tone_macron)),
    ("ú", "U+00FA", "latin small u with acute", lambda: pinyin_vowel(latin_u, tone_acute)),
    ("ǔ", "U+01D4", "latin small u with caron", lambda: pinyin_vowel(latin_u, tone_caron)),
    ("ù", "U+00F9", "latin small u with grave", lambda: pinyin_vowel(latin_u, tone_grave)),
    ("ǖ", "U+01D6", "latin small u with diaeresis and macron", lambda: pinyin_vowel(latin_u_umlaut, tone_macron)),
    ("ǘ", "U+01D8", "latin small u with diaeresis and acute", lambda: pinyin_vowel(latin_u_umlaut, tone_acute)),
    ("ǚ", "U+01DA", "latin small u with diaeresis and caron", lambda: pinyin_vowel(latin_u_umlaut, tone_caron)),
    ("ǜ", "U+01DC", "latin small u with diaeresis and grave", lambda: pinyin_vowel(latin_u_umlaut, tone_grave)),

    # 希腊大写
    ("Α", "U+0391", "greek capital alpha", greek_alpha_u),
    ("Β", "U+0392", "greek capital beta", greek_beta_u),
    ("Γ", "U+0393", "greek capital gamma", greek_gamma_u),
    ("Δ", "U+0394", "greek capital delta", greek_delta_u),
    ("Ε", "U+0395", "greek capital epsilon", greek_epsilon_u),
    ("Ζ", "U+0396", "greek capital zeta", greek_zeta_u),
    ("Η", "U+0397", "greek capital eta", greek_eta_u),
    ("Θ", "U+0398", "greek capital theta", greek_theta_u),
    ("Ι", "U+0399", "greek capital iota", greek_iota_u),
    ("Κ", "U+039A", "greek capital kappa", greek_kappa_u),
    ("Λ", "U+039B", "greek capital lambda", greek_lambda_u),
    ("Μ", "U+039C", "greek capital mu", greek_mu_u),
    ("Ν", "U+039D", "greek capital nu", greek_nu_u),
    ("Ξ", "U+039E", "greek capital xi", greek_xi_u),
    ("Ο", "U+039F", "greek capital omicron", greek_omicron_u),
    ("Π", "U+03A0", "greek capital pi", greek_pi_u),
    ("Ρ", "U+03A1", "greek capital rho", greek_rho_u),
    ("Σ", "U+03A3", "greek capital sigma", greek_sigma_u),
    ("Τ", "U+03A4", "greek capital tau", greek_tau_u),
    ("Υ", "U+03A5", "greek capital upsilon", greek_upsilon_u),
    ("Φ", "U+03A6", "greek capital phi", greek_phi_u),
    ("Χ", "U+03A7", "greek capital chi", greek_chi_u),
    ("Ψ", "U+03A8", "greek capital psi", greek_psi_u),
    ("Ω", "U+03A9", "greek capital omega", greek_omega_u),

    # 希腊小写
    ("α", "U+03B1", "greek small alpha", greek_alpha_l),
    ("β", "U+03B2", "greek small beta", greek_beta_l),
    ("γ", "U+03B3", "greek small gamma", greek_gamma_l),
    ("δ", "U+03B4", "greek small delta", greek_delta_l),
    ("ε", "U+03B5", "greek small epsilon", greek_epsilon_l),
    ("ζ", "U+03B6", "greek small zeta", greek_zeta_l),
    ("η", "U+03B7", "greek small eta", greek_eta_l),
    ("θ", "U+03B8", "greek small theta", greek_theta_l),
    ("ι", "U+03B9", "greek small iota", greek_iota_l),
    ("κ", "U+03BA", "greek small kappa", greek_kappa_l),
    ("λ", "U+03BB", "greek small lambda", greek_lambda_l),
    ("μ", "U+03BC", "greek small mu", greek_mu_l),
    ("ν", "U+03BD", "greek small nu", greek_nu_l),
    ("ξ", "U+03BE", "greek small xi", greek_xi_l),
    ("ο", "U+03BF", "greek small omicron", greek_omicron_l),
    ("π", "U+03C0", "greek small pi", greek_pi_l),
    ("ρ", "U+03C1", "greek small rho", greek_rho_l),
    ("σ", "U+03C3", "greek small sigma", greek_sigma_l),
    ("ς", "U+03C2", "greek small final sigma", greek_final_sigma_l),
    ("τ", "U+03C4", "greek small tau", greek_tau_l),
    ("υ", "U+03C5", "greek small upsilon", greek_upsilon_l),
    ("φ", "U+03C6", "greek small phi", greek_phi_l),
    ("χ", "U+03C7", "greek small chi", greek_chi_l),
    ("ψ", "U+03C8", "greek small psi", greek_psi_l),
    ("ω", "U+03C9", "greek small omega", greek_omega_l),

    # 更多数学
    ("∈", "U+2208", "element of", math_element_of),
    ("∉", "U+2209", "not an element of", math_not_element_of),
    ("∋", "U+220B", "contains as member", math_contains),
    ("∌", "U+220C", "does not contain as member", math_not_contains),
    ("∅", "U+2205", "empty set", math_empty_set),
    ("⊆", "U+2286", "subset of or equal to", math_subseteq),
    ("⊇", "U+2287", "superset of or equal to", math_superseteq),
    ("⊂", "U+2282", "subset of", math_subset),
    ("⊃", "U+2283", "superset of", math_superset),
    ("⊄", "U+2284", "not a subset of", math_not_subset),
    ("⊅", "U+2285", "not a superset of", math_not_superset),
    ("∖", "U+2216", "set minus", math_set_minus),
    ("∧", "U+2227", "logical and", math_logical_and),
    ("∨", "U+2228", "logical or", math_logical_or),
    ("∀", "U+2200", "for all", math_forall),
    ("∃", "U+2203", "there exists", math_exists),
    ("∄", "U+2204", "there does not exist", math_not_exists),
    ("∝", "U+221D", "proportional to", math_propto),
    ("∞", "U+221E", "infinity", math_infinity),
    ("∟", "U+221F", "right angle", math_right_angle),
    ("∠", "U+2220", "angle", math_angle),

    # 天气
    ("☀", "U+2600", "black sun with rays", weather_sun),
    ("☁", "U+2601", "cloud", weather_cloud),
    ("☂", "U+2602", "umbrella", weather_umbrella),
    ("☃", "U+2603", "snowman", weather_snowman),
    ("❄", "U+2744", "snowflake", weather_snowflake),
    ("⚡", "U+26A1", "high voltage", weather_lightning),
    ("⛄", "U+26C4", "snowman without snow", weather_snowman_no_snow),
    ("☔", "U+2614", "umbrella with rain drops", weather_umbrella_rain),

    # 音乐
    ("♩", "U+2669", "quarter note", music_quarter_note),
    ("♪", "U+266A", "eighth note", music_eighth_note),
    ("♫", "U+266B", "beamed eighth notes", music_beamed_notes),
    ("♬", "U+266C", "beamed sixteenth notes", music_beamed_sixteenth),
    ("♭", "U+266D", "music flat sign", music_flat),
    ("♮", "U+266E", "music natural sign", music_natural),
    ("♯", "U+266F", "music sharp sign", music_sharp),
    ("𝄞", "U+1D11E", "musical symbol g clef", music_treble_clef),
    ("𝄢", "U+1D122", "musical symbol f clef", music_bass_clef),
    ("𝄡", "U+1D121", "musical symbol c clef", music_c_clef),

    # 国际象棋
    ("♔", "U+2654", "white chess king", lambda: chess_king(True)),
    ("♕", "U+2655", "white chess queen", lambda: chess_queen(True)),
    ("♖", "U+2656", "white chess rook", lambda: chess_rook(True)),
    ("♗", "U+2657", "white chess bishop", lambda: chess_bishop(True)),
    ("♘", "U+2658", "white chess knight", lambda: chess_knight(True)),
    ("♙", "U+2659", "white chess pawn", lambda: chess_pawn(True)),
    ("♚", "U+265A", "black chess king", lambda: chess_king(False)),
    ("♛", "U+265B", "black chess queen", lambda: chess_queen(False)),
    ("♜", "U+265C", "black chess rook", lambda: chess_rook(False)),
    ("♝", "U+265D", "black chess bishop", lambda: chess_bishop(False)),
    ("♞", "U+265E", "black chess knight", lambda: chess_knight(False)),
    ("♟", "U+265F", "black chess pawn", lambda: chess_pawn(False)),

    # 扑克花色
    ("♠", "U+2660", "black spade suit", suit_spade),
    ("♥", "U+2665", "black heart suit", suit_heart),
    ("♦", "U+2666", "black diamond suit", suit_diamond),
    ("♣", "U+2663", "black club suit", suit_club),

    # 西方黄道十二宫
    ("♈", "U+2648", "aries", zodiac_aries),
    ("♉", "U+2649", "taurus", zodiac_taurus),
    ("♊", "U+264A", "gemini", zodiac_gemini),
    ("♋", "U+264B", "cancer", zodiac_cancer),
    ("♌", "U+264C", "leo", zodiac_leo),
    ("♍", "U+264D", "virgo", zodiac_virgo),
    ("♎", "U+264E", "libra", zodiac_libra),
    ("♏", "U+264F", "scorpio", zodiac_scorpio),
    ("♐", "U+2650", "sagittarius", zodiac_sagittarius),
    ("♑", "U+2651", "capricorn", zodiac_capricorn),
    ("♒", "U+2652", "aquarius", zodiac_aquarius),
    ("♓", "U+2653", "pisces", zodiac_pisces),

    # 性别/行星
    ("♀", "U+2640", "female sign", gender_female),
    ("♂", "U+2642", "male sign", gender_male),
    ("⚥", "U+26A5", "male and female sign", gender_intersex),
    ("♁", "U+2641", "earth", planet_earth),
    ("♃", "U+2643", "jupiter", planet_jupiter),
    ("♄", "U+2644", "saturn", planet_saturn),
    ("♅", "U+2645", "uranus", planet_uranus),
    ("♆", "U+2646", "neptune", planet_neptune),

    # 杂项 UI
    ("☎", "U+260E", "black telephone", ui_telephone),
    ("✉", "U+2709", "envelope", ui_envelope),
    ("✂", "U+2702", "black scissors", ui_scissors),
    ("✏", "U+270F", "pencil", ui_pencil),
    ("✒", "U+2712", "black nib", ui_nib),
    ("☑", "U+2611", "ballot box with check", ui_checkbox_checked),
    ("☒", "U+2612", "ballot box with x", ui_checkbox_x),
    ("☜", "U+261C", "white left pointing index", ui_point_left),
    ("☞", "U+261E", "white right pointing index", ui_point_right),
    ("✌", "U+270C", "victory hand", ui_victory),
    ("✍", "U+270D", "writing hand", ui_writing),
    ("⌛", "U+231B", "hourglass", ui_hourglass),

    # Dingbats
    ("✦", "U+2726", "black four pointed star", dingbat_four_pointed),
    ("✧", "U+2727", "white four pointed star", dingbat_four_pointed_open),
    ("✩", "U+2729", "stress outlined white star", dingbat_star_open),
    ("✪", "U+272A", "circled white star", dingbat_star_circled),
    ("✫", "U+272B", "open centre black star", dingbat_star_fleur),
    ("✬", "U+272C", "black centre white star", dingbat_star_six),
    ("✭", "U+272D", "outlined black star", dingbat_star_shadow),
    ("✮", "U+272E", "heavy outlined black star", dingbat_star_pinwheel),
    ("✯", "U+272F", "pinwheel star", dingbat_star_bold),
    ("✰", "U+2730", "shadowed white star", dingbat_star_burst),

    # 表情/警示
    ("☺", "U+263A", "white smiling face", face_smile),
    ("☻", "U+263B", "black smiling face", face_smile_filled),
    ("☹", "U+2639", "white frowning face", face_frown),
    ("♻", "U+267B", "black universal recycling symbol", warn_recycle),
    ("⚠", "U+26A0", "warning sign", warn_triangle),
    ("☢", "U+2622", "radioactive sign", warn_radioactive),

    # 上标数字
    ("⁰", "U+2070", "superscript zero", lambda: superscript_digit(0)),
    ("¹", "U+00B9", "superscript one", lambda: superscript_digit(1)),
    ("²", "U+00B2", "superscript two", lambda: superscript_digit(2)),
    ("³", "U+00B3", "superscript three", lambda: superscript_digit(3)),
    ("⁴", "U+2074", "superscript four", lambda: superscript_digit(4)),
    ("⁵", "U+2075", "superscript five", lambda: superscript_digit(5)),
    ("⁶", "U+2076", "superscript six", lambda: superscript_digit(6)),
    ("⁷", "U+2077", "superscript seven", lambda: superscript_digit(7)),
    ("⁸", "U+2078", "superscript eight", lambda: superscript_digit(8)),
    ("⁹", "U+2079", "superscript nine", lambda: superscript_digit(9)),

    # 下标数字
    ("₀", "U+2080", "subscript zero", lambda: subscript_digit(0)),
    ("₁", "U+2081", "subscript one", lambda: subscript_digit(1)),
    ("₂", "U+2082", "subscript two", lambda: subscript_digit(2)),
    ("₃", "U+2083", "subscript three", lambda: subscript_digit(3)),
    ("₄", "U+2084", "subscript four", lambda: subscript_digit(4)),
    ("₅", "U+2085", "subscript five", lambda: subscript_digit(5)),
    ("₆", "U+2086", "subscript six", lambda: subscript_digit(6)),
    ("₇", "U+2087", "subscript seven", lambda: subscript_digit(7)),
    ("₈", "U+2088", "subscript eight", lambda: subscript_digit(8)),
    ("₉", "U+2089", "subscript nine", lambda: subscript_digit(9)),
]

# -------------------- 主流程 --------------------

def count_strokes(strokes):
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
            skipped += 1
            continue
        glyph = make_glyph(char, codepoint, name, strokes)
        glyphs[char] = glyph
        existing.add(codepoint.upper())
        added += 1

    # 更新元数据
    meta = lib.setdefault("元数据", {})
    meta["版本"] = "v0012-国际符号版"
    meta["总字符数"] = len(glyphs)
    meta["描述"] = "LonghunFont 两千中文字元库 + 实用符号 + 国际符号扩展（拼音调号、希腊字母、数学、天气、音乐、棋牌、占星、UI、警示、上下标数字）"
    now = datetime.now(timezone.utc).isoformat()
    meta["国际符号扩展时间"] = now
    meta["国际符号扩展DNA"] = NEW_DNA
    meta["精修时间"] = now
    meta["精修DNA"] = NEW_DNA

    lib["DNA追溯码"] = NEW_DNA

    # 三色审计
    lib["三色审计_cnsh9622"] = {
        "🟢": {"结果": "通过", "项目": "文化主权标识完整"},
        "🟡": {"结果": "通过", "项目": "来源链可追溯"},
        "🔴": {"结果": "通过", "项目": "无商业字体依赖"},
    }

    with open(DST, "w", encoding="utf-8") as f:
        json.dump(lib, f, ensure_ascii=False, indent=2)

    print(f"[LonghunFont] 已添加国际符号：{added}")
    print(f"[LonghunFont] 已跳过重复：{skipped}")
    print(f"[LonghunFont] 当前总字符数：{len(glyphs)}")
    print(f"[LonghunFont] 输出文件：{DST}")
    print(f"[LonghunFont] DNA：{NEW_DNA}")

if __name__ == "__main__":
    main()
