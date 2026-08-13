#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂车载实景导航 · 边缘索引服务 v1.1（Kimi审阅修正版 · 零依赖纯标准库）
==============================================================================
DNA: #龍芯⚡️2026-08-11-CAR-EDGE-INDEX-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

v1.0 → v1.1 修正清单（Kimi审查）:
  ① Flask 依赖去除——纯标准库 http.server 实现，任何装 Python3 的机器都能跑
  ② INSERT OR REPLACE 版本自增改为标准 UPSERT（原子操作，不再依赖子查询时序）
  ③ 所有写/查接口加确认码闸门（X-LongHun-Confirm），与网关 :8785 铁律对齐
  ④ 合规硬检：《汽车数据安全管理若干规定》——车外影像必须匿名化
     （人脸/车牌脱敏）后才允许索引，未脱敏直接 🔴 422 拒绝
  ⑤ 经纬度入参校验 + 查询半径上限钳制 + 存储路径环境变量化

来源: Kimi Agent 三色审计页面结构完善 → 龍魂车载导航_边缘索引服务_v1.1.py
审查: Kimi 审核通过 ✅ | 合并人: CodeBuddy AI (2026-08-11)
"""

import json
import os
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse, parse_qs

DB_DIR = os.environ.get('LONGHUN_CAR_DIR', './car_index')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'index.db')

# 确认码闸门（铁律：确认码只进环境变量，不进代码不进文档）
CONFIRM_CODE = os.environ.get('LONGHUN_CONFIRM_CODE', '')
MAX_RADIUS = 0.05  # 查询半径上限，防全库扫描


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS road_tiles (
            tile_id TEXT PRIMARY KEY,
            dna TEXT,
            gps_lat REAL,
            gps_lng REAL,
            road_name TEXT,
            captured_at TEXT,
            source_vehicle TEXT,
            anonymized INTEGER DEFAULT 0,
            version INTEGER DEFAULT 1,
            hash TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehicle_online (
            vehicle_id TEXT PRIMARY KEY,
            gps_lat REAL,
            gps_lng REAL,
            last_seen TEXT
        )
    ''')
    conn.commit()
    conn.close()


def index_tile(data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    """索引一块实景瓦片。返回 (http_status, dict)。"""
    tile_id = data.get('tile_id')
    dna = data.get('dna')
    if not tile_id or not dna:
        return 400, {'status': '🔴', 'error': 'tile_id 与 dna 必填'}

    # 合规硬检：车外影像必须已匿名化（人脸/车牌脱敏）
    if not data.get('anonymized', False):
        return 422, {'status': '🔴',
                     'error': '未匿名化的车外影像禁止索引（汽车数据安全规定：人脸/车牌须脱敏）'}

    lat, lng = data.get('gps_lat'), data.get('gps_lng')
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)) \
            or not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        return 400, {'status': '🔴', 'error': 'GPS坐标非法'}

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO road_tiles
        (tile_id, dna, gps_lat, gps_lng, road_name, captured_at,
         source_vehicle, anonymized, version, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1, ?)
        ON CONFLICT(tile_id) DO UPDATE SET
            dna=excluded.dna, gps_lat=excluded.gps_lat, gps_lng=excluded.gps_lng,
            road_name=excluded.road_name, captured_at=excluded.captured_at,
            source_vehicle=excluded.source_vehicle, hash=excluded.hash,
            version=road_tiles.version+1
    ''', (tile_id, dna, lat, lng, data.get('road_name', '未知路段'),
          datetime.now().isoformat(), data.get('source', 'vehicle'),
          data.get('hash', '')))
    conn.commit()
    c.execute('SELECT version FROM road_tiles WHERE tile_id=?', (tile_id,))
    ver = c.fetchone()[0]
    conn.close()
    return 200, {'status': '🟢', 'tile_id': tile_id, 'dna': dna, 'version': ver}


def query_tiles(lat: float, lng: float, radius: float = 0.02) -> dict[str, Any]:
    radius = min(radius, MAX_RADIUS)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT tile_id, dna, gps_lat, gps_lng, road_name, captured_at, source_vehicle, version
        FROM road_tiles
        WHERE gps_lat BETWEEN ? AND ? AND gps_lng BETWEEN ? AND ?
    ''', (lat - radius, lat + radius, lng - radius, lng + radius))
    rows = c.fetchall()
    conn.close()
    return {'status': '🟢', 'count': len(rows),
            'tiles': [{'tile_id': r[0], 'dna': r[1], 'gps_lat': r[2], 'gps_lng': r[3],
                       'road_name': r[4], 'captured_at': r[5], 'version': r[7]}
                      for r in rows]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict[str, Any]):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _gate(self) -> bool:
        """确认码闸门：未配置时放行本机调试，配置后强制校验"""
        if not CONFIRM_CODE:
            return True
        return self.headers.get('X-LongHun-Confirm') == CONFIRM_CODE

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/health':
            return self._send(200, {'status': '🟢', 'service': 'longhun-car-edge-index', 'version': 'v1.1'})
        if path == '/api/road/query':
            if not self._gate():
                return self._send(403, {'status': '🔴', 'error': '确认码校验失败'})
            qs = parse_qs(urlparse(self.path).query)
            try:
                lat = float(qs.get('lat', ['30.57'])[0])
                lng = float(qs.get('lng', ['104.06'])[0])
                radius = float(qs.get('radius', ['0.02'])[0])
            except ValueError:
                return self._send(400, {'status': '🔴', 'error': '参数格式错误'})
            return self._send(200, query_tiles(lat, lng, radius))
        return self._send(404, {'status': '🔴', 'error': 'not found'})

    def do_POST(self):
        if urlparse(self.path).path != '/api/road/index':
            return self._send(404, {'status': '🔴', 'error': 'not found'})
        if not self._gate():
            return self._send(403, {'status': '🔴', 'error': '确认码校验失败'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length) or b'{}')
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {'status': '🔴', 'error': 'JSON格式错误'})
        code, obj = index_tile(data)
        return self._send(code, obj)

    def log_message(self, *args):
        pass  # 静默；正式部署落 JSONL 审计日志


def main(port: int = 8080):
    init_db()
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'🐉 龍魂车载边缘索引服务 v1.1 已启动 :{port}（确认码闸门: {"开" if CONFIRM_CODE else "关·调试模式"}）')
    server.serve_forever()


if __name__ == '__main__':
    main()
