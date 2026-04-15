"""
DNA-Calendar 时空胶囊数据模型
每个日历事件 = 时间锚点 + 多维上下文

Author: 诸葛鑫 (UID9622)
"""

import hashlib
import json
import os
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


DB_PATH = os.path.expanduser("~/.longhun/dna_calendar.db")
GENESIS_HASH = "0" * 64
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ─── 数据模型 ─────────────────────────────────────────────────────

@dataclass
class WeatherContext:
    temperature: float = 0.0       # 摄氏度
    humidity: float = 0.0          # %
    pressure: float = 1013.0       # hPa
    weather_code: int = 0          # WMO天气码
    description: str = "未知"
    wind_speed: float = 0.0        # km/h


@dataclass
class GeoContext:
    latitude: float = 0.0
    longitude: float = 0.0
    address: str = ""
    city: str = ""
    country: str = "中国"


@dataclass
class DNACalendarEvent:
    # ── 基础DNA（必填）
    title: str
    timestamp: float                          # Unix时间戳
    user_id: str = "UID9622"

    # ── 时空上下文（自动采集或手动填）
    geo: Optional[GeoContext] = None
    weather: Optional[WeatherContext] = None
    mood: str = ""                            # 心情标签
    notes: str = ""                           # 备注原文
    tags: list = field(default_factory=list)

    # ── DNA链（自动生成）
    dna_trace: str = ""
    event_hash: str = ""
    prev_hash: str = GENESIS_HASH
    this_hash: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def display_time(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M")

    def display_date(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d")


# ─── DNA 生成 ──────────────────────────────────────────────────────

def generate_event_hash(event: DNACalendarEvent) -> str:
    content = f"{event.title}|{event.timestamp}|{event.user_id}|{event.notes}"
    return hashlib.sha256(content.encode()).hexdigest()


def generate_chain_hash(prev_hash: str, event_hash: str, timestamp: float) -> str:
    data = f"{prev_hash}||{event_hash}||{timestamp}||{GPG_FINGERPRINT}"
    return hashlib.sha256(data.encode()).hexdigest()


def generate_dna_trace(timestamp: float, action_tag: str, chain_hash: str) -> str:
    dt = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    h8 = chain_hash[:8].upper()
    return f"#LONGHUN⚡️{dt}-{action_tag.upper()}-{h8}"


# ─── SQLite 数据库 ────────────────────────────────────────────────

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       TEXT NOT NULL,
            title         TEXT NOT NULL,
            timestamp     REAL NOT NULL,
            display_date  TEXT NOT NULL,
            mood          TEXT DEFAULT '',
            notes         TEXT DEFAULT '',
            tags          TEXT DEFAULT '[]',
            geo_lat       REAL DEFAULT 0.0,
            geo_lng       REAL DEFAULT 0.0,
            geo_city      TEXT DEFAULT '',
            geo_address   TEXT DEFAULT '',
            wx_temp       REAL DEFAULT 0.0,
            wx_humidity   REAL DEFAULT 0.0,
            wx_desc       TEXT DEFAULT '',
            wx_code       INTEGER DEFAULT 0,
            wx_wind       REAL DEFAULT 0.0,
            event_hash    TEXT NOT NULL,
            prev_hash     TEXT NOT NULL,
            this_hash     TEXT NOT NULL,
            dna_trace     TEXT NOT NULL,
            created_at    TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_last_hash(user_id: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT this_hash FROM calendar_events WHERE user_id=? ORDER BY timestamp DESC LIMIT 1",
        (user_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else GENESIS_HASH


def save_event(event: DNACalendarEvent) -> DNACalendarEvent:
    init_db()

    # 计算哈希
    event.event_hash = generate_event_hash(event)
    event.prev_hash  = get_last_hash(event.user_id)
    event.this_hash  = generate_chain_hash(event.prev_hash, event.event_hash, event.timestamp)
    event.dna_trace  = generate_dna_trace(event.timestamp, "CAPSULE", event.this_hash)

    geo = event.geo or GeoContext()
    wx  = event.weather or WeatherContext()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO calendar_events
        (user_id, title, timestamp, display_date, mood, notes, tags,
         geo_lat, geo_lng, geo_city, geo_address,
         wx_temp, wx_humidity, wx_desc, wx_code, wx_wind,
         event_hash, prev_hash, this_hash, dna_trace, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        event.user_id, event.title, event.timestamp, event.display_date(),
        event.mood, event.notes, json.dumps(event.tags, ensure_ascii=False),
        geo.latitude, geo.longitude, geo.city, geo.address,
        wx.temperature, wx.humidity, wx.description, wx.weather_code, wx.wind_speed,
        event.event_hash, event.prev_hash, event.this_hash, event.dna_trace,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()
    return event


def query_events(user_id: str, date: str = None, limit: int = 50) -> list:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if date:
        rows = conn.execute(
            "SELECT * FROM calendar_events WHERE user_id=? AND display_date=? ORDER BY timestamp DESC",
            (user_id, date)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM calendar_events WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()

    conn.close()
    return [dict(r) for r in rows]


def query_event_by_dna(dna_trace: str) -> Optional[dict]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM calendar_events WHERE dna_trace=?", (dna_trace,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def verify_calendar_chain(user_id: str) -> bool:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM calendar_events WHERE user_id=? ORDER BY timestamp ASC", (user_id,)
    ).fetchall()
    conn.close()

    prev = GENESIS_HASH
    for r in rows:
        expected = generate_chain_hash(r["prev_hash"], r["event_hash"], r["timestamp"])
        if expected != r["this_hash"] or r["prev_hash"] != prev:
            return False
        prev = r["this_hash"]
    return True
