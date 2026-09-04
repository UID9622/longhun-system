#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 K线 系统测试 v1.0
DNA: #龍芯⚡️2026-08-31-KLINE-TEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2
功能: 采集器真实数据 + 服务API 冒烟测试（P05 审计）
运行: python3 13_TESTS/test_kline.py
"""
import re
import sys
import time
import urllib.request
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08_BIN"))
from lh_kline_fetcher import fetcher, DEFAULT_SYMBOLS

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}  {detail}")


def test_fetcher_real_data():
    print("◆ 采集器·真实数据")
    # A股 新浪
    d = fetcher.fetch("sh600036")
    check("A股-招商银行 新浪真实日K", d and len(d.get("data", [])) > 20,
          f"source={d and d.get('source')} n={d and len(d.get('data', []))}")
    if d and d["data"]:
        last = d["data"][-1]
        check("A股-最新K线 OHLC 有效", all(x > 0 for x in [last["open"], last["close"], last["high"], last["low"]]),
              str(last))
    # 加密 币安
    d = fetcher.fetch("BTCUSDT")
    check("加密-BTCUSDT 币安真实K线", d and len(d.get("data", [])) > 20,
          f"source={d and d.get('source')}")
    # 数据完整性
    ok = all(k in ("date", "open", "high", "low", "close", "volume") for k in last.keys())
    check("K线字段完整(date/open/high/low/close/volume)", ok)
    # 缓存生效
    t0 = time.time()
    fetcher.fetch("sh600036")
    check("缓存生效(<0.3s 返回)", time.time() - t0 < 0.3)
    # 未知标的降级
    d = fetcher.fetch("ZZZZZZ")
    check("未知标的安全降级(不崩溃)", d is None or isinstance(d, dict))


def test_server_api(port=8897):
    print(f"◆ 服务 API (127.0.0.1:{port})")
    base = f"http://127.0.0.1:{port}"
    try:
        with urllib.request.urlopen(f"{base}/api/kline/health", timeout=5) as r:
            j = json.load(r)
        check("health 健康检查", j.get("status") == "healthy")
    except Exception as e:
        check("health 健康检查", False, str(e))

    try:
        with urllib.request.urlopen(f"{base}/api/kline/symbols", timeout=5) as r:
            j = json.load(r)
        check("symbols 列表", len(j.get("symbols", [])) >= 6)
    except Exception as e:
        check("symbols 列表", False, str(e))

    try:
        with urllib.request.urlopen(f"{base}/api/kline/data/sh600036?days=5", timeout=10) as r:
            j = json.load(r)
        check("data 真实行情", j.get("count", 0) >= 3 and len(j.get("data", [])) >= 3,
              f"count={j.get('count')}")
    except Exception as e:
        check("data 真实行情", False, str(e))

    try:
        with urllib.request.urlopen(f"{base}/kline.html", timeout=5) as r:
            html = r.read().decode("utf-8")
        check("kline.html 页面托管", "龍魂 K线" in html and "echarts" in html)
    except Exception as e:
        check("kline.html 页面托管", False, str(e))


def test_security():
    print("◆ 安全审计")
    src = Path(__file__).resolve().parent.parent / "08_BIN"
    bad = []
    for f in ["lh_kline_fetcher.py", "lh_kline_server.py"]:
        text = (src / f).read_text(encoding="utf-8")
        # 真实密钥特征（占位 Key / sk-开头的长 token / AKIA 云密钥）
        if "YOUR_API_KEY" in text or re.search(r"sk-[A-Za-z0-9]{16,}", text) \
                or "AKIA[0-9A-Z]{16}" in text:
            bad.append(f)
    check("无硬编码密钥/占位Key", not bad, str(bad))
    # 绑定 localhost 检查
    server = (src / "lh_kline_server.py").read_text(encoding="utf-8")
    check("服务绑定 127.0.0.1(不裸奔公网)", 'HOST = "127.0.0.1"' in server)


if __name__ == "__main__":
    print("🐉 龍魂 K线 系统测试 v1.0")
    test_fetcher_real_data()
    test_server_api()
    test_security()
    print(f"\n结果: {PASS} 通过 / {FAIL} 失败 / {PASS + FAIL} 总")
    sys.exit(1 if FAIL else 0)
