#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·乙巳·巳时·䷋否-NOTION-OAUTH-EXCHANGE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂 · Notion OAuth 授权码换取 access_token

流程: 生成授权链接 → 老大浏览器授权 → 本地回调捕获 code → 换 access_token → 存 vault

用法:
  python3 bin/lh_notion_oauth.py            # 一键: 起回调服务 + 打印授权链接
  python3 bin/lh_notion_oauth.py --port 9876
"""
import argparse
import base64
import json
import os
import socket
import sys
import threading
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTHORIZE_URL = "https://api.notion.com/v1/oauth/authorize"
TOKEN_URL = "https://api.notion.com/v1/oauth/token"

for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"


def _vault(sub, key):
    r = os.popen(f"python3 bin/lh_vault.py {sub} {key}").read().strip()
    return r


def load_oauth_creds():
    client_id = os.environ.get("NOTION_OAUTH_CLIENT_ID") or _vault("get", "notion-oauth-client-id")
    client_secret = os.environ.get("NOTION_OAUTH_CLIENT_SECRET") or _vault("get", "notion-oauth-client-secret")
    if not client_id or not client_secret:
        print("❌ 未找到 OAuth 凭据（vault: notion-oauth-client-id/secret）")
        sys.exit(1)
    return client_id.strip(), client_secret.strip()


def exchange_code(code, client_id, client_secret, redirect_uri):
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }).encode()
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()[:300]}


def main():
    ap = argparse.ArgumentParser(description="Notion OAuth 授权码换 token")
    ap.add_argument("--port", type=int, default=9876)
    ap.add_argument("--wait", type=int, default=600, help="等待回调秒数(默认600)")
    args = ap.parse_args()

    client_id, client_secret = load_oauth_creds()
    redirect_uri = f"http://localhost:{args.port}/callback"
    code_holder = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.urlparse(self.path)
            if q.path == "/callback":
                params = urllib.parse.parse_qs(q.query)
                code_holder["code"] = params.get("code", [""])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = "<h3>授权成功 ✅ 请关闭此页</h3>" if code_holder["code"] else "<h3>未获取到 code ❌</h3>"
                self.wfile.write(html.encode())
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, *a):
            pass

    # 双栈监听: localhost 可能解析为 ::1 (IPv6)，故绑定所有接口
    class DualStackServer(HTTPServer):
        address_family = socket.AF_INET6
        def server_bind(self):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            super().server_bind()
    try:
        server = DualStackServer(("::", args.port), Handler)
    except OSError:
        server = HTTPServer(("0.0.0.0", args.port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    auth_url = (f"{AUTHORIZE_URL}?client_id={client_id}"
                f"&response_type=code&owner=user&redirect_uri={urllib.parse.quote(redirect_uri, safe='')}")
    print("=" * 60)
    print("👉 请老大在浏览器打开以下链接并点击「允许/Authorize」：")
    print()
    print(f"  {auth_url}")
    print()
    print(f"等待回调 (127.0.0.1:{args.port}/callback) ... (最多 {args.wait} 秒)", flush=True)
    deadline = args.wait
    while deadline > 0:
        if code_holder.get("code"):
            break
        deadline -= 1
        import time; time.sleep(1)
    server.shutdown()

    if not code_holder.get("code"):
        print("❌ 超时未收到授权回调")
        sys.exit(2)

    code = code_holder["code"]
    print(f"✅ 收到授权 code (len={len(code)})")
    tok = exchange_code(code, client_id, client_secret, redirect_uri)
    if "access_token" not in tok:
        print(f"❌ 换 token 失败: {json.dumps(tok, ensure_ascii=False)[:300]}")
        sys.exit(3)

    at = tok["access_token"]
    workspace = tok.get("workspace_name", "?")
    workspace_id = tok.get("workspace_id", "?")
    # 保存（不在 stdout 打印完整 token）
    r1 = os.popen(f'python3 bin/lh_vault.py put notion-access-token --value "{at}" --note "Notion OAuth access_token workspace={workspace}"').read().strip()
    r2 = os.popen(f'python3 bin/lh_vault.py put notion-workspace-id --value "{workspace_id}" --note "Notion workspace id"').read().strip()
    print(f"✅ 换取成功 · workspace: {workspace} ({workspace_id})")
    print(f"✅ 已存入 vault: notion-access-token  (前缀 {at[:10]}...)")
    print(f"   vault: {r1.splitlines()[-1] if r1 else ''}")
    print("")
    print("👉 下一步: 用新 token 测试花名册数据库 →")
    print("   python3 - <<'EOF' 或直接告诉我'测试'")
    print(f"   curl -H 'Authorization: Bearer {at[:10]}...' https://api.notion.com/v1/databases/4cf99c3e7a014e919fdab705ceb4cbc4")


if __name__ == "__main__":
    main()
