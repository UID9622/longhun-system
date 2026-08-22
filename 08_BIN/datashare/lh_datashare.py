#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-DATASHARE-CTRL-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · DataShare 权限控制机制 v1.1
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-DATASHARE-CTRL-UID9622

核心思想: 共享必须可控，授权必须精确，操作必须可追溯。
DataShare 不是"开门"，是"开一个精确的洞"。

功能:
  1. 授权令牌签发 (JWT + 龍魂DNA)
  2. 权限范围精确控制 (Scope)
  3. 有效期管理 (TTL)
  4. 操作黑白名单 (Allow/Deny)
  5. 全链路审计追踪 (append-only)
  6. 鲲鹏服务器适配 (统一字体)

v1.1 修复:
  - verify_token 中 conn 关闭后复用导致崩溃的 bug
  - MD5 替换为 SHA256 (禁MD5铁律)
  - JWT_SECRET 不硬编码默认值，改从密钥文件读取，无则自动生成
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
import logging

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 密钥文件: ~/.longhun/datashare/secret.key (600 权限)
DATA_DIR = Path.home() / ".longhun" / "datashare"
SECRET_FILE = DATA_DIR / "secret.key"


def _load_or_create_secret() -> str:
    """读取密钥文件，无则生成 32 字节随机密钥。密钥永不硬编码、永不入云。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text().strip()
    secret = hashlib.sha256(os.urandom(32)).hexdigest()
    SECRET_FILE.write_text(secret)
    os.chmod(SECRET_FILE, 0o600)
    return secret


JWT_SECRET = os.environ.get("DATASHARE_JWT_SECRET") or _load_or_create_secret()


def generate_dna(suffix: str = "DATASHARE") -> str:
    h = hashlib.sha256(f"{suffix}{time.time()}{os.urandom(4)}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{suffix}-{h}-{UID}"


def _short_hash(*parts) -> str:
    """SHA256 短哈希 (替代 MD5，遵禁MD5铁律)"""
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:8]


# ============================================================
# 日志
# ============================================================

LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"datashare_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("datashare")

# ============================================================
# 数据模型
# ============================================================


@dataclass
class DataShareToken:
    """数据共享授权令牌"""
    token_id: str
    owner: str                          # 数据所有者
    grantee: str                        # 被授权者
    scope: List[str]                    # 权限范围
    ttl: int                            # 有效期(秒)
    allow: List[str]                    # 允许的操作
    deny: List[str]                     # 禁止的操作
    dna: str = field(default_factory=lambda: generate_dna("TOKEN"))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expires_at: str = ""
    status: str = "active"              # active | revoked | expired
    last_used: str = ""

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        expiry = datetime.fromisoformat(self.expires_at)
        return datetime.now() > expiry

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_jwt(self) -> str:
        if not JWT_AVAILABLE:
            raise RuntimeError("缺少 pyjwt 依赖: pip install pyjwt")
        payload = {
            "token_id": self.token_id,
            "owner": self.owner,
            "grantee": self.grantee,
            "scope": self.scope,
            "ttl": self.ttl,
            "allow": self.allow,
            "deny": self.deny,
            "dna": self.dna,
            "exp": int(time.time()) + self.ttl
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


@dataclass
class DataAccessRecord:
    """数据访问记录"""
    record_id: str
    token_id: str
    grantee: str
    operation: str
    resource: str
    allowed: bool
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    dna: str = field(default_factory=lambda: generate_dna("ACCESS"))


# ============================================================
# DataShare 核心引擎
# ============================================================


class DataShareEngine:
    """DataShare 权限控制引擎"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (DATA_DIR / "datashare.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn

    def _init_db(self):
        """初始化数据库"""
        conn = self._connect()
        cur = conn.cursor()

        # 令牌表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS datashare_tokens (
                token_id TEXT PRIMARY KEY,
                owner TEXT NOT NULL,
                grantee TEXT NOT NULL,
                scope TEXT NOT NULL,
                ttl INTEGER,
                allow TEXT,
                deny TEXT,
                dna TEXT,
                created_at TEXT,
                expires_at TEXT,
                status TEXT DEFAULT 'active',
                last_used TEXT
            )
        """)

        # 访问记录表 (append-only 审计)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS datashare_audit (
                record_id TEXT PRIMARY KEY,
                token_id TEXT,
                grantee TEXT,
                operation TEXT,
                resource TEXT,
                allowed INTEGER,
                reason TEXT,
                timestamp TEXT,
                dna TEXT
            )
        """)

        # 索引
        cur.execute("CREATE INDEX IF NOT EXISTS idx_token_owner ON datashare_tokens(owner)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_token_grantee ON datashare_tokens(grantee)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_token ON datashare_audit(token_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON datashare_audit(timestamp)")

        conn.commit()
        conn.close()
        logger.info("DataShare 数据库初始化完成")

    # ============================================================
    # 1. 授权签发
    # ============================================================

    def issue_token(self, owner: str, grantee: str, scope: List[str],
                    ttl: int = 3600, allow: List[str] = None,
                    deny: List[str] = None) -> DataShareToken:
        """签发授权令牌"""
        token_id = f"DS-{int(time.time())}-{_short_hash(owner, grantee, time.time())}"
        expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()

        token = DataShareToken(
            token_id=token_id,
            owner=owner,
            grantee=grantee,
            scope=scope,
            ttl=ttl,
            allow=allow or [],
            deny=deny or [],
            expires_at=expires_at
        )

        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO datashare_tokens
            (token_id, owner, grantee, scope, ttl, allow, deny, dna, created_at, expires_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            token.token_id,
            token.owner,
            token.grantee,
            json.dumps(token.scope),
            token.ttl,
            json.dumps(token.allow),
            json.dumps(token.deny),
            token.dna,
            token.created_at,
            token.expires_at,
            "active"
        ))
        conn.commit()
        conn.close()

        logger.info(f"✅ 签发令牌: {token.token_id} (授权给 {grantee})")
        return token

    # ============================================================
    # 2. 授权验证
    # ============================================================

    def _get_token_row(self, token_id: str) -> Optional[tuple]:
        """查令牌状态行，返回 (status, expires_at) 或 None"""
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT status, expires_at FROM datashare_tokens WHERE token_id = ?", (token_id,))
            return cur.fetchone()
        finally:
            conn.close()

    def _mark_token(self, token_id: str, status: str) -> None:
        """更新令牌状态"""
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE datashare_tokens SET status = ? WHERE token_id = ?", (status, token_id))
            conn.commit()
        finally:
            conn.close()

    def _touch_token(self, token_id: str) -> None:
        """更新最后使用时间"""
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE datashare_tokens SET last_used = ? WHERE token_id = ?",
                        (datetime.now().isoformat(), token_id))
            conn.commit()
        finally:
            conn.close()

    def verify_token(self, token_jwt: str) -> Dict:
        """验证JWT令牌"""
        if not JWT_AVAILABLE:
            return {"valid": False, "reason": "缺少 pyjwt 依赖"}
        try:
            payload = jwt.decode(token_jwt, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"valid": False, "reason": "JWT签名已过期"}
        except jwt.InvalidTokenError:
            return {"valid": False, "reason": "无效的JWT令牌"}

        token_id = payload.get("token_id")
        row = self._get_token_row(token_id)
        if not row:
            return {"valid": False, "reason": "令牌不存在"}

        status, expires_at = row
        if status == "revoked":
            return {"valid": False, "reason": "令牌已被撤销"}

        # 过期检查（数据库行 + JWT exp 双保险）
        expired = False
        if status == "expired":
            expired = True
        elif expires_at:
            try:
                expired = datetime.fromisoformat(expires_at) < datetime.now()
            except ValueError:
                expired = False
        if expired:
            self._mark_token(token_id, "expired")
            return {"valid": False, "reason": "令牌已过期"}

        self._touch_token(token_id)

        return {
            "valid": True,
            "token_id": token_id,
            "owner": payload.get("owner"),
            "grantee": payload.get("grantee"),
            "scope": payload.get("scope", []),
            "allow": payload.get("allow", []),
            "deny": payload.get("deny", [])
        }

    # ============================================================
    # 3. 权限检查
    # ============================================================

    def check_permission(self, token_jwt: str, operation: str, resource: str) -> Dict:
        """检查权限"""
        verify_result = self.verify_token(token_jwt)
        if not verify_result["valid"]:
            self._log_access(
                token_id=verify_result.get("token_id", "unknown"),
                grantee=verify_result.get("grantee", "unknown"),
                operation=operation,
                resource=resource,
                allowed=False,
                reason=verify_result["reason"]
            )
            return {
                "allowed": False,
                "reason": verify_result["reason"],
                "dna": generate_dna("DENY")
            }

        token_id = verify_result["token_id"]
        scope = verify_result["scope"]
        allow_list = verify_result["allow"]
        deny_list = verify_result["deny"]

        # 资源是否在授权范围内
        resource_in_scope = any(
            resource.startswith(item) or item == "*" for item in scope
        )
        if not resource_in_scope:
            self._log_access(token_id, verify_result["grantee"], operation, resource,
                             False, f"资源不在授权范围内: {resource}")
            return {"allowed": False, "reason": f"资源不在授权范围内: {resource}", "dna": generate_dna("DENY")}

        # 操作白名单
        if allow_list and operation not in allow_list:
            self._log_access(token_id, verify_result["grantee"], operation, resource,
                             False, f"操作不在允许列表中: {operation}")
            return {"allowed": False, "reason": f"操作不在允许列表中: {operation}", "dna": generate_dna("DENY")}

        # 操作黑名单
        if deny_list and operation in deny_list:
            self._log_access(token_id, verify_result["grantee"], operation, resource,
                             False, f"操作在拒绝列表中: {operation}")
            return {"allowed": False, "reason": f"操作在拒绝列表中: {operation}", "dna": generate_dna("DENY")}

        # 通过
        self._log_access(token_id, verify_result["grantee"], operation, resource,
                         True, "权限通过")
        return {
            "allowed": True,
            "reason": "权限通过",
            "dna": generate_dna("ALLOW"),
            "token_data": verify_result
        }

    # ============================================================
    # 4. 审计追踪
    # ============================================================

    def _log_access(self, token_id: str, grantee: str, operation: str,
                    resource: str, allowed: bool, reason: str):
        """记录访问审计 (append-only)"""
        record_id = f"AD-{int(time.time())}-{_short_hash(token_id, operation, time.time())}"
        record = DataAccessRecord(
            record_id=record_id,
            token_id=token_id,
            grantee=grantee,
            operation=operation,
            resource=resource,
            allowed=allowed,
            reason=reason
        )
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO datashare_audit
                (record_id, token_id, grantee, operation, resource, allowed, reason, timestamp, dna)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.record_id, record.token_id, record.grantee, record.operation,
                record.resource, 1 if record.allowed else 0, record.reason,
                record.timestamp, record.dna
            ))
            conn.commit()
        finally:
            conn.close()
        logger.info(f"📋 审计: {grantee} -> {operation} {resource} = {allowed}")

    # ============================================================
    # 5. 令牌管理
    # ============================================================

    def revoke_token(self, token_id: str) -> Dict:
        """撤销令牌"""
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE datashare_tokens SET status = 'revoked' WHERE token_id = ?", (token_id,))
            conn.commit()
        finally:
            conn.close()
        logger.info(f"🚫 令牌已撤销: {token_id}")
        return {"status": "revoked", "token_id": token_id}

    def list_tokens(self, owner: str = None) -> List[Dict]:
        """列出令牌"""
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if owner:
            cur.execute("SELECT * FROM datashare_tokens WHERE owner = ?", (owner,))
        else:
            cur.execute("SELECT * FROM datashare_tokens")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_audit_log(self, token_id: str = None, limit: int = 100) -> List[Dict]:
        """获取审计日志"""
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if token_id:
            cur.execute("SELECT * FROM datashare_audit WHERE token_id = ? ORDER BY timestamp DESC LIMIT ?",
                        (token_id, limit))
        else:
            cur.execute("SELECT * FROM datashare_audit ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]


# ============================================================
# 6. API 网关 (FastAPI 可选)
# ============================================================

def run_api_server(port: int = 8788, host: str = "127.0.0.1"):
    """启动 DataShare API 服务"""
    try:
        from fastapi import FastAPI, HTTPException, Request
        from fastapi.responses import JSONResponse
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        logger.error("请安装: pip install fastapi uvicorn pydantic")
        return

    app = FastAPI(title="🐉 龍魂 DataShare 权限控制", version="1.1")

    engine = DataShareEngine()

    class TokenRequest(BaseModel):
        grantee: str
        scope: List[str]
        ttl: int = 3600
        allow: List[str] = []
        deny: List[str] = []

    class AccessRequest(BaseModel):
        token: str
        operation: str
        resource: str

    @app.get("/")
    async def root():
        return {"service": "🐉 龍魂 DataShare 权限控制", "version": "1.1", "dna": generate_dna("API")}

    @app.post("/api/token/issue")
    async def issue_token(req: TokenRequest):
        token = engine.issue_token(UID, req.grantee, req.scope, req.ttl, req.allow, req.deny)
        return {"token": token.to_jwt(), "token_id": token.token_id,
                "dna": token.dna, "expires_at": token.expires_at}

    @app.post("/api/token/verify")
    async def verify_token(request: Request):
        data = await request.json()
        token_jwt = data.get("token")
        if not token_jwt:
            raise HTTPException(status_code=400, detail="缺少token")
        return JSONResponse(engine.verify_token(token_jwt))

    @app.post("/api/access/check")
    async def check_access(req: AccessRequest):
        return JSONResponse(engine.check_permission(req.token, req.operation, req.resource))

    @app.post("/api/token/revoke")
    async def revoke_token(request: Request):
        data = await request.json()
        token_id = data.get("token_id")
        if not token_id:
            raise HTTPException(status_code=400, detail="缺少token_id")
        return JSONResponse(engine.revoke_token(token_id))

    @app.get("/api/token/list")
    async def list_tokens(owner: str = None):
        return {"tokens": engine.list_tokens(owner)}

    @app.get("/api/audit")
    async def get_audit(token_id: str = None, limit: int = 100):
        return {"logs": engine.get_audit_log(token_id, limit)}

    @app.get("/api/health")
    async def health():
        return {"status": "healthy", "dna": generate_dna("HEALTH")}

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · DataShare 权限控制 API v1.1                      ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: {generate_dna('API')}
║  端口: {port}  主机: {host}
╠══════════════════════════════════════════════════════════════╣
║  POST /api/token/issue    签发令牌                          ║
║  POST /api/token/verify   验证令牌                          ║
║  POST /api/access/check   检查权限                          ║
║  POST /api/token/revoke   撤销令牌                          ║
║  GET  /api/token/list     列出令牌                          ║
║  GET  /api/audit          审计日志                          ║
║  GET  /api/health         健康检查                          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host=host, port=port)


