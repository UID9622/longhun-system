#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·网站健康检查 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-网站健康-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能：定时检测网站可用性，错误率>5%告警
"""

import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

import requests

# 配置
SITES = [
    {
        "name": "uid9622.cn",
        "url": "https://uid9622.cn",
        "type": "主站"
    },
    {
        "name": "longhun888.com",
        "url": "https://longhun888.com",
        "type": "备用站"
    },
    {
        "name": "CSDN博客",
        "url": "https://blog.csdn.net/UID9622",
        "type": "内容站"
    }
]

ALERT_THRESHOLD = 5  # 错误率>5%触发告警
CHECK_INTERVAL = 300  # 5分钟检查一次（cron模式用）
LOG_DIR = Path.home() / ".longhun/health_check"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def check_site(site):
    """检查单个站点"""
    result = {
        "name": site["name"],
        "url": site["url"],
        "type": site["type"],
        "timestamp": datetime.now().isoformat(),
        "status_code": None,
        "response_time": None,
        "error": None,
        "ok": False
    }
    try:
        start = time.time()
        resp = requests.get(site["url"], timeout=15, allow_redirects=True,
                            headers={"User-Agent": "LongHun-HealthCheck/1.0"})
        result["status_code"] = resp.status_code
        result["response_time"] = round((time.time() - start) * 1000, 1)  # ms
        result["ok"] = 200 <= resp.status_code < 400
    except requests.Timeout:
        result["error"] = "连接超时(>15s)"
    except requests.ConnectionError:
        result["error"] = "连接失败(DNS/网络不通)"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    return result


def check_all():
    """检查所有站点"""
    results = []
    for site in SITES:
        r = check_site(site)
        results.append(r)
    return results


def compute_error_rate():
    """计算整体错误率（基于最近10次检查）"""
    log_file = LOG_DIR / "history.jsonl"
    if not log_file.exists():
        return 0.0

    records = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    records = records[-10:]
    if not records:
        return 0.0

    errors = sum(1 for r in records if not r.get("ok", False))
    return (errors / len(records)) * 100


def alert(site_name, error_rate):
    """触发告警（macOS通知 + 日志）"""
    msg = f"🚨 告警：{site_name} 错误率 {error_rate:.1f}% 超过阈值 {ALERT_THRESHOLD}%"
    print(msg)

    # 写入告警日志
    alert_log = LOG_DIR / "alerts.log"
    with open(alert_log, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} {msg}\n")

    # macOS 系统通知
    try:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{msg}" with title "龍魂健康检查"'
        ], check=False, timeout=3)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="龍魂网站健康检查")
    parser.add_argument("--once", action="store_true", help="只检查一次")
    parser.add_argument("--loop", action="store_true", help=f"循环检查（间隔{CHECK_INTERVAL}s）")
    parser.add_argument("--alert-threshold", type=int, default=ALERT_THRESHOLD,
                        help=f"告警阈值百分比（默认{ALERT_THRESHOLD}）")
    args = parser.parse_args()

    if args.loop:
        print(f"🔄 进入循环检查模式（间隔 {CHECK_INTERVAL}s）· Ctrl+C 退出")
        try:
            while True:
                _run_check(args.alert_threshold)
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n👋 退出循环检查")
            sys.exit(0)
    else:
        _run_check(args.alert_threshold)


def _run_check(threshold):
    """执行一次检查"""
    results = check_all()

    # 记录历史
    with open(LOG_DIR / "history.jsonl", 'a', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 打印结果
    print(f"\n{'='*60}")
    print(f"🐉 龍魂网站健康检查 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"{'='*60}")
    for r in results:
        status = "✅" if r["ok"] else "❌"
        print(f"{status} {r['name']} [{r['type']}]")
        if r["ok"]:
            print(f"   状态码: {r['status_code']}  响应: {r['response_time']}ms")
        else:
            print(f"   错误: {r.get('error', '未知')}")

    # 本次错误率
    error_count = sum(1 for r in results if not r["ok"])
    current_rate = (error_count / len(results)) * 100 if results else 0

    # 历史错误率
    hist_rate = compute_error_rate()

    print(f"{'='*60}")
    print(f"本次错误率: {current_rate:.1f}% | 历史错误率(近10次): {hist_rate:.1f}% | 阈值: {threshold}%")

    if current_rate > threshold or hist_rate > threshold:
        alert("整体", max(current_rate, hist_rate))
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
