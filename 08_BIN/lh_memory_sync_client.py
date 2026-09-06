#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丁酉·癸未·丑时·䷞咸-MEMORY-SYNC-CLIENT-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
lh_memory_sync_client.py — 鲲鹏8787 DNA记忆同步客户端 v1.1

契约(服务端 lh_memory_sync_server.py v1.0 实测):
  POST /sync/store   — 须 X-API-Token(远程) · MemoryPayload: id/dna/timestamp/
                       device/device_fp/topic/content 必填(其余有默认)
  GET  /sync/pull    — ?limit=&since=&device_fp= (无 dna 参数 → 本地过滤)
  GET  /sync/health  — 免认证健康检查
幂等: 同 DNA 服务端返回 duplicate(不覆盖)

用法:
  lh memory-sync push --data '{"dna":"…","topic":"…","content":"…"}' [--host H:PORT]
  lh memory-sync pull [--limit N] [--dna 码] [--device-fp xx]
  lh memory-sync health
"""
import sys, json, hashlib, uuid, argparse, platform, getpass
from datetime import datetime, timezone, timedelta
from pathlib import Path
import urllib.request, urllib.error

# 直连（防全局 socks5h 代理毒化 · 与 Notion MCP 同源问题 · 2026-09-06）
_NO_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))

KPENG_HOST = "https://uid9622.cn"  # nginx 443 反代 /sync/ → 127.0.0.1:8787(华为云安全组未放8787公网·经nginx唯一通道)
CST = timezone(timedelta(hours=8))
TOKEN_CANDIDATES = (
    Path(__file__).resolve().parent.parent / ".codebuddy" / "memory" / ".memory_sync_token",
    Path.home() / ".longhun" / ".memory_sync_token",
    Path.home() / ".longhun" / ".memory_token",
    Path(__file__).resolve().parent.parent / ".codebuddy" / "memory" / ".api_token",
)

def _load_token() -> str:
    import os
    env_t = os.environ.get("LH_MEMORY_TOKEN", "").strip()
    if env_t:
        return env_t
    for f in TOKEN_CANDIDATES:
        if f.exists():
            t = f.read_text("utf-8").strip()
            if t and t.isascii():
                return t
    return ""

def _device_fp() -> str:
    return hashlib.sha256(f"{platform.node()}:{getpass.getuser()}".encode()).hexdigest()[:8]

def _full_payload(data: dict) -> dict:
    now = datetime.now(CST).isoformat()
    d = data.get("dna", "")
    meta = {k: v for k, v in data.items()
            if k not in ("id", "dna", "timestamp", "device", "device_fp",
                         "topic", "content", "session_id", "priority", "tags",
                         "version", "parent_dna", "checksum", "encrypted")}
    return {
        "id": data.get("id") or uuid.uuid4().hex,
        "dna": d,
        "timestamp": data.get("timestamp") or now,
        "device": data.get("device") or f"mac-{getpass.getuser()}",
        "device_fp": data.get("device_fp") or _device_fp(),
        "session_id": data.get("session_id", ""),
        "topic": data.get("topic") or "memory-sync 测试推送",
        "content": data.get("content") or json.dumps(meta, ensure_ascii=False),
        "priority": data.get("priority", "P2"),
        "tags": data.get("tags") or [],
        "version": int(data.get("version", 1)),
        "parent_dna": data.get("parent_dna", ""),
        "checksum": data.get("checksum") or hashlib.sha256(d.encode()).hexdigest()[:16],
        "encrypted": bool(data.get("encrypted", False)),
    }

def _req(url: str, token: str, method="GET", payload=None):
    headers = {"X-API-Token": token}
    if payload is not None:
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                     headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    with _NO_PROXY.open(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))

def cmd_push(args):
    data = json.loads(args.data) if args.data else {}
    if not data.get("dna"):
        print("❌ 缺少 dna 字段，拒绝推送")
        sys.exit(1)
    token = _load_token()
    if not token:
        print("❌ 未找到 X-API-Token（~/.longhun/.memory_token 或 .codebuddy/memory/.api_token）")
        sys.exit(1)
    try:
        resp = _req(f"{args.host}/sync/store", token, payload=_full_payload(data))
        print(f"✅ push: {resp.get('status')} · {resp.get('message','')} · dna={resp.get('dna','')[:24]}…")
    except urllib.error.HTTPError as e:
        print(f"❌ push HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ push 失败: {e}")
        sys.exit(1)

def cmd_pull(args):
    token = _load_token()
    if not token:
        print("❌ 未找到 X-API-Token")
        sys.exit(1)
    url = f"{args.host}/sync/pull?limit={args.limit}"
    if args.since:
        url += f"&since={args.since}"
    if args.device_fp:
        url += f"&device_fp={args.device_fp}"
    try:
        resp = _req(url, token)
    except urllib.error.HTTPError as e:
        print(f"❌ pull HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ pull 失败: {e}")
        sys.exit(1)
    entries = resp.get("entries", [])
    if args.dna:
        entries = [e for e in entries if e.get("dna", "") == args.dna]
    print(f"📦 total={resp.get('total', len(entries))} server_time={resp.get('server_time','')}")
    for e in entries[:args.limit]:
        print(f"  · [{e.get('dna','')[:20]}…] {e.get('topic','')} @ {e.get('timestamp','')} ({e.get('device','')})")

def cmd_health(args):
    try:
        with _NO_PROXY.open(f"{args.host}/sync/health", timeout=10) as r:
            print(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"❌ health 失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="鲲鹏8787 DNA记忆同步客户端")
    p.add_argument("cmd", choices=["push", "pull", "health"])
    p.add_argument("--host", default=KPENG_HOST)
    p.add_argument("--data", help="push: JSON字符串(含dna·可选topic/content等)")
    p.add_argument("--limit", type=int, default=20, help="pull: 条数")
    p.add_argument("--since", default="", help="pull: ISO时间戳过滤")
    p.add_argument("--device-fp", dest="device_fp", default="", help="pull: 按设备过滤")
    p.add_argument("--dna", default="", help="pull: 本地按DNA过滤")
    a = p.parse_args()
    {"push": cmd_push, "pull": cmd_pull, "health": cmd_health}[a.cmd](a)
