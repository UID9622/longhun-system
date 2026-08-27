#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-丁卯-GITHUB-APP-TOOL-v1.0-gha1f2b3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂 GitHub App 工具 v1.0
# 统一管理龍魂系统的 GitHub App（longhun-bot）：
#   - 签发 App JWT（RS256，有效期 9 分钟，GitHub 上限 10 分钟）
#   - 换取 installation token（1 小时有效，作用域=被安装仓库）
#   - 列安装、调 API、验证 webhook 签名
#
# 用法:
#   python3 bin/lh_github_app.py init <app_id> <client_id> <slug> [pem_path]
#   python3 bin/lh_github_app.py jwt
#   python3 bin/lh_github_app.py installations
#   python3 bin/lh_github_app.py token [installation_id]
#   python3 bin/lh_github_app.py call GET /repos/UID9622/longhun-financial-deep-seek
#   python3 bin/lh_github_app.py call POST /repos/UID9622/longhun-financial-deep-seek/issues '{"title":"t"}'
#   python3 bin/lh_github_app.py webhook-verify <payload_file> <signature> [secret]
#   python3 bin/lh_github_app.py doctor
#
# 私钥 D1 级铁律: 只存 ~/.longhun/github-app/ 本地物理隔离，永不入云/入 git/入日志。

import sys
import os
import json
import base64
import time
import hashlib
import hmac
import urllib.request
import urllib.error
import subprocess
import tempfile
from pathlib import Path

try:
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

# ── 常量 ─────────────────────────────────────────────
APP_DIR = Path.home() / ".longhun" / "github-app"
CONFIG_PATH = APP_DIR / "config.json"
GITHUB_API = "https://api.github.com"
GITHUB_APP_HEADER = "application/vnd.github+json"

# ── 配置读写 ─────────────────────────────────────────
def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    # 配置文件含 App ID 等元信息，收紧权限
    os.chmod(CONFIG_PATH, 0o600)
    print(f"✅ 配置已保存: {CONFIG_PATH}")


