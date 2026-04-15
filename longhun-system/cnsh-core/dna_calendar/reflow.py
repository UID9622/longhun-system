"""
时光回流引擎
输入: DNA追溯码 或 timestamp+坐标
输出: 当时的完整时空切片

Author: 诸葛鑫 (UID9622)
"""

from datetime import datetime
from .models import query_event_by_dna, query_events
from .context.weather import fetch_weather, weather_emoji


def reflow_by_dna(dna_trace: str) -> dict:
    """给定DNA码，还原当时场景"""
    event = query_event_by_dna(dna_trace)
    if not event:
        return {"error": f"DNA不存在: {dna_trace}"}
    return _build_scene(event)


def reflow_by_date(user_id: str, date: str) -> list:
    """给定日期，还原当天所有事件"""
    events = query_events(user_id=user_id, date=date)
    return [_build_scene(e) for e in events]


def _build_scene(event: dict) -> dict:
    ts  = event.get("timestamp", 0)
    lat = event.get("geo_lat", 0.0)
    lng = event.get("geo_lng", 0.0)
    dt  = datetime.fromtimestamp(ts)

    # 如果有坐标且天气数据缺失，尝试实时拉取
    wx_desc = event.get("wx_desc", "")
    if lat != 0.0 and lng != 0.0 and (not wx_desc or wx_desc == "未知"):
        live_wx = fetch_weather(lat, lng, ts)
        wx_desc  = live_wx["description"]
        wx_temp  = live_wx["temperature"]
        wx_code  = live_wx["weather_code"]
        wx_wind  = live_wx["wind_speed"]
        wx_humi  = live_wx["humidity"]
    else:
        wx_temp  = event.get("wx_temp", 0.0)
        wx_code  = event.get("wx_code", 0)
        wx_wind  = event.get("wx_wind", 0.0)
        wx_humi  = event.get("wx_humidity", 0.0)

    emoji = weather_emoji(wx_code)

    return {
        "dna_trace":    event.get("dna_trace"),
        "title":        event.get("title"),
        "time":         dt.strftime("%Y-%m-%d %H:%M:%S"),
        "weekday":      ["周一","周二","周三","周四","周五","周六","周日"][dt.weekday()],
        "mood":         event.get("mood", ""),
        "notes":        event.get("notes", ""),
        "location": {
            "lat":     lat,
            "lng":     lng,
            "city":    event.get("geo_city", ""),
            "address": event.get("geo_address", ""),
        },
        "weather": {
            "emoji":       emoji,
            "description": wx_desc,
            "temperature": wx_temp,
            "humidity":    wx_humi,
            "wind_speed":  wx_wind,
            "code":        wx_code,
        },
        "chain": {
            "prev_hash":  event.get("prev_hash", ""),
            "this_hash":  event.get("this_hash", ""),
            "event_hash": event.get("event_hash", ""),
        },
        "summary": (
            f"{emoji} {wx_desc} {wx_temp}°C · "
            f"{event.get('geo_city') or '未知地点'} · "
            f"{dt.strftime('%Y年%m月%d日 %H:%M')}"
        ),
    }
