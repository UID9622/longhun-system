# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-FONT-GLYPH-GENERATOR-CALLIGRAPHY-v2.0
# 用途: 生成 LonghunFont 书法风格占位骨架 v2.0（曲线笔意 +  brush tips）

"""
LonghunFont 书法骨架生成器 v2.0

与 glyph_generator.py 保持相同公开接口：
  - structure_of(char)
  - stroke_count_of(char)
  - generate_skeleton(char)

本模块生成的骨架带有倾斜势、三角笔锋与二次贝塞尔曲线化笔画，
用于模拟毛笔书写的“势”，仍作为可编辑占位字形使用。
"""

import json
import math
import random
from pathlib import Path
from datetime import datetime


DNA = "#龍芯⚡️2026-06-23-LONGHUN-FONT-GLYPH-GENERATOR-CALLIGRAPHY-v2.0"

CORE_CHARS = (
    "一二三四五六七八九十"
    "人口手大小上下左右中"
    "天地日月水火木土金石"
    "山河江海田野林草花风"
    "雨雪云雾雷电春夏秋冬"
    "东南西北国家乡心文明"
    "和平正义自由民主富强"
    "工农科技智慧学问思考"
    "创新团结奋斗强盛贵望"
    "信爱真善美德道理法将"
    "王皇帝龍魂中华民芯"
    "制造产业机器电脑软件"
    "系统网络安全数据云端"
    "智能硬件芯片材料能源"
    "汽车飞机铁路桥梁建筑"
    "食品药品衣服住房交通"
    "医教商银钱股市政军警"
    "颜色形声香味味冷热光"
    "快慢高低远近长短宽窄"
    "多少轻重深浅难易新旧"
    "来去出入开关升降进出"
)


# ---------------------------------------------------------------------------
# 结构判断：高频经验字典 + 部首 fallback
# ---------------------------------------------------------------------------

_LEFT_RIGHT = set(
    "你他们何江河湖海林标说话认得识纪给结缔伯仲佟佬佃"
    "但作使依便信候借值做停偷像全公共关具分刘刚创"
    "别制刷剂刻刺剧剪加动助努劳励医华协卓单卖博却印压"
    "呀咳啊唉哦喂喘喝喊嘛嘴嘿嗯啪啦啫嗅嗜嗟嗡嗦"
    "啤啷喀喏嗒喃善喑喓喔嗔嘘"
    "左右结构常见字"
)

_LEFT_MIDDLE_RIGHT = set("衍衔街衙彬棚滩辩辨辫鵰嫩嗽懒獭")

_TOP_BOTTOM = set(
    "一二三四五六七八九十天地金雪雷思字音示旨冒昔昙春昼"
    "显晋查旦早旨旬旭旱旷时旷昆昌明昏易昔星春是显晋晒晓晕晚景"
    "晴晶智暂暑暴曙曛耀枣果某架案桌桨梨梯检棋棕棚楚概槽"
    "歪泵皇孟盅盆盒盘益盖盟盘尽"
    "上下结构常见字"
)

_TOP_MIDDLE_BOTTOM = set("曼宴莺意章竟嚣翼冀累呆器葬幕慕募摹蔓孽暴暹")

_SURROUND = set("回田目口囗国因园困团图圈圈围圆固团圆")

_HALF_SURROUND = set(
    "匡区巨匠匣医匿匾匹汇匠匣匡匿匾匹"
    "句勾包匆旬甸匍匏匐勺勾包甸匍匐匀勿"
    "厅庄庆床庐店庙府度庭康庸廊庑庋庇庖店庙府庚庶庵康庸"
    "建延廷廸廵巡"
    "病疾疼疲疯疫疵痒痕痛痴痊"
    "起跑超越趄趟趔趣趱"
    "左下包右上左上包右下右上包左下"
)

_PIN = set("品晶森众磊鑫矗聂焱淼犇羴蟲猋麤掱龘骉贔")

_INLAY = set("坐巫噩爽夾")


def structure_of(char: str) -> str:
    """基于经验字典判断结构"""
    if char in _SURROUND:
        return "包围"
    if char in _PIN:
        return "品字形"
    if char in _INLAY:
        return "镶嵌"
    if char in _HALF_SURROUND:
        return "半包围"
    if char in _LEFT_MIDDLE_RIGHT:
        return "左中右"
    if char in _LEFT_RIGHT:
        return "左右"
    if char in _TOP_MIDDLE_BOTTOM:
        return "上中下"
    if char in _TOP_BOTTOM:
        return "上下"
    left_radicals = "亻彳讠忄扌木氵钅纟衤礻阝刂牜犭王足目耳口饣鱼虫马羊鸟虫禾米矢石钅衤"
    if any(char.startswith(r) for r in left_radicals):
        return "左右"
    return "单一"