# ============================================================
# 7. 命令行接口 (本地 Kimi/源码可直接调用)
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂 DataShare 权限控制 v1.1")
    parser.add_argument("--issue", nargs=2, metavar=("GRANTEE", "SCOPE"), help="签发令牌 (scope 逗号分隔)")
    parser.add_argument("--ttl", type=int, default=3600, help="令牌有效期秒 (默认3600)")
    parser.add_argument("--allow", type=str, default="", help="允许的操作 (逗号分隔)")
    parser.add_argument("--deny", type=str, default="", help="禁止的操作 (逗号分隔)")
    parser.add_argument("--verify", type=str, help="验证令牌")
    parser.add_argument("--check", nargs=3, metavar=("TOKEN", "OPERATION", "RESOURCE"), help="检查权限")
    parser.add_argument("--revoke", type=str, help="撤销令牌")
    parser.add_argument("--list", action="store_true", help="列出令牌")
    parser.add_argument("--audit", nargs="?", const="", default=None, help="查看审计日志 (不带值=查全部)")
    parser.add_argument("--api", action="store_true", help="启动 API 服务")
    parser.add_argument("--port", type=int, default=8788, help="API 端口")

    args = parser.parse_args()
    engine = DataShareEngine()

    if args.api:
        run_api_server(port=args.port)
        return

    if args.issue:
        grantee, scope_str = args.issue
        scope = [s.strip() for s in scope_str.split(",") if s.strip()]
        allow = [s.strip() for s in args.allow.split(",") if s.strip()] if args.allow else []
        deny = [s.strip() for s in args.deny.split(",") if s.strip()] if args.deny else []
        token = engine.issue_token(UID, grantee, scope, ttl=args.ttl, allow=allow, deny=deny)
        print("✅ 令牌签发成功")
        print(f"  Token ID: {token.token_id}")
        print(f"  JWT: {token.to_jwt()}")
        print(f"  DNA: {token.dna}")
        print(f"  有效期: {token.ttl}秒")
        return

    if args.verify:
        print(json.dumps(engine.verify_token(args.verify), indent=2, ensure_ascii=False))
        return

    if args.check:
        token, operation, resource = args.check
        print(json.dumps(engine.check_permission(token, operation, resource), indent=2, ensure_ascii=False))
        return

    if args.revoke:
        print(json.dumps(engine.revoke_token(args.revoke), indent=2, ensure_ascii=False))
        return

    if args.list:
        tokens = engine.list_tokens()
        print(f"📋 令牌列表 ({len(tokens)}个)")
        for t in tokens[:20]:
            print(f"  {t['token_id']} -> {t['grantee']} ({t['status']}) scope={t.get('scope','')[:60]}")
        return

    if args.audit is not None:
        logs = engine.get_audit_log(args.audit or None)
        print(f"📋 审计日志 ({len(logs)}条)")
        for log in logs[:20]:
            mark = "✅" if log["allowed"] else "❌"
            print(f"  {log['timestamp']} {log['grantee']} {log['operation']} {log['resource']} = {mark} {log['reason'][:40]}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
