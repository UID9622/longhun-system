#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂车载系统 · 云端索引服务 v2.1（Kimi审阅修正版 · 零依赖纯标准库）
DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷑蛊-CAR-INDEX-v2.1-UID9622（生成器回填，禁止手写干支）

合并：v2.0 完整表结构（vehicles/navigation_records/dna_chain/wall_of_shame/road_tiles）
修正 v2.0 → v2.1：
  ① Flask/flask-cors 依赖去除——纯标准库 http.server，任何Python3机器可跑
  ② 全部写接口+敏感操作加确认码闸门（X-LongHun-Confirm，只进环境变量）
  ③ 耻辱墙 resolve 必须确认码+登记修复说明——不可删除原则有了牙齿
  ④ 实景瓦片匿名化硬检回归（汽车数据安全规定：人脸/车牌须脱敏，未脱敏🔴422）
  ⑤ 存储路径环境变量化 LONGHUN_CAR_DIR，GPS合法性校验，DNA格式校验
  ⑥ /api/dna/chain 追加时校验 prev_hash 链序，断链🔴拒绝
"""
import json
import os
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DB_DIR = os.environ.get('LONGHUN_CAR_DIR', './car_index')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'index.db')
CONFIRM_CODE = os.environ.get('LONGHUN_CONFIRM_CODE', '')
MAX_RADIUS = 0.05

SCHEMA = '''
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id TEXT PRIMARY KEY, model TEXT, platform TEXT,
    first_seen TEXT, last_seen TEXT, dna TEXT);
CREATE TABLE IF NOT EXISTS navigation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT, vehicle_id TEXT,
    start_lat REAL, start_lng REAL, end_lat REAL, end_lng REAL,
    route_hash TEXT, sancai_decision TEXT, hexagram TEXT, dna TEXT,
    timestamp TEXT, hash_chain TEXT);
CREATE TABLE IF NOT EXISTS dna_chain (
    id INTEGER PRIMARY KEY AUTOINCREMENT, dna TEXT, vehicle_id TEXT,
    operation TEXT, detail TEXT, prev_hash TEXT, current_hash TEXT, timestamp TEXT);
CREATE TABLE IF NOT EXISTS wall_of_shame (
    id TEXT PRIMARY KEY, vehicle_id TEXT, error_type TEXT, error_detail TEXT,
    severity INTEGER, status TEXT, dna TEXT, timestamp TEXT,
    resolution TEXT, resolved_at TEXT);
CREATE TABLE IF NOT EXISTS road_tiles (
    tile_id TEXT PRIMARY KEY, dna TEXT, gps_lat REAL, gps_lng REAL,
    road_name TEXT, captured_at TEXT, source_vehicle TEXT,
    anonymized INTEGER DEFAULT 0, version INTEGER DEFAULT 1, hash TEXT);
'''


def db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def valid_dna(dna):
    return isinstance(dna, str) and dna.startswith('#龍芯⚡️')


def valid_gps(lat, lng):
    return isinstance(lat, (int, float)) and isinstance(lng, (int, float)) \
        and -90 <= lat <= 90 and -180 <= lng <= 180


# ---------- 业务函数（可独立单测） ----------

def register_vehicle(data):
    vid = data.get('vehicle_id')
    if not vid:
        return 400, {'status': '🔴', 'error': 'vehicle_id 必填'}
    now = datetime.now().isoformat()
    conn = db()
    conn.execute('''
        INSERT INTO vehicles (vehicle_id, model, platform, first_seen, last_seen, dna)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(vehicle_id) DO UPDATE SET last_seen=excluded.last_seen,
            model=excluded.model, platform=excluded.platform, dna=excluded.dna
    ''', (vid, data.get('model', ''), data.get('platform', ''), now, now, data.get('dna', '')))
    conn.commit(); conn.close()
    return 200, {'status': '🟢', 'vehicle_id': vid}


def record_navigation(data):
    if not valid_gps(data.get('start_lat'), data.get('start_lng')):
        return 400, {'status': '🔴', 'error': 'GPS坐标非法'}
    conn = db()
    conn.execute('''
        INSERT INTO navigation_records
        (vehicle_id, start_lat, start_lng, end_lat, end_lng, route_hash,
         sancai_decision, hexagram, dna, timestamp, hash_chain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data.get('vehicle_id'), data.get('start_lat'), data.get('start_lng'),
          data.get('end_lat'), data.get('end_lng'), data.get('route_hash'),
          data.get('sancai_decision'), data.get('hexagram'), data.get('dna'),
          datetime.now().isoformat(), data.get('hash_chain')))
    conn.commit(); conn.close()
    return 200, {'status': '🟢'}


def append_dna_chain(data):
    dna, cur = data.get('dna'), data.get('current_hash')
    if not valid_dna(dna):
        return 400, {'status': '🔴', 'error': 'DNA格式非法（须以 #龍芯⚡️ 开头）'}
    if not cur:
        return 400, {'status': '🔴', 'error': 'current_hash 必填'}
    conn = db()
    c = conn.cursor()
    c.execute('SELECT current_hash FROM dna_chain ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    prev_expected = row[0] if row else '0'
    prev_given = data.get('prev_hash', '0')
    if prev_given != prev_expected:
        conn.close()
        return 409, {'status': '🔴', 'error': '链序断裂：prev_hash 与链尾不一致',
                     'expected': prev_expected}
    c.execute('''
        INSERT INTO dna_chain (dna, vehicle_id, operation, detail, prev_hash, current_hash, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (dna, data.get('vehicle_id'), data.get('operation'), data.get('detail'),
          prev_given, cur, datetime.now().isoformat()))
    conn.commit(); conn.close()
    return 200, {'status': '🟢', 'prev_hash': prev_given}


def register_shame(data):
    sid = data.get('id')
    if not sid or not data.get('error_detail'):
        return 400, {'status': '🔴', 'error': 'id 与 error_detail 必填'}
    sev = data.get('severity', 3)
    if not isinstance(sev, int) or not 1 <= sev <= 5:
        return 400, {'status': '🔴', 'error': 'severity 须为 1-5'}
    conn = db()
    conn.execute('''
        INSERT INTO wall_of_shame (id, vehicle_id, error_type, error_detail,
            severity, status, dna, timestamp)
        VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
    ''', (sid, data.get('vehicle_id'), data.get('error_type', 'other'),
          data.get('error_detail'), sev, data.get('dna'), datetime.now().isoformat()))
    conn.commit(); conn.close()
    return 200, {'status': '🟢', 'id': sid}


def resolve_shame(data):
    """耻辱墙不可删除，只能登记修复——且必须确认码（路由层已验）+修复说明"""
    sid, resolution = data.get('id'), data.get('resolution')
    if not sid or not resolution:
        return 400, {'status': '🔴', 'error': 'id 与 resolution 必填'}
    conn = db()
    cur = conn.execute('''
        UPDATE wall_of_shame SET status='resolved', resolution=?, resolved_at=?
        WHERE id=? AND status != 'resolved'
    ''', (resolution, datetime.now().isoformat(), sid))
    n = cur.rowcount
    conn.commit(); conn.close()
    if n == 0:
        return 404, {'status': '🟡', 'error': '记录不存在或已修复'}
    return 200, {'status': '🟢', 'id': sid, 'resolution': resolution}


def index_road_tile(data):
    tile_id, dna = data.get('tile_id'), data.get('dna')
    if not tile_id or not dna:
        return 400, {'status': '🔴', 'error': 'tile_id 与 dna 必填'}
    # 合规硬检：车外影像必须已匿名化（人脸/车牌脱敏）
    if not data.get('anonymized', False):
        return 422, {'status': '🔴',
                     'error': '未匿名化的车外影像禁止索引（汽车数据安全规定）'}
    if not valid_gps(data.get('gps_lat'), data.get('gps_lng')):
        return 400, {'status': '🔴', 'error': 'GPS坐标非法'}
    conn = db()
    conn.execute('''
        INSERT INTO road_tiles
        (tile_id, dna, gps_lat, gps_lng, road_name, captured_at,
         source_vehicle, anonymized, version, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1, ?)
        ON CONFLICT(tile_id) DO UPDATE SET
            dna=excluded.dna, gps_lat=excluded.gps_lat, gps_lng=excluded.gps_lng,
            road_name=excluded.road_name, captured_at=excluded.captured_at,
            source_vehicle=excluded.source_vehicle, hash=excluded.hash,
            version=road_tiles.version+1
    ''', (tile_id, dna, data['gps_lat'], data['gps_lng'],
          data.get('road_name', '未知路段'), datetime.now().isoformat(),
          data.get('source', 'vehicle'), data.get('hash', '')))
    conn.commit()
    ver = conn.execute('SELECT version FROM road_tiles WHERE tile_id=?', (tile_id,)).fetchone()[0]
    conn.close()
    return 200, {'status': '🟢', 'tile_id': tile_id, 'version': ver}


def query_tiles(lat, lng, radius=0.02):
    radius = min(radius, MAX_RADIUS)
    conn = db()
    rows = conn.execute('''
        SELECT tile_id, dna, gps_lat, gps_lng, road_name, captured_at, version
        FROM road_tiles
        WHERE gps_lat BETWEEN ? AND ? AND gps_lng BETWEEN ? AND ?
    ''', (lat - radius, lat + radius, lng - radius, lng + radius)).fetchall()
    conn.close()
    return {'status': '🟢', 'count': len(rows),
            'tiles': [{'tile_id': r[0], 'dna': r[1], 'gps_lat': r[2], 'gps_lng': r[3],
                       'road_name': r[4], 'captured_at': r[5], 'version': r[6]} for r in rows]}


def status():
    conn = db()
    counts = {t: conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
              for t in ('vehicles', 'navigation_records', 'dna_chain',
                        'wall_of_shame', 'road_tiles')}
    conn.close()
    return {'status': '🟢', 'version': 'v2.1', **counts,
            'timestamp': datetime.now().isoformat()}


# ---------- HTTP 层 ----------

POST_ROUTES = {
    '/api/vehicle/register': register_vehicle,
    '/api/nav/record': record_navigation,
    '/api/dna/chain': append_dna_chain,
    '/api/shame/register': register_shame,
    '/api/shame/resolve': resolve_shame,
    '/api/road/index': index_road_tile,
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _gate(self):
        if not CONFIRM_CODE:
            return True
        return self.headers.get('X-LongHun-Confirm') == CONFIRM_CODE

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ('/health', '/api/status'):
            return self._send(200, {'service': 'longhun-car-index', **status()} if path == '/api/status'
                            else {'status': '🟢', 'version': 'v2.1'})
        if path == '/api/road/query':
            if not self._gate():
                return self._send(403, {'status': '🔴', 'error': '确认码校验失败'})
            qs = parse_qs(urlparse(self.path).query)
            try:
                return self._send(200, query_tiles(
                    float(qs.get('lat', ['30.57'])[0]),
                    float(qs.get('lng', ['104.06'])[0]),
                    float(qs.get('radius', ['0.02'])[0])))
            except ValueError:
                return self._send(400, {'status': '🔴', 'error': '参数格式错误'})
        return self._send(404, {'status': '🔴', 'error': 'not found'})

    def do_POST(self):
        fn = POST_ROUTES.get(urlparse(self.path).path)
        if not fn:
            return self._send(404, {'status': '🔴', 'error': 'not found'})
        if not self._gate():
            return self._send(403, {'status': '🔴', 'error': '确认码校验失败'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length) or b'{}')
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {'status': '🔴', 'error': 'JSON格式错误'})
        code, obj = fn(data)
        return self._send(code, obj)

    def log_message(self, *args):
        pass


def main(port=8080):
    init_db()
    print(f'🐉 龍魂车载索引服务 v2.1 已启动 :{port}（确认码闸门: {"开" if CONFIRM_CODE else "关·调试模式"}）')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()


if __name__ == '__main__':
    main()
