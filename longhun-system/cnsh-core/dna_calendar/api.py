"""
DNA-Calendar API 路由
挂载到 CNSH-64 FastAPI 服务 (port 9622)

Author: 诸葛鑫 (UID9622)
"""

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .models import (
    DNACalendarEvent, GeoContext, WeatherContext,
    save_event, query_events, verify_calendar_chain
)
from .reflow import reflow_by_dna, reflow_by_date
from .context.weather import fetch_weather, weather_emoji

router = APIRouter(prefix="/calendar", tags=["DNA-Calendar"])


# ─── 请求模型 ────────────────────────────────────────────────────

class CreateEventRequest(BaseModel):
    title:     str
    timestamp: Optional[float] = None    # 默认当前时间
    user_id:   str = "UID9622"
    mood:      str = ""
    notes:     str = ""
    tags:      List[str] = []
    lat:       float = 0.0
    lng:       float = 0.0
    city:      str = ""
    address:   str = ""
    fetch_weather: bool = True           # 自动抓取天气


# ─── 路由 ────────────────────────────────────────────────────────

@router.post("/event")
def create_calendar_event(req: CreateEventRequest):
    """创建日历事件（时空胶囊）"""
    ts = req.timestamp or datetime.utcnow().timestamp()

    geo = GeoContext(
        latitude=req.lat, longitude=req.lng,
        city=req.city, address=req.address
    )

    wx = WeatherContext()
    if req.fetch_weather and req.lat != 0.0 and req.lng != 0.0:
        data = fetch_weather(req.lat, req.lng, ts)
        wx = WeatherContext(
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"],
            weather_code=data["weather_code"],
            description=data["description"],
            wind_speed=data["wind_speed"],
        )

    event = DNACalendarEvent(
        title=req.title,
        timestamp=ts,
        user_id=req.user_id,
        geo=geo,
        weather=wx,
        mood=req.mood,
        notes=req.notes,
        tags=req.tags,
    )

    saved = save_event(event)
    return {
        "dna_trace":   saved.dna_trace,
        "display_time": saved.display_time(),
        "weather":     f"{weather_emoji(wx.weather_code)} {wx.description} {wx.temperature}°C",
        "location":    f"{geo.city or '未记录'} ({geo.latitude:.4f}, {geo.longitude:.4f})",
        "chain":       saved.this_hash[:16] + "...",
    }


@router.get("/events/{user_id}")
def get_events(user_id: str, date: Optional[str] = None, limit: int = 30):
    """查询事件列表"""
    events = query_events(user_id=user_id, date=date, limit=limit)
    return {"user_id": user_id, "count": len(events), "events": events}


@router.get("/reflow/dna/{dna_trace:path}")
def reflow_dna(dna_trace: str):
    """时光回流 - 通过DNA还原场景"""
    scene = reflow_by_dna(dna_trace)
    if "error" in scene:
        raise HTTPException(status_code=404, detail=scene["error"])
    return scene


@router.get("/reflow/date/{user_id}/{date}")
def reflow_date(user_id: str, date: str):
    """时光回流 - 还原某天所有事件"""
    scenes = reflow_by_date(user_id=user_id, date=date)
    return {"date": date, "count": len(scenes), "scenes": scenes}


@router.get("/verify/{user_id}")
def verify_chain(user_id: str):
    """验证日历DNA链完整性"""
    ok = verify_calendar_chain(user_id)
    return {
        "user_id":   user_id,
        "integrity": "🟢 完好" if ok else "🔴 已篡改",
        "verified":  ok,
    }


@router.get("/weather/preview")
def preview_weather(lat: float, lng: float, timestamp: float = None):
    """预览某坐标某时刻的天气（测试用）"""
    ts = timestamp or datetime.utcnow().timestamp()
    data = fetch_weather(lat, lng, ts)
    data["emoji"] = weather_emoji(data["weather_code"])
    return data
