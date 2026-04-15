"""
CNSH Projection · 隐私层

天然去敏规则：
  GPS    → 100米范围内随机偏移（经纬度模糊）
  心情   → 详细标签 → 7色系颜色标签（不暴露具体文字）
  内容   → 永不包含（私域保留，投影层不可见）
  标题   → 永不包含
  DNA码  → 完整公开（本身就是哈希指纹）

Author: 诸葛鑫 (UID9622)
"""

import math
import random
import hashlib

# ── 心情 → 颜色映射（去敏：只显示颜色，不显示文字）────────────────

MOOD_PALETTE = {
    # 兴奋系
    "激动": "#FFD700",   # 金
    "兴奋": "#FF6B35",   # 橙红
    "热情": "#FF4757",   # 红
    # 愉悦系
    "愉快": "#FF9F43",   # 暖橙
    "欢乐": "#FFEAA7",   # 亮黄
    # 平静系
    "平静": "#4ECDC4",   # 青绿
    "平和": "#74B9FF",   # 浅蓝
    "淡然": "#A29BFE",   # 紫蓝
    # 专注系
    "专注": "#6C5CE7",   # 深紫
    "思考": "#81ECEC",   # 冰蓝
    # 感恩/思念
    "感恩": "#55EFC4",   # 翡翠绿
    "思念": "#DDA0DD",   # 淡紫
    # 低落系
    "忧郁": "#636E72",   # 暗灰
    "疲惫": "#2D3436",   # 深灰（投影时稍亮）
    # 坚定
    "坚定": "#E17055",   # 赤棕
    "勇气": "#D63031",   # 深红
    # 好奇
    "好奇": "#00CEC9",   # 青
    "期待": "#FD79A8",   # 粉
}

DEFAULT_COLOR = "#FFFFFF"   # 未知心情 → 白

# 情绪大类（用于统计显示）
MOOD_CATEGORY = {
    "激动": "激情",  "兴奋": "激情",  "热情": "激情",
    "愉快": "愉悦",  "欢乐": "愉悦",
    "平静": "平和",  "平和": "平和",  "淡然": "平和",
    "专注": "专注",  "思考": "专注",
    "感恩": "感恩",  "思念": "感恩",
    "忧郁": "忧郁",  "疲惫": "忧郁",
    "坚定": "坚毅",  "勇气": "坚毅",
    "好奇": "好奇",  "期待": "好奇",
}


def mood_to_color(mood: str) -> str:
    """心情标签 → 颜色代码"""
    if not mood:
        return DEFAULT_COLOR
    # 精确匹配
    if mood in MOOD_PALETTE:
        return MOOD_PALETTE[mood]
    # 前缀模糊匹配
    for key, color in MOOD_PALETTE.items():
        if key in mood or mood in key:
            return color
    # 哈希稳定颜色（确保相同心情输入总得到相同颜色）
    h = int(hashlib.md5(mood.encode()).hexdigest()[:6], 16)
    return f"#{h:06X}"


def mood_to_category(mood: str) -> str:
    return MOOD_CATEGORY.get(mood, "其他")


# ── GPS 模糊化 ─────────────────────────────────────────────────────

def fuzz_gps(lat: float, lng: float, radius_m: float = 100.0) -> tuple:
    """
    GPS模糊化：在半径 radius_m 米内随机偏移。

    默认100米 → 无法定位到具体建筑或房间。
    保证：相同输入不同次调用结果不同（随机，不可反推）。
    """
    if lat == 0 and lng == 0:
        return 0.0, 0.0

    earth_r = 6_371_000.0
    # 1度纬度 ≈ 111km
    delta_lat = (radius_m / earth_r) * (180 / math.pi)
    cos_lat = math.cos(math.radians(lat)) or 0.0001
    delta_lng = delta_lat / cos_lat

    # 均匀分布在圆内（非矩形）
    angle = random.uniform(0, 2 * math.pi)
    dist  = math.sqrt(random.uniform(0, 1)) * radius_m

    fuzz_lat = lat + (dist / earth_r) * (180 / math.pi) * math.cos(angle)
    fuzz_lng = lng + (dist / earth_r) * (180 / math.pi) * math.sin(angle) / cos_lat

    # 保留4位小数（精度约11米，足够模糊）
    return round(fuzz_lat, 4), round(fuzz_lng, 4)


# ── 天气 → 粒子效果标签 ───────────────────────────────────────────

WEATHER_EFFECT = {
    "晴":  "sunny",
    "多云": "cloudy",
    "阴":  "overcast",
    "雨":  "rain",
    "雪":  "snow",
    "雾":  "fog",
    "雷":  "storm",
}

def weather_to_effect(weather_desc: str) -> str:
    """天气描述 → 粒子效果名（供前端Three.js使用）"""
    if not weather_desc:
        return "clear"
    for key, effect in WEATHER_EFFECT.items():
        if key in weather_desc:
            return effect
    return "clear"


# ── 节点隐私净化 ──────────────────────────────────────────────────

def sanitize_node(raw: dict, fuzz_radius: float = 100.0) -> dict:
    """
    将原始 DNA-Calendar 事件净化为投影安全节点。

    投影节点包含：时间 / 模糊GPS / 城市 / 情绪颜色 / 天气效果 / DNA码
    投影节点不含：标题 / 备注 / 具体内容 / 完整GPS
    """
    lat, lng = fuzz_gps(
        float(raw.get("lat") or 0),
        float(raw.get("lng") or 0),
        fuzz_radius,
    )
    mood  = raw.get("mood") or ""
    color = mood_to_color(mood)

    return {
        "dna":      raw.get("dna_trace") or raw.get("dna") or "",
        "lat":      lat,
        "lng":      lng,
        "city":     raw.get("city") or "",
        "color":    color,
        "mood_cat": mood_to_category(mood),     # 大类，不暴露具体文字
        "weather":  raw.get("weather_desc") or "",
        "temp":     raw.get("weather_temp"),
        "emoji":    raw.get("weather_emoji") or "🌍",
        "effect":   weather_to_effect(raw.get("weather_desc") or ""),
        "time":     raw.get("timestamp") or 0,
        # 注意：title / notes / content 永不出现
    }
