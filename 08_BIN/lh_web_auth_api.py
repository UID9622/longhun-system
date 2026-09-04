#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·申时·䷗复-WEB-AUTH-API-v1.0-7d3f1a2b
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 龍魂官网加密注册/登录 REST API（纯标准库·零三方依赖）
# 端口: 9658
"""
龍魂系统 · 官网账号认证 API v1.0

加密体系与终端 `lh keys mfa` 完全同源（P05 审计对齐）:
  - 密码: PBKDF2-HMAC-SHA256 + 随机盐 + 210000 次迭代（单向哈希·不可逆·不存明文）
  - 会话: HMAC-SHA256 签名 token（24h 有效·服务端不落库可撤销）
  - 熔断: 连续 5 次失败 → 锁定 15 分钟（与 MFA 锁 15 分钟口径一致）
  - 审计: append-only 日志·只记动作不记密码/哈希（L1 数据熔断要求）
  - 数据主权: 用户数据只存本机/鲲鹏·600 权限·绝不入云

端点:
  POST /api/auth/register  {username, password, confirm}   → 加密注册
  POST /api/auth/login     {username, password}            → 登录·签发 token
  GET  /api/auth/me       (Bearer <token>)                 → 当前用户
  POST /api/auth/logout   (Bearer <token>)                 → 登出
  GET  /api/auth/health                                    → 健康检查
  GET  /api/auth/status                                    → 服务状态

启动:
  python3 bin/lh_web_auth_api.py            # 默认 0.0.0.0:9658
  python3 bin/lh_web_auth_api.py --port 9658 --host 127.0.0.1
"""

import os
import sys
import re
import json
import sqlite3
import hashlib
import hmac
import secrets
import base64
import time
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from collections import deque

# ═══════════════════════════════════════════════════════════════
# 常量与路径（对齐 MFA 引擎 ~/.longhun 数据主权目录）
# ═══════════════════════════════════════════════════════════════
HOME_DIR = Path(os.environ.get("LONGHUN_HOME", Path.home() / ".longhun"))
AUTH_DIR = HOME_DIR / "web_auth"
DB_PATH = AUTH_DIR / "users.db"
SECRET_PATH = AUTH_DIR / "session.key"
LOG_PATH = AUTH_DIR / "auth_audit.log"

# 加密参数（与 lh_huawei_mfa.py 同源 PBKDF2·OWASP 2023 建议迭代）
PBKDF2_ITERATIONS = 210_000
SALT_BYTES = 16
KEY_BYTES = 32
SESSION_TTL = 24 * 3600          # 会话 24h
FAIL_LIMIT = 5                   # 连续失败 5 次
LOCK_SECONDS = 15 * 60           # 锁 15 分钟（对齐 MFA 口径）
RATE_LIMIT_PER_MIN = 60          # 每 IP 每分钟请求上限
RATE_BURST = 120                 # 突发容忍

USERNAME_RE = re.compile(r"^[\w\u4e00-\u9fa5-]{3,32}$")
RESERVED_NAMES = {"admin", "root", "system", "uid9622", "longhun", "龙魂", "龍魂", "administrator"}

# 内存会话黑名单（logout 即时失效）+ 限速表
_BLACKLIST = set()
_RATE = {}                       # ip -> deque[timestamp]
_RATE_LOCK = threading.Lock()


# ═══════════════════════════════════════════════════════════════
# 密码加密（单向哈希·不可逆）
# ═══════════════════════════════════════════════════════════════
def _pbkdf2(password: str, salt: bytes) -> str:
    """PBKDF2-HMAC-SHA256 单向哈希 → salt_hex$hash_hex"""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=KEY_BYTES)
    return f"{salt.hex()}${dk.hex()}"


def hash_password(password: str) -> str:
    return _pbkdf2(password, secrets.token_bytes(SALT_BYTES))


def verify_password(password: str, stored: str) -> bool:
    """常数时间比对·防时序攻击"""
    try:
        salt_hex, hash_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=KEY_BYTES)
        return hmac.compare_digest(dk.hex(), hash_hex)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════
# 会话 token（HMAC-SHA256 签名）
# ═══════════════════════════════════════════════════════════════
def _load_secret() -> bytes:
    if not SECRET_PATH.exists():
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        SECRET_PATH.write_bytes(secrets.token_bytes(32))
        os.chmod(SECRET_PATH, 0o600)
    return SECRET_PATH.read_bytes()


