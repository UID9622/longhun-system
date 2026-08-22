#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 云端索引服务
车载DNA索引后台 · Flask REST API
License: MulanPSL v2
DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷃蒙-CAR-INDEX-SERVER-v2.0-UID9622
"""
import sqlite3
import json
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('longhun_car.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        id TEXT PRIMARY KEY, model TEXT, vin TEXT, brand TEXT,
        platform TEXT, dna TEXT, registered_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS navigation_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT, vehicle_id TEXT,
        sancai_decision TEXT, hexagram TEXT, dna TEXT,
        created_at TEXT, FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS dna_chain (
        id INTEGER PRIMARY KEY AUTOINCREMENT, vehicle_id TEXT,
        dna TEXT, operation TEXT, detail TEXT, hash TEXT,
        prev_hash TEXT, created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS wall_of_shame (
        id TEXT PRIMARY KEY, vehicle_id TEXT, error_type TEXT,
        error_detail TEXT, severity INTEGER, dna TEXT,
        status TEXT DEFAULT 'pending', resolution TEXT,
        resolved_at TEXT, created_at TEXT
    )''')
    conn.commit()
    conn.close()


@app.route('/api/vehicle/register', methods=['POST'])
def register_vehicle():
    """车辆注册"""
    data = request.json
    conn = sqlite3.connect('longhun_car.db')
    try:
        conn.execute(
            'INSERT OR REPLACE INTO vehicles VALUES (?,?,?,?,?,?,?)',
            (data['id'], data['model'], data['vin'], data['brand'],
             data.get('platform', 'unknown'), data.get('dna', ''),
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return jsonify({'status': 'ok', 'dna': data.get('dna', '')})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()


@app.route('/api/nav/record', methods=['POST'])
def record_navigation():
    """导航记录"""
    data = request.json
    conn = sqlite3.connect('longhun_car.db')
    try:
        c = conn.cursor()
        c.execute(
            'INSERT INTO navigation_records (vehicle_id, sancai_decision, hexagram, dna, created_at) VALUES (?,?,?,?,?)',
            (data['vehicle_id'], data.get('sancai_decision', 'proceed'),
             data.get('hexagram', '乾卦'), data.get('dna', ''),
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return jsonify({'status': 'ok', 'record_id': c.lastrowid})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()


@app.route('/api/dna/chain', methods=['POST'])
def dna_chain():
    """DNA上链"""
    data = request.json
    conn = sqlite3.connect('longhun_car.db')
    try:
        c = conn.cursor()
        prev = c.execute(
            'SELECT hash FROM dna_chain ORDER BY id DESC LIMIT 1'
        ).fetchone()
        prev_hash = prev[0] if prev else '0'
        content = f"{data.get('vehicle_id')}{data.get('operation')}{data.get('dna')}{prev_hash}{time.time()}"
        import hashlib
        hash_val = hashlib.sha256(content.encode()).hexdigest()[:16]
        c.execute(
            'INSERT INTO dna_chain (vehicle_id, dna, operation, detail, hash, prev_hash, created_at) VALUES (?,?,?,?,?,?,?)',
            (data['vehicle_id'], data['dna'], data.get('operation', 'unknown'),
             data.get('detail', ''), hash_val, prev_hash,
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return jsonify({'status': 'ok', 'tx_hash': hash_val})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()


@app.route('/api/shame/register', methods=['POST'])
def register_shame():
    """耻辱墙登记"""
    data = request.json
    conn = sqlite3.connect('longhun_car.db')
    try:
        conn.execute(
            'INSERT INTO wall_of_shame (id, vehicle_id, error_type, error_detail, severity, dna, created_at) VALUES (?,?,?,?,?,?,?)',
            (data['id'], data['vehicle_id'], data['error_type'],
             data['error_detail'], data.get('severity', 3), data.get('dna', ''),
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()


@app.route('/api/shame/resolve', methods=['POST'])
def resolve_shame():
    """耻辱墙修复"""
    data = request.json
    conn = sqlite3.connect('longhun_car.db')
    try:
        conn.execute(
            'UPDATE wall_of_shame SET status = "resolved", resolution = ?, resolved_at = ? WHERE id = ?',
            (data.get('resolution', ''), datetime.now(timezone.utc).isoformat(), data['id'])
        )
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()


@app.route('/api/status', methods=['GET'])
def status():
    """系统状态"""
    conn = sqlite3.connect('longhun_car.db')
    c = conn.cursor()
    vehicles = c.execute('SELECT COUNT(*) FROM vehicles').fetchone()[0]
    nav_records = c.execute('SELECT COUNT(*) FROM navigation_records').fetchone()[0]
    dna_records = c.execute('SELECT COUNT(*) FROM dna_chain').fetchone()[0]
    shame_records = c.execute('SELECT COUNT(*) FROM wall_of_shame').fetchone()[0]
    pending_shame = c.execute(
        'SELECT COUNT(*) FROM wall_of_shame WHERE status="pending"'
    ).fetchone()[0]
    conn.close()
    return jsonify({
        'status': 'running',
        'vehicles': vehicles,
        'navigation_records': nav_records,
        'dna_chain_records': dna_records,
        'shame_wall_records': shame_records,
        'pending_shame': pending_shame
    })


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8880, debug=True)
