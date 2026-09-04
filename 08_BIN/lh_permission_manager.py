#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 权限管理引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-PERMISSION-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
功能: 基础RBAC — 用户/角色/权限管理（SQLite本地存储）
用法:
  lh 权限 --add-user <用户名> [--role admin|user|auditor] [--password ...]
  lh 权限 --list-users
  lh 权限 --list-roles
  lh 权限 --grant <用户> --role <角色>
  lh 权限 --check <用户> --perm <权限名>
安全: 密码SHA-256哈希存储·操作日志append-only·不存储明文
"""

import sqlite3
import hashlib
import secrets
import argparse
import json
import time
from pathlib import Path
from getpass import getpass
from typing import List, Optional, Tuple

# ── 数据库路径 ──
DB_PATH = Path.home() / ".longhun" / "permissions.db"
AUDIT_LOG = Path.home() / ".longhun" / "perm_audit.jsonl"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── 默认角色定义 ──
DEFAULT_ROLES = {
    "admin":    ["*"],                                          # 全权限
    "user":     ["read", "execute", "audit_view"],              # 普通用户
    "auditor":  ["read", "audit_view", "audit_write"],          # 审计员
    "viewer":   ["read"],                                       # 只读
}

# ── 权限清单（与系统功能对应） ──
PERMISSIONS = ["*", "read", "execute", "deploy", "admin_users",
               "audit_view", "audit_write", "audit_approve",
               "gpg_sign", "config_edit", "alert_send"]


# ═══════════════════════════════════════════════════
#  数据库初始化
# ═══════════════════════════════════════════════════

def init_db():
    """初始化数据库和默认角色"""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username   TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role       TEXT NOT NULL DEFAULT 'user',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            last_login TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role        TEXT PRIMARY KEY,
            permissions TEXT NOT NULL,  -- JSON array
            description TEXT DEFAULT ''
        )
    """)

    # 填充默认角色（不覆盖已有）
    for role_name, perms in DEFAULT_ROLES.items():
        cur.execute(
            "INSERT OR IGNORE INTO roles (role, permissions, description) VALUES (?, ?, ?)",
            (role_name, json.dumps(perms, ensure_ascii=False),
             f"系统内置·{role_name}角色")
        )

    conn.commit()
    conn.close()


def audit_log(action: str, detail: str):
    """记录权限操作审计日志"""
    entry = {
        "timestamp": time.time(),
        "iso": time.strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════
#  用户管理
# ═══════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """SHA-256哈希密码"""
    salt = "longhun_salt_v1"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def add_user(username: str, password: Optional[str] = None,
             role: str = "user") -> bool:
    """添加用户"""
    init_db()

    if not password:
        password = getpass(f"为用户 {username} 设置密码: ")
        confirm = getpass("确认密码: ")
        if password != confirm:
            print("❌ 两次密码不一致")
            return False
    if len(password) < 6:
        print("❌ 密码至少6位")
        return False

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # 验证角色存在
    cur.execute("SELECT role FROM roles WHERE role=?", (role,))
    if not cur.fetchone():
        print(f"⚠️ 角色 '{role}' 不存在，将创建默认权限")
        cur.execute(
            "INSERT OR IGNORE INTO roles (role, permissions) VALUES (?, '[\"read\",\"execute\"]')",
            (role,)
        )

    pwd_hash = hash_password(password)
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, pwd_hash, role)
        )
        conn.commit()
        audit_log("user_add", f"添加用户 {username}，角色 {role}")
        print(f"✅ 用户 {username} 已创建（角色: {role}）")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ 用户 {username} 已存在")
        return False
    finally:
        conn.close()


def list_users():
    """列出所有用户"""
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT username, role, created_at, last_login FROM users ORDER BY created_at")
    rows = cur.fetchall()
    if not rows:
        print("📋 暂无注册用户")
    else:
        print("╔══════════════════════════════════════════════════╗")
        print("║  📋 龍魂 · 用户列表                               ║")
        print("╠══════════════════════════════════════════════════╣")
        for row in rows:
            last = row[3] or "从未登录"
            print(f"  {row[0]:<18s} {row[1]:<10s} {row[2]:<20s} {last}")
    conn.close()


