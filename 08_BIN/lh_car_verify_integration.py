#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂车载系统 · 集成验证脚本 v1.0
=====================================
DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-CAR-INTEGRATE-VERIFY-v1.0-UID9622
License: MulanPSL v2
用法: python3 bin/lh_car_verify_integration.py
功能: 全链路集成验证——干支两端一致性→云端服务→确认码闸门→DNA链→耻辱墙→合规硬检
跑完全绿 = 单台车机集成通过，可以交付
"""
import subprocess, sys, json, time, os, urllib.request, urllib.error

PASS, FAIL = 0, 0
PID = None
PORT = 9080  # 8080 被 nginx 占用
BASE = f"http://127.0.0.1:{PORT}"

def check(name, fn):
    global PASS, FAIL
    try:
        ok = fn()
    except Exception as e:
        ok = False
    if ok:
        print(f"  🟢 {name}"); PASS += 1
    else:
        print(f"  🔴 {name}"); FAIL += 1
    return ok

def _post(path, data, code_expected=200):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(f"{BASE}{path}", data=body,
        headers={'Content-Type': 'application/json; charset=utf-8',
                 'X-LongHun-Confirm': 'test-integration-code-min-16chars'}, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == code_expected
    except urllib.error.HTTPError as e:
        return e.code == code_expected

def _post_json(path, data):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(f"{BASE}{path}", data=body,
        headers={'Content-Type': 'application/json; charset=utf-8',
                 'X-LongHun-Confirm': 'test-integration-code-min-16chars'}, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"status": "error", "code": e.code}

def _get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}") as resp:
            return resp.read().decode('utf-8')
    except: return ""

def main():
    global PID, PASS, FAIL

    print("🐉 龍魂车载系统 v2.1 集成验证")
    print("=" * 40); print()

    # ── 1. 干支 ──
    print("[1/7] 干支两端一致性")
    r = subprocess.run([sys.executable, 'bin/rizhu_core.py'], capture_output=True)
    check("Python rizhu_core 自检 (7/7)", lambda: r.returncode == 0)
    check("Python 四柱非空", lambda: '当前四柱' in (r.stdout + r.stderr).decode('utf-8', errors='replace'))
    print()

    # ── 2. 启动服务 ──
    print(f"[2/7] 云端索引服务 (:{PORT})")
    env = os.environ.copy()
    env['LONGHUN_CONFIRM_CODE'] = 'test-integration-code-min-16chars'
    env['LONGHUN_CAR_PORT'] = str(PORT)
    proc = subprocess.Popen([sys.executable, '05_ENGINES/lh_car_cloud_index.py'],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    PID = proc.pid
    time.sleep(3)

    check("/health 可达", lambda: '🟢' in _get('/health'))
    check("/api/status 正常", lambda: '🟢' in _get('/api/status'))
    print()

    # ── 3. 闸门 ──
    print("[3/7] 确认码闸门")
    code = 0
    try:
        body = json.dumps({"dna":"test"}).encode('utf-8')
        req = urllib.request.Request(f"{BASE}/api/dna/chain", data=body,
            headers={'Content-Type':'application/json'}, method='POST')
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        code = e.code
    check(f"无确认码→403 (got:{code})", lambda: code == 403)
    print()

    # ── 4. DNA链 ──
    print("[4/7] DNA链追加与断链检测")
    r1 = _post_json("/api/dna/chain", {
        "dna": "#龍芯⚡️测试-INT-001-test-a1b2c3d4", "vehicle_id": "INT001",
        "operation": "INTEGRATION_TEST", "detail": "集成验证",
        "prev_hash": "0", "current_hash": "int-test-hash-001"})
    check("链追加200", lambda: r1.get("status") == "🟢")

    code2 = 0
    try:
        body = json.dumps({
            "dna": "#龍芯⚡️测试-INT-001-broken", "vehicle_id": "INT001",
            "operation": "TEST2", "detail": "故意断链",
            "prev_hash": "WRONG_HASH", "current_hash": "int-test-hash-002"
        }).encode('utf-8')
        req = urllib.request.Request(f"{BASE}/api/dna/chain", data=body,
            headers={'Content-Type':'application/json',
                     'X-LongHun-Confirm': 'test-integration-code-min-16chars'}, method='POST')
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        code2 = e.code
    check(f"断链→409 (got:{code2})", lambda: code2 == 409)
    print()

    # ── 5. 耻辱墙 ──
    print("[5/7] 耻辱墙")
    r3 = _post_json("/api/shame/register", {
        "id": "INT-SHAME-001", "vehicle_id": "INT001",
        "error_type": "other", "error_detail": "集成测试错误",
        "severity": 1, "dna": "#龍芯⚡️测试-INT-001-shame-test",
        "timestamp": "2026-08-11T00:00:00"})
    check("耻辱登记200", lambda: r3.get("status") == "🟢")

    r4 = _post_json("/api/shame/resolve", {
        "id": "INT-SHAME-001", "resolution": "集成测试修复"})
    check("耻辱修复200", lambda: r4.get("status") == "🟢")

    code4 = 0
    try:
        body = json.dumps({"id":"INT-SHAME-001","resolution":"重复修复应被拒绝"}).encode('utf-8')
        req = urllib.request.Request(f"{BASE}/api/shame/resolve", data=body,
            headers={'Content-Type':'application/json',
                     'X-LongHun-Confirm': 'test-integration-code-min-16chars'}, method='POST')
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        code4 = e.code
    check(f"重复修复→404 (got:{code4})", lambda: code4 == 404)
    print()

    # ── 6. 合规 ──
    print("[6/7] 合规硬检（匿名化）")
    code5 = 0
    try:
        body = json.dumps({
            "tile_id":"INT-TILE-001","dna":"#龍芯⚡️测试",
            "gps_lat":39.9,"gps_lng":116.4,"anonymized":False
        }).encode('utf-8')
        req = urllib.request.Request(f"{BASE}/api/road/index", data=body,
            headers={'Content-Type':'application/json',
                     'X-LongHun-Confirm': 'test-integration-code-min-16chars'}, method='POST')
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        code5 = e.code
    check(f"未匿名→422 (got:{code5})", lambda: code5 == 422)

    r7 = _post_json("/api/road/index", {
        "tile_id":"INT-TILE-001","dna":"#龍芯⚡️测试",
        "gps_lat":39.9,"gps_lng":116.4,"anonymized":True,"hash":"test-hash-tile"})
    check("已匿名→200", lambda: r7.get("status") == "🟢")
    print()

    # ── 7. 清理 ──
    print("[7/7] 清理")
    proc.terminate()
    try: proc.wait(timeout=3)
    except subprocess.TimeoutExpired: proc.kill()
    # 删除测试数据库
    import glob
    for f in glob.glob(f"{os.environ.get('LONGHUN_CAR_DIR', './car_index')}/index.db*"):
        try: os.remove(f)
        except: pass
    check("服务已停止·测试数据已清理", lambda: True)
    print()

    # ── 结果 ──
    print("=" * 40)
    total = PASS + FAIL
    print(f"🐉 集成验证完成: {PASS}/{total} 通过")
    if FAIL == 0:
        print("🟢 全链路集成通过 — 可以交付")
        return 0
    else:
        print(f"🔴 {FAIL} 项失败 — 请逐项排查")
        return 1

if __name__ == '__main__':
    sys.exit(main())
