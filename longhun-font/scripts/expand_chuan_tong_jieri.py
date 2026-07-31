# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-CHUAN_TONG_JIERI-v1.0
"""
龍魂字体 · 传统节日图标片段生成器
生成 15 个传统节日图标，起始于 PUA 码位 U+E432。
"""

import json
import math
import os

OUTPUT_DIR = "/Users/zuimeidedeyihan/longhun-system/longhun-font/glyphs/fragments"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "chuan_tong_jieri.json")

SYMBOL_SET_NAME = "chuan_tong_jieri"
COUNT = 15
START_CODEPOINT = 0xE432
DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-CHUAN_TONG_JIERI-v1.0"


def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [round(x, 2), round(y, 2)]}


def stroke_line(x, y):
    return {"类型": "直线段", "终点": [round(x, 2), round(y, 2)]}


def polyline(points):
    if not points:
        return []
    cmds = [stroke_move(points[0][0], points[0][1])]
    for x, y in points[1:]:
        cmds.append(stroke_line(x, y))
    return cmds


def circle(cx, cy, r, segments=12):
    cmds = []
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if i == 0:
            cmds.append(stroke_move(x, y))
        else:
            cmds.append(stroke_line(x, y))
    return cmds


def arc(cx, cy, r, start_angle, end_angle, segments=12):
    cmds = []
    for i in range(segments + 1):
        t = i / segments
        angle = start_angle + (end_angle - start_angle) * t
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if i == 0:
            cmds.append(stroke_move(x, y))
        else:
            cmds.append(stroke_line(x, y))
    return cmds


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


def star(cx, cy, outer_r, inner_r, points=5):
    cmds = []
    for i in range(points * 2 + 1):
        angle = math.pi / 2 + i * math.pi / points
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + r * math.cos(angle)
        y = cy - r * math.sin(angle)
        if i == 0:
            cmds.append(stroke_move(x, y))
        else:
            cmds.append(stroke_line(x, y))
    return cmds


# ---------------------------------------------------------------------------
# 节日图标设计：每个图标均由粗线条轮廓构成，保证小尺寸可识别。
# ---------------------------------------------------------------------------

def icon_chunjie():
    """春节 —— 红灯笼"""
    cmds = []
    # 顶部挂环
    cmds.extend(arc(300, 125, 15, math.pi, 0, segments=8))
    # 灯笼外框
    cmds.extend(rect(250, 155, 350, 325))
    # 灯笼骨架
    cmds.extend(vline(283, 155, 325))
    cmds.extend(vline(317, 155, 325))
    cmds.extend(hline(210, 250, 350))
    cmds.extend(hline(270, 250, 350))
    # 底部流苏
    cmds.extend(vline(300, 325, 390))
    cmds.extend(hline(370, 285, 315))
    cmds.extend(hline(390, 285, 315))
    return cmds


def icon_yuanxiao():
    """元宵 —— 圆灯笼"""
    cmds = []
    # 挂钩
    cmds.extend(polyline([(300, 130), (300, 155)]))
    # 圆形灯身
    cmds.extend(circle(300, 245, 85, segments=16))
    # 灯身装饰横纹
    cmds.extend(hline(200, 230, 370))
    cmds.extend(hline(290, 230, 370))
    # 底部流苏
    cmds.extend(vline(300, 330, 390))
    cmds.extend(polyline([(285, 350), (315, 350)]))
    cmds.extend(polyline([(285, 370), (315, 370)]))
    return cmds


def icon_qingming():
    """清明 —— 柳枝与雨滴"""
    cmds = []
    # 主干
    cmds.extend(vline(300, 120, 420))
    # 柳条
    cmds.extend(polyline([(300, 180), (250, 220), (235, 210)]))
    cmds.extend(polyline([(300, 220), (350, 260), (365, 250)]))
    cmds.extend(polyline([(300, 260), (250, 300), (235, 290)]))
    cmds.extend(polyline([(300, 300), (350, 340), (365, 330)]))
    # 雨滴
    cmds.extend(polyline([(230, 360), (220, 385)]))
    cmds.extend(polyline([(260, 370), (250, 395)]))
    cmds.extend(polyline([(340, 360), (330, 385)]))
    cmds.extend(polyline([(370, 370), (360, 395)]))
    return cmds