def stroke_count_of(char: str) -> int:
    """返回笔画数（简化，使用常见值）"""
    common_counts = {
        "一": 1, "二": 2, "三": 3, "四": 5, "五": 4, "六": 4, "七": 2, "八": 2, "九": 2, "十": 2,
        "人": 2, "口": 3, "手": 4, "大": 3, "小": 3, "上": 3, "下": 3, "左": 5, "右": 5, "中": 4,
        "天": 4, "地": 6, "日": 4, "月": 4, "水": 4, "火": 4, "木": 4, "土": 3, "金": 8, "石": 5,
        "山": 3, "河": 8, "江": 6, "海": 10, "田": 5, "野": 11, "林": 8, "草": 9, "花": 7, "风": 4,
        "雨": 8, "雪": 11, "云": 4, "雾": 13, "雷": 13, "电": 5, "春": 9, "夏": 10, "秋": 9, "冬": 5,
        "东": 5, "西": 6, "南": 9, "北": 5, "国": 8, "家": 10, "乡": 3, "心": 4, "文": 4, "明": 8,
        "和": 8, "平": 5, "正": 5, "义": 3, "自": 6, "由": 5, "民": 5, "主": 5, "富": 12, "强": 12,
        "工": 3, "农": 6, "科": 9, "技": 7, "智": 12, "慧": 15, "学": 8, "问": 6, "思": 9, "考": 6,
        "创": 12, "新": 13, "团": 6, "结": 9, "奋": 8, "斗": 4, "盛": 11, "贵": 9, "望": 11, "信": 9,
        "爱": 10, "真": 10, "善": 12, "美": 9, "德": 15, "道": 12, "理": 11, "法": 8, "将": 9, "王": 4,
        "皇": 9, "帝": 9, "龍": 5, "魂": 13, "中": 4, "华": 6, "民": 5, "芯": 7,
        "制": 8, "造": 10, "产": 6, "业": 5, "机": 6, "器": 16, "电": 5, "脑": 10, "软": 8, "件": 6,
        "系": 7, "络": 9, "安": 6, "全": 6, "数": 13, "据": 11, "云": 4, "端": 14,
        "汽": 7, "车": 4, "飞": 3, "铁": 10, "路": 13, "桥": 10, "梁": 11, "建": 8, "筑": 12,
        "食": 9, "医": 7, "教": 11, "商": 11, "银": 14, "钱": 10, "股": 8, "市": 5, "政": 9, "军": 6, "警": 19,
        "颜": 15, "色": 6, "形": 7, "声": 7, "香": 9, "味": 8, "冷": 7, "热": 10, "光": 6,
        "快": 7, "慢": 14, "高": 10, "低": 7, "远": 7, "近": 7, "长": 4, "短": 12, "宽": 10, "窄": 10,
        "多": 6, "少": 4, "轻": 9, "重": 9, "深": 11, "浅": 8, "难": 10, "易": 8, "新": 13, "旧": 5,
        "来": 7, "去": 5, "出": 5, "入": 2, "开": 4, "关": 6, "升": 4, "降": 8, "进": 7, "出": 5,
    }
    return common_counts.get(char, 8)


# ---------------------------------------------------------------------------
# 骨架绘制辅助（书法笔意）
# ---------------------------------------------------------------------------

def _move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def _line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def _curve_points(p0, p1, p2, segments=8):
    """二次贝塞尔曲线采样，返回中间点（不含 p0，含 p2）"""
    points = []
    for i in range(1, segments + 1):
        t = i / segments
        t1 = 1 - t
        x = t1 * t1 * p0[0] + 2 * t1 * t * p1[0] + t * t * p2[0]
        y = t1 * t1 * p0[1] + 2 * t1 * t * p1[1] + t * t * p2[1]
        points.append([x, y])
    return points


