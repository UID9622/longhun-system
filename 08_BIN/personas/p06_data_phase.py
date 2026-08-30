#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·丙子·申时·䷔噬嗑-P06-DATA-PHASE-v1.0-2e1f8c4b
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
P06 数学大师 · 数据相位引擎 v1.0
Data Phase Engine · 玻璃墙实时数据 → 数字根/五行 → 三色相位 → 联动告警

功能:
  1. 拉取玻璃墙公开快照(脱敏聚合) /api/auth/glass
  2. 复用 P06 数字根/五行计算 → 数据相位判定
  3. 三色: 🟢正常 / 🟡关注 / 🔴异常
  4. 🔴/🟡 联动 Bark 告警(去重30min) · 全部写 append-only 相位日志
  5. P0 合规: 只读聚合数字 · 不碰 IP/用户名原文

用法:
  python3 08_BIN/personas/p06_data_phase.py --once            # 单次检测
  python3 08_BIN/personas/p06_data_phase.py --watch 300       # 按需轮询(不常驻·手动触发)
  python3 08_BIN/personas/p06_data_phase.py --once --no-bark  # 测试·不推送
  python3 08_BIN/personas/p06_data_phase.py --url http://127.0.0.1:9658/api/auth/glass

上游: P01 诸葛亮(决策) · P13 姜子牙(调度)
下游: P05 上帝之眼(审计输入) · P72 龍盾(熔断·异常时联动)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PERSONA_CODE = "P06"
PERSONA_NAME = "數學大師"
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 默认数据源: 玻璃墙公开快照(仅脱敏聚合 · P0 无后台)
DEFAULT_URL = "http://127.0.0.1:9658/api/auth/glass"
# 告警去重窗口(分钟) · 对齐 health_check.sh DEDUP_MINUTES=30
DEDUP_MINUTES = 30
# 相位日志(append-only) · 只记聚合不记原文
LOG_PATH = ROOT / "08_STATE" / "p06_data_phase.log"
# 告警去重状态
BARK_STATE = ROOT / "08_STATE" / "p06_data_phase_bark_state.json"
BARK_SEND = ROOT / "executors" / "bark" / "bark_send.py"