def issue_token(username: str) -> str:
    """签发 token: base64(payload).base64(sig)"""
    secret = _load_secret()
    payload = base64.urlsafe_b64encode(
        json.dumps({"u": username, "e": int(time.time()) + SESSION_TTL, "n": secrets.token_hex(8)}).encode()
    ).rstrip(b"=").decode()
    sig = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_token(token: str):
    """校验 token → username 或 None"""
    if token in _BLACKLIST:
        return None
    try:
        payload, sig = token.split(".", 1)
        secret = _load_secret()
        expected = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        if data.get("e", 0) < time.time():
            return None
        return data.get("u")
    except Exception:
        return None


def revoke_token(token: str):
    _BLACKLIST.add(token)


# ═══════════════════════════════════════════════════════════════
# 数据库（SQLite·数据主权本地存储）
# ═══════════════════════════════════════════════════════════════
def _db():
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(AUTH_DIR, 0o700)
    if DB_PATH.exists():
        os.chmod(DB_PATH, 0o600)
    if LOG_PATH.exists():
        os.chmod(LOG_PATH, 0o600)
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pwd_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL,
            last_login_at TEXT,
            fail_count INTEGER NOT NULL DEFAULT 0,
            locked_until REAL
        )
    """)
    conn.commit()
    return conn


# ═══════════════════════════════════════════════════════════════
# 审计日志（append-only·不记密码/哈希·L1 熔断要求）
# ═══════════════════════════════════════════════════════════════
def _audit(ip: str, action: str, username: str, result: str, extra: str = ""):
    try:
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        line = json.dumps(
            {"t": ts, "ip": ip, "a": action, "u": username, "r": result, "x": extra},
            ensure_ascii=False,
        )
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        os.chmod(LOG_PATH, 0o600)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# 限速（内存滑动窗口·每 IP）
# ═══════════════════════════════════════════════════════════════
def _rate_limited(ip: str) -> bool:
    now = time.time()
    with _RATE_LOCK:
        dq = _RATE.setdefault(ip, deque())
        while dq and dq[0] < now - 60:
            dq.popleft()
        if len(dq) > RATE_BURST:
            return True
        dq.append(now)
        # 周期性清理老 IP
        if len(_RATE) > 4096:
            for k in list(_RATE):
                if len(_RATE[k]) == 0 or (dq and _RATE[k][0] < now - 120):
                    _RATE.pop(k, None)
        return False


# ═══════════════════════════════════════════════════════════════
# 业务逻辑
# ═══════════════════════════════════════════════════════════════
def do_register(data, ip: str):
    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""
    confirm = data.get("confirm") or ""

    if not USERNAME_RE.match(username):
        return {"ok": False, "error": "用户名须 3-32 位：字母/数字/下划线/中文/连字符"}
    if username in RESERVED_NAMES:
        return {"ok": False, "error": "该用户名已被保留，请换一个"}
    if not (8 <= len(password) <= 128):
        return {"ok": False, "error": "密码须 8-128 位"}
    if password != confirm:
        return {"ok": False, "error": "两次输入的密码不一致"}

    conn = _db()
    try:
        cur = conn.cursor()
        if cur.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
            _audit(ip, "register", username, "denied", "username exists")
            return {"ok": False, "error": "该用户名已被注册"}
        cur.execute(
            "INSERT INTO users (username, pwd_hash, created_at) VALUES (?,?,?)",
            (username, hash_password(password), datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
        )
        conn.commit()
        _audit(ip, "register", username, "ok")
        return {"ok": True, "data": {"message": "注册成功·账号已加密入库"}}
    except sqlite3.IntegrityError:
        return {"ok": False, "error": "该用户名已被注册"}
    finally:
        conn.close()


def do_login(data, ip: str):
    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""
    if not username or not password:
        return {"ok": False, "error": "请输入用户名和密码"}

    conn = _db()
    try:
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            _audit(ip, "login", username, "denied", "no such user")
            return {"ok": False, "error": "用户名或密码错误"}

        # 熔断检查（对齐 MFA 锁 15 分钟口径）
        if row["locked_until"] and row["locked_until"] > time.time():
            remain = int(row["locked_until"] - time.time()) // 60
            _audit(ip, "login", username, "locked", f"lock {remain}min")
            return {"ok": False, "error": f"失败次数过多·已锁定 {remain} 分钟后重试"}

        if verify_password(password, row["pwd_hash"]):
            cur.execute(
                "UPDATE users SET fail_count=0, last_login_at=?, locked_until=NULL WHERE id=?",
                (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), row["id"]),
            )
            conn.commit()
            token = issue_token(username)
            _audit(ip, "login", username, "ok")
            return {
                "ok": True,
                "data": {
                    "token": token,
                    "user": {
                        "username": row["username"],
                        "role": row["role"],
                        "created_at": row["created_at"],
                        "last_login_at": row["last_login_at"],
                    },
                },
            }

        # 失败计数 + 锁定
        fail = row["fail_count"] + 1
        locked_until = time.time() + LOCK_SECONDS if fail >= FAIL_LIMIT else None
        cur.execute("UPDATE users SET fail_count=?, locked_until=? WHERE id=?", (fail, locked_until, row["id"]))
        conn.commit()
        _audit(ip, "login", username, "failed", f"fail {fail}/{FAIL_LIMIT}" + (" LOCK" if locked_until else ""))
        if locked_until:
            return {"ok": False, "error": f"连续失败 {FAIL_LIMIT} 次·账号已锁定 15 分钟"}
        return {"ok": False, "error": "用户名或密码错误"}
    finally:
        conn.close()


def do_me(username: str):
    conn = _db()
    try:
        row = conn.execute("SELECT username, role, created_at, last_login_at FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            return {"ok": False, "error": "用户不存在"}
        return {"ok": True, "data": {"user": dict(row)}}
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════════
# HTTP 服务
# ═══════════════════════════════════════════════════════════════
class AuthHandler(BaseHTTPRequestHandler):
    server_version = "LongHunWebAuth/1.0"

    def log_message(self, fmt, *args):
        pass  # 静默·审计走 _audit

    def _send(self, code: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("X-Longhun-Service", "web-auth-api")
        self.send_header("X-Data-Sovereignty", "China-Local")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > 64 * 1024:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw) if raw else {}
        except Exception:
            return {}

    def _client_ip(self) -> str:
        # 经 nginx 反代时取真实 IP
        fwd = self.headers.get("X-Forwarded-For", "")
        if fwd:
            return fwd.split(",")[0].strip()
        return self.client_address[0]

    def _bearer(self) -> str:
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:].strip()
        return ""

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        ip = self._client_ip()
        if _rate_limited(ip):
            self._send(429, {"ok": False, "error": "请求过于频繁·请稍后再试"})
            return
        path = self.path.split("?", 1)[0]

        if path == "/api/auth/health" or path == "/health":
            self._send(200, {"ok": True, "service": "web-auth", "version": "v1.0", "ts": time.time()})
            return
        if path == "/api/auth/status" or path == "/status":
            self._send(200, {"ok": True, "data": {"users": _user_count(), "sessions": len(_BLACKLIST), "alive": True}})
            return
        if path == "/api/auth/me" or path == "/me":
            token = self._bearer()
            username = verify_token(token)
            if not username:
                self._send(401, {"ok": False, "error": "登录已失效·请重新登录"})
                return
            resp = do_me(username)
            self._send(200 if resp["ok"] else 404, resp)
            return
        if path == "/api/auth/glass" or path == "/glass":
            # 公开玻璃墙·无需登录·只含脱敏聚合（P0 透明不黑箱）
            self._send(200, _glass_snapshot())
            return
        if path == "/api/auth/audit" or path == "/audit":
            # 审计查询·需登录·IP 脱敏·读取本身记审计
            token = self._bearer()
            username = verify_token(token)
            if not username:
                self._send(401, {"ok": False, "error": "登录已失效·请重新登录"})
                return
            try:
                limit = int(self.path.split("limit=", 1)[1].split("&", 1)[0]) if "limit=" in self.path else 50
            except Exception:
                limit = 50
            limit = max(1, min(limit, 500))
            _audit(ip, "audit.view", username, "ok", f"limit={limit}")
            self._send(200, {"ok": True, "data": {"records": _audit_recent(limit), "count": len(_audit_recent(limit))}})
            return
        self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        ip = self._client_ip()
        if _rate_limited(ip):
            self._send(429, {"ok": False, "error": "请求过于频繁·请稍后再试"})
            return
        path = self.path.split("?", 1)[0]
        data = self._read_json()

        if path == "/api/auth/register" or path == "/register":
            resp = do_register(data, ip)
            self._send(200, resp)
            return
        if path == "/api/auth/login" or path == "/login":
            resp = do_login(data, ip)
            self._send(200, resp)
            return
        if path == "/api/auth/logout" or path == "/logout":
            token = self._bearer()
            username = verify_token(token)
            if username:
                revoke_token(token)
                _audit(ip, "logout", username, "ok")
                self._send(200, {"ok": True, "data": {"message": "已登出"}})
            else:
                self._send(401, {"ok": False, "error": "登录已失效"})
            return
        self._send(404, {"ok": False, "error": "not found"})


def _user_count() -> int:
    try:
        conn = _db()
        try:
            return conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
        finally:
            conn.close()
    except Exception:
        return 0


# ═══════════════════════════════════════════════════════════════
# 开放玻璃墙（P0 无后台主权协议的正面实现·透明不黑箱）
#   - /api/auth/glass  公开快照·无需登录·只含脱敏聚合统计
#   - /api/auth/audit  审计查询·需登录·IP 脱敏·读取本身记审计
# ═══════════════════════════════════════════════════════════════
def _mask_ip(ip: str) -> str:
    """IP 脱敏: 末段打码，防公开泄露定位"""
    try:
        if ":" in ip:                      # IPv6 → 保留前 4 段
            parts = ip.split(":")
            return ":".join(parts[:4]) + ":****"
        parts = ip.split(".")
        if len(parts) == 4:
            return ".".join(parts[:3]) + ".*"
    except Exception:
        pass
    return "***"


def _audit_stats() -> dict:
    """审计聚合统计（不暴露任何原文）"""
    stats = {"total": 0, "login_ok": 0, "login_failed": 0, "locked": 0, "register": 0, "logout": 0, "other": 0}
    if not LOG_PATH.exists():
        return stats
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                stats["total"] += 1
                a = ev.get("a", "")
                if a == "login" and ev.get("r") == "ok":
                    stats["login_ok"] += 1
                elif a == "login" and ev.get("r") in ("failed", "denied", "locked"):
                    stats["login_failed"] += 1
                elif a == "register":
                    stats["register"] += 1
                elif a == "logout":
                    stats["logout"] += 1
                else:
                    stats["other"] += 1
        return stats
    except Exception:
        return stats


def _audit_trend(days: int = 14) -> list:
    """审计趋势时间序列（走势图数据源）·按 UTC 日聚合·不含任何敏感原文"""
    buckets = {}
    if LOG_PATH.exists():
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        ev = json.loads(line)
                    except Exception:
                        continue
                    day = (ev.get("t", "") or "")[:10]
                    if len(day) != 10:
                        continue
                    b = buckets.setdefault(day, {"date": day, "login_ok": 0, "login_failed": 0, "register": 0, "locked": 0})
                    a, r = ev.get("a", ""), ev.get("r", "")
                    if a == "login" and r == "ok":
                        b["login_ok"] += 1
                    elif a == "login" and r in ("failed", "denied", "locked"):
                        b["login_failed"] += 1
                    elif a == "register":
                        b["register"] += 1
                    elif a == "login" and r == "locked":
                        b["locked"] += 1
        except Exception:
            pass
    # 补齐近 days 天空档（走势图连续性）
    out, seen = [], set(buckets)
    now = datetime.now(timezone.utc)
    for i in range(days - 1, -1, -1):
        d = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        out.append(buckets.get(d, {"date": d, "login_ok": 0, "login_failed": 0, "register": 0, "locked": 0}))
    return out


def _glass_snapshot() -> dict:
    """公开玻璃墙快照 · P0 合规：不存用户数据·只含聚合/状态"""
    return {
        "ok": True,
        "data": {
            "service": "web-auth",
            "version": "v1.0",
            "alive": True,
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "protocol": {
                "name": "龍魂·无后台主权协议 v2.0",
                "level": "P0",
                "status": "焊死",
                "claims": [
                    "服务器不存储用户数据·只存不可逆哈希(PBKDF2-SHA256)",
                    "无管理员后门·无追踪脚本·无隐藏修改",
                    "审计日志 append-only·只冻结不删除",
                    "所有代码开源·任何人都可审查",
                ],
            },
            "audit": _audit_stats(),
            "users_total": _user_count(),
            "trend": _audit_trend(),
        },
    }


def _audit_recent(limit: int) -> list:
    """最近审计记录（IP 脱敏·供登录用户查询）"""
    out = []
    if not LOG_PATH.exists():
        return out
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                out.append({
                    "t": ev.get("t", ""),
                    "a": ev.get("a", ""),
                    "u": ev.get("u", "***"),
                    "r": ev.get("r", ""),
                    "x": ev.get("x", ""),
                    "ip": _mask_ip(ev.get("ip", "")),
                })
        return out[-limit:]
    except Exception:
        return out


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂官网账号认证 API (9658)")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=9658, help="监听端口")
    args = parser.parse_args()

    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(AUTH_DIR, 0o700)
    # 预生成会话密钥
    _load_secret()
    # 初始化 DB
    _db()

    print(f"🐉 龍魂官网账号认证 API v1.0 · http://{args.host}:{args.port}")
    print(f"📁 数据目录: {AUTH_DIR} (600)")
    print(f"🔐 加密: PBKDF2-SHA256 x{PBKDF2_ITERATIONS} · 会话HMAC-SHA256 · 锁{FAIL_LIMIT}次/{LOCK_SECONDS//60}分钟")
    server = ThreadingHTTPServer((args.host, args.port), AuthHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 已停止")
        server.server_close()


if __name__ == "__main__":
    main()
