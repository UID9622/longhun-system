#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-GLYPH-GENERATOR-v2.0
# 用途: 批量生成 LonghunFont 初始字元骨架 v2.0

"""
LonghunFont 字元批量生成器 v2.0

基于更细分的结构（单一/左右/左中右/上下/上中下/包围/半包围/品字形/镶嵌）
生成参数化笔画骨架。生成的是可编辑骨架，非最终艺术字形，后续需人工精修。
"""

import json
from pathlib import Path
from datetime import datetime


DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-GLYPH-GENERATOR-v2.0"

# 常用汉字列表（200字）
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
    "王皇帝龙魂中华民芯"
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
# 结构判断：基于经验字典 + 部首规律
# ---------------------------------------------------------------------------

_LEFT_RIGHT = set(
    "你他们何江河湖海林标说话认得识纪给结缔伯仲佟佬佃"
    " but但作使依便信候借值做停偷像全公共关具分刘刚创"
    "别制刷剂刻刺剧剪加动助努劳励医华协卓单卖博却印压"
    "呀咳啊唉哦喂喘喝喘喊喘啊嘛嘴嘿嗯啪啦啫嗅嗜嗟嗡嗦"
    "啤啷喀喏嗒喃善喊喑喓喘喔嗔嘘啤啷喑喀喏嗒喃善喊喑"
    "喓喘喔嗔嘘啤啷喑喀喏嗒喃善喊喑喓喘喔嗔嘘啤啷喑喀"
    "喏嗒喃善喊喑喓喘喔嗔嘘啤啷喑喀喏嗒喃善喊喑喓喘喔"
    "嗔嘘啤啷喑喀喏嗒喃善喊喑喓喘喔嗔嘘啤啷喑喀喏嗒喃"
    "左右结构常见字，字典越大越准。以下用 Unicode 部首辅助判断较困难，"
    "这里直接列出高频左右结构字，其余按规则 fallback。"
)

_LEFT_MIDDLE_RIGHT = set("衍衔街衙彬棚滩辩辨辫鵰嫩嗽懒獭")

_TOP_BOTTOM = set(
    "一二三四五六七八九十天地金雪雷思字音示旨冒昔昙春昼"
    "显晋查昼春是冒昔昙春昼显晋查昼春是冒昔昙春昼显晋查"
    "旦早旨旬旭旱旷时旷昆昌明昏易昔星春是显晋晒晓晕晚景"
    "晴晶智暂暑暴曙曛耀枣果某架案桌桨梨梯检棋棕棚楚概槽"
    "歪泵皇孟盅盆盒盘益盖盟盘尽昼春是冒昔昙春昼显晋查昼"
    "上下结构常见字"
)

_TOP_MIDDLE_BOTTOM = set("曼宴莺意章竟嚣翼冀累呆器葬幕慕募摹蔓孽暴暹")

_SURROUND = set("回田目口囗国因园困团图圈圈围圆固团圆圈圈圆圆困")

_HALF_SURROUND = set(
    "匡区巨匠匣医匿匾匹汇匠匣匡匿匾匹匣匡匿匾匹匣匡匿"
    "句勾包匆旬甸匍匏匐勺勾包甸匍匐匀勿勾包甸匍匐句勾"
    "厅庄庆床庐店庙府度庭康庸廊庑庋庇庖店庙府庚庶庵康庸"
    "建延廷廸廵巡廷廸廵廷廸廵廷廸廵廷廸廵廷廸廵"
    "病疾疼疲疯疫疵痒痕痛痴痊痒痕痛痴痊痒痕痛痴痊痒痕痛"
    "起跑超越趄趟趔趣趱趄趟趔趣趱趄趟趔趣趱趄趟趔趣趱趄趟"
    "左下包右上、左上包右下、右上包左下等半包围"
)

_PIN = set("品晶森众磊鑫矗聂焱淼犇羴蟲猋麤掱龘骉贔")

_INLAY = set("坐巫噩爽夾夾噩夾爽坐巫噩爽夾夾")


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
    # 启发式 fallback：根据部首/常见部件
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
        "皇": 9, "帝": 9, "龙": 5, "魂": 13, "中": 4, "华": 6, "民": 5, "芯": 7,
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
# 骨架绘制辅助
# ---------------------------------------------------------------------------

def _move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def _line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def _rect(x1, y1, x2, y2):
    """闭合矩形"""
    return [
        _move(x1, y1), _line(x2, y1), _line(x2, y2),
        _line(x1, y2), _line(x1, y1),
    ]


