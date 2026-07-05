#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  龍魂·熔断控制器 — 主权人唯一开关                                ║
║  DNA: #龍芯⚡️2026-07-06-FUSE-CONTROL-v1.0                        ║
║                                                                      ║
║  命令：                                                              ║
║    trip          → 🔴 全局熔断（阻断一切 push/高危操作）            ║
║    reset         → 🟢 重置熔断（恢复正常）                          ║
║    status        → 📊 查看当前熔断状态                              ║
║    push-confirm  → 🔑 生成一次性主权 push 确认令牌（5分钟有效）    ║
║    lock-github   → 🔒 永久锁定 GitHub 推送（不可恢复）             ║
║                                                                      ║
║  主权人: UID9622 💎 龍芯北辰                                       ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import json
import os
import sys
import time
import hashlib
import uuid
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUSE_DIR = os.path.join(PROJECT_ROOT, ".longhun")
FUSE_FILE = os.path.join(FUSE_DIR, "fuse_state.json")
CONFIRM_FILE = os.path.join(FUSE_DIR, "sovereign_push_confirm.txt")
AUDIT_LOG = os.path.join(PROJECT_ROOT, "logs", "fuse_audit.jsonl")
SOVEREIGN_UID = "UID9622"
SOVEREIGN_NAME = "💎 龍芯北辰·诸葛鑫·Lucky"


def ensure_dirs():
    os.makedirs(FUSE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)


def read_fuse_state():
    if os.path.exists(FUSE_FILE):
        with open(FUSE_FILE) as f:
            return json.load(f)
    return {
        "status": "ACTIVE",
        "github_locked": False,
        "trip_count": 0,
        "last_trip": None,
        "last_reset": None,
        "sovereign_uid": SOVEREIGN_UID,
        "sovereign_name": SOVEREIGN_NAME,
        "created": datetime.now(timezone.utc).isoformat(),
        "dna": "#龍芯⚡️2026-07-06-FUSE-CONTROL-v1.0",
    }


