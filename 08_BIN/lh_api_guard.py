#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·甲子·庚午·䷾既济-API-GUARD-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  龍魂·统一API守卫层 v1.0 — 一次修全部·三个根因一个模块               ║
║  DNA: #龍芯⚡️丙午·癸未·甲子·庚午·䷾既济-API-GUARD-v1.0                       ║
║  #CONFIRM🌌9622-ONLY-ONCE🧬GUARD-B8A1                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                       ║
║                                                                       ║
║  解决猎手计划43条鲲鹏API审计建议的三个根因:                            ║
║  1. 输入验证 — 统一拦截·白名单校验·注入防御                            ║
║  2. 权限控制 — 五级角色·令牌验证·细粒度                                ║
║  3. 传输加密 — HTTPS强制检测·响应头注入                                ║
║                                                                       ║
║  主权人: UID9622 💎 龍芯北辰·诸葛鑫·Lucky                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import json
import time
import hashlib
import hmac
import secrets
import logging
import threading
from typing import Any, Dict, List, Optional, Tuple, Callable
from enum import Enum
from functools import wraps
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ── 焊死常量 ──
DNA = "#龍芯⚡️丙午·癸未·甲子·庚午·䷾既济-API-GUARD-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬GUARD-B8A1"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGN_UID = "UID9622"

# ═══════════════════════════════════════════════════════
# 角色权限体系（五级·对齐第五层认证分级）
# ═══════════════════════════════════════════════════════

class Role(Enum):
    L5_SOVEREIGN = "R1"      # UID9622·全权限
    L4_SYS_ADMIN = "R2"      # P02/P03·系统管理
    L3_PERSONA_LEAD = "R3"   # P01/P06·人格组长
    L2_PERSONA_AUDIT = "R4"  # P05/P13/P15·审计
    L1_PUBLIC = "R5"         # 公开访问

    @classmethod
    def from_token_level(cls, level: int) -> "Role":
        mapping = {5: cls.L5_SOVEREIGN, 4: cls.L4_SYS_ADMIN, 3: cls.L3_PERSONA_LEAD,
                   2: cls.L2_PERSONA_AUDIT, 1: cls.L1_PUBLIC}
        return mapping.get(min(max(level, 1), 5), cls.L1_PUBLIC)

# 端点权限映射: 路径前缀 -> 最低角色要求
ENDPOINT_ACL: Dict[str, Role] = {
    "/sovereign/": Role.L5_SOVEREIGN,
    "/fuse/reset": Role.L5_SOVEREIGN,
    "/admin/": Role.L4_SYS_ADMIN,
    "/audit/": Role.L3_PERSONA_LEAD,
    "/deploy/": Role.L4_SYS_ADMIN,
    "/persona/": Role.L3_PERSONA_LEAD,
    "/metrics/": Role.L3_PERSONA_LEAD,
    "/system/": Role.L4_SYS_ADMIN,
    "/_internal/": Role.L3_PERSONA_LEAD,
}

# ═══════════════════════════════════════════════════════
# L3·统一输入验证引擎
# ═══════════════════════════════════════════════════════

# SQL注入模式
SQL_INJECTION_PATTERNS = [
    r"(?i)(union\s+select|select\s+.*\s+from|insert\s+into|drop\s+table|delete\s+from)",
    r"(?i)(--[^\n]*$|;\s*(select|drop|insert|delete|update|alter)\b)",
    r"(?i)(1\s*=\s*1|\bOR\b\s+['\"].*['\"]\s*=\s*['\"].*['\"])",
    r"(?i)(\bexec\b|\bexecute\b|\bsp_executesql\b)",
]

# 命令注入模式
CMD_INJECTION_PATTERNS = [
    r"(?i)(;\s*(cat|rm\b|wget|curl|bash|sh\b|nc\b|ncat)\s)",
    r"(?i)(\$\{.*?\}|`.*?`|\$\(.*?\))",
    r"(?i)(\b/etc/passwd\b|\b/etc/shadow\b)",
    r"(?i)(2>&1|\/dev\/null)",
]