def icon_duanwu():
    """端午 —— 粽子"""
    cmds = []
    # 粽叶外形（三角形）
    cmds.extend(polyline([(250, 170), (350, 170), (300, 330), (250, 170)]))
    # 缠绕的棉线
    cmds.extend(polyline([(265, 190), (335, 190)]))
    cmds.extend(polyline([(275, 250), (325, 250)]))
    cmds.extend(polyline([(250, 170), (350, 170)]))
    # 装饰竖线
    cmds.extend(vline(300, 170, 330))
    return cmds


def icon_qixi():
    """七夕 —— 鹊桥与双星"""
    cmds = []
    # 鹊桥弧线
    cmds.extend(arc(300, 360, 130, math.pi, 0, segments=16))
    # 桥栏
    cmds.extend(polyline([(190, 345), (190, 315)]))
    cmds.extend(polyline([(230, 295), (230, 265)]))
    cmds.extend(polyline([(300, 230), (300, 200)]))
    cmds.extend(polyline([(370, 265), (370, 295)]))
    cmds.extend(polyline([(410, 315), (410, 345)]))
    # 双星
    cmds.extend(star(220, 155, 18, 8, points=4))
    cmds.extend(star(380, 155, 18, 8, points=4))
    return cmds


def icon_zhongqiu():
    """中秋 —— 圆月"""
    cmds = []
    # 月亮外圆
    cmds.extend(circle(300, 280, 95, segments=18))
    # 月兔简笔
    cmds.extend(polyline([(300, 220), (300, 340)]))
    cmds.extend(polyline([(270, 250), (330, 250)]))
    cmds.extend(polyline([(300, 280), (260, 310)]))
    cmds.extend(polyline([(300, 280), (340, 310)]))
    # 云朵
    cmds.extend(arc(420, 350, 30, math.pi, 0, segments=8))
    cmds.extend(arc(460, 340, 25, math.pi, 0, segments=8))
    return cmds


def icon_chongyang():
    """重阳 —— 菊花"""
    cmds = []
    # 花心
    cmds.extend(circle(300, 300, 30, segments=10))
    # 花瓣（8瓣）
    for i in range(8):
        angle = i * math.pi / 4
        cx = 300 + 65 * math.cos(angle)
        cy = 300 + 65 * math.sin(angle)
        cmds.extend(circle(cx, cy, 28, segments=8))
    return cmds


def icon_dongzhi():
    """冬至 —— 饺子"""
    cmds = []
    # 饺子月牙外形
    cmds.extend(arc(300, 300, 100, math.pi * 0.85, math.pi * 0.15, segments=16))
    # 褶边
    cmds.extend(polyline([(235, 260), (245, 280), (260, 295), (280, 305), (300, 310), (320, 305), (340, 295), (355, 280), (365, 260)]))
    return cmds


def icon_laba():
    """腊八 —— 粥碗"""
    cmds = []
    # 碗身
    cmds.extend(arc(300, 260, 100, 0, math.pi, segments=14))
    # 碗口
    cmds.extend(hline(200, 200, 400))
    # 热气
    cmds.extend(arc(270, 170, 18, math.pi, 0, segments=8))
    cmds.extend(arc(300, 155, 18, math.pi, 0, segments=8))
    cmds.extend(arc(330, 170, 18, math.pi, 0, segments=8))
    # 勺子
    cmds.extend(polyline([(360, 240), (410, 190)]))
    cmds.extend(circle(410, 185, 12, segments=8))
    return cmds


def icon_xiaonian():
    """小年 —— 灶糖/糖瓜"""
    cmds = []
    # 糖瓜主体
    cmds.extend(circle(300, 300, 75, segments=14))
    # 表面芝麻/糖纹
    cmds.extend(polyline([(260, 270), (340, 270)]))
    cmds.extend(polyline([(250, 300), (350, 300)]))
    cmds.extend(polyline([(260, 330), (340, 330)]))
    cmds.extend(polyline([(300, 240), (300, 360)]))
    return cmds


def icon_chuxi():
    """除夕 —— 鞭炮"""
    cmds = []
    # 炮身
    cmds.extend(rect(275, 150, 325, 360))
    # 引信
    cmds.extend(polyline([(300, 150), (300, 120), (330, 100)]))
    # 火花
    cmds.extend(polyline([(330, 100), (345, 80)]))
    cmds.extend(polyline([(330, 100), (355, 95)]))
    cmds.extend(polyline([(330, 100), (350, 115)]))
    # 装饰横纹
    cmds.extend(hline(180, 275, 325))
    cmds.extend(hline(220, 275, 325))
    cmds.extend(hline(260, 275, 325))
    cmds.extend(hline(300, 275, 325))
    cmds.extend(hline(340, 275, 325))
    return cmds


