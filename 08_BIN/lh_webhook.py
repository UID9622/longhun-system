#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-WEBHOOK-OUTLET-v1.0-9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂·Webhook 出口引擎 v1.0 — 耻辱墙新增 / 健康检查异常 → 推送外部回调

事件:
  shamewall  耻辱墙新增记录（lh_judge 入库钩子）
  health     健康检查失败（lh_health 钩子）
  ping       register/test 探测

命令:
  python3 08_BIN/lh_webhook.py register <url> [--event shamewall|health|ping|all]
  python3 08_BIN/lh_webhook.py list
  python3 08_BIN/lh_webhook.py remove <url>
  python3 08_BIN/lh_webhook.py test <url>
  python3 08_BIN/lh_webhook.py fire --event shamewall --summary "..."
  python3 08_BIN/lh_webhook.py drop           # 清空全部回调（默认只读，需显式）

数据: ~/.longhun/webhooks.json（白名单回调地址 · append 式登记 · last_status 追踪）
请求体: {"event","event_cn","timestamp","summary","source","signature"}
  signature: 可选项（预留 GPG 分离签名 · 现为 HMAC 摘要位留空 · 详见集成指南）

零依赖（标准库 urllib）。触发失败绝不影响主流程（judge/health 调用侧 try/except）。
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

WEBHOOKS_FILE = Path.home() / ".longhun" / "webhooks.json"
EVENT_CN = {"shamewall": "耻辱墙新增", "health": "健康检查异常", "ping": "连通性探测"}
DEFAULT_EVENTS = ("shamewall", "health")   # register 默认订阅两类


def load_webhooks() -> dict:
    try:
        if WEBHOOKS_FILE.exists():
            return json.loads(WEBHOOKS_FILE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        pass
    return {"webhooks": []}


def save_webhooks(data: dict) -> None:
    WEBHOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    WEBHOOKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")


def _deliver(url: str, event: str, summary: str) -> dict:
    """推送单条 → 返回 {ok, code, reason}。失败抛/返回均可由调用方消化。"""
    payload = {
        "event": event,
        "event_cn": EVENT_CN.get(event, event),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "summary": (summary or "")[:500],
        "source": "longhun-uid9622",
        "signature": "",          # 预留 GPG 分离签名（可选）
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "LongHun-Webhook/1.0 (UID9622)"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            return {"ok": True, "code": resp.status, "reason": ""}
    except urllib.error.HTTPError as e:
        return {"ok": False, "code": e.code, "reason": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "code": 0, "reason": str(e)[:120]}


def fire_event(event: str, summary: str) -> dict:
    """触发某事件的全部注册回调（judge/health 钩子调用入口 · 内部容错）。

    返回 {"event", "fired": int, "failed": [(url, reason)], "ts": ...}
    """
    data = load_webhooks()
    hooks = [h for h in data["webhooks"]
             if event in h.get("events", []) or "all" in h.get("events", [])]
    fired, failed = 0, []
    ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    for h in hooks:
        url = h["url"]
        r = _deliver(url, event, summary)
        h["last_status"] = {"ok": r["ok"], "code": r["code"], "at": ts,
                            "reason": r["reason"]}
        if r["ok"]:
            fired += 1
        else:
            failed.append([url, r["reason"]])
    if hooks:
        save_webhooks(data)   # 仅在有回调时落盘状态（节能·不空写）
    return {"event": event, "fired": fired, "failed": failed, "ts": ts}


def cmd_register(url: str, events: list) -> None:
    if not (url.startswith("http://") or url.startswith("https://")):
        print("🔴 URL 必须是 http(s):// 开头"); sys.exit(1)
    data = load_webhooks()
    for h in data["webhooks"]:
        if h["url"] == url:   # 已注册 → 合并订阅事件
            for e in events:
                if e not in h["events"]:
                    h["events"].append(e)
            save_webhooks(data)
            print(f"🟢 已更新订阅 {url} · 事件 {h['events']}")
            return
    data["webhooks"].append({
        "url": url,
        "events": events,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "last_status": None,
    })
    save_webhooks(data)
    print(f"🟢 已注册 {url} · 订阅 {events} · 登记 {WEBHOOKS_FILE}")


def cmd_list() -> None:
    data = load_webhooks()
    hooks = data["webhooks"]
    if not hooks:
        print("📭 无注册回调（lh webhook register <url> --event shamewall|health）")
        return
    print(f"🌐 已注册回调 {len(hooks)} 条")
    for i, h in enumerate(hooks, 1):
        st = h.get("last_status")
        mark = "🟢" if st and st.get("ok") else ("🟡" if st else "⚪")
        print(f"  {i}. {mark} {h['url']} · 事件 {h['events']}"
              f"{' · 上次 ' + str(st.get('code')) + ' @' + str(st.get('at')) if st else ''}")


def cmd_remove(url: str) -> None:
    data = load_webhooks()
    before = len(data["webhooks"])
    data["webhooks"] = [h for h in data["webhooks"] if h["url"] != url]
    save_webhooks(data)
    print(f"{'🟢 已移除 ' + url if len(data['webhooks']) < before else '⚪ 未找到 ' + url}")


def cmd_test(url: str) -> None:
    """测试回调可达（发 ping 事件）。"""
    cmd_register(url, ["ping"])
    print("  → 发送 ping …")
    r = _deliver(url, "ping", "龍魂 Webhook 连通性测试 · UID9622")
    print(f"  {'🟢' if r['ok'] else '🔴'} {url} → HTTP {r['code']} {r['reason']}"
          .rstrip())
    sys.exit(0 if r["ok"] else 1)


def main() -> None:
    ap = argparse.ArgumentParser(description="🐉 龍魂·Webhook 出口引擎 v1.0")
    ap.add_argument("cmd", nargs="?", choices=("register", "list", "remove", "test", "fire", "drop"))
    ap.add_argument("url", nargs="?", help="回调 URL")
    ap.add_argument("--event", action="append", help="事件: shamewall|health|ping|all (可多次)")
    ap.add_argument("--summary", default="", help="fire 手动事件摘要")
    args = ap.parse_args()

    if not args.cmd:
        cmd_list()
        return
    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "register":
        if not args.url:
            print("🔴 需要 URL: lh webhook register <url> --event shamewall"); sys.exit(1)
        events = args.event or list(DEFAULT_EVENTS)
        events = [e if e != "all" else "all" for e in events]
        cmd_register(args.url, events)
    elif args.cmd == "remove":
        cmd_remove(args.url or "")
    elif args.cmd == "test":
        cmd_test(args.url or "")
    elif args.cmd == "fire":
        if not args.event:
            print("🔴 fire 需 --event"); sys.exit(1)
        res = fire_event(args.event[0], args.summary or "手动触发")
        print(f"🟢 fired={res['fired']} · 失败 {res['failed'] or '无'}")
    elif args.cmd == "drop":
        confirm = input("⚠️ 清空全部 webhook 回调？输入 yes 确认: ")
        if confirm.strip().lower() == "yes":
            save_webhooks({"webhooks": []})
            print("🟢 已清空")
        else:
            print("⚪ 已取消")


if __name__ == "__main__":
    main()