# XSS/HTML注入模式
XSS_PATTERNS = [
    r"(?i)(<script[^>]*>.*?</script>)",
    r"(?i)(javascript\s*:|onerror\s*=|onload\s*=|onclick\s*=)",
    r"(?i)(document\.cookie|document\.location|window\.location)",
]

# 文件路径遍历
PATH_TRAVERSAL_PATTERNS = [
    r"(\.\.\/|\.\.\\|%2e%2e%2f|%2e%2e/)",
    r"(~\/\.\w+|/\.\./|\\\.\.\\)",
]

class InputValidator:
    """统一输入验证 — 零信任·白名单优先"""

    MAX_KEY_LENGTH = 256
    MAX_VALUE_LENGTH = 10000
    MAX_NESTED_DEPTH = 10
    MAX_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10MB

    # 允许的安全key字符（白名单）
    SAFE_KEY_PATTERN = re.compile(r'^[\w\-\.@:]+$')
    # 允许的安全value字符（白名单·基础）
    SAFE_VALUE_PATTERN = re.compile(r'^[\w\s\-\.@:,\!\?\(\)\[\]\{\}\'\"\/\+\=\*\%\#\&\;\<\>\~\`\^\|\u4e00-\u9fff\u3400-\u4dbf]*$')

    @classmethod
    def validate_string(cls, value: str, field_name: str = "unknown",
                        min_len: int = 0, max_len: int = MAX_VALUE_LENGTH) -> Tuple[bool, str]:
        """验证单个字符串字段"""
        if not isinstance(value, str):
            return False, f"{field_name}: expected string, got {type(value).__name__}"

        real_len = len(value.encode('utf-8'))
        if real_len < min_len:
            return False, f"{field_name}: too short ({real_len} < {min_len})"
        if real_len > max_len:
            return False, f"{field_name}: too long ({real_len} > {max_len})"

        return True, "ok"

    @classmethod
    def validate_filename(cls, value: str) -> Tuple[bool, str]:
        """验证文件名（防路径遍历）"""
        if not isinstance(value, str):
            return False, "filename must be string"

        # 禁止路径分隔符
        if any(c in value for c in ['/', '\\', '\0']):
            return False, "filename contains path separators"

        # 禁止路径遍历
        if value in ('.', '..') or value.startswith('..'):
            return False, "filename is path traversal"

        # 安全检查
        ok, msg = cls.validate_string(value, "filename", max_len=255)
        return ok, msg

    @classmethod
    def validate_id(cls, value: str, field_name: str = "id") -> Tuple[bool, str]:
        """验证ID字段（字母数字+连字符）"""
        if not isinstance(value, str):
            return False, f"{field_name}: expected string"
        if not re.match(r'^[\w\-\.]+$', value):
            return False, f"{field_name}: contains invalid characters"
        ok, msg = cls.validate_string(value, field_name, min_len=1, max_len=128)
        return ok, msg

    @classmethod
    def detect_sql_injection(cls, text: str) -> List[str]:
        """检测SQL注入"""
        found = []
        for pat in SQL_INJECTION_PATTERNS:
            if re.search(pat, text):
                found.append(pat[:50])
        return found

    @classmethod
    def detect_cmd_injection(cls, text: str) -> List[str]:
        """检测命令注入"""
        found = []
        for pat in CMD_INJECTION_PATTERNS:
            if re.search(pat, text):
                found.append(pat[:50])
        return found

    @classmethod
    def detect_xss(cls, text: str) -> List[str]:
        """检测XSS"""
        found = []
        for pat in XSS_PATTERNS:
            if re.search(pat, text):
                found.append(pat[:50])
        return found

    @classmethod
    def detect_path_traversal(cls, text: str) -> List[str]:
        """检测路径遍历"""
        found = []
        for pat in PATH_TRAVERSAL_PATTERNS:
            if re.search(pat, text):
                found.append(pat[:50])
        return found

    @classmethod
    def validate_dict_keys(cls, data: Dict, depth: int = 0) -> Tuple[bool, str]:
        """递归验证所有dict key的安全性"""
        if depth > cls.MAX_NESTED_DEPTH:
            return False, f"exceeded max nesting depth ({cls.MAX_NESTED_DEPTH})"

        for key, value in data.items():
            # key验证
            if not cls.SAFE_KEY_PATTERN.match(str(key)):
                return False, f"unsafe key: {str(key)[:50]}"
            if len(str(key).encode('utf-8')) > cls.MAX_KEY_LENGTH:
                return False, f"key too long: {str(key)[:50]}"

            # 递归验证嵌套dict
            if isinstance(value, dict):
                ok, msg = cls.validate_dict_keys(value, depth + 1)
                if not ok:
                    return False, msg
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        ok, msg = cls.validate_dict_keys(item, depth + 1)
                        if not ok:
                            return False, msg

        return True, "ok"

    @classmethod
    def full_scan(cls, data: Any) -> Tuple[bool, str, Dict[str, Any]]:
        """
        完整输入扫描管线
        返回: (是否放行, 原因, 审计详情)
        """
        audit_detail = {"checks": [], "timestamp": datetime.now(timezone.utc).isoformat()}

        # 1. 序列化为字符串做注入检测
        content = json.dumps(data, ensure_ascii=False) if isinstance(data, (dict, list)) else str(data)

        # 2. SQL注入检测
        sql_hits = cls.detect_sql_injection(content)
        if sql_hits:
            audit_detail["checks"].append({"type": "sql_injection", "hits": sql_hits})
            return False, f"SQL injection detected: {sql_hits[0][:60]}", audit_detail

        # 3. 命令注入检测
        cmd_hits = cls.detect_cmd_injection(content)
        if cmd_hits:
            audit_detail["checks"].append({"type": "cmd_injection", "hits": cmd_hits})
            return False, f"Command injection detected: {cmd_hits[0][:60]}", audit_detail

        # 4. XSS检测
        xss_hits = cls.detect_xss(content)
        if xss_hits:
            audit_detail["checks"].append({"type": "xss", "hits": xss_hits})
            return False, f"XSS detected: {xss_hits[0][:60]}", audit_detail

        # 5. 路径遍历检测
        path_hits = cls.detect_path_traversal(content)
        if path_hits:
            audit_detail["checks"].append({"type": "path_traversal", "hits": path_hits})
            return False, f"Path traversal detected: {path_hits[0][:60]}", audit_detail

        # 6. 载荷大小
        payload_size = len(content.encode('utf-8'))
        if payload_size > cls.MAX_PAYLOAD_SIZE:
            return False, f"Payload too large ({payload_size} > {cls.MAX_PAYLOAD_SIZE})", audit_detail

        # 7. Dict key验证
        if isinstance(data, dict):
            ok, msg = cls.validate_dict_keys(data)
            if not ok:
                audit_detail["checks"].append({"type": "key_validation", "error": msg})
                return False, msg, audit_detail

        audit_detail["checks"].append({"type": "all_clear", "payload_size": payload_size})
        return True, "ok", audit_detail

    @classmethod
    def sanitize_path_param(cls, value: str) -> str:
        """净化路径参数"""
        if not value:
            return ""
        # 只保留安全字符
        return re.sub(r'[^\w\-\.@:]', '', value)