def write_fuse_state(state):
    with open(FUSE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def audit_log(action, detail=""):
    event = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action,
        "detail": detail,
        "uid": SOVEREIGN_UID,
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def cmd_trip(reason=""):
    """🔴 全局熔断"""
    state = read_fuse_state()
    
    if state["status"] == "CIRCUIT_TRIPPED":
        print("🔴 熔断已处于激活状态，无需重复触发")
        return

    state["status"] = "CIRCUIT_TRIPPED"
    state["trip_count"] += 1
    state["last_trip"] = datetime.now(timezone.utc).isoformat()
    state["trip_reason"] = reason or "主权人手动触发"
    write_fuse_state(state)
    audit_log("CIRCUIT_TRIPPED", reason or "manual_trip")

    print("""
╔═══════════════════════════════════════════════════════════╗
║  🔴 龍魂熔断 · 电路已熔断                                  ║
║                                                             ║
║  FUSE STATUS: CIRCUIT_TRIPPED                                ║
║                                                             ║
║  以下操作已锁定：                                            ║
║    ❌  git push（全部远程）                                 ║
║    ❌  文件删除操作                                         ║
║    ❌  生产环境部署                                         ║
║                                                             ║
║  原因: {reason: <47}║
║                                                             ║
║  重置: python3 bin/fuse_control.py reset                   ║
╚═══════════════════════════════════════════════════════════╝
""".format(reason=(reason or "主权人手动触发")[:47]))


def cmd_reset():
    """🟢 重置熔断"""
    state = read_fuse_state()
    
    if state["status"] == "ACTIVE":
        print("🟢 熔断未激活，无需重置")
        return

    state["status"] = "ACTIVE"
    state["last_reset"] = datetime.now(timezone.utc).isoformat()
    write_fuse_state(state)
    audit_log("CIRCUIT_RESET", "manual_reset")

    print("""
╔═══════════════════════════════════════════════════════════╗
║  🟢 龍魂熔断 · 已重置                                       ║
║                                                             ║
║  FUSE STATUS: ACTIVE                                         ║
║  trip_count: {trip_count: <47}║
║  github_locked: {github_locked: <43}║
║                                                             ║
║  所有推送操作已恢复正常                                      ║
╚═══════════════════════════════════════════════════════════╝
""".format(
        trip_count=str(state.get("trip_count", 0))[:47],
        github_locked=str(state.get("github_locked", False))[:43]
    ))


def cmd_status():
    """📊 查看状态"""
    state = read_fuse_state()
    status = state["status"]
    
    icon = "🔴" if status == "CIRCUIT_TRIPPED" else "🟢"
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  {icon} 龍魂熔断 · 状态报告                                 ║
╠═══════════════════════════════════════════════════════════╣
║  FUSE STATUS:    {status: <43}║
║  GitHub 锁定:    {'🔒 已锁定' if state.get('github_locked') else '⚠️ 未锁定': <39}║
║  熔断次数:       {str(state.get('trip_count', 0)): <43}║
║  上次熔断:       {(state.get('last_trip') or '从未'): <43}║
║  上次重置:       {(state.get('last_reset') or '从未'): <43}║
║  主权人:         {SOVEREIGN_NAME: <24}║
╠═══════════════════════════════════════════════════════════╣
║  HTTP 阻断列表:                                             ║
║    ❌ github.com → 永久阻断 (pre-push hook)                ║
║    🟡 gitcode.com → 需主权确认令牌                         ║
║    🟡 gitee.com → 需主权确认令牌                           ║
╚═══════════════════════════════════════════════════════════╝
""")


def cmd_push_confirm():
    """🔑 生成一次性主权 push 确认令牌"""
    state = read_fuse_state()
    
    if state["status"] == "CIRCUIT_TRIPPED":
        print("🔴 熔断已激活！无法生成 push 确认令牌。请先 reset。")
        return

    # GitHub 已永久锁定，但 gitcode/gitee 仍可推送（需令牌）
    if state.get("github_locked"):
        print("⚠️  GitHub 已永久锁定。本令牌仅对 gitcode/gitee 有效。")

    now = datetime.now(timezone.utc)
    token_id = uuid.uuid4().hex[:12]
    token_hash = hashlib.sha256(
        f"{SOVEREIGN_UID}:{now.isoformat()}:{token_id}".encode()
    ).hexdigest()[:16]

    ensure_dirs()
    with open(CONFIRM_FILE, "w") as f:
        f.write(f"{now.strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"UID:{SOVEREIGN_UID}\n")
        f.write(f"TOKEN:{token_hash}\n")
        f.write(f"EXPIRES:5min\n")
        f.write(f"DNA:#龍芯⚡️2026-07-06-PUSH-CONFIRM-{token_id}\n")

    audit_log("PUSH_CONFIRM_GENERATED", f"token={token_hash}")

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🔑 龍魂主权 Push 确认令牌 · 已生成                        ║
╠═══════════════════════════════════════════════════════════╣
║  TOKEN:     {token_hash: <46}║
║  生成时间:  {now.strftime('%Y-%m-%dT%H:%M:%SZ'): <43}║
║  有效期:    5分钟                                           ║
║                                                             ║
║  允许推送目标: gitcode.com / gitee.com                     ║
║  阻断目标:     github.com（永久）                           ║
║                                                             ║
║  立即执行 git push（5分钟内有效）                           ║
╚═══════════════════════════════════════════════════════════╝
""")


def cmd_lock_github():
    """🔒 永久锁定 GitHub 推送"""
    state = read_fuse_state()
    state["github_locked"] = True
    state["github_locked_at"] = datetime.now(timezone.utc).isoformat()
    write_fuse_state(state)
    audit_log("GITHUB_PERMANENTLY_LOCKED", "irreversible")

    print("""
╔═══════════════════════════════════════════════════════════╗
║  🔒 GitHub 推送 · 永久锁定                                 ║
║                                                             ║
║  ⚠️  此操作不可逆                                           ║
║  ⚠️  github.com 推送功能已被永久关闭                       ║
║  ⚠️  连手动发布开源也做不到了                                ║
║                                                             ║
║  龍魂系统代码安全：已保全                                   ║
╚═══════════════════════════════════════════════════════════╝
""")


def print_usage():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    
    if cmd == "trip":
        reason = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_trip(reason)
    elif cmd == "reset":
        cmd_reset()
    elif cmd == "status":
        cmd_status()
    elif cmd == "push-confirm":
        cmd_push_confirm()
    elif cmd == "lock-github":
        cmd_lock_github()
    elif cmd == "help":
        print_usage()
    else:
        print(f"❌ 未知命令: {cmd}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