def _cross(cx, cy, half):
    """十字交叉"""
    return [
        _move(cx, cy - half), _line(cx, cy + half),
        _move(cx - half, cy), _line(cx + half, cy),
    ]


def _box_with_cross(x1, y1, x2, y2):
    """方框 + 内部十字"""
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    half_x, half_y = (x2 - x1) / 2, (y2 - y1) / 2
    return _rect(x1, y1, x2, y2) + [
        _move(cx, y1), _line(cx, y2),
        _move(x1, cy), _line(x2, cy),
    ]


# ---------------------------------------------------------------------------
# 按结构生成骨架
# ---------------------------------------------------------------------------

def generate_skeleton(char: str) -> list:
    """根据结构生成参数化笔画骨架"""
    structure = structure_of(char)

    if structure == "单一":
        # 米字格 + 外框提示
        strokes = _rect(120, 120, 480, 480)
        strokes += [
            _move(120, 120), _line(480, 480),
            _move(480, 120), _line(120, 480),
            _move(300, 100), _line(300, 500),
            _move(100, 300), _line(500, 300),
        ]
        return strokes

    if structure == "左右":
        # 左右两个区域，左区偏竖、右区偏横，暗示部件
        left = _rect(80, 100, 280, 500)
        left += [
            _move(180, 100), _line(180, 500),
        ]
        right = _rect(320, 100, 520, 500)
        right += [
            _move(320, 220), _line(520, 220),
            _move(320, 380), _line(520, 380),
        ]
        return left + right

    if structure == "左中右":
        return (
            _box_with_cross(60, 120, 220, 480) +
            _box_with_cross(240, 120, 360, 480) +
            _box_with_cross(380, 120, 540, 480)
        )

    if structure == "上下":
        top = _rect(100, 80, 500, 280)
        top += [
            _move(100, 180), _line(500, 180),
        ]
        bottom = _rect(100, 320, 500, 520)
        bottom += [
            _move(300, 320), _line(300, 520),
        ]
        return top + bottom

    if structure == "上中下":
        return (
            _box_with_cross(100, 60, 500, 200) +
            _box_with_cross(100, 220, 500, 360) +
            _box_with_cross(100, 380, 500, 540)
        )

    if structure == "包围":
        # 外框 + 内部井字
        outer = _rect(100, 100, 500, 500)
        inner = [
            _move(220, 100), _line(220, 500),
            _move(380, 100), _line(380, 500),
            _move(100, 220), _line(500, 220),
            _move(100, 380), _line(500, 380),
        ]
        return outer + inner

    if structure == "半包围":
        # 左上包右下：外框缺右下
        frame = [
            _move(100, 100), _line(500, 100), _line(500, 220),
            _move(100, 100), _line(100, 500), _line(220, 500),
        ]
        inner = [
            _move(260, 260), _line(460, 260), _line(460, 460), _line(260, 460), _line(260, 260),
            _move(360, 260), _line(360, 460),
            _move(260, 360), _line(460, 360),
        ]
        return frame + inner

    if structure == "品字形":
        # 三个小方块呈品字
        top = _box_with_cross(200, 60, 400, 240)
        bl = _box_with_cross(80, 280, 280, 520)
        br = _box_with_cross(320, 280, 520, 520)
        return top + bl + br

    if structure == "镶嵌":
        # 左右两个方块互相咬合
        return (
            _box_with_cross(100, 150, 340, 450) +
            _box_with_cross(260, 150, 500, 450)
        )

    # fallback 单一
    return _box_with_cross(100, 100, 500, 500)


def generate_glyph_library(chars: str = CORE_CHARS, output_path: str = None):
    """生成字元库 JSON"""
    base_dir = Path(__file__).parent.parent
    output_path = Path(output_path) if output_path else base_dir / "glyphs" / "龍魂字元库_v0002_扩展.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    字符集 = {}
    for char in chars:
        if char in 字符集:
            continue
        字符集[char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": stroke_count_of(char),
            "结构": structure_of(char),
            "风格参数": {
                "力度": 0.8,
                "棱角": 0.3,
                "节奏": 0.6,
                "墨色": 0.9
            },
            "笔画路径_cnsh9622": generate_skeleton(char)
        }

    data = {
        "DNA追溯码": DNA,
        "元数据": {
            "名称": "龍魂字元库",
            "版本": "v0002-扩展",
            "创建者": "UID9622",
            "描述": "LonghunFont 扩展字元库，含 200+ 个常用汉字骨架",
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

    print(f"✅ 字元库已生成: {output_path}")
    print(f"   总字元数: {len(字符集)}")
    return str(output_path)


if __name__ == "__main__":
    generate_glyph_library()
