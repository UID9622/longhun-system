#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
╔══════════════════════════════════════════════════════════════════════╗
║  龍魂·熔断控制器 v2.0 — 多协议 · 三级策略 · 主权令牌管理         ║
║  DNA: #龍芯⚡️2026-07-06-FUSE-CONTROL-v2.0                         ║
║                                                                      ║
║  命令：                                                              ║
║    trip                           → 🔴 全局熔断                     ║
║    reset                          → 🟢 重置熔断                     ║
║    status                         → 📊 查看熔断状态                 ║
║    push-confirm                   → 🔑 生成一次性推送令牌           ║
║    block  <domain> [--protocol] [--level]   → 🚫 阻断域名          ║
║    unblock <domain> [--protocol]           → ✅ 解除阻断            ║
║    override <domain> [--duration]          → ⏳ 临时放行            ║
║    token status                            → 🔐 令牌状态            ║
║    token renew                             → 🔄 续期令牌            ║
║    audit [--tail N]                        → 📜 审计日志            ║
║                                                                      ║
║  策略分级：                                                          ║
║    警告级 (WARN)  → 记录访问日志，不阻断                            ║
║    软阻断 (SOFT)  → 阻断但可临时放行 (override)                      ║
║    硬阻断 (HARD)  → 永久阻断 (不可覆盖)                             ║
║                                                                      ║
║  主权人: UID9622 💎 龍芯北辰                                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import json
import os
import sys
import time
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from enum import Enum

# ── 路径配置 ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = Path.home()
FUSE_DIR = os.path.join(PROJECT_ROOT, ".longhun", "fuse")
FUSE_FILE = os.path.join(FUSE_DIR, "fuse_state.json")
BLOCKLIST_FILE = os.path.join(FUSE_DIR, "blocklist.json")
TOKEN_FILE = os.path.join(FUSE_DIR, "sovereign_tokens.json")
CONFIRM_FILE = os.path.join(FUSE_DIR, "sovereign_push_confirm.txt")
AUDIT_LOG = os.path.join(PROJECT_ROOT, "logs", "fuse_audit.jsonl")
FALLBACK_LOG = os.path.join(PROJECT_ROOT, "logs", "fallback.log")

SOVEREIGN_UID = "UID9622"
SOVEREIGN_NAME_HASH = hashlib.sha256(
    "💎 龍芯北辰·诸葛鑫·Lucky@UID9622@LONGHUN".encode()
).hexdigest()[:12]  # 0x前缀用于脱敏

DNA = "#龍芯⚡️2026-07-06-FUSE-CONTROL-v2.0"


class BlockLevel(Enum):
    WARN = "WARN"    # 警告级：仅记录
    SOFT = "SOFT"    # 软阻断：可临时放行
    HARD = "HARD"    # 硬阻断：永久

class BlockProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    DNS = "dns"
    ALL = "all"