# ═══════════════════════════════════════════════════════
# L2·权限控制引擎
# ═══════════════════════════════════════════════════════

class TokenManager:
    """主权令牌管理"""

    # 令牌 -> (角色, 过期时间, 签发者)
    _tokens: Dict[str, Tuple[Role, float, str]] = {}
    _lock = threading.Lock()
    TOKEN_TTL = 3600 * 24  # 24小时

    @classmethod
    def _derive_token(cls, secret: str, salt: str) -> str:
        """派生主权令牌"""
        return hashlib.sha256(f"{secret}:{salt}:{GPG_FINGERPRINT}".encode()).hexdigest()[:32]

    @classmethod
    def issue_token(cls, role: Role, issuer: str = "gateway") -> str:
        """签发令牌"""
        salt = secrets.token_hex(8)
        token = cls._derive_token(CONFIRM, salt)
        with cls._lock:
            cls._tokens[token] = (role, time.time() + cls.TOKEN_TTL, issuer)
        return token

    @classmethod
    def validate_token(cls, token: str) -> Tuple[bool, Optional[Role], str]:
        """验证令牌"""
        with cls._lock:
            if token not in cls._tokens:
                return False, None, "invalid token"

            role, expiry, issuer = cls._tokens[token]
            if time.time() > expiry:
                del cls._tokens[token]
                return False, None, "token expired"

            return True, role, issuer

    @classmethod
    def revoke_token(cls, token: str) -> bool:
        """吊销令牌"""
        with cls._lock:
            if token in cls._tokens:
                del cls._tokens[token]
                return True
            return False

    @classmethod
    def cleanup_expired(cls):
        """清理过期令牌"""
        now = time.time()
        with cls._lock:
            expired = [t for t, (r, e, _) in cls._tokens.items() if now > e]
            for t in expired:
                del cls._tokens[t]

    @classmethod
    def stats(cls) -> Dict[str, Any]:
        with cls._lock:
            return {
                "active_tokens": len(cls._tokens),
                "tokens": [{"role": r.name, "issuer": i, "expires_in": int(e - time.time())}
                          for _, (r, e, i) in list(cls._tokens.items())[:10]]
            }


