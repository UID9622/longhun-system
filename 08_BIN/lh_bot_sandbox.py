#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 功能: 龍魂 P2 GitHub 开源机器人外接口沙箱隔离 v1.0（P72 龍盾）
# DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·䷳艮-BOT-SANDBOX-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 上位: 01_protocols/LH-AI-ASSISTANT-CHANNELS-v1.0.md §3
"""
龍魂 P2 GitHub 开源机器人外接口沙箱 v1.0

拦截 lh_github_app.py call 的全部外接口请求，强制:
  - 方法白名单: GET/HEAD 放行 · POST/PATCH/PUT 审核 · DELETE 默认禁
  - 路径规则:   默认仅 UID9622/* 仓库 · 禁 forks 递归/orgs/user 写/admin
  - 危险动作:   force-push/transfer/delete 等关键词 → 🔴 拦截
审计:         _work/bot_sandbox_audit.jsonl（append-only）

用法:
  lh_bot_sandbox.py check GET /repos/UID9622/cnsh-spec     # 审核放行 → 0
  lh_bot_sandbox.py check DELETE /repos/UID9622/xxx        # 拦截   → 1
  lh_bot_sandbox.py audit                                   # 查看最近审计
  （集成: lh_github_app.py cmd_call 内嵌 check 调用）
"""

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_FILE = ROOT / "_work" / "bot_sandbox_audit.jsonl"

# ── 方法白名单 ──
ALLOWED_METHODS = {"GET", "HEAD"}
REVIEW_METHODS = {"POST", "PATCH", "PUT"}          # 审核放行（非破坏）
BANNED_METHODS = {"DELETE"}                         # 默认禁止

# ── 路径规则 ──
ALLOWED_OWNERS = {"UID9622"}                        # 默认仓库所有者白名单
BANNED_PATH_PATTERNS = [
    r"/repos/[^/]+/[^/]+/forks?",                   # fork 递归创建
    r"^/orgs/",                                     # 组织级操作
    r"^/user/?$",                                   # user 级根
    r"/admin",                                      # 管理接口
    r"/repos/[^/]+/[^/]+/(settings|transfer)",      # 仓库设置/转移
]

# ── 危险动作关键词 ──
DANGER_KEYWORDS = [
    "force", "force_push", "delete", "transfer", "remove",
    "rename", "archive", "private", "visibility",
]


def _audit(entry: dict):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check(method: str, path: str, allow_delete: bool = False) -> tuple[bool, str]:
    """审核外接口请求。返回 (是否放行, 原因)。"""
    method = method.upper()
    path = path if path.startswith("/") else "/" + path

    # 1. 方法白名单
    if method in BANNED_METHODS and not allow_delete:
        return False, f"DELETE 默认禁止（需显式 --allow-delete + 审计）"
    if method not in ALLOWED_METHODS | REVIEW_METHODS | BANNED_METHODS:
        return False, f"未知方法 {method}"

    # 2. 路径规则：仓库归属白名单
    m = re.match(r"^/repos/([^/]+)/", path)
    if m:
        owner = m.group(1)
        if owner not in ALLOWED_OWNERS:
            return False, f"仓库所有者 {owner} 不在白名单 {sorted(ALLOWED_OWNERS)}"

    # 3. 禁止路径模式
    for pat in BANNED_PATH_PATTERNS:
        if re.search(pat, path):
            return False, f"命中禁止路径模式 {pat}"

    # 4. 危险动作关键词（写操作时才检查）
    if method not in ALLOWED_METHODS:
        path_lower = path.lower()
        for kw in DANGER_KEYWORDS:
            if kw in path_lower:
                return False, f"命中危险动作关键词: {kw}"

    return True, "沙箱放行"


def cmd_check(args):
    if len(args) < 2:
        print("用法: check <METHOD> <path> [--allow-delete]", file=sys.stderr)
        return 1
    method = args[0]
    path = args[1]
    allow_delete = "--allow-delete" in args
    ok, reason = check(method, path, allow_delete)
    _audit({"action": "check", "method": method, "path": path,
            "verdict": "ALLOW" if ok else "BLOCK", "reason": reason})
    if ok:
        print(f"🟢 放行 {method} {path}  · {reason}")
        return 0
    print(f"🔴 拦截 {method} {path}  · {reason}")
    return 1


def cmd_audit(_args):
    if not AUDIT_FILE.exists():
        print("暂无沙箱审计记录")
        return 0
    lines = AUDIT_FILE.read_text(encoding="utf-8").strip().splitlines()
    print(f"── P2 沙箱审计（最近 {min(10, len(lines))}/{len(lines)} 条）──")
    for ln in lines[-10:]:
        d = json.loads(ln)
        icon = "🟢" if d["verdict"] == "ALLOW" else "🔴"
        print(f"  {icon} {d.get('ts','')} {d['method']} {d['path']} → {d['verdict']} ({d['reason']})")
    return 0


COMMANDS = {"check": cmd_check, "audit": cmd_audit}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    sys.exit(COMMANDS[sys.argv[1]](sys.argv[2:]))