def _curve_strokes(p0, p1, p2, segments=8, tip_end=True, tip_start=False):
    """用连续直线段逼近二次贝塞尔曲线，可带笔锋"""
    pts = _curve_points(p0, p1, p2, segments)
    strokes = [_move(p0[0], p0[1])]
    for x, y in pts:
        strokes.append(_line(x, y))
    if tip_end:
        strokes += _brush_tip(pts[-1][0], pts[-1][1], pts[-2][0], pts[-2][1])
    if tip_start:
        strokes += _brush_tip(p0[0], p0[1], pts[0][0], pts[0][1])
    return strokes


def _brush_tip(end_x, end_y, prev_x, prev_y, tip_len=10, base_w=6):
    """在笔画末端添加三角笔锋"""
    dx = end_x - prev_x
    dy = end_y - prev_y
    d = math.hypot(dx, dy)
    if d < 1:
        return []
    ux, uy = dx / d, dy / d
    px, py = -uy, ux
    ax = end_x + ux * tip_len
    ay = end_y + uy * tip_len
    bx = end_x - ux * tip_len * 0.5 + px * base_w
    by = end_y - uy * tip_len * 0.5 + py * base_w
    cx = end_x - ux * tip_len * 0.5 - px * base_w
    cy = end_y - uy * tip_len * 0.5 - py * base_w
    return [
        _move(bx, by), _line(ax, ay), _line(cx, cy)
    ]


def _line_with_tips(x1, y1, x2, y2, tip_end=True, tip_start=False):
    strokes = [_move(x1, y1), _line(x2, y2)]
    if tip_end:
        strokes += _brush_tip(x2, y2, x1, y1)
    if tip_start:
        strokes += _brush_tip(x1, y1, x2, y2)
    return strokes


def _slanted_points(x1, y1, x2, y2, shear=0.0, ox=0.0, oy=0.0):
    """返回经过剪切与偏移的矩形四个角（顺序：左上、右上、右下、左下）"""
    cx = (x1 + x2) / 2 + ox
    cy = (y1 + y2) / 2 + oy
    hx = (x2 - x1) / 2
    hy = (y2 - y1) / 2

    def pt(rx, ry):
        return [cx + rx + shear * ry, cy + ry]

    return pt(-hx, -hy), pt(hx, -hy), pt(hx, hy), pt(-hx, hy)


def _rect_sides(p0, p1, p2, p3):
    """绘制倾斜矩形的四条边，并在每个端点加笔锋"""
    strokes = []
    for a, b in ((p0, p1), (p1, p2), (p2, p3), (p3, p0)):
        strokes += _line_with_tips(a[0], a[1], b[0], b[1], tip_end=True, tip_start=True)
    return strokes