# 三色阈值(对齐 P05 三色审计语义 · 阈值出处: P06 数据相位 v1.0)
THRESHOLD_RED = 0.40      # 失败占比 ≥40% → 🔴 撞库/爆破特征
THRESHOLD_YELLOW = 0.15   # 失败占比 ≥15% → 🟡 关注
LOCKED_RED = 3            # locked >3 → 🔴


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_snapshot(url: str) -> dict:
    """拉玻璃墙快照 · 失败不自动重试(节能协议)"""
    req = urllib.request.Request(url, headers={"Cache-Control": "no-store"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data.get("ok"):
        raise RuntimeError(data.get("error") or "snapshot error")
    return data["data"]


def compute_phase(snapshot: dict) -> dict:
    """P06 数据相位判定 · 数字根/五行 + 三色"""
    try:
        from p06_mathmaster import P06Mathmaster
        p06 = P06Mathmaster()
    except Exception:
        p06 = None

    a = (snapshot.get("audit") or {})
    total = int(a.get("total") or 0)
    login_ok = int(a.get("login_ok") or 0)
    login_failed = int(a.get("login_failed") or 0)
    locked = int(a.get("locked") or 0)
    register = int(a.get("register") or 0)
    users_total = int(snapshot.get("users_total") or 0)

    denom = login_ok + login_failed
    fail_rate = round(login_failed / denom, 4) if denom > 0 else 0.0

    # 趋势: 近14天失败是否上升(后5天 vs 前5天日均)
    trend_up = False
    trend = snapshot.get("trend") or []
    if len(trend) >= 10:
        def day_fail(d):
            return int(d.get("login_failed") or 0)
        early = [day_fail(d) for d in trend[:5]]
        late = [day_fail(d) for d in trend[-5:]]
        avg_e = sum(early) / 5
        avg_l = sum(late) / 5
        trend_up = avg_e > 0 and avg_l > avg_e * 1.5

    # 三色判定
    if fail_rate >= THRESHOLD_RED or locked > LOCKED_RED or (locked > 0 and fail_rate >= 0.30):
        color, phase = "🔴", "异常"
    elif fail_rate >= THRESHOLD_YELLOW or locked > 0 or trend_up:
        color, phase = "🟡", "关注"
    else:
        color, phase = "🟢", "正常"

    # 健康指数 0-100(100=最佳)
    health = max(0, min(100, round(100 - fail_rate * 100 * 2.5 - locked * 8)))

    # 数字根/五行: 聚合核心量
    core = f"{total}-{login_failed}-{locked}-{register}"
    dr = wuxing = bagua = None
    if p06:
        try:
            r = p06.compute_dr(core)
            dr, wuxing = r["digital_root"], r["wuxing"]
            b = p06.bagua_analysis(core)
            bagua = {"gua": b.get("gua"), "symbol": b.get("symbol")}
        except Exception:
            pass
    else:
        dr = sum(int(c) for c in core if c.isdigit()) % 9 or 9

    advice = []
    if color == "🔴":
        advice.append("失败占比过高或锁定激增 → 疑似撞库/爆破 · 联动 P72 熔断 + P05 审计")
    if locked > 0:
        advice.append(f"检测到 {locked} 次账号锁定 → 关注爆破行为")
    if trend_up:
        advice.append("近5天登录失败呈上升趋势 → 建议收紧限流")
    if color == "🟢":
        advice.append("数据相位平稳 · 无异常")

    return {
        "snapshot": {"total": total, "login_ok": login_ok, "login_failed": login_failed,
                     "locked": locked, "register": register, "users_total": users_total},
        "computed": {
            "fail_rate": fail_rate, "trend_up": trend_up,
            "health_score": health, "phase": phase, "color": color,
            "digital_root": dr, "wuxing": wuxing, "bagua": bagua,
        },
        "advice": advice,
    }


def get_bark_key() -> str:
    """取 Bark key: 环境变量 → lh_vault(Keychain) · 成功走 stdout(裸值) · 失败走 stderr"""
    key = os.environ.get("BARK_KEY", "").strip()
    if key:
        return key
    try:
        out = subprocess.run(
            [sys.executable, str(ROOT / "bin" / "lh_vault.py"), "get", "BARK_KEY"],
            capture_output=True, text=True, timeout=15)
        raw = out.stdout.strip()
        if raw and "未找到" not in raw and "🔴" not in raw:
            return raw
        return ""
    except Exception:
        return ""


def _bark_state() -> dict:
    st = {}
    if BARK_STATE.exists():
        try:
            st = json.loads(BARK_STATE.read_text(encoding="utf-8"))
        except Exception:
            st = {}
    return st


def check_dedup(level: str) -> bool:
    """30 分钟内同级别告警去重 · 只读判断 · 防刷屏(节能)"""
    now = time.time()
    last = float(_bark_state().get(level, 0))
    return (now - last) >= DEDUP_MINUTES * 60


def mark_bark(level: str) -> None:
    """推送成功后才写去重标记 · 失败不记(可重试)"""
    st = _bark_state()
    st[level] = time.time()
    BARK_STATE.parent.mkdir(parents=True, exist_ok=True)
    BARK_STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def notify(level: str, title: str, body: str) -> dict:
    """联动 Bark 告警 · 异常才大声 · 正常静默 · 成功才去重"""
    if not check_dedup(level):
        return {"pushed": False, "reason": "dedup"}
    key = get_bark_key()
    if not key:
        return {"pushed": False, "reason": "no BARK_KEY"}
    env = dict(os.environ)
    env["BARK_KEY"] = key
    # 剥离代理(socks5h 坑) · urllib 直连 api.day.app · 对齐 memory: 代理坑=清HTTP_PROXY
    for k in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy",
              "ALL_PROXY", "all_proxy"):
        env.pop(k, None)
    try:
        r = subprocess.run(
            [sys.executable, str(BARK_SEND), title, body],
            capture_output=True, text=True, timeout=15, env=env)
        ok = r.returncode == 0
        if ok:
            mark_bark(level)
        return {"pushed": ok, "reason": "ok" if ok else (r.stderr or r.stdout or "send fail")[:120]}
    except Exception as e:
        return {"pushed": False, "reason": str(e)[:120]}


def append_log(phase: dict) -> None:
    """相位日志 append-only · 只记聚合 · 不记 IP/用户名原文"""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": _now_iso(), "phase": phase}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def run(url: str, no_bark: bool) -> dict:
    snap = fetch_snapshot(url)
    result = compute_phase(snap)
    c = result["computed"]
    out = {
        "ok": True,
        "persona": PERSONA_CODE,
        "action": "data_phase",
        "ts": _now_iso(),
        "service": snap.get("service", "web-auth"),
        **result,
    }

    # 异常才大声 · 关注/异常联动 Bark(P72 熔断语义)
    if not no_bark and c["color"] != "🟢":
        title = f"🐉 P06 数据相位 {c['color']} {c['phase']}"
        body = (
            f"总量 {result['snapshot']['total']} · 成功 {result['snapshot']['login_ok']} · "
            f"失败 {result['snapshot']['login_failed']}({c['fail_rate']:.0%}) · "
            f"锁定 {result['snapshot']['locked']} · 注册 {result['snapshot']['register']}\n"
            f"健康 {c['health_score']}/100 · 数字根 {c['digital_root']} 五行 {c['wuxing']}\n"
            f"建议: {' | '.join(result['advice'])}"
        )
        out["bark"] = notify("timeSensitive" if c["color"] == "🔴" else "normal", title, body)
    else:
        out["bark"] = {"pushed": False, "reason": "green or no-bark"}

    append_log(result)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="P06 数据相位引擎")
    ap.add_argument("--once", action="store_true", help="单次检测")
    ap.add_argument("--watch", type=int, metavar="SECONDS", help="轮询间隔(按需·不常驻)")
    ap.add_argument("--url", default=DEFAULT_URL, help="玻璃墙快照地址")
    ap.add_argument("--no-bark", action="store_true", help="禁用 Bark 推送")
    args = ap.parse_args()

    if not args.once and not args.watch:
        ap.error("请指定 --once 或 --watch SECONDS")

    def one():
        try:
            print(json.dumps(run(args.url, args.no_bark), ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"ok": False, "error": str(e)[:200],
                              "hint": "API 不可达? 先启动: python3 bin/lh_web_auth_api.py(端口9658) · 节能: 不自动重试"},
                             ensure_ascii=False))

    if args.once:
        one()
        return 0
    try:
        while True:
            one()
            time.sleep(args.watch)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