# ── 私钥加载 ─────────────────────────────────────────
def load_private_key(pem_path=None):
    cfg = load_config()
    pem = Path(pem_path or cfg.get("pem_path") or APP_DIR / "longhun-bot.pem")
    if not pem.exists():
        print(f"🔴 私钥不存在: {pem}")
        print("   请先在 https://github.com/settings/apps 创建 App 并下载私钥，放到该路径")
        sys.exit(1)
    with open(pem, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    return key


# ── JWT 签发（App 身份，9 分钟有效）───────────────────
def sign_jwt():
    cfg = load_config()
    app_id = cfg.get("app_id")
    if not app_id:
        print("🔴 未配置 App ID，先运行: lh_github_app.py init <app_id> <client_id> <slug>")
        sys.exit(1)
    if not HAVE_CRYPTO:
        print("🔴 缺少 cryptography 库，运行: pip3 install cryptography")
        sys.exit(1)
    key = load_private_key()

    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    payload = {
        "iat": now - 60,          # 留 60 秒时钟偏移余量
        "exp": now + 9 * 60,      # GitHub 要求 exp ≤ iat+10min
        "iss": str(app_id),
    }
    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()
    signing_input = b64url(json.dumps(header, separators=(",", ":")).encode()) + "." + \
                    b64url(json.dumps(payload, separators=(",", ":")).encode())
    sig = key.sign(signing_input.encode(), padding.PKCS1v15(), hashes.SHA256())
    return signing_input + "." + b64url(sig)


# ── HTTP 封装 ─────────────────────────────────────────
def gh_request(method, path, token=None, data=None, jwt=None, extra_headers=None):
    headers = {
        "Accept": GITHUB_APP_HEADER,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if jwt:
        headers["Authorization"] = f"Bearer {jwt}"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra_headers:
        headers.update(extra_headers)

    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(GITHUB_API + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except Exception:
            detail = raw
        return e.code, detail


# ── 子命令 ───────────────────────────────────────────
def cmd_init(args):
    if len(args) < 3:
        print("用法: init <app_id> <client_id> <slug> [pem_path]")
        sys.exit(1)
    cfg = load_config()
    cfg["app_id"] = args[0]
    cfg["client_id"] = args[1]
    cfg["slug"] = args[2]
    if len(args) >= 4:
        cfg["pem_path"] = args[3]
    save_config(cfg)
    print(f"App ID={args[0]} · Client ID={args[1]} · Slug={args[2]}")
    print("下一步: 下载私钥到 ~/.longhun/github-app/longhun-bot.pem")


def cmd_jwt(_args):
    print(sign_jwt())


def cmd_installations(_args):
    jwt = sign_jwt()
    code, data = gh_request("GET", "/app/installations", jwt=jwt)
    if code != 200:
        print(f"🔴 获取安装列表失败 HTTP {code}: {data}")
        sys.exit(1)
    if not data:
        print("⚠️ 还没有任何安装。去 https://github.com/apps/<slug>/installations/new 安装到仓库。")
        return
    for inst in data:
        print(f"installation_id={inst['id']} · target={inst['account']['login']} "
              f"({inst['target_type']}) · 仓库数={inst.get('repository_selection')}")
        cfg = load_config()
        cfg["installation_id"] = inst["id"]
        save_config(cfg)


def cmd_token(args):
    cfg = load_config()
    inst_id = args[0] if args else cfg.get("installation_id")
    if not inst_id:
        print("🔴 未指定 installation_id，先运行: installations")
        sys.exit(1)
    jwt = sign_jwt()
    code, data = gh_request("POST", f"/app/installations/{inst_id}/access_tokens", jwt=jwt)
    if code != 201:
        print(f"🔴 获取安装令牌失败 HTTP {code}: {data}")
        sys.exit(1)
    print(data["token"])
    print(f"# 有效期至 {data.get('expires_at')} · 仓库: {data.get('repository_selection')}", file=sys.stderr)


def cmd_call(args):
    if len(args) < 2:
        print("用法: call <METHOD> <path> [json_body] [--allow-delete] [--no-sandbox]")
        sys.exit(1)
    method = args[0].upper()
    path = args[1] if args[1].startswith("/") else "/" + args[1]
    data = None
    if len(args) >= 3:
        data = json.loads(args[2])
    # ── P72 沙箱拦截（默认开启；--no-sandbox 仅调试用，须审计）──
    allow_delete = "--allow-delete" in args
    if "--no-sandbox" not in args:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lh_bot_sandbox import check as sandbox_check
        ok, reason = sandbox_check(method, path, allow_delete)
        if not ok:
            print(f"🔴 P2沙箱拦截: {method} {path} · {reason}")
            print("  如需放行: 显式审查后 --allow-delete / --no-sandbox（须写入审计）")
            sys.exit(1)
    else:
        print("⚠️ --no-sandbox 已启用（调试模式，须人工审计）")
    token = cmd_token_inner()
    code, resp = gh_request(method, path, token=token, data=data)
    if isinstance(resp, dict):
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        print(resp)
    if code >= 400:
        print(f"🔴 HTTP {code}", file=sys.stderr)
        sys.exit(1)


def cmd_token_inner():
    cfg = load_config()
    inst_id = cfg.get("installation_id")
    if not inst_id:
        print("🔴 未配置 installation_id，先运行: installations")
        sys.exit(1)
    jwt = sign_jwt()
    code, data = gh_request("POST", f"/app/installations/{inst_id}/access_tokens", jwt=jwt)
    if code != 201:
        print(f"🔴 获取安装令牌失败 HTTP {code}: {data}")
        sys.exit(1)
    return data["token"]


def cmd_webhook_verify(args):
    if len(args) < 2:
        print("用法: webhook-verify <payload_file> <signature> [secret]")
        print("      signature 形如: sha256=xxxxxxxx（来自 X-Hub-Signature-256 头）")
        sys.exit(1)
    payload = Path(args[0]).read_bytes()
    sig = args[1]
    secret = args[2] if len(args) >= 3 else load_config().get("webhook_secret", "")
    if not secret:
        print("🔴 未提供 webhook secret")
        sys.exit(1)
    expect = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    if hmac.compare_digest(expect, sig):
        print("✅ webhook 签名验证通过")
    else:
        print("🔴 webhook 签名不匹配!")
        print(f"  收到: {sig}")
        print(f"  期望: {expect}")
        sys.exit(1)


def cmd_doctor(_args):
    cfg = load_config()
    print("── 龍魂 GitHub App 配置体检 ──")
    if not cfg.get("app_id"):
        print("🟡 App ID       : 未配置（创建 App 后 init）")
    else:
        print(f"🟢 App ID       : {cfg['app_id']}")
    if not cfg.get("client_id"):
        print("🟡 Client ID    : 未配置")
    else:
        print(f"🟢 Client ID    : {cfg['client_id']}")
    if not cfg.get("slug"):
        print("🟡 Slug         : 未配置")
    else:
        print(f"🟢 Slug         : {cfg['slug']}")
    pem = Path(cfg.get("pem_path") or APP_DIR / "longhun-bot.pem")
    print("🟢 私钥存在     :" if pem.exists() else "🔴 私钥缺失     :", pem)
    print(f"🟢 安装ID        : {cfg.get('installation_id', '未配置')}")
    if cfg.get("app_id") and pem.exists() and cfg.get("installation_id"):
        print("\n全链路就绪 🟢 可运行: lh_github_app.py call GET /installation/repositories")


COMMANDS = {
    "init": cmd_init,
    "jwt": cmd_jwt,
    "installations": cmd_installations,
    "token": cmd_token,
    "call": cmd_call,
    "webhook-verify": cmd_webhook_verify,
    "doctor": cmd_doctor,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