def list_roles():
    """列出所有角色"""
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT role, permissions, description FROM roles ORDER BY role")
    rows = cur.fetchall()
    print("╔══════════════════════════════════════════════════╗")
    print("║  🎭 龍魂 · 角色清单                               ║")
    print("╠══════════════════════════════════════════════════╣")
    for row in rows:
        perms = json.loads(row[1])
        desc = row[2] or ""
        print(f"  {row[0]:<12s} {'·'.join(perms):<30s} {desc}")
    print("╚══════════════════════════════════════════════════╝")
    conn.close()


def grant_role(username: str, role: str) -> bool:
    """修改用户角色"""
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("SELECT role FROM roles WHERE role=?", (role,))
    if not cur.fetchone():
        print(f"❌ 角色 '{role}' 不存在")
        conn.close()
        return False

    cur.execute("UPDATE users SET role=? WHERE username=?", (role, username))
    if cur.rowcount == 0:
        print(f"❌ 用户 '{username}' 不存在")
        conn.close()
        return False

    conn.commit()
    audit_log("role_grant", f"授予 {username} 角色 {role}")
    print(f"✅ {username} 的角色已更新为 {role}")
    conn.close()
    return True


def check_permission(username: str, permission: str) -> bool:
    """检查用户是否有某权限"""
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("SELECT role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if not row:
        print(f"❌ 用户 '{username}' 不存在")
        conn.close()
        return False

    role = row[0]
    cur.execute("SELECT permissions FROM roles WHERE role=?", (role,))
    role_row = cur.fetchone()
    conn.close()

    if not role_row:
        print(f"⚠️ 角色 '{role}' 无定义")
        return False

    perms = json.loads(role_row[0])
    has = "*" in perms or permission in perms
    return has


# ═══════════════════════════════════════════════════
#  安全：用户认证
# ═══════════════════════════════════════════════════

def verify_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    """
    验证用户密码。
    返回 (是否通过, 角色名)。
    """
    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False, None

    expected_hash = row[0]
    actual_hash = hash_password(password)
    if not secrets.compare_digest(expected_hash, actual_hash):
        return False, None

    # 更新最后登录时间
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_login=datetime('now','localtime') WHERE username=?",
                (username,))
    conn.commit()
    conn.close()

    return True, row[1]


# ═══════════════════════════════════════════════════
#  CLI入口
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·权限管理 — 基础RBAC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 权限 --add-user zhangsan --role user
  lh 权限 --list-users
  lh 权限 --list-roles
  lh 权限 --grant zhangsan --role admin
  lh 权限 --check zhangsan --perm deploy
        """
    )
    parser.add_argument("--add-user", metavar="USERNAME", help="添加用户")
    parser.add_argument("--password", help="密码（不提供则交互输入）")
    parser.add_argument("--role", default="user", help="角色 (默认: user)")
    parser.add_argument("--list-users", action="store_true", help="列出所有用户")
    parser.add_argument("--list-roles", action="store_true", help="列出所有角色")
    parser.add_argument("--grant", metavar="USERNAME", help="修改用户角色（需配合--role）")
    parser.add_argument("--check", metavar="USERNAME", help="检查用户权限（需配合--perm）")
    parser.add_argument("--perm", metavar="PERM", help="权限名")
    parser.add_argument("--init", action="store_true", help="初始化数据库")

    args = parser.parse_args()

    if args.init:
        init_db()
        print("✅ 权限数据库已初始化")
        print(f"   路径: {DB_PATH}")
        return

    if args.list_users:
        list_users()
        return

    if args.list_roles:
        list_roles()
        return

    if args.add_user:
        add_user(args.add_user, args.password, args.role)
        return

    if args.grant and args.role:
        grant_role(args.grant, args.role)
        return

    if args.check and args.perm:
        has = check_permission(args.check, args.perm)
        if has:
            print(f"✅ {args.check} 拥有权限 '{args.perm}'")
        else:
            print(f"🔴 {args.check} 无权限 '{args.perm}'")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
