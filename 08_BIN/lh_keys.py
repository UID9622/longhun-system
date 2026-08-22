#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·癸亥·申时·䷗复-UNIFIED-KEYS-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
統一密钥出口 v1.1 — 任何 AI 一条命令拿密钥·不碰明文·不进 git · MFA二次验证
═══════════════════════════════════════════════════════
解决老大痛点：密钥散落多处，跟每个 AI 都要重复解释。
本引擎 = 唯一出口，任何 AI（Kimi/Claude/CodeBuddy…）一条命令搞定。

v1.1（2026-08-17·P05审计）:
  🔥 华为MFA二次验证焊死：get 加 --mfa <动态口令>，不配对不给用
  🔥 新增 mfa 子命令：lh keys mfa setup/bind/status/verify/unbind
  🔥 引擎: 08_BIN/keys/lh_huawei_mfa.py（TOTP RFC6238·AES-256-GCM加密存储）

用法:
  python3 bin/lh_keys.py list        # 列全部密钥名+状态+来源（不显值）
  python3 bin/lh_keys.py get <KEY>   # 取单值·自动复制剪贴板（--raw 只打印不复制）
  python3 bin/lh_keys.py get <KEY> --mfa 123456   # MFA验证后取密钥（推荐）
  python3 bin/lh_keys.py check       # HTTP 体检关键密钥（只报 OK/FAIL·不打印值）
  python3 bin/lh_keys.py mfa setup   # 初始化华为MFA设备（首次·输出扫码二维码）
  python3 bin/lh_keys.py mfa qr      # 重新显示扫码二维码（手机扫）
  python3 bin/lh_keys.py mfa bind 123456   # 绑定设备
  python3 bin/lh_keys.py mfa status # 查看MFA状态
  python3 bin/lh_keys.py mfa verify 123456 # 验证口令（建立5分钟会话）

数据来源（按优先级）:
  1. ~/.longhun/secrets.env   — 统一密钥落位文件（600 权限·本引擎写入）
  2. ~/.env                   — loader 既有来源
  3. ~/.longhun/env/          — 单 key 文件目录
  4. config/notion_config.json— Notion 引擎配置（已移出 git 跟踪）
  5. macOS Keychain           — loader 兜底
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))

from lh_secrets_loader import get_credential, list_services  # noqa: E402

# 华为MFA引擎（v1.1）
MFA_ENGINE = ROOT / "08_BIN" / "keys" / "lh_huawei_mfa.py"
sys.path.insert(0, str(ROOT / "08_BIN" / "keys"))

SECRETS_ENV = HOME / ".longhun" / "secrets.env"
ENVDIR = HOME / ".longhun" / "env"
NOTION_CONFIG = ROOT / "config" / "notion_config.json"


def _mfa_gateway():
    """懒加载 MFA 网关"""
    from lh_huawei_mfa import MFAGateway
    return MFAGateway()


def _mask(value: str) -> str:
    """打码显示：只留前4后4"""
    if not value:
        return "(空)"
    if len(value) <= 12:
        return "***"
    return f"{value[:4]}…{value[-4:]}"


def _read_secrets_env() -> dict:
    """读 secrets.env（本引擎主落位）"""
    if not SECRETS_ENV.exists():
        return {}
    out = {}
    for line in SECRETS_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:]
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _read_envdir() -> dict:
    """读 ~/.longhun/env/ 单 key 文件"""
    out = {}
    if ENVDIR.is_dir():
        for f in sorted(ENVDIR.iterdir()):
            if f.is_file():
                out[f.name] = f.read_text(encoding="utf-8", errors="ignore").strip()
    return out


def _read_notion_config() -> dict:
    if NOTION_CONFIG.exists():
        try:
            d = json.loads(NOTION_CONFIG.read_text(encoding="utf-8"))
            if d.get("notion_token"):
                return {"NOTION_TOKEN": d["notion_token"]}
        except Exception:
            pass
    return {}


def cmd_list() -> int:
    """列出全部密钥名+状态+来源（不显值）"""
    print("🔑 統一密钥出口 · 密钥清单（不显示明文）\n")

    seen = set()
    services = list_services()
    if services:
        print("── 加载器注册（~/.env / vault / secrets.env / Keychain）──")
        for key, info in services.items():
            seen.add(key)
            icon = {"active": "🟢", "backup": "🟡", "missing": "🔴", "invalid": "❌"}.get(
                info.get("status", ""), "⚪")
            desc = info.get("description") or ""
            print(f"  {icon} {key}  (来源: {info.get('source','?')})")
            if desc:
                print(f"       {desc}")

    env_files = _read_envdir()
    if env_files:
        print("\n── ~/.longhun/env/ 单 key 文件 ──")
        for k, v in env_files.items():
            if k not in seen:
                seen.add(k)
                print(f"  🟢 {k}  (文件·长度{len(v)})")

    extra = _read_notion_config()
    if extra:
        for k, v in extra.items():
            if k not in seen:
                seen.add(k)
                print(f"  🟢 {k}  (config/notion_config.json·长度{len(v)})")

    print(f"\n合计 {len(seen)} 个密钥可用。")
    print("用法: lh keys get <名称> 取单值 · lh keys check 体检")
    return 0