class AccessController:
    """细粒度权限控制"""

    @classmethod
    def check_endpoint_access(cls, path: str, role: Role) -> Tuple[bool, str]:
        """检查端点权限"""
        # 默认公开端点放行
        required = Role.L1_PUBLIC

        for prefix, req_role in ENDPOINT_ACL.items():
            if path.startswith(prefix) or path == prefix.rstrip('/'):
                required = req_role
                break

        # 角色值越小权限越高 (R1=5 > R5=1)
        role_levels = {Role.L5_SOVEREIGN: 5, Role.L4_SYS_ADMIN: 4,
                       Role.L3_PERSONA_LEAD: 3, Role.L2_PERSONA_AUDIT: 2, Role.L1_PUBLIC: 1}
        if role_levels[role] < role_levels[required]:
            return False, f"insufficient role: {role.name} < required {required.name}"

        return True, "ok"

    @classmethod
    def extract_auth(cls, headers: Dict, cookies: Dict, query_params: Dict) -> Optional[str]:
        """从请求中提取认证令牌"""
        # 1. Authorization header (Bearer)
        auth = headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()

        # 2. X-LongHun-Token header
        token = headers.get("x-longhun-token", "").strip()
        if token:
            return token

        # 3. Cookie
        token = cookies.get("lh_token", "").strip()
        if token:
            return token

        # 4. Query parameter (仅用于GET请求·安全降级)
        token = query_params.get("token", "").strip()
        if token:
            return token

        return None


# ═══════════════════════════════════════════════════════
# HTTPS强制检测
# ═══════════════════════════════════════════════════════

class TransportSecurity:
    """传输安全检测"""

    # 允许跳过HTTPS检测的路径（内网健康检查等）
    HTTPS_SKIP_PATHS = {"/health", "/healthz", "/_internal/heartbeat", "/ws/"}

    @classmethod
    def check_https(cls, request_scheme: str, request_path: str,
                    forwarded_proto: Optional[str] = None) -> Tuple[bool, str]:
        """
        检查是否HTTPS
        - 允许代理头 X-Forwarded-Proto
        - 内网健康检查路径豁免
        """
        # 豁免路径
        for skip in cls.HTTPS_SKIP_PATHS:
            if request_path.startswith(skip):
                return True, "exempted"

        # 检查代理头
        if forwarded_proto and forwarded_proto.lower() == "https":
            return True, "HTTPS via proxy"

        # 直接HTTPS
        if request_scheme.lower() == "https":
            return True, "direct HTTPS"

        return False, f"HTTPS required, got {request_scheme}"

    @classmethod
    def security_headers(cls) -> Dict[str, str]:
        """返回安全响应头"""
        return {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
            "X-LongHun-DNA": "longhun-api-guard-v1.0",
            "X-LongHun-Sovereign": SOVEREIGN_UID,
            "X-LongHun-GPG": GPG_FINGERPRINT[:16],
        }


