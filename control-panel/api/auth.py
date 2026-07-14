#!/usr/bin/env python3
"""
🐉 龍魂操作台 · 认证模块 v1.0
JWT 登录认证 + 管理员密码管理
"""
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Optional

import jwt

# ── 配置 ──
CONFIG_DIR = Path(__file__).resolve().parent.parent
ADMIN_FILE = CONFIG_DIR / ".admin.json"
JWT_SECRET = os.environ.get("LONGHUN_JWT_SECRET", "longhun-uid9622-admin-panel-secret-v1")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = int(os.environ.get("LONGHUN_JWT_EXPIRE_HOURS", "24"))


def _hash_password(password: str, salt: str = "") -> tuple[str, str]:
    """SHA-256 + salt 哈希密码，返回 (hash, salt)"""
    if not salt:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return h.hex(), salt


def _init_admin() -> dict:
    """初始化或读取管理员配置"""
    if ADMIN_FILE.exists():
        try:
            return json.loads(ADMIN_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    # 默认管理员账号
    default_password = "longhun9622"
    pw_hash, salt = _hash_password(default_password)
    admin_config = {
        "username": "admin",
        "password_hash": pw_hash,
        "salt": salt,
        "created_at": int(time.time()),
        "last_login": 0,
        "login_count": 0,
        "must_change_password": True,  # 首次登录强制改密码
    }
    ADMIN_FILE.write_text(json.dumps(admin_config, indent=2, ensure_ascii=False), encoding="utf-8")
    os.chmod(ADMIN_FILE, 0o600)  # 仅 owner 可读写
    return admin_config


def _save_admin(config: dict):
    """保存管理员配置"""
    ADMIN_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    os.chmod(ADMIN_FILE, 0o600)


def verify_password(username: str, password: str) -> tuple[bool, Optional[dict]]:
    """验证用户名密码，返回 (成功, 管理员配置)"""
    config = _init_admin()
    if username != config.get("username", "admin"):
        return False, None
    
    pw_hash, _ = _hash_password(password, config.get("salt", ""))
    if not hmac.compare_digest(pw_hash, config.get("password_hash", "")):
        return False, None
    
    # 更新登录记录
    config["last_login"] = int(time.time())
    config["login_count"] = config.get("login_count", 0) + 1
    _save_admin(config)
    return True, config


def change_password(old_password: str, new_password: str) -> tuple[bool, str]:
    """修改管理员密码"""
    config = _init_admin()
    
    # 验证旧密码
    old_hash, _ = _hash_password(old_password, config.get("salt", ""))
    if not hmac.compare_digest(old_hash, config.get("password_hash", "")):
        return False, "旧密码错误"
    
    # 新密码强度检查
    if len(new_password) < 8:
        return False, "新密码至少8位"
    
    # 更新密码
    new_hash, new_salt = _hash_password(new_password)
    config["password_hash"] = new_hash
    config["salt"] = new_salt
    config["must_change_password"] = False
    _save_admin(config)
    return True, "密码修改成功"


def create_token(username: str) -> str:
    """生成 JWT 登录令牌"""
    now = int(time.time())
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + JWT_EXPIRE_HOURS * 3600,
        "jti": secrets.token_hex(8),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """验证 JWT 令牌，返回 payload 或 None"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_admin_info() -> dict:
    """获取管理员信息（不含密码哈希）"""
    config = _init_admin()
    return {
        "username": config.get("username", "admin"),
        "created_at": config.get("created_at", 0),
        "last_login": config.get("last_login", 0),
        "login_count": config.get("login_count", 0),
        "must_change_password": config.get("must_change_password", False),
    }