# ── 工具函数 ──
def ensure_dirs():
    os.makedirs(FUSE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    os.makedirs(os.path.dirname(FALLBACK_LOG), exist_ok=True)

def audit_log(action: str, detail: str = "", level: str = "INFO"):
    """写入熔断审计日志（主权人脱敏）"""
    ensure_dirs()
    event = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action,
        "detail": detail,
        "level": level,
        "sovereign_hash": f"0x{SOVEREIGN_NAME_HASH}",  # 脱敏
        "dna": DNA,
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def fallback_log(msg: str):
    """写入 fallback 日志"""
    ensure_dirs()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(FALLBACK_LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


# ── 熔断状态管理 ──
def read_fuse_state() -> dict[str, Any]:
    if os.path.exists(FUSE_FILE):
        with open(FUSE_FILE) as f:
            return json.load(f)
    return {
        "status": "ACTIVE",
        "trip_count": 0,
        "last_trip": None,
        "last_reset": None,
        "sovereign_uid": SOVEREIGN_UID,
        "sovereign_hash": f"0x{SOVEREIGN_NAME_HASH}",
        "created": datetime.now(timezone.utc).isoformat(),
        "dna": DNA,
        "block_levels": {"github.com": "HARD"},
        "overrides": {},  # {domain: expires_at}
    }

def write_fuse_state(state: dict[str, Any]):
    ensure_dirs()
    with open(FUSE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def read_blocklist() -> dict[str, Any]:
    if os.path.exists(BLOCKLIST_FILE):
        with open(BLOCKLIST_FILE) as f:
            return json.load(f)
    return {
        "domains": {
            "github.com": {
                "protocols": ["http", "https"],
                "level": "HARD",
                "reason": "海外代码平台永久阻断，保障数据主权",
                "blocked_at": datetime.now(timezone.utc).isoformat(),
            }
        },
        "dna": DNA,
    }

def write_blocklist(data: dict[str, Any]):
    ensure_dirs()
    with open(BLOCKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_tokens() -> dict[str, Any]:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return {
        "tokens": {
            "gitcode.com": {"token": None, "expires_at": None, "remaining": -1},
            "gitee.com": {"token": None, "expires_at": None, "remaining": -1},
        },
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "dna": DNA,
    }

def write_tokens(data: dict[str, Any]):
    ensure_dirs()
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── 命令实现 ──

def cmd_trip(reason: str = ""):
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

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🔴 龍魂熔断 · 电路已熔断                                ║
║  状态: CIRCUIT_TRIPPED | 次数: {state['trip_count']}    ║
║  原因: {(reason or '主权人手动触发')[:45]}              ║
║  重置: python3 bin/fuse_control.py reset                ║
╚═══════════════════════════════════════════════════════════╝
""")

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
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🟢 龍魂熔断 · 已重置 · 电路恢复正常                    ║
╚═══════════════════════════════════════════════════════════╝
""")

def cmd_status():
    """📊 状态查看（含多协议阻断列表）"""
    state = read_fuse_state()
    blocklist = read_blocklist()
    tokens = read_tokens()

    status = state["status"]
    icon = "🔴" if status == "CIRCUIT_TRIPPED" else "🟢"

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  {icon} 龍魂熔断 v2.0 · 状态报告                         ║
╠═══════════════════════════════════════════════════════════╣
║  主熔断: {status: <46}║
║  熔断次数: {state.get('trip_count', 0): <44}║
║  主权人: 0x{SOVEREIGN_NAME_HASH}    (脱敏)                ║
╠═══════════════════════════════════════════════════════════╣
║  阻断域名列表:                                            ║""")

    for domain, config in blocklist.get("domains", {}).items():
        level = config["level"]
        protocols = ", ".join(config["protocols"])
        level_icon = "🔴" if level == "HARD" else ("🟡" if level == "SOFT" else "⚪")
        # 检查是否有 override
        overrides = state.get("overrides", {})
        override_info = ""
        if domain in overrides:
            expires = overrides[domain]
            override_info = f" [临时放行至 {expires[:16]}]"
        print(f"║  {level_icon} {domain[:20]: <22} {level: <6} [{protocols: <20}]{override_info}")

    print("""╠═══════════════════════════════════════════════════════════╣
║  令牌状态:                                                ║""")
    for platform, t in tokens.get("tokens", {}).items():
        has_token = "✅" if t.get("token") else "❌无"
        expires = t.get("expires_at", "未设置") or "未设置"
        print(f"║  {platform: <14} {has_token}  到期: {expires[:20]}")

    print("╚═══════════════════════════════════════════════════════════╝")

def cmd_push_confirm():
    """🔑 生成一次性主权推送确认令牌"""
    state = read_fuse_state()
    if state["status"] == "CIRCUIT_TRIPPED":
        print("🔴 熔断已激活！无法生成 push 确认令牌。请先 reset。")
        return

    now = datetime.now(timezone.utc)
    token_id = uuid.uuid4().hex[:12]
    token_hash = hashlib.sha256(f"{SOVEREIGN_UID}:{now.isoformat()}:{token_id}".encode()).hexdigest()[:16]

    ensure_dirs()
    with open(CONFIRM_FILE, "w") as f:
        f.write(f"{now.strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"UID:{SOVEREIGN_UID}\n")
        f.write(f"TOKEN:{token_hash}\n")
        f.write(f"EXPIRES:5min\n")
        f.write(f"DNA:{DNA}\n")

    audit_log("PUSH_CONFIRM_GENERATED", f"token={token_hash}")
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🔑 主权 Push 确认令牌 · 有效 5 分钟                     ║
║  TOKEN: {token_hash}                                     ║
╚═══════════════════════════════════════════════════════════╝
""")

def cmd_block(domain: str, protocol: str = "http", level: str = "HARD", reason: str = ""):
    """🚫 阻断域名"""
    protocols = protocol.split(",")
    valid_protos = []
    for p in protocols:
        p = p.strip().lower()
        if p in ("http", "https", "ssh", "dns", "all"):
            if p == "all":
                valid_protos = ["http", "https", "ssh", "dns"]
                break
            valid_protos.append(p)

    if not valid_protos:
        print("❌ 请指定有效协议: http, https, ssh, dns, all")
        return

    try:
        blevel = BlockLevel[level.upper()]
    except KeyError:
        print("❌ 请指定有效阻断级别: WARN, SOFT, HARD")
        return

    blocklist = read_blocklist()
    blocklist["domains"][domain] = {
        "protocols": valid_protos,
        "level": blevel.value,
        "reason": reason or f"主权人命令阻断 · {blevel.value}级",
        "blocked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_blocklist(blocklist)

    level_desc = {"WARN": "⚪ 警告级(仅记录)", "SOFT": "🟡 软阻断(可临时放行)", "HARD": "🔴 硬阻断(永久)"}
    audit_log("DOMAIN_BLOCKED", f"{domain}/{','.join(valid_protos)}/{blevel.value}")
    print(f"{level_desc.get(blevel.value, blevel.value)} · {domain} [{', '.join(valid_protos)}] 已阻断")

def cmd_unblock(domain: str, protocol: str = "all"):
    """✅ 解除域名阻断"""
    blocklist = read_blocklist()
    if protocol == "all":
        if domain in blocklist["domains"]:
            del blocklist["domains"][domain]
            write_blocklist(blocklist)
            print(f"✅ {domain} 已从阻断列表移除")
            audit_log("DOMAIN_UNBLOCKED", f"{domain}/all")
        else:
            print(f"⚠️ {domain} 不在阻断列表中")
    else:
        if domain in blocklist["domains"]:
            config = blocklist["domains"][domain]
            if protocol in config["protocols"]:
                config["protocols"].remove(protocol)
                if not config["protocols"]:
                    del blocklist["domains"][domain]
                write_blocklist(blocklist)
                print(f"✅ {domain} 的 {protocol} 协议阻断已解除")
                audit_log("DOMAIN_UNBLOCKED", f"{domain}/{protocol}")
            else:
                print(f"⚠️ {domain} 未对 {protocol} 协议阻断")
        else:
            print(f"⚠️ {domain} 不在阻断列表中")

def cmd_override(domain: str, duration: str = "1h"):
    """⏳ 临时放行（仅对 SOFT 级阻断有效）"""
    blocklist = read_blocklist()
    if domain not in blocklist["domains"]:
        print(f"⚠️ {domain} 不在阻断列表中")
        return

    config = blocklist["domains"][domain]
    if config["level"] == "HARD":
        print(f"🔴 {domain} 为硬阻断(HARD)域名，不可临时放行")
        return

    # 解析时长
    dur = duration.lower()
    unit = dur[-1]
    try:
        amount = int(dur[:-1])
    except ValueError:
        amount = 1

    if unit == "h":
        delta = timedelta(hours=amount)
    elif unit == "m":
        delta = timedelta(minutes=amount)
    elif unit == "d":
        delta = timedelta(days=amount)
    else:
        delta = timedelta(hours=1)

    expires = (datetime.now(timezone.utc) + delta).isoformat()
    state = read_fuse_state()
    state.setdefault("overrides", {})[domain] = expires
    write_fuse_state(state)

    audit_log("DOMAIN_OVERRIDE", f"{domain}/duration={duration}/expires={expires}")
    print(f"⏳ {domain} 已临时放行 · 有效期至 {expires[:19]}Z")

def cmd_token_status():
    """🔐 主权令牌状态"""
    tokens = read_tokens()
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  🔐 主权令牌状态                                         ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    for platform, t in tokens.get("tokens", {}).items():
        has_token = t.get("token") is not None
        remaining = t.get("remaining", -1)
        expires = t.get("expires_at", "未设置") or "未设置"

        if not has_token:
            print(f"║  ❌ {platform: <14} 未配置令牌                          ║")
        else:
            # 检查是否即将过期
            try:
                exp_dt = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
                days_left = (exp_dt - datetime.now(timezone.utc)).days
                if days_left <= 0:
                    print(f"║  🔴 {platform: <14} 令牌已过期！请运行 lh6 token renew ║")
                elif days_left <= 7:
                    print(f"║  🟡 {platform: <14} 即将过期({days_left}天) 剩余{remaining}次 ║")
                else:
                    print(f"║  🟢 {platform: <14} 有效 剩余{remaining}次 · {days_left}天后过期║")
            except Exception:
                print(f"║  🟢 {platform: <14} 已配置 · 到期{expires[:16]}        ║")
    print("╚═══════════════════════════════════════════════════════════╝")

def cmd_token_renew(platform: str = "all"):
    """🔄 续期令牌"""
    tokens = read_tokens()
    now = datetime.now(timezone.utc)
    renewed = []

    platforms = ["gitcode.com", "gitee.com"] if platform == "all" else [platform]

    for p in platforms:
        if p in tokens["tokens"]:
            # 续期逻辑（实际应调用对应平台的 API）
            tokens["tokens"][p]["expires_at"] = (now + timedelta(days=90)).isoformat()
            tokens["tokens"][p]["remaining"] = 1000
            renewed.append(p)

    tokens["last_updated"] = now.isoformat()
    write_tokens(tokens)
    audit_log("TOKEN_RENEWED", f"platforms={','.join(renewed)}")

    if renewed:
        print(f"🔄 令牌已续期: {', '.join(renewed)}（90天有效期，1000次配额）")
    else:
        print(f"⚠️ 未找到需续期的平台: {platform}")

def cmd_audit(tail: int = 20):
    """📜 查看熔断审计日志"""
    if not os.path.exists(AUDIT_LOG):
        print("📜 暂无审计日志")
        return

    with open(AUDIT_LOG) as f:
        lines = f.readlines()

    recent = lines[-tail:] if len(lines) > tail else lines
    print(f"\n📜 熔断审计日志（最近 {len(recent)} 条）")
    print("─" * 70)
    for line in recent:
        try:
            e = json.loads(line)
            ts = e.get("timestamp", "")[:19]
            action = e.get("action", "?")
            detail = e.get("detail", "")[:35]
            sh = e.get("sovereign_hash", "?")
            print(f"  {ts} | {action: <24} | {detail: <35} | {sh}")
        except Exception:
            print(f"  {line.strip()[:90]}")
    print("─" * 70)

def cmd_validate_plist():
    """校验龍魂 plist（委托 plist_validator）"""
    import subprocess
    validator = os.path.join(PROJECT_ROOT, "bin", "plist_validator.py")
    plist = os.path.join(PROJECT_ROOT, "launchd", "com.longhun.symbiote.plist")
    result = subprocess.run(
        ["python3", validator, plist],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        # fallback 机制：校验失败建议手动启动
        print("\n🔄 触发 fallback：建议手动启动共生体服务")
        print("   bash bin/start_symbiote.sh")
        fallback_log(f"PLIST_VALIDATION_FAILED: exit_code={result.returncode}")

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

    elif cmd == "block":
        if len(sys.argv) < 3:
            print("❌ 用法: fuse block <域名> [--protocol http,https,ssh,dns,all] [--level WARN|SOFT|HARD]")
            return
        domain = sys.argv[2]
        protocol = "all"
        level = "SOFT"
        reason = ""
        # 简单参数解析
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--protocol" and i + 1 < len(args):
                protocol = args[i + 1]
                i += 2
            elif args[i] == "--level" and i + 1 < len(args):
                level = args[i + 1]
                i += 2
            elif args[i] == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_block(domain, protocol, level, reason)

    elif cmd == "unblock":
        if len(sys.argv) < 3:
            print("❌ 用法: fuse unblock <域名> [--protocol <协议>]")
            return
        domain = sys.argv[2]
        protocol = "all"
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--protocol" and i + 1 < len(args):
                protocol = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_unblock(domain, protocol)

    elif cmd == "override":
        if len(sys.argv) < 3:
            print("❌ 用法: fuse override <域名> [--duration <时长如1h/30m/7d>]")
            return
        domain = sys.argv[2]
        duration = "1h"
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--duration" and i + 1 < len(args):
                duration = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_override(domain, duration)

    elif cmd == "token":
        if len(sys.argv) < 3:
            print("❌ 用法: fuse token <status|renew> [platform]")
            return
        sub = sys.argv[2].lower()
        if sub == "status":
            cmd_token_status()
        elif sub == "renew":
            platform = sys.argv[3] if len(sys.argv) > 3 else "all"
            cmd_token_renew(platform)
        else:
            print(f"❌ 未知子命令: {sub}")

    elif cmd == "audit":
        tail = 20
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--tail" and i + 1 < len(args):
                tail = int(args[i + 1])
                i += 2
            else:
                i += 1
        cmd_audit(tail)

    elif cmd == "validate":
        cmd_validate_plist()

    elif cmd == "help":
        print_usage()

    else:
        print(f"❌ 未知命令: {cmd}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