# ═══════════════════════════════════════════════════════
# FastAPI 守卫装饰器
# ═══════════════════════════════════════════════════════

logger = logging.getLogger("lh_api_guard")

# 审计日志
AUDIT_DIR = Path(os.environ.get("LONGHUN_LOG_DIR", Path.home() / ".longhun" / "logs"))
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = AUDIT_DIR / "api_guard_audit.jsonl"

def _write_audit(level: str, event: str, detail: Dict):
    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "level": level, "event": event, "detail": detail, "dna": DNA
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ════════════════════════════════════════════════════════════════
# 入链前置网关 · 四重守护（P72 龍盾 · 2026-08-25 全员议事会 v2.0 落地）
# 外部内容（社区讨论/拉取/API入站）进系统前强制过四重守护：
#   ①毒内容熔断 → ②数据主权闸 → ③一票否决词 → ④DNA来源追溯
# ════════════════════════════════════════════════════════════════

# ① 毒内容模式（恶意代码/诱导上传/隐私窃取）
TOXIC_PATTERNS = [
    r"(?i)(eval\(|exec\(|os\.system\(|subprocess\.|rm\s+-rf\s+/)",
    r"(?i)(curl\s+.*\|\s*(ba)?sh|wget\s+.*\|\s*(ba)?sh)",
    r"(?i)(上传.*(身份证|银行卡|密码|验证码)|诱导.*上传)",
    r"(?i)(抓取.*(cookie|token|session)|窃取.*(密码|数据|隐私))",
]

# ② 数据主权红线（众包/用户行为分析类方法论——碰 P0 数据主权，一律拒收）
SOVEREIGN_BLOCK_PATTERNS = [
    r"众包", r"用户行为分析", r"行为追踪", r"数据收集.*(默认|自动)",
    r"(crowdsourc\w*|behavioral analysis|user analytics|behavior tracking)",
]

# ③ 一票否决词（第十层 · 绕协议借口，出现即强制审计）
VETO_WORDS = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]


