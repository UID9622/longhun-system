#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三方追踪 cookie / Service Worker 清扫 · 任务 B · 本机 only"""
from __future__ import annotations

import glob
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

TRACK_DOMAINS = (
    "doubleclick.net",
    "google-analytics.com",
    "facebook.com",
    "yandex.ru",
    "criteo.com",
    "umeng.com",
    "umeng.co",
    "jiguang.cn",
    "sensorsdata.cn",
    "talkingdata.com",
    "hm.baidu.com",
    "mmstat.com",
    "tenpay.com",
    "wx.qq.com",
)

HOME = Path.home()
REPO = Path(__file__).resolve().parents[1]
LOG = REPO / "日志" / f"清扫追踪_{datetime.now():%Y%m%d}.txt"


def _chrome_profiles() -> list[Path]:
    base = HOME / "Library/Application Support/Google/Chrome"
    if not base.is_dir():
        return []
    out = []
    for name in ("Default",) + tuple(
        p.name for p in base.glob("Profile *") if p.is_dir()
    ):
        cookies = base / name / "Cookies"
        if cookies.is_file():
            out.append(cookies)
    return out


def _clear_chrome_cookies(db: Path) -> int:
    if not db.is_file():
        return 0
    n = 0
    try:
        conn = sqlite3.connect(f"file:{db}?mode=rw", uri=True, timeout=5)
        cur = conn.cursor()
        for dom in TRACK_DOMAINS:
            cur.execute(
                "DELETE FROM cookies WHERE host_key LIKE ? OR host_key LIKE ?",
                (f"%{dom}", f"%.{dom}"),
            )
            n += cur.rowcount
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"⚠️ Chrome Cookies 锁定(请先完全退出 Chrome): {db}\n  {e}\n")
        return -1
    return n


def _clear_service_workers() -> int:
    base = HOME / "Library/Application Support/Google/Chrome"
    removed = 0
    for sw in base.glob("**/Service Worker"):
        if sw.is_dir():
            try:
                shutil.rmtree(sw)
                removed += 1
            except OSError:
                pass
    return removed


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"=== 清扫追踪 {datetime.now().isoformat()} ===",
        f"目标域: {', '.join(TRACK_DOMAINS[:5])}… 共 {len(TRACK_DOMAINS)} 个",
    ]
    total = 0
    locked = False
    for db in _chrome_profiles():
        c = _clear_chrome_cookies(db)
        if c < 0:
            locked = True
        else:
            total += c
            lines.append(f"Chrome {db.parent.name}: 删除 cookie 行 {c}")
    sw = _clear_service_workers()
    lines.append(f"Service Worker 目录清除: {sw} 处")
    lines.append(f"合计删除 cookie 行: {total}")
    if locked:
        lines.append("🟡 部分未清: 请退出 Chrome 后重跑 清扫追踪.command")
    else:
        lines.append("🟢 Chrome 追踪域 cookie 已扫·请在 F12→Application 复核")
    text = "\n".join(lines)
    LOG.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\n留痕: {LOG}")


if __name__ == "__main__":
    main()