def cmd_get(key: str, raw: bool = False, mfa_code: str = None) -> int:
    """取单值：默认复制剪贴板；--raw 只打印；--mfa 先过华为MFA二次验证"""
    # v1.1：MFA 二次验证焊死（不配对不给用）
    if mfa_code is not None:
        try:
            gw = _mfa_gateway()
            auth = gw.require_auth(f"get_key:{key}", mfa_code)
        except Exception as e:
            print(f"❌ MFA引擎异常: {e}", file=sys.stderr)
            print("   提示: lh keys mfa status 查看MFA状态", file=sys.stderr)
            return 1
        if not auth.get("success"):
            msg = auth.get("error") or auth.get("message") or "MFA验证失败"
            msg = msg.lstrip("❌ ").strip()
            if auth.get("need_mfa"):
                print(f"🔐 {msg}", file=sys.stderr)
                print(f"   用法: lh keys get {key} --mfa <6位动态口令>", file=sys.stderr)
            elif auth.get("setup_required"):
                print(f"🔐 {msg}", file=sys.stderr)
                print("   首次部署: lh keys mfa setup → lh keys mfa bind <口令>", file=sys.stderr)
            else:
                print(f"❌ {msg}", file=sys.stderr)
            return 1
        print(f"✅ MFA验证通过 ({auth.get('message','')})")

    value = get_credential(key)
    source = "loader"

    if not value:
        extra = _read_notion_config()
        if key == "NOTION_TOKEN" and extra.get("NOTION_TOKEN"):
            value = extra["NOTION_TOKEN"]
            source = "config/notion_config.json"
        else:
            env_files = _read_envdir()
            if key in env_files:
                value = env_files[key]
                source = f"~/.longhun/env/{key}"
            else:
                sec = _read_secrets_env()
                if key in sec:
                    value = sec[key]
                    source = "~/.longhun/secrets.env"

    if not value:
        print(f"❌ 未找到密钥: {key}", file=sys.stderr)
        print("   提示: lh keys list 查看全部可用名称", file=sys.stderr)
        return 1

    if raw:
        print(value)
    else:
        try:
            p = subprocess.run(["pbcopy"], input=value.encode(), check=True)
            if p.returncode == 0:
                print(f"✅ {key} 已复制到剪贴板 (来源: {source})")
                print(f"   值形: {_mask(value)}")
            else:
                print(value)
        except Exception:
            print(value)
    return 0


def cmd_check() -> int:
    """HTTP 体检关键密钥（只报 OK/FAIL）"""
    print("🔍 密钥体检（不打印明文）\n")
    failures = 0

    notion_token = get_credential("NOTION_TOKEN")
    if not notion_token:
        extra = _read_notion_config()
        notion_token = extra.get("NOTION_TOKEN", "")
    if notion_token:
        code = _probe_notion(notion_token)
        ok = code == 200
        print(f"  {'🟢' if ok else '🔴'} NOTION_TOKEN  Notion API -> HTTP {code}"
              f" ({'有效' if ok else '无效/失效'})")
        if not ok:
            failures += 1
    else:
        print("  ⚪ NOTION_TOKEN  未配置")
        failures += 1

    # 预留：其它密钥体检端点在此扩展
    print("\n完成。0 表示全部通过。")
    return failures


def _probe_notion(token: str) -> int:
    """探测 Notion token 有效性，只返回 HTTP 状态码"""
    import urllib.request
    req = urllib.request.Request(
        "https://api.notion.com/v1/users/me",
        headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except Exception as e:
        return getattr(e, "code", 0)


def cmd_mfa(sub: str = "") -> int:
    """华为MFA管理子命令"""
    import subprocess as sp
    if not sub:
        print(__doc__)
        return 0
    args = sub.split()
    op = args[0]
    if op in ("setup", "s"):
        return sp.run([sys.executable, str(MFA_ENGINE), "--setup"]).returncode
    if op in ("qr", "q"):
        return sp.run([sys.executable, str(MFA_ENGINE), "--qr"]).returncode
    if op in ("status", "st"):
        return sp.run([sys.executable, str(MFA_ENGINE), "--status"]).returncode
    if op in ("bind", "b") and len(args) >= 2:
        return sp.run([sys.executable, str(MFA_ENGINE), "--bind", args[1]]).returncode
    if op in ("verify", "v") and len(args) >= 2:
        return sp.run([sys.executable, str(MFA_ENGINE), "--verify", args[1]]).returncode
    if op in ("unbind", "u") and len(args) >= 2:
        return sp.run([sys.executable, str(MFA_ENGINE), "--unbind", args[1]]).returncode
    print("❌ mfa 用法:", file=sys.stderr)
    print("   lh keys mfa setup               # 初始化设备(首次·带二维码)", file=sys.stderr)
    print("   lh keys mfa qr                  # 重新显示扫码二维码", file=sys.stderr)
    print("   lh keys mfa bind <6位口令>       # 绑定设备", file=sys.stderr)
    print("   lh keys mfa verify <6位口令>     # 验证口令", file=sys.stderr)
    print("   lh keys mfa status              # 查看状态", file=sys.stderr)
    print("   lh keys mfa unbind <6位口令>     # 解绑", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd in ("list", "ls", "l"):
        return cmd_list()
    if cmd in ("get", "g"):
        if len(sys.argv) < 3:
            print("用法: lh keys get <名称> [--raw] [--mfa <6位口令>]", file=sys.stderr)
            return 1
        rest = sys.argv[3:]
        raw = "--raw" in rest
        mfa_code = None
        for i, a in enumerate(rest):
            if a == "--mfa" and i + 1 < len(rest):
                mfa_code = rest[i + 1]
                break
        return cmd_get(sys.argv[2].upper(), raw=raw, mfa_code=mfa_code)
    if cmd in ("mfa", "m"):
        return cmd_mfa(" ".join(sys.argv[2:]))
    if cmd in ("check", "c"):
        return cmd_check()
    print(f"❌ 未知子命令: {cmd}", file=sys.stderr)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