def icon_zhongyuan():
    """中元 —— 河灯"""
    cmds = []
    # 莲花瓣
    for i in range(6):
        angle = i * math.pi / 3
        cx = 300 + 45 * math.cos(angle)
        cy = 300 + 45 * math.sin(angle)
        cmds.extend(circle(cx, cy, 35, segments=8))
    # 花心烛焰
    cmds.extend(circle(300, 300, 18, segments=8))
    cmds.extend(polyline([(300, 300), (300, 255)]))
    # 水面波纹
    cmds.extend(arc(300, 380, 70, 0, math.pi, segments=10))
    cmds.extend(arc(300, 405, 55, 0, math.pi, segments=10))
    return cmds


def icon_hanshi():
    """寒食 —— 禁火冷食"""
    cmds = []
    # 锅/鼎
    cmds.extend(polyline([(230, 380), (230, 260), (370, 260), (370, 380)]))
    cmds.extend(arc(300, 380, 70, 0, math.pi, segments=10))
    # 锅盖
    cmds.extend(polyline([(220, 260), (300, 200), (380, 260)]))
    # 禁火符号（斜叉）
    cmds.extend(polyline([(255, 320), (345, 320)]))
    return cmds


def icon_sheri():
    """社日 —— 土坛"""
    cmds = []
    # 三层祭坛
    cmds.extend(rect(180, 400, 420, 440))
    cmds.extend(rect(220, 340, 380, 400))
    cmds.extend(rect(260, 280, 340, 340))
    # 顶部立牌/社木
    cmds.extend(vline(300, 200, 280))
    cmds.extend(hline(200, 270, 330))
    cmds.extend(polyline([(270, 200), (330, 200)]))
    return cmds


def icon_lichun():
    """立春 —— 春芽"""
    cmds = []
    # 地面
    cmds.extend(hline(420, 200, 400))
    # 幼芽茎
    cmds.extend(polyline([(300, 420), (300, 320)]))
    # 左叶
    cmds.extend(arc(300, 320, 50, math.pi, math.pi / 2, segments=10))
    cmds.extend(polyline([(250, 320), (300, 320)]))
    # 右叶
    cmds.extend(arc(300, 300, 45, 0, -math.pi / 2, segments=10))
    cmds.extend(polyline([(300, 300), (345, 300)]))
    # 顶芽
    cmds.extend(circle(300, 270, 18, segments=8))
    return cmds


FESTIVALS = [
    ("春节", icon_chunjie),
    ("元宵", icon_yuanxiao),
    ("清明", icon_qingming),
    ("端午", icon_duanwu),
    ("七夕", icon_qixi),
    ("中秋", icon_zhongqiu),
    ("重阳", icon_chongyang),
    ("冬至", icon_dongzhi),
    ("腊八", icon_laba),
    ("小年", icon_xiaonian),
    ("除夕", icon_chuxi),
    ("中元", icon_zhongyuan),
    ("寒食", icon_hanshi),
    ("社日", icon_sheri),
    ("立春", icon_lichun),
]

STYLE_PARAMS = {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9}


def make_glyph(codepoint, name, path):
    return {
        "unicode": f"U+{codepoint:04X}",
        "笔画数": len(path),
        "结构": "节日图标",
        "名称": name,
        "风格参数": STYLE_PARAMS,
        "笔画路径_cnsh9622": path,
    }


def main():
    fragment = {}
    for idx, (name, builder) in enumerate(FESTIVALS):
        codepoint = START_CODEPOINT + idx
        path = builder()
        glyph = make_glyph(codepoint, name, path)
        fragment[chr(codepoint)] = glyph

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    end_codepoint = START_CODEPOINT + COUNT - 1
    print(f"【龍魂字体】传统节日图标片段生成完毕")
    print(f"符号集名称: {SYMBOL_SET_NAME}")
    print(f"生成数量: {COUNT}")
    print(f"码位范围: U+{START_CODEPOINT:04X} - U+{end_codepoint:04X}")
    print(f"输出文件: {OUTPUT_FILE}")
    print(f"DNA: {DNA}")


if __name__ == "__main__":
    main()