class InboundGuard:
    """入链前置网关 · 四重守护（P72 龍盾 · 内容治理层）

    区别于 InputValidator（技术注入检测），本闸管的是「内容治理」：
    社区方法论/外部讨论/API 入站内容，吸收前必须过四重守护。
    铁律: 审核不严不入链 · 每条入链留 DNA 审计痕迹。
    """
    DNA = "#龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-INBOUND-GUARD-v1.0-UID9622"
    _stats = {"passed": 0, "blocked": 0, "last": None}

    @classmethod
    def stats(cls) -> Dict:
        return dict(cls._stats)

    @classmethod
    def gate_inbound(cls, content: str, source: str = "") -> Tuple[bool, str, Dict]:
        """四重守护总闸。返回 (是否放行, 原因, 审计详情)。"""
        audit = {
            "checks": [], "source": source, "dna": cls.DNA,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        text = content or ""

        # Gate1 毒内容熔断
        for pat in TOXIC_PATTERNS:
            if re.search(pat, text):
                hit = pat[:60]
                audit["checks"].append({"gate": 1, "type": "toxic_content", "hit": hit})
                cls._blocked(audit)
                return False, f"Gate1 毒内容熔断: {hit}", audit

        # Gate2 数据主权闸（众包/行为分析 = 碰 P0 数据主权红线）
        for pat in SOVEREIGN_BLOCK_PATTERNS:
            if re.search(pat, text):
                hit = pat[:60]
                audit["checks"].append({"gate": 2, "type": "sovereign_block", "hit": hit})
                cls._blocked(audit)
                return False, f"Gate2 数据主权闸(拒收): {hit}", audit

        # Gate3 一票否决词（第十层 · 出现即 P05 强制审计）
        for word in VETO_WORDS:
            if word in text:
                audit["checks"].append({"gate": 3, "type": "veto_word", "hit": word})
                cls._blocked(audit)
                return False, f"Gate3 一票否决词: {word}", audit

        # Gate4 DNA 来源追溯（要求来源标识 · 记录来源哈希，来源链不可切断）
        has_source = bool(source and source.strip())
        source_hash = hashlib.sha256(f"{text}|{source}".encode()).hexdigest()[:16]
        audit["checks"].append({
            "gate": 4, "type": "dna_trace",
            "has_source": has_source, "source": source or "(无来源标识·🟡待补)",
            "source_hash": source_hash,
        })
        audit["checks"].append({"type": "all_gates_pass"})
        cls._stats["passed"] += 1
        cls._stats["last"] = audit["timestamp"]
        _write_audit("PASS", "inbound_gate", audit)
        return True, f"四重守护全部通过 source_hash={source_hash}", audit

    @classmethod
    def _blocked(cls, audit: Dict) -> None:
        cls._stats["blocked"] += 1
        cls._stats["last"] = audit["timestamp"]
        _write_audit("BLOCK", "inbound_gate", audit)


def guarded(min_role: Role = Role.L1_PUBLIC, require_https: bool = True):
    """
    FastAPI 端点守卫装饰器
    用法:
        @app.post("/api/data")
        @guarded(min_role=Role.L3_PERSONA_LEAD)
        async def my_endpoint(request: Request, ...):
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 尝试从参数中提取 Request 对象
            from fastapi import Request, HTTPException
            from fastapi.responses import JSONResponse

            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if request is None:
                for v in kwargs.values():
                    if isinstance(v, Request):
                        request = v
                        break

            if request is None:
                logger.warning("Guard: no Request object found, skipping security checks")
                return await func(*args, **kwargs)

            path = request.url.path
            client_ip = request.client.host if request.client else "unknown"
            scheme = request.url.scheme or "http"

            # ── 1. 传输加密检查 ──
            if require_https:
                forwarded = request.headers.get("x-forwarded-proto", "")
                https_ok, https_msg = TransportSecurity.check_https(scheme, path, forwarded)
                if not https_ok:
                    _write_audit("RED", "HTTPS_REQUIRED", {"path": path, "ip": client_ip, "scheme": scheme})
                    return JSONResponse(status_code=403, content={
                        "error": "HTTPS required", "message": https_msg, "dna": DNA
                    })

            # ── 2. 权限认证 ──
            auth_header = dict(request.headers)
            cookies = dict(request.cookies)
            query_params = dict(request.query_params)

            token = AccessController.extract_auth(auth_header, cookies, query_params)
            role = Role.L1_PUBLIC  # 默认游客

            if min_role != Role.L1_PUBLIC:
                if not token:
                    _write_audit("RED", "AUTH_MISSING", {"path": path, "ip": client_ip, "required_role": min_role.name})
                    return JSONResponse(status_code=401, content={
                        "error": "Authentication required", "dna": DNA
                    })

                valid, token_role, issuer = TokenManager.validate_token(token)
                if not valid:
                    _write_audit("RED", "AUTH_INVALID", {"path": path, "ip": client_ip, "reason": token_role or "invalid"})
                    return JSONResponse(status_code=401, content={
                        "error": "Invalid or expired token", "dna": DNA
                    })
                role = token_role

                access_ok, access_msg = AccessController.check_endpoint_access(path, role)
                if not access_ok:
                    _write_audit("RED", "ACCESS_DENIED", {"path": path, "ip": client_ip, "role": role.name, "required": min_role.name})
                    return JSONResponse(status_code=403, content={
                        "error": "Insufficient permissions",
                        "required": min_role.name, "current": role.name, "dna": DNA
                    })

            # ── 3. 输入验证 ──
            if request.method in ("POST", "PUT", "PATCH"):
                try:
                    body_bytes = await request.body()
                    if body_bytes:
                        body_text = body_bytes.decode("utf-8", errors="ignore")
                        try:
                            body_data = json.loads(body_text)
                        except json.JSONDecodeError:
                            body_data = body_text

                        valid, msg, audit_detail = InputValidator.full_scan(body_data)
                        if not valid:
                            _write_audit("RED", "INPUT_REJECTED", {
                                "path": path, "ip": client_ip, "reason": msg
                            })
                            return JSONResponse(status_code=422, content={
                                "error": "Input validation failed",
                                "message": msg, "dna": DNA
                            })
                except Exception as e:
                    logger.warning(f"Input scan error: {e}")

            # ── 放行 ──
            _write_audit("GREEN", "GUARD_PASS", {
                "path": path, "ip": client_ip, "role": role.name, "method": request.method
            })

            # 注入安全头到响应
            response = await func(*args, **kwargs)
            if hasattr(response, 'headers'):
                for k, v in TransportSecurity.security_headers().items():
                    response.headers[k] = v
            return response

        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════
# 自测
# ═══════════════════════════════════════════════════════

def self_test():
    """模块自测·不需启动服务器"""
    results = []
    print("🧪 龍魂·统一API守卫层 v1.0 自测")

    # 1. InputValidator
    print("\n── L3·输入验证 ──")
    # SQL注入
    ok, msg, _ = InputValidator.full_scan({"q": "1' OR '1'='1"})
    assert not ok, f"SQL注入应被拦截: {msg}"
    results.append(("SQL注入检测", True))

    ok, msg, _ = InputValidator.full_scan({"name": "hello"})
    assert ok, f"正常输入应通过: {msg}"
    results.append(("正常输入", True))

    # 命令注入
    ok, msg, _ = InputValidator.full_scan({"cmd": "; cat /etc/passwd"})
    assert not ok, f"命令注入应被拦截: {msg}"
    results.append(("命令注入检测", True))

    # XSS
    ok, msg, _ = InputValidator.full_scan({"html": "<script>alert(1)</script>"})
    assert not ok, f"XSS应被拦截: {msg}"
    results.append(("XSS检测", True))

    # 路径遍历
    ok, msg, _ = InputValidator.full_scan({"file": "../../etc/passwd"})
    assert not ok, f"路径遍历应被拦截: {msg}"
    results.append(("路径遍历检测", True))

    # 文件名验证
    ok, msg = InputValidator.validate_filename("normal_file.txt")
    assert ok, results.append(("文件名验证·正常", True))

    ok, msg = InputValidator.validate_filename("../etc/passwd")
    assert not ok, results.append(("文件名验证·拒绝", True))

    # 2. TokenManager
    print("\n── L2·权限控制 ──")
    token = TokenManager.issue_token(Role.L4_SYS_ADMIN)
    assert token and len(token) == 32, "令牌应为32字符hex"
    results.append(("令牌签发", True))

    valid, role, issuer = TokenManager.validate_token(token)
    assert valid and role == Role.L4_SYS_ADMIN, f"令牌验证失败: role={role}"
    results.append(("令牌验证", True))

    TokenManager.revoke_token(token)
    valid, role, _ = TokenManager.validate_token(token)
    assert not valid, "已吊销令牌不应有效"
    results.append(("令牌吊销", True))

    # 3. AccessController
    print("\n── 端点权限 ──")
    ok, msg = AccessController.check_endpoint_access("/health", Role.L1_PUBLIC)
    assert ok, results.append(("公开端点·放行", True))

    ok, msg = AccessController.check_endpoint_access("/sovereign/secrets", Role.L1_PUBLIC)
    assert not ok, results.append(("主权端点·拒绝游客", True))

    ok, msg = AccessController.check_endpoint_access("/sovereign/secrets", Role.L5_SOVEREIGN)
    assert ok, results.append(("主权端点·放行R1", True))

    # 4. TransportSecurity
    print("\n── 传输安全 ──")
    ok, msg = TransportSecurity.check_https("http", "/api/data")
    assert not ok, results.append(("HTTP拒绝", True))

    ok, msg = TransportSecurity.check_https("https", "/api/data")
    assert ok, results.append(("HTTPS通过", True))

    ok, msg = TransportSecurity.check_https("http", "/api/data", "https")
    assert ok, results.append(("代理HTTPS通过", True))

    ok, msg = TransportSecurity.check_https("http", "/health")
    assert ok, results.append(("健康检查豁免", True))

    # 汇总
    passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\n{'='*50}")
    print(f"🏆 自测结果: {passed}/{total} 通过")
    for name, ok in results:
        print(f"  {'✅' if ok else '❌'} {name}")
    return passed == total


if __name__ == "__main__":
    success = self_test()
    sys.exit(0 if success else 1)