def _cross_in_panel(p0, p1, p2, p3):
    """在倾斜矩形内部绘制十字，两端带笔锋"""
    top_mid = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2]
    bottom_mid = [(p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2]
    left_mid = [(p0[0] + p3[0]) / 2, (p0[1] + p3[1]) / 2]
    right_mid = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return (
        _line_with_tips(top_mid[0], top_mid[1], bottom_mid[0], bottom_mid[1])
        + _line_with_tips(left_mid[0], left_mid[1], right_mid[0], right_mid[1])
    )


def _panel(x1, y1, x2, y2, shear=0.0, ox=0.0, oy=0.0):
    """倾斜矩形 + 内部十字"""
    p0, p1, p2, p3 = _slanted_points(x1, y1, x2, y2, shear, ox, oy)
    return _rect_sides(p0, p1, p2, p3) + _cross_in_panel(p0, p1, p2, p3)


def _curved_horizontal(left_x, left_y, right_x, right_y, bulge=12):
    """用二次贝塞尔曲线生成带弧度的横画"""
    mx = (left_x + right_x) / 2
    my = (left_y + right_y) / 2 + bulge
    return _curve_strokes(
        [left_x, left_y], [mx, my], [right_x, right_y],
        segments=8, tip_end=True, tip_start=True
    )


def _curved_slash(x1, y1, x2, y2, bulge=20):
    """弯曲撇/捺"""
    mx = (x1 + x2) / 2 + bulge
    my = (y1 + y2) / 2
    return _curve_strokes(
        [x1, y1], [mx, my], [x2, y2],
        segments=8, tip_end=True, tip_start=True
    )


def _in_bounds(strokes, low=0, high=600):
    """检查所有坐标是否在边界内"""
    for s in strokes:
        for k in ("坐标", "终点"):
            if k in s:
                x, y = s[k]
                if not (low <= x <= high and low <= y <= high):
                    return False
    return True


# ---------------------------------------------------------------------------
# 按结构生成书法骨架
# ---------------------------------------------------------------------------

def generate_skeleton(char: str) -> list[Any]:
    """根据结构生成带有手写笔意的参数化骨架"""
    structure = structure_of(char)
    rng = random.Random(ord(char))

    def vary(scale=0.06, trans=12):
        return rng.uniform(-scale, scale), rng.uniform(-trans, trans), rng.uniform(-trans, trans)

    if structure == "单一":
        s, ox, oy = vary()
        p0, p1, p2, p3 = _slanted_points(120, 120, 480, 480, s, ox, oy)
        strokes = _rect_sides(p0, p1, p2, p3)
        # 米字交叉：横竖用微曲贝塞尔
        cx = (p0[0] + p1[0] + p2[0] + p3[0]) / 4
        cy = (p0[1] + p1[1] + p2[1] + p3[1]) / 4
        strokes += _curve_strokes(
            [p0[0], p0[1]],
            [cx + rng.uniform(-25, 25), cy + rng.uniform(-25, 25)],
            [p2[0], p2[1]],
            segments=8, tip_end=True, tip_start=True
        )
        strokes += _curve_strokes(
            [p1[0], p1[1]],
            [cx + rng.uniform(-25, 25), cy + rng.uniform(-25, 25)],
            [p3[0], p3[1]],
            segments=8, tip_end=True, tip_start=True
        )
        # 短撇短捺曲线
        strokes += _curved_slash(
            cx - 40, cy - 50, cx - 90, cy + 40,
            bulge=rng.choice((-18, 18))
        )
        strokes += _curved_slash(
            cx + 40, cy - 50, cx + 90, cy + 40,
            bulge=rng.choice((-18, 18))
        )
        return strokes

    if structure == "左右":
        s1, ox1, oy1 = vary()
        s2, ox2, oy2 = vary()
        # 左部：竖向长面板 + 竖divider（整体向左倾）
        lp0, lp1, lp2, lp3 = _slanted_points(80, 100, 280, 500, s1 - 0.03, ox1 - 5, oy1)
        left = _rect_sides(lp0, lp1, lp2, lp3)
        left += _line_with_tips(
            (lp0[0] + lp3[0]) / 2, (lp0[1] + lp3[1]) / 2,
            (lp1[0] + lp2[0]) / 2, (lp1[1] + lp2[1]) / 2,
            tip_end=True, tip_start=True
        )
        # 右部：横向长面板 + 两条微曲横画 + 斜向 divider
        rp0, rp1, rp2, rp3 = _slanted_points(320, 100, 520, 500, s2 + 0.03, ox2 + 5, oy2)
        right = _rect_sides(rp0, rp1, rp2, rp3)
        right += _line_with_tips(
            (rp0[0] + rp3[0]) / 2 + 10, (rp0[1] + rp3[1]) / 2,
            (rp1[0] + rp2[0]) / 2 - 10, (rp1[1] + rp2[1]) / 2,
            tip_end=True, tip_start=True
        )
        right += _curved_horizontal(
            (rp0[0] + rp3[0]) / 2, (rp0[1] + rp3[1]) / 2 + 35,
            (rp1[0] + rp2[0]) / 2, (rp1[1] + rp2[1]) / 2 + 35,
            bulge=rng.choice((-12, 12))
        )
        right += _curved_horizontal(
            (rp0[0] + rp3[0]) / 2, (rp0[1] + rp3[1]) / 2 - 35,
            (rp1[0] + rp2[0]) / 2, (rp1[1] + rp2[1]) / 2 - 35,
            bulge=rng.choice((-12, 12))
        )
        # 斜向分隔线
        divider = _line_with_tips(
            (lp1[0] + lp2[0]) / 2, (lp1[1] + lp2[1]) / 2 - 60,
            (rp0[0] + rp3[0]) / 2, (rp0[1] + rp3[1]) / 2 + 60,
            tip_end=True, tip_start=True
        )
        return left + divider + right

    if structure == "左中右":
        strokes = []
        shears = [-0.04, 0.0, 0.04]
        for idx, (x1, x2) in enumerate(((60, 220), (240, 360), (380, 540))):
            s, ox, oy = vary()
            s += shears[idx]
            strokes += _panel(x1, 120, x2, 480, s, ox, oy)
        return strokes

    if structure == "上下":
        s1, ox1, oy1 = vary()
        s2, ox2, oy2 = vary()
        # 上梯形面板：上窄下宽
        tp0, tp1 = [110 + ox1, 90 + oy1], [490 + ox1, 90 + oy1]
        tp2 = [520 + ox1 + s1 * 190, 270 + oy1]
        tp3 = [80 + ox1 + s1 * 190, 270 + oy1]
        top = _line_with_tips(tp0[0], tp0[1], tp1[0], tp1[1], tip_end=True, tip_start=True)
        top += _line_with_tips(tp1[0], tp1[1], tp2[0], tp2[1], tip_end=True, tip_start=True)
        top += _line_with_tips(tp2[0], tp2[1], tp3[0], tp3[1], tip_end=True, tip_start=True)
        top += _line_with_tips(tp3[0], tp3[1], tp0[0], tp0[1], tip_end=True, tip_start=True)
        top += _line_with_tips(
            (tp0[0] + tp3[0]) / 2, (tp0[1] + tp3[1]) / 2,
            (tp1[0] + tp2[0]) / 2, (tp1[1] + tp2[1]) / 2,
            tip_end=True, tip_start=True
        )
        # 下梯形面板：上宽下窄
        bp3, bp2 = [80 + ox2, 510 + oy2], [520 + ox2, 510 + oy2]
        bp1 = [490 + ox2 + s2 * 190, 330 + oy2]
        bp0 = [110 + ox2 + s2 * 190, 330 + oy2]
        bottom = _line_with_tips(bp0[0], bp0[1], bp1[0], bp1[1], tip_end=True, tip_start=True)
        bottom += _line_with_tips(bp1[0], bp1[1], bp2[0], bp2[1], tip_end=True, tip_start=True)
        bottom += _line_with_tips(bp2[0], bp2[1], bp3[0], bp3[1], tip_end=True, tip_start=True)
        bottom += _line_with_tips(bp3[0], bp3[1], bp0[0], bp0[1], tip_end=True, tip_start=True)
        bottom += _line_with_tips(
            (bp0[0] + bp3[0]) / 2, (bp0[1] + bp3[1]) / 2,
            (bp1[0] + bp2[0]) / 2, (bp1[1] + bp2[1]) / 2,
            tip_end=True, tip_start=True
        )
        return top + bottom

    if structure == "上中下":
        strokes = []
        shears = [-0.03, 0.0, 0.03]
        for idx, (y1, y2) in enumerate(((60, 200), (220, 360), (380, 540))):
            s, ox, oy = vary()
            s += shears[idx]
            strokes += _panel(100, y1, 500, y2, s, ox, oy)
        return strokes

    if structure == "包围":
        s, ox, oy = rng.uniform(-0.04, 0.04), rng.uniform(-10, 10), rng.uniform(-10, 10)
        x1, y1, x2, y2 = 100, 100, 500, 500
        cx = (x1 + x2) / 2 + ox
        cy = (y1 + y2) / 2 + oy
        r = 50

        def frame_point(rx, ry):
            return [cx + rx + s * ry, cy + ry]

        # 圆转倒角外框
        pts = [
            frame_point(-(200 - r), -200),
            frame_point(200 - r, -200),
            frame_point(200, -(200 - r)),
            frame_point(200, 200 - r),
            frame_point(200 - r, 200),
            frame_point(-(200 - r), 200),
            frame_point(-200, 200 - r),
            frame_point(-200, -(200 - r)),
        ]
        strokes = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            strokes += _line_with_tips(a[0], a[1], b[0], b[1], tip_end=True, tip_start=True)
        # 内部倾斜十字，略旋转
        angle = rng.uniform(-0.12, 0.12)
        strokes += _line_with_tips(
            cx - 80 * math.cos(angle), cy - 80 * math.sin(angle),
            cx + 80 * math.cos(angle), cy + 80 * math.sin(angle),
            tip_end=True, tip_start=True
        )
        strokes += _line_with_tips(
            cx - 80 * math.sin(angle), cy + 80 * math.cos(angle),
            cx + 80 * math.sin(angle), cy - 80 * math.cos(angle),
            tip_end=True, tip_start=True
        )
        # 内部小横画，模拟“玉”字点
        strokes += _curved_horizontal(cx - 30, cy - 40, cx + 30, cy - 40, bulge=4)
        return strokes

    if structure == "半包围":
        s, ox, oy = vary(scale=0.05, trans=10)
        x1, y1, x2, y2 = 100, 100, 500, 500
        # L 形外框：左上包右下，带弧度 hook
        p_top_l = [x1 + ox + s * y1, y1 + oy]
        p_top_r = [x2 + ox + s * y1, y1 + oy]
        p_mid_r = [x2 + ox + s * (y1 + 120), y1 + 120 + oy]
        p_bot_l = [x1 + ox + s * y2, y2 + oy]
        p_mid_b = [x1 + 140 + ox + s * y2, y2 + oy]
        frame = (
            _line_with_tips(p_top_l[0], p_top_l[1], p_top_r[0], p_top_r[1], tip_end=True, tip_start=True)
            + _line_with_tips(p_top_l[0], p_top_l[1], p_bot_l[0], p_bot_l[1], tip_end=True, tip_start=True)
            + _line_with_tips(p_bot_l[0], p_bot_l[1], p_mid_b[0], p_mid_b[1], tip_end=True, tip_start=True)
            + _curve_strokes(
                [p_top_r[0], p_top_r[1]],
                [p_mid_r[0] + 30, (p_top_r[1] + p_mid_r[1]) / 2],
                [p_mid_r[0], p_mid_r[1]],
                segments=8, tip_end=True, tip_start=False
            )
        )
        # 内部小十字，偏右下
        ix = (x1 + x2) / 2 + 60 + ox
        iy = (y1 + y2) / 2 + 60 + oy
        inner = (
            _curved_horizontal(ix - 70, iy, ix + 70, iy, bulge=rng.choice((-6, 6)))
            + _line_with_tips(ix, iy - 70, ix, iy + 70, tip_end=True, tip_start=True)
        )
        return frame + inner

    if structure == "品字形":
        strokes = []
        configs = (
            (220, 380, 70, 220, -0.03),   # 上
            (70, 250, 260, 520, 0.04),    # 左下
            (350, 530, 260, 520, -0.04),  # 右下
        )
        for x1, x2, y1, y2, shear_bias in configs:
            s, ox, oy = vary()
            s += shear_bias
            strokes += _panel(x1, y1, x2, y2, s, ox, oy)
        return strokes

    if structure == "镶嵌":
        s1, ox1, oy1 = vary()
        s2, ox2, oy2 = vary()
        strokes = _panel(100, 150, 340, 450, s1 - 0.03, ox1 - 5, oy1)
        strokes += _panel(260, 150, 500, 450, s2 + 0.03, ox2 + 5, oy2)
        # 中央交叉装饰线
        strokes += _line_with_tips(300 + ox1, 180 + oy1, 300 + ox2, 420 + oy2, tip_end=True, tip_start=True)
        return strokes

    # fallback 单一
    s, ox, oy = vary()
    return _panel(100, 100, 500, 500, s, ox, oy)


def generate_glyph_library(chars: str = CORE_CHARS, output_path: str | None = None):
    """生成书法风格字元库 JSON"""
    base_dir = Path(__file__).parent.parent
    output_path = Path(output_path) if output_path else base_dir / "glyphs" / "龍魂字元库_v0002_书法骨架版.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    字符集 = {}
    for char in chars:
        if char in 字符集:
            continue
        strokes = generate_skeleton(char)
        if not _in_bounds(strokes):
            raise ValueError(f"字元 '{char}' 生成坐标越界")
        字符集[char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": stroke_count_of(char),
            "结构": structure_of(char),
            "风格参数": {
                "力度": 0.85,
                "棱角": 0.25,
                "节奏": 0.75,
                "墨色": 0.9
            },
            "笔画路径_cnsh9622": strokes
        }

    data = {
        "DNA追溯码": DNA,
        "元数据": {
            "名称": "龍魂字元库",
            "版本": "v0002-书法骨架版-v2.0",
            "创建者": "UID9622",
            "描述": "LonghunFont 书法风格占位骨架 v2.0，含毛笔笔锋、曲线横画与倾斜结构",
            "编码标准": "UTF-8",
            "viewBox": "0 0 600 600",
            "生成时间": datetime.now().isoformat()
        },
        "三色审计_cnsh9622": {
            "🟢": {"结果": "通过", "项目": "文化主权标识完整"},
            "🟡": {"结果": "通过", "项目": "来源链可追溯"},
            "🔴": {"结果": "通过", "项目": "无商业字体依赖"}
        },
        "字符集_cnsh9622": 字符集
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 书法字元库已生成: {output_path}")
    print(f"   总字元数: {len(字符集)}")
    return str(output_path)


if __name__ == "__main__":
    generate_glyph_library()
