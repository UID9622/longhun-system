"""
天气上下文采集器
使用 Open-Meteo API（免费，无需Key，支持历史数据）

Author: 诸葛鑫 (UID9622)
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timezone


# WMO 天气码 → 中文描述
WMO_CODES = {
    0: "晴天", 1: "基本晴", 2: "局部多云", 3: "阴天",
    45: "雾", 48: "冻雾",
    51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "阵雨", 81: "中阵雨", 82: "暴阵雨",
    95: "雷暴", 96: "冰雹雷暴", 99: "大冰雹雷暴",
}


def fetch_weather(lat: float, lng: float, timestamp: float) -> dict:
    """
    获取指定坐标和时间的天气数据
    timestamp: Unix时间戳
    返回: WeatherContext字段的dict
    """
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")
    hour = dt.hour

    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lng,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": "temperature_2m,relativehumidity_2m,surface_pressure,weathercode,windspeed_10m",
        "timezone": "auto",
    })

    url = f"https://archive-api.open-meteo.com/v1/archive?{params}"

    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read())

        hourly = data.get("hourly", {})
        times  = hourly.get("time", [])

        # 找最接近的小时
        idx = hour if hour < len(times) else -1

        code = int(hourly.get("weathercode", [0])[idx] or 0)
        return {
            "temperature": round(float(hourly.get("temperature_2m", [0])[idx] or 0), 1),
            "humidity":    round(float(hourly.get("relativehumidity_2m", [0])[idx] or 0), 1),
            "pressure":    round(float(hourly.get("surface_pressure", [1013])[idx] or 1013), 1),
            "weather_code": code,
            "description": WMO_CODES.get(code, "未知"),
            "wind_speed":  round(float(hourly.get("windspeed_10m", [0])[idx] or 0), 1),
        }
    except Exception as e:
        return {
            "temperature": 0.0, "humidity": 0.0, "pressure": 1013.0,
            "weather_code": -1, "description": f"获取失败:{e}", "wind_speed": 0.0,
        }


def weather_emoji(code: int) -> str:
    if code == 0:   return "☀️"
    if code <= 2:   return "🌤️"
    if code == 3:   return "☁️"
    if code <= 48:  return "🌫️"
    if code <= 65:  return "🌧️"
    if code <= 75:  return "❄️"
    if code <= 82:  return "🌦️"
    return "⛈️"
